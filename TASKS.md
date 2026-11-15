# Implementation backlog

All tasks are **not started**. This is the sole progress ledger. Architectural
planning is complete; no implementation task is marked done by document creation.

Execute the first ready task in numeric order. Dependencies are exact task IDs;
`none` means ready initially. Each task includes only its bounded implementation
scope. References to scenario IDs mean the full assertions in
[testing.md](docs/architecture/testing.md), not file-presence-only substitutes.

Common definition of done: scoped artifacts are reviewable, listed acceptance
criteria and tests are satisfied, relevant user documentation is accurate, no
unrelated files changed, and this ledger records exact checks/results. An unavailable
required tool/check leaves the task incomplete. Use `in progress`, `blocked`, or
`done` in the status field and log evidence at the end of this file.

## MVP tasks: 22

### T01 — Establish the maintainer toolchain

- **Status:** done
- **Goal:** Make selected tool versions reproducibly provisionable without consumer application dependencies.
- **Required inputs:** [Research](docs/research/tooling.md), [validation](docs/architecture/validation.md), ADR-0008.
- **Implementation scope:** Add `requirements-dev.txt` with exact Copier 9.19.1/pre-commit 4.7.0 pins and an inspected full-commit `skills-ref` source pin; record resolved dependency versions. Add MIT `LICENSE`, minimal `.gitignore`, and maintainer setup documentation. Resolve Python 3.12/Node 24 patch versions, Lychee 0.24.2 provisioning, and full action SHAs for checkout/setup-python/setup-node/install-action. Use existing installers; no new runtime package, downloader, or lock framework.
- **Dependencies:** none
- **Acceptance criteria:** A clean isolated environment can provision the selected toolchain; versions/refs and provenance are recorded. No consumer package manifest is assumed. Skill validator remains development-only. Unavailable selected versions are reported, not silently replaced. No `latest` or moving refs in final setup instructions.
- **Tests:** Run and record actual version/help commands for Copier, pre-commit, Node, Lychee, and skills-ref; smoke-check validator invocation. No product test success is claimed yet.
- **Definition of done:** Version/provenance record and exact setup commands exist; common definition of done applies.

### T02 — Create isolated Git integration fixtures

- **Status:** done
- **Goal:** Test template behavior without touching the user's repository history or external services.
- **Required inputs:** T01 setup, [testing protocol](docs/architecture/testing.md).
- **Implementation scope:** Add standard-library unittest discovery, `tests/support.py`, and small existing-project/non-software/independent-template fixture inputs. Helpers create temporary repositories/tags, set only local Git identity, invoke argument-list subprocesses with timeouts, and compare inventories/hashes. Snapshot the working template into temporary Git, excluding `.git` and local caches.
- **Dependencies:** T01
- **Acceptance criteria:** Fixtures work in parent paths with spaces; failures include tool output; required tools fail visibly when missing; cleanup is limited to temp paths. No global Git config, source-repository tag, network application setup, or custom validator.
- **Tests:** Smoke-test creation of two local tagged fixture revisions and execution of real Git/selected tool help commands. Run unittest discovery and inspect source repository status afterward.
- **Definition of done:** Harness command is documented and isolated fixture lifecycle is demonstrated; common definition of done applies.

### T03 — Implement the Copier skeleton and questions

- **Status:** done
- **Goal:** Render only the intended consumer surface with dedicated installation state.
- **Required inputs:** [Installation contract](docs/architecture/installation.md), installation spec R01/R03, ADR-0001/0002.
- **Implementation scope:** Add `copier.yml`, `template/`, the dynamic answers-file template, two questions/validators, subdirectory/min-version settings, skip-existing patterns, and completion guidance. No hooks, migrations, extensions, wrappers, or extra questions. This task establishes skeleton files; later tasks supply content.
- **Dependencies:** T01
- **Acceptance criteria:** Default/custom roots render; Copier records source/ref/answers; invalid paths/names are rejected using native validators. All generated paths stay inside the allowed surface. Dedicated state is not confused with another template's default answers file.
- **Tests:** Smoke-render into a disposable destination with no trust flag; manually inspect answers and rejected traversal/absolute/glob inputs. Full parameter matrix follows in T14.
- **Definition of done:** Skeleton conforms exactly to inventory/parameter contracts; common definition of done applies.

