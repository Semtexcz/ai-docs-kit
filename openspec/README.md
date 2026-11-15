# Implementation specifications

These four Markdown specifications define the target behavior of v0.1.0. Their
presence does not mean it is implemented. They use OpenSpec's purpose, requirements,
and scenario conventions without initializing an agent integration or requiring
its CLI. Current plans are not described as existing product behavior.

| Specification | Requirement IDs | Contract |
| --- | --- | --- |
| [Installation](specs/installation/spec.md) | R01–R05 | Install, own, compose, update, and preserve |
| [Documentation](specs/documentation/spec.md) | R06–R10 | Content, discovery, evidence, and review |
| [Agent capabilities](specs/agent-capabilities/spec.md) | R11–R14 | Portable workflows and boundaries |
| [Validation](specs/validation/spec.md) | R15–R20 | Checks, automation, tests, and acceptance |

`TASKS.md` is the only implementation progress ledger. No parallel OpenSpec change
task list is needed. Optional CLI validation and the limits of empty-scope success
are described in [integrations](../docs/architecture/integrations.md).
