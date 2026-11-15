"""Validator failure, scope, and offline scenarios V01-V08 (T17)."""

from __future__ import annotations

import hashlib
import http.server
import os
import shutil
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import support


class ValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temporary = tempfile.TemporaryDirectory(prefix="ai-docs-kit-validation-")
        cls.root = Path(cls._temporary.name)
        cls.template = support.snapshot_template(cls.root / "template")

    @classmethod
    def tearDownClass(cls):
        cls._temporary.cleanup()

    def new_project(self, name: str) -> Path:
        project = self.root / name
        support.init_repo(project)
        support.render_project(self.template, project, project_name="Validation")
        support.commit_all(project, "install")
        return project

    def test_v01_valid_docs_pass_without_rewrites(self):
        project = self.new_project("valid")
        before = support.tree_hashes(project)
        support.run_checks(project)
        self.assertEqual(support.tree_hashes(project), before)

    def test_v02_markdown_violation_fails_and_scope_is_bounded(self):
        project = self.new_project("markdown")
        policy = project / ".ai-docs/policy.md"
        original = policy.read_text()

        policy.write_text(original + "\n## Valid heading\n\n#### Skipped level\n")
        failed = support.run_checks(project, check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("MD001", failed.stdout + failed.stderr)

        policy.write_text(original)
        support.run_checks(project)

        outside = support.write(
            project / "unrelated/bad.md", "# Unrelated\n\n#### Skipped level\n"
        )
        result = support.run_checks(project)
        self.assertNotIn("unrelated", result.stdout + result.stderr)
        self.assertTrue(outside.is_file())

    def test_v03_missing_file_and_image_fail_then_pass(self):
        project = self.new_project("links")
        index = project / "docs/ai-docs/README.md"
        original = index.read_text()

        index.write_text(original + "\n[missing page](missing-page.md)\n")
        failed = support.run_checks(project, check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("missing-page.md", failed.stdout + failed.stderr)

        support.write(project / "docs/ai-docs/missing-page.md", "# Missing page\n")
        support.run_checks(project)

        index.write_text(
            original + "\n[missing page](missing-page.md)\n\n![diagram](images/diagram.png)\n"
        )
        failed = support.run_checks(project, check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("images/diagram.png", failed.stdout + failed.stderr)

        support.write(project / "docs/ai-docs/images/diagram.png", "not-a-real-png")
        support.run_checks(project)

    def test_v04_fragments_unicode_and_encoded_spaces(self):
        project = self.new_project("fragments")
        index = project / "docs/ai-docs/README.md"
        original = index.read_text()

        index.write_text(original + "\n[same page](#missing-anchor)\n")
        failed = support.run_checks(project, check=False)
        self.assertNotEqual(failed.returncode, 0)

        index.write_text(
            original
            + "\n[cross page](how-to/update-documentation.md#missing-anchor)\n"
        )
        failed = support.run_checks(project, check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("Cannot find fragment", failed.stdout + failed.stderr)

        support.write(
            project / "docs/ai-docs/reference/unicode.md",
            "# Unicode page\n\n## Nastavení žluťoučký\n\nText.\n",
        )
        support.write(
            project / "docs/ai-docs/reference/release notes.md",
            "# Release notes\n\nText.\n",
        )
        index.write_text(
            original
            + "\n- [valid cross page](how-to/update-documentation.md#update-the-documentation)\n"
            + "- [unicode](reference/unicode.md#nastavení-žluťoučký)\n"
            + "- [encoded spaces](reference/release%20notes.md)\n"
        )
        support.run_checks(project)

    def test_v05_offline_run_makes_no_remote_requests(self):
        project = self.new_project("offline")

        class CountingHandler(http.server.BaseHTTPRequestHandler):
            hits = 0

            def do_GET(self):  # noqa: N802 - stdlib handler API
                CountingHandler.hits += 1
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"remote content")

            def log_message(self, *args):
                pass

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), CountingHandler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            support.write(
                project / "docs/ai-docs/reference/remote.md",
                "# Remote page\n\nSee [the remote document]"
                f"(http://127.0.0.1:{port}/documented).\n",
            )
            support.run_checks(project)
            self.assertEqual(
                CountingHandler.hits,
                0,
                "offline default checks must not request remote documentation URLs",
            )
        finally:
            server.shutdown()
            server.server_close()


    def test_v06_missing_tool_and_invalid_config_fail_visibly(self):
        project = self.new_project("missing-tool")

        lychee = Path(support.require_tool("lychee")).parent
        path_without_lychee = os.pathsep.join(
            entry
            for entry in os.environ["PATH"].split(os.pathsep)
            if entry and Path(entry).resolve() != lychee.resolve()
        )
        self.assertIsNone(
            shutil.which("lychee", path=path_without_lychee),
            "test setup must remove lychee from PATH",
        )
        env = os.environ.copy()
        env["PATH"] = path_without_lychee
        result = support.run_checks(project, check=False, env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("lychee", (result.stdout + result.stderr).lower())

        config = project / ".ai-docs/lychee.toml"
        original = config.read_text()
        config.write_text(original + "\ninclude_fragments = 42\n")
        failed = support.run_checks(project, check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("config", (failed.stdout + failed.stderr).lower())
        config.write_text(original)
        support.run_checks(project)

    def test_v07_incoming_link_failure_is_caught_by_full_scope(self):
        project = self.new_project("incoming")
        target = project / "docs/ai-docs/how-to/update-documentation.md"
        referring = project / "docs/ai-docs/README.md"
        original_referring = referring.read_text()
        support.write(
            referring,
            original_referring
            + "\n[routing link](how-to/update-documentation.md#update-the-documentation)\n",
        )
        support.commit_all(project, "add incoming link")
        referring_hash = hashlib.sha256(referring.read_bytes()).hexdigest()

        text = target.read_text().replace(
            "# Update the documentation", "# Change the documentation", 1
        )
        target.write_text(text)

        failed = support.run_checks(project, check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("update-documentation.md", failed.stdout + failed.stderr)
        self.assertEqual(
            hashlib.sha256(referring.read_bytes()).hexdigest(),
            referring_hash,
            "the referring page was intentionally not edited",
        )

        target.write_text(
            text.replace(
                "# Change the documentation", "# Update the documentation", 1
            )
        )
        support.run_checks(project)

    def test_v08_native_config_precedence_is_not_an_isolation_guarantee(self):
        project = self.new_project("precedence")
        root_config = support.write(
            project / ".markdownlint-cli2.jsonc",
            '{\n  "config": {\n    "MD013": true\n  }\n}\n',
        )
        config_hash = hashlib.sha256(root_config.read_bytes()).hexdigest()

        entry = project / ".ai-docs/README.md"
        self.assertIn("base configuration", entry.read_text())
        entry.write_text(
            entry.read_text() + "\n" + ("long line " * 19) + "long line\n"
        )

        failed = support.run_checks(project, check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("MD013", failed.stdout + failed.stderr)
        self.assertEqual(
            hashlib.sha256(root_config.read_bytes()).hexdigest(),
            config_hash,
            "the consumer-native configuration must not be rewritten",
        )

        root_config.unlink()
        support.run_checks(project)


if __name__ == "__main__":
    unittest.main()