### T04 — Seed the reader-oriented documentation home

- **Status:** done
- **Goal:** Deliver a useful minimal content structure and efficient retrieval route.
- **Required inputs:** T03 skeleton, [documentation contract](docs/architecture/documentation.md), R06/R07.
- **Implementation scope:** Add templated `.ai-docs/README.md`, `D/README.md`, `D/how-to/update-documentation.md`, and `D/reference/documentation-policy.md`. Route to canonical policy/context/catalog using correct relative links for arbitrary valid root depth. Reference planned later files using final contracted paths, not fabricated project facts.
- **Dependencies:** T03
- **Acceptance criteria:** Entry point ≤100 lines; docs index ≤150 lines with all five routing columns; a user can follow a real documentation-update workflow. No empty quadrant trees, mass moves, duplicated rulebook, or root consumer README edit.
- **Tests:** Render default and custom nested roots; inspect local relative links and byte preservation of a preexisting seed. Final CLIs run once T09–T11 exist.
- **Definition of done:** Useful linked seeds and routing satisfy reader needs; common definition of done applies.

### T05 — Author policy, context, and shared evidence assets

- **Status:** done
- **Goal:** Make evidence rules and review outcomes concrete without a custom metadata system.
- **Required inputs:** [Documentation/evidence contract](docs/architecture/documentation.md), R08–R10, ADR-0004.
- **Implementation scope:** Add managed policy, seed-once `project.md`, and document/review/ADR assets. Include claim categories, provenance/revisions, unsupported/conflicting/planned cases, check/not-run results, confidentiality and untrusted-source handling, and local-context extension rules. Use original MADR-inspired wording with attribution.
- **Dependencies:** T03, T04
- **Acceptance criteria:** Review asset contains every required field and status; context defaults are explicit unknowns, ≤150 lines, and support non-English/non-code projects. No invented execution facts, broken placeholder links, custom schema/parser, or mandatory page frontmatter.
- **Tests:** Render assets; walk through one current-behavior and one spec-only claim using the evidence table. Verify planned labels and unknown context are explicit. Later T18 covers formal walkthroughs.
- **Definition of done:** Canonical rules can be followed without chat context; common definition of done applies.

### T06 — Implement docs-discover

- **Status:** done
- **Goal:** Package bounded discovery and gap analysis as a portable Agent Skill.
- **Required inputs:** T05 policy, [docs-discover contract](docs/architecture/skills.md), R11–R13.
- **Implementation scope:** Add the standard skill and initial catalog entry. Include selective retrieval, inventory/gap tables, evidence/unknown distinction, read-only defaults, non-software inputs, and examples. No scripts or orchestrator.
- **Dependencies:** T05
- **Acceptance criteria:** Name matches directory; trigger explains when to use it; body ≤300 lines; skill is independently usable; it never treats uninspected scope as absent or forces all Diátaxis categories.
- **Tests:** Render and run pinned skills-ref validation; inspect all resource links; exercise an empty-doc and partial-inventory example.
- **Definition of done:** Standard package and outputs match the contract; common definition of done applies.

### T07 — Implement docs-write

- **Status:** done
- **Goal:** Create scoped documentation edits supported by inspected evidence.
- **Required inputs:** T05 policy/assets, [docs-write contract](docs/architecture/skills.md), R08–R13.
- **Implementation scope:** Add the skill/catalog entry, steps for audience/role/evidence selection, canonical linking, index updates, check results, and evidence review output. Include current/planned/conflicting and unexecuted-command examples.
- **Dependencies:** T05
- **Acceptance criteria:** Standard metadata/body budget pass; no assumption of a previous discovery run; unsupported facts are omitted/qualified/flagged; write scope remains bounded. Commands are not represented as tested without execution evidence.
- **Tests:** Run pinned format validation on rendered skill; walkthrough an evidence-backed page and a spec-only draft; check resource paths on a custom docs root.
- **Definition of done:** Instructions produce the contracted edits and evidence output; common definition of done applies.

### T08 — Implement docs-review and finalize catalog

