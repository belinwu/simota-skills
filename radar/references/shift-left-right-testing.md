# Shift-Left/Shift-Right & Production Testing

> 開発ライフサイクル全体でのテスト戦略、可観測性駆動テスト、カオステスト、QAOps

## 1. Shift-Left テスティング

### 定義

テスト活動を開発ライフサイクルの「左側」（早期段階）に移動し、バグの早期発見・修正コスト削減を実現するアプローチ。

### Shift-Left 成熟度モデル

| レベル | 段階 | テスト活動 | コスト |
|--------|------|----------|--------|
| L0 | コーディング後 | 手動テスト | ×100 |
| L1 | コーディング中 | ユニットテスト（TDD） | ×10 |
| L2 | 設計中 | 仕様からのテスト生成 | ×1 |
| L3 | 要件定義中 | BDD/ATDD、受入基準テスト | ×0.1 |

### Shift-Left プラクティス

| プラクティス | タイミング | 効果 |
|------------|----------|------|
| **Static Analysis** | コミット前 | 構文・型・セキュリティの即時検出 |
| **Pre-commit hooks** | コミット時 | リンター・フォーマッター自動実行 |
| **TDD** | コーディング中 | 設計品質 + テストカバレッジ同時獲得 |
| **BDD** | 要件定義時 | ビジネス要件とテストの直結 |
| **Contract-First** | API設計時 | インターフェース互換性の早期保証 |
| **Threat Modeling** | 設計時 | セキュリティリスクの早期特定 |

---

## 2. Shift-Right テスティング

### 定義

テスト活動を開発ライフサイクルの「右側」（本番環境）に拡張し、実際のユーザー行動・負荷・環境での品質を検証するアプローチ。

### Shift-Right テスト種別

| テスト種別 | 目的 | リスク | ツール例 |
|-----------|------|--------|---------|
| **カナリアリリース** | 段階的デプロイで影響確認 | 低 | Argo Rollouts, Flagger |
| **Feature Flags** | 特定ユーザーに限定公開 | 低 | LaunchDarkly, Unleash |
| **A/B テスト** | ユーザー行動の統計的比較 | 低 | Optimizely, GrowthBook |
| **Synthetic Monitoring** | 合成トラフィックで常時監視 | 低 | Datadog, New Relic |
| **Chaos Testing** | 意図的な障害注入 | 中-高 | Chaos Monkey, Litmus |
| **Traffic Mirroring** | 本番トラフィックのコピーでテスト | 中 | Istio, Envoy |

---

## 3. 可観測性駆動テスト（Observability-Driven Testing）

### 概念

テストの設計と優先付けを、本番環境の可観測性データ（メトリクス、ログ、トレース）に基づいて行うアプローチ。

### 3本柱との統合

```
Metrics（メトリクス）
  → エラーレート上昇 → 回帰テスト追加
  → レイテンシ劣化 → パフォーマンステスト追加

Logs（ログ）
  → 未処理例外パターン → エッジケーステスト追加
  → ユーザーエラー頻度 → バリデーションテスト強化

Traces（トレース）
  → 高頻度パス → 優先テストカバレッジ
  → 障害伝播パターン → 統合テスト追加
```

### テスト優先度への反映

| 可観測性シグナル | テストアクション | 優先度 |
|----------------|----------------|--------|
| エラーレート急増 | 回帰テスト即時追加 | P0 |
| SLO バジェット消費 > 50% | 関連パスのテスト強化 | P1 |
| 新規エラーパターン検出 | エッジケーステスト追加 | P1 |
| レイテンシ P99 悪化 | パフォーマンステスト追加 | P2 |
| 低頻度パスの障害 | ロングテールテスト追加 | P3 |

---

## 4. カオステスティング

### カオスエンジニアリング原則

```
1. 定常状態の仮説を立てる
2. 現実世界のイベントを変数化する
3. 本番環境で実験する（安全に）
4. 自動化して継続的に実行する
5. 影響範囲を最小化する（ブラストラディウス制御）
```

### カオス実験テンプレート

