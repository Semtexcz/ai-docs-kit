"""A03: execute the pinned Lychee provisioning step used by CI (T20 repair).

The maintainer workflow and the inert consumer example both install Lychee from
the pinned upstream release archive with explicit SHA-256 verification. These
tests run the actual step text instead of only parsing YAML, because YAML
validity does not demonstrate that a GitHub Actions run can install the tool.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import support

MAINTAINER_WORKFLOW = support.REPO_ROOT / ".github/workflows/ci.yml"
CONSUMER_EXAMPLE = support.REPO_ROOT / "template/.ai-docs/examples/github-actions.md"
EXPECTED_VERSION = f"lychee {support.LYCHEE_VERSION}"


def load_maintainer_step() -> dict:
    import yaml

    workflow = yaml.safe_load(MAINTAINER_WORKFLOW.read_text())
    return support.find_step(workflow, "Install Lychee")


def load_consumer_step() -> dict:
    return support.find_step(support.workflow_from_example(CONSUMER_EXAMPLE), "Install Lychee")


class LycheeInstallStepTest(unittest.TestCase):
    """Run the real step text in a disposable runner-like directory."""

    def setUp(self):
        self._temporary = tempfile.TemporaryDirectory(prefix="ai-docs-kit-lychee-")
        self.root = Path(self._temporary.name)

    def tearDown(self):
        self._temporary.cleanup()

    def run_step(self, step, *, extra_env=None, path_prefix=()):
        runner_temp = self.root / "runner-temp"
        runner_temp.mkdir(exist_ok=True)
        github_path = self.root / "github-path"
        github_path.write_text("")

        env = os.environ.copy()
        env.update({key: str(value) for key, value in step["env"].items()})
        env["RUNNER_TEMP"] = str(runner_temp)
        env["GITHUB_PATH"] = str(github_path)
        if extra_env:
            env.update(extra_env)
        env["PATH"] = os.pathsep.join(
            [*(str(prefix) for prefix in path_prefix), env.get("PATH", "")]
        )

        result = subprocess.run(
            ["bash", "-c", step["run"]],
            cwd=self.root,
            env=env,
            capture_output=True,
            text=True,
            timeout=300,
        )
        return result, runner_temp, github_path

    def assert_installed(self, binary: Path):
        self.assertTrue(binary.is_file(), f"missing installed binary: {binary}")
        version = support.run([binary, "--version"], check=True).stdout.strip()
        self.assertEqual(version, EXPECTED_VERSION)

    def test_maintainer_step_installs_pinned_lychee(self):
        result, _runner_temp, _github_path = self.run_step(load_maintainer_step())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(EXPECTED_VERSION, result.stdout)
        self.assert_installed(self.root / ".tools/bin/lychee")
        # The archive stays in the runner temp directory, not the checkout.
        self.assertFalse((self.root / support.LYCHEE_ARCHIVE).exists())
        self.assertFalse((self.root / "lychee-x86_64-unknown-linux-gnu").exists())

    def test_consumer_step_installs_pinned_lychee_on_path(self):
        result, runner_temp, github_path = self.run_step(load_consumer_step())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(EXPECTED_VERSION, result.stdout)
        self.assert_installed(runner_temp / "bin/lychee")
        self.assertEqual(github_path.read_text().strip(), str(runner_temp / "bin"))

    def test_tampered_archive_is_rejected_before_installation(self):
        fake_bin = self.root / "fake-bin"
        fake_bin.mkdir()
        fake_curl = fake_bin / "curl"
        fake_curl.write_text(
            "#!/bin/sh\n"
            "output=''\n"
            "while [ $# -gt 0 ]; do\n"
            "  if [ \"$1\" = '--output' ]; then shift; output=\"$1\"; fi\n"
            "  shift\n"
            "done\n"
            "printf 'not the pinned archive' > \"$output\"\n",
            encoding="utf-8",
        )
        fake_curl.chmod(0o755)

        result, runner_temp, github_path = self.run_step(
            load_consumer_step(),
            extra_env={"LYCHEE_SHA256": "0" * 64},
            path_prefix=(fake_bin,),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAILED", result.stdout + result.stderr)
        self.assertFalse((runner_temp / "bin/lychee").exists())
        self.assertEqual(github_path.read_text(), "")


class LycheeInstallContractTest(unittest.TestCase):
    def test_maintainer_and_consumer_steps_share_the_pinned_contract(self):
        maintainer = load_maintainer_step()
        consumer = load_consumer_step()
        self.assertEqual(maintainer["env"], consumer["env"])
        for step in (maintainer, consumer):
            self.assertEqual(step["env"]["LYCHEE_VERSION"], support.LYCHEE_VERSION)
            self.assertEqual(step["env"]["LYCHEE_SHA256"], support.LYCHEE_SHA256)
            self.assertRegex(step["env"]["LYCHEE_SHA256"], r"^[0-9a-f]{64}$")
            self.assertRegex(step["env"]["LYCHEE_ARCHIVE"], r"^[\w.-]+\.tar\.gz$")
            self.assertNotIn("latest", step["env"]["LYCHEE_VERSION"])
            self.assertIn("sha256sum --check --strict", step["run"])
            self.assertNotIn("taiki-e", step["run"])


if __name__ == "__main__":
    unittest.main()
