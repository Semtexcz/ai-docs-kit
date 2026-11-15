# Reader needs and progressive documentation discovery

- Status: accepted
- Date: 2026-11-15

## Context and drivers

Agents need relevant evidence without full-repository loading. Small projects
should not inherit a large empty documentation hierarchy.

## Options

Mandatory four-quadrant trees; a generated metadata/search database; small linked
Markdown indexes organized by actual reader needs.

## Decision

Use [Diátaxis](https://diataxis.fr/start-here/) where applicable and ordinary Markdown
indexes with audience, purpose, path, and evidence routes. Seed useful how-to and
reference pages only. Governance and project planning retain their own roles.
Load entry point→policy/context→index→one skill→selected evidence.

## Consequences

No embeddings, index generator, schema parser, or frontmatter requirement is needed.
Humans/agents maintain routes with content changes. Budgets keep entry points
small, and linked topic indexes accommodate growth. Retrieval completeness still
depends on honest scope reporting.

## Confirmation

T04/T18 check the rendered routes and size budgets; semantic walkthrough M08 checks
bounded retrieval. See [documentation](../architecture/documentation.md).