- **Status:** done
- **Goal:** Review semantic support separately from deterministic tool results.
- **Required inputs:** T05 review asset, T07 writing output contract, [docs-review contract](docs/architecture/skills.md).
- **Implementation scope:** Add skill/catalog entry, severity/disposition rubric, claim-level source inspection, read-only default, and unsupported/conflicting/irrelevant-citation examples. Final catalog lists exactly the three implemented skills and stays ≤80 lines.
- **Dependencies:** T05, T06, T07
- **Acceptance criteria:** Skill works independently; green lint is not semantic approval; unavailable required evidence/checks yields incomplete; outputs include scope/revision/sources/results/findings/uncertainties/disposition. Deferred skills are not advertised as installed.
- **Tests:** Format validation and resource-link inspection; manually review syntactically valid prose containing an invented flag and irrelevant source.
- **Definition of done:** Review package and catalog satisfy R09/R11–R14; common definition of done applies.

### T09 — Configure Markdown validation

- **Status:** done
- **Goal:** Reuse markdownlint-cli2 without adding consumer package management.
- **Required inputs:** [Validation contract](docs/architecture/validation.md), R15, toolchain record.
- **Implementation scope:** Add `.ai-docs/markdownlint-cli2.jsonc` template with native default rules except disabled MD013; document direct CLI invocation and native override precedence. Do not add custom rules or automatic fixes.
- **Dependencies:** T03
- **Acceptance criteria:** Explicit two-root scope is possible; rendered skills/assets/docs can be checked; shared consumer Markdown config is untouched; no claim that base config isolates native overrides.
- **Tests:** Run real markdownlint-cli2 against a rendered sample; a deliberate rule violation fails and repair passes; inspect content hashes for no mutation.
- **Definition of done:** Native config and documented behavior are verified; common definition of done applies.

### T10 — Configure offline link and fragment validation

- **Status:** done
- **Goal:** Catch broken local documentation references using Lychee.
- **Required inputs:** [Validation contract](docs/architecture/validation.md), R16, Lychee baseline.
- **Implementation scope:** Add native `.ai-docs/lychee.toml` and document exact offline/fragment/hidden-file CLI arguments and two-root globs. No downloader, preprocessing, email checking, or skip-missing policy.
- **Dependencies:** T03
- **Acceptance criteria:** Relative files/images and local fragments fail when broken; remote reachability is explicitly unchecked; ordinary Unicode/encoded-space cases use native behavior. Existing root Lychee config stays untouched through explicit config selection.
- **Tests:** Real CLI smoke cases for missing file and cross-page fragment; both repaired versions pass. Full edge and network tests follow in T17.
- **Definition of done:** Native settings and limitations are recorded; common definition of done applies.

### T11 — Assemble the standalone check entry point

- **Status:** done
- **Goal:** Provide the same deterministic checks locally and in CI without installing Git hooks.
- **Required inputs:** T09/T10, [validation hook contract](docs/architecture/validation.md), R17/R18.
- **Implementation scope:** Add namespaced pre-commit config with pinned upstream markdownlint-cli2 and Lychee system hooks. Use Node system runtime, explicit configs/globs, `pass_filenames: false`, `always_run: true`, and read-only check behavior.
- **Dependencies:** T09, T10
- **Acceptance criteria:** Exact standalone command runs both checks over all scoped Markdown, including hidden/new files; no reliance on staged-only selection. Root hook/config files are neither generated nor installed.
- **Tests:** Run `pre-commit validate-config` then the exact standalone command in a rendered committed fixture; break an incoming link via its target and require failure.
- **Definition of done:** Entry-point behavior and prerequisites are documented; common definition of done applies.

### T12 — Document safe installation and agent activation

- **Status:** done
- **Goal:** Make the rendered kit usable in an existing project without implicit integration edits.
- **Required inputs:** Completed seeds/skills/checks and [installation lifecycle](docs/architecture/installation.md).
- **Implementation scope:** Add user-facing maintainer docs and `.ai-docs/examples/AGENTS.snippet.md`; finish rendered entry-point instructions. Cover preflight, preview/copy/update commands, separate answers, seed behavior, stable root, symlink/collision limits, tool provisioning, manual skill reads, native-config precedence, and extending scope to existing docs by explicit config edits.
- **Dependencies:** T04, T05, T06, T07, T08, T11
- **Acceptance criteria:** A reader can install from a supplied actual source/ref, validate, activate a skill, and update without chat context. Instructions contain no fake release URL, force/trust flags, auto-hook install, or false air-gap/transaction claims. The snippet is inert.
- **Tests:** Follow the instructions in a disposable existing project; verify shared-file hashes and inspect skipped existing seeds. Lint completed rendered output.
- **Definition of done:** Adoption guide and activation example are accurate and complete; common definition of done applies.

