# Optional integration boundaries

## Independent toolkits

ai-docs-kit may consume links to requirements, specs, tasks, accepted decisions,
source, configuration, and tests. It does not establish a new authoritative copy
of those artifacts. An ai-project-planner requirement can support a planned claim;
ai-devkit implementation/test artifacts can support observed behavior. Neither
toolkit is a dependency and their layouts must be inspected rather than guessed.

Consumers add actual evidence entry points and toolkit indexes to `project.md`
and their documentation routing table. Missing siblings are a normal installation.
No script calls a sibling CLI, changes their configuration, updates their task
state, or depends on their answer schema. Generic independent-template fixtures
test file coexistence; they do not prove compatibility with uninspected releases.

## OpenSpec

Use Markdown requirement/scenario files in this repository's `openspec/specs/` as
implementation contracts. Do not run `openspec init` during ai-docs-kit installation,
ship an `openspec/` tree, or create OpenSpec-specific agent commands in consumers.
This project does not require an OpenSpec runtime for its MVP checks.

In a consumer that already uses OpenSpec, skills can read a bounded requirement
or change as intended behavior. They inspect implementation/test evidence before
describing it as delivered. Links remain references; no spec synchronization,
automatic archive, or duplicate task system is introduced. Consumers own any
OpenSpec project-config context additions. `TASKS.md` is the sole implementation
progress ledger here; do not duplicate its checkboxes in OpenSpec changes.

For optional maintainer validation, the current CLI documents `openspec validate
--specs --strict --no-interactive`. Pin the CLI before running it, assert the
expected four specs were discovered, and record the version. Empty bulk scopes
can succeed, so exit status alone is not evidence that these specs were checked.
This optional check is not an added consumer dependency or MVP release gate.

## MADR

Use a small MADR-inspired Markdown template for architectural decisions. Status,
date, context, drivers, options, outcome, consequences, and confirmation are enough.
No ADR CLI, generator, or dependency is needed. Attribute the source template and
preserve applicable notices if copying upstream content; prefer original concise
wording inspired by its structure. ADRs are governance records, not product specs.

## Vale — F04

Vale is useful for a selected prose style and terminology. It does not prove
grammar, meaning, or factual support. Do not ship an empty or noisy default gate.
After MVP, an opt-in profile can add a namespaced `.ai-docs/vale.ini` with an
explicit style, locale, vocabulary, package versions, provenance, and native
`vale --config` invocation. Existing `.vale.ini` remains user-owned. A non-English
project must not inherit an English style automatically. Validate representative
good/bad prose before adding a CI gate; package sync may require network.

## Zensical — F05

Zensical is the preferred first optional static-site profile to evaluate. Use
canonical Markdown and namespaced configuration, with output outside source paths.
Do not assume all MkDocs plugins work: review supported replacements and renderer
differences for the selected release. Existing publication configuration stays
untouched. A renderer profile must have an explicit build/version compatibility
test, local artifact review, asset/link checks, and public-content review.
No renderer or hosting/deployment dependency is needed for v0.1.0.

## pre-commit and GitHub Actions

The MVP ships native standalone configuration and an inert, copyable workflow
example. Users can adopt either without changing existing hooks. The example
does not install on copy; copying into `.github/workflows/` is an explicit
consumer action. It uses the same default offline gates as local checks.
Online link checks, scheduled checks, auto-fix PRs, AI review, release publishing,
and deployment need separate scope and are deferred.
