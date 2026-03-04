# Outcome Roadmapping & Stakeholder Alignment

> NOW/NEXT/LATER, OKR 統合, アウトカムロードマップ, DACI, プロダクトトリオ, デザインスプリント

## 1. ロードマップの進化

### 3つのロードマップタイプ

| タイプ | フォーカス | メリット | リスク |
|--------|----------|---------|-------|
| **Feature Roadmap** | 何を・いつ作るか | 具体的で実行しやすい | 硬直的、変更に弱い |
| **Theme-Based Roadmap** | フォーカスエリア | ストーリーテリングに有効 | 優先順位が曖昧になりやすい |
| **Outcome Roadmap** | どの成果を達成するか | 戦略的柔軟性、適応性高い | 具体性が低く実行チームに不安 |

### Spark での推奨

- 提案書に**アウトカム（成果）を必ず記載**（既存の RICE + 仮説に加えて）
- 複数提案をロードマップ化する場合は **Theme-Based + Outcome** のハイブリッド
- Feature Roadmap は実行フェーズ（Sherpa/Builder）に委譲

---

## 2. NOW / NEXT / LATER フレームワーク

### 概要

タイムラインベースの厳密なスケジュールではなく、**確信度ベースの優先度分類**。

| 区分 | 確信度 | スコープ | Spark 提案との対応 |
|------|--------|---------|-----------------|
| **NOW** | 高 | 短期で測定可能な OKR | RICE ≥ 100 + 仮説検証済み |
| **NEXT** | 中 | NOW 完了後にフォーカス | RICE 50-100 or 検証中 |
| **LATER** | 低 | 長期的な志向 | アイデア段階 / 探索中 |

### OKR との統合

```
Company OKR: 「月間アクティブユーザーを20%増加」
  ↓
NOW: オンボーディングフロー改善（KR: 7日目リテンション +15%）
  → Spark 提案 A（RICE: 120, 検証済み）
NEXT: ソーシャルシェア機能（KR: バイラル係数 +0.3）
  → Spark 提案 B（RICE: 85, Fake Door テスト予定）
LATER: コミュニティ機能（KR: UGC 投稿数 1000/月）
  → Spark 提案 C（RICE: 未算出, 探索段階）
```

### Spark 提案テンプレートへの追加

```markdown
## Roadmap Position
- **Position**: [NOW | NEXT | LATER]
- **Confidence**: [High | Medium | Low]
- **関連 OKR**: ___
- **昇格条件**: LATER→NEXT: ___ / NEXT→NOW: ___
```

---

## 3. ステークホルダー整合手法

### DACI フレームワーク

意思決定プロセスの役割を明確化。

| 役割 | 責任 | Spark での典型例 |
|------|------|---------------|
| **Driver（推進者）** | 意思決定プロセスを推進 | PM（Spark の呼び出し元） |
| **Approver（承認者）** | 最終判断を下す1人 | プロダクトリード / CTO |
| **Contributors（貢献者）** | 専門知識を提供 | Designer, Engineer, Data |
| **Informed（周知対象）** | 結果を知る必要がある人 | CS, Sales, Marketing |

### Spark 提案への DACI 組み込み

```markdown
## Decision Framework (DACI)
| Role | Person | Responsibility |
|------|--------|----------------|
| Driver | ___ | 提案の推進、レビュー調整 |
| Approver | ___ | Go/No-Go 最終判断 |
| Contributors | ___ | 技術/デザイン/ビジネスインプット |
| Informed | ___ | 結果の周知対象 |
```

---

## 4. プロダクトトリオ

### 概要

Teresa Torres が提唱。**PM + Designer + Lead Engineer** の3者が共同でディスカバリーを行う協働モデル。

### なぜトリオか

| 単独ディスカバリーの問題 | トリオの利点 |
|---------------------|------------|
| PM だけの視点に偏る | 3つの視点（ビジネス・UX・技術） |
| 実現可能性の見落とし | Engineer が早期に技術制約を提示 |
| デザインが後付けに | Designer が UX を初期から設計 |
| サイロ化・引き継ぎコスト | 共有コンテキストで引き継ぎ不要 |

### Spark エージェント連携での模倣

```
Product Trio の模倣:
  PM 視点     → Spark（ビジネス価値・優先度）
  Design 視点 → Echo / Palette（UX・ユーザビリティ）
  Eng 視点    → Scout / Lens（技術実現可能性）
```

---

## 5. デザインスプリント（2025年動向）

