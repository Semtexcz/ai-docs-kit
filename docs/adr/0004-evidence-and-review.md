# Evidence-based claims and separate semantic review

- Status: accepted
- Date: 2026-11-15

## Context and drivers

Markdown can be syntactically valid while claiming unsupported behavior. A source
link may be reachable yet irrelevant. Intended behavior and delivered behavior differ.

## Options

Treat green CI as approval; require citations for every sentence; require inspected
evidence for material claims and a structured semantic review.

## Decision

Use the claim/evidence contract in [documentation](../architecture/documentation.md).
Label plans, inference, missing evidence, and conflicts. Review includes both
deterministic results and semantic findings, with separate status. No automatic
truth score or hosted AI check is added.

## Consequences

Reviews require judgment and can be incomplete. Evidence may be grouped by claim
or procedure rather than cluttering each sentence. No invented test results,
versions, owners, URLs, or implementation facts are acceptable. A working-tree
source is explicitly identified when commit-pinned evidence is unavailable.

## Confirmation

T05/T07/T08 implement the policy. T18's M02–M07 walkthroughs challenge unsupported,
conflicting, planned-only, unexecuted, untrusted, and non-software evidence.
