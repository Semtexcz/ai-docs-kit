# Maintainer setup and toolchain record

This page is maintainer-only. It is not rendered into consumer repositories.
It records the exact tool versions, provenance, and provisioning commands used to
develop and test ai-docs-kit. Observed commands and versions below were executed on
2026-11-15 on Ubuntu 26.04 LTS (Linux x86_64).

## Selected versions

| Component | Version | Source of record | Notes |
| --- | --- | --- | --- |
| Python | 3.12.16 | mise python precompiled build | Supported runtime family 3.12; no consumer Python dependency |
| Node.js | 24.22.3 | mise node precompiled build | Required by markdownlint-cli2 0.24.1 (Node >= 22) |
| Copier | 9.19.1 | PyPI package, `requirements-dev.txt` | `_min_copier_version` in `copier.yml` |
| pre-commit | 4.7.0 | PyPI package, `requirements-dev.txt` | Standalone check entry point |
| markdownlint-cli2 | 0.24.1 | npm package (markdownlint 0.42.1) | Hook revision `v0.24.1` |
| Lychee | 0.24.2 | GitHub release `lychee-v0.24.2`, `x86_64-unknown-linux-gnu` | Hook revision `lychee-v0.24.2` |
| skills-ref | 0.1.0 from commit `83021e2be457a9b6679148719c1f6074f0ad975e` | `agentskills/agentskills`, `skills-ref/` subdirectory | Development-only format validator; upstream labels it demonstration-only |

Resolved Python dependencies are captured for review in the session log in
[TASKS.md](../TASKS.md). Directly pinned packages are frozen in
[requirements-dev.txt](../requirements-dev.txt); transitive versions are resolved by
pip at install time and are not locked.

## Provisioning commands

The following commands were used. They install only maintainer tooling; no consumer
package manifest, Node project, or application runtime is created.

```sh
# Python 3.12 and Node 24 (one provisioning path; any existing installer is fine)
mise install python@3.12.16 node@24.22.3

# Isolated maintainer virtual environment with exact Python pins
~/.local/share/mise/installs/python/3.12.16/bin/python3.12 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt

# markdownlint-cli2 in an isolated prefix (no global npm installation)
export PATH="$HOME/.local/share/mise/installs/node/24.22.3/bin:$PATH"
npm install --prefix .tools/npm markdownlint-cli2@0.24.1

# Lychee binary from the pinned release, verified against its published checksum
mkdir -p .tools/bin
curl -sSLo /tmp/lychee.tar.gz \
  https://github.com/lycheeverse/lychee/releases/download/lychee-v0.24.2/lychee-x86_64-unknown-linux-gnu.tar.gz
curl -sSLo /tmp/lychee.sha256 \
  https://github.com/lycheeverse/lychee/releases/download/lychee-v0.24.2/lychee-x86_64-unknown-linux-gnu.tar.gz.sha256
(cd /tmp && sha256sum -c lychee.sha256)
tar xzf /tmp/lychee.tar.gz -C /tmp
install -m 0755 /tmp/lychee-x86_64-unknown-linux-gnu/lychee .tools/bin/lychee
```

Observed checksum for the selected Lychee archive:
`1f4e0ef7f6554a6ed33dd7ac144fb2e1bbed98598e7af973042fc5cd43951c9a`.

## Tool environment for checks

Activate the pinned environment before running tests or hooks:

```sh
export PATH="$PWD/.venv/bin:$PWD/.tools/bin:$PWD/.tools/npm/node_modules/.bin:$PATH"
export PATH="$HOME/.local/share/mise/installs/node/24.22.3/bin:$PATH"

copier --version          # 9.19.1
pre-commit --version      # 4.7.0
node --version            # v24.22.3
markdownlint-cli2 --version
lychee --version          # lychee 0.24.2
skills-ref validate --help
```

Integration tests use tools from `PATH` and fail visibly when one is missing; they
never skip silently. Use `mise exec python@3.12.16 -- ...` variants only if your
shell cannot place these directories on `PATH`.

## Checks

```sh
python -m unittest discover -s tests -v
pre-commit run --all-files
```

The first command renders and checks real temporary consumer repositories. The second
uses the root maintainer configuration and never treats raw Jinja under `template/` or
intentional negative fixtures as ordinary Markdown.

## Provisioned GitHub Actions references

Maintainer CI and the inert consumer example pin full commit SHAs:

| Action | Release tag | Commit SHA |
| --- | --- | --- |
| `actions/checkout` | `v7.0.1` | `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| `actions/setup-python` | `v7.1.0` | `6d4fd22b20465ccc0f7354476588e8df7c9ca0e0` |
| `actions/setup-node` | `v7.1.0` | `949feb2413d6458794dcd2491c4babbbce0c15c1` |
| `taiki-e/install-action` | `v2.90.5` | `ab49d3c64680143e184118bed66a46419fc15519` |

The Lychee step uses `taiki-e/install-action` with `tool: lychee@0.24.2`,
`checksum: true`, and `fallback: none`. The action inputs were inspected in its
`action.yml` at that commit.

## Limitations

- Only Ubuntu Linux is exercised. macOS and Windows are unverified for v0.1.
- Cold provisioning needs network access (PyPI, npm, GitHub releases). Offline
  validation applies to document checking after tools exist, not to bootstrap.
- The skills-ref validator is a demonstration tool kept outside the consumer
  dependency graph.
