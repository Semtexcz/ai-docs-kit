# Installation

## Purpose

Specify independent, incrementally adoptable Copier installation and upgrades for
new and existing Git projects without shared-file ownership conflicts.

## Requirements

### Requirement: R01 Independent installation

The toolkit SHALL install using Copier without executable template tasks,
migrations, extensions, consumer application packages, or AI service credentials.
Only `template/` SHALL render. Its dedicated answers filename SHALL be
`.copier-answers.ai-docs-kit.yml` by default.

#### Scenario: Clean installation

- GIVEN a tagged toolkit source and an empty destination
- WHEN the user runs Copier copy with valid answers and no trust flag
- THEN the required consumer inventory SHALL render and record source/ref
- AND maintainer plans, tests, development files, and OpenSpec tree SHALL NOT render.

### Requirement: R02 Preservation and ownership

The toolkit SHALL preserve user-owned shared root files and existing seeded
documentation. Reserved toolkit paths SHALL be checked by the documented
installation preflight. The toolkit SHALL NOT claim transactional collision handling.

#### Scenario: Existing repository

- GIVEN a repository with docs, instructions, manifests, hooks, and workflows
- WHEN installation uses absent reserved paths and a valid documentation subtree
- THEN existing shared files SHALL remain byte-identical
- AND missing seeded pages SHALL be created without replacing present seed files.

#### Scenario: Reserved path collision

- GIVEN an unrelated file at a reserved managed path
- WHEN a user attempts copy and declines native Copier overwrite prompts
- THEN that file's contents SHALL remain intact
- AND the instructions SHALL require diff inspection for a possible partial result.

### Requirement: R03 Valid configurable documentation root

The template SHALL expose only `project_name` and `docs_dir` as MVP questions,
using the exact validations in the installation architecture. The default root
SHALL be `docs/ai-docs`. Non-software projects SHALL be supported.

#### Scenario: Custom root and non-software content

- GIVEN a non-software repository and valid Unicode project name
- WHEN installation selects a valid nested documentation root
- THEN links/configuration SHALL resolve to that root without requiring source code.

#### Scenario: Invalid destination answer

- GIVEN an absolute, traversal, newline, glob, empty, or reserved-root `docs_dir`
- WHEN Copier validates the question
- THEN it SHALL reject the answer rather than accepting that path.

### Requirement: R04 Independent template composition

The toolkit SHALL use disjoint managed paths and dedicated state so another
independent Copier template can be installed and updated in the same repository.
It SHALL NOT rewrite another template's state or shared integration files.

#### Scenario: Both orders and independent upgrades

- GIVEN representative independent templates with separate answers files
- WHEN installed in either order and each is later updated individually
- THEN both installations SHALL retain their answers and owned artifacts
- AND updates SHALL NOT alter the other template's files.

### Requirement: R05 Versioned upgrades and visible conflicts

Updates SHALL use Copier's history-aware update with the dedicated answers file.
Managed files SHALL participate in merges. Existing seed-once content SHALL be
preserved; missing shipped seeds MAY be recreated as documented. Installation
identity and documentation root SHALL remain stable within the supported v0.1 lifecycle.

#### Scenario: Clean and non-conflicting upgrade

- GIVEN a clean committed consumer based on tagged template A
- WHEN updating to tagged B with a managed-file improvement
- THEN the improvement SHALL arrive and non-conflicting user edits SHALL survive.

#### Scenario: Conflicting upgrade

- GIVEN overlapping consumer/template edits
- WHEN updating
- THEN unresolved conflicts or rejections SHALL remain visible
- AND the update SHALL NOT be declared complete until resolved and checked.

#### Scenario: Dirty consumer

- GIVEN uncommitted consumer changes
- WHEN standard Copier update is attempted without dirty-state overrides
- THEN the update SHALL be rejected without discarding those changes.
