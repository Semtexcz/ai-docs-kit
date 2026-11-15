# Tool research and selection

Verified against primary sources on **2026-11-15**. Web documentation and source
inspection establish design compatibility; they do not establish that the proposed
combined toolchain has run. T01 records exact executable/commit pins and T14–T21
establish runtime compatibility. No dependencies were installed during planning.

## Findings and decisions

| Tool | Primary-source finding | Project decision |
| --- | --- | --- |
| Diátaxis | Four reader needs distinguish tutorials, how-to, reference, and explanation. [Primer](https://diataxis.fr/start-here/) | Organize by need, create categories only when useful; no runtime dependency |
| Copier | Supports a separate answers path, template subdirectory, and native skip-existing rules. [Template configuration](https://copier.readthedocs.io/en/stable/configuring/) | Use a namespaced state file and dedicated subtree; no tasks/extensions |
| Copier updates | Updates use tracked template history and preserve evolution where merges allow; conflicts need review. [Updating](https://copier.readthedocs.io/en/stable/updating/) | Test real tagged upgrades; require clean consumer state and conflict inspection |
| Agent Skills | A directory with `SKILL.md`, required name/description YAML metadata, and optional resources is the standard. [Specification](https://agentskills.io/specification) | Three MVP skills, three deferred contracts; portable manual discovery |
| Skill discovery | Clients choose discovery locations; metadata-first loading supports progressive disclosure. [Client integration](https://agentskills.io/client-implementation/adding-skills-support) | A short catalog and direct reads; do not promise arbitrary-path automatic host discovery |
| Zensical | A documentation renderer distributed as a Python package. [Getting started](https://zensical.org/docs/get-started/) Its MkDocs compatibility includes supported settings/plugin replacements, with caveats. [Compatibility](https://zensical.org/docs/compatibility/mkdocs/) | Preferred optional renderer evaluation after MVP; no default dependency |
| markdownlint-cli2 | Native external base config and an upstream pre-commit hook are available. [README](https://github.com/DavidAnson/markdownlint-cli2) Version 0.24.1 requires Node >=22. [Tagged metadata](https://github.com/DavidAnson/markdownlint-cli2/blob/v0.24.1/package.json) | Required Markdown gate; Node 24 family; no root consumer Node manifest |
| Vale | Applies configurable prose style rules rather than general correctness. [Introduction](https://docs.vale.sh/) | Optional later profile with an explicit style and locale; not a truth checker |
| Lychee | Provides offline blocking of URL requests and fragment checking. [CLI](https://lychee.cli.rs/guides/cli/) Markdown anchors have renderer-specific limits. [Anchors](https://lychee.cli.rs/recipes/anchors/) | Required local-file/fragment gate; remote links explicitly unchecked by default |
| Lychee hooks | A system-binary hook is available. [Tagged hook manifest](https://github.com/lycheeverse/lychee/blob/lychee-v0.24.2/.pre-commit-hooks.yaml) The auto-install hook bootstraps cargo-binstall from a moving installer URL. [Tagged installer](https://github.com/lycheeverse/lychee/blob/lychee-v0.24.2/scripts/lychee_pre_commit.sh) | Use `lychee-system` with explicit binary provisioning; do not add the auto-installer chain |
| MADR | A lean Markdown structure records significant decisions. [MADR](https://adr.github.io/madr/) | Original MADR-inspired ADR prose and template; no ADR tooling dependency |
| OpenSpec | Current CLI supports spec validation with strict and noninteractive modes, and empty bulk scopes can succeed. [CLI](https://openspec.dev/docs/cli) | Plain compatible requirement/scenario files here; no consumer initialization or required CLI |
| OpenSpec installation | npm installation requires Node >=22.12.0; standalone installation is also documented. [Installation](https://openspec.dev/docs/installation) | Optional developer integration only; never install or initialize as a Copier side effect |
| pre-commit | Manages hooks for multiple tool languages and supports explicit config selection. [Documentation](https://pre-commit.com/) Version 4.7.0 requires Python >=3.11. [Tagged metadata](https://github.com/pre-commit/pre-commit/blob/v4.7.0/setup.cfg) | Reuse as standalone check entry point; Python 3.12 family; hook installation optional |
| GitHub Actions | Recommends least privilege and immutable action pins. [Secure use](https://docs.github.com/en/actions/reference/security/secure-use) | Read-only maintainer CI; inert consumer example; no secrets or deployment |
| install-action | Supports exact tool versions, checksum checking, and disabling fallbacks. [README](https://github.com/taiki-e/install-action) | Reuse for CI Lychee provisioning; full action SHA, checksums enabled, fallback none |
| skills-ref | Official reference validator exists but upstream calls it demonstration-only. [README](https://github.com/agentskills/agentskills/blob/main/skills-ref/README.md) | Pin an inspected commit for maintainer format checks only; no consumer dependency |

## Selected initial baseline

| Component | Observed source / selected version | What still needs execution verification |
| --- | --- | --- |
| Copier | [v9.19.1 release](https://github.com/copier-org/copier/releases/tag/v9.19.1) | Render, skip-existing, multi-template updates/conflicts |
| pre-commit | [v4.7.0 release](https://github.com/pre-commit/pre-commit/releases/tag/v4.7.0) | Standalone config, full-scope hooks, failure behavior |
| markdownlint-cli2 | [v0.24.1 package](https://github.com/DavidAnson/markdownlint-cli2/blob/v0.24.1/package.json) | Node 24 execution, config precedence, rendered skill lint |
| Lychee | [0.24.2 release](https://github.com/lycheeverse/lychee/releases/tag/lychee-v0.24.2) | Offline links/fragments, hidden paths, binary provisioning |
| Node | 24.x selected from supported [release families](https://nodejs.org/en/about/previous-releases) | Record actual patch and check with both validator entry points |
| Python | 3.12.x selected above tools' declared floors | Record actual patch; no consumer source-code dependency |
| skills-ref | Commit pin to resolve in T01, package declares [Python >=3.11](https://github.com/agentskills/agentskills/blob/main/skills-ref/pyproject.toml) | Validate rendered files using its CLI; keep outside consumer dependency graph |

T01 must resolve existing immutable action refs and the skill-validator commit,
record their source/revision, and fail visibly if the chosen version is unavailable.
This is bounded supply-chain pinning, not permission to substitute tools or add
frameworks. No `latest`, moving branch, unreviewed new major, or global installation
is allowed in release instructions or checked-in workflows.

## Reuse assessment

No relevant reusable local CLI was found in the environment's
`/mnt/Data/automation/agent-tools/README.md`; its catalog lists only a private-mail
tool. The catalog was read, and no mailbox data was accessed.

Copier replaces custom installation/upgrades; pre-commit replaces a custom runner;
markdownlint-cli2 and Lychee replace custom deterministic validators; Markdown
indexes replace a discovery database. Original executable code is limited to
integration-test glue. Vale and Zensical justify no MVP dependency because their
optional capabilities do not affect useful Git-native installation.

The named sibling kits were not supplied with repositories or versioned contracts.
Only independent ownership/reference integration is promised; compatibility with
particular upstream releases remains unverified, without blocking this independent MVP.
