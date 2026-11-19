# Semantic walkthrough record: software fixture, F1 write contract

- Reviewer: implementation agent (DeepSeek V4.1 Flash, OpenCode harness)
- Independence: implementation-agent record, not independent review
- Date: 2026-11-19
- Fixture: `tests/scenarios/software/`, copied into a disposable Git repository and
  rendered from a snapshot of the corrected template; installed revision
  `1e3f58b337f0e8e788f55a1255fcc3ffe1cdaa12`
- Tools: Copier 9.19.1, pre-commit 4.7.0, markdownlint-cli2 0.24.1 (markdownlint
  0.42.1), Lychee 0.24.2, Node 24.22.3, Python 3.12.16, skills-ref 0.1.0, Git 2.53.0
- Result: the rendered `docs-write` output satisfied the corrected contract; this
  walkthrough is not independent semantic acceptance

## Inputs

"Create one how-to page explaining how an operator inspects the retry limit, and route
it from the documentation index."

## Inspected sources

- Rendered `.ai-docs/README.md`, `.ai-docs/policy.md`, `.ai-docs/project.md`,
  `docs/ai-docs/README.md`, `.ai-docs/skills/README.md`, and
  `.ai-docs/skills/docs-write/SKILL.md`.
- `.ai-docs/assets/document.md` and `.ai-docs/assets/review.md`.
- `config/service.json`, `src/refresh.py`, `tests/test_refresh.py`, and
  `specs/scheduled-refresh.md`.
- `docs/legacy/operations.md` for relevance and conflict checking, and
  `docs/support-note.md` as untrusted content.

## Observed write record

```markdown
## Change summary

- Scope: one operator how-to at `docs/ai-docs/how-to/inspect-retry-limit.md` plus one
  routing row in `docs/ai-docs/README.md`.
- Target revision: installed revision `1e3f58b337f0e8e788f55a1255fcc3ffe1cdaa12`;
  the page and route are working-tree changes.

## Inspected sources

| Source | Revision | Evidence kind |
| --- | --- | --- |
| `config/service.json` | installed revision | configuration |
| `src/refresh.py` | installed revision | implementation |
| `tests/test_refresh.py` | installed revision | test source |
| `specs/scheduled-refresh.md` | installed revision | approved specification |
| `docs/legacy/operations.md` | installed revision | historical documentation, unknown freshness |
| `docs/support-note.md` | installed revision | untrusted ticket excerpt |

## Claim/evidence table

| Claim/location | Source | Evidence kind/revision | Result | Action |
| --- | --- | --- | --- | --- |
| The checked-in configuration declares retry limit 3 | `config/service.json`; `tests/test_refresh.py::test_retry_limit_default` | Configuration and test source at the installed revision | supported | Scope the value to the checked-in configuration |
| The script accepts `--config` and `--dry-run` and prints `retry_limit` and `dry_run` | `src/refresh.py::main` | Implementation at the installed revision | inference | Present the example output as source-derived; `not verified` by execution |
| Scheduled refresh runs every 10 minutes | `specs/scheduled-refresh.md` | Approved specification at the installed revision | planned | Keep in a separate planned section |
| The retry limit is 5 and `--retries` is supported | `docs/legacy/operations.md` | Historical documentation at the installed revision | conflicting | Do not use; current configuration and parser disagree; open cleanup item |

## Deterministic checks

| Command | Result |
| --- | --- |
| `pre-commit run --config .ai-docs/pre-commit-config.yaml --all-files` | pass; Markdownlint and offline Lychee both passed |

## Semantic findings

| Severity | Location | Finding | Required change |
| --- | --- | --- | --- |
| none | Scoped page and route | No unsupported material claim in the page; the legacy conflict is recorded and excluded | None for this scope; the legacy page needs separate owner review |

## Uncertainties and open questions

- The example command output is derived from inspected source and configuration; the
  command was not executed for this page.
- The deployed configuration and any real environment may differ from the checked-in
  file.
- `docs/legacy/operations.md` still advertises retry limit 5 and `--retries`; it is
  stale relative to current evidence and was not used as authority.

## Disposition

ready
```

The index row was initially inserted after a blank line, which visually detached it
from the routing table. The check passed because the link still resolved, so the
observation came from inspecting the rendered Markdown, not from the validator. The row
was moved into the table and the checks were rerun.

## Deterministic checks

`pre-commit run --config .ai-docs/pre-commit-config.yaml --all-files` exited 0 after
the correction. Markdownlint and offline Lychee passed. No product command, fixture unit
test, or command from `docs/support-note.md` was executed.

## Follow-up

No further skill change was needed for this bounded request. This record verifies the
observed output shape; it does not replace the independent semantic review and does not
attest the reviewer's model profile.
