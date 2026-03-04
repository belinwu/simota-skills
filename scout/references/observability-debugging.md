# Observability-Driven Debugging

> OpenTelemetry 統合、分散トレーシング、構造化ログ、継続的プロファイリング、本番デバッグ

## 1. Observability の4シグナル

| シグナル | 役割 | ツール例 |
|---------|------|---------|
| **メトリクス** | リソースの時系列データ、異常検出 | Prometheus, Grafana |
| **トレース** | リクエストの分散パス追跡 | Jaeger, Tempo, Zipkin |
| **ログ** | 個別イベントの詳細記録 | Loki, Elasticsearch |
| **プロファイル** | CPU/メモリの関数レベル分析 | Pyroscope, pprof |

### シグナル間の相関

```
メトリクス: エラーレート↑を検出
  → トレース: 障害サービスとスパンを特定
    → ログ: trace_id で具体的エラーを確認
      → プロファイル: ホットスポットの関数を特定
```

**鍵**: `trace_id` と `span_id` をすべてのシグナルに含めることで相関が可能になる。

---

## 2. 分散トレーシング

### 基本概念

| 用語 | 説明 |
|------|------|
| Trace | 1つのリクエストの全サービス横断パス |
| Span | 個別の操作単位（関数呼び出し、DB クエリ等） |
| Trace ID | リクエスト全体の一意識別子 |
| Span ID | 個別操作の一意識別子 |
| Parent Span ID | 親操作への参照 |
| Baggage | サービス境界を越えて伝搬するメタデータ |

### W3C Trace Context

```
traceparent: 00-{trace-id}-{span-id}-{flags}
```

**重要**: 下流サービスが新しいトレースを開始してはならない（`traceparent` ヘッダーを伝搬する）。

### 相関 ID パターン

分散システムに入るすべてのリクエストにランダム生成された識別子を付与。リクエストがシステム内を移動する際の接続スレッドとして機能。

### Scout での活用

- TRACE フェーズでトレースデータを活用し、障害箇所を特定
- 「共通祖先」分析: エラートレースの50%以上に出現するオペレーションを優先調査
- サービス間の依存関係マップから影響範囲を評価

---

## 3. 構造化ログ

### 必須フィールド

```json
{
  "timestamp": "2026-03-04T10:15:30.123Z",
  "level": "ERROR",
  "service": "payment-service",
  "trace_id": "abc123def456",
  "span_id": "789ghi",
  "message": "Payment processing failed",
  "error_code": "PAYMENT_TIMEOUT",
  "user_id": "u-12345",
  "duration_ms": 5032
}
```

### ログレベルの使い分け

| レベル | 用途 | 本番での扱い |
|--------|------|------------|
| ERROR | エラー・障害 | 常時有効、アラート対象 |
| WARN | 潜在的問題 | 常時有効 |
| INFO | 通常操作の記録 | 常時有効 |
| DEBUG | 詳細デバッグ情報 | 通常無効、フラグで有効化 |

### 本番ログのベストプラクティス

- JSON 形式で機械解析可能に
- **機密データを絶対にログに含めない**（トークン、パスワード、秘密鍵、個人情報）
- イベントベースサンプリング: エラー=100%保持、ルーチン=10%サンプリング
- OTel コレクターで機密フィールドの自動マスキング

---

## 4. 継続的プロファイリング

### ツールと手法

| ツール | 対応言語 | オーバーヘッド | 特徴 |
|--------|---------|------------|------|
| Pyroscope | Go, Python, Ruby, Java, .NET, Rust | 2-5% | Grafana 統合 |
| pprof | Go | ~1% | 標準ライブラリ |
| async-profiler | Java | ~2% | JFR 互換 |
| eBPF エージェント | 全言語 | ~1% | コード変更不要 |

### フレイムグラフ

スタックトレースの可視化。最も頻繁なコードパスを迅速に特定。

**読み方:**
- **幅** = 関数がサンプルに占める割合（広い = CPU 消費大）
- **深さ** = コールスタックの深さ
- **差分フレイムグラフ** = 2つのフレイムグラフの比較でリグレッション箇所を特定

### メモリリーク検出

| 手法 | ツール | 用途 |
|------|--------|------|
| 3スナップショット法 | Chrome DevTools | ブラウザ JS |
| MemLab | Facebook MemLab | React アプリ |
| Valgrind | Valgrind | C/C++ |
| tracemalloc | Python 標準 | Python |
| ヒープダンプ比較 | JVisualVM, MAT | Java |

**よくある JS メモリリークパターン:**
- 解放されないタイマー/インターバル
- デタッチされた DOM ノード参照
- クロージャに保持された参照
- 未クリーンアップのイベントリスナー

---

## 5. 本番環境の安全なデバッグ

### シャドートラフィック

本番リクエストを新バージョンに複製。レスポンスはユーザーに影響しない。

**必須要件**: シャドーパスからの書き込みと外部呼び出しが本番状態に影響しないこと。

### カナリア分析

1-5%のユーザーに新バージョンをリリースし、メトリクスを監視:
- エラーレート
- レスポンスタイム
- CPU/メモリ使用量
- 変更固有のメトリクス

### Feature Flag によるデバッグ

```
通常時: INFO ログレベル
デバッグ時: 特定サービス/リクエストに対してのみ DEBUG を有効化（Feature Flag 制御）
```

**利点**: デプロイなしで即座にデバッグ情報を取得・無効化可能。

---

## 6. Scout への統合ポイント

| Scout フェーズ | Observability 活用 |
|-------------|------------------|
| RECEIVE | アラート・メトリクス異常から症状を定量化 |
| REPRODUCE | トレースデータで障害パスを特定、ログで詳細を確認 |
| TRACE | 分散トレースでサービス間の因果関係を追跡 |
| LOCATE | プロファイリングデータで関数レベルの原因を特定 |
| ASSESS | メトリクスで影響範囲を定量的に評価 |
| REPORT | Observability データへのリンクをレポートに含める |

**Source:** [OpenTelemetry RCA - OneUpTime](https://oneuptime.com/blog/post/2026-02-06-root-cause-analysis-opentelemetry/view) · [OpenTelemetry Docs](https://opentelemetry.io/docs/concepts/) · [Distributed Tracing - Apica](https://www.apica.io/blog/what-is-distributed-tracing-how-it-works-and-best-practices/) · [Flame Graphs - Brendan Gregg](https://www.brendangregg.com/flamegraphs.html) · [Pyroscope - Grafana](https://grafana.com/docs/pyroscope/latest/) · [Shadow Traffic Patterns 2025](https://debugg.ai/resources/from-staging-to-shadow-traffic-production-replay-patterns-2025) · [Structured Logging - OneUpTime](https://oneuptime.com/blog/post/2026-01-25-structured-logging-best-practices/view)
