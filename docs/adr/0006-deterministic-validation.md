# Existing deterministic validators and standalone configuration

- Status: accepted
- Date: 2026-11-15

## Context and drivers

The MVP needs repeatable Markdown/link checks without a custom runner or consumer
application dependencies. Hook/CI setup must coexist with existing configuration.

## Options

Custom Python checks; root-manifest scripts; native CLIs with standalone pre-commit
configuration and explicit tool provisioning.

## Decision

Use markdownlint-cli2 and Lychee through pre-commit. Check all Markdown in the
toolkit/doc subtrees on each run. Check local files/fragments offline by default.
Use Lychee's system hook, not its extra bootstrap installer. No auto-fix, hook
installation, external URL requests, or root configuration edits are implicit.
Native behavior and sources are recorded in [research](../research/tooling.md).

## Consequences

Python tooling, Node, and a Lychee binary must be provisioned. Tool bootstrap can
need network even though offline link checking does not. Native Markdown config
overrides can influence selected files. Semantic correctness is outside the gate.

## Confirmation

T09–T11/T17 exercise real success/failure cases, all-scope links, zero check-time
requests, and no mutations. See [validation](../architecture/validation.md).
