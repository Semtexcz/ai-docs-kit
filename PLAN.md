# Implementation roadmap

## Release target

Deliver `v0.1.0`: an installable, tested Copier template with useful documentation
guidance and deterministic Markdown/link checks. This target was implemented and tested
on Ubuntu Linux; see [CHANGELOG.md](CHANGELOG.md), [TASKS.md](TASKS.md), and the
[release checklist](docs/release-checklist.md).

## MVP deliverables

- A hook-free Copier template; dedicated `.copier-answers.ai-docs-kit.yml`.
- `.ai-docs/` for toolkit policy, project context, skill catalog, three skills,
  authoring assets, and validation configuration.
- A configurable, minimally seeded documentation home, default `docs/ai-docs/`.
- A concise routing index and progressive disclosure conventions.
- `docs-discover`, `docs-write`, and `docs-review` in standard skill directories.
- Evidence-based writing and review, including unsupported and conflicting claims.
- markdownlint-cli2 and Lychee, with local files and local fragments checked offline.
- A standalone pre-commit configuration usable without installing Git hooks.
- An opt-in GitHub Actions workflow supplied as a copyable example, plus actual
  maintainer CI that tests generated projects.
- New/existing/non-software installations, template composition, upgrade/conflict
  tests, meaningful negative scenarios, and a concrete end-to-end acceptance test.
- User instructions for installation, updates, tool provisioning, agent activation,
  extending validation to existing docs, and optional integration by references.

## Deferred scope

F01–F05 in [TASKS.md](TASKS.md) cover the remaining three skills, opt-in Vale,
and an optional Zensical profile. The six skill contracts are designed now.
No default website, deployment, external-link CI gate, automatic impact scanner,
custom config parser, hosted AI integration, or shared-file merger belongs in v0.1.0.

## Milestones and exit gates

| Milestone | Tasks | Exit evidence |
| --- | --- | --- |
| Toolchain and fixtures | T01–T02 | Pinned tools and isolated temporary-Git harness |
| Template and content contracts | T03–T05 | Renderable ownership-safe scaffold and policy |
| Agent workflows | T06–T08 | Three portable skills with examples |
| Deterministic checks and adoption | T09–T13 | Real CLIs, standalone config, installation guide, inert CI example |
| Compatibility and negative cases | T14–T19 | Render, composition, upgrade, validator, skill, integration evidence |
| Maintainer automation | T20 | Maintainer CI runs all required checks |
| MVP acceptance | T21–T22 | End-to-end test, release checklist, completed task evidence |

The numeric task order is a valid serial execution order. Independent readiness is
defined by each task's explicit dependencies, not by these broad milestone ranges.

## Implementation policy

Do not decide the architecture again during implementation. Mechanical work such
as resolving action SHAs, a Python patch release, and a validator commit is assigned
to T01 and must retain the selected tools and runtime families. A verified
incompatibility requires a documented adjustment, not silent substitution.

Use real CLIs in integration tests. Dependency/bootstrap downloads may need network;
the warmed default validation run must not request remote document URLs.
Semantic review uses recorded rubric scenarios; it is not a model call in CI.

See [handoff](IMPLEMENTATION_HANDOFF.md), [test strategy](docs/architecture/testing.md),
and [planning review](docs/planning-review.md) for completion gates and limitations.
