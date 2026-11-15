"""Maintainer CI and repository gate scenario A01 (T20)."""

from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import support

PIN_PATTERN = re.compile(r"^[\w.-]+/[\w.-]+@[0-9a-f]{40}$")
WORKFLOW = support.REPO_ROOT / ".github/workflows/ci.yml"
MAINTAINER_CONFIG = support.REPO_ROOT / ".pre-commit-config.yaml"


class MaintainerCiTest(unittest.TestCase):
    def setUp(self):
        import yaml

        self.workflow = yaml.safe_load(WORKFLOW.read_text())
        self.job = next(iter(self.workflow["jobs"].values()))
        self.steps = self.job["steps"]

    def test_workflow_is_least_privilege_and_pinned(self):
        self.assertEqual(self.workflow["permissions"], {"contents": "read"})
        triggers = self.workflow.get("on", self.workflow.get(True))
        self.assertIn("pull_request", triggers)
        self.assertIn("push", triggers)
        self.assertNotIn("pull_request_target", str(self.workflow))
        self.assertNotIn("secrets", str(self.workflow))
        self.assertIn("timeout-minutes", self.job)
        self.assertEqual(self.job["runs-on"], "ubuntu-latest")

        used = {}
        for step in self.steps:
            if "uses" not in step:
                continue
            self.assertRegex(step["uses"], PIN_PATTERN)
            name, sha = step["uses"].split("@", 1)
            used[name] = sha
        self.assertEqual(
            used["actions/checkout"], "3d3c42e5aac5ba805825da76410c181273ba90b1"
        )
        self.assertEqual(
            used["actions/setup-python"],
            "6d4fd22b20465ccc0f7354476588e8df7c9ca0e0",
        )
        self.assertEqual(
            used["actions/setup-node"], "949feb2413d6458794dcd2491c4babbbce0c15c1"
        )
        self.assertEqual(
            used["taiki-e/install-action"],
            "ab49d3c64680143e184118bed66a46419fc15519",
        )

        lychee = next(
            step
            for step in self.steps
            if step.get("uses", "").startswith("taiki-e/install-action@")
        )
        self.assertEqual(lychee["with"]["tool"], "lychee@0.24.2")
        self.assertIs(lychee["with"]["checksum"], True)
        self.assertEqual(lychee["with"]["fallback"], "none")

    def test_workflow_installs_pinned_versions_and_runs_required_commands(self):
        steps_by_name = {step.get("name"): step for step in self.steps}
        python = steps_by_name["Set up Python"]
        self.assertEqual(python["with"]["python-version"], "3.12.16")
        node = steps_by_name["Set up Node.js"]
        self.assertEqual(node["with"]["node-version"], "24.22.3")

        commands = "\n".join(step.get("run", "") for step in self.steps)
        self.assertIn("requirements-dev.txt", commands)
        self.assertIn("markdownlint-cli2@0.24.1", commands)
        self.assertIn("python -m unittest discover -s tests -v", commands)
        self.assertIn("pre-commit run --all-files", commands)
        self.assertIn("git diff --exit-code", commands)
        self.assertNotIn("|| true", commands)
        self.assertNotIn("continue-on-error", str(self.workflow))

        requirements = (support.REPO_ROOT / "requirements-dev.txt").read_text()
        self.assertIn("copier==9.19.1", requirements)
        self.assertIn("pre-commit==4.7.0", requirements)
        self.assertIn("83021e2be457a9b6679148719c1f6074f0ad975e", requirements)

    def test_maintainer_gate_configuration_is_scoped(self):
        import yaml

        config = yaml.safe_load(MAINTAINER_CONFIG.read_text())
        repos = {repo["repo"]: repo for repo in config["repos"]}
        markdownlint = repos["https://github.com/DavidAnson/markdownlint-cli2"]
        self.assertEqual(markdownlint["rev"], "v0.24.1")
        lychee = repos["https://github.com/lycheeverse/lychee"]
        self.assertEqual(lychee["rev"], "lychee-v0.24.2")
        hooks = repos["https://github.com/pre-commit/pre-commit-hooks"]
        self.assertRegex(hooks["rev"], r"^[0-9a-f]{40}$")

        args = "\n".join(
            str(item)
            for repo in config["repos"]
            for hook in repo["hooks"]
            for item in hook.get("args", [])
        )
        self.assertNotIn("template/", args)
        self.assertNotIn("tests/", args)
        self.assertNotIn("--fix", args)
        self.assertIn("--offline", args)
        self.assertIn("--include-fragments", args)

    def test_maintainer_documentation_gates_pass_locally(self):
        before = support.run(
            ["git", "status", "--porcelain"], cwd=support.REPO_ROOT, check=True
        ).stdout
        result = support.run(
            ["pre-commit", "run", "--all-files"],
            cwd=support.REPO_ROOT,
            check=False,
            timeout=900,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        # The checks are read-only: the working tree state must be unchanged.
        after = support.run(
            ["git", "status", "--porcelain"], cwd=support.REPO_ROOT, check=True
        ).stdout
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
