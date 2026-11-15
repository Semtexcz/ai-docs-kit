"""Toolchain and fixture-harness checks (T01, T02).

These tests fail, not skip, when a required external tool is missing. They never
modify the source repository, its history, tags, or global Git configuration.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import support


class ToolchainTest(unittest.TestCase):
    def test_pinned_tool_versions_available(self):
        versions = support.tool_versions()
        self.assertEqual(versions["copier"], "copier 9.19.1")
        self.assertEqual(versions["pre-commit"], "pre-commit 4.7.0")
        self.assertIn("markdownlint-cli2 v0.24.1", versions["markdownlint-cli2"])
        self.assertEqual(versions["lychee"], "lychee 0.24.2")
        self.assertIn("skills-ref", versions["skills-ref"])
        self.assertRegex(versions["node"], r"^v24\.")
        self.assertRegex(versions["git"], r"^git version 2\.")

    def test_supported_python_family(self):
        self.assertEqual(
            sys.version_info[:2],
            (3, 12),
            "Integration tests target the selected Python 3.12 family. "
            "Provision it as documented in docs/maintainer-setup.md.",
        )

    def test_skill_validator_cli_is_available(self):
        support.require_tool("skills-ref")
        result = support.run(["skills-ref", "validate", "--help"], check=True)
        self.assertIn("Validate a skill directory", result.stdout)

    def test_two_tagged_fixture_revisions_in_parent_path_with_spaces(self):
        before = support.run(
            ["git", "status", "--porcelain"], cwd=support.REPO_ROOT, check=True
        ).stdout
        with tempfile.TemporaryDirectory(prefix="ai docs kit  fixture ") as tmp:
            root = Path(tmp)
            self.assertIn(" ", str(root))
            first = support.snapshot_template(root / "template source")
            self.assertEqual(
                support.run(["git", "tag", "--list"], cwd=first).stdout.split(),
                ["v0.1.0"],
            )

            support.write(first / "EXAMPLE_VERSION.txt", "second revision\n")
            second_sha = support.commit_all(first, "second fixture revision")
            support.tag(first, "v0.1.1")

            tags = support.run(["git", "tag", "--list"], cwd=first).stdout.split()
            self.assertEqual(tags, ["v0.1.0", "v0.1.1"])
            self.assertEqual(
                support.run(["git", "rev-parse", "v0.1.1"], cwd=first).stdout.strip(),
                second_sha,
            )

            # The harness must not touch the repository under test.
            after = support.run(
                ["git", "status", "--porcelain"], cwd=support.REPO_ROOT, check=True
            ).stdout
            self.assertEqual(before, after)

    def test_snapshot_excludes_caches_and_keeps_template_surface(self):
        with tempfile.TemporaryDirectory(prefix="ai-docs-kit-snapshot-") as tmp:
            snapshot = support.snapshot_template(Path(tmp) / "source")
            files = support.inventory(snapshot)
            for required in (
                "copier.yml",
                "template/.ai-docs/policy.md",
                "template/.ai-docs/skills/README.md.jinja",
                "requirements-dev.txt",
            ):
                self.assertIn(required, files)
            for forbidden in (".venv", ".tools", "__pycache__"):
                self.assertFalse(
                    any(part.startswith(forbidden) for part in files),
                    f"{forbidden} must not be copied into template snapshots",
                )


if __name__ == "__main__":
    unittest.main()
