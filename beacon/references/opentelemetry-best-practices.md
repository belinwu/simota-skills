# OpenTelemetry Best Practices

> OTel 計装戦略、Semantic Conventions、Collector パイプライン、サンプリング、テレメトリ相関

## 1. 計装戦略

| # | プラクティス | 説明 | 重要度 |
|---|-----------|------|--------|
| **OT-01** | **Auto-first, Manual-second** | 自動計装で即時可視化→ビジネスクリティカルパスに手動計装追加 | 必須 |
| **OT-02** | **SDK 初期化を最優先** | アプリケーション起動シーケンスの最初に OTel SDK を初期化 | 必須 |
| **OT-03** | **Span は必ず close** | async/await + finally ブロックで確実にクローズ | 必須 |
| **OT-04** | **ビジネス属性の付加** | 自動スパンにビジネス関連属性を追加（customer_tier, order_value 等） | 推奨 |
| **OT-05** | **エラーとイベントの記録** | 状態遷移やエラーをスパンイベントとして記録 | 推奨 |

```
初期化順序（重要）:
  // 1. OTel SDK を最初に初期化
  const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
  const provider = new NodeTracerProvider();
  provider.register();

  // 2. その後にアプリケーションモジュールをインポート
  const express = require('express');
```

---

## 2. Semantic Conventions & 属性管理

```
標準属性（必ず準拠）:
  HTTP:   http.method, http.status_code, http.route
  DB:     db.system, db.statement, db.name
  Messaging: messaging.system, messaging.destination
  RPC:    rpc.system, rpc.service, rpc.method

アプリケーション固有属性:
  - プレフィックス: app.* を使用
  - 命名規則: snake_case で統一
  - 例: app.customer_tier, app.order_value, app.feature_flag

属性追加のアンチパターン:
  ❌ 全スパンに高カーディナリティ属性（user_id 等）を付加
  ❌ 同一属性の重複（親子スパンで同じ値）
  ❌ メトリクスやログ情報をスパン属性に混在
  ❌ 省略形・略語の使用（svc → service）
```

---

## 3. Collector デプロイメントパターン

| パターン | 構成 | メリット | デメリット | 推奨度 |
|---------|------|---------|----------|--------|
| **Agent** | 各アプリ横にサイドカー | ネットワーク最小、アプリ間分離 | 設定管理が分散 | 小規模 |
| **Gateway** | 中央集約サーバー | 設定一元化、ルーティング集約 | SPOF リスク | 中規模 |
| **Hierarchical** | Agent + Gateway 併用 | 信頼性と管理性の最適バランス | 複雑性増 | 大規模（推奨） |

```
Collector 基本設定:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317

  processors:
    memory_limiter:        # OOM 防止（必須）
      check_interval: 1s
      limit_mib: 1000
    batch:                 # ネットワーク効率化
      send_batch_size: 10000
      timeout: 10s

  exporters:
    otlp:
      endpoint: observability-backend:4317

  service:
    pipelines:
      traces:
        receivers: [otlp]
        processors: [memory_limiter, batch]  # memory_limiter は常に最初
        exporters: [otlp]

PII/PHI フィルタリング（Collector で処理）:
  processors:
    filter:
      spans:
        include:
          match_type: regexp
          attributes:
            - key: db.statement
              value: "(?i)(?:password|passwd)\\s*=\\s*[^\\s,;]+"
        actions:
          - key: db.statement
            action: update
            value: "REDACTED"
```

---

## 4. サンプリング戦略

| 方式 | 決定タイミング | メリット | デメリット | 用途 |
|------|-------------|---------|----------|------|
| **Head Sampling** | トレース開始時 | シンプル、低オーバーヘッド | エラートレース取りこぼし | 開発環境 |
| **Tail Sampling** | トレース完了後 | インテリジェント判断 | バッファリング必要 | 本番推奨 |
| **Probabilistic** | ランダム % | 予測可能なコスト | エラー見逃しリスク | 高トラフィック |
| **Rate Limiting** | 時間単位上限 | トラフィックスパイク制御 | 重要トレース欠損リスク | バースト対策 |

```
推奨: 複合サンプリング戦略
  - エラートレース: 100% 保持
  - 通常トラフィック: 10% サンプリング
  - ヘルスチェック等: 除外

メトリクス精度の維持:
  - サンプリング前にメトリクスを生成
  - spanmetrics processor で RED メトリクス自動生成
  processors:
    spanmetrics:
      metrics_exporter: prometheus
      dimensions:
        - name: service.name
        - name: http.method
        - name: http.status_code
```

---

## 5. テレメトリ相関（三本柱の統合）

```
Log-Trace 相関:
  - ログに trace_id / span_id を自動注入
  - 構造化ログ（JSON）で統一
  - ログレベル: ERROR/WARN は必ずスパンイベントとしても記録

Trace → Metrics 変換:
  - spanmetrics processor で RED メトリクス自動生成
  - servicegraph processor で依存関係マップ自動生成

コンテキスト伝播:
  - W3C Trace Context 標準（デフォルト推奨）
  - Baggage で横断コンテキスト伝播（customer_id 等）
  - 注意: Baggage は全下流サービスに伝播→機密情報を含めない

パフォーマンス最適化:
  - BatchSpanProcessor 設定:
    maxQueueSize: 2048        # メモリ制限
    maxExportBatchSize: 512   # バッチサイズ
    scheduledDelayMillis: 5000 # 送信間隔
    exportTimeoutMillis: 30000 # タイムアウト
  - gzip 圧縮の有効化（帯域削減）
  - サーキットブレーカー（テレメトリが可用性に影響しない）
```

---

## 6. Beacon との連携

```
Beacon での活用:
  1. DESIGN モードで OTel 計装戦略の設計
  2. SPECIFY モードで Collector パイプライン仕様の策定
  3. MEASURE モードでサンプリング戦略の最適化
  4. 定期レビューで Semantic Conventions 準拠チェック

品質ゲート:
  - OTel SDK 初期化がアプリ起動最初にあるか（OT-02）
  - memory_limiter processor が pipeline 最初に配置されているか
  - エラートレースが 100% 保持されているか
  - ログに trace_id が注入されているか（相関可能か）
  - PII/PHI フィルタリングが Collector で実施されているか
  - Semantic Conventions に準拠した属性命名か
```

**Source:** [Better Stack: OpenTelemetry Best Practices](https://betterstack.com/community/guides/observability/opentelemetry-best-practices/) · [OpenTelemetry: Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/) · [Dash0: OpenTelemetry Collector Guide](https://dash0.com/blog/opentelemetry-collector-guide)
