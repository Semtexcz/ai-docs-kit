# Planning review

Reviewed 2026-11-15. Outcome: **implementation-ready plan**, with explicit execution
risks and no unresolved blocking scope decision. This review approves the plan's
coverage and consistency; it does not claim an implemented or tested toolkit.

## Requirement coverage

| Requirement | Implementation tasks | Acceptance evidence |
| --- | --- | --- |
| R01 Copier installation without runtime framework | T01–T03, T14 | I01/I06 |
| R02 Existing-file preservation and ownership | T03/T04/T12/T14/T15 | I02/I04/C03 |
| R03 Minimal valid questions and non-software/custom roots | T03/T14 | I03/I05 |
| R04 Independent template composition | T03/T15 | C01/C02 |
| R05 Versioned upgrades and failures | T12/T16 | U01–U05 |
| R06 Useful minimal Diátaxis structure | T04/T14 | I01, reviewed seeded workflow |
| R07 Efficient selective discovery | T04/T06/T18 | S03/M01/M08 |
| R08 Evidence-based claims | T05/T07/T08/T18 | M02–M05 |
| R09 Honest review results | T05/T08/T18 | M03–M05 |
| R10 Canonical Markdown and non-code evidence | T04/T05/T18/T19 | I03/B01/M07 |
| R11 Standard portable skills | T06–T08/T18 | S01–S03 |
| R12 Discovery/writing/review workflows | T06–T08/T18 | M01–M08 walkthroughs |
| R13 Bounded authority and untrusted content | T05–T08/T18 | M06, scope review |
| R14 All six designed; only three MVP skills | T08/T18/T19; F01–F03 later | Exact package inventory, deferred contracts |
| R15 Established Markdown lint | T09/T11/T17 | V01/V02/V08 |
| R16 Local link/fragment validation offline | T10/T11/T17 | V03–V05/V07 |
| R17 Composable check entry point | T11–T15 | A02/I02/C01 |
| R18 Failure behavior and CI | T01/T13/T17/T20 | V06/A01/A02 |
| R19 Real integration tests and semantic separation | T02/T14–T20 | All relevant automated groups plus separate M records |
| R20 Concrete end-to-end acceptance | T21/T22 | E01 and release evidence |

All requested technologies were researched against primary sources in
[tooling.md](research/tooling.md). Diátaxis and MADR inform content; Copier,
Agent Skills, markdownlint-cli2, Lychee, and pre-commit support MVP behavior;
GitHub Actions supplies tested maintainer automation and an opt-in consumer
example. OpenSpec is a compatible local specification format and optional
reference interface. Vale and Zensical are deliberately optional after MVP.

## Dependency and atomicity review

There are 22 MVP tasks and five deferred tasks. Each contains a unique ID, status,
goal, required inputs, bounded scope, exact dependencies, testable acceptance
criteria, tests, and definition of done. Task descriptions name outputs and
scenario IDs rather than leaving architecture to DeepSeek.

T01 is the initial ready task. T01→T22 is a valid topological serial order.
All deferred tasks depend on MVP completion; F05 additionally depends on F03.
No MVP task depends on a deferred task. T22 transitively depends on every other
MVP task. Tests follow the files they verify: in particular the inert consumer
workflow example (T13) precedes complete output-inventory acceptance (T14).

The larger compatibility tasks are bounded by named scenario groups using the
same harness, not open-ended automation projects. Semantic walkthroughs assess
reasoning with rubrics and retained records, rather than claiming deterministic
LLM test coverage.

## Simplicity and decision completeness

- No original runtime code is required; custom executable scope is limited to tests.
- No generic config schema/parser, orchestrator, discovery database, or hosted AI dependency.
- Exact generated file inventory, ownership, question set, supported lifecycle,
  validation scope, check command, evidence model, and six skill interfaces are fixed.
- Tool runtimes are explicit and separate from consumer project language.
- Root/shared integration remains consumer-owned; automatic host registration is not promised.
- Mutable user docs and project context are distinct from managed policy/configuration.
- No automatic migrations or silent path relocation; unsupported changes are documented.
- T01 resolves mechanical version/commit pins within the selected toolchain;
  it cannot choose a different architecture or new framework.