### T13 — Supply the inert consumer CI example

- **Status:** done
- **Goal:** Let users explicitly adopt the same gate without taking over existing workflows.
- **Required inputs:** T12 adoption docs, T01 selected provisioning and T11 verified command sequence, A02.
- **Implementation scope:** Add `.ai-docs/examples/github-actions.md` with a fenced complete workflow using pinned actions/tool versions, read-only permissions, and exact standalone check command. Explain deliberate activation/copy into a uniquely named workflow and consumer ownership afterward. Do not ship executable workflow YAML in `.github/`.
- **Dependencies:** T12
- **Acceptance criteria:** Render creates no active consumer workflow. Example remains correct for custom documentation roots because its command reads generated config. No deployment/online-link schedule/AI API is included.
- **Tests:** A02; extract example in test via its labelled fenced block, parse with the existing YAML dependency already provided by Copier, and execute equivalent provisioned job commands on a rendered fixture. Check action pins and scopes; don't build a workflow validator.
- **Definition of done:** Accurate inert example and adoption instructions pass; common definition of done applies.

### T14 — Automate render and installation acceptance

- **Status:** done
- **Goal:** Establish real default/custom/existing/non-software installation behavior.
- **Required inputs:** T02 harness, T12 adoption documentation, T13 completed consumer example, scenario inventory I01–I06.
- **Implementation scope:** Add parameterized unittest cases for the entire inventory, question validation, path/link rendering, dedicated state, root-file preservation, seed preservation, absence of executable features, and non-software inputs. Use actual Copier CLI and local tagged sources.
- **Dependencies:** T02, T12, T13
- **Acceptance criteria:** I01–I06 pass; generated projects do not contain maintainer plans or optional runtime artifacts. Test expectations derive from public contracts, not full-tree golden snapshots.
- **Tests:** `python -m unittest discover -s tests -v`; include every invalid-input category, nested custom roots, Unicode name, and spaces in parent paths. Validate generated defaults using the real standalone command.
- **Definition of done:** All required installation scenarios are automated and passing; common definition of done applies.

### T15 — Automate independent-template composition

- **Status:** done
- **Goal:** Prove coexistence through disjoint ownership and independent state.
- **Required inputs:** T14 fixtures, ownership inventory, C01–C03.
- **Implementation scope:** Add synthetic foreign Copier template fixture with its own answers and owned paths, both install orders, separate updates, and declined reserved-path collision tests. Include root configs/workflows/agent-directory sentinel hashes.
- **Dependencies:** T14
- **Acceptance criteria:** Both installs and individual updates preserve foreign bytes/state. A collision decline preserves sentinels; no rollback guarantee or claimed validation of actual sibling releases is inferred.
- **Tests:** C01–C03 using real copy/update and native interaction; run full suite to ensure no order/history dependency.
- **Definition of done:** Composition guarantees and tested limits are evidenced; common definition of done applies.

### T16 — Automate upgrades, preservation, and conflicts

- **Status:** done
- **Goal:** Verify the supported versioned lifecycle including failures.
- **Required inputs:** T15 composition setup, U01–U05, [update contract](docs/architecture/installation.md).
- **Implementation scope:** Add local tagged A/B template tests for managed upgrades, non-conflicting local edits, overlapping conflicts, skip-existing seed edits/deletion, and dirty-state rejection. Use standard Git/conflict tools rather than a new consumer scanner.
- **Dependencies:** T15
- **Acceptance criteria:** U01–U05 pass; conflicts remain visible and never count as ready based solely on exit code. Missing seeds recreate as documented. Identity stays stable in the supported flow; root relocation is documented as unsupported.
- **Tests:** Real CLI copy/update for each scenario; assert conflict/rejection state and preserved hashes; rerun checks after a resolved clean upgrade.
- **Definition of done:** Upgrade guide matches observed behavior and all scenarios pass; common definition of done applies.

