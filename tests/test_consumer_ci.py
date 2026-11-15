"""Inert consumer CI example scenario A02 (T13)."""

from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import support

START = "<!-- ai-docs-kit:workflow-example:start -->"
END = "<!-- ai-docs-kit:workflow-example:end -->"
PINNED_ACTIONS = {
    "actions/checkout": "3d3c42e5aac5ba805825da76410c181273ba90b1",
    "actions/setup-python": "6d4fd22b20465ccc0f7354476588e8df7c9ca0e0",
    "actions/setup-node": "949feb2413d6458794dcd2491c4babbbce0c15c1",
    "taiki-e/install-action": "ab49d3c64680143e184118bed66a46419fc15519",
}
PIN_PATTERN = re.compile(r"^[\w.-]+/[\w.-]+@[0-9a-f]{40}$")


def workflow_from_example(path: Path) -> dict:
    import yaml

    block = support.read_fenced_block(path, START, END).strip()
    if not block.startswith("```yaml"):
        raise AssertionError("the workflow example must be a fenced yaml block")
    body = block[len("```yaml") :].strip()
    if body.endswith("```"):
        body = body[: -len("```")].rstrip()
    return yaml.safe_load(body)


class ConsumerCiExampleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temporary = tempfile.TemporaryDirectory(prefix="ai-docs-kit-ci-example-")
        cls.root = Path(cls._temporary.name)
        cls.template = support.snapshot_template(cls.root / "template")

    @classmethod
    def tearDownClass(cls):
        cls._temporary.cleanup()

    def render(self, name: str, **kwargs) -> Path:
        project = self.root / name
        support.init_repo(project)
        support.render_project(self.template, project, project_name="CI example", **kwargs)
        support.commit_all(project, "install")
        return project

    def test_example_is_inert_after_render(self):
        project = self.render("inert")
        self.assertFalse((project / ".github").exists())
        self.assertEqual(
            [path for path in support.inventory(project) if path.startswith(".github/")],
            [],
        )

    def test_workflow_contract(self):
        project = self.render("contract")
        example = project / ".ai-docs/examples/github-actions.md"
        workflow = workflow_from_example(example)

        self.assertEqual(workflow["permissions"], {"contents": "read"})

        triggers = workflow.get("on", workflow.get(True))
        self.assertIn("pull_request", triggers)
        self.assertIn("push", triggers)
        self.assertNotIn("pull_request_target", triggers)
        self.assertNotIn("schedule", triggers)
        self.assertNotIn("secrets", str(workflow))
        self.assertNotIn("pull_request_target", str(workflow))

        job = next(iter(workflow["jobs"].values()))
        self.assertIn("timeout-minutes", job)
        steps = job["steps"]

        used = {}
        for step in steps:
            if "uses" not in step:
                continue
            self.assertRegex(step["uses"], PIN_PATTERN)
            name, sha = step["uses"].split("@", 1)
            used[name] = sha
            self.assertRegex(step.get("name", ""), r".+")
        for action, sha in PINNED_ACTIONS.items():
            self.assertEqual(used.get(action), sha, action)

        install = next(
            step for step in steps
            if step.get("uses", "").startswith("taiki-e/install-action@")
        )
        self.assertEqual(install["with"]["tool"], "lychee@0.24.2")
        self.assertIs(install["with"]["checksum"], True)
        self.assertEqual(install["with"]["fallback"], "none")

        python_step = next(
            step for step in steps
            if step.get("uses", "").startswith("actions/setup-python@")
        )
        self.assertEqual(python_step["with"]["python-version"], "3.12")
        node_step = next(
            step for step in steps
            if step.get("uses", "").startswith("actions/setup-node@")
        )
        self.assertEqual(node_step["with"]["node-version"], "24")

        commands = "\n".join(step.get("run", "") for step in steps)
        self.assertIn(
            "pre-commit run --config .ai-docs/pre-commit-config.yaml --all-files",
            commands,
        )
        self.assertIn("pre-commit==4.7.0", commands)
        self.assertEqual(
            support.run(["pre-commit", "--version"]).stdout.strip(),
            "pre-commit 4.7.0",
        )

    def test_example_commands_work_for_default_and_custom_roots(self):
        for name, docs_dir in (("default", None), ("custom", "handbook/v2")):
            with self.subTest(render=name):
                project = self.render(f"run-{name}", docs_dir=docs_dir)
                workflow = workflow_from_example(
                    project / ".ai-docs/examples/github-actions.md"
                )
                commands = "\n".join(
                    step.get("run", "")
                    for step in next(iter(workflow["jobs"].values()))["steps"]
                )
                self.assertNotIn("handbook", commands)
                self.assertNotIn("docs/ai-docs", commands)
                support.run_checks(project)


if __name__ == "__main__":
    unittest.main()
