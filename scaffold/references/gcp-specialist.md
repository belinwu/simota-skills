# GCP Infrastructure Specialist Reference

Advanced reference for GCP infrastructure design. Provides deep expertise beyond the basic templates in `multicloud-patterns.md`.

---

## 1. Advanced Networking

### Shared VPC

Multiple projects share a host project's network. Centralized network management.

```hcl
# Enable Shared VPC on Host Project
resource "google_compute_shared_vpc_host_project" "host" {
  project = var.host_project_id
}

# Attach Service Projects
resource "google_compute_shared_vpc_service_project" "service" {
  for_each = toset(var.service_project_ids)

  host_project    = var.host_project_id
  service_project = each.value

  depends_on = [google_compute_shared_vpc_host_project.host]
}

// ...
```

**Decision Criteria**: Shared VPC vs Separate VPCs
- No network isolation needed between teams → Shared VPC (centralized management)
- Fully independent per team → Separate VPC + VPC Peering
- Regulatory requirements mandate network isolation → VPC Service Controls

### VPC Service Controls

Restrict access to GCP services within a security perimeter. Data exfiltration prevention.

```hcl
resource "google_access_context_manager_service_perimeter" "main" {
  parent = "accessPolicies/${var.access_policy_id}"
  name   = "accessPolicies/${var.access_policy_id}/servicePerimeters/${var.perimeter_name}"
  title  = var.perimeter_name

  status {
    resources = [for p in var.protected_projects : "projects/${p}"]

    restricted_services = [
      "bigquery.googleapis.com",
      "storage.googleapis.com",
      "cloudsql.googleapis.com",
    ]

    ingress_policies {
// ...
```

### Private Google Access & Private Service Connect

```hcl
# Private Google Access (subnet level)
resource "google_compute_subnetwork" "private" {
  name                     = "${var.project_name}-${var.environment}-private"
  ip_cidr_range            = var.private_cidr
  region                   = var.region
  network                  = google_compute_network.main.id
  private_ip_google_access = true  # Private access to Google APIs
}

# Private Service Connect (connection to private services)
resource "google_compute_global_address" "psc" {
  name         = "${var.project_name}-psc-address"
  purpose      = "PRIVATE_SERVICE_CONNECT"
  address_type = "INTERNAL"
  network      = google_compute_network.main.id
// ...
```

---

## 2. Compute Patterns

### GKE (Deep)

Standard vs Autopilot + Workload Identity configuration.

```hcl
# modules/gcp-gke/main.tf

resource "google_container_cluster" "main" {
  name     = "${var.project_name}-${var.environment}"
  location = var.region
  project  = var.project_id

  # For Autopilot mode
  enable_autopilot = var.use_autopilot

  # For Standard mode only
  dynamic "node_pool" {
    for_each = var.use_autopilot ? [] : [1]
    content {
      name = "default"
// ...
```

**Standard vs Autopilot**:
| Criteria | Standard | Autopilot |
|----------|----------|-----------|
| Node management | Manual (Node Pool) | Automatic |
| Billing | Per node | Per pod |
| GPU | Supported | Supported (with limitations) |
| Customization | High | Limited |
| Recommended for | Advanced customization needed | Most use cases |

### Cloud Run (Advanced)

```hcl
resource "google_cloud_run_v2_service" "main" {
  name     = "${var.project_name}-${var.environment}"
  location = var.region
  project  = var.project_id

  template {
    service_account = google_service_account.app.email

    containers {
      image = var.container_image

      resources {
        limits   = { cpu = var.cpu_limit, memory = var.memory_limit }
        cpu_idle = var.environment != "prod"  # dev/staging: stop CPU when idle
      }
// ...
```

---

## 3. Database Patterns

### Cloud SQL (Advanced)

```hcl
# modules/gcp-cloudsql/main.tf

resource "google_sql_database_instance" "main" {
  name             = "${var.project_name}-${var.environment}"
  database_version = var.database_version
  region           = var.region
  project          = var.project_id

  settings {
    tier              = var.tier
    availability_type = var.environment == "prod" ? "REGIONAL" : "ZONAL"
    disk_autoresize   = true
    disk_type         = "PD_SSD"

    ip_configuration {
// ...
```

### AlloyDB vs Cloud SQL vs Spanner

