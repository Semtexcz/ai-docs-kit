# Documentation, discovery, and evidence

## Content model

Apply Diátaxis by reader need: learning by doing (tutorial), accomplishing a task
(how-to), looking up facts (reference), understanding concepts (explanation).
An index can route several kinds. ADRs, policies, and planning records remain
distinct governance artifacts; do not force them into a Diátaxis quadrant.

Create a page only for a real need. The MVP seeds one how-to and one reference
entry, not four empty trees. Existing documents keep their paths until an explicit
reorganization is reviewed. Markdown with ordinary relative links and fenced
code is the portable baseline; no renderer-specific extensions are required.

## Retrieval protocol

1. Start with `.ai-docs/README.md`, policy, and short `project.md` context.
2. Read the documentation home index. Follow its audience/topic/source routes.
3. Select one skill from the catalog and load its body only when relevant.
4. Read the target page and immediately relevant evidence. Use file listing and
   scoped `rg` queries; expand scope only for a concrete unresolved question.
5. Record files inspected, checks run, and remaining unknowns in the review output.

The index is a Markdown table with `Topic`, `Reader need/type`, `Audience`, `Path`,
and `Evidence entry point` columns. Paths are clickable relative links. Include
existing docs routes and links to policy and the skill catalog, but do not repeat
all skill instructions or all evidence. Keep the seed index under 150 lines;
use linked topic indexes as it grows. The generated `.ai-docs/README.md` stays
under 100 lines, the skill catalog under 80, and seeded project context under 150.
No generated search index, embeddings,
frontmatter database, or full-repository ingestion is required.

## Page conventions

Use one descriptive H1, state audience and purpose briefly, separate current from
planned behavior, give prerequisites and expected outcomes for procedures, and
link related pages. Reader-facing pages do not require YAML frontmatter.
An optional visible `Sources` section groups evidence near the claim it supports.
Navigation, policy pointers, and explicit templates contain no invented project facts.

Keep placeholders explicit: `Unknown — owner to confirm`, never plausible-looking
defaults for behavior that has not been verified. Do not insert broken Markdown
links to nonexistent placeholder files; use inline code for proposed paths.

## Material claims

A material claim affects a reader's action or understanding of project behavior:
commands, flags, defaults, supported versions, configuration, security properties,
procedures, compatibility, contracts, and decisions. Common explanatory prose need
not cite every sentence. A valid link establishes reachability, not support.

For each new or materially changed claim, an agent must inspect evidence and
associate it with the paragraph, table row, or procedure in the page or review.
Public docs should link sources where useful; the review records granular support
when inline citations would obscure the reader's task.

| Claim kind | Acceptable evidence | Required qualification |
| --- | --- | --- |
| Current behavior | Inspected implementation/config plus relevant test or observed command result | State revision and execution limits; code alone may be incomplete |
| Planned behavior | Approved spec, ADR, or requirement | Explicitly label proposed/planned; never say it already works |
| Decision/rationale | Accepted ADR or maintainer decision | Link the decision and status |
| External tool behavior | Primary documentation or release source | Record URL, observed version, and verification date |
| Operational/non-software fact | Owner-approved record, policy, experiment, or authoritative source | State provenance and confidentiality limits |
| Inference | Relevant inspected sources | Label inference; state uncertainty |

Prefer commit-pinned repository URLs for version-sensitive evidence when a remote
is known, otherwise use relative paths with symbols/headings and a Git revision
in the review. Do not invent repository URLs, commit IDs, execution results, owners,
review dates, benchmark numbers, or product behavior. Avoid brittle line numbers
as the only locator. Uncommitted evidence is identified as working-tree evidence.

When sources disagree, report the conflict. Code/tests explain observed behavior;
specifications describe intent; neither silently replaces the other. Resolve or
clearly qualify the claim before approving it. If evidence is unavailable, omit
the claim, mark it unresolved, or request the missing fact; do not fabricate support.

## Review record

The write and review skills emit Markdown in the conversation by default. They
write a report file only to an explicitly requested path, avoiding generated
report churn in consumer repositories.

Required sections: scope and target revision; inspected sources; claim/evidence
table; deterministic checks with command/result/not-run reason; semantic findings;
uncertainties and disposition. Claim table columns: `Claim/location`, `Source`,
`Evidence kind/revision`, `Result`, `Action`. Results: `supported`, `planned`,
`inference`, `unsupported`, or `conflicting`. Overall disposition: `ready`,
`changes required`, or `incomplete`. Missing tools/evidence cannot be reported as
passing. An intentional example of unsupported prose must be labelled as an example.

## Policy extension and maintenance

`.ai-docs/policy.md` contains the managed baseline. `project.md` holds audience,
language, terminology, known evidence locations, existing index links, and local
additions. Local instructions may tighten the baseline; any weakened evidence
requirement must be explicitly disclosed in the review, not silently inferred.

Each content change updates its routing entry when needed. Review freshness on
relevant changes and before publication, not via arbitrary automatic expiry.
The future maintenance skill consumes an explicit Git range and declared evidence
routes; it does not invent a reliable dependency graph from citations alone.
