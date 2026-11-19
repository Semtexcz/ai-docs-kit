# Release checklist

Maintainer checklist for a v0.1.0 release. Publication (push, tag, hosted release) needs
separate explicit authorization; completing this checklist does not publish anything.

## 1. Environment

- [ ] Pinned tools provisioned from [maintainer setup](maintainer-setup.md) and versions
      recorded in the ledger.
- [ ] Repository is at the intended revision with unrelated changes preserved.
- [ ] `git status` reviewed before and after all checks.

## 2. Automated gates

- [ ] `python -m unittest discover -s tests -v` passes with no skips for required tools.
- [ ] `pre-commit run --all-files` passes and rewrites no files.
- [ ] No required integration test is excluded; unavailable tools fail the run.
- [ ] `tests/test_lychee_install.py` executes the maintainer and consumer Lychee install
      steps against the pinned release asset, reports 0.24.2, and rejects a tampered
      checksum (A03).
- [ ] Rendered output contains no maintainer files, raw Jinja, executables, hooks, or
      activated workflows.

## 3. Scenario evidence

- [ ] I01–I06, C01–C03, U01–U05, V01–V08, S01–S03, B01, A01–A03 pass.
- [ ] E01 passes and its recorded evidence includes source refs, tool versions, final
      inventory, and preserved hashes.
- [ ] Semantic walkthrough records for software and non-software fixtures cover M01–M08
      with reviewer, revision, inputs, outputs, and results.
- [ ] Green syntax checks are not presented as factual correctness.

## 4. Documentation

- [ ] Installation, update, activation, tool provisioning, scope extension, and limits
      match observed behavior.
- [ ] README status, CHANGELOG, and TASKS.md ledger describe the delivered scope.
- [ ] No fake release URL, no moving refs, no claim of untested platforms or sibling
      compatibility.
- [ ] Optional integrations are documented as absent-by-default and require explicit
      consumer action.

## 5. Independent semantic acceptance

- [ ] An independent reviewer (GPT-6.1-Sol) reproduces the inputs in
      [tests/scenarios/independent-review-packet.md](../tests/scenarios/independent-review-packet.md)
      and records M01–M08 results.
- [ ] The 2026-11-15 walkthrough records are cited only as implementation-agent evidence,
      not as independent verification.
- [ ] Status when no independent review has been performed:
      `PENDING INDEPENDENT REVIEW` (current state as of 2026-11-19).

## 6. Release artifacts (not publication)

- [ ] Version and provenance recorded for Copier, pre-commit, markdownlint-cli2, Lychee,
      Node, Python, skills-ref, and all action SHAs.
- [ ] Licensing reviewed: MIT for original materials; third-party notices preserved.
- [ ] Consumer installation instructions runnable from a local Git source without a
      hosted release.
- [ ] Final disposable installation inspected with a clean diff and passing checks.

## 7. Hosted CI verification

- [ ] The corrected maintainer workflow has an observed successful hosted run:
      Lychee installs, all toolchain components are available, the integration suite
      passes, maintainer documentation gates pass, and `git diff --exit-code` is clean.
- [ ] Status when no authorized push has occurred:
      `HOSTED CI VERIFICATION PENDING` (current state as of 2026-11-19).

## Sign-off

- Reviewer:
- Date:
- Revision:
- Result: pass, or the exact failing item and the follow-up task.
