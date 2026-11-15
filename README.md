# ai-docs-kit

A reusable, Git-native toolkit for evidence-based, agent-assisted documentation.
Markdown remains canonical; Copier installs and updates the toolkit; Agent Skills
guide reasoning; existing CLIs validate syntax and links.

**Status: architecture and implementation planning only, 2026-11-15.**
There is no installable template, implemented skill, or passing product test suite yet.

Start implementation with [IMPLEMENTATION_HANDOFF.md](IMPLEMENTATION_HANDOFF.md).
The [charter](CHARTER.md) defines purpose and scope, the
[architecture index](docs/architecture/README.md) routes technical decisions, and
[TASKS.md](TASKS.md) contains the ordered backlog. [PLAN.md](PLAN.md) defines the MVP.

The intended MVP installs into existing repositories without taking ownership of
their root instructions, package manifests, CI workflows, or documentation home.
Its default documentation home is `docs/ai-docs/`; that path can be chosen at installation.

Research and its limits are recorded in [tool research](docs/research/tooling.md).
The [planning review](docs/planning-review.md) maps requirements to tasks and tests.
