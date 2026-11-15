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
- [ ] Rendered output contains no maintainer files, raw Jinja, executables, hooks, or
      activated workflows.

## 3. Scenario evidence

- [ ] I01–I06, C01–C03, U01–U05, V01–V08, S01–S03, B01, A01–A02 pass.
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

## 5. Release artifacts (not publication)

- [ ] Version and provenance recorded for Copier, pre-commit, markdownlint-cli2, Lychee,
      Node, Python, skills-ref, and all action SHAs.
- [ ] Licensing reviewed: MIT for original materials; third-party notices preserved.
- [ ] Consumer installation instructions runnable from a local Git source without a
      hosted release.
- [ ] Final disposable installation inspected with a clean diff and passing checks.

## Sign-off

- Reviewer:
- Date:
- Revision:
- Result: pass, or the exact failing item and the follow-up task.
