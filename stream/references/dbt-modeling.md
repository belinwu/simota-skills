# dbt Model Design

## Model Layer Structure

```
models/
├── staging/           # 1:1 with source tables
│   ├── stg_orders.sql
│   └── stg_customers.sql
├── intermediate/      # Business logic, joins
│   ├── int_orders_enriched.sql
│   └── int_customer_metrics.sql
├── marts/            # Final business entities
│   ├── core/
│   │   ├── dim_customers.sql
│   │   └── fct_orders.sql
│   └── marketing/
│       └── fct_campaigns.sql
└── exposures/        # BI tool connections
    └── exposures.yml
```

## Staging Model Template

```sql
-- models/staging/stg_orders.sql
{{
    config(
        materialized='view',
        tags=['staging', 'orders']
    )
}}

with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        -- Primary key
        id as order_id,

        -- Foreign keys
        customer_id,
        store_id,

        -- Dimensions
        status,
        channel,

        -- Measures
        total_amount,
        discount_amount,

        -- Timestamps
        created_at,
        updated_at,

        -- Metadata
        _loaded_at

    from source
)

select * from renamed
```

## Intermediate Model Template

```sql
-- models/intermediate/int_orders_enriched.sql
{{
    config(
        materialized='table',
        tags=['intermediate', 'orders']
    )
}}

with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

stores as (
    select * from {{ ref('stg_stores') }}
),

enriched as (
    select
        o.order_id,
        o.customer_id,
        c.customer_name,
        c.customer_segment,
        o.store_id,
        s.store_name,
        s.region,
        o.total_amount,
        o.discount_amount,
        o.total_amount - o.discount_amount as net_amount,
        o.created_at,
        date_trunc('day', o.created_at) as order_date

    from orders o
    left join customers c on o.customer_id = c.customer_id
    left join stores s on o.store_id = s.store_id
)

select * from enriched
```

## dbt Tests

```yaml
# models/staging/schema.yml
version: 2

models:
  - name: stg_orders
    description: "Staged orders from source system"
    columns:
      - name: order_id
        description: "Primary key"
        tests:
          - unique
          - not_null

      - name: customer_id
        description: "Foreign key to customers"
        tests:
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: customer_id

      - name: total_amount
        description: "Order total in cents"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 10000000  # $100,000 max
```
