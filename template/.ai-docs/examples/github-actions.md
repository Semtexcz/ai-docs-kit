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
full commit SHAs. The Lychee step installs the pinned upstream release archive and
verifies its published SHA-256 checksum before extraction; ai-docs-kit does not
implement a reusable binary downloader.

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
        # The pinned release archive is installed directly because Lychee is not
        # available from a supported tool installer action. The checksum is
        # verified before extraction.
        env:
          LYCHEE_VERSION: "0.24.2"
          LYCHEE_ARCHIVE: lychee-x86_64-unknown-linux-gnu.tar.gz
          LYCHEE_SHA256: "1f4e0ef7f6554a6ed33dd7ac144fb2e1bbed98598e7af973042fc5cd43951c9a"
        run: |
          set -euo pipefail
          curl --proto '=https' --tlsv1.2 --fail --silent --show-error \
            --location --retry 3 --retry-delay 2 \
            --output "$RUNNER_TEMP/$LYCHEE_ARCHIVE" \
            "https://github.com/lycheeverse/lychee/releases/download/lychee-v${LYCHEE_VERSION}/${LYCHEE_ARCHIVE}"
          echo "$LYCHEE_SHA256  $RUNNER_TEMP/$LYCHEE_ARCHIVE" | sha256sum --check --strict
          tar --extract --gzip --file "$RUNNER_TEMP/$LYCHEE_ARCHIVE" --directory "$RUNNER_TEMP"
          install -D -m 0755 \
            "$RUNNER_TEMP/lychee-x86_64-unknown-linux-gnu/lychee" "$RUNNER_TEMP/bin/lychee"
          echo "$RUNNER_TEMP/bin" >> "$GITHUB_PATH"
          "$RUNNER_TEMP/bin/lychee" --version
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
