# Deterministic validation contract

## Toolchain boundary

Installation needs Git and Copier. Validation additionally needs pre-commit,
Node.js for markdownlint-cli2, and an explicit Lychee binary. No consumer
`package.json`, `pyproject.toml`, Python application, Rust toolchain, Docker,
AI API, or global Git-hook installation is required.

The tested versions are Copier 9.19.1, pre-commit 4.7.0, markdownlint-cli2 0.24.1,
and Lychee 0.24.2. Python 3.12 and Node.js 24 are the supported runtime families; the
exact patch versions and immutable references are recorded in
[maintainer setup](../maintainer-setup.md). They were exercised together on Ubuntu Linux
locally on 2026-11-15 and in hosted CI on 2026-11-19 (run `44503559840`, revision
`f5c90492aa22592d430c4960a8e42b7fee44cf22`); other platforms remain unverified. See
[research](../research/tooling.md) and the [release checklist](../release-checklist.md).

## Default scope and command

From the consumer root:

```sh
pre-commit run --config .ai-docs/pre-commit-config.yaml --all-files
```

Both configured checks always run over all `*.md` files recursively in `.ai-docs/`
and `docs_dir`, including new files and link targets affected by other changes.
They do not select unrelated Markdown elsewhere. Use `pass_filenames: false` and
`always_run: true`; configure the two explicit glob arguments in each hook.
Do not rely on staged-file selection or silently pass because no files matched.
The standalone config assumes Git even though direct individual CLIs can be run
without Git. The initial render must include known files in both roots.

Examples and maintainer tests may contain intentionally invalid snippets inside
fences. Negative fixture files live outside the rendered tree and are only
introduced into disposable consumers by tests. Examples of future paths use code
spans, not links to missing output.

## Markdown

Use the upstream `markdownlint-cli2` pre-commit hook at `v0.24.1`, its Node
environment with `language_version: system`, and an explicit `--config
.ai-docs/markdownlint-cli2.jsonc`. Provision Node 24 first. Check mode only:
no `--fix`, generated rewrites, custom rules, formatter, or Markdown parser.

Native rule defaults apply except `MD013` (line length) is disabled to avoid
wrapping URLs, tables, and evidence rows. Keep `MD033` enabled; use ordinary
Markdown for the MVP. The selected rule config and effective root/subdirectory
overrides must be documented. markdownlint-cli2's `--config` is a base config,
not an isolation guarantee: existing native configs can influence selected files.
Respect deliberate consumer overrides; test and document their precedence instead
of rewriting shared files or promising stronger isolation than the tool provides.

## Links

Use the upstream Lychee `lychee-system` hook at `lychee-v0.24.2`; provision
Lychee 0.24.2 explicitly. Configure arguments for `.ai-docs/lychee.toml`, `--offline`,
`--include-fragments`, `--no-progress`, `--hidden`, and the same two scope globs.
Local file paths and fragment anchors must fail when broken. Do not use
`--skip-missing`, broad path exclusions, or blanket success statuses.

Remote HTTP(S) links are not requested by the default offline run; report them as
unchecked externally. Do not claim remote validation. No link preprocessing,
email validation, executable snippets, or remote-auth credentials are enabled.
Relative links resolve from their source file; use file links rather than
renderer-dependent extensionless routes. Test same-file anchors, cross-file
anchors, Unicode headings, spaces/percent-encoded file paths, and images against
the selected Lychee version. Renderer-specific fragment semantics remain a future
publication-profile concern.

Offline describes document checking after tools are provisioned. pip, pre-commit's
hook bootstrap, and npm may require network on first use. Do not describe a cold
installation as air-gapped. Tests must distinguish bootstrap from check-time
traffic and fail if a remote documentation URL is contacted during offline checks.

## Optional automation

The standalone config can be run manually without changing any Git hook. Do not
automatically call `pre-commit install`. A maintainer can explicitly copy hook
entries into existing configuration or add an isolated CI job after reviewing
scope. Such edits are consumer-owned and not updated by Copier.

An inert fenced GitHub Actions example lives under `.ai-docs/examples/`. It uses
read-only contents permission, pull requests and pushes, no AI secrets, and the
same standalone command. It never uses `pull_request_target`. Third-party actions
are pinned to reviewed full commit SHAs. Provision the Lychee binary from the
pinned upstream release archive (`lychee-x86_64-unknown-linux-gnu.tar.gz` for
0.24.2), verify its published SHA-256 before extraction, and install only the
binary. Lychee is not available from the generic tool-installer action used for
other tools, so each workflow contains one short explicit step for this archive.
Do not implement a reusable downloader, a package manager, an unchecked fallback,
or a pipe-to-shell install. CI also provisions Python and Node.

Tests parse both workflow files and execute the install step text against the real
release asset, including a tampered-checksum rejection (A03). A hosted workflow is
still only proven by a hosted run; YAML parsing and local step execution must not
be reported as a green GitHub Actions result.

Maintainer CI runs unittest integration tests and checks ordinary maintainer docs.
Raw Jinja source must not be treated as rendered Markdown: test rendered outputs;
scope maintainer lint away from `template/` and intentionally bad fixtures.

## Guarantees and gaps

Syntax and reachability are deterministic checks. Diátaxis fit, evidence support,
clarity, accuracy, security implications, and completeness require review.
Missing binaries, invalid config, validator failures, and unresolved update
conflicts prevent completion. Do not replace a failed tool with an agent's opinion.
External-link checks and Vale are opt-in later; they cannot silently become MVP gates.
