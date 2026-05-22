# dbt Model Design

Purpose: canonical dbt layer structure, naming, materialization defaults, and test expectations for Stream output.

## Contents

1. Layer structure
2. Naming rules
3. Materialization defaults
4. Minimal templates
5. Core tests
6. 2026 engine baseline (dbt Fusion + Semantic Layer)

## 2026 Engine Baseline

- **dbt Fusion engine** (Rust-based, true SQL compiler) is now the recommended engine for new projects. Published benchmarks show it parses a `10,000`-model project up to `~30x` faster than dbt Core. Use it whenever the project is greenfield or the team is already migrating; stay on dbt Core only when third-party adapters have not been ported yet.
- **Semantic Layer (new YAML spec)** embeds semantic-model definitions inside the corresponding model YAML — no more parallel `*.yml` directory for semantics. Measures are now expressed as simple metrics; deeply nested option blocks have been flattened into top-level keys.
- **Data contracts** are first-class: a contract on a model enforces column names, data types, and constraints at build time, and Fusion blocks PRs that would break a contracted column without an explicit versioned migration.
- **Model versions** pair with contracts to evolve schemas without breaking downstream — define `v1`, `v2` and let consumers migrate on their own cadence.

These four pieces together — Fusion, embedded Semantic Layer YAML, contracts, model versions — are the 2026 production baseline. Greenfield projects should adopt all four from day one; legacy projects should migrate in the order: contracts on critical marts → model versions on changing tables → Semantic Layer flatten → Fusion engine.

## Layer Structure

```text
models/
├── staging/
├── intermediate/
├── marts/
└── exposures/
```

### Roles

| Layer | Purpose | Rules |
|-------|---------|-------|
| `staging` | source-aligned cleanup | `1:1` with source tables; no joins |
| `intermediate` | business logic and enrichment | small, reusable, single-responsibility transforms |
| `marts` | business-facing outputs | `dim_*`, `fct_*`, `rpt_*` |
| `exposures` | BI or API dependencies | document downstream usage |

## Naming Rules

- `stg_{source}__{entity}`
- `int_{entity}_{verb}`
- `dim_{entity}`
- `fct_{event}`
- `rpt_{report}`

## Materialization Defaults

| Layer | Default |
|-------|---------|
| `stg_*` | `view` |
| `int_*` | `ephemeral` or `table` |
| `dim_*` | `table` |
| `fct_*` | `table` or `incremental` |
| `rpt_*` | `table` |

## Minimal Templates

### Staging

```sql
{{ config(materialized='view', tags=['staging']) }}

with source as (
  select * from {{ source('raw', 'orders') }}
)
select
  id as order_id,
  customer_id,
  total_amount,
  created_at,
  updated_at
from source
```

### Intermediate

```sql
{{ config(materialized='table', tags=['intermediate']) }}

with orders as (
  select * from {{ ref('stg_orders') }}
)
select
  order_id,
  customer_id,
  total_amount,
  date_trunc('day', created_at) as order_date
from orders
```

## Core Tests

Always define:
- `unique` and `not_null` on primary keys
- `relationships` on foreign keys
- range or business-rule tests for critical measures
