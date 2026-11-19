# Changelog

All notable changes to ai-docs-kit are recorded here. The project follows a
tag-per-release Copier workflow; consumers select an explicit tag.

## Unreleased — corrective pass (2026-11-19)

### Fixed

- GitHub Actions failed before any check ran because `taiki-e/install-action` does not
  support Lychee. The maintainer workflow and the inert consumer example now install the
  pinned `lychee-v0.24.2` `x86_64-unknown-linux-gnu` release archive and verify its
  published SHA-256 before extracting only the binary. Version 0.24.2, the archive name,
  and the checksum stay pinned; no fallback or pipe-to-shell installation is used.
- The consumer example continued to propagate the broken installer and is corrected with
  the same verified mechanism.
- F1 from the independent review: the `docs-write` output record now matches the review
  contract in `docs/architecture/documentation.md`, `policy.md`, and `review.md`. It
  includes inspected sources, deterministic check results, semantic findings,
  uncertainties, and an explicit `ready`, `changes required`, or `incomplete`
  disposition. Source-inspected command behavior is recorded as `inference` with
  `not verified` in the Action, not as supported execution evidence.

### Added

- `tests/test_lychee_install.py` executes both workflow install steps in disposable
  directories, checks the reported version, and rejects a tampered archive (A03).
- `tests/scenarios/independent-review-packet.md` provides reproducible inputs and
  expected outcomes for independent semantic review; the completed review is recorded
  separately.
- `tests/test_skills.py` checks the rendered write-skill output sections, dispositions,
  and inference/execution distinction for default and custom documentation roots.
- `docs/audits/v0.1.0-documentation-audit.md` records the documentation audit,
  remediation matrix, and remaining verification limits.

### Documentation

- `TASKS.md` no longer claims that all tasks are unstarted and records this corrective
  pass separately from the historical 2026-11-15 evidence.
- `AGENTS.md` replaces one developer's local tool paths with a portable rule about
  private data and external actions.
- Toolchain, validation, testing, release-checklist, README, and handoff documents
  describe the corrected installation method and the remaining verification limits.
- Release status cites hosted CI run `44508800002` for the corrective commit `3a158cd`
  and run `44503559840` for baseline `f5c9049`, plus the independent Codex review for
  `b8aded9` (`PASS WITH CONDITIONS`, serving profile not attested). The review is not
  described as pending, and the correction commit is explicitly distinguished from the
  review baseline.

### Verification

- Hosted CI run `44508800002` for commit
  `3a158cde2e3359f698ac66a7ce9c86ac621b81c5` completed successfully: `Ran 57 tests`,
  all five maintainer documentation gates passed, and `git diff --exit-code` was clean.
  This verifies the corrective commit, not a later documentation-only revision.
- The independent semantic review remains scoped to `b8aded9`; it did not evaluate the
  F1 correction. No independent re-review of `3a158cd` was performed.

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
