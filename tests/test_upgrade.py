"""Upgrade, preservation, and conflict scenarios U01-U05 (T16)."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import support

POLICY = ".ai-docs/policy.md"


def add_upstream_policy_section(template: Path) -> None:
    policy = template / "template" / POLICY
    policy.write_text(
        policy.read_text()
        + "\n## Upstream v0.1.1 additions\n\n"
        + "This managed section arrives through a versioned Copier update.\n"
    )


def make_template_pair(root: Path, mutate=None) -> Path:
    """Snapshot v0.1.0, apply a controlled managed change, and tag v0.1.1."""
    template = support.snapshot_template(Path(root) / "template source")
    (mutate or add_upstream_policy_section)(template)
    support.commit_all(template, "ai-docs-kit v0.1.1")
    support.tag(template, "v0.1.1")
    return template


class UpgradeTest(unittest.TestCase):
    def setUp(self):
        self._temporary = tempfile.TemporaryDirectory(prefix="ai-docs-kit-upgrade-")
        self.root = Path(self._temporary.name)

    def tearDown(self):
        self._temporary.cleanup()

    def installed_consumer(self, template: Path, name: str = "consumer") -> Path:
        project = self.root / name
        support.init_repo(project)
        support.render_project(template, project, project_name="Upgrade project")
        support.commit_all(project, "install v0.1.0")
        return project

    def test_u01_clean_upgrade_changes_managed_policy_and_keeps_identity(self):
        template = make_template_pair(self.root)
        project = self.installed_consumer(template)
        before_answers = (project / support.ANSWERS_FILE).read_text()

        support.update_project(project, ref="v0.1.1")

        policy = (project / POLICY).read_text()
        self.assertIn("## Upstream v0.1.1 additions", policy)
        after_answers = (project / support.ANSWERS_FILE).read_text()
        self.assertIn("docs_dir: docs/ai-docs", after_answers)
        self.assertIn("project_name: Upgrade project", after_answers)
        self.assertIn("v0.1.1", after_answers)
        self.assertNotEqual(before_answers, after_answers)
        self.assertEqual(support.conflict_files(project), [])

        support.commit_all(project, "upgrade to v0.1.1")
        support.run_checks(project)

    def test_u02_non_conflicting_consumer_edit_survives(self):
        template = make_template_pair(self.root)
        project = self.installed_consumer(template)

        policy = project / POLICY
        text = policy.read_text()
        marker = "## Writing rules"
        self.assertIn(marker, text)
        edited = text.replace(
            marker,
            "## Local review note\n\nCONSUMER LOCAL EDIT preserved across updates.\n\n"
            + marker,
            1,
        )
        self.assertNotEqual(edited, text)
        policy.write_text(edited)
        support.commit_all(project, "consumer policy edit")

        support.update_project(project, ref="v0.1.1")

        updated = policy.read_text()
        self.assertIn("CONSUMER LOCAL EDIT preserved across updates.", updated)
        self.assertIn("## Upstream v0.1.1 additions", updated)
        self.assertEqual(support.conflict_files(project), [])


    def test_u03_overlapping_edits_remain_visible(self):
        sentence = "without an authorized, reviewed change."

        def upstream_overlap(template: Path) -> None:
            policy = template / "template" / POLICY
            text = policy.read_text()
            self.assertIn(sentence, text)
            policy.write_text(
                text.replace(
                    sentence,
                    "only after an upstream-approved reorganization.\nUPSTREAM-V011",
                )
            )

        template = make_template_pair(self.root, upstream_overlap)
        project = self.installed_consumer(template)

        policy = project / POLICY
        text = policy.read_text()
        self.assertIn(sentence, text)
        policy.write_text(
            text.replace(
                sentence,
                "only after a consumer-approved reorganization.\nCONSUMER-EDIT",
            )
        )
        support.commit_all(project, "consumer overlapping edit")

        result = support.update_project(project, ref="v0.1.1", check=False)

        # Copier can exit zero while leaving conflicts in the working tree; readiness
        # must be derived from conflict state, not from the exit code alone.
        conflicts = support.conflict_files(project)
        unmerged = support.unmerged_paths(project)
        combined = result.stdout + result.stderr
        self.assertTrue(
            conflicts or unmerged or result.returncode != 0,
            "overlapping edits must leave a visible conflict or a failed update\n"
            + combined,
        )
        self.assertTrue(
            any("policy.md" in path for path in conflicts + unmerged)
            or "policy.md" in combined,
        )

    def test_u04_seed_edits_persist_and_deleted_seed_is_recreated(self):
        template = make_template_pair(self.root)
        project = self.installed_consumer(template)

        context = project / ".ai-docs/project.md"
        context.write_text(context.read_text() + "\nCONSUMER CONTEXT EDIT\n")
        index = project / "docs/ai-docs/README.md"
        index.write_text(index.read_text() + "\nCONSUMER INDEX EDIT\n")
        support.commit_all(project, "seed edits")

        missing = project / "docs/ai-docs/how-to/update-documentation.md"
        missing.unlink()
        support.commit_all(project, "delete shipped seed")

        support.update_project(project, ref="v0.1.1")

        self.assertIn("CONSUMER CONTEXT EDIT", context.read_text())
        self.assertIn("CONSUMER INDEX EDIT", index.read_text())
        self.assertTrue(
            missing.is_file(),
            "a deleted shipped seed is recreated by update, as documented",
        )

    def test_u05_dirty_destination_is_rejected_without_discarding_changes(self):
        template = make_template_pair(self.root)
        project = self.installed_consumer(template)

        index = project / "docs/ai-docs/README.md"
        dirty_text = index.read_text() + "\nUNCOMMITTED USER CHANGE\n"
        index.write_text(dirty_text)

        result = support.update_project(project, ref="v0.1.1", check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("dirty", (result.stdout + result.stderr).lower())
        self.assertEqual(index.read_text(), dirty_text)


if __name__ == "__main__":
    unittest.main()
