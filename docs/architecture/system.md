# System and component boundaries

## Design

The distribution is a Git-versioned Copier template, not an application package.
Copier renders portable Markdown and native validator configuration. Agents read
skills and relevant evidence; maintainers invoke existing tools. No daemon,
database, hosted service, application runtime, or custom executable is installed.

```text
ai-docs-kit Git tag
  copier.yml + template/
           | Copier copy/update
           v
consumer Git repository
  .copier-answers.ai-docs-kit.yml   installation identity
  .ai-docs/                       policy, skills, tool configuration
  docs/ai-docs/                   default content and routing index
           |                      |
           | agent + evidence     | pre-commit -> existing CLIs
           v                      v
  proposed/reviewed Markdown      syntax and link findings
           \______________________/
                    Git review
```

The diagram shows relationships only; it does not introduce an execution engine.

## Components

| Component | Responsibility | Implementation medium |
| --- | --- | --- |
| Installer/updater | Parameters, rendering, answers, merge behavior | Copier configuration and Jinja |
| Policy and context | Evidence, ownership, terminology, retrieval rules | Markdown |
| Content and routing | Reader-facing docs and small linked indexes | Markdown |
| Agent capabilities | Discovery, writing, review; later three more | Standard skill directories |
| Syntax validation | CommonMark/Markdown style checks | markdownlint-cli2 native config |
| Link validation | File existence and local heading fragments | Lychee native config |
| Check entry point | Reuse the same checks locally and in CI | pre-commit native config |
| Compatibility assurance | Real installation/update/composition tests | Maintainer-only Python unittest |
| Publication/style extras | Optional profiles after MVP | Existing CLIs and config |

## Repository separation

Implementation adds `copier.yml`, `template/`, `tests/`, `requirements-dev.txt`,
`.pre-commit-config.yaml`, and `.github/workflows/ci.yml` to this maintainer repository.
Only `template/` renders into consumers (`_subdirectory: template`). The root
planning documents, test fixtures, development requirements, and maintainer workflow
are excluded by construction. There is no publishable Python package or root Node
package. Tool runtimes do not imply a consumer project language.

## Original work versus reused work

Original deliverables are policy, skill instructions, authoring assets, Jinja
templates, configuration, examples, and integration tests. No original runtime
code is required. Test helpers may create temporary repositories, invoke subprocesses
with argument lists, capture exit status, and compare file inventories and hashes.
They must not become an alternative installer or validator.

No generic `.ai-docs/config.yml` is introduced. User choices live in Copier answers;
prose context lives in `.ai-docs/project.md`; each tool reads its own configuration.
This avoids a configuration schema and translation layer.

## Ownership boundary

The kit is independently useful without ai-project-planner, ai-devkit, OpenSpec,
Vale, Zensical, GitHub, or an AI vendor. Existing repository instructions govern
agent permissions. Skills provide procedures, not permission grants. Optional
integration means explicit links and user-controlled configuration, never a shared
file rewrite. See [installation](installation.md) for the exact file surface.