| Requirement | Cloud SQL | AlloyDB | Cloud Spanner |
|-------------|-----------|---------|---------------|
| Use case | General OLTP | High-performance PostgreSQL | Global distribution, strong consistency |
| Scaling | Vertical (up to 96 vCPU) | Vertical + read pools | Horizontal (unlimited) |
| Availability | 99.95% | 99.99% | 99.999% (multi-region) |
| Cost estimate (monthly) | $50+ | $500+ | $2,000+ |
| PostgreSQL compatible | Full | Full | Not compatible (proprietary SQL) |
| Recommended for | Standard web apps | Mixed analytics + transactional | Finance, gaming, global apps |

---

## 4. Storage & CDN

### Cloud Storage (Advanced)

```hcl
resource "google_storage_bucket" "main" {
  name     = "${var.project_id}-${var.project_name}-${var.environment}"
  location = var.region
  project  = var.project_id

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning { enabled = var.environment == "prod" }

  lifecycle_rule {
    condition { age = 90 }
    action { type = "SetStorageClass"; storage_class = "NEARLINE" }
  }

// ...
```

**Storage Class Selection Criteria**:
- **STANDARD**: Frequently accessed data
- **NEARLINE**: Accessed ~once per month (30-day minimum storage)
- **COLDLINE**: Accessed ~once per quarter (90-day minimum)
- **ARCHIVE**: Accessed less than once per year (365-day minimum)

### Cloud Armor (WAF + DDoS Protection)

```hcl
resource "google_compute_security_policy" "main" {
  name    = var.policy_name
  project = var.project_id

  rule {
    action   = "allow"
    priority = "2147483647"
    match { versioned_expr = "SRC_IPS_V1"; config { src_ip_ranges = ["*"] } }
    description = "Default allow"
  }

  # OWASP Top 10 protection
  rule {
    action   = "deny(403)"
    priority = "1000"
// ...
```

---

## 5. Messaging & Events

### Pub/Sub

```hcl
resource "google_pubsub_topic" "main" {
  name    = var.topic_name
  project = var.project_id
  message_retention_duration = "86400s"
  labels = { managed-by = "terraform" }
}

resource "google_pubsub_topic" "dead_letter" {
  name    = "${var.topic_name}-dead-letter"
  project = var.project_id
  labels = { managed-by = "terraform", purpose = "dead-letter" }
}

resource "google_pubsub_subscription" "main" {
  for_each = var.subscriptions
// ...
```

### Cloud Tasks vs Pub/Sub

| Aspect | Pub/Sub | Cloud Tasks |
|--------|---------|-------------|
| Pattern | 1:N (fan-out) | 1:1 (task queue) |
| Rate control | None | Available (QPS limiting) |
| Scheduled execution | None | Available (delayed delivery) |
| Recommended for | Event notifications, streaming | API call throttling, batch processing |

### Workflows

Orchestration of multiple services. Sequenced control of Cloud Run / Cloud Functions / API calls.

```yaml
# workflow.yaml - Example: Order processing pipeline
main:
  params: [input]
  steps:
    - validate_order:
        call: http.post
        args:
          url: ${VALIDATE_URL}
          body: ${input}
        result: validation_result
    - check_validation:
        switch:
          - condition: ${validation_result.body.valid == true}
            next: process_payment
          - condition: ${validation_result.body.valid == false}
# ...
```

---

## 6. IAM & Security (Advanced)

### Organization Policies

```hcl
# Region restriction
resource "google_org_policy_policy" "restrict_regions" {
  name   = "organizations/${var.org_id}/policies/gcp.resourceLocations"
  parent = "organizations/${var.org_id}"
  spec {
    rules {
      values { allowed_values = ["in:asia-northeast1-locations", "in:asia-northeast2-locations"] }
    }
  }
}

# Enforce uniform bucket-level access
resource "google_org_policy_policy" "uniform_bucket_access" {
  name   = "organizations/${var.org_id}/policies/storage.uniformBucketLevelAccess"
  parent = "organizations/${var.org_id}"
// ...
```

### Workload Identity Federation (GitHub Actions)

Eliminate service account keys; use short-lived authentication tokens via OIDC.

```hcl
resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = "github-actions"
  display_name              = "GitHub Actions"
  project                   = var.project_id
}

resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-oidc"
  display_name                       = "GitHub OIDC"
  project                            = var.project_id

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
// ...
```

GitHub Actions side:
```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    permissions: { contents: read, id-token: write }
    steps:
      - uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-actions/providers/github-oidc
          service_account: deploy-sa@PROJECT_ID.iam.gserviceaccount.com
```

---

## 7. Observability

