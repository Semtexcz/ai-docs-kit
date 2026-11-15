"""Independent template composition scenarios C01-C03 (T15)."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import support

FOREIGN_ANSWERS = ".copier-answers.foreign.yml"
FOREIGN_OWNED = (
    FOREIGN_ANSWERS,
    ".foreign-notes.md",
    ".foreign-state/marker.txt",
    "foreign/README.md",
    "foreign/config.txt",
)
ROOT_SENTINELS = (
    "README.md",
    "AGENTS.md",
    ".pre-commit-config.yaml",
    ".markdownlint-cli2.jsonc",
    "lychee.toml",
    ".github/workflows/ci.yml",
    ".claude/settings.json",
)


def snapshot_foreign_template(destination) -> Path:
    source = support.copy_fixture("foreign_template", Path(destination))
    support.init_repo(source)
    support.commit_all(source, "foreign template v1.0.0")
    support.tag(source, "v1.0.0")
    return source


def install_foreign(source, project, ref="v1.0.0"):
    return support.run(
        [
            support.require_tool("copier"),
            "copy",
            "--defaults",
            "--vcs-ref",
            ref,
            "--answers-file",
            FOREIGN_ANSWERS,
            str(source),
            ".",
        ],
        cwd=Path(project),
        timeout=600,
    )


def update_foreign(project, ref="v1.0.1"):
    return support.run(
        [
            support.require_tool("copier"),
            "update",
            "--defaults",
            "--vcs-ref",
            ref,
            "--answers-file",
            FOREIGN_ANSWERS,
        ],
        cwd=Path(project),
        timeout=600,
    )


class CompositionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temporary = tempfile.TemporaryDirectory(prefix="ai-docs-kit-compose-")
        root = Path(cls._temporary.name)
        cls.template = support.snapshot_template(root / "ai-docs-kit")
        cls.foreign = snapshot_foreign_template(root / "foreign-template")

    @classmethod
    def tearDownClass(cls):
        cls._temporary.cleanup()

    def new_consumer(self, parent: Path, name: str) -> Path:
        project = parent / name
        support.copy_fixture("existing_project", project)
        support.init_repo(project)
        support.commit_all(project, "existing consumer")
        return project

    def assert_kit_owned(self, project):
        for path in support.EXPECTED_CONSUMER_INVENTORY:
            self.assertTrue((project / path).is_file(), path)

    def test_c01_both_install_orders_preserve_each_other(self):
        with tempfile.TemporaryDirectory(prefix="ai-docs-kit-order-a-") as tmp:
            project = self.new_consumer(Path(tmp), "kit-first")
            root_before = support.file_hashes(project, ROOT_SENTINELS)

            support.render_project(self.template, project, project_name="Kit first")
            kit_hashes = support.file_hashes(project, support.EXPECTED_CONSUMER_INVENTORY)

            install_foreign(self.foreign, project)

            self.assert_kit_owned(project)
            self.assertEqual(
                support.file_hashes(project, support.EXPECTED_CONSUMER_INVENTORY),
                kit_hashes,
                "installing the foreign template must not change kit files",
            )
            for path in FOREIGN_OWNED:
                self.assertTrue((project / path).is_file(), path)
            self.assertEqual(
                support.file_hashes(project, ROOT_SENTINELS),
                root_before,
                "shared root files must stay byte-identical",
            )

        with tempfile.TemporaryDirectory(prefix="ai-docs-kit-order-b-") as tmp:
            project = self.new_consumer(Path(tmp), "foreign-first")
            install_foreign(self.foreign, project)
            foreign_hashes = support.file_hashes(project, FOREIGN_OWNED)

            support.render_project(self.template, project, project_name="Foreign first")

            self.assert_kit_owned(project)
            self.assertEqual(
                support.file_hashes(project, FOREIGN_OWNED),
                foreign_hashes,
                "installing ai-docs-kit must not change foreign files",
            )

    def test_c02_updates_stay_independent(self):
        with tempfile.TemporaryDirectory(prefix="ai-docs-kit-updates-") as tmp:
            project = self.new_consumer(Path(tmp), "consumer")
            support.render_project(self.template, project, project_name="Updates")
            install_foreign(self.foreign, project)
            support.commit_all(project, "both templates installed")

            # A controlled managed change in each template, tagged separately.
            foreign_change = self.foreign / "template/foreign/config.txt"
            foreign_change.write_text(
                foreign_change.read_text() + "foreign upstream v1.0.1\n"
            )
            support.commit_all(self.foreign, "foreign v1.0.1")
            support.tag(self.foreign, "v1.0.1")

            kit_change = self.template / "template/.ai-docs/policy.md"
            kit_change.write_text(kit_change.read_text() + "\nUpstream policy note.\n")
            support.commit_all(self.template, "kit v0.1.1")
            support.tag(self.template, "v0.1.1")

            kit_hashes = support.file_hashes(project, support.EXPECTED_CONSUMER_INVENTORY)

            update_foreign(project)

            self.assertIn(
                "foreign upstream v1.0.1",
                (project / "foreign/config.txt").read_text(),
            )
            self.assertEqual(
                support.file_hashes(project, support.EXPECTED_CONSUMER_INVENTORY),
                kit_hashes,
                "updating the foreign template must not change kit files",
            )
            support.commit_all(project, "foreign update")

            foreign_hashes = support.file_hashes(project, FOREIGN_OWNED)

            support.update_project(project, ref="v0.1.1")

            self.assertIn(
                "Upstream policy note.",
                (project / ".ai-docs/policy.md").read_text(),
            )
            self.assertEqual(
                support.file_hashes(project, FOREIGN_OWNED),
                foreign_hashes,
                "updating ai-docs-kit must not change foreign files",
            )
            self.assertEqual(support.conflict_files(project), [])

    def test_c03_declining_collision_preserves_sentinel(self):
        with tempfile.TemporaryDirectory(prefix="ai-docs-kit-collision-") as tmp:
            project = Path(tmp) / "consumer"
            support.init_repo(project)
            collision = support.copy_fixture(
                "collision_template", Path(tmp) / "collision-template"
            )
            support.init_repo(collision)
            support.commit_all(collision, "collision template")
            support.tag(collision, "v1.0.0")
            support.run(
                [
                    support.require_tool("copier"),
                    "copy",
                    "--defaults",
                    "--vcs-ref",
                    "v1.0.0",
                    "--answers-file",
                    ".copier-answers.collision.yml",
                    str(collision),
                    ".",
                ],
                cwd=project,
            )
            sentinel = (project / ".ai-docs/policy.md").read_bytes()

            result = support.render_project(
                self.template,
                project,
                project_name="Collision",
                check=False,
                stdin_text="n\nn\nn\n",
            )

            self.assertEqual(
                (project / ".ai-docs/policy.md").read_bytes(),
                sentinel,
                "declining the native overwrite prompt must preserve sentinel bytes",
            )
            # No rollback is promised. A declined collision either fails visibly or
            # skips the file; it must never report a silent overwrite as success.
            combined = result.stdout + result.stderr
            self.assertTrue(
                result.returncode != 0
                or "conflict" in combined.lower()
                or "skip" in combined.lower(),
                combined,
            )


if __name__ == "__main__":
    unittest.main()
