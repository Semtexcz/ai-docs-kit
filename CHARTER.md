# Project charter

## Purpose

ai-docs-kit helps people and agents create, organize, validate, review, and maintain
documentation that readers can use and whose material claims can be checked.
It is independently installable into a new or existing Git repository.

## Users and outcomes

Maintainers adopt a small documentation baseline without changing their application
toolchain. Contributors discover the relevant page and evidence before editing.
Agents receive bounded, reusable instructions. Reviewers can distinguish checked
facts, proposed behavior, and unresolved questions.

Software projects are the initial audience. The content model also accommodates
research, operations, policy, and other projects with documents and evidence.
Neither Python source files nor any application runtime are required in consumers.

## Principles

1. Reuse established tools; prefer configuration, templates, CLIs, and Agent Skills.
2. Use Markdown as the canonical, Git-reviewable content format.
3. Apply Diátaxis to reader needs without requiring four empty directory trees.
4. Use Copier for installation and versioned upgrades.
5. Package agent capabilities using the open `SKILL.md` format.
6. Separate agent judgment from deterministic checks and label each result honestly.
7. Trace material claims to inspected evidence; expose uncertainty and conflicts.
8. Keep dependencies, custom code, and automation small and justified.
9. Support incremental adoption and independently installed Copier templates.
10. Provide concise entry points and selective retrieval instead of whole-repository loading.
11. Preserve consumer ownership of content and shared configuration.
12. Work without a hosted AI service, API key, vector database, or agent orchestrator.

## Scope

The toolkit owns documentation conventions, evidence rules, agent guidance,
document templates, validation configuration, and optional publication preparation.
It supplies a repeatable installation and upgrade path and tests that path.

The MVP includes discovery, writing, and review skills. Structure, maintenance,
and publication skills have contracts in this plan and follow after the MVP.

## Boundaries and non-goals

ai-project-planner owns requirements, specifications, planning, and task management.
ai-devkit owns implementation, testing standards, and software engineering practice.
ai-docs-kit can link to their artifacts as evidence without requiring either toolkit.
Their current formats are not assumed or claimed compatible without inspection.

This project does not implement a planner, test runner, generic linter, link checker,
agent execution engine, documentation truth detector, RAG service, or deployment platform.
It does not promise that a green CI result establishes factual correctness.
It does not automatically reorganize existing docs, merge shared configuration,
publish content, or run commands copied from untrusted documents.

## Success and evolution

The MVP is complete only when a clean installation, an existing-project installation,
independent-template composition, upgrades, failure cases, and the end-to-end
acceptance scenario pass. See [test strategy](docs/architecture/testing.md).

Scope changes require a recorded decision and updates to specifications and tasks.
The project uses MIT for original toolkit materials; implementation adds the license
and preserves any third-party notices. Consumer content retains its own licensing.
