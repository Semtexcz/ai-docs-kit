# Semantic walkthrough record: non-software fixture

- Reviewer: Cline coding agent (DeepSeek model, high reasoning effort)
- Independence: implementation-agent record, not independent review
- Date: 2026-11-15
- Fixture: `tests/scenarios/non-software/`, copied into a disposable Git repository and
  rendered with the working-tree template snapshot tagged `v0.1.0`
- Tools: Copier 9.19.1, pre-commit 4.7.0, markdownlint-cli2 0.24.1, Lychee 0.24.2,
  Node 24.22.3, Python 3.12.16 (Ubuntu Linux 26.04)
- Result: pass against the rubric

## Inputs

- Discover: "Which documentation does the intake team have for applying the approval
  threshold, and what is missing?"
- Write: "Create one how-to page for intake officers applying the approval threshold,
  and route it from the documentation index."
- Review: "Review the new page for evidence support and readiness."

## Inspected sources

- Rendered `.ai-docs/README.md`, `.ai-docs/policy.md`, `.ai-docs/project.md`,
  `.ai-docs/skills/README.md`, and the three skill bodies.
- Rendered `docs/ai-docs/README.md` routing index.
- `policies/approval-policy.md`, `records/2026-06-review.md`,
  `operations/intake.md`, `handbook/intake-notes.md`.
- File listing of the fixture. No source-code tree exists and none was requested.
- Checks: `pre-commit run --config .ai-docs/pre-commit-config.yaml --all-files`.

## Output summary

Discovery recorded the policy, review record, intake steps, and handbook notes. The gap
was the absence of a task-oriented page that tells an intake officer when owner approval
is required. The existing notes deliberately do not restate the threshold.

The write step created `docs/ai-docs/how-to/apply-approval-threshold.md`. It cites the
approved policy (five working days, approved 2026-01-15) and the June 2026 review record
that retained the threshold, states the intake-officer exception, and records that no
intake system was executed. A routing row with five columns was added. The full check
run passed on the first attempt.

The review step assessed the page as `ready`: both material claims resolve to the
approved policy and its review record, no planned behavior was presented as delivered,
and no Python or sibling-toolkit evidence was demanded.

## Rubric results

| ID | Result | Evidence from this walkthrough |
| --- | --- | --- |
| M01 | pass | Missing reader journey identified from an inspected index and file listing; unrelated record types were not opened and are reported as not inspected; no restructure proposed |
| M02 | pass | Page written from the approved policy and review record, routed with all five columns; no planned feature is claimed as delivered |
| M03 | not applicable here | The invented-flag review was exercised in the software record |
| M04 | pass | No conflicting sources were found; the handbook notes defer to the policy rather than competing with it, and the page links the canonical source |
| M05 | pass | The page states that no intake system was executed instead of claiming a test; checks were run and reported separately |
| M06 | not applicable here | Untrusted embedded instructions were exercised in the software record |
| M07 | pass | Operational evidence (policy and review record) supported every claim; no source files, Python project, or sibling toolkit was requested |
| M08 | pass | The index route led to the policy; operations and records were read only because the policy points to them; unrelated trees were not loaded |

## Follow-up

No skill or asset change was required for the non-software path.
