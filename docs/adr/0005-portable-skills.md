# Portable Agent Skills and explicit discovery

- Status: accepted
- Date: 2026-11-15

## Context and drivers

Capabilities must be reusable across agents. Host discovery paths vary, and shared
agent directories can already be owned by other templates or users.

## Options

Vendor commands and wrappers; automatic copies/symlinks into several host paths;
standard skill directories with a portable catalog and explicit invocation.

## Decision

Implement standard `SKILL.md` packages in `.ai-docs/skills/`, following the
[format specification](https://agentskills.io/specification). Use direct file
reading as the baseline and optional consumer-owned host search-path configuration.
MVP implements discovery, writing, and review; the other three contracts are deferred.

## Consequences

Automatic discovery is not universal and is not promised for the namespaced path.
No duplicated skill copies or synchronization code is introduced. A selected skill
must work independently using common policy and assets. It does not grant tools
or choose/delegate to models.

## Confirmation

T06–T08/T18 check packaging, links, examples, and scenarios. All six interfaces are
defined in [skill contracts](../architecture/skills.md).
