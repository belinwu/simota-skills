# Load Testing Anti-Patterns

> 負荷テストの 10 大アンチパターン、Shift-Left パフォーマンス戦略、パフォーマンスバジェット

## 1. 負荷テスト 10 大アンチパターン

### テスト設計のアンチパターン

| # | アンチパターン | 症状 | 対策 |
|---|-------------|------|------|
| **AP-01** | **Happy Path Only** | 正常系のみテスト、エラーパス未検証 | エラーシナリオ（4xx/5xx/timeout）を 20-30% 混入 |
| **AP-02** | **Unrealistic Data** | テストデータが本番と乖離 | 本番データのサニタイズ版を使用、データ分布を再現 |
| **AP-03** | **Single Endpoint Focus** | 1 API のみ負荷をかける | ユーザージャーニー全体をシナリオ化（Browse→Search→Buy） |
| **AP-04** | **Missing Think Time** | ユーザーの待機時間なし（非現実的な高負荷） | `sleep(1-3s)` でリアルなペーシング |
| **AP-05** | **Flat Load Profile** | 一定負荷のみ、ランプアップ/スパイクなし | Step ramp + Spike + Soak を組み合わせ |

### インフラ・環境のアンチパターン

| # | アンチパターン | 症状 | 対策 |
|---|-------------|------|------|
| **AP-06** | **Testing in Isolation** | ステージングが本番と異なるスペック | 本番同等環境 or スケール比率を明示して補正 |
| **AP-07** | **Shared Test Environment** | 他チームの負荷が結果に干渉 | 専用環境 or 時間帯分離、ベースライン比較 |
| **AP-08** | **No Warmup Phase** | JIT/キャッシュ未準備で測定開始 | 5-10 分のウォームアップ後に計測開始 |

### 分析・報告のアンチパターン

| # | アンチパターン | 症状 | 対策 |
|---|-------------|------|------|
| **AP-09** | **Average-Only Metrics** | 平均値のみ報告、外れ値を無視 | p50/p95/p99/max を必ず報告、ヒストグラム分析 |
| **AP-10** | **One-Shot Testing** | 1 回実行して完了、再現性未確認 | 最低 3 回実行、統計的有意性を確認 |

---

## 2. Azure 10 大パフォーマンスアンチパターン

Microsoft Azure Architecture Center が定義する本番で頻出するスケーラビリティ問題:

| アンチパターン | 説明 | 検出方法 |
|-------------|------|---------|
| **Busy Database** | データストアに過剰な処理をオフロード | DB CPU/クエリ時間の監視 |
| **Busy Front End** | リソース集約タスクをフロントエンドで実行 | ブラウザ CPU/メインスレッド占有率 |
| **Chatty I/O** | 多数の小さなネットワークリクエスト | リクエスト数/レイテンシ相関 |
| **Extraneous Fetching** | 必要以上のデータ取得 | レスポンスサイズ/使用率の比較 |
| **Improper Instantiation** | 共有すべきオブジェクトの繰り返し生成 | GC 頻度/メモリプロファイル |
| **Monolithic Persistence** | 異なるアクセスパターンに単一データストア | 読み取り/書き込みパターン分析 |
| **No Caching** | キャッシュの不活用 | 同一クエリの繰り返し実行検出 |
| **Noisy Neighbor** | マルチテナントでのリソース不公平消費 | テナント別リソース使用量 |
| **Retry Storm** | 失敗リクエストの過剰リトライ | リトライ率/バックエンド負荷急増 |
| **Synchronous I/O** | I/O 完了までスレッドをブロック | スレッドプール枯渇/レイテンシ増加 |

---

## 3. Shift-Left パフォーマンス戦略

### パフォーマンスエンジニアリングの統合ポイント

```
開発フェーズ別のパフォーマンス活動:

設計段階:
  - パフォーマンスバジェットの定義（レスポンス/スループット/リソース上限）
  - キャパシティモデリング（予想ユーザー数 × 操作頻度 × リソース消費）
  - アーキテクチャレビュー（上記 10 アンチパターンのチェック）

開発段階:
  - コンポーネント単位のマイクロベンチマーク
  - N+1 クエリ/Chatty I/O の早期検出（ORM 設定レビュー）
  - 開発環境での Soak テスト（メモリリーク早期発見）

CI/CD 段階:
  - PR ごとのパフォーマンス回帰テスト（変更ファイル関連 API のみ）
  - 閾値ベースの自動ゲート（p95 > 500ms で PR ブロック）
  - 夜間の フル負荷テスト

リリース前:
  - ステージングでの本番シナリオ再現
  - SLO 検証テスト（99.9% 可用性の確認）
  - カナリアデプロイ + パフォーマンス比較
```

### パフォーマンスバジェット

| リソース | バジェット例 | 測定方法 |
|---------|------------|---------|
| **API レスポンスタイム** | p95 < 200ms, p99 < 500ms | k6 thresholds |
| **ページロード** | LCP < 2.5s, FID < 100ms | Lighthouse CI |
| **バンドルサイズ** | JS < 200KB gzip | bundlesize / size-limit |
| **DB クエリ** | 単一リクエストで ≤ 5 クエリ | ORM query counter |
| **メモリ使用量** | ≤ 512MB / pod | Prometheus + alerts |

---

## 4. Siege との連携

```
Siege の LOAD モードでの活用:
  1. テスト設計時に AP-01〜10 のチェックリストを適用
  2. Azure 10 アンチパターンをスキャン候補に含める
  3. Shift-Left 戦略に沿った CI/CD 統合を推奨
  4. パフォーマンスバジェット超過を自動検出

Bolt へのハンドオフ:
  - 検出されたアンチパターン → Bolt が最適化実装
  - パフォーマンスバジェット超過 → Bolt が改善提案
```

**Source:** [Azure Performance Antipatterns](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/) · [LoadView: Load Testing Strategy 2025](https://www.loadview-testing.com/blog/plan-load-testing-strategy-2025/) · [Full Scale: Performance Testing Guide 2025](https://fullscale.io/blog/performance-testing/) · [Codepipes: Software Testing Antipatterns](https://blog.codepipes.com/testing/software-testing-antipatterns.html)
