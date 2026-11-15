# Real integration tests and bounded toolchain pinning

- Status: accepted
- Date: 2026-11-15

## Context and drivers

A template's main behavior appears during rendering and updating real repositories.
Mocking those tools would miss preservation and merge failures. LLM behavior cannot
be made deterministic by a normal CI assertion.

## Options

Snapshot-only tests; a dedicated testing framework; standard-library integration
tests invoking real CLIs plus separate recorded semantic walkthroughs.

## Decision

Use Python unittest and temporary tagged Git repositories. Run installation,
composition, upgrade, validator-negative, and end-to-end scenarios. Use the upstream
skill reference validator as a pinned maintainer-only format check; it is described
as demonstration-only in its [README](https://github.com/agentskills/agentskills/blob/main/skills-ref/README.md).
Record semantic walkthroughs separately; no model API is added to CI.

## Consequences

The test suite needs actual tool provisioning and must not skip required tools.
T01 resolves immutable action/validator references and runtime patch versions within
the selected baseline. Initial execution support is Linux; portability beyond it
is unverified until tested. No framework or custom validator is added.

## Confirmation

T01/T02/T14–T22 implement [the test protocol](../architecture/testing.md), including
E01. CI must test both positive and negative behavior, not only file existence.
