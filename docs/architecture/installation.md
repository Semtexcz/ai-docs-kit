# Installation, ownership, and upgrades

## Supported lifecycle

One ai-docs-kit installation per consumer Git repository. Other Copier templates
may be installed independently. Multiple ai-docs-kit instances and changing the
documentation root during an upgrade are outside v0.1 support.

Installation must work in an empty directory and in an existing Git project.
Updates require a clean committed consumer repository and an available original
template Git revision. Local tests use disposable template repositories with tags;
users select an actual release ref, never a moving branch by default.

## Copier contract

| Setting | Required decision |
| --- | --- |
| `_subdirectory` | `template` |
| `_answers_file` | `.copier-answers.ai-docs-kit.yml` |
| `_min_copier_version` | `9.19.1`; v0.1 tested with exactly 9.19.1 |
| Templates suffix | `.jinja` |
| Executable extensions/tasks/migrations | None; no `--trust` requirement |
| Skip existing content | `.ai-docs/project.md` and all paths under the chosen `docs_dir` |
| Answers template filename | `{{ _copier_conf.answers_file }}.jinja` |
| Answers contents | Copier's `_copier_answers` serialized using its documented YAML filter |

Do not synthesize `_commit` or `_src_path`; let Copier record them. Do not edit the
answers file manually. No generic `.copier-answers.yml` is generated.

## Public questions

| Question | Type/default | Validation and use |
| --- | --- | --- |
| `project_name` | string, `My project` | Trimmed, 1–100 characters; Unicode letters/numbers, spaces, `_`, `-`, `.` only; at least one letter/number; rendered as text and YAML-escaped where necessary |
| `docs_dir` | string, `docs/ai-docs` | Slash-separated lowercase segments matching `[a-z0-9][a-z0-9_-]*`; no absolute path, dot segments, backslash, whitespace, glob or newline; forbidden first segments `openspec`, `template`, `tests`, `node_modules`, `vendor`, `build`, `dist`, `site`; unchanged during update |

Use Copier question validators and Jinja's available documented filters; no custom
extension or Python validation hook. No other MVP questions. Descriptions, audience,
language, evidence roots, existing-doc entry points, and terminology are editable
Markdown in `project.md`, with explicit unknowns instead of inferred commitments.
Non-English content is allowed; no English prose linter is enabled by default.

`docs_dir` names a subtree, not a request to restructure existing documents. Users
may choose an existing docs home, but seeded filenames are preserved when present.
For existing projects, prefer a fresh subtree and index the existing docs by link.
Lexical validation does not secure an existing symlink: the installation procedure
requires inspecting destination parents and reserved paths first.

## Rendered file inventory

`D` below means the chosen `docs_dir`. These are rendered output paths; they are created
in a consumer repository, not at this maintainer repository root.

| Consumer path | Ownership / lifecycle |
| --- | --- |
| `.copier-answers.ai-docs-kit.yml` | Copier installation state; managed |
| `.ai-docs/README.md` | Managed entry point: policy, docs home, skill catalog, commands |
| `.ai-docs/policy.md` | Managed base policy; local edits merge through Copier |
| `.ai-docs/project.md` | Seed once; consumer context and scoped policy additions |
| `.ai-docs/skills/README.md` | Managed catalog: name, trigger, path; only MVP skills |
| `.ai-docs/skills/docs-discover/SKILL.md` | Managed skill |
| `.ai-docs/skills/docs-write/SKILL.md` | Managed skill |
| `.ai-docs/skills/docs-review/SKILL.md` | Managed skill |
| `.ai-docs/assets/document.md` | Managed page-writing starting point |
| `.ai-docs/assets/review.md` | Managed structured review starting point |
| `.ai-docs/assets/adr.md` | Managed MADR-inspired decision starting point with attribution |
| `.ai-docs/markdownlint-cli2.jsonc` | Managed native Markdown configuration |
| `.ai-docs/lychee.toml` | Managed native local-link configuration |
| `.ai-docs/pre-commit-config.yaml` | Managed standalone check configuration |
| `.ai-docs/examples/AGENTS.snippet.md` | Managed optional routing text; never applied automatically |
| `.ai-docs/examples/github-actions.md` | Managed fenced workflow example; never activated automatically |
| `D/README.md` | Seed once; documentation routing index |
| `D/how-to/update-documentation.md` | Seed once; usable first workflow |
| `D/reference/documentation-policy.md` | Seed once; links to canonical policy, no duplicate rulebook |

