"""Installation, rendering, and preservation scenarios I01-I06 (T14)."""

from __future__ import annotations

import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import support

MAINTAINER_ONLY = (
    "TASKS.md",
    "CHARTER.md",
    "PLAN.md",
    "AGENTS.md",
    "IMPLEMENTATION_HANDOFF.md",
    "requirements-dev.txt",
    "copier.yml",
    "tests",
    "openspec",
    "docs/architecture",
    ".github",
)


class RenderTestBase(unittest.TestCase):
    """Share one tagged template snapshot across the render scenarios."""

    @classmethod
    def setUpClass(cls):
        cls._temporary = tempfile.TemporaryDirectory(prefix="ai-docs-kit-render-")
        cls.template = support.snapshot_template(Path(cls._temporary.name) / "source")

    @classmethod
    def tearDownClass(cls):
        cls._temporary.cleanup()

    def render(self, destination, **kwargs):
        return support.render_project(self.template, destination, **kwargs)

    def assert_no_maintainer_artifacts(self, project):
        files = support.inventory(project)
        for path in MAINTAINER_ONLY:
            prefix = path.rstrip("/")
            self.assertFalse(
                any(item == prefix or item.startswith(prefix + "/") for item in files),
                f"maintainer artifact leaked into the consumer: {path}",
            )
        for item in files:
            self.assertNotIn("{{", Path(project, item).read_text(errors="ignore"))
            self.assertNotIn("{%", Path(project, item).read_text(errors="ignore"))

    def assert_entry_budgets(self, project):
        limits = {
            ".ai-docs/README.md": 100,
            ".ai-docs/skills/README.md": 80,
            ".ai-docs/project.md": 150,
            "docs/ai-docs/README.md": 150,
        }
        for relative, limit in limits.items():
            lines = len(Path(project, relative).read_text().splitlines())
            self.assertLessEqual(lines, limit, f"{relative} exceeds {limit} lines")

    def assert_no_executables(self, project):
        for relative in support.inventory(project):
            mode = Path(project, relative).stat().st_mode
            self.assertFalse(
                mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH),
                f"rendered file is executable: {relative}",
            )


