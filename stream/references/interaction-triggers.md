# Interaction Triggers — YAML Templates

## ON_ARCHITECTURE_DECISION

```yaml
trigger: pipeline_design_start
questions:
  - question: "このパイプラインに最適なアーキテクチャは？"
    header: "アーキテクチャ"
    options:
      - label: "バッチ処理（推奨：日次以上の頻度）"
        description: "Airflow + dbt / Sparkで定期実行"
      - label: "ストリーミング処理"
        description: "Kafka + Flink/Sparkでリアルタイム処理"
      - label: "ハイブリッド（Lambda/Kappa）"
        description: "バッチ＋リアルタイムの両方"
      - label: "要件を確認してから決定"
        description: "レイテンシとボリュームの詳細を確認"
    multiSelect: false
```

## ON_TOOL_SELECTION

```yaml
trigger: orchestration_tool_needed
questions:
  - question: "パイプラインオーケストレーションツールは？"
    header: "ツール選定"
    options:
      - label: "Airflow（推奨：汎用性高い）"
        description: "Python DAG、豊富なオペレーター"
      - label: "Dagster"
        description: "Software-defined assets、型安全"
      - label: "Prefect"
        description: "動的ワークフロー、クラウドネイティブ"
      - label: "dbt Cloud"
        description: "SQL中心、ELT特化"
    multiSelect: false
```

## ON_QUALITY_STRATEGY

```yaml
trigger: quality_checks_design
questions:
  - question: "データ品質チェックの厳格さは？"
    header: "品質レベル"
    options:
      - label: "厳格（品質ゲート必須）"
        description: "チェック失敗でパイプライン停止"
      - label: "警告ベース"
        description: "チェック失敗は警告、処理は継続"
      - label: "サンプリング"
        description: "一部データのみチェック、パフォーマンス優先"
    multiSelect: false
```

## ON_BACKFILL_SCOPE

```yaml
trigger: backfill_planning
questions:
  - question: "バックフィルの範囲は？"
    header: "バックフィル"
    options:
      - label: "全期間再処理"
        description: "履歴データすべてを再処理"
      - label: "影響期間のみ"
        description: "問題が発生した期間のみ"
      - label: "インクリメンタル"
        description: "差分のみを段階的に処理"
    multiSelect: false
```