### Cloud Monitoring & Logging

```hcl
# Alert Policy: Cloud Run error rate
resource "google_monitoring_alert_policy" "cloudrun_error_rate" {
  display_name = "${var.project_name}-${var.environment} Cloud Run Error Rate"
  combiner     = "OR"
  project      = var.project_id

  conditions {
    display_name = "Error rate > 5%"
    condition_threshold {
      filter          = "resource.type = \"cloud_run_revision\" AND metric.type = \"run.googleapis.com/request_count\" AND metric.labels.response_code_class != \"2xx\""
      comparison      = "COMPARISON_GT"
      threshold_value = 5
      duration        = "300s"
      aggregations {
        alignment_period     = "60s"
// ...
```

---

## 8. Cost Optimization (GCP-Specific)

### Cost Reference (Tokyo Region, approximate)

| Resource | Spec | Monthly (USD) |
|----------|------|---------------|
| **Cloud Run** | 0.5 vCPU, 256 MiB, 1M requests | $20-50 |
| **Cloud SQL** | db-custom-2-8192 (HA) | $250 |
| **Cloud SQL** | db-custom-2-8192 (Single) | $130 |
| **GKE Autopilot** | 2 vCPU, 4 GiB (always-on) | $80 |
| **GKE Standard** | e2-standard-4 x 3 nodes | $300 |
| **Cloud Storage** | 100 GB (Standard) | $2.6 |
| **Cloud NAT** | Gateway + 1 GB transfer | $35 |
| **Cloud Armor** | Policy + 1M requests | $12 |
| **Pub/Sub** | 1M messages | $0.04 |

### CUD (Committed Use Discounts)

| Type | Discount | Applicable to |
|------|----------|---------------|
| Resource-based | 1-year: 37%, 3-year: 55% | vCPU, memory (GCE, GKE Standard) |
| Spend-based | 1-year: 25%, 3-year: 52% | Cloud SQL, Cloud Run (partial) |

### Environment-Specific Cost Optimization Patterns

| Pattern | Dev | Staging | Prod |
|---------|-----|---------|------|
| Cloud SQL | Single-AZ, small tier | Single-AZ | Regional HA |
| Cloud Run min_instances | 0 | 0 | 1-2 |
| GKE nodes | Spot VMs only | Spot + On-demand | On-demand + Spot (burst) |
| Cloud NAT | Remove if unnecessary | Shared | Dedicated |
| Log retention | 7 days | 30 days | 90-365 days |
| Cloud Armor | Not needed | Basic | Full WAF |

---

## 9. Cloud Architecture Framework Quick Reference

| Pillar | Key Points | Key Practices |
|--------|-----------|---------------|
| **System Design** | Region/zone selection, redundancy | Multi-zone / multi-region configuration |
| **Operational Excellence** | SRE practices, error budgets | SLI/SLO definition, automated incident response |
| **Security** | Zero trust, BeyondCorp | Workload Identity, VPC SC, IAP |
| **Reliability** | Disaster recovery, chaos engineering | Multi-region failover |
| **Cost Optimization** | CUDs, right-sizing | Label-based cost allocation, Active Assist |
| **Performance** | Caching, CDN, global LB | Cloud CDN, Memorystore |

---

## 10. GCP Service Decision Matrix

| Use Case | Recommended | Alternative | Avoid |
|----------|-------------|-------------|-------|
| Web API (stateless) | Cloud Run | GKE Autopilot (when K8s required) | Compute Engine |
| Batch processing | Cloud Run Jobs | Dataflow (streaming) | Compute Engine |
| Static site | Cloud Storage + CDN | Firebase Hosting | Compute Engine |
| Message queue | Pub/Sub | Cloud Tasks (when rate control needed) | Self-managed Kafka |
| Relational DB | Cloud SQL | AlloyDB (high-performance requirements) | Self-managed on GCE |
| NoSQL | Firestore (Native mode) | Bigtable (large-scale analytics data) | Datastore mode (new projects) |
| Container orchestration | Cloud Run | GKE Autopilot | GKE Standard (unless requirements demand it) |
| Data warehouse | BigQuery | AlloyDB (HTAP) | Cloud SQL |
| CI/CD | Cloud Build | GitHub Actions + WIF | Jenkins on GCE |
| Secrets management | Secret Manager | - | Hardcoded in environment variables |

**Selection Principles**:
- Serverless-first (Cloud Run > GKE > GCE)
- Prefer managed services
- Thorough labeling for cost visibility