### 進化

- 大企業がスプリントを**自社文化・タイムライン・ステークホルダーに合わせてカスタマイズ**
- 銀行・建設業など従来縁遠かった業界でも採用拡大
- **目的の多様化**: 新機能検証だけでなく、ステークホルダー整合、リフレーミング、意思決定加速

### Spark 提案のキックオフでの活用

| スプリント Day | Spark 連携 |
|-------------|----------|
| Day 1: Understand | IGNITE フェーズの入力収集 |
| Day 2: Sketch | 複数ソリューション案の生成（Multi-Engine Mode） |
| Day 3: Decide | RICE + 投票で最適案選定 |
| Day 4: Prototype | Forge エージェントでプロトタイプ |
| Day 5: Test | Echo エージェントでユーザー検証 |

---

## 6. North Star Metric との整合

### 概要

プロダクト全チームが一つの指標に集結することで、優先順位付けが明確になるフレームワーク。

### よくある落とし穴（2025年）

| 落とし穴 | 対策 |
|---------|------|
| バニティメトリクスを North Star にする | ユーザー価値を直接反映する指標を選ぶ |
| 設定するだけで組織に浸透させない | 全提案に North Star への貢献度を記載 |
| 市場変化に応じて更新しない | 四半期ごとに妥当性を再評価 |

### Leading vs Lagging Indicators

| タイプ | 役割 | 例 | 比率 |
|--------|------|-----|------|
| **Leading** | 将来の成果を予測 | 機能採用率、エンゲージメント | 60% |
| **Lagging** | 過去の成果を測定 | 収益、チャーン率 | 40% |

**推奨**: Leading 60% : Lagging 40% の比率で、予測と検証のフィードバックループを維持。

### Spark 提案への組み込み

```markdown
## North Star Alignment
- **North Star Metric**: ___
- **この提案の貢献**: ___
- **Leading Indicator**: ___ (目標値: ___)
- **Lagging Indicator**: ___ (期待変化: ___)
```

---

## 7. 実験文化（Ship to Validate）

### パラダイムシフト

```
従来: Ship to Release（リリースのために出荷）
  ↓
現代: Ship to Validate（検証のために出荷）
```

### ベストプラクティス

| プラクティス | 説明 |
|------------|------|
| **最小検証ファースト** | 「何を作るか」→「検証に最もシンプルなテストは？」 |
| **Feature Flags** | 全面展開前に小セグメントで検証 |
| **失敗の共有** | 反直観的結果を分析付きで全チームに共有 |
| **QA サイクル短縮** | 検証目的の出荷はフルQAを省略可能 |

### Spark 提案のバリデーション戦略

```markdown
## Validation Strategy

### Phase 1: Pre-build (1-3日)
- [ ] Fake Door Test (CTR ≥ ___%)
- [ ] ユーザーインタビュー (n=___人)

### Phase 2: Prototype (1週間)
- [ ] Wizard of Oz or Forge プロトタイプ
- [ ] Echo エージェントでユーザビリティ検証

### Phase 3: Limited Release
- [ ] Feature Flag で ___% にリリース
- [ ] Leading Indicator を ___日間追跡
- [ ] Kill Criteria: ___ の場合ロールバック

### Phase 4: Full Release
- [ ] ガードレールメトリクス確認
- [ ] Lagging Indicator の追跡開始
```

**Source:** [Outcome-Based Roadmaps - Product School](https://productschool.com/blog/product-strategy/outcome-based-roadmap) · [NOW-NEXT-LATER - Product School](https://productschool.com/blog/product-strategy/now-next-later-roadmap) · [OKRs and Roadmaps - Roman Pichler](https://www.romanpichler.com/blog/okrs-and-product-roadmaps/) · [DACI - Atlassian](https://www.atlassian.com/team-playbook/plays/daci) · [OST - Product Talk](https://www.producttalk.org/opportunity-solution-trees/) · [Design Sprints 2025](https://www.designsprint.academy/blog/design-sprints-in-2025-the-questions-enterprise-teams-are-really-asking) · [North Star Metric - Amplitude](https://amplitude.com/blog/product-north-star-metric) · [Leading vs Lagging - Statsig](https://www.statsig.com/perspectives/leading-vs-lagging-indicators-in-product-metrics) · [Ship to Validate - Optimizely](https://www.optimizely.com/product-experimentation/) · [Experimentation Culture Awards 2025](https://experimentationcultureawards.com)
