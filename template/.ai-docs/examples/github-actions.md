# Optional GitHub Actions check example

This example is inert. Rendering the template does not create or modify anything under
`.github/`. To adopt the check, review the workflow below, copy it into
`.github/workflows/` under a name that is unique in your repository, and commit it
yourself. The workflow then belongs to your project and is not updated by Copier.

Why it stays correct for a custom documentation root: the job runs the same standalone
pre-commit configuration that reads the generated `.ai-docs/` files, so no path is
duplicated here.

The workflow uses read-only `contents` permission, no repository secrets, no AI service,
no deployment, and no `pull_request_target`. Third-party actions are pinned to reviewed
full commit SHAs. The Lychee step uses `taiki-e/install-action` with an exact version,
checksum verification enabled, and fallbacks disabled; ai-docs-kit does not implement a
binary downloader.

<!-- ai-docs-kit:workflow-example:start -->
```yaml
name: ai-docs checks

on:
  pull_request:
  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  documentation:
    name: Markdown and local links
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Check out repository
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - name: Set up Python
        uses: actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0 # v7.1.0
        with:
          python-version: "3.12"
      - name: Set up Node.js
        uses: actions/setup-node@949feb2413d6458794dcd2491c4babbbce0c15c1 # v7.1.0
        with:
          node-version: "24"
      - name: Install Lychee
        uses: taiki-e/install-action@ab49d3c64680143e184118bed66a46419fc15519 # v2.90.5
        with:
          tool: lychee@0.24.2
          checksum: true
          fallback: none
      - name: Install pre-commit
        run: python -m pip install pre-commit==4.7.0
      - name: Run ai-docs-kit checks
        run: pre-commit run --config .ai-docs/pre-commit-config.yaml --all-files
```
<!-- ai-docs-kit:workflow-example:end -->

Notes:

- The first run installs pre-commit hook environments (npm for markdownlint-cli2) and
  therefore needs network access. Document checks themselves run offline and do not
  request remote documentation URLs.
- External link checking, scheduled runs, auto-fix pull requests, AI review, and
  deployment are intentionally out of scope for this example.
- If your repository mandates a different action pinning policy, keep the reviewed full
  commit SHA and update it deliberately.
