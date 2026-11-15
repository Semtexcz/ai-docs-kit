# Install, activate, and update ai-docs-kit

This guide is for a maintainer installing the toolkit into an existing or new Git
repository. It describes what the toolkit owns, how to preview and install it, how to
run the checks, how to activate a skill, and how to update. It does not require
ai-project-planner, ai-devkit, OpenSpec, a hosted AI service, or an application runtime.

Observed on 2026-11-15 with Copier 9.19.1, pre-commit 4.7.0, markdownlint-cli2 0.24.1,
Lychee 0.24.2, Python 3.12.16, and Node 24.22.3 on Ubuntu Linux. Exact tool records are
in [maintainer setup](maintainer-setup.md). macOS and Windows are unverified for v0.1.

## What gets installed

Only `template/` renders. The installation creates:

- `.copier-answers.ai-docs-kit.yml`: installation state. Do not edit or delete it;
  `copier update` reads it.
- `.ai-docs/`: managed entry point, evidence policy, seed-once project context, skill
  catalog, three skills, authoring assets, native validator configuration, and inert
  examples.
- `docs/ai-docs/` (or the `docs_dir` you choose): a seed-once routing index, one how-to,
  and one reference page.

It never edits your root `README.md`, `AGENTS.md`, `CLAUDE.md`, `.pre-commit-config.yaml`,
Markdown or Lychee configuration, `.gitignore`, package manifests, `copier.yml`,
`.github/**`, `.agents/**`, `.claude/**`, or `.codex/**`. It does not install Git hooks
or activate workflows. Examples in `.ai-docs/examples/` are inert text.

## Choose the source and revision

Use a Git revision of this repository. A local clone and a hosted URL are both valid
sources; substitute the source you actually have:

```sh
# Example with a local clone; a hosted URL works the same way.
git clone <this-repository-url> /path/to/ai-docs-kit
git -C /path/to/ai-docs-kit tag --list
```

Set `SOURCE=/path/to/ai-docs-kit` and `REF=<release-tag>` for the commands below. Use a
tag, not a moving branch. v0.1 sets `_min_copier_version: 9.19.1`.

## Preflight

Before rendering, confirm all of the following:

1. `git status` is clean, or your changes are committed or separately preserved.
2. The documentation subtree you plan to use is not reached through a symlink, and its
   parent directories are the ones you expect.
3. `.ai-docs/` and `.copier-answers.ai-docs-kit.yml` are absent. These reserved paths
   must be free for a first installation; ai-docs-kit cannot machine-enforce collision
   safety.
4. The intended `docs_dir` is a subtree you may seed. Slash-separated lowercase segments
   only; no absolute path, dot segments, backslash, whitespace, or glob characters; the
   first segment must not be `openspec`, `template`, `tests`, `node_modules`, `vendor`,
   `build`, `dist`, or `site`. The default is `docs/ai-docs`.
5. You have `git` and Copier 9.19.1 available.

For an existing project, prefer a fresh subtree and index existing documentation by link
instead of moving it. Seeded filenames that already exist are preserved.

## Preview and install

Preview first. `--pretend` prints the planned changes; it is a preview, not a
transaction:

```sh
cd /path/to/consumer
copier copy --pretend --vcs-ref "$REF" --answers-file .copier-answers.ai-docs-kit.yml "$SOURCE" .
```

Then run the same arguments without `--pretend` and answer the two questions:

```sh
copier copy --vcs-ref "$REF" --answers-file .copier-answers.ai-docs-kit.yml "$SOURCE" .
```

- `project_name`: human-readable name; trimmed, 1–100 characters, Unicode letters,
  digits, spaces, `_`, `-`, `.` only, at least one letter or digit.
- `docs_dir`: documentation root as described in the preflight.

Do not add `--force`, `--overwrite`, or `--trust`; the template has no tasks, migrations,
or Jinja extensions that would require trust. If Copier prompts about an existing path
you did not intend to replace, decline it and inspect the diff. Declining preserves the
existing file, but a declined collision can leave a partial result; ai-docs-kit makes no
rollback guarantee.

## Verify the installation

1. Review `git status` and the diff. Only the files listed in
   [the rendered inventory](architecture/installation.md) should appear.
2. Check that any file you had under `docs_dir` still has its original bytes.
3. Read `.ai-docs/README.md`, fill in `.ai-docs/project.md`, and add routes to existing
   documentation in `docs_dir/README.md`.
4. Provision the validation tools, then run the checks:

   ```sh
   pre-commit run --config .ai-docs/pre-commit-config.yaml --all-files
   ```

5. Commit the installation so the first update starts from a clean history.

### Provision the validation tools

ai-docs-kit does not install them and does not add a consumer package manifest.

- `pre-commit` (4.7.0 tested) in a user-level environment.
- Node.js 24 on `PATH` for the markdownlint-cli2 hook (markdownlint-cli2 0.24.1 is
  installed by pre-commit inside its hook environment on first run; that bootstrap needs
  network).