No empty tutorial/explanation trees, `.gitkeep` files, automatic reports, or
unimplemented skills are rendered. Toolkit policy is canonical in `.ai-docs/`;
consumer prose is canonical in `D` or in existing docs linked from its index.

## Preserved shared surface

Never generate or patch consumer `README.md`, `AGENTS.md`, `CLAUDE.md`,
`.pre-commit-config.yaml`, `.markdownlint*`, `.vale.ini`, `lychee.toml`,
`.gitignore`, `package.json`, `pyproject.toml`, `copier.yml`, `openspec/**`,
other templates' answers files, `.agents/**`, `.claude/**`, `.codex/**`, or
`.github/**`. Examples are inert files inside `.ai-docs/examples/`.

The maintainer repository may own its own root files; this rule concerns consumers.
Do not generate `.ai-docs/AGENTS.md`: its scope would not govern consumer docs.
Native agent discovery is host-specific, so the portable baseline is direct
reading of the skill catalog and selected `SKILL.md`. A user may add the provided
snippet to existing instructions, or configure a host's skill search path after
checking its current documentation. No managed copies or symlinks are installed.

## Installation procedure to document and test

1. Inspect Git status, destination parents, `.ai-docs/`, the dedicated answers
   path, and `docs_dir`. Reserved toolkit paths must be absent for a first install.
   Never render through a symlink or into an unrelated `.ai-docs/` directory.
2. Commit or separately preserve existing changes. Review a `copier copy --pretend`
   with an explicit source/ref and answers path. This is a preview, not a transaction.
3. Run `copier copy --vcs-ref <release-ref> --answers-file
   .copier-answers.ai-docs-kit.yml <template-source> .`, answering the two questions.
   Use the same arguments for preview and execution. Do not use `--force`,
   `--overwrite`, or `--trust` in the standard installation instructions.
4. Review the Git diff and inventory; existing seeded files must retain their
   bytes. Set project context and add existing-doc routes. Commit the installation.
5. Provision validation tools and run the standalone command. Agent usage can start
   by explicitly reading `.ai-docs/README.md`; editing shared instructions is optional.

Absent reserved paths are a documented precondition, not a promise of atomic
machine-enforced collision refusal. Copier may prompt or leave a partial result
on an existing-path collision. Decline overwrites, inspect the diff, and revert
only files from that attempt. Automated fresh fixtures may use `--defaults` only
after asserting the destination inventory. Collision tests must verify preservation
when overwrites are declined; they must not claim rollback guarantees.

## Update procedure and content ownership

From a clean committed consumer root, use `copier update --answers-file
.copier-answers.ai-docs-kit.yml --vcs-ref <next-release-ref>`.
Managed files receive Copier's normal merge behavior, including conflicts.
Review changed configuration, resolve conflicts, rerun checks, and commit.
Use `update`, not `recopy`, for evolution; never delete installation state to upgrade.

Seed-once paths use `_skip_if_exists`; present content is not updated. A missing
seed can be recreated by an update, so deletion of a shipped seed is not durable.
Document this explicitly. New seed filenames can appear in future releases;
existing user filenames still win. No automatic rename or migration is attempted.
Managed policy/skill conflicts must remain visible; a zero exit code alone is
insufficient proof of a clean update. Inspect Git conflict state, marker lines,
and `.rej` files with standard Git/pre-commit tools before declaring success.

Installation identity (`docs_dir`, answers path, source identity) stays stable in
v0.1. Project context changes go in `project.md`; name changes may be passed to
Copier update normally. A future relocation feature requires a separate ADR.

## Composition guarantee

Disjoint paths and separate answers files make independent templates composable;
this is not a shared-file merge guarantee. Test a representative independent
template in both installation orders and update each separately. Preserve all
foreign answers, shared root files, agent directories, and workflow bytes.
Without inspected upstream fixtures, do not advertise tested compatibility with
specific releases of ai-project-planner or ai-devkit.
