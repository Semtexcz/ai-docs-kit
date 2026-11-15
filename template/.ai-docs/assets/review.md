# Documentation review record

Use this structure for a documentation review. Replace placeholders with inspected
facts; leave a row out only when the category was actually inspected and empty. Do not
record a check as passing when it was not run.

## Scope and target revision

- Files or sections:
- Revision (commit, range, or working tree):
- Intended audience and reader need:
- Requested outcome (readiness, claim verification, diff review):
- Out of scope:

## Inspected sources

| Source | Revision | Evidence kind |
| --- | --- | --- |
| Unknown — owner to confirm | Unknown | implementation, configuration, test, operational record, specification, decision record |

## Claim/evidence table

| Claim/location | Source | Evidence kind/revision | Result | Action |
| --- | --- | --- | --- | --- |
| Unknown | Unknown | Unknown | supported, planned, inference, unsupported, or conflicting | Unknown |

Result definitions:

- `supported`: an inspected source at the stated revision states or demonstrates it.
- `planned`: approved intent without implementation evidence; the page must say so.
- `inference`: reasoned from inspected sources; label the uncertainty.
- `unsupported`: no inspected source supports it, or the source is irrelevant.
- `conflicting`: inspected sources disagree; report both.

## Deterministic checks

| Command | Result |
| --- | --- |
| `pre-commit run --config .ai-docs/pre-commit-config.yaml --all-files` | pass, fail, or not run with reason |
| markdownlint-cli2 component, if run separately | pass, fail, or not run with reason |
| Lychee component, if run separately | pass, fail, or not run with reason |

Remote URLs are not requested by the default offline link check. Do not claim external
reachability or external link validation.

## Semantic findings

| Severity | Location | Finding | Required change |
| --- | --- | --- | --- |
| blocker, major, or minor | Unknown | Unknown | Unknown |

Severity guidance: unsupported behavior, flags, commands, results, compatibility, or
security claims are blockers; missing reader-essential prerequisites or navigation are
major; wording and formatting are minor.

## Uncertainties

- Unknown — owner to confirm

## Disposition

- ready: all material claims have recorded support, required checks passed, findings
  resolved.
- changes required: deterministic checks pass but semantic findings remain.
- incomplete: required evidence or a required check is unavailable.

Selected disposition: Unknown — owner to confirm