class CleanInstallationTest(RenderTestBase):
    """I01: empty destination renders only the contracted consumer surface."""

    def test_required_inventory_and_state(self):
        with tempfile.TemporaryDirectory(prefix="ai-docs-kit-empty-") as tmp:
            project = Path(tmp) / "consumer"
            support.init_repo(project)
            self.render(project, project_name="Clean project")

            self.assertEqual(
                support.inventory(project), sorted(support.EXPECTED_CONSUMER_INVENTORY)
            )
            self.assert_no_maintainer_artifacts(project)
            self.assert_entry_budgets(project)
            self.assert_no_executables(project)

            answers = (project / support.ANSWERS_FILE).read_text()
            self.assertIn("_src_path:", answers)
            self.assertIn("_commit:", answers)
            self.assertIn("project_name: Clean project", answers)
            self.assertIn("docs_dir: docs/ai-docs", answers)
            self.assertFalse((project / ".copier-answers.yml").exists())

    def test_readme_links_resolve_to_rendered_files(self):
        with tempfile.TemporaryDirectory(prefix="ai-docs-kit-empty-") as tmp:
            project = Path(tmp) / "consumer"
            support.init_repo(project)
            self.render(project)
            support.commit_all(project, "install")
            result = support.run_checks(project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class ExistingProjectTest(RenderTestBase):
    """I02: shared and user-owned files stay byte-identical."""

    def test_existing_project_preserved(self):
        with tempfile.TemporaryDirectory(prefix="ai-docs-kit-existing-") as tmp:
            project = Path(tmp) / "consumer"
            support.copy_fixture("existing_project", project)
            support.init_repo(project)
            support.commit_all(project, "existing project")
            before = support.tree_hashes(project)

            self.render(project, project_name="Existing project")

            after = support.tree_hashes(project)
            for path, digest in before.items():
                self.assertEqual(
                    after.get(path), digest, f"user-owned file was modified: {path}"
                )
            for path in (
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
            ):
                self.assertIn(path, after)

            # The existing root Lychee/Markdown configuration is untouched and the
            # kit uses its own explicit configuration.
            self.assertNotIn(
                "# USER-OWNED LYCHEE CONFIG SENTINEL",
                (project / ".ai-docs/lychee.toml").read_text(),
            )

            support.commit_all(project, "ai-docs-kit install")
            support.run_checks(project)



class NonSoftwareCustomRootTest(RenderTestBase):
    """I03: non-software content, Unicode name, nested root, spaces in parent."""

    def test_custom_root_and_unicode_project_name(self):
        with tempfile.TemporaryDirectory(prefix="ai docs kit custom ") as tmp:
            self.assertIn(" ", tmp)
            project = Path(tmp) / "handbook project"
            support.copy_fixture("non_software", project)
            support.init_repo(project)
            before = support.tree_hashes(project)

            docs_dir = "handbook/ai-documentation/v1"
            self.render(
                project,
                docs_dir=docs_dir,
                project_name="Příručka Žluťoučký kůň 2.0",
            )

            after = support.tree_hashes(project)
            for path, digest in before.items():
                self.assertEqual(after.get(path), digest)

            for path in (
                f"{docs_dir}/README.md",
                f"{docs_dir}/how-to/update-documentation.md",
                f"{docs_dir}/reference/documentation-policy.md",
            ):
                self.assertTrue((project / path).is_file(), path)

            pre_commit = (project / ".ai-docs/pre-commit-config.yaml").read_text()
            self.assertIn(f'"{docs_dir}/**/*.md"', pre_commit)
            self.assertNotIn('"docs/ai-docs/**/*.md"', pre_commit)

            entry = (project / ".ai-docs/README.md").read_text()
            self.assertIn(f"../{docs_dir}/README.md", entry)
            self.assertIn("Příručka Žluťoučký kůň 2.0", entry)

            answers = (project / support.ANSWERS_FILE).read_text()
            self.assertIn(f"docs_dir: {docs_dir}", answers)
            self.assertIn("project_name: Příručka Žluťoučký kůň 2.0", answers)

            # A non-software project needs no source code for checks or links.
            support.commit_all(project, "install kit")
            support.run_checks(project)


class SeedPreservationTest(RenderTestBase):
    """I04: seed-once files retain bytes; missing seeds are recreated."""

    def test_preexisting_seed_is_not_replaced(self):
        with tempfile.TemporaryDirectory(prefix="ai-docs-kit-seed-") as tmp:
            project = Path(tmp) / "consumer"
            support.init_repo(project)
            sentinel = "# Existing documentation index\n\nUSER SEED SENTINEL\n"
            support.write(project / "docs/ai-docs/README.md", sentinel)
            support.commit_all(project, "pre-existing seed")

            self.render(project)

            self.assertEqual(
                (project / "docs/ai-docs/README.md").read_text(), sentinel
            )
            self.assertTrue(
                (project / "docs/ai-docs/how-to/update-documentation.md").is_file()
            )
            self.assertTrue(
                (project / "docs/ai-docs/reference/documentation-policy.md").is_file()
            )

    def test_repeated_copy_preserves_edits_and_recreates_missing_seed(self):
        with tempfile.TemporaryDirectory(prefix="ai-docs-kit-seed-") as tmp:
            project = Path(tmp) / "consumer"
            support.init_repo(project)
            self.render(project)
            support.commit_all(project, "install")

            context = project / ".ai-docs/project.md"
            index = project / "docs/ai-docs/README.md"
            context.write_text(context.read_text() + "\nUSER CONTEXT EDIT\n")
            index.write_text(index.read_text() + "\nUSER INDEX EDIT\n")
            (project / "docs/ai-docs/how-to/update-documentation.md").unlink()
            support.commit_all(project, "user edits and deleted seed")

            self.render(project)

            self.assertIn("USER CONTEXT EDIT", context.read_text())
            self.assertIn("USER INDEX EDIT", index.read_text())
            self.assertTrue(
                (project / "docs/ai-docs/how-to/update-documentation.md").is_file(),
                "a missing shipped seed is recreated by a repeated copy",
            )



class QuestionValidationTest(RenderTestBase):
    """I05: invalid answers are rejected by native Copier validators."""

    INVALID_DOCS_DIRS = (
        "/absolute/path",
        "../escape",
        "docs/../escape",
        "docs/./nested",
        "docs\\ai-docs",
        "docs/ai docs",
        "docs/ai\nmodified",
        "docs/*",
        "docs/ai?.md",
        "Docs/AI-Docs",
        "docs/ai-docs/",
        "docs//ai-docs",
        "",
        "openspec/specs",
        "template/content",
        "tests/fixtures",
        "node_modules/pkg",
        "vendor/docs",
        "build/docs",
        "dist/docs",
        "site/docs",
    )

    INVALID_NAMES = (
        "",
        "   ",
        "---",
        "!!!",
        "x" * 101,
        " Leading space",
        "Trailing space ",
        "Tab\tname",
        "Newline\nname",
    )

    def test_invalid_docs_dir_rejected_without_writes(self):
        for value in self.INVALID_DOCS_DIRS:
            with self.subTest(docs_dir=value):
                with tempfile.TemporaryDirectory(prefix="ai-docs-kit-invalid-") as tmp:
                    project = Path(tmp) / "consumer"
                    support.init_repo(project)
                    result = self.render(
                        project, docs_dir=value, project_name="Valid name", check=False
                    )
                    self.assertNotEqual(result.returncode, 0, value)
                    self.assertIn("docs_dir", result.stdout + result.stderr)
                    self.assertFalse((project / support.ANSWERS_FILE).exists())

    def test_invalid_project_name_rejected_without_writes(self):
        for value in self.INVALID_NAMES:
            with self.subTest(project_name=value):
                with tempfile.TemporaryDirectory(prefix="ai-docs-kit-invalid-") as tmp:
                    project = Path(tmp) / "consumer"
                    support.init_repo(project)
                    result = self.render(project, project_name=value, check=False)
                    self.assertNotEqual(result.returncode, 0, repr(value))
                    self.assertIn("project_name", result.stdout + result.stderr)
                    self.assertFalse((project / support.ANSWERS_FILE).exists())

    def test_valid_boundary_answers_are_accepted(self):
        with tempfile.TemporaryDirectory(prefix="ai-docs-kit-boundary-") as tmp:
            project = Path(tmp) / "consumer"
            support.init_repo(project)
            self.render(project, docs_dir="docs/a", project_name="A")
            self.assertTrue((project / "docs/a/README.md").is_file())


class TemplateContractTest(RenderTestBase):
    """I06: no executable template features, trust flags, or accidental output."""

    def test_copier_configuration_contract(self):
        import yaml

        config = yaml.safe_load((support.REPO_ROOT / "copier.yml").read_text())
        self.assertEqual(config["_subdirectory"], "template")
        self.assertEqual(config["_answers_file"], ".copier-answers.ai-docs-kit.yml")
        self.assertEqual(config["_min_copier_version"], "9.19.1")
        self.assertEqual(config["_templates_suffix"], ".jinja")
        for forbidden in ("_tasks", "_migrations", "_jinja_extensions", "tasks"):
            self.assertNotIn(forbidden, config)
        questions = {key for key in config if not key.startswith("_")}
        self.assertEqual(questions, {"project_name", "docs_dir"})

    def test_no_executable_or_host_specific_output(self):
        with tempfile.TemporaryDirectory(prefix="ai-docs-kit-contract-") as tmp:
            project = Path(tmp) / "consumer"
            support.init_repo(project)
            self.render(project)
            self.assert_no_executables(project)
            self.assert_no_maintainer_artifacts(project)

            files = support.inventory(project)
            for forbidden in (
                ".ai-docs/AGENTS.md",
                ".ai-docs/skills/docs-structure/SKILL.md",
                ".ai-docs/skills/docs-maintain/SKILL.md",
                ".ai-docs/skills/docs-publish/SKILL.md",
            ):
                self.assertNotIn(forbidden, files)
            self.assertFalse(any("scripts/" in item for item in files))
            self.assertFalse(any(item.startswith(".github/") for item in files))
            self.assertFalse(any(item.startswith(".claude/") for item in files))
            self.assertFalse((project / ".git/hooks/pre-commit").exists())

            for skill in ("docs-discover", "docs-write", "docs-review"):
                text = (project / f".ai-docs/skills/{skill}/SKILL.md").read_text()
                self.assertTrue(text.startswith("---\n"), skill)
                self.assertIn(f"name: {skill}\n", text)

    def test_pretend_preview_writes_nothing(self):
        with tempfile.TemporaryDirectory(prefix="ai-docs-kit-pretend-") as tmp:
            project = Path(tmp) / "consumer"
            support.init_repo(project)
            result = self.render(project, extra_args=["--pretend"], check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(support.inventory(project), [])
