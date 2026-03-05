# Strategic Planning Anti-Patterns

> 戦略策定・実行における失敗パターン、実行ギャップ、組織アラインメント課題

## 1. 戦略策定 10 大アンチパターン

| # | アンチパターン | 症状 | 対策 |
|---|-------------|------|------|
| **SP-01** | **Static Planning** | 年1回策定して放置 → 市場変化に追従不能 | 四半期ローリング + ドリフト検出 |
| **SP-02** | **Overambition** | 同時に5+優先事項 → リソース分散（30%効果減） | 3つ以内に絞る · 優先順位の明確化 |
| **SP-03** | **Data Ignorance** | 直感・経験ベースで市場データ無視 | データ駆動意思決定 · 三角測量 |
| **SP-04** | **Market Blindness** | 市場調査を軽視 → 存在しないセグメントへ投資 | 競合分析 · 顧客インタビュー必須化 |
| **SP-05** | **Communication Gap** | 戦略が現場に伝わらない（80%の経営者が認める） | 全社キャスケード · OKR分解 |
| **SP-06** | **Silo Strategy** | 部門間連携なし → 77%が障壁と報告 | クロスファンクショナルレビュー |
| **SP-07** | **Entire Market Fallacy** | 市場全体を狙う → 差別化なし | セグメント特化 · ポジショニング明確化 |
| **SP-08** | **Growth Driver Error** | 誤った成長ドライバーに基づく計画 | 仮説検証 · A/Bテスト · パイロット |
| **SP-09** | **Clarity Deficit** | 戦略が曖昧 → 解釈が人によって異なる | 具体的KPI · 成功基準の数値化 |
| **SP-10** | **Execution Neglect** | 策定に注力、実行計画なし | 実行ロードマップ · マイルストーン設定 |

---

## 2. 戦略実行ギャップ（Strategy-Execution Gap）

### 実行失敗の統計データ

```
実行ギャップの実態:
  - 適切に策定された戦略の 67% が実行段階で失敗（Bridges Business Consultancy）
  - 組織の 90% が戦略を成功裏に実行できていない（Harvard Business Review）
  - 経営者の 4/5 が「戦略が組織に理解されていない」と認める
  - 79% の失敗がコラボレーション不足に起因（ClearPoint Strategy）
  - リソースミスアラインメントで 60% のリソースが浪費（Cascade）
  - 5 つ以上の優先事項を持つ組織は効果が 30% 低下
```

### 実行失敗の根本原因

| 原因 | 影響度 | 説明 |
|------|--------|------|
| **アラインメント不足** | Critical | 戦略→部門→個人の目標が連鎖していない |
| **リソース配分ミス** | Critical | 戦略的優先事項と予算配分の不一致 |
| **コミュニケーション断絶** | High | 経営層の意図が現場に伝わらない |
| **サイロ化** | High | 部門間の情報・知識の断絶 |
| **アカウンタビリティ欠如** | High | 誰が何に責任を持つか不明確 |
| **変化への抵抗** | Medium | 組織慣性 · 既存利益の保護 |
| **測定不足** | Medium | 進捗を追跡するKPIが未定義 |

### 実行成功フレームワーク

```
Strategy-to-Execution Bridge:
  1. Translate（翻訳）: 戦略をOKR/KPIに分解
  2. Align（整合）: 部門目標と個人目標を連鎖
  3. Resource（配分）: 優先事項に合わせた予算・人員配置
  4. Communicate（伝達）: 全レベルへの戦略カスケード
  5. Monitor（監視）: 月次/四半期レビューサイクル
  6. Adapt（適応）: 環境変化に応じた戦略修正
```

---

## 3. Helm との連携

```
Helm での活用:
  1. SCAN モードでアンチパターン該当チェック（SP-01〜10）
  2. ROADMAP モードで実行ギャップリスクを事前評価
  3. strategy-monitoring の ANCHOR フェーズでアラインメント検証
  4. SIMULATE モードで優先事項数の影響をシミュレーション
  5. FORESIGHT キャリブレーションで実行率トラッキング

レポート出力:
  - 戦略ヘルスチェックに SP-01〜10 の該当/非該当を含める
  - 実行ギャップスコア = f(アラインメント, コミュニケーション, リソース配分)
  - 四半期レビューで実行進捗 vs 計画のギャップ分析
```

**Source:** [Bridges Business Consultancy: Strategy Execution Statistics](https://www.bridgesconsultancy.com/) · [Harvard Business Review: Strategy Execution](https://hbr.org/) · [ClearPoint Strategy: Why Strategies Fail](https://www.clearpointstrategy.com/) · [Cascade: Strategy Execution Statistics](https://www.cascade.app/blog/strategy-execution-statistics) · [Spider Strategies: Strategic Planning Mistakes 2025](https://www.spiderstrategies.com/blog/strategic-planning-mistakes-2025/)