```markdown
## Chaos Experiment

### 仮説
[定常状態の定義: 例「API レスポンスタイム P95 < 200ms」]

### 変数（注入する障害）
- [ ] ネットワーク遅延（100ms-500ms）
- [ ] サービス停止（依存サービス A）
- [ ] CPU 高負荷（80%+）
- [ ] ディスク枯渇（90%+）
- [ ] DNS 障害

### ブラストラディウス
- 対象: [特定のサービス/Pod/リージョン]
- 影響ユーザー: [%]
- ロールバック: [自動/手動、タイムアウト]

### 結果
- 定常状態維持: [Yes/No]
- 検出されたレジリエンスギャップ: [...]
- 改善アクション: [...]
```

### ツール比較

| ツール | 対象 | 特徴 |
|--------|------|------|
| **Chaos Monkey** | VM/インスタンス | Netflix発、ランダムインスタンス終了 |
| **Litmus** | Kubernetes | CNCF、宣言的カオス実験 |
| **Gremlin** | マルチプラットフォーム | SaaS、安全な実験管理 |
| **Toxiproxy** | ネットワーク | プロキシベースの障害注入 |
| **Chaos Toolkit** | 汎用 | 拡張可能なフレームワーク |

---

## 5. QAOps

### 定義

QA プラクティスと DevOps パイプラインを統合し、品質を継続的デリバリーの一部として組み込むアプローチ。

### QAOps パイプライン設計

```
コミット → ビルド → テスト（段階的ゲート） → デプロイ → 監視
                      │
              ┌───────┼───────┐
              │       │       │
           Gate 1  Gate 2  Gate 3
           Static  Unit+   E2E+
           Analysis Integration Performance
           < 1min  < 5min  < 15min
```

### テストゲート設計

| ゲート | 含むテスト | 制限時間 | 失敗時 |
|--------|----------|---------|--------|
| **Gate 1: Fast** | Lint, Type check, Unit | < 2min | PR ブロック |
| **Gate 2: Standard** | Integration, Contract | < 10min | マージブロック |
| **Gate 3: Full** | E2E, Performance, Security | < 30min | デプロイブロック |
| **Gate 4: Production** | Smoke, Synthetic, Canary | 継続 | ロールバック |

---

## 6. Synthetic Monitoring（合成監視）

### 定義

スクリプト化されたユーザーシナリオを定期的に自動実行し、本番環境の可用性とパフォーマンスを常時監視する手法。

### テストシナリオ設計

| シナリオ種別 | 頻度 | 例 |
|------------|------|-----|
| **ヘルスチェック** | 1分 | API エンドポイント応答確認 |
| **クリティカルパス** | 5分 | ログイン→主要機能→ログアウト |
| **トランザクション** | 15分 | 決済フロー全体の検証 |
| **グローバル** | 30分 | 複数リージョンからのアクセス |

### E2E テストとの差異

| 観点 | E2E テスト | Synthetic Monitoring |
|------|----------|---------------------|
| 実行タイミング | CI/CD パイプライン内 | 本番環境で継続的 |
| 目的 | リリース前の品質保証 | リリース後の可用性監視 |
| 失敗時アクション | デプロイ停止 | アラート→インシデント対応 |
| 環境 | ステージング/テスト | 本番 |
| 頻度 | デプロイごと | 定期的（分〜時間） |

---

## 7. Radar との統合

### Shift-Left/Right の適用マップ

| Radar モード | Shift-Left 適用 | Shift-Right 適用 |
|-------------|----------------|-----------------|
| Default | エッジケーステスト早期追加 | 本番エラーパターンからのテスト逆生成 |
| FLAKY | 非決定的テストの早期検出 | 本番フレーキーの可観測性分析 |
| AUDIT | カバレッジギャップの設計段階検出 | 本番パスカバレッジとの差分分析 |
| SELECT | 変更影響のテスト自動選択 | 本番障害パターンに基づくテスト優先度 |

**Source:** [SmartBear: Shift-Left Testing](https://smartbear.com/learn/automated-testing/shift-left-testing/) · [Netflix: Chaos Engineering](https://netflixtechblog.com/tagged/chaos-engineering) · [Gremlin: Chaos Engineering Guide](https://www.gremlin.com/community/tutorials/chaos-engineering-the-history-principles-and-practice/) · [Datadog: Synthetic Monitoring](https://www.datadoghq.com/product/synthetic-monitoring/) · [Testlio: QAOps](https://testlio.com/blog/software-testing-trends/)
