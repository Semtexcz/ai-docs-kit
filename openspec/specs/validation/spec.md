# Validation and quality gates

## Purpose

Specify deterministic checks and acceptance evidence without custom validators,
hidden consumer dependencies, or unsupported claims about AI correctness.

## Requirements

### Requirement: R15 Existing Markdown validator

The MVP SHALL use markdownlint-cli2 in check mode with native configuration,
documented rule choices, and explicit input scope. It SHALL NOT implement custom
Markdown linting, enable implicit auto-fix, or modify shared native config.

#### Scenario: Valid and invalid Markdown

- GIVEN a generated consumer with valid scoped Markdown
- WHEN the standalone checks run
- THEN they SHALL pass without rewriting files
- AND a deliberate meaningful scoped violation SHALL fail until repaired.

### Requirement: R16 Offline local file and fragment checks

Lychee SHALL check relative file/image targets and local fragments in all Markdown
under the two configured roots. Default checks SHALL block remote URL requests
and SHALL disclose that external reachability was not checked.

#### Scenario: Stale incoming fragment

- GIVEN a referring page and an unchanged local link
- WHEN its target heading is removed
- THEN the full-scope default check SHALL fail even if only the target page changed.

#### Scenario: Offline URL handling

- GIVEN provisioned tools and an HTTP URL in scoped documentation
- WHEN default checks run
- THEN no request SHALL be made to that URL and no remote-check success SHALL be claimed.

### Requirement: R17 Composable check entry point

The toolkit SHALL ship standalone pre-commit configuration and use it as the
local/CI check entry point. Installation SHALL NOT activate Git hooks, workflows,
or shared configuration edits. Tool provisioning SHALL be explicit and versioned.

#### Scenario: Existing hook configuration

- GIVEN a repository with its own pre-commit config and Git hook
- WHEN the kit is installed and its standalone checks are invoked
- THEN the original config/hook SHALL remain unchanged
- AND both kit validators SHALL execute over their full configured scope.

### Requirement: R18 Honest failure and automation

Missing tools, malformed config, and required-check failures SHALL prevent a
passing quality gate. CI SHALL use reviewed immutable action refs, read-only
contents permission, and no hosted-model secrets. Optional tools SHALL NOT become
undocumented release gates.

#### Scenario: Missing Lychee

- GIVEN Lychee is absent from the execution environment
- WHEN the required link check runs
- THEN it SHALL fail visibly rather than skip or substitute agent judgment.

### Requirement: R19 Integration and semantic test separation

Automated tests SHALL run real toolchain installation/render/update/validation
behavior in isolated Git fixtures. Skill format validation SHALL reuse an existing
validator. Semantic scenarios SHALL have expected findings and recorded walkthrough
results without asserting deterministic model responses.

#### Scenario: Skill acceptance

- GIVEN a correctly rendered skill and a malformed disposable copy
- WHEN the pinned reference format validator runs
- THEN the valid package SHALL pass and malformed copy SHALL fail
- AND a separate semantic walkthrough SHALL assess evidence reasoning.

### Requirement: R20 End-to-end MVP acceptance

MVP completion SHALL require E01 in the test architecture: install into an existing
repository, preserve foreign files, add evidence-backed docs, detect and repair
broken local links/fragments, update between tagged versions, and pass checks again.

#### Scenario: Release readiness

- GIVEN all implementation tasks claim completion
- WHEN the release checklist is reviewed
- THEN E01, all required automated scenarios, and semantic walkthrough records
  SHALL be present with exact tool versions and honest execution results
- AND optional publication infrastructure SHALL NOT be needed for acceptance.
