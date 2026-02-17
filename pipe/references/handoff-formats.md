# Handoff Formats

Agent-to-agent handoff templates for Pipe collaboration patterns.

---

## Pattern A: Infra-to-Pipeline (Scaffold → Pipe → Gear)

### Receiving from Scaffold

```yaml
## NEXUS_HANDOFF
step: infrastructure_provisioned
from_agent: Scaffold
summary: "Infrastructure provisioned, CI/CD pipeline needed"
artifacts:
  - type: infrastructure
    details:
      cloud_provider: AWS|GCP|Azure
      deployment_target: ECS|Cloud Run|App Service|Kubernetes
      environments: [staging, production]
      iac_tool: Terraform|Pulumi|CloudFormation
      registry: ECR|GCR|ACR|GHCR
context:
  repository: owner/repo
  branch_strategy: trunk-based|gitflow|github-flow
  existing_workflows: []
request: "Design CI/CD pipeline for provisioned infrastructure"
```

### Sending to Gear

```yaml
## NEXUS_HANDOFF
step: pipeline_designed
from_agent: Pipe
summary: "Workflow designed, ongoing maintenance needed"
artifacts:
  - type: workflow_files
    paths:
      - .github/workflows/ci.yml
      - .github/workflows/deploy.yml
      - .github/actions/setup/action.yml
  - type: configuration
    details:
      triggers: [push, pull_request, workflow_dispatch]
      environments: [staging, production]
      caching: pnpm + Docker layer
      security: permissions minimized, SHA-pinned
risks:
  - "Cache invalidation may need tuning after first runs"
next_agent: Gear
next_action: "Monitor and maintain CI/CD pipeline"
```

---

## Pattern B: Release Workflow (Pipe ↔ Launch)

### Receiving from Launch

```yaml
## NEXUS_HANDOFF
step: release_strategy_defined
from_agent: Launch
summary: "Release strategy defined, workflow implementation needed"
artifacts:
  - type: release_strategy
    details:
      versioning: semver|calver
      changelog: keep-a-changelog|conventional-changelog
      release_tool: semantic-release|changesets|manual
      environments: [staging, production]
      approval_required: true|false
      rollback_strategy: feature-flag|container|full-deploy
context:
  current_workflows: []
  branch_strategy: trunk-based|gitflow
request: "Implement release workflow based on strategy"
```

### Sending to Launch

```yaml
## NEXUS_HANDOFF
step: release_workflow_implemented
from_agent: Pipe
summary: "Release workflow implemented and validated"
artifacts:
  - type: workflow_files
    paths:
      - .github/workflows/release.yml
      - .github/workflows/deploy-staging.yml
      - .github/workflows/deploy-production.yml
  - type: configuration
    details:
      trigger: tag-push|workflow_dispatch|merge-to-main
      environments: [staging, production]
      approval_gates: [production]
      rollback_workflow: .github/workflows/rollback.yml
verification:
  - "Workflow syntax validated with actionlint"
  - "Local test passed with act"
next_agent: Launch
next_action: "Configure release schedule and versioning"
```

---

## Pattern C: Security Pipeline (Pipe → Sentinel → Pipe)

### Sending to Sentinel

```yaml
## NEXUS_HANDOFF
step: security_audit_requested
from_agent: Pipe
summary: "Workflow security audit needed"
artifacts:
  - type: workflow_files
    paths: [".github/workflows/*.yml"]
  - type: security_assessment
    details:
      permissions_model: job-level-minimal
      third_party_actions:
        - name: actions/checkout
          pinned: sha
        - name: docker/build-push-action
          pinned: sha
      oidc_configured: true|false
      secrets_usage: [GITHUB_TOKEN, NPM_TOKEN]
concerns:
  - "pull_request_target usage needs review"
  - "New third-party action introduced"
request: "Review workflow security posture"
```

### Receiving from Sentinel

```yaml
## NEXUS_HANDOFF
step: security_audit_completed
from_agent: Sentinel
summary: "Security audit complete, remediation needed"
findings:
  - severity: HIGH
    issue: "Action pinned by tag, not SHA"
    location: .github/workflows/ci.yml:15
    recommendation: "Pin to SHA: abc123..."
  - severity: MEDIUM
    issue: "Permissions broader than necessary"
    location: .github/workflows/deploy.yml:5
    recommendation: "Remove contents: write, add only needed"
next_agent: Pipe
next_action: "Apply security remediations"
```

---

## Pattern D: Workflow Visualization (Pipe → Canvas)

```yaml
## NEXUS_HANDOFF
step: visualization_requested
from_agent: Pipe
summary: "Complex workflow chain needs visualization"
artifacts:
  - type: workflow_graph
    details:
      workflows:
        - name: CI
          triggers: [push, pull_request]
          jobs: [lint, test, build]
          dependencies: {build: [lint, test]}
        - name: Deploy
          triggers: [workflow_run(CI)]
          jobs: [deploy-staging, deploy-production]
          dependencies: {deploy-production: [deploy-staging]}
      chain_type: workflow_run
      environments: [staging, production]
request: "Generate Mermaid diagram of workflow chain"
format: mermaid
```

---

## Pattern E: PR Strategy (Pipe → Guardian)

```yaml
## NEXUS_HANDOFF
step: branch_protection_designed
from_agent: Pipe
summary: "Branch protection and PR automation configured"
artifacts:
  - type: protection_config
    details:
      required_checks: [ci, lint, test]
      required_reviewers: 2
      merge_queue: enabled
      auto_merge: dependabot-only
      codeowners: configured
  - type: workflow_files
    paths:
      - .github/workflows/labeler.yml
      - .github/labeler.yml
      - .github/CODEOWNERS
next_agent: Guardian
next_action: "Integrate with PR commit strategy"
```

---

## Pattern F: Performance Pipeline (Pipe ↔ Bolt)

```yaml
## NEXUS_HANDOFF
step: benchmark_pipeline_designed
from_agent: Pipe
summary: "Benchmark CI workflow created"
artifacts:
  - type: workflow_files
    paths:
      - .github/workflows/benchmark.yml
  - type: configuration
    details:
      trigger: pull_request
      benchmark_tool: vitest-bench|hyperfine|criterion
      comparison: base-branch vs PR
      comment: auto-post results
      threshold: 10% regression = warning, 20% = failure
next_agent: Bolt
next_action: "Define benchmark targets and thresholds"
```
