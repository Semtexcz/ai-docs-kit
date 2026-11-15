# DeepSeek implementation handoff

## Mission and current state

Implement ai-docs-kit: an independently installable, reusable, Git-native,
agent-assisted documentation toolkit. Use Copier, portable Markdown/Agent Skills,
and established deterministic CLIs. Support software first while permitting
non-software projects. Keep material documentation claims traceable to inspected
evidence. Compose with independently installed templates through disjoint ownership.

This repository contains **planning only** as of 2026-11-15. No template, runtime
skill, consumer config, or automated toolkit test has been implemented or run.
Do not mark implementation work done because its specification exists.

## Authoritative reading order

1. [AGENTS.md](AGENTS.md): repository and environment instructions.
2. [CHARTER.md](CHARTER.md): enduring scope, principles, boundaries, and licensing decision.
3. [PLAN.md](PLAN.md): MVP/deferred distinction and milestones.
4. [ADR index](docs/adr/README.md): accepted architectural decisions.
5. [Architecture index](docs/architecture/README.md): route to the contract relevant to the next task.
6. [Specification index](openspec/README.md): the four behavioral specifications, R01–R20.
7. [TASKS.md](TASKS.md): exact scopes, dependencies, checks, and progress ledger.
8. [Tool research](docs/research/tooling.md) and [planning review](docs/planning-review.md): sources, risks, and coverage.

Current user instructions outrank repository documents. Within the plan, scope
comes from the charter, decisions from accepted ADRs, behavior from specs, detail
from architecture, and work sequence from tasks. If they conflict, document the
conflict and resolve it explicitly; do not silently choose a new architecture.

## Fixed implementation decisions

- Git-versioned Copier template; only `template/` renders. No application package.
- `.copier-answers.ai-docs-kit.yml` for state, `.ai-docs/` for managed guidance/tools,
  `docs/ai-docs/` as configurable default documentation root.
- Exactly two questions: `project_name` and `docs_dir`, with the validators and
  ownership/lifecycle in [installation.md](docs/architecture/installation.md).
- Seed-once user documentation/context; managed policy/config/skills merge via Copier.
- No automatic root README/AGENTS/manifests/hooks/CI/host-skill-directory edits.
- Standard skills live canonically in `.ai-docs/skills/`; portable direct reads
  work without host registration. Supply inert integration examples.
- MVP implements `docs-discover`, `docs-write`, `docs-review`. The three other
  contracts are future work and are not rendered as installed skills.
- Markdown is canonical; linked indexes implement selective retrieval. No schema
  database or custom frontmatter/config parser.
- Existing markdownlint-cli2 and Lychee checks run through standalone pre-commit
  config, with all scoped docs checked each invocation and local links offline.
- No runtime custom Python, orchestrator, installer, validator, renderer, wrapper,
  AI API, or consumer dependency manifest. Original executable code is test glue.
- Optional OpenSpec/sibling references require no initialization or shared-state
  mutations. Vale/Zensical and publication infrastructure are deferred.

## Implementation order

There are **22 MVP tasks, T01–T22**, and **five deferred tasks, F01–F05**.
Numeric T01→T22 order is a valid complete serial order. Start with T01.
Read its exact required inputs, implement only its scope, run its checks, then
record results and continue. Dependencies permit independent work, but no agent
delegation or parallel worker framework is necessary or assumed.

| Stage | Work |
| --- | --- |
| T01–T02 | Pin/provision tools and establish isolated Git fixtures |
| T03–T05 | Copier contract, useful content, evidence policy/assets |
| T06–T08 | Three standard skills and catalog |
| T09–T11 | Native Markdown/link checks and standalone entry point |
| T12–T13 | Installation/activation docs and inert consumer CI example |
| T14–T19 | Render, composition, upgrade, negative-validator, skill, integration acceptance |
| T20 | Actual maintainer CI and repository quality gates |
| T21–T22 | End-to-end lifecycle acceptance and release-readiness record |

Do not start F01–F05 as part of this MVP instruction. Do not invent a new task
system, copy progress checkboxes into OpenSpec, or implement optional publication
to make the MVP seem complete.

## Tooling instructions

T01 establishes an isolated maintainer environment. Use the standard Python
venv/pip workflow; no application `pyproject.toml` or Node project is required.
The selected baseline is Python 3.12, Node 24, Copier 9.19.1, pre-commit 4.7.0,
markdownlint-cli2 0.24.1, and Lychee 0.24.2. Record actual runtime patch versions,
resolved dependencies, full action SHAs, and an inspected skills-ref commit.
These source-verified versions have not been combined/executed during planning.

Use upstream `lychee-system`, not the extra auto-install chain. Provision the
binary explicitly; CI uses the established install-action with an exact version,
checksums enabled, fallback none, and full action SHA. Skills-ref is a
development-only format check; upstream labels it demonstration-only.

