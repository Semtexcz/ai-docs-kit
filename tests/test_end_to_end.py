"""End-to-end MVP installation acceptance scenario E01 (T21).

One executable scenario over real tools and disposable repositories:
existing consumer + foreign template -> install -> evidence-backed docs -> validation
failure/repair -> tagged upgrade -> final checks, with byte-preservation assertions.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import support

KIT_INVENTORY = set(support.EXPECTED_CONSUMER_INVENTORY)
FOREIGN_FILES = (
    ".copier-answers.foreign.yml",
    ".foreign-notes.md",
    ".foreign-state/marker.txt",
    "foreign/README.md",
    "foreign/config.txt",
)
ROOT_SENTINELS = (
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    ".pre-commit-config.yaml",
    ".markdownlint-cli2.jsonc",
    "lychee.toml",
    ".gitignore",
    "package.json",
    "pyproject.toml",
    "docs/guide.md",
    ".github/workflows/ci.yml",
    ".claude/settings.json",
)
EVIDENCE_FILE = "app/config.json"
EVIDENCE_PAGE = "docs/ai-docs/how-to/configure-refresh.md"


class EndToEndTest(unittest.TestCase):
    def test_e01_existing_consumer_lifecycle(self):
        with tempfile.TemporaryDirectory(
            prefix="ai docs kit e01 "
        ) as temporary_directory:
            root = Path(temporary_directory)
            self.assertIn(" ", temporary_directory)

            # 1. Tagged toolkit snapshot and an independent foreign template.
            template = support.snapshot_template(root / "toolkit source")
            foreign = support.copy_fixture("foreign_template", root / "foreign source")
            support.init_repo(foreign)
            support.commit_all(foreign, "foreign template v1.0.0")
            support.tag(foreign, "v1.0.0")

            # 2. Committed existing consumer with foreign artifacts already present.
            consumer = root / "consumer project"
            support.copy_fixture("existing_project", consumer)
            support.init_repo(consumer)
            support.run(
                [
                    support.require_tool("copier"),
                    "copy",
                    "--defaults",
                    "--vcs-ref",
                    "v1.0.0",
                    "--answers-file",
                    ".copier-answers.foreign.yml",
                    str(foreign),
                    ".",
                ],
                cwd=consumer,
            )
            support.commit_all(consumer, "existing project with foreign template")
            owned_files = ROOT_SENTINELS + FOREIGN_FILES
            owned_before = support.file_hashes(consumer, owned_files)

            # 3. Reserved paths absent; install without trust or force flags.
            self.assertFalse((consumer / ".ai-docs").exists())
            self.assertFalse((consumer / support.ANSWERS_FILE).exists())
            support.render_project(
                template,
                consumer,
                docs_dir="docs/ai-docs",
                project_name="E01 consumer",
                ref="v0.1.0",
            )

            # 4. Inventory, answers, preservation, and absence of activation.
            files = set(support.inventory(consumer))
            self.assertTrue(KIT_INVENTORY <= files, sorted(KIT_INVENTORY - files))
            kit_only = {
                item
                for item in files
                if item.startswith((".ai-docs/", "docs/ai-docs/"))
                or item == support.ANSWERS_FILE
            }
            self.assertEqual(kit_only, KIT_INVENTORY)
            answers = (consumer / support.ANSWERS_FILE).read_text()
            self.assertIn("_src_path:", answers)
            self.assertIn("_commit: v0.1.0", answers)
            self.assertIn("docs_dir: docs/ai-docs", answers)
            self.assertEqual(
                support.file_hashes(consumer, owned_files),
                owned_before,
                "shared root and foreign files must be byte-identical",
            )
            self.assertFalse((consumer / ".git/hooks/pre-commit").exists())
            self.assertFalse(
                any(
                    path.startswith(
                        (".github/workflows/ai-docs", ".agents/", ".claude/skills/")
                    )
                    for path in files
                )
            )


            # Read entry point -> index -> catalog -> selected skill.
            budgets = {
                ".ai-docs/README.md": 100,
                ".ai-docs/skills/README.md": 80,
                ".ai-docs/project.md": 150,
                "docs/ai-docs/README.md": 150,
            }
            for path, limit in budgets.items():
                self.assertLessEqual(
                    len((consumer / path).read_text().splitlines()), limit, path
                )
            catalog = (consumer / ".ai-docs/skills/README.md").read_text()
            for skill in ("docs-discover", "docs-write", "docs-review"):
                self.assertIn(f"`{skill}`", catalog)
                skill_file = consumer / f".ai-docs/skills/{skill}/SKILL.md"
                self.assertTrue(skill_file.is_file())
                self.assertLessEqual(len(skill_file.read_text().splitlines()), 300)

            support.commit_all(consumer, "install ai-docs-kit v0.1.0")

            # 5. A tiny real evidence fixture plus an evidence-backed page and route.
            support.write(
                consumer / EVIDENCE_FILE, '{\n  "refresh_interval_minutes": 15\n}\n'
            )
            support.write(
                consumer / EVIDENCE_PAGE,
                "# Configure the refresh interval\n\n"
                "Audience: operators configuring the example service.\n\n"
                "## Current behavior\n\n"
                "The shipped example configuration sets the refresh interval to 15 minutes\n"
                f"([{EVIDENCE_FILE}](../../../{EVIDENCE_FILE})).\n\n"
                "## Verification\n\n"
                "The value above is read from the configuration file in this repository at\n"
                "the revision under review. No runtime execution was performed for this page.\n\n"
                "## Sources\n\n"
                f"- [{EVIDENCE_FILE}](../../../{EVIDENCE_FILE})\n",
            )
            index = consumer / "docs/ai-docs/README.md"
            row = (
                "| Refresh interval configuration | Reference | Operators |"
                f" [how-to/configure-refresh.md](how-to/configure-refresh.md)"
                f" | [{EVIDENCE_FILE}](../../{EVIDENCE_FILE}) |"
            )
            lines = index.read_text().splitlines()
            for position, line in enumerate(lines):
                if line.startswith("| Documentation validation commands |"):
                    lines.insert(position + 1, row)
                    break
            else:
                self.fail("the seeded routing table must contain the anchor row")
            index.write_text("\n".join(lines) + "\n")
            support.run_checks(consumer)
            support.commit_all(consumer, "evidence-backed page and route")


            # 6. Break and repair a local file link and a fragment.
            evidence_page = consumer / EVIDENCE_PAGE
            page_text = evidence_page.read_text()
            evidence_page.write_text(
                page_text + "\n[broken local link](../missing-page.md)\n"
            )
            failed = support.run_checks(consumer, check=False)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("missing-page.md", failed.stdout + failed.stderr)
            evidence_page.write_text(page_text)
            support.run_checks(consumer)

            evidence_page.write_text(
                page_text + "\n[broken fragment](#missing-fragment)\n"
            )
            failed = support.run_checks(consumer, check=False)
            self.assertNotEqual(failed.returncode, 0)
            evidence_page.write_text(page_text)
            support.run_checks(consumer)

            # 7. Controlled managed-policy change in a new tagged template revision.
            policy = template / "template/.ai-docs/policy.md"
            policy.write_text(
                policy.read_text()
                + "\n## E01 managed change\n\nThis managed policy line arrives in v0.1.1.\n"
            )
            support.commit_all(template, "toolkit v0.1.1")
            support.tag(template, "v0.1.1")

            support.update_project(consumer, ref="v0.1.1")

            self.assertIn(
                "## E01 managed change",
                (consumer / ".ai-docs/policy.md").read_text(),
            )
            self.assertTrue((consumer / EVIDENCE_FILE).is_file())
            self.assertIn("15 minutes", (consumer / EVIDENCE_PAGE).read_text())
            self.assertIn("configure-refresh.md", index.read_text())
            self.assertEqual(
                support.file_hashes(consumer, owned_files),
                owned_before,
                "foreign and user-owned files must survive the upgrade",
            )
            self.assertEqual(support.conflict_files(consumer), [])
            self.assertEqual(support.unmerged_paths(consumer), [])
            self.assertEqual(
                list(consumer.rglob("*.rej")), [], "no rejected hunks may remain"
            )
            after_answers = (consumer / support.ANSWERS_FILE).read_text()
            self.assertIn("v0.1.1", after_answers)
            self.assertIn("docs_dir: docs/ai-docs", after_answers)

            # 8. Final checks and recorded evidence.
            support.commit_all(consumer, "upgrade to v0.1.1")
            support.run_checks(consumer)
            versions = support.tool_versions()
            evidence = (
                "E01 evidence: source refs v0.1.0 -> v0.1.1; "
                f"final inventory files={len(support.inventory(consumer))}; "
                "foreign/user hashes preserved; tools="
                + ", ".join(f"{name}={version}" for name, version in versions.items())
            )
            print(evidence)
            self.assertIn("copier=copier 9.19.1", evidence)


if __name__ == "__main__":
    unittest.main()
