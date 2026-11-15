"""Portable skill package scenarios S01-S03 (T18)."""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import support

SKILL_NAMES = ("docs-discover", "docs-write", "docs-review")
LINK_PATTERN = re.compile(r"\]\(([^)\s]+)\)")


def local_links(text: str) -> list[str]:
    links = []
    for target in LINK_PATTERN.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        links.append(target.split("#", 1)[0])
    return [link for link in links if link]


def frontmatter(text: str) -> dict[str, str]:
    _, block, _ = text.split("---", 2)
    fields = {}
    for line in block.splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


class SkillPackageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temporary = tempfile.TemporaryDirectory(prefix="ai-docs-kit-skills-")
        cls.root = Path(cls._temporary.name)
        cls.template = support.snapshot_template(cls.root / "template")

    @classmethod
    def tearDownClass(cls):
        cls._temporary.cleanup()

    def render(self, name: str, **kwargs) -> Path:
        project = self.root / name
        support.init_repo(project)
        support.render_project(self.template, project, project_name="Skills", **kwargs)
        return project

    def test_s01_rendered_skills_validate_and_links_resolve(self):
        for label, docs_dir in (("default", None), ("custom", "handbook/v2")):
            with self.subTest(render=label):
                project = self.render(f"skills-{label}", docs_dir=docs_dir)
                expected_root = docs_dir or "docs/ai-docs"
                for skill in SKILL_NAMES:
                    skill_dir = project / f".ai-docs/skills/{skill}"
                    result = support.run(
                        ["skills-ref", "validate", str(skill_dir)], check=False
                    )
                    self.assertEqual(
                        result.returncode,
                        0,
                        f"{skill}: {result.stdout}{result.stderr}",
                    )

                    text = (skill_dir / "SKILL.md").read_text()
                    fields = frontmatter(text)
                    self.assertEqual(fields["name"], skill)
                    self.assertTrue(fields["description"])
                    self.assertEqual(set(fields), {"name", "description"})
                    self.assertLessEqual(len(text.splitlines()), 300)

                    for link in local_links(text):
                        target = (skill_dir / link).resolve()
                        self.assertTrue(
                            target.exists(), f"{skill} has a broken resource link: {link}"
                        )
                    index_links = [
                        (skill_dir / link).resolve()
                        for link in local_links(text)
                        if link.endswith("README.md")
                    ]
                    self.assertTrue(
                        any(expected_root in path.as_posix() for path in index_links),
                        f"{skill} must link the configured documentation index",
                    )

                    self.assertEqual(
                        sorted(p.name for p in skill_dir.iterdir()), ["SKILL.md"]
                    )

                catalog = (project / ".ai-docs/skills/README.md").read_text()
                for skill in SKILL_NAMES:
                    self.assertIn(f"`{skill}`", catalog)
                for deferred in ("docs-structure", "docs-maintain", "docs-publish"):
                    self.assertNotIn(f"`{deferred}`", catalog)

    def test_s02_malformed_copy_fails_upstream_validator(self):
        project = self.render("skills-malformed")
        source = project / ".ai-docs/skills/docs-write"
        with tempfile.TemporaryDirectory(prefix="ai-docs-kit-bad-skill-") as tmp:
            broken = Path(tmp) / "docs-write"
            shutil.copytree(source, broken)
            text = (broken / "SKILL.md").read_text()
            (broken / "SKILL.md").write_text(
                text.replace("name: docs-write", "name: wrong-name", 1)
            )
            failed = support.run(
                ["skills-ref", "validate", str(broken)], check=False
            )
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("must match", failed.stdout + failed.stderr)

        valid = support.run(
            ["skills-ref", "validate", str(source)], check=False
        )
        self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)

    def test_s03_budgets_and_catalog_contents(self):
        project = self.render("skills-budget")
        budgets = {
            ".ai-docs/README.md": 100,
            ".ai-docs/skills/README.md": 80,
            ".ai-docs/project.md": 150,
            "docs/ai-docs/README.md": 150,
        }
        for path, limit in budgets.items():
            self.assertLessEqual(
                len((project / path).read_text().splitlines()), limit, path
            )
        catalog = (project / ".ai-docs/skills/README.md").read_text()
        self.assertLessEqual(len(catalog.splitlines()), 80)
        self.assertEqual(
            sorted(p.name for p in (project / ".ai-docs/skills").iterdir()),
            sorted(["README.md", *SKILL_NAMES]),
        )
        self.assertIn("Manual invocation", catalog)


if __name__ == "__main__":
    unittest.main()
