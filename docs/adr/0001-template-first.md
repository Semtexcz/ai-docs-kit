# Template-first distribution

- Status: accepted
- Date: 2026-11-15

## Context and drivers

The toolkit must install into varied projects and evolve with Git while minimizing
custom code and assumptions about the consumer's language.

## Options

An application package with a custom installer; a one-time skeleton; a Copier
template distributing Markdown, skills, and native tool configuration.

## Decision

Use a Git-versioned Copier template with `template/` as its only render root.
No application package, runtime library, agent runner, config translation layer,
template hooks, migrations, or executable extension is part of the MVP.
Copier is the selected existing lifecycle tool; see its
[update model](https://copier.readthedocs.io/en/stable/updating/).

## Consequences

Most implementation is original guidance and configuration. Tool installation is
explicit, and consumers need tooling runtimes even when their project has no
Python/JavaScript source. Complex relocation/migrations remain out of scope.
Original Python is permitted only in maintainer integration tests.

## Confirmation

T03/T14 assert render-root separation and no trust requirement. T16 exercises
updates. [System architecture](../architecture/system.md) defines the boundaries.