Inspect available tools before downloading. Do not substitute a new framework
because one command is unavailable. Record the incompatibility and propose a
bounded correction if necessary. Cold tool bootstrap can need network; default
link checking after bootstrap must not request remote document URLs.

Implementation will establish these actual check commands:

```sh
python -m unittest discover -s tests -v
pre-commit run --all-files
```

The first tests real rendered consumers; the second uses the maintainer root
configuration added in T20. In a generated consumer, the required entry point is:

```sh
pre-commit run --config .ai-docs/pre-commit-config.yaml --all-files
```

Do not invoke nonexistent checks and call them passing before their tasks exist.
Do not install Git hooks automatically. Format/lint raw Jinja by testing rendered
output; intentional invalid fixtures must not poison ordinary maintainer checks.

## Quality gates

Use the complete [test strategy](docs/architecture/testing.md): 29 automated
scenario groups I01–I06, C01–C03, U01–U05, V01–V08, S01–S03, B01, A01–A02,
and E01; plus eight semantic walkthrough scenarios M01–M08.

Required scenarios include existing and non-software projects, both independent
template orders, separate updates, dirty state, conflicts, preserved seeds,
bad filenames/paths, hidden files, local images/fragments, missing tools, native
config precedence, zero check-time HTTP requests, portable skills, and no implicit
optional tool installation. Required integration tests may not silently skip.

T21 implements E01 exactly: existing consumer + foreign template→install→add
evidence-backed docs→pass→break/fix local links and anchors→tagged upgrade→pass,
with byte preservation assertions. It is the concrete installation release gate.

Record semantic walkthroughs separately from CI: a human or coding agent follows
the skills on software and non-software fixtures against expected-findings rubrics.
Record the reviewer, revision, sources, output, and result. No API key or model
snapshot comparison is needed. Green syntax/link checks do not establish truth.

## Autonomy boundaries

Within an authorized implementation request, proceed through ready MVP tasks,
routine fixes, local fixtures, docs, and checks without repeated permission requests.
Preserve unrelated changes. Record blockers accurately and continue independent
ready work where possible.

Stop for an actual unresolved architecture/scope contradiction, necessary destructive
operation, unavailable required permission, or external publication authorization.
Do not change toolkit boundaries, file ownership, runtime/tool families, licensing,
or deferred scope silently. A proposed architectural change needs an ADR and
corresponding spec/task changes before implementing the changed contract.

Do not push, tag/publish releases, deploy, access private mail, change global
configuration, or read unrelated private data under this handoff. Local test tags
belong only in disposable repositories. T22 prepares release artifacts, not publication.

## Progress across sessions

At session start read this handoff, current user instructions, Git status, and
`TASKS.md`. Select the first task whose dependencies are done. Mark it in progress.
At the end record paths changed, exact checks/results, retained evidence, blockers,
and next ready task in the session log. Resume from that state without redoing the
architecture. Do not rely on hidden chat context or a claimed pass from a prior
session without a recorded result. Update stale guidance when implementation
verification changes an observed tool detail, preserving the accepted scope.

## Definition of MVP completion

All T01–T22 are done with check evidence; all R01–R20 and required automated
scenarios pass; three packaged skills and semantic walkthroughs pass; E01 passes;
the user guide is runnable from a local Git source; composition/update/preservation
are tested; version/provenance and platform limits are documented; no optional
publication/style/AI dependency is required. Required tools missing or tests skipped
means incomplete. A hosted release or public repository URL is not required to
demonstrate installability.

## Exact start instruction

Open your coding-agent harness with a DeepSeek coding model in this repository:

```sh
cd '/mnt/Data/1_Drive/1_Projekty/10_Aktivní/Software/ai-docs-kit'
```

Use the following as the initial agent prompt. The harness determines the actual
launch command; no nonexistent `deepseek` CLI is assumed.

```text
Implement the ai-docs-kit MVP in this repository.
Read AGENTS.md and IMPLEMENTATION_HANDOFF.md first, then their authoritative
references and the required inputs for the first ready task in TASKS.md.
Execute T01 through T22, respecting explicit dependencies, accepted ADRs,
specifications, file ownership, tool versions, and the deferred-scope boundary.
Start with T01. Work in real files. Do not redesign the architecture or implement
F01–F05. Run the required checks, retain evidence, and update TASKS.md status and
session log after each completed task. Preserve unrelated changes.
Continue autonomously through the MVP. Surface actual blockers and contradictions;
do not report skipped tests as passing. Do not push, publish, deploy, or tag this
repository. Finish only when the documented MVP completion criteria are satisfied,
or clearly report the exact external blocker preventing further authorized work.
```