### T17 — Automate validator failures, scope, and offline behavior

- **Status:** done
- **Goal:** Prove deterministic gates catch meaningful defects and fail honestly.
- **Required inputs:** T14 rendered projects, V01–V08, actual selected CLIs.
- **Implementation scope:** Add negative/repair tests for Markdown, files, images, anchors, native override precedence, omitted binaries/config errors, full-scope incoming links, and offline HTTP handling. Count requests with a temporary standard-library HTTP test server after bootstrap; no external endpoint required.
- **Dependencies:** T14
- **Acceptance criteria:** V01–V08 pass with no file rewrites. Broken local links are not hidden by exclusions. Required missing binaries fail visibly. A remote URL gets zero requests from warmed default checks, without claiming cold bootstrap is offline.
- **Tests:** Execute direct CLIs and the exact standalone command; verify failure diagnostics and repair success. Test hidden paths, Unicode headings, and percent-encoded spaces.
- **Definition of done:** Validator success and failure behavior is demonstrated; common definition of done applies.

### T18 — Verify skills and record semantic walkthroughs

- **Status:** done
- **Goal:** Validate portable packages and assess actual guidance without a hosted AI dependency.
- **Required inputs:** T14 outputs, [skill contracts](docs/architecture/skills.md), S01–S03 and M01–M08.
- **Implementation scope:** Add rendered-skill format validation using pinned skills-ref, malformed-copy rejection, resource/catalog/inventory/budget checks, scenario inputs and expected-findings rubric. Record software and non-software walkthroughs for discover/write/review using a human or coding agent; no model-call CI.
- **Dependencies:** T14
- **Acceptance criteria:** All three packages validate and bad copy fails; entry/catalog/index/body budgets hold; every M01–M08 behavior has a recorded reviewer/revision/input/output/result. Do not substitute exact model-response snapshots or source-word matching for semantic evidence.
- **Tests:** S01–S03 run automatically; M01–M08 use documented rubric with retained evidence. Failed walkthroughs result in fixes and a new recorded result.
- **Definition of done:** Both automated packaging and separate semantic acceptance records pass; common definition of done applies.

### T19 — Document and test optional integration boundaries

- **Status:** done
- **Goal:** Support reference-based integration without importing sibling responsibilities.
- **Required inputs:** [Integration contract](docs/architecture/integrations.md), T15/T18, B01.
- **Implementation scope:** Add consumer how-to examples for linking existing planning/dev/OpenSpec evidence through context/indexes. Include absent/present OpenSpec/sibling sentinel cases in tests. Explain intended-versus-delivered behavior. Keep Vale/Zensical as roadmap material only.
- **Dependencies:** T15, T18
- **Acceptance criteria:** No sibling/optional CLI install, initialization, write, schema dependency, or duplicate spec/task tree occurs. Specific sibling releases are labelled unverified. All six design contracts remain available in maintainer docs, but only three skills render.
- **Tests:** B01; render/check a project without integrations and one with an existing `openspec/` sentinel tree. Verify its bytes remain unchanged and evidence links resolve.
- **Definition of done:** Integration examples and tested independence are documented; common definition of done applies.

### T20 — Add maintainer CI and repository quality checks

- **Status:** done
- **Goal:** Exercise all required deterministic and integration checks on changes.
- **Required inputs:** T01 pins, completed T16–T19 tests, A01, [CI policy](docs/architecture/validation.md).
- **Implementation scope:** Add actual maintainer GitHub Actions workflow and root maintainer pre-commit configuration. Provision Python/Node/Lychee, install dev tools, run full unittest suite, lint ordinary maintainer docs, and use upstream conflict-marker/forbidden-rejection checks. Exclude raw Jinja and intentional negative fixtures from ordinary Markdown lint; validate their rendered outputs through tests.
- **Dependencies:** T16, T17, T18, T19
- **Acceptance criteria:** Read-only contents permission, immutable action SHAs, no secrets/AI calls, no pull_request_target, no skipped integration tools, explicit timeout, and Linux support are declared. Actual workflow is maintainer-only and never renders into consumers.
- **Tests:** A01; run all job commands locally in the provisioned environment. Inspect workflow configuration and required test count. Record hosted CI status only if actually available.
- **Definition of done:** Required commands pass and workflow is reviewable; common definition of done applies.

