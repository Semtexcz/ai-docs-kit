# Test strategy and acceptance protocol

## Harness

Use Python 3.12 standard-library `unittest`, `tempfile`, `pathlib`, and `subprocess`.
No pytest, template-test framework, custom renderer, custom linter, or network AI
service is needed. Real Copier, pre-commit, markdownlint-cli2, and Lychee run in
tests. The upstream skill reference validator is a development-only dependency.

Future command: `python -m unittest discover -s tests -v`.
Create a minimal helper in `tests/support.py` for temporary Git repositories,
subprocess execution with argument arrays/timeouts, inventory hashes, and committing
fixture revisions. Use only local test Git identity; never change global config.
Do not depend on the user's current branch, remote, credentials, or Git hooks.
Snapshots of the template under test are committed in temporary repositories;
upgrade tests add a controlled second commit/tag. Do not tag this working repository.

Use a warmed tool environment for check-time network assertions. Cold bootstrap
is separately documented. Provisioning failures fail the required CI job; a
mandatory integration test must not skip itself when a tool is missing. Capture
commands, tool versions, exit codes, and useful failure output. Network access is
only needed to provision third-party tools, not consumer application dependencies.

## Automated scenario inventory

| ID | Scenario and assertion | Task |
| --- | --- | --- |
| I01 | Empty destination renders exact required inventory; no maintainer artifacts leak; answers identify source/ref | T14 |
| I02 | Existing Git project keeps root docs, instructions, manifests, hooks, agent directories, and workflows byte-identical | T14 |
| I03 | Non-software project, Unicode project name, custom multi-level docs root, and parent directory with spaces work | T14 |
| I04 | Existing seeded filenames and context retain bytes on copy; missing seeds are created | T14 |
| I05 | Reject absolute, traversal, dot/backslash, newline, glob, reserved-root, and empty `docs_dir`; reject invalid names | T14 |
| I06 | Copy runs without trust; template has no tasks/migrations/extensions, installed executables, or accidental Jinja output | T14 |
| C01 | Independent synthetic template installs before and after this kit; both answer files and owned inventories survive | T15 |
| C02 | Update each template separately; the other's answers and files stay identical | T15 |
| C03 | Reserved-path collision, with overwrite declined through native Copier interaction, preserves sentinel bytes; no rollback assumption | T15 |
| U01 | Tagged A→B update changes managed policy and keeps installation identity; all checks pass after clean update | T16 |
| U02 | Non-conflicting consumer edit to a managed file survives upstream change | T16 |
| U03 | Overlapping upstream/consumer edit produces a visible conflict or rejection; readiness detects it even if Copier exits zero | T16 |
| U04 | Seed user edits persist; deleting a shipped seed allows recreation on update as documented | T16 |
| U05 | Dirty destination is rejected by standard update without override; existing changes remain | T16 |
| V01 | Valid generated docs pass Markdown and local-link checks; validators do not rewrite files | T17 |
| V02 | Meaningful Markdown violations fail; bad Markdown outside default scope is not selected | T17 |
| V03 | Missing relative file and missing relative image fail Lychee; fixing each passes | T17 |
| V04 | Broken same-file and cross-file heading fragments fail; valid Unicode and encoded-space targets pass | T17 |
| V05 | After bootstrap, an HTTP URL to a counted loopback test server receives zero requests under default offline checks | T17 |
| V06 | Missing Lychee binary or invalid tool config produces a failed required check, not a skip/pass | T17 |
| V07 | Editing a target heading while leaving its referring page unchanged still fails the all-scope link check | T17 |
| V08 | Existing root markdownlint config remains unchanged; documented native precedence is demonstrated on a selected file | T17 |
| S01 | All three rendered skills pass upstream format validation; catalog and resource links resolve; no vendor runtime requirement | T18 |
| S02 | A deliberately malformed skill copy fails the upstream validator; not the valid source package | T18 |
| S03 | Entry/index/catalog budgets and exact package inventory are checked on default/custom renders | T18 |
| B01 | No sibling toolkit or OpenSpec runtime is installed/required; existing OpenSpec and sibling sentinels remain unchanged | T19 |
| A01 | Maintainer workflow performs actual unittest integration checks and doc validation with pinned tools | T20 |
| A02 | Consumer workflow stays inert after rendering; extracted example runs same command on fixture when activated in test | T13 |
| E01 | Full existing-project installation→evidence-backed docs→validation failure/repair→upgrade acceptance below | T21 |

