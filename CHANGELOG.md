# Changelog

All notable changes to ai-docs-kit are recorded here. The project follows a
tag-per-release Copier workflow; consumers select an explicit tag.

## v0.1.0 — 2026-11-15

First implementation. Tested on Ubuntu Linux 26.04 with Copier 9.19.1, pre-commit
4.7.0, markdownlint-cli2 0.24.1, Lychee 0.24.2, Python 3.12.16, and Node 24.22.3.

### Added

- Hook-free Copier template with exactly two questions (`project_name`, `docs_dir`),
  dedicated `.copier-answers.ai-docs-kit.yml` state, native validators, and seed-once
  content for `.ai-docs/project.md` and the documentation root.
- `.ai-docs/` entry point, managed evidence policy, seed-once project context, skill
  catalog, and three portable Agent Skills: `docs-discover`, `docs-write`,
  `docs-review`.
- Authoring assets for pages, reviews, and MADR-inspired decision records.
- Seed-once documentation home with a five-column routing index, a documentation-update
  how-to, and a policy reference.
- markdownlint-cli2 and Lychee native configuration plus a standalone pre-commit
  configuration that checks both roots on every run without installing Git hooks.
- Inert consumer examples: an optional agent routing snippet and a fenced GitHub
  Actions workflow with pinned actions and offline checks.
- Maintainer toolchain pins, provisioning record with checksums and action SHAs, MIT
  license, maintainer pre-commit gates, and GitHub Actions CI.
- Integration tests for installation, preservation, validation, composition, upgrades,
  skill packaging, integration boundaries, and the end-to-end acceptance scenario.
- Semantic walkthrough rubric and recorded software/non-software walkthroughs.

### Limitations

- Only Ubuntu Linux was exercised; macOS and Windows are unverified.
- `docs_dir` is immutable within the v0.1 lifecycle; relocation is not implemented.
- Remote URL checks, Vale, Zensical, and the three deferred skills are out of scope.
- Installation is not transactional; declined collisions can leave a partial result,
  and ai-docs-kit makes no rollback guarantee.
- No compatibility claim is made for specific ai-project-planner, ai-devkit, or
  OpenSpec releases.