### T21 — Implement the end-to-end installation acceptance test

- **Status:** done
- **Goal:** Prove the complete MVP consumer lifecycle in one executable scenario.
- **Required inputs:** E01 protocol in [testing](docs/architecture/testing.md), completed installation/upgrade/validation/skills/integration/example contracts.
- **Implementation scope:** Add `tests/test_end_to_end.py` implementing every E01 step using only temporary local repositories and real selected tools. Reuse the fixture helpers; do not create a separate product acceptance runner.
- **Dependencies:** T16, T17, T18, T19, T13
- **Acceptance criteria:** Existing-project install, foreign-byte preservation, routing, actual evidence fixture, link/anchor failure and repair, tagged upgrade, and final checks all pass. Captured evidence includes source refs/tool versions. No application install, trust/force flag, or global Git modification.
- **Tests:** E01 alone for clear diagnostics, then full unittest and maintainer gates. Re-run after any required fix; semantic walkthrough records remain a separate gate.
- **Definition of done:** End-to-end result is retained and all required assertions pass; common definition of done applies.

### T22 — Finalize MVP user docs and completion evidence

- **Status:** done
- **Goal:** Leave a truthful, release-ready v0.1.0 toolkit and complete handoff record.
- **Required inputs:** T21 E01 evidence, T20 gates, all MVP acceptance criteria, semantic walkthrough records.
- **Implementation scope:** Replace planning-only README status with actual implemented scope, installation/update/validation examples using a real source or explicit local path, support limits, dependency rationale, extension/integration docs, changelog, and release checklist. Reconcile specs/task ledger with delivered behavior and record final verification. Do not push/tag/publish as part of this task.
- **Dependencies:** T21, T20
- **Acceptance criteria:** All T01–T21 are done with evidence; all automated scenarios and semantic rubric records pass; first-time installation instructions are runnable; no false cross-platform/sibling/publication claims or hidden optional gates. The kit is installable from local Git without a hosted release.
- **Tests:** Run complete maintainer gates once against the final changes; review every MVP requirement mapping and E01 record. Confirm intended output via a final disposable installation and clean diff inspection.
- **Definition of done:** MVP completion definition in the handoff is satisfied and documented; common definition of done applies. Release publication still requires separate authorization.

## Deferred tasks: 5 (outside MVP)

### F01 — Implement docs-structure

- **Status:** not started
- **Goal:** Add scoped information-architecture proposals and safe restructuring guidance.
- **Required inputs:** [docs-structure contract](docs/architecture/skills.md), existing discovery outputs.
- **Implementation scope:** Add standard skill, catalog entry, examples, and route/migration assets; no bulk generator.
- **Dependencies:** T22
- **Acceptance criteria:** Minimal reader-based tree and old→new path plan; no unauthorized moves or forced empty quadrants.
- **Tests:** Format/resource checks and small-project/existing-URL/move-link walkthroughs from the contract.
- **Definition of done:** Tests and walkthroughs pass; catalog/docs updated; common definition of done applies.

### F02 — Implement docs-maintain

- **Status:** not started
- **Goal:** Analyze documentation impact from explicit changes without a scanner service.
- **Required inputs:** [docs-maintain contract](docs/architecture/skills.md), Git range fixtures and evidence routes.
- **Implementation scope:** Standard skill and native Git procedures for changed/deleted/renamed evidence; impact-table asset.
- **Dependencies:** T22
- **Acceptance criteria:** Explicit range and confidence; incomplete analysis for missing history; no guaranteed global impact coverage.
- **Tests:** Format checks and config deletion/rename-only/shallow-history/non-code-change rubric cases.
- **Definition of done:** Contract scenarios pass; catalog/docs updated; common definition of done applies.

### F03 — Implement docs-publish preparation

