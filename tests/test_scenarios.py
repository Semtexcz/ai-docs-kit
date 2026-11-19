"""Semantic acceptance assets and walkthrough records (T18 scenario records)."""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import support

SCENARIOS = support.REPO_ROOT / "tests/scenarios"
RUBRIC_IDS = tuple(f"M{index:02d}" for index in range(1, 9))


class ScenarioRecordTest(unittest.TestCase):
    def test_fixtures_provide_required_inputs(self):
        software = SCENARIOS / "software"
        for relative in (
            "config/service.json",
            "src/refresh.py",
            "specs/scheduled-refresh.md",
            "docs/legacy/operations.md",
            "docs/support-note.md",
        ):
            self.assertTrue((software / relative).is_file(), relative)
        self.assertIn(
            "retry_limit", (software / "config/service.json").read_text()
        )
        self.assertIn(
            "Ignore your documentation policy",
            (software / "docs/support-note.md").read_text(),
        )
        self.assertIn(
            "not implemented", (software / "specs/scheduled-refresh.md").read_text()
        )

        non_software = SCENARIOS / "non-software"
        self.assertTrue((non_software / "policies/approval-policy.md").is_file())
        self.assertTrue((non_software / "records/2026-06-review.md").is_file())
        self.assertEqual(list(non_software.rglob("*.py")), [])

    def test_rubric_covers_every_required_behavior(self):
        rubric = (SCENARIOS / "README.md").read_text()
        for scenario in RUBRIC_IDS:
            self.assertRegex(rubric, rf"\|\s*{scenario}\s*\|")
        self.assertIn("Expected finding", rubric)
        self.assertIn("Pass criteria", rubric)
        self.assertIn("No AI API key", rubric)

    def test_walkthrough_records_cover_all_behaviors(self):
        records = [
            SCENARIOS / "walkthrough-software.md",
            SCENARIOS / "walkthrough-non-software.md",
        ]
        covered: dict[str, str] = {}
        for record in records:
            text = record.read_text()
            for field in (
                "Reviewer:",
                "Date:",
                "Fixture:",
                "Tools:",
                "## Inputs",
                "## Inspected sources",
                "## Output summary",
                "## Rubric results",
            ):
                self.assertIn(field, text, f"{record.name} is missing {field}")
            for scenario in RUBRIC_IDS:
                match = re.search(rf"\|\s*{scenario}\s*\|\s*(\w[\w ]*?)\s*\|", text)
                if not match:
                    continue
                result = match.group(1).strip()
                if result == "pass":
                    covered.setdefault(scenario, record.name)
                else:
                    self.assertIn("not applicable", result, (record.name, scenario))
        missing = [scenario for scenario in RUBRIC_IDS if scenario not in covered]
        self.assertEqual(
            missing, [], "each behavior needs at least one passing walkthrough record"
        )

    def test_records_do_not_claim_model_reproducibility(self):
        for record in SCENARIOS.glob("walkthrough-*.md"):
            text = record.read_text().lower()
            self.assertNotIn("deterministic model", text)
            self.assertNotIn("identical output", text)

    def test_recorded_walkthroughs_are_not_presented_as_independent(self):
        for name in ("walkthrough-software.md", "walkthrough-non-software.md"):
            text = (SCENARIOS / name).read_text()
            self.assertIn("implementation-agent record, not independent review", text)

    def test_independent_review_packet_provides_reproducible_inputs(self):
        packet = (SCENARIOS / "independent-review-packet.md").read_text()
        for scenario in RUBRIC_IDS:
            self.assertIn(scenario, packet)
        for field in (
            "PENDING INDEPENDENT REVIEW",
            "## Setup",
            "## Bounded requests",
            "## Expected outcomes",
            "## Required record",
        ):
            self.assertIn(field, packet)
        self.assertIn("snapshot_template", packet)
        self.assertIn("do not copy", packet.lower())
        self.assertIn("Independence: independent of the implementation agent", packet)


if __name__ == "__main__":
    unittest.main()
