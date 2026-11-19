# Release checklist

Maintainer checklist for a v0.1.0 release. Publication (push, tag, hosted release) needs
separate explicit authorization; completing this checklist does not publish anything.

- Baseline review revision: `f5c90492aa22592d430c4960a8e42b7fee44cf22`, clean tree.
- Independent semantic review revision: `b8aded9f80613c79c8a988c7f4161e5627828e49`.
- Current evidence: [hosted run 44503559840](https://github.com/Semtexcz/ai-docs-kit/actions/runs/44503559840),
  [independent review](../tests/scenarios/independent-review-v0.1.0.md), and the
  [documentation audit](audits/v0.1.0-documentation-audit.md).
- The final modified revision is a working tree derived from the baseline. Checks below
  distinguish baseline evidence from final-revision evidence; a baseline result is not
  evidence for later changes.

## 1. Environment

- [x] Pinned tools provisioned from [maintainer setup](maintainer-setup.md) and versions
      recorded in the ledger (2026-11-15 session in [TASKS.md](../TASKS.md)).
- [x] Repository was at the intended baseline revision with a clean working tree before
      the documentation audit.
- [x] `git status` reviewed before and after the baseline checks.
- [x] Final working-tree revision: rerun with Python 3.12.16, Node 24.22.3,
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
- [x] Final working-tree rerun: `python -m unittest discover -s tests -v` exited 0 with
      `Ran 57 tests in 142.215s` and `OK`; `pre-commit run --all-files` passed all five
      hooks; `git diff --check` exited 0. Details are in [TASKS.md](../TASKS.md) and the
      [audit](audits/v0.1.0-documentation-audit.md).

## 3. Scenario evidence

- [x] I01–I06, C01–C03, U01–U05, V01–V08, S01–S03, B01, and A01–A03 passed within the
      56-test baseline run.
- [x] E01 passed; the hosted log records source refs `v0.1.0` → `v0.1.1`, a 38-file
      inventory, preserved foreign/user hashes, and the tool versions.
- [x] Semantic walkthrough records exist for the software and non-software fixtures. The
      2026-11-15 records identify themselves as implementation-agent evidence.
- [x] Independent semantic acceptance records M01–M08 with reviewer, revision, inputs,
      outputs, and results (2026-11-19 review, 8/8 passed).
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
- [x] F1 is corrected separately in `template/.ai-docs/skills/docs-write/SKILL.md.jinja`,
      with rendered-skill regression tests and a bounded implementation-agent
      walkthrough. This correction is not a second independent semantic review.
- [ ] Advisory, not a v0.1.0 gate: independent semantic re-review of the F1 correction.
      The baseline review and the F1 fix are separate evidence; the rendered-skill tests
      and implementation-agent walkthrough verify the output shape, not independent
      semantic quality.

## 6. Release artifacts (not publication)

- [x] Version and provenance recorded for Copier, pre-commit, markdownlint-cli2, Lychee,
      Node, Python, skills-ref, and all action SHAs.
- [x] Licensing reviewed: MIT for original materials; third-party notices preserved.
- [x] Consumer installation instructions are runnable from a local Git source without a
      hosted release.
- [x] Final disposable installation was inspected with a clean diff and passing checks in
      E01.
- [ ] Release tag and GitHub release: not created. They require separate authorization
      and a final-revision hosted run.

## 7. Hosted CI verification

- [x] The corrected maintainer workflow has an observed successful hosted run for
      baseline `f5c9049`: [run 44503559840](https://github.com/Semtexcz/ai-docs-kit/actions/runs/44503559840).
      Lychee installed, all toolchain components were available, the integration suite
      passed, maintainer documentation gates passed, and `git diff --exit-code` was clean.
- [x] The earlier review revision `b8aded9` also passed hosted CI in
      [run 44498410442](https://github.com/Semtexcz/ai-docs-kit/actions/runs/44498410442).
- [ ] Final modified revision: `FINAL REVISION HOSTED CI PENDING`. The changes are not
      committed or pushed, so no hosted result can be claimed for them.

## Sign-off

- Independent semantic review: Codex, 2026-11-19, `b8aded9`, PASS WITH CONDITIONS;
  serving profile not attested. One minor finding, F1, corrected afterward.
- Documentation audit and F1 repair: implementation agent, 2026-11-19, working tree
  derived from `f5c9049`; local gate results are recorded in
  [TASKS.md](../TASKS.md) and the [audit](audits/v0.1.0-documentation-audit.md).
- Maintainer release approval: **pending**. Requires the final-revision checks above and
  explicit authorization to tag or publish.
