# Security Pipeline Integration Pitfalls

> CI/CD セキュリティパイプラインの落とし穴、DAST 統合アンチパターン、Shift-Left の課題

## 1. セキュリティパイプライン 8 大アンチパターン

| # | アンチパターン | 問題 | 対策 |
|---|-------------|------|------|
| **SP-01** | **セキュリティシアター** | ツール導入のみで運用なし → 検出結果を誰も見ない · 形式的なチェック | アクション可能なアラートのみ通知 · オーナーシップの明確化 |
| **SP-02** | **パイプラインブロッカー化** | フルスキャンが長時間 → 開発速度の低下 · スキャンのスキップ横行 | 軽量スキャン + 夜間フルスキャン · スキャンスコープの最適化 |
| **SP-03** | **アラート洪水** | 全検出結果を通知 → アラート疲労 · 本物の脆弱性を見逃し | 重要度ベースゲーティング · 偽陽性フィルタリング |
| **SP-04** | **サイロ化セキュリティ** | セキュリティチームのみが結果を見る → 開発者との断絶 · 修正遅延 | 開発者ワークフローへの統合 · PR コメント · IDE 統合 |
| **SP-05** | **ツール過多** | SAST + DAST + SCA + IAST を全ステージで実行 → 重複検出 · 矛盾する結果 | ツール間の相関分析 · ステージに応じた適切なツール選択 |
| **SP-06** | **本番スキャン依存** | 本番環境のみでテスト → 修正コストが最大化 | Shift-Left: 開発・ステージング環境での早期テスト |
| **SP-07** | **静的ゲート基準** | 「Critical = ブロック」の固定ルール → コンテキスト無視 · 不要なブロック | リスクベースのゲーティング · 資産価値 + 悪用可能性の複合評価 |
| **SP-08** | **監視なきパイプライン** | パイプラインの健全性を監視しない → スキャン失敗の見逃し · 技術的負債の蓄積 | スキャン完了率 · 偽陽性率 · MTTR の追跡 |

---

## 2. DAST の CI/CD 配置戦略

### ステージ別スキャン配置

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│   COMMIT     │   │    BUILD     │   │   STAGING    │   │  PRODUCTION  │
│              │   │              │   │              │   │              │
│  SAST        │   │  SCA         │   │  DAST Full   │   │  Passive     │
│  Secret Scan │   │  Container   │   │  API Scan    │   │  Monitoring  │
│  Lint        │   │  Scan        │   │  Auth Test   │   │  WAF Logs    │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
   < 5 min           < 10 min          30-60 min         Continuous
```

### 推奨配置パターン

| ステージ | テスト種類 | トリガー | 時間制限 | ブロック基準 |
|---------|----------|---------|---------|------------|
| **PR/Commit** | SAST · Secret Scan · Lint | Push/PR | < 5 分 | Critical SAST |
| **Build** | SCA · Container Scan | Build 完了 | < 10 分 | Known CVE (Critical) |
| **Deploy to Staging** | 軽量 DAST · API テスト | Deploy 完了 | < 15 分 | Critical/High |
| **Staging (Scheduled)** | フル DAST · 認証テスト | 夜間/週次 | 60 分+ | なし（通知のみ） |
| **Production** | パッシブモニタリング | 継続 | N/A | なし（アラート） |

---

## 3. Shift-Left の落とし穴

### Shift-Left の 5 つの誤解

```
誤解 1: "全てを左にシフトすれば良い"
  現実: DAST は稼働中のアプリが必要 → コミット時点では実行不能
  対策: テスト種類に応じた適切なステージ配置

誤解 2: "自動化すれば人間は不要"
  現実: ビジネスロジック脆弱性 · 認可テストは自動化困難
  対策: 自動テストで基本カバレッジ + 定期的な手動テスト

誤解 3: "開発者がセキュリティを担当すべき"
  現実: 開発者のセキュリティ知識は限定的 · 本業を圧迫
  対策: セキュリティチャンピオンプログラム · ガイダンス付きツール

誤解 4: "ツールを増やせばカバレッジが上がる"
  現実: ツール過多 → 重複・矛盾 · 管理コスト増大
  対策: ツール間の相関分析 · 各ステージに最適なツール 1-2 個

誤解 5: "シフトレフトすればリリース後のテストは不要"
  現実: 設定ミス · 環境依存の問題はリリース後にしか検出できない
  対策: 左右両方でテスト（Shift-Left + Shift-Right）
