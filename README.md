# ai-docs-kit

An installable, Git-native toolkit for evidence-based, agent-assisted documentation.
Markdown is canonical; Copier installs and updates the toolkit; portable Agent Skills
guide reasoning; existing CLIs validate syntax and local links.

**Status: v0.1.0 implementation complete and tested on Ubuntu Linux (2026-11-15).**
No hosted release, registry package, or public URL is required: install from a local Git
clone or any Git URL of this repository. macOS and Windows are unverified for v0.1.

## What it provides

- A hook-free Copier template with two questions, `project_name` and `docs_dir`
  (default `docs/ai-docs`), and a dedicated answers file.
- `.ai-docs/` with an entry point, evidence policy, seed-once project context, skill
  catalog, three skills (`docs-discover`, `docs-write`, `docs-review`), authoring
  assets, native validator configuration, and inert examples.
- A seed-once documentation home: routing index, a documentation-update how-to, and a
  policy reference. Existing documents are indexed by link, not moved.
- Deterministic checks with markdownlint-cli2 and Lychee through a standalone
  pre-commit configuration that never installs Git hooks.
- An inert, copyable GitHub Actions example and real maintainer CI that tests generated
  projects.
- Integration tests that render, check, compose, and upgrade real temporary Git
  repositories with the pinned CLIs.

It does not implement a planner, test runner, generic linter, link checker, agent
runtime, RAG service, or deployment platform. Green checks establish syntax and local
reachability, not factual correctness.

## Requirements

- Git and Copier 9.19.1 to install and update.
- pre-commit 4.7.0, Node.js 24, and a Lychee 0.24.2 binary on `PATH` to validate.
- Python 3.12 only for this repository's maintainer tests; consumers need no Python
  application, Node project, or package manifest.

Exact versions, checksums, and provisioning commands are recorded in
[docs/maintainer-setup.md](docs/maintainer-setup.md).

## Install

```sh
# Source: a local clone of this repository. A Git URL works the same way.
git clone <this-repository-url> /path/to/ai-docs-kit
cd /path/to/your-project

# Preview, then install with the same arguments. No --force or --trust.
copier copy --pretend --vcs-ref <release-tag> \
  --answers-file .copier-answers.ai-docs-kit.yml /path/to/ai-docs-kit .
copier copy --vcs-ref <release-tag> \
  --answers-file .copier-answers.ai-docs-kit.yml /path/to/ai-docs-kit .
```

Answer `project_name` and `docs_dir`, review the diff, fill in `.ai-docs/project.md`,
provision the validation tools, and run:

```sh
pre-commit run --config .ai-docs/pre-commit-config.yaml --all-files
```

Commit the installation. Full preflight, existing-project, non-software, activation, and
update instructions are in [docs/installation.md](docs/installation.md).

## Use with an agent

Read `.ai-docs/README.md`, then the catalog `.ai-docs/skills/README.md`, then one
`SKILL.md` whose trigger matches the task. Host-specific automatic discovery is not
assumed. An optional inert routing snippet is provided at
`.ai-docs/examples/AGENTS.snippet.md`; it is never applied automatically.

## Update

From a clean committed consumer repository:

```sh
copier update --vcs-ref <next-release-tag> \
  --answers-file .copier-answers.ai-docs-kit.yml
```

Managed files merge; seed-once context and documentation keep your edits. Inspect `git
status`, conflict markers, and `.rej` files before declaring success; Copier can exit
zero while conflicts remain. `docs_dir` is stable in v0.1.

## Validation scope

The standalone command checks all Markdown under `.ai-docs/` and `docs_dir/` on every
run: markdownlint-cli2 in check mode (native defaults, line length disabled) and Lychee
offline with fragment checking. Remote URLs are not requested and their reachability is
not claimed. A closer consumer-native configuration can still influence files; `--config`
is a base configuration, not an isolation layer.

## Optional integrations

Link existing requirements, specifications, plans, tests, or OpenSpec-style requirement
files as evidence from `.ai-docs/project.md` and the documentation index. ai-docs-kit
does not install, initialize, or require ai-project-planner, ai-devkit, or OpenSpec, and
it does not claim tested compatibility with specific sibling releases. Vale and Zensical
profiles are deferred.

## Repository layout

| Path | Purpose |
| --- | --- |
| `copier.yml`, `template/` | Installable template; only `template/` renders |
| `tests/` | Real-CLI integration tests, fixtures, and semantic scenario records |
| `docs/architecture/`, `docs/adr/` | Contracts and accepted decisions |
| `docs/installation.md`, `docs/maintainer-setup.md` | User installation guide and pinned toolchain record |
| `openspec/specs/` | Behavioral specifications R01–R20 |
| `TASKS.md` | Implementation ledger and session evidence |
| `CHARTER.md`, `PLAN.md` | Scope and release plan |

## Develop this repository

```sh
python3.12 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
export PATH="$PWD/.venv/bin:$PWD/.tools/bin:$PWD/.tools/npm/node_modules/.bin:$PATH"

python -m unittest discover -s tests -v
pre-commit run --all-files
```

The tests use real Copier, pre-commit, markdownlint-cli2, Lychee, and skills-ref in
temporary Git repositories. They fail, not skip, when a required tool is missing. See
[docs/maintainer-setup.md](docs/maintainer-setup.md) for provisioning and
[docs/release-checklist.md](docs/release-checklist.md) for release gates.

## License

MIT for original toolkit materials; see [LICENSE](LICENSE). Third-party tools keep their
own licenses. Consumer documentation keeps its own licensing.
