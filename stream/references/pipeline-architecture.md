# Pipeline Architecture

## Batch vs Streaming Decision Matrix

| Factor | Batch | Streaming | Hybrid |
|--------|-------|-----------|--------|
| **Latency requirement** | Hours/Days | Seconds/Minutes | Mixed |
| **Data volume** | Large, bounded | Continuous | Both |
| **Processing complexity** | Complex joins/aggregations | Simple transforms | Both |
| **Cost sensitivity** | High (optimize resources) | Lower (always-on) | Balanced |
| **Replay requirement** | Easy | Complex | Depends |

## Decision Tree

```
                    Latency < 1 minute?
                    /              \
                  YES               NO
                   |                 |
          Volume > 10K/sec?     Complex analytics?
          /          \          /          \
        YES          NO       YES           NO
         |            |        |             |
     Kafka +       Kafka    Batch        Simple Batch
     Flink/Spark   Only     (Spark)      (Airflow)
```

## Architecture Patterns

### Pattern 1: Lambda Architecture (Legacy)

```
Raw Data ──┬── Batch Layer ──── Batch View ──┐
           │                                  ├── Serving Layer
           └── Speed Layer ──── Real-time ───┘
```

**Use when:** Legacy systems require both batch accuracy and real-time speed
**Avoid:** Complexity is high; prefer Kappa for new systems

### Pattern 2: Kappa Architecture (Recommended)

```
Raw Data ─── Stream Processing ─── Serving Layer
                    │
              Replay from log
```

**Use when:** All processing can be unified as stream processing
**Key:** Kafka as immutable log enables replay

### Pattern 3: Medallion Architecture (Data Lake)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Bronze    │───▶│   Silver    │───▶│    Gold     │
│   (Raw)     │    │  (Cleaned)  │    │ (Business)  │
└─────────────┘    └─────────────┘    └─────────────┘
```

**Use when:** Data lake with progressive refinement
**Tools:** Databricks, Delta Lake, Apache Iceberg

---

## ETL vs ELT Selection

| Aspect | ETL | ELT |
|--------|-----|-----|
| **Transform location** | Before loading | After loading |
| **Best for** | Limited destination compute | Powerful data warehouse |
| **Data volume** | Small to medium | Large |
| **Flexibility** | Less (predefined transforms) | More (SQL-based) |
| **Tools** | Airflow + Python | dbt + Snowflake/BigQuery |

## ELT Pipeline Template (dbt)

```
Sources ─── Staging ─── Intermediate ─── Marts ─── Exposures
   │           │             │             │           │
   │       Raw copy      Business      Aggregated   BI/API
   │       + types       logic         metrics      output
   │
   └── External systems (APIs, files, DBs)
```

## ETL Pipeline Template (Airflow)

```python
# dags/etl_pipeline.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'etl_orders_daily',
    default_args=default_args,
    description='Daily orders ETL pipeline',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['etl', 'orders'],
) as dag:

    extract = PythonOperator(
        task_id='extract_orders',
        python_callable=extract_from_source,
        op_kwargs={'date': '{{ ds }}'},
    )

    validate_source = PythonOperator(
        task_id='validate_source_data',
        python_callable=run_quality_checks,
        op_kwargs={'stage': 'source'},
    )

    transform = PythonOperator(
        task_id='transform_orders',
        python_callable=apply_business_logic,
    )

    validate_transform = PythonOperator(
        task_id='validate_transformed',
        python_callable=run_quality_checks,
        op_kwargs={'stage': 'transform'},
    )

    load = PostgresOperator(
        task_id='load_to_warehouse',
        postgres_conn_id='warehouse',
        sql='sql/load_orders.sql',
    )

    extract >> validate_source >> transform >> validate_transform >> load
```
