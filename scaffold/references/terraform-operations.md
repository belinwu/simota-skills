# Terraform Operations

State management, import, drift detection, workspaces, and module versioning patterns.

---

## State Management

### State Commands Quick Reference

| Command | Purpose | Risk |
|---------|---------|------|
| `terraform state list` | List all resources in state | Safe |
| `terraform state show <addr>` | Show resource details | Safe |
| `terraform state mv <src> <dst>` | Rename/move resource in state | Medium |
| `terraform state rm <addr>` | Remove resource from state (no destroy) | High |
| `terraform state pull` | Download remote state to stdout | Safe |
| `terraform state push` | Upload local state to remote | High |
| `terraform state replace-provider` | Change provider in state | Medium |

### State Move (Refactoring)

```hcl
# Rename a resource (state-only, no infrastructure change)
terraform state mv 'aws_instance.web' 'aws_instance.app'

# Move into a module
terraform state mv 'aws_instance.app' 'module.compute.aws_instance.app'

# Move between modules
terraform state mv 'module.old.aws_s3_bucket.data' 'module.new.aws_s3_bucket.data'

# Move indexed resource
terraform state mv 'aws_subnet.public[0]' 'aws_subnet.public["az-a"]'
```

### Moved Blocks (Terraform 1.1+)

Declarative refactoring — safer alternative to `terraform state mv`:

```hcl
# Rename resource
moved {
  from = aws_instance.web
  to   = aws_instance.app
}

# Move into module
moved {
  from = aws_s3_bucket.assets
  to   = module.storage.aws_s3_bucket.assets
}

# Rename module
moved {
  from = module.old_name
  to   = module.new_name
}
```

**Best practice:** Keep `moved` blocks for 2-3 months after apply, then remove.

### Import

#### Import Block (Terraform 1.5+, Recommended)

```hcl
# import.tf
import {
  to = aws_s3_bucket.existing
  id = "my-existing-bucket-name"
}

import {
  to = aws_iam_role.existing
  id = "existing-role-name"
}

import {
  to = google_compute_instance.existing
  id = "projects/my-project/zones/asia-northeast1-a/instances/my-vm"
}
```

```bash
# Generate HCL from imported resources
terraform plan -generate-config-out=generated.tf
```

#### CLI Import (Legacy)

```bash
terraform import aws_s3_bucket.existing my-existing-bucket-name
terraform import 'aws_instance.web[0]' i-1234567890abcdef0
terraform import 'module.vpc.aws_vpc.main' vpc-abc123
```

### State Remove (Unmanage)

```bash
# Stop managing a resource without destroying it
terraform state rm 'aws_instance.legacy'
terraform state rm 'module.deprecated'

# Remove all resources in a module
terraform state rm 'module.old_module'
```

---

## Workspaces

### When to Use

| Approach | Use Case | Recommendation |
|----------|----------|----------------|
| **Workspaces** | Same config, different state (dev/staging/prod) | Simple projects |
| **Directory-per-env** | Different configs per environment | Complex projects (recommended) |
| **Terragrunt** | DRY multi-environment with overrides | Large-scale projects |

### Workspace Commands

```bash
terraform workspace list
terraform workspace new dev
terraform workspace select prod
terraform workspace show        # Current workspace
terraform workspace delete dev  # Cannot delete if resources exist
```

### Workspace-Aware Config

```hcl
locals {
  env_config = {
    dev = {
      instance_type = "t3.micro"
      min_size      = 1
      max_size      = 2
      multi_az      = false
    }
    staging = {
      instance_type = "t3.small"
      min_size      = 1
      max_size      = 3
      multi_az      = false
    }
    prod = {
      instance_type = "t3.medium"
      min_size      = 2
      max_size      = 10
      multi_az      = true
    }
  }

  config = local.env_config[terraform.workspace]
}

resource "aws_instance" "app" {
  instance_type = local.config.instance_type
  # ...
}
```

---

## Drift Detection

### Plan-Based Detection

```bash
# Exit code: 0 = no changes, 1 = error, 2 = changes detected
terraform plan -detailed-exitcode -out=drift.tfplan

# JSON output for automation
terraform plan -json -out=drift.tfplan 2>/dev/null | jq '.resource_changes[]? | select(.change.actions != ["no-op"])'
```

### CI/CD Drift Detection (GitHub Actions)

```yaml
# .github/workflows/drift-detection.yml
name: Terraform Drift Detection
on:
  schedule:
    - cron: '0 9 * * 1-5'  # Weekdays 9 AM UTC

jobs:
  drift:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3

      - name: Terraform Init
        run: terraform init
        working-directory: environments/${{ matrix.environment }}

      - name: Drift Check
        id: plan
        run: |
          terraform plan -detailed-exitcode -no-color 2>&1 | tee plan.txt
          echo "exitcode=$?" >> $GITHUB_OUTPUT
        working-directory: environments/${{ matrix.environment }}
        continue-on-error: true

      - name: Notify on Drift
        if: steps.plan.outputs.exitcode == '2'
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {"text": "Terraform drift detected in ${{ matrix.environment }}"}
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Refresh and Reconcile

```bash
# Refresh state from real infrastructure
terraform apply -refresh-only

# Preview refresh changes
terraform plan -refresh-only
```

---

## Module Versioning

### Registry Module Source

```hcl
# Terraform Registry
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"  # Allow 5.x patches, block 6.0
}

# Git with tag
module "internal" {
  source = "git::https://github.com/org/terraform-modules.git//modules/vpc?ref=v1.2.0"
}

# S3 bucket
module "shared" {
  source = "s3::https://s3-ap-northeast-1.amazonaws.com/terraform-modules/vpc.zip"
}
```

### Version Constraint Patterns

| Constraint | Meaning | Use When |
|-----------|---------|----------|
| `= 1.2.3` | Exact version | Maximum stability |
| `~> 1.2` | Allow 1.2.x (patch only) | Production (recommended) |
| `~> 1.0` | Allow 1.x.x (minor + patch) | Staging |
| `>= 1.0, < 2.0` | Range | Flexible but bounded |

### Module Upgrade Workflow

```bash
# 1. Check current versions
terraform providers lock -platform=linux_amd64 -platform=darwin_amd64

# 2. Update .terraform.lock.hcl
terraform init -upgrade

# 3. Preview changes
terraform plan

# 4. Apply if safe
terraform apply
```

---

## Terraform Upgrade Patterns

### Version Constraint

```hcl
terraform {
  required_version = ">= 1.5.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}
```

### Upgrade Checklist

1. Read changelog for breaking changes
2. Run `terraform init -upgrade` in dev first
3. Run `terraform plan` — check for unexpected changes
4. Apply to dev → staging → prod with validation between each
5. Update `.terraform.lock.hcl` and commit

---

## Backend Migration

### S3 → S3 (Different Bucket/Key)

```bash
# 1. Pull current state
terraform state pull > terraform.tfstate.backup

# 2. Update backend config
# backend.tf: change bucket/key

# 3. Re-init with migration
terraform init -migrate-state

# 4. Verify
terraform plan  # Should show no changes
```

### Local → Remote

```bash
# 1. Add backend config
# backend.tf: add S3/GCS backend block

# 2. Init with migration
terraform init -migrate-state
# Terraform will ask: "Do you want to copy existing state?"
# Answer: yes

# 3. Verify
terraform plan  # Should show no changes

# 4. Remove local state file
rm terraform.tfstate terraform.tfstate.backup
```
