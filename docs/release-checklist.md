# Release checklist

Maintainer checklist for a v0.1.0 release. **Release readiness** and **release
publication** are distinct: this checklist records readiness evidence. Publication
(pushing new commits, creating a tag, or publishing a GitHub release) needs separate
explicit authorization; completing this checklist does not publish anything.

- Documentation-audit baseline: `f5c90492aa22592d430c4960a8e42b7fee44cf22`, clean tree.
- Independent semantic review revision: `b8aded9f80613c79c8a988c7f4161e5627828e49`.
- Correction commit: `3a158cde2e3359f698ac66a7ce9c86ac621b81c5`, containing the
  documentation audit corrections and the F1 write-output fix.
- Current evidence: [hosted run 44508800002](https://github.com/Semtexcz/ai-docs-kit/actions/runs/44508800002)
  for `3a158cd`, [baseline run 44503559840](https://github.com/Semtexcz/ai-docs-kit/actions/runs/44503559840)
  for `f5c9049`, [independent review](../tests/scenarios/independent-review-v0.1.0.md),
  and the [documentation audit](audits/v0.1.0-documentation-audit.md).
- Each hosted result verifies only its recorded revision. The independent reviewer
  evaluated `b8aded9`, not the later F1 correction.
- No v0.1.0 tag or GitHub release exists.

## 1. Environment

- [x] Pinned tools provisioned from [maintainer setup](maintainer-setup.md) and versions
      recorded in the ledger (2026-11-15 session in [TASKS.md](../TASKS.md)).
- [x] Repository was at the intended documentation-audit baseline revision with a clean
      working tree before the audit.
- [x] `git status` reviewed before and after the baseline checks.
- [x] Correction commit `3a158cd`: rerun with Python 3.12.16, Node 24.22.3,
      Copier 9.19.1, pre-commit 4.7.0, markdownlint-cli2 0.24.1, Lychee 0.24.2,
      skills-ref 0.1.0, and Git 2.53.0; `git status` recorded before and after.

## 2. Automated gates

- [x] `python -m unittest discover -s tests -v` passed for baseline `f5c9049` in hosted
      CI run `44503559840`: `Ran 56 tests in 96.856s` followed by `OK`.
- [x] `pre-commit run --all-files` passed in the same hosted run, and
      `git diff --exit-code` confirmed that the gates rewrote no files.
- [x] No required integration test was excluded; missing required tools fail instead of
      skipping (`tests/support.py`).
- [x] `tests/test_lychee_install.py` executed the maintainer and consumer Lychee install
      steps against the pinned release asset, reported 0.24.2, and rejected a tampered
      checksum (A03) in the hosted run.
- [x] Rendered output contained no maintainer files, raw Jinja, executables, hooks, or
      activated workflows; I01/I06/S03 passed within the hosted suite.
- [x] Correction commit `3a158cd` passed hosted CI in
      [run 44508800002](https://github.com/Semtexcz/ai-docs-kit/actions/runs/44508800002):
      `Ran 57 tests in 71.494s` followed by `OK`, all five maintainer documentation hooks
      passed, and `git diff --exit-code` was clean. The job log records E01 with source
      refs `v0.1.0` → `v0.1.1` and preserved foreign/user hashes.
- [x] Local rerun on the closure working tree derived from `3a158cd`:
      `python -m unittest discover -s tests -v` exited 0 with
      `Ran 57 tests in 165.380s` and `OK`; `pre-commit run --all-files` passed all five
      hooks; `git diff --check` exited 0. This working tree is uncommitted, so the
      result is local evidence only. A new commit needs its own hosted run.

## 3. Scenario evidence

- [x] I01–I06, C01–C03, U01–U05, V01–V08, S01–S03, B01, and A01–A03 passed within the
      56-test baseline run.
- [x] S04 was added after that run and passed in the 57-test run for `3a158cd`. It checks
      the rendered `docs-write` review-record contract on default and custom roots.
- [x] E01 passed in both hosted runs; the logs record source refs `v0.1.0` → `v0.1.1`, a
      38-file inventory, preserved foreign/user hashes, and the tool versions.
- [x] Semantic walkthrough records exist for the software and non-software fixtures. The
      2026-11-15 records identify themselves as implementation-agent evidence.
- [x] Independent semantic acceptance records M01–M08 with reviewer, revision, inputs,
      outputs, and results (2026-11-19 review, 8/8 passed for `b8aded9`).
- [x] Green syntax checks are not presented as factual correctness in the README,
      architecture, policy, review asset, or audit.

## 4. Documentation

- [x] Installation, update, activation, tool provisioning, scope extension, and limits
      match observed behavior on Ubuntu Linux.
- [x] README status, CHANGELOG, and TASKS.md ledger describe the delivered scope and
      distinguish implementation completion from a published release.
- [x] No fake release URL, moving ref, or claim of untested platform or sibling
      compatibility is used.
- [x] Optional integrations are documented as absent by default and require explicit
      consumer action.
- [x] The documentation audit recorded navigation, evidence, consistency, template, and
      agent-guidance findings with a remediation matrix.

## 5. Independent semantic acceptance

- [x] An independent reviewer, independent of the implementation agent, reproduced the
      inputs in [the review packet](../tests/scenarios/independent-review-packet.md) and
      recorded M01–M08 results.
- [x] The reviewer was Codex, not the implementing Cline/DeepSeek agent. The requested
      GPT-6.1-Sol model and HIGH reasoning setting could not be attested; the review
      records that limitation instead of asserting the profile.
- [x] The 2026-11-15 walkthrough records are cited only as implementation-agent evidence,
      not as independent verification.
- [x] Result is recorded as `PASS WITH CONDITIONS` for `b8aded9`, with one nonblocking
      minor finding (F1, write output contract).
- [x] F1 is corrected in `3a158cd` in `template/.ai-docs/skills/docs-write/SKILL.md.jinja`,
      with rendered-skill regression tests and a bounded implementation-agent
      walkthrough. This correction is not a second independent semantic review.
- [ ] Advisory, not a v0.1.0 gate: independent semantic re-review of the F1 correction.
      Not performed. The independent reviewer assessed `b8aded9` only; the rendered-skill
      tests and implementation-agent walkthrough verify output shape, not independent
      semantic quality.

## 6. Release artifacts (not publication)

- [x] Version and provenance recorded for Copier, pre-commit, markdownlint-cli2, Lychee,
      Node, Python, skills-ref, and all action SHAs.
- [x] Licensing reviewed: MIT for original materials; third-party notices preserved.
- [x] Consumer installation instructions are runnable from a local Git source without a
      hosted release.
- [x] Final disposable installation was inspected with a clean diff and passing checks in
      E01.
- [ ] Release tag and GitHub release: not created. They require separate authorization;
      hosted CI for `3a158cd` is complete, but this checklist does not publish anything.
- [ ] Documentation-closure changes: not committed or pushed. Publication is
      unauthorized. If committed, the new commit requires its own hosted run.

## 7. Hosted CI verification

- [x] The corrected maintainer workflow has an observed successful hosted run for
      baseline `f5c9049`: [run 44503559840](https://github.com/Semtexcz/ai-docs-kit/actions/runs/44503559840).
      Lychee installed, all toolchain components were available, the integration suite
      passed, maintainer documentation gates passed, and `git diff --exit-code` was clean.
- [x] The earlier review revision `b8aded9` also passed hosted CI in
      [run 44498410442](https://github.com/Semtexcz/ai-docs-kit/actions/runs/44498410442).
- [x] Correction commit `3a158cd` passed hosted CI in
      [run 44508800002](https://github.com/Semtexcz/ai-docs-kit/actions/runs/44508800002).
      GitHub reported `conclusion: success`; every setup, test, documentation-gate, and
      no-rewrite step succeeded. The log records 57 tests and all five passed hooks.
- [ ] Documentation-closure working tree after `3a158cd`: not hosted. If it is committed,
      that new commit requires its own successful run before being declared fully
      verified. This is a publication-step requirement, not a defect in `3a158cd`.

## Sign-off

- Independent semantic review: Codex, 2026-11-19, `b8aded9`, PASS WITH CONDITIONS;
  serving profile not attested. F1 was corrected afterward in `3a158cd` and was not
  independently re-reviewed.
- Documentation audit and F1 repair: implementation agent, 2026-11-19; audit baseline
  `f5c9049`; corrections committed as `3a158cd` and hosted-verified in run `44508800002`.
- Release readiness: complete for `3a158cd`, with the optional independent re-review of
  the F1 correction still open.
- Maintainer release approval: **pending**. Publication requires explicit authorization.
