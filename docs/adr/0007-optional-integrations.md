# Optional integrations by reference and deferred publication

- Status: accepted
- Date: 2026-11-15

## Context and drivers

The project must remain independent from planning/development kits and avoid a
publication stack that is unnecessary for a useful Git-native MVP.

## Options

Bundle planning, style, and publishing frameworks; require one ecosystem; expose
small reference interfaces and defer optional profiles.

## Decision

Use references to sibling toolkit evidence and optional OpenSpec specs. Do not
initialize or mutate their trees. Use MADR-inspired original Markdown decisions.
Design all six skills now; defer structure/maintenance/publication implementation,
Vale prose-style gates, and Zensical publication configuration until after MVP.

## Consequences

No sibling toolkit, OpenSpec CLI, Vale, renderer, deployment, or AI API is required.
This repository stores OpenSpec-compatible requirement/scenario files without
adding another progress ledger. Specific sibling releases remain unverified.
Future renderer/style profiles need explicit versions, tests, and scoped ownership.

## Confirmation

T19 verifies absent/present sibling independence; F01–F05 define follow-up work.
See [integration contracts](../architecture/integrations.md) and
[tool research](../research/tooling.md) for current primary sources.