- A Lychee 0.24.2 binary on `PATH`. The `lychee-system` hook uses the system binary and
  fails visibly when it is missing.

See [maintainer setup](maintainer-setup.md) for exact provisioning commands and
checksums. No Git hook is installed; the config is invoked explicitly.

## Activate a skill

The portable baseline is manual and host-neutral:

1. Read `.ai-docs/README.md` (entry point) and `.ai-docs/policy.md`.
2. Read the catalog `.ai-docs/skills/README.md`.
3. Read only the `SKILL.md` whose trigger matches the task, for example
   `.ai-docs/skills/docs-review/SKILL.md`, and perform the scoped request.
4. Read the documentation index at `docs_dir/README.md` and follow the relevant route.

If your agent host supports automatic skill discovery, check its current documentation
and configure the search path for `.ai-docs/skills/` yourself. ai-docs-kit does not
promise host-specific discovery and does not create managed copies or symlinks. To route
an existing instruction file you already own, copy the inert snippet from
`.ai-docs/examples/AGENTS.snippet.md` and keep it under your own review; Copier does not
update it.

## Update

From a clean, committed consumer repository:

```sh
git status                      # must be clean
copier update --vcs-ref "$NEXT_REF" --answers-file .copier-answers.ai-docs-kit.yml
```

Managed files merge; seed-once paths (`.ai-docs/project.md` and everything under
`docs_dir`) are preserved. A missing shipped seed can be recreated by an update, so
deleting a seed file is not durable. `docs_dir` and the answers path must stay unchanged
in v0.1; changing the documentation root requires a new installation. Do not use
`copier recopy` or delete the answers file to upgrade.

After the update, inspect rather than trusting the exit code:

```sh
git status
git diff --check
rg -n '^(<<<<<<<|=======|>>>>>>>)' .ai-docs docs 2>/dev/null
find . -name '*.rej' -not -path './.git/*'
pre-commit run --config .ai-docs/pre-commit-config.yaml --all-files
```

Resolve conflicts and rerun the checks. Copier can exit zero while leaving conflict
markers, so readiness depends on the inspected state. Commit the resolved update.

## Extend the checks to existing documentation

The standalone configuration checks `.ai-docs/**/*.md` and `<docs_dir>/**/*.md`. To
include other documentation trees you own, edit the two hook argument lists in
`.ai-docs/pre-commit-config.yaml` and add the paths, for example:

```yaml
args:
  - --config
  - .ai-docs/markdownlint-cli2.jsonc
  - ".ai-docs/**/*.md"
  - "docs/ai-docs/**/*.md"
  - "docs/legacy/**/*.md"
```

That edit is consumer-owned: Copier may report a conflict on a later update, and you
resolve it. Alternatively, copy the hook entries into your own configuration; the kit
does not modify it. Keep the standalone command working for CI.

`--config` passes a base configuration; it is not an isolation layer. An existing
`.markdownlint-cli2.jsonc` or `.markdownlint.jsonc` referenced by your setup can still
influence selected files. Test your native precedence instead of assuming otherwise.
Remote URLs are not requested by the offline Lychee run; external reachability is
unchecked.

## Coexistence with other Copier templates

Another independently installed template may coexist if its owned paths are disjoint and
it uses its own answers file. Both installation orders are supported. Update each
template with its own answers file. ai-docs-kit does not merge shared files or rewrite
another template's state.

## Optional evidence from other toolkits

Link existing requirements, specifications, plans, or tests as evidence from
`.ai-docs/project.md` and the documentation index. Do not copy their trees, synchronize
their state, or install their CLIs. Missing siblings are a normal installation; the
instructions in this guide never require them.

## Removing the toolkit

ai-docs-kit has no uninstaller. Delete `.ai-docs/` and
`.copier-answers.ai-docs-kit.yml`, and decide separately what to keep under `docs_dir`:
those seed pages are yours and may be useful without the toolkit. Remove any consumer
hook or workflow entries you copied yourself.

## Limits and troubleshooting

- Tested on Ubuntu Linux only; other platforms are unverified for v0.1.
- Cold provisioning needs network access for PyPI, npm, and the Lychee release. Offline
  validation applies after tools exist; do not describe a cold install as air-gapped.
- Installation is not transactional and has no automatic rollback.
- `pre-commit` not found: install it; do not substitute a manual claim that checks ran.
- `lychee` not found: install the pinned binary; the hook failure is a real gate failure.
- markdownlint-cli2 cannot find Node: put Node 24 on `PATH`.
- No files matched: the standalone hooks use explicit globs and `always_run`; a missing
  scope indicates a configuration or path problem, not a pass.
- A broken link appears after editing a heading: the all-scope check catches incoming
  links; fix the referring page or the heading.