- **Status:** not started
- **Goal:** Assess publication readiness for Git-native Markdown or a selected existing renderer.
- **Required inputs:** [docs-publish contract](docs/architecture/skills.md), review outputs, chosen target.
- **Implementation scope:** Standard skill, readiness checklist, local-output procedures, catalog entry; no deployment automation.
- **Dependencies:** T22
- **Acceptance criteria:** Git-native use needs no renderer; missing evidence/build is explicit; public/private-source issues are raised without copying secrets.
- **Tests:** Format checks and no-renderer/missing-tool/private-evidence/no-deployment walkthroughs.
- **Definition of done:** Readiness contract passes and authorization boundary is documented; common definition of done applies.

### F04 — Add opt-in Vale profile

- **Status:** not started
- **Goal:** Offer useful, explicitly selected prose-style checks.
- **Required inputs:** [Vale integration boundary](docs/architecture/integrations.md), chosen locale/style/vocabulary and upstream version research.
- **Implementation scope:** Namespaced native config and optional adoption guide; selected established style package, pinned provenance; no custom prose engine.
- **Dependencies:** T22
- **Acceptance criteria:** No default install/gate or root-config overwrite; locale/package/network requirements explicit; no factual correctness claim.
- **Tests:** Good/bad prose, terminology, unsupported locale, package provisioning failure, and existing-config preservation.
- **Definition of done:** Opt-in profile builds/runs with recorded versions and meaningful outcomes; common definition of done applies.

### F05 — Add optional Zensical publication profile

- **Status:** not started
- **Goal:** Render canonical Markdown using an explicitly adopted existing site generator.
- **Required inputs:** [Zensical integration boundary](docs/architecture/integrations.md), refreshed primary-source compatibility research, selected renderer release.
- **Implementation scope:** Namespaced renderer config and local preview/build instructions; preserve existing publication stack; no hosting/deployment.
- **Dependencies:** T22, F03
- **Acceptance criteria:** Build local artifact from canonical sources; output outside source tree; supported-plugin assumptions verified; core install remains renderer-free.
- **Tests:** Versioned clean build, navigation/assets/links, existing-site preservation, missing/unsupported plugin, and no-deployment assertions.
- **Definition of done:** Optional profile has execution evidence and accurate limitations; common definition of done applies.

## Session log

### 2026-11-15 — MVP implementation (T01–T22)

- Implementer: Cline coding agent (DeepSeek model, high reasoning effort).
- Environment: Ubuntu 26.04 LTS, Linux x86_64. Python 3.12.16 and Node 24.22.3
  provisioned with mise; Copier 9.19.1 and pre-commit 4.7.0 in `.venv`;
  markdownlint-cli2 0.24.1 (markdownlint 0.42.1) in an isolated npm prefix; Lychee
  0.24.2 from the release archive with checksum
  `1f4e0ef7f6554a6ed33dd7ac144fb2e1bbed98598e7af973042fc5cd43951c9a`; skills-ref 0.1.0
  from commit `83021e2be457a9b6679148719c1f6074f0ad975e`.
- Status changes: T01–T22 not started → done. F01–F05 remain not started.
- Evidence paths: `tests/`, `tests/scenarios/walkthrough-software.md`,
  `tests/scenarios/walkthrough-non-software.md`, `docs/maintainer-setup.md`,
  `docs/release-checklist.md`.

Commands and exact results:

