# Feature Flag Pitfalls & Lifecycle Management

> フラグ技術的負債、ライフサイクル管理の落とし穴、クリーンアップ戦略、Uber 事例

## 1. Feature Flag 8 大アンチパターン

| # | アンチパターン | 問題 | 対策 |
|---|-------------|------|------|
| **FF-01** | **Stale Flag（陳腐化フラグ）** | 目的完了後もコードに残留 → デッドブランチの蓄積・認知負荷増大 | 有効期限を作成時に設定 · 定期クリーンアップ Sprint |
| **FF-02** | **Orphaned Flag（孤児フラグ）** | オーナー不在（退職・チーム再編）→ 誰も削除判断できない | フラグ作成時にオーナー必須 · チーム移管プロセス |
| **FF-03** | **Nested Flag（入れ子フラグ）** | フラグ内にフラグ → テストパス指数爆発（2^n） | 最大ネスト深度 1 · フラグ間の依存関係を禁止 |
| **FF-04** | **命名規則の不統一** | `newFeatureToggle` のような汎用名 → 目的不明 | プレフィックス規則（`exp_`, `temp_`, `ops_`, `perm_`） |
| **FF-05** | **ビジネスロジック制御** | コアロジックをフラグで分岐 → フラグ削除時に本番障害リスク | フラグは公開制御のみ · ロジック分岐は entitlement/backend で |
| **FF-06** | **テスト網羅性の欠如** | フラグ ON/OFF 両方のテストがない → 片方のパスにバグ潜在 | フラグごとに ON/OFF 両パスのテストを必須化 |
| **FF-07** | **フラグ過多** | アクティブフラグが 50 個超 → 組み合わせ爆発・デバッグ困難 | アクティブフラグ上限設定 · 古いフラグの強制削除 |
| **FF-08** | **フォールバック未設定** | フラグサービス障害時のデフォルト動作未定義 → 予測不能な挙動 | フラグごとにフォールバック値を必須設定 |

---

## 2. フラグ技術的負債の影響

### 4 つの影響領域

```
1. パフォーマンス劣化
   - Stale フラグが処理能力・メモリを消費
   - フラグ評価のオーバーヘッドが蓄積
   - 大規模コードベースでユーザー体感速度に影響

2. 開発者の生産性低下
   - フラグ関連のコンテキストスイッチ増加
   - デバッグ時に古いフラグのパスを調査する時間浪費
   - 新メンバーのオンボーディング障壁

3. テスト複雑性の爆発
   - n個のフラグ → 最大 2^n のテストパス
   - Nested フラグで組み合わせがさらに増加
   - テストスイートの実行時間・メンテナンスコスト増大

4. 予期せぬ動作
   - 忘れられたフラグが意図せず機能やデータを露出
   - フラグ間の暗黙的依存で想定外の挙動
   - セキュリティリスク（非公開機能の意図しない公開）
```

### Uber の事例

```
事例: Uber はモバイルアプリから約 2,000 個の Stale フラグを削除
  - 手法: Piranha（OSS 静的解析ツール）で AST ベースの自動検出・削除
  - 結果: 手動作業を最小化しつつ大規模クリーンアップを達成
  - 教訓: 自動化なしでは人間のフラグクリーンアップは追いつかない
```

---

## 3. フラグライフサイクル管理

### 5 フェーズモデル

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ CREATE   │──▶│ ROLLOUT  │──▶│ STABLE   │──▶│ CLEANUP  │──▶│ REMOVED  │
│ 作成     │   │ 展開     │   │ 安定     │   │ 削除準備 │   │ 削除完了 │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
  Day 0         Day 1-14       Day 14-30      Day 30-60      Day 60+

各フェーズの必須項目:
  CREATE:  オーナー、目的、タイプ、有効期限、フォールバック値、削除チケット
  ROLLOUT: 段階（5%→25%→50%→100%）、成功基準、ロールバック条件
  STABLE:  100% 到達確認、副作用なし確認、メトリクス安定
  CLEANUP: フラグ分岐のコード削除 PR 作成、テスト更新
  REMOVED: コードから完全削除、フラグ管理サービスからも削除
```

### フラグタイプ別ライフサイクル

| タイプ | 推奨寿命 | 自動アラート | 強制削除 |
|-------|---------|------------|---------|
| **Release Flag** (temp_) | 7-30 日 | 14 日で警告 | 60 日 |
| **Experiment Flag** (exp_) | 14-60 日 | 30 日で警告 | 90 日 |
| **Ops Flag** (ops_) | 永続可 | 90 日で再確認 | なし |
| **Permission Flag** (perm_) | 永続可 | 180 日で再確認 | なし |

---

## 4. フラグクリーンアップ戦略

### 検出手法

| 手法 | ツール例 | 精度 | コスト |
|------|---------|------|-------|
| **手動監査** | スプレッドシート · チームレビュー | 低 | 高 |
| **静的解析** | Piranha (Uber) · ESLint ルール · Tree-sitter | 高 | 中 |
| **使用メトリクス** | LaunchDarkly · Split.io · Statsig | 高 | 低 |
| **CI/CD 統合** | ビルド時の Age チェック · 期限超過でビルド失敗 | 中 | 低 |

### クリーンアップのベストプラクティス

```
プロセスへの組み込み:
  □ フラグ作成時に削除チケットを同時作成
  □ Definition of Done にフラグ削除を含める
  □ Sprint ごとにフラグ棚卸し（5 分）
  □ 四半期ごとの大規模クリーンアップ Sprint

命名規則:
  temp_checkout_v2      → Release Flag（一時的）
  exp_pricing_model_b   → Experiment Flag（実験）
  ops_circuit_breaker   → Ops Flag（運用）
  perm_beta_access      → Permission Flag（永続）

自動化:
  - Age ベースのアラート（作成から N 日で通知）
  - 未評価フラグの検出（30 日間評価なし → 候補）
  - ダッシュボードでフラグ総数・Age 分布を可視化
```

---

## 5. Launch との連携

```
Launch での活用:
  1. Feature Flag 戦略設計時に FF-01〜08 のチェックを適用
  2. フラグ作成時に 5 フェーズモデルの必須項目を強制
  3. Rollout 計画に成功基準とロールバック条件を必ず含める
  4. リリース完了後にフラグクリーンアップタイムラインを提示

品質ゲート:
  - フラグにオーナー未設定 → 作成ブロック（FF-02 防止）
  - フォールバック値未設定 → 作成ブロック（FF-08 防止）
  - ネスト深度 > 1 → 警告（FF-03 防止）
  - アクティブフラグ > 50 → 新規フラグ作成に承認要求（FF-07 防止）
  - Age > 60 日の Release Flag → 強制クリーンアップ要求（FF-01 防止）
```

**Source:** [FlagShark: Feature Flag Technical Debt Guide](https://flagshark.com/blog/feature-flag-technical-debt-guide/) · [LaunchDarkly: 3 Ways to Avoid Technical Debt](https://launchdarkly.com/blog/3-ways-to-avoid-technical-debt-when-feature-flagging/) · [Statsig: Feature Flag Debt Management](https://www.statsig.com/perspectives/feature-flag-debt-management) · [Unleash: Feature Flag Best Practices at Scale](https://docs.getunleash.io/topics/feature-flags/best-practices-using-feature-flags-at-scale) · [Acid Tango: The Case Against Feature Flags](https://acidtango.com/thelemoncrunch/the-case-against-feature-flags-when-toggles-become-technical-debt/)
