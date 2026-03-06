# Supply Chain Security & SCA (Software Composition Analysis)

Purpose: Use this reference when scanning dependencies, lockfiles, SBOMs, CI/CD pipelines, or AI-recommended packages.

## Contents

- threat landscape
- attack vectors
- SCA tooling
- SBOM requirements
- CI/CD hardening
- dependency workflows
- scan commands

## Threat Landscape

- `70-90%` of modern applications are composed of OSS components.
- OWASP Top 10 (2025) elevates supply-chain risk to `A03`.
- AI-recommended dependencies are a major risk source.

### Attack Vectors

| Vector | Method | Example |
|--------|--------|---------|
| `Typosquatting` | Publish a similar package name | `lodash` -> `lodahs` |
| `Dependency Confusion` | Publish an internal package name publicly | 2021 Alex Birsan |
| `Slopsquatting` | Register a non-existent package suggested by AI | `5-21%` of AI-suggested packages may not exist |
| `Compromised Maintainer` | Take over a maintainer account | `event-stream` |
| `Build System Attack` | Inject into CI/CD | `SolarWinds` |
| `Malicious Update` | Ship a hostile update from a legitimate package | `ua-parser-js` |

### AI Dependency Risk

- `44-49%` of AI-suggested dependencies may already have known CVEs
- only about `20%` of AI-suggested packages are considered safe by default
- security-tool-assisted AI improves safe-package selection to about `57%`
- treat AI-generated code and AI-suggested packages as untrusted third-party input

## SCA And Reachability

SCA manages third-party component risk. Use it alongside SAST, not instead of SAST.

| Tool | Strength |
|------|----------|
| `Snyk` | Developer-friendly, auto-fix PRs |
| `Dependabot` | GitHub-native, low setup |
| `Socket` | Supply-chain attack detection |
| `Mend (WhiteSource)` | Enterprise license and policy control |
| `Endor Labs` | Reachability and noise reduction |
| `OWASP Dependency-Check` | Language-agnostic NVD matching |
| `Trivy` | Filesystem, container, and IaC scanning |

Reachability factors:

1. `CVSS` and `EPSS`
2. runtime reachability
3. exploit maturity
4. network exposure and privilege context

## SBOM

An SBOM is required when provenance, regulated delivery, or broad dependency traceability matters.

### Accepted Formats

- `SPDX`
- `CycloneDX`
- `SWID`

### CISA 2025 Minimum Elements

- `Supplier Name`
- `Component Name`
- `Version`
- `Unique Identifiers` such as `CPE`, `PURL`, `SWID`
- `Dependency Relationship`
- `Author`
- `Timestamp`

Sentinel checks:

- all required fields present
- transitive dependencies included
- AI-related components identified where relevant

### Generation Commands

```bash
# CycloneDX (npm)
npx @cyclonedx/cyclonedx-npm --output-format json > sbom.json

# Syft
syft dir:. -o cyclonedx-json > sbom.json

# Trivy
trivy fs . --format cyclonedx --output sbom.json
```

## CI/CD Hardening

Pipeline principles:

1. least privilege
2. isolation
3. immutable signed artifacts
4. hash pinning for third-party actions
5. audit logging

```yaml
name: Supply Chain Security
on: [push, pull_request]

jobs:
  sca-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
      - name: Run npm audit
        run: npm audit --audit-level=high
      - name: Generate SBOM
        run: npx @cyclonedx/cyclonedx-npm --output-format json > sbom.json
      - name: Verify lockfile integrity
        run: npm ci --ignore-scripts
      - name: License check
        run: npx license-checker --failOn "GPL-3.0;AGPL-3.0"
```

## Dependency Workflow

Required:

- commit the lockfile (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`)
- use deterministic install commands such as `npm ci` in CI
- review lockfile diffs

Forbidden:

- ignoring lockfiles in git
- using non-deterministic dependency installs in CI

Recommended flow:

1. run daily CVE scans
2. prioritize by `CVSS + EPSS + reachability`
3. fix with controlled PRs
4. verify with tests
5. track unresolved risk explicitly

## Sentinel Checklist And Commands

Checklist:

- run `npm audit` / `yarn audit`
- detect known CVEs
- flag unused packages
- check lockfile existence and integrity
- check private package names against public registries
- inspect `postinstall` scripts
- review license compatibility

Commands:

```bash
npm audit --json > audit-report.json
yarn audit --json > audit-report.json
npx snyk test --json > snyk-report.json
trivy fs . --severity HIGH,CRITICAL --format json > trivy-report.json

npm update package-name
npm audit fix
npm audit fix --force
```