| Task | Evidence |
| --- | --- |
| T01 | `copier --version` = 9.19.1; `pre-commit --version` = 4.7.0; `node --version` = v24.22.3; `markdownlint-cli2 --version` = v0.24.1; `lychee --version` = 0.24.2; `skills-ref validate --help` exit 0; Lychee archive checksum matched |
| T02 | `test_toolchain.py`: 5 tests OK, including two tagged snapshot revisions in a parent path with spaces and unchanged source status |
| T03 | Render smoke into a disposable repository; answers recorded `_src_path`, `_commit: v0.1.0`, both answers; I05 rejects 21 invalid `docs_dir` values and 9 invalid names without writes; `--pretend` wrote no files |
| T04 | Default and nested roots rendered; I03/I04 verified links, byte-preserved seeds, and recreated missing seed; entry 65 lines, index 66 lines, catalog 34 lines, project context 81 lines at final verification |
| T05 | Policy, project context, and three assets rendered and linted; walkthrough used one current-behavior and one planned claim; context defaults remain explicit unknowns |
| T06–T08 | `skills-ref validate` accepted all three rendered skills; S01–S03 3 tests OK; catalog lists exactly three skills; semantic walkthroughs recorded for discover/write/review |
| T09 | Rendered markdownlint-cli2 config passes V01; MD001 violation fails and repair passes; V08 demonstrates root-config precedence without rewriting it |
| T10 | Rendered Lychee config passes V03/V04/V07; missing file, missing image, same-file and cross-file fragments fail then pass after repair; Unicode and encoded-space targets pass |
| T11 | `pre-commit validate-config .ai-docs/pre-commit-config.yaml` exit 0; standalone command passed in a committed fixture; incoming-link break failed and repair passed |
| T12 | `docs/installation.md` documents preflight, preview/install/update, provisioning, activation, scope extension, composition, removal, and limits; inert snippet rendered |
| T13 | A02 3 tests OK: workflow extracted and parsed, pins/permissions/timeout checked, inert after render, commands pass for default and custom roots |
| T14 | `test_install.py`: 12 tests OK (I01–I06) including existing-project byte preservation, non-software custom root, Unicode name, spaces in parent path |
| T15 | `test_composition.py`: 3 tests OK (C01–C03), both install orders, independent updates, declined collision preserved sentinel |
| T16 | `test_upgrade.py`: 5 tests OK (U01–U05), clean upgrade, non-conflicting edit, visible overlap conflict, seed recreation, dirty rejection |
| T17 | `test_validation.py`: 8 tests OK (V01–V08), zero loopback HTTP requests offline, missing Lychee and invalid config fail visibly |
| T18 | `test_skills.py` 3 tests OK; `test_scenarios.py` 4 tests OK; rendered skills 127/132/154 lines; walkthrough records cover M01–M08 with reviewer, revision, inputs, outputs, results |
| T19 | `test_integrations.py`: 2 tests OK (B01), absent siblings normal, existing OpenSpec/planner/devkit sentinels unchanged, checks pass without sibling CLIs |
| T20 | `test_maintainer_ci.py`: 4 tests OK (A01); `pre-commit run --all-files` passed; workflow uses read-only contents, pinned action SHAs, no secrets, timeout |
| T21 | `test_end_to_end.py` OK: E01 existing consumer + foreign template, evidence page, broken link/fragment repair, tagged v0.1.0→v0.1.1 upgrade, preserved hashes; final inventory 38 files |
| T22 | Full suite `python -m unittest discover -s tests -v` = 50 tests OK in 139.6 s (final rerun after ledger edits: 50 tests OK in 144.6 s); `pre-commit run --all-files` passed; final disposable install rendered 19 files with `validate-config` exit 0, checks pass, clean `git status` |

Changed paths (grouped):

- Template and installation: `copier.yml`, `template/**`, `requirements-dev.txt`, `LICENSE`,
  `.gitignore`.
- Tests and fixtures: `tests/support.py`, `tests/test_*.py`, `tests/fixtures/**`,
  `tests/scenarios/**`.
- Maintainer tooling: `.pre-commit-config.yaml`, `.markdownlint-cli2.jsonc`,
  `.github/workflows/ci.yml`.
- Documentation: `README.md`, `CHANGELOG.md`, `docs/installation.md`,
  `docs/maintainer-setup.md`, `docs/release-checklist.md`, status corrections in
  `AGENTS.md`, `PLAN.md`, `IMPLEMENTATION_HANDOFF.md`, `docs/architecture/*.md`.
- Ledger: `TASKS.md` statuses and this log.

Limitations retained:

- Only Ubuntu Linux was exercised; macOS and Windows are unverified.
- No hosted release, push, or tag was created in this repository. All test tags live in
  disposable temporary repositories.
- Remote URL checking, Vale, Zensical, and F01–F05 are out of scope.
- `docs_dir` relocation and multiple installations per repository are unsupported.
- Declined path collisions can leave a partial result; no rollback guarantee is claimed.
- Compatibility with specific sibling kit releases remains unverified.

Blockers / unresolved questions: none blocking the MVP. Deferred work remains F01–F05.

Next ready task: none in the MVP. F01 requires T22, which is now done; F01–F05 are
deferred by the approved plan and were intentionally not started.

If a test could not run, retain that fact and leave its task incomplete. A scope
change requires an ADR/spec/task update; a session log alone cannot change architecture.
