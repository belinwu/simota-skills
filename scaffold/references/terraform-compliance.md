# Terraform Compliance & Policy-as-Code

Static analysis, policy enforcement, and compliance validation for Terraform configurations.

---

## Tool Comparison

| Tool | Type | Language | Best For |
|------|------|----------|----------|
| **tfsec** (trivy) | Static analysis | Go (built-in rules) | Quick security scanning |
| **Checkov** | Static analysis | Python (built-in + custom) | Broad compliance coverage |
| **OPA/Conftest** | Policy engine | Rego | Custom organizational policies |
| **Sentinel** | Policy-as-code | Sentinel | HCP Terraform/Enterprise gate |
| **terraform validate** | Built-in | HCL | Syntax and type checking |
| **TFLint** | Linter | Go | Provider-specific best practices |

---

## tfsec (Trivy)

tfsec is now part of Trivy. Fast, zero-config security scanner.

### Setup

```bash
brew install trivy        # macOS
# or
brew install tfsec        # Legacy standalone

# Run
trivy config /path/to/terraform
# or
tfsec /path/to/terraform
```

### Common Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| AVD-AWS-0086 | S3 bucket without encryption | HIGH |
| AVD-AWS-0089 | S3 bucket with public access | CRITICAL |
| AVD-AWS-0107 | RDS without encryption | HIGH |
| AVD-AWS-0104 | Security group with unrestricted ingress | HIGH |
| AVD-AWS-0178 | ECS task definition with root user | HIGH |
| AVD-GCP-0029 | Cloud SQL without SSL | HIGH |
| AVD-GCP-0024 | GKE cluster without network policy | MEDIUM |

### Inline Ignoring

```hcl
resource "aws_security_group_rule" "allow_all_egress" {
  #trivy:ignore:AVD-AWS-0104
  type        = "egress"
  cidr_blocks = ["0.0.0.0/0"]  # Required for internet access
  # ...
}
```

### Config File

```yaml
# .trivy.yaml
severity:
  - CRITICAL
  - HIGH
scan:
  skip-dirs:
    - modules/deprecated
  skip-files:
    - "**/*_test.tf"
```

---

## Checkov

Comprehensive policy scanner with 1000+ built-in checks.

### Setup

```bash
pip install checkov
# or
brew install checkov
```

### Usage

```bash
# Scan directory
checkov -d /path/to/terraform

# Specific framework
checkov -d . --framework terraform

# Output formats
checkov -d . -o json
checkov -d . -o sarif  # GitHub Security tab

# Skip specific checks
checkov -d . --skip-check CKV_AWS_18,CKV_AWS_21

# Run specific checks only
checkov -d . --check CKV_AWS_79,CKV_AWS_88
```

### Key Check IDs

| Check ID | Description |
|----------|-------------|
| CKV_AWS_18 | S3 access logging enabled |
| CKV_AWS_19 | S3 SSE enabled |
| CKV_AWS_21 | S3 versioning enabled |
| CKV_AWS_79 | Instance metadata v2 (IMDSv2) |
| CKV_AWS_88 | EC2 public IP disabled |
| CKV_AWS_145 | RDS encryption enabled |
| CKV_AWS_161 | RDS IAM auth enabled |
| CKV_GCP_6 | Cloud SQL no public IP |
| CKV_GCP_12 | GKE network policy enabled |

### Custom Check (Python)

```python
# custom_checks/s3_naming.py
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories

class S3BucketNaming(BaseResourceCheck):
    def __init__(self):
        name = "Ensure S3 bucket follows naming convention"
        id = "CKV_CUSTOM_1"
        supported_resources = ["aws_s3_bucket"]
        categories = [CheckCategories.CONVENTION]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        bucket = conf.get("bucket", [""])[0]
        if bucket and bucket.startswith(("dev-", "staging-", "prod-")):
            return CheckResult.PASSED
        return CheckResult.FAILED

check = S3BucketNaming()
```

```bash
checkov -d . --external-checks-dir custom_checks/
```

### .checkov.yaml

```yaml
# .checkov.yaml
directory:
  - .
framework:
  - terraform
skip-check:
  - CKV_AWS_18   # S3 logging - handled by centralized logging
  - CKV2_AWS_62  # S3 event notifications - not needed
output:
  - cli
  - sarif
soft-fail-on:
  - CKV_AWS_21   # S3 versioning - warn only for dev
```

---

## OPA / Conftest

Custom organizational policies using Open Policy Agent (Rego).

### Setup

```bash
brew install conftest
```

### Policy Structure

```
policy/
├── terraform.rego       # Main policy
├── tagging.rego         # Tagging policies
├── cost.rego            # Cost guard policies
└── data.json            # Policy data (allowed instance types, etc.)
```

### Tagging Policy

```rego
# policy/tagging.rego
package terraform

required_tags := {"Environment", "Project", "ManagedBy"}

deny[msg] {
  resource := input.resource_changes[_]
  resource.change.actions[_] == "create"

  tags := object.get(resource.change.after, "tags", {})
  missing := required_tags - {key | tags[key]}
  count(missing) > 0

  msg := sprintf(
    "%s '%s' is missing required tags: %v",
    [resource.type, resource.address, missing]
  )
}
```

### Cost Guard Policy