```

### 開発者フレンドリーな統合

```
原則:
  1. 開発者のワークフローに合わせる（ツールに合わせない）
  2. アクション可能な結果のみ通知（ノイズ排除）
  3. 修正ガイダンスを含める（問題だけでなく解決策）
  4. 既存ツールチェーンに統合（Jira, GitHub, Slack）

実装:
  □ PR にセキュリティ検出結果をインラインコメント
  □ IDE プラグインでリアルタイムフィードバック
  □ 修正テンプレートの自動生成
  □ セキュリティトレーニングへのリンク
  □ 偽陽性マークのワンクリック対応
```

---

## 4. セキュリティゲート設計

### リスクベースゲーティング

```
従来: severity == "Critical" → BLOCK
問題: コンテキスト無視 · 偽陽性によるブロック · 開発者の信頼低下

推奨: リスクスコア = f(severity, exploitability, asset_value, context)

リスクスコア計算:
  Base: CVSS Score (0-10)
  × Exploitability Factor:
    - Proof-Based Confirmed: 1.5x
    - DAST + SAST 両方検出: 1.3x
    - DAST のみ: 1.0x
    - SAST のみ: 0.7x
  × Asset Value:
    - Payment/Auth: 1.5x
    - User Data: 1.3x
    - Public Content: 0.8x

  結果:
    Score > 12: BLOCK（即時修正必須）
    Score 8-12: WARN（次スプリントで修正）
    Score < 8: INFO（バックログ追加）
```

### ゲート基準テンプレート

| 環境 | Critical | High | Medium | Low |
|------|----------|------|--------|-----|
| **PR Gate** | Block | Warn | Info | - |
| **Staging Gate** | Block | Block (confirmed) | Warn | - |
| **Release Gate** | Block | Block | Warn | Info |

---

## 5. KPI とメトリクス

### セキュリティパイプライン健全性指標

| KPI | 目標値 | 計測方法 |
|-----|-------|---------|
| **スキャン完了率** | > 95% | 成功スキャン / 全スキャン |
| **偽陽性率** | < 20% | FP / 全検出結果 |
| **MTTR（修正時間）** | Critical < 24h, High < 7d | 検出から修正マージまで |
| **スキャン時間** | PR < 15 分, Full < 60 分 | パイプライン実行時間 |
| **脆弱性再発率** | < 10% | 修正後に再検出された脆弱性 |
| **セキュリティ負債** | 減少トレンド | 未修正の検出結果総数 |

### ダッシュボード推奨項目

```
1. 脆弱性トレンド（週次）: 新規 / 修正済み / 残存
2. MTTR 推移: Critical / High / Medium / Low 別
3. 偽陽性率推移: ツール別 · ルール別
4. スキャンカバレッジ: スキャン済みリポジトリ / 全リポジトリ
5. Top 5 脆弱性カテゴリ: 頻出パターンの特定
```

---

## 6. Probe との連携

```
Probe での活用:
  1. SARIF 統合設計時に SP-01〜08 のチェックを適用
  2. DAST 配置戦略でステージ別のスキャン計画を策定
  3. リスクベースゲーティングでセキュリティゲートを設計
  4. KPI 設計で Harvest への指標提供

品質ゲート:
  - DAST がパイプラインに未統合 → 推奨提案
  - スキャン時間 > 30 分（PR ゲート）→ スコープ最適化を提案（SP-02 防止）
  - 偽陽性率 > 30% → ルールチューニングを要求（SP-03 防止）
  - スキャン完了率 < 90% → パイプライン健全性チェック（SP-08 防止）
  - セキュリティ結果が開発者に通知されていない → 統合提案（SP-04 防止）
```

**Source:** [Snyk: DAST in CI/CD Pipelines](https://snyk.io/articles/dast-ci-cd-pipelines/) · [Invicti: DAST-First DevSecOps Integration](https://www.invicti.com/blog/web-security/dast-first-devsecops-integration) · [Wiz: CI/CD Security Scanning](https://www.wiz.io/academy/application-security/ci-cd-security-scanning) · [DevOps.com: Shift Left With DAST](https://devops.com/shift-left-with-dast-dynamic-testing-in-the-ci-cd-pipeline/) · [Checkmarx: Integrating DAST and SAST into DevSecOps](https://checkmarx.com/learn/integrating-dast-and-sast-into-devsecops-for-continuous-api-security/)