- E01 defines an executable end-to-end installation/reviewable-content/validation/
  upgrade lifecycle without requiring publication infrastructure.

The plan contains 29 automated scenario groups and eight semantic scenario groups.
Its integration tests must assert behavior, preservation, and real failure/repair,
not just that files exist.

## Risks and mitigations

| Risk | Consequence | Mitigation / owner task |
| --- | --- | --- |
| Source-verified tools have not run together | CLI/config differences could invalidate assumptions | T01 provisioning; T14/T17 real tool tests; report verified incompatibility before changing scope |
| Copier copy is not transactional | Collision or invalid destination can leave partial output | T12 preflight/preview/diff instructions; C03 decline test; no force/rollback promise |
| Existing destination symlinks | Lexically valid path can resolve elsewhere | Explicit preflight of parents/reserved paths; no symlink-security claim or custom installer |
| Consumer changes managed files | Updates may conflict even with a successful exit status | T16 overlap tests; native conflict/rejection inspection and explicit resolution |
| Skip-existing seed semantics | Upstream seed fixes do not overwrite content; deleted seeds can return | T12 documentation and U04 tests; intentionally stable lifecycle |
| Native Markdown config precedence | Consumer overrides influence the selected scope | V08 demonstrates precedence; preserve existing config and document effective behavior |
| Offline links are only local | External rot remains undetected by default | Explicit unchecked status; future opt-in online checks, no misleading green claim |
| Tool bootstrap needs network | A cold run is not air-gapped | Separate provisioning from warmed checks; V05 verifies URL-request boundary |
| CI/tool supply chain changes | Moving dependencies or unavailable binaries can break runs | Exact tool pins, reviewed action SHAs, checksums, no installer fallback; record resolved versions |
| Skill format validator is demonstration-only | Passing format does not guarantee host support or reasoning | Dev-only pin, direct-read baseline, independent semantic walkthroughs |
| Agent citations may be wrong | Reachable links can mask unsupported prose | Claim-level source inspection; irrelevant/conflicting-citation walkthroughs |
| Sibling kit contracts were not supplied | Specific release interoperability is unverified | Generic composition fixture; reference interface; no false named-release compatibility claim |
| Initial test platform is Linux | macOS/Windows execution behavior unknown | Document v0.1 execution support honestly; add platform tests before claiming support |
| Public repository URL/release does not exist yet | Hosted quick-start cannot name a real release | Prove installation from local Git; use actual source/ref supplied by user; no invented URL |

No item requires approval before starting T01. A demonstrated need to change an
accepted boundary, overwrite unrelated data, or publish externally would require
an explicit decision at that time. Routine implementation and verification are
already within the handoff's intended scope.

## Planning verification record

The following checks ran successfully against the completed planning artifacts:

| Check | Observed result |
| --- | --- |
| Planning file inventory | 30 Markdown files; no toolkit implementation files |
| Local Markdown file-link target existence | 95 links checked; zero missing targets |
| Task contract completeness | 27 unique tasks; all eight required fields present; all not started |
| Dependency graph | Acyclic; numeric order valid; no MVP→deferred edges |
| MVP completion closure | T22 transitively depends on all other 21 MVP tasks |
| Specification coverage | 20 unique requirements; each has SHALL behavior, scenario, and review mapping |
| Scenario inventory | 29 unique automated groups and eight semantic groups |
| Whitespace | `git diff --no-index --check` against each planning file passed |

Link checks verified local file targets, not external URLs or a full Markdown
parser/renderer. Task/coverage checks inspected the actual Markdown contracts.
The checks ran as one-off local planning inspection; no custom validator was
added to the proposed toolkit or repository.

No markdownlint-cli2, pre-commit, or Lychee executable is present in the current
environment. No implementation tests or product CLI gates were run, no dependencies
were installed, and no skill runtime packages were created. Those are assigned
to the implementation backlog. Primary-source research establishes the selected
baseline; actual compatibility remains an explicit implementation gate.

Start instructions and the exact initial prompt are in
[IMPLEMENTATION_HANDOFF.md](../IMPLEMENTATION_HANDOFF.md).
