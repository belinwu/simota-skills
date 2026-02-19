# Multi-Cloud Patterns

IaC templates and patterns for GCP, Azure, and Pulumi (TypeScript). Cross-cloud comparison reference.

---

## Cloud Provider Comparison

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **VPC/Network** | VPC | VPC Network | VNet |
| **Compute** | EC2, ECS, Lambda | Compute Engine, Cloud Run, Functions | VMs, App Service, Functions |
| **Database** | RDS, Aurora, DynamoDB | Cloud SQL, Spanner, Firestore | Azure SQL, Cosmos DB |
| **Kubernetes** | EKS | GKE | AKS |
| **Object Storage** | S3 | Cloud Storage | Blob Storage |
| **Secrets** | Secrets Manager | Secret Manager | Key Vault |
| **IaC State** | S3 + DynamoDB | GCS | Azure Blob |

---

## GCP - VPC Network Module

```hcl
# modules/gcp-vpc/main.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

locals {
  common_labels = {
    project     = var.project_name
    environment = var.environment
    managed-by  = "terraform"
// ...
```

## GCP - Cloud Run Service

```hcl
# modules/gcp-cloudrun/main.tf
resource "google_cloud_run_v2_service" "main" {
  name     = "${var.project_name}-${var.environment}"
  location = var.region
  project  = var.gcp_project_id

  template {
    containers {
      image = var.container_image

      resources {
        limits = {
          cpu    = var.cpu_limit
          memory = var.memory_limit
        }
// ...
```

---

## Azure - VNet Module

```hcl
# modules/azure-vnet/main.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
// ...
```

## Azure - App Service

```hcl
# modules/azure-appservice/main.tf
resource "azurerm_service_plan" "main" {
  name                = "${var.project_name}-${var.environment}-plan"
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  sku_name            = var.sku_name
  tags                = local.common_tags
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.project_name}-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location
  service_plan_id     = azurerm_service_plan.main.id
// ...
```

---

## Multi-Cloud Backend Configuration

```hcl
# GCP Backend
terraform {
  backend "gcs" {
    bucket = "myproject-terraform-state"
    prefix = "dev/terraform.tfstate"
  }
}

# Azure Backend
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "myprojecttfstate"
    container_name       = "tfstate"
    key                  = "dev/terraform.tfstate"
// ...
```

---

## Pulumi Templates (TypeScript)

### Project Structure

```
pulumi/
├── Pulumi.yaml           # Project definition
├── Pulumi.dev.yaml       # Dev stack config
├── Pulumi.staging.yaml   # Staging stack config
├── Pulumi.prod.yaml      # Prod stack config
├── index.ts              # Main entry point
├── vpc.ts                # VPC module
├── database.ts           # Database module
└── package.json
```

### VPC Module

```typescript
// pulumi/vpc.ts
import * as aws from "@pulumi/aws";
import * as pulumi from "@pulumi/pulumi";

export interface VpcArgs {
  projectName: string;
  environment: string;
  cidrBlock?: string;
  availabilityZones?: string[];
  enableNatGateway?: boolean;
}

export class Vpc extends pulumi.ComponentResource {
  public readonly vpcId: pulumi.Output<string>;
  public readonly publicSubnetIds: pulumi.Output<string>[];
// ...
```

### Main Entry Point

```typescript
// pulumi/index.ts
import * as pulumi from "@pulumi/pulumi";
import { Vpc } from "./vpc";

const config = new pulumi.Config();
const projectName = config.require("projectName");
const environment = pulumi.getStack();

const vpc = new Vpc("main", {
  projectName,
  environment,
  enableNatGateway: environment === "prod",
});

export const vpcId = vpc.vpcId;
// ...
```

### Stack Configuration

```yaml
# Pulumi.dev.yaml
config:
  aws:region: ap-northeast-1
  myproject:projectName: myproject

# Pulumi.prod.yaml
config:
  aws:region: ap-northeast-1
  myproject:projectName: myproject
  myproject:enableNatGateway: true
```

### Pulumi Commands Reference

```bash
pulumi new aws-typescript     # Initialize new project
pulumi stack select dev       # Select stack
pulumi stack init staging     # Create new stack
pulumi preview                # Preview changes
pulumi up                     # Apply changes
pulumi destroy                # Destroy resources
pulumi stack output           # View outputs
pulumi import aws:ec2/vpc:Vpc main vpc-12345678  # Import existing
```