```rego
# policy/cost.rego
package terraform

expensive_instance_types := {
  "m5.4xlarge", "m5.8xlarge", "m5.12xlarge",
  "c5.4xlarge", "c5.9xlarge",
  "r5.4xlarge", "r5.8xlarge",
  "p3.2xlarge", "p3.8xlarge",
}

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_instance"
  resource.change.actions[_] == "create"

  instance_type := resource.change.after.instance_type
  expensive_instance_types[instance_type]

  msg := sprintf(
    "Instance '%s' uses expensive type '%s'. Requires approval.",
    [resource.address, instance_type]
  )
}

warn[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_nat_gateway"
  resource.change.actions[_] == "create"

  msg := sprintf(
    "NAT Gateway '%s' costs ~$45/month. Consider VPC endpoints instead.",
    [resource.address]
  )
}
```

### Security Policy

```rego
# policy/security.rego
package terraform

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_security_group_rule"
  resource.change.actions[_] == "create"

  resource.change.after.type == "ingress"
  cidr := resource.change.after.cidr_blocks[_]
  cidr == "0.0.0.0/0"
  resource.change.after.from_port != 443
  resource.change.after.from_port != 80

  msg := sprintf(
    "Security group rule '%s' allows unrestricted ingress on port %d",
    [resource.address, resource.change.after.from_port]
  )
}

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  resource.change.actions[_] == "create"

  not resource.change.after.server_side_encryption_configuration

  msg := sprintf("S3 bucket '%s' must have encryption enabled", [resource.address])
}
```

### Usage

```bash
# Generate plan JSON
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json

# Run policies
conftest test plan.json -p policy/

# Specific policy file
conftest test plan.json -p policy/tagging.rego

# Output formats
conftest test plan.json -p policy/ -o json
conftest test plan.json -p policy/ -o table
```

### CI/CD Integration

```yaml
# .github/workflows/terraform-policy.yml
- name: Policy Check
  run: |
    terraform plan -out=plan.tfplan
    terraform show -json plan.tfplan > plan.json
    conftest test plan.json -p policy/ --no-fail
```

---

## Sentinel (HCP Terraform / Enterprise)

### Policy Example

```sentinel
# Enforce tagging
import "tfplan/v2" as tfplan

required_tags = ["Environment", "Project", "ManagedBy"]

main = rule {
  all tfplan.resource_changes as _, rc {
    rc.mode is "managed" and
    rc.change.actions contains "create" implies
    all required_tags as tag {
      rc.change.after.tags contains tag
    }
  }
}
```

### Enforcement Levels

| Level | Behavior |
|-------|----------|
| `advisory` | Warn but allow apply |
| `soft-mandatory` | Block apply, can override |
| `hard-mandatory` | Block apply, no override |

---

## Terraform Custom Validation

Built-in validation rules (no external tools required):

```hcl
variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_type" {
  type = string
  validation {
    condition     = can(regex("^t3\\.|^t4g\\.", var.instance_type))
    error_message = "Only t3.* and t4g.* instance types are allowed in this project."
  }
}

variable "cidr_block" {
  type = string
  validation {
    condition     = can(cidrhost(var.cidr_block, 0))
    error_message = "Must be a valid CIDR block."
  }
}
```

### Lifecycle Preconditions/Postconditions (Terraform 1.2+)

```hcl
resource "aws_instance" "app" {
  instance_type = var.instance_type
  ami           = data.aws_ami.app.id

  lifecycle {
    precondition {
      condition     = data.aws_ami.app.architecture == "x86_64"
      error_message = "AMI must be x86_64 architecture."
    }

    postcondition {
      condition     = self.public_ip != ""
      error_message = "Instance must have a public IP assigned."
    }
  }
}
```

---

## Pre-Commit Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.96.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
        args: ['--args=--config=__GIT_WORKING_DIR__/.tflint.hcl']
      - id: terraform_docs
        args: ['--args=--config=.terraform-docs.yml']

  - repo: https://github.com/aquasecurity/trivy
    rev: v0.55.0
    hooks:
      - id: trivy-config
        args: ['--severity', 'HIGH,CRITICAL']

  - repo: https://github.com/bridgecrewio/checkov
    rev: 3.2.0
    hooks:
      - id: checkov
        args: ['--framework', 'terraform', '--quiet']
```

---

## TFLint

Provider-aware linter for Terraform.

### Setup

```bash
brew install tflint
```

### Config

```hcl
# .tflint.hcl
config {
  call_module_type = "local"
}

plugin "aws" {
  enabled = true
  version = "0.31.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

plugin "google" {
  enabled = true
  version = "0.28.0"
  source  = "github.com/terraform-linters/tflint-ruleset-google"
}

rule "terraform_naming_convention" {
  enabled = true
  format  = "snake_case"
}

rule "terraform_documented_variables" {
  enabled = true
}

rule "terraform_documented_outputs" {
  enabled = true
}
```

### Key Rules

| Rule | Description |
|------|-------------|
| `aws_instance_invalid_type` | Invalid EC2 instance type |
| `aws_db_instance_invalid_type` | Invalid RDS instance class |
| `google_compute_instance_invalid_machine_type` | Invalid GCE machine type |
| `terraform_naming_convention` | Enforce naming patterns |
| `terraform_unused_declarations` | Unused variables/locals |
