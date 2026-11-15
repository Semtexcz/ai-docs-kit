# Documentation

## Purpose

Specify useful, discoverable, evidence-based Markdown for both software and
non-software projects without a mandatory publication stack.

## Requirements

### Requirement: R06 Minimal reader-oriented structure

The toolkit SHALL seed a routing index, a useful documentation-update how-to, and
a policy reference. Diátaxis SHALL guide reader roles where appropriate without
mandatory empty categories or automatic moves of existing documents.

#### Scenario: Small initial project

- GIVEN a project with no existing documentation
- WHEN the template is rendered
- THEN the seed pages SHALL form a usable linked path
- AND unnecessary empty quadrant directories SHALL NOT be required.

### Requirement: R07 Selective discovery

The entry point SHALL link policy, context, documentation home, and a skill catalog.
The documentation index SHALL route by topic, reader need/type, audience, path, and
evidence entry point. Agents SHALL read relevant routes and evidence progressively.

#### Scenario: Relevant page lookup

- GIVEN indexed relevant and unrelated documentation trees
- WHEN an agent investigates a bounded topic
- THEN it SHALL follow the relevant index and source route
- AND report inspected scope without requiring the entire repository in context.

### Requirement: R08 Evidence for material claims

New or materially changed behavioral claims SHALL be supported by inspected
evidence. Plans and inferences SHALL be labelled. Missing or conflicting support
SHALL be disclosed; source reachability alone SHALL NOT establish support.

#### Scenario: Specification without implementation

- GIVEN an approved specification but no implementation evidence
- WHEN an agent documents that capability
- THEN it SHALL label the capability as planned rather than delivered.

#### Scenario: Unsupported claim

- GIVEN prose asserting a flag not found in inspected sources
- WHEN an agent writes or reviews the prose
- THEN it SHALL omit, qualify, or flag the claim and SHALL NOT invent evidence.

### Requirement: R09 Review results and uncertainty

Reviews SHALL identify scope/revision, inspected evidence, claim-level status,
deterministic commands/results, semantic findings, unknowns, and disposition.
Missing checks SHALL be reported as not run, never as passed.

#### Scenario: Green lint with false prose

- GIVEN valid Markdown whose material claim lacks support
- WHEN deterministic checks pass and semantic review runs
- THEN the review SHALL separately report passing checks and required changes.

### Requirement: R10 Consumer context and canonical content

Markdown SHALL remain canonical. Managed policy SHALL be distinct from seeded
consumer context. Existing canonical sources SHALL be linked instead of copied
into competing truth sources. Non-software evidence SHALL be valid input.

#### Scenario: Independent operational project

- GIVEN no source-code files and an approved operational record
- WHEN docs are written from that record
- THEN the agent SHALL trace claims to it without requiring a Python project,
  sibling toolkit, renderer, or duplicated requirements store.
