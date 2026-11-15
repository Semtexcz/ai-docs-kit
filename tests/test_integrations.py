"""Optional integration boundary scenario B01 (T19)."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import support

SIBLING_SENTINELS = (
    "openspec/specs/example/spec.md",
    "openspec/project.md",
    ".ai-planner/TASKS.md",
    ".devkit/standards.md",
)


class IntegrationBoundaryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temporary = tempfile.TemporaryDirectory(prefix="ai-docs-kit-integration-")
        cls.root = Path(cls._temporary.name)
        cls.template = support.snapshot_template(cls.root / "template")

    @classmethod
    def tearDownClass(cls):
        cls._temporary.cleanup()

    def test_b01_absent_integrations_are_normal_and_nothing_is_installed(self):
        project = self.root / "absent"
        support.copy_fixture("non_software", project)
        support.init_repo(project)

        support.render_project(self.template, project, project_name="No siblings")

        self.assertFalse((project / "openspec").exists())
        self.assertFalse((project / ".ai-planner").exists())
        self.assertFalse((project / ".devkit").exists())
        self.assertFalse((project / "package.json").exists())
        self.assertFalse((project / "pyproject.toml").exists())

        context = (project / ".ai-docs/project.md").read_text()
        self.assertIn("Absent unless added by this project", context)
        self.assertIn("Optional integrations", context)

        rendered = "\n".join(
            (project / path).read_text()
            for path in support.inventory(project)
            if path.endswith((".md", ".yaml", ".yml", ".toml", ".jsonc"))
        )
        for command in ("openspec init", "openspec update", "ai-devkit", "ai-project-planner"):
            self.assertNotIn(command, rendered)

        support.commit_all(project, "install kit")
        support.run_checks(project)

    def test_b01_existing_sibling_trees_are_untouched_and_linkable(self):
        project = self.root / "present"
        support.copy_fixture("non_software", project)
        for sentinel in SIBLING_SENTINELS:
            support.write(project / sentinel, f"# SENTINEL {sentinel}\n\nUser-owned.\n")
        support.init_repo(project)
        support.commit_all(project, "sibling trees")
        before = support.file_hashes(project, SIBLING_SENTINELS)

        support.render_project(self.template, project, project_name="With siblings")
        self.assertEqual(support.file_hashes(project, SIBLING_SENTINELS), before)

        # The consumer links existing evidence through its own index and context.
        index = project / "docs/ai-docs/README.md"
        index.write_text(
            index.read_text()
            + "\n| Intended behavior | Reference | Maintainers |"
            " [openspec requirement](../../openspec/specs/example/spec.md)"
            " | [spec sentinel](../../openspec/specs/example/spec.md) |\n"
        )
        context = project / ".ai-docs/project.md"
        context.write_text(
            context.read_text()
            + "\nLinked requirement index: `openspec/specs/` (inspected).\n"
        )
        support.commit_all(project, "link sibling evidence")

        # Checks pass with sibling CLIs made unavailable: no runtime dependency.
        sibling_tools = []
        for tool in ("openspec",):
            found = support.require_tool(tool) if _which(tool) else None
            if found:
                sibling_tools.append(str(Path(found).parent.resolve()))
        env = os.environ.copy()
        env["PATH"] = os.pathsep.join(
            entry
            for entry in os.environ["PATH"].split(os.pathsep)
            if entry and str(Path(entry).resolve()) not in sibling_tools
        )
        support.run_checks(project, env=env)
        self.assertEqual(support.file_hashes(project, SIBLING_SENTINELS), before)


def _which(name: str):
    import shutil

    return shutil.which(name)


if __name__ == "__main__":
    unittest.main()
