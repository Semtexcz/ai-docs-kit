# Architecture index

Read the smallest relevant contract before changing a component.

| Question | Document |
| --- | --- |
| What are the components and boundaries? | [System](system.md) |
| Which files can Copier create or update? | [Installation and ownership](installation.md) |
| How are content and claims represented? | [Documentation and evidence](documentation.md) |
| How do all six skills behave? | [Skill contracts](skills.md) |
| What do deterministic checks guarantee? | [Validation](validation.md) |
| How do optional tools and sibling kits compose? | [Integrations](integrations.md) |
| Which automated and manual checks are required? | [Testing](testing.md) |
| Why were these decisions chosen? | [ADRs](../adr/README.md) |
| Which upstream behavior was verified? | [Tool research](../research/tooling.md) |
| What was reviewed before handoff? | [Planning review](../planning-review.md) |

Consumer paths in these documents are contracts for generated output. They do not exist
at this maintainer repository root; they appear only after the template is rendered into
a consumer repository. The maintained implementation lives in `template/` and `tests/`.