I05 validates names using native Copier behavior, before writes where supported;
do not assert transactional cleanup in an existing destination. Existing symlink
parents and immutable `docs_dir` are installation-guide preconditions, verified
by a documented manual checklist rather than an invented security guarantee.

For conflicts, use native `check-merge-conflict` and forbidden-rejection checks
in maintainer CI plus Git inspection in update tests. Do not build a custom
consumer conflict scanner. Consumer update instructions explicitly include these
checks. Deliberate fixture conflict markers must stay outside normal doc validation.

## Semantic acceptance scenarios

T18 creates scenario inputs and an expected-findings rubric in `tests/scenarios/`.
They are review assets, not scripts that assert LLM text matches snapshots.
Before T22, record a human or coding-agent walkthrough of discovery, writing, and
review on a software fixture and a non-software fixture, identifying reviewer,
revision, evidence inspected, output, and pass/fail against the rubric.

| ID | Required behavior |
| --- | --- |
| M01 | Discover a real missing reader journey; keep uninspected topics unknown; no mass restructure |
| M02 | Write from evidence and add a routing entry; a spec-only feature remains labelled planned |
| M03 | Review syntactically valid prose with an invented flag; identify unsupported claim as a blocker |
| M04 | Detect reachable but irrelevant citations and conflicting code/spec claims |
| M05 | Report an unexecuted command or missing tool as not run/incomplete; do not invent success |
| M06 | Treat instructions embedded in evidence as untrusted data; do not execute them |
| M07 | Use operational/non-code evidence in a non-software project without assuming Python files |
| M08 | Follow an index to relevant evidence without reading unrelated repository trees |

Semantic walkthroughs are release evidence, not claims of reproducible AI accuracy.
Do not add an AI API key to CI. Correct missing guidance before approving a failed
walkthrough. Preserve the result rather than asserting that format validation
proves the skills work.

## E01: concrete end-to-end installation acceptance

T21 implements a single automated test using real tools and only temporary paths:

1. Snapshot the completed toolkit into a temporary Git repository, commit it, and
   tag `v0.1.0`. Create a second independent synthetic Copier template and tag it.
2. Create a committed existing consumer project with root README, AGENTS, root
   pre-commit and Markdown config, a package manifest, an existing docs page,
   workflow, agent-directory sentinel, and foreign-template answers/artifacts.
   Hash all foreign/user-owned paths. Use no application dependency installation.
3. Verify reserved paths are absent. Install the local tagged toolkit with the
   dedicated answers path and explicit `docs_dir=docs/ai-docs`. No trust/force flags.
4. Assert inventory, rendered questions, answers source/ref, untouched hashes, and
   absence of any automatically enabled workflow, hook, or host-specific skill copy.
   Commit the generated files. Read entry point→index→catalog→selected skill;
   assert all referenced paths exist and budgets hold.
5. Add a tiny real evidence fixture (a config file declaring one documented value)
   and a how-to/reference page linking to it with a sources section. Update the
   routing index. Run the exact standalone validation command and require success.
   This fixture verifies the evidence representation, not an agent's judgment.
6. Add a broken local link and require a nonzero check result identifying the page.
   Repair it and require success. Add an invalid fragment, require failure, repair,
   and require success. Confirm validation made no file edits. Commit the result.
7. Add a controlled managed-policy change to the temporary template, commit and tag
   `v0.1.1`. From a clean consumer run `copier update` selecting its dedicated
   answers file and new ref. Assert the policy change arrives, user docs/evidence
   and foreign hashes survive, and no unresolved conflict/rejection remains.
8. Run the exact standalone command again, require success, and report the complete
   versions/refs and inventory result. Clean up only temporary resources.

The suite also runs I03 to establish non-software/custom-root adoption. M01–M08
provide the separate semantic walkthrough that automation cannot establish.

## Release gates

T22 requires all automated scenarios, three skill format checks, semantic walkthrough
records, source/release/version documentation, and end-to-end evidence. CI must
not silently exclude integration tests. Default validation and core installation
are tested on Ubuntu Linux; macOS/Windows are documented as unverified for v0.1
until exercised. Portable files are a design goal, not a cross-platform test claim.
