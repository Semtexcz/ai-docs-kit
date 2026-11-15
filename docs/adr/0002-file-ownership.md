# Namespaced ownership and seed-once content

- Status: accepted
- Date: 2026-11-15

## Context and drivers

Independent Copier templates cannot safely claim the same root files. Existing
projects already have docs, instructions, workflow, hook, and package configuration.

## Options

Automatically patch shared files; skip arbitrary collisions; reserve a dedicated
toolkit namespace and let consumers opt into shared integration.

## Decision

Manage `.ai-docs/` and `.copier-answers.ai-docs-kit.yml`; seed a configurable docs
subtree, default `docs/ai-docs/`. Preserve present consumer content and project
context using native skip-existing patterns. Root instructions, manifests, workflows,
and host skill directories are never automatically changed. The
[Copier configuration reference](https://copier.readthedocs.io/en/stable/configuring/)
supports separate answers files for independent templates.

## Consequences

Consumers explicitly activate routing/hooks/CI. Manual skill loading works without
shared-file edits. Seed improvements do not automatically overwrite user pages,
and missing shipped seeds can return on updates. One installation and stable
`docs_dir` are supported. Reserved path/symlink checks are documented preconditions;
the template does not promise transactional collision handling.

## Confirmation

T14–T16 cover preservation, both template orders, independent updates, and visible
conflicts. The exact inventory is in [installation](../architecture/installation.md).
