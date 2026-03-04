# Lean Validation Techniques

> Fake Door Test, Wizard of Oz, Concierge MVP, 軽量 PRD フォーマット, Spec-Driven Development

## 1. 構築前バリデーション手法

### 手法比較

| 手法 | コスト | 期間 | 検証対象 | 忠実度 |
|------|--------|------|---------|--------|
| **Fake Door Test** | 極低 | 数時間〜1日 | 需要・関心度 | 低 |
| **Wizard of Oz** | 低〜中 | 1〜2週間 | 体験・ユーザビリティ | 中〜高 |
| **Concierge MVP** | 中 | 2〜4週間 | 価値・ワークフロー | 高 |
| **Prototype (Forge)** | 中 | 1〜2週間 | UX・フロー | 中 |
| **A/B Test (Experiment)** | 高 | 2〜6週間 | 効果・成果 | 高 |

### 選択フローチャート

```
「この機能に需要があるか？」
  → 不明 → Fake Door Test
  → ありそう →
    「ユーザーはこの体験を使いたいか？」
      → 不明 → Wizard of Oz / Concierge
      → 使いたそう →
        「どの実装が最も効果的か？」
          → Prototype → A/B Test
```

---

## 2. Fake Door Test (Painted Door Test)

### 概要

実際の機能を構築せずに、ユーザーの関心度を測定する手法。CTA ボタン、メニュー項目、通知などで存在しない機能の「ファサード」を提示。

### 実装パターン

| パターン | 説明 | 測定指標 |
|---------|------|---------|
| **CTA ボタン** | 「新機能を試す」ボタン → ウェイトリスト登録 | CTR, 登録率 |
| **メニュー項目** | 新メニュー追加 → 「Coming Soon」表示 | クリック率 |
| **アプリ内通知** | 「新機能のベータ版に参加しませんか？」 | 応答率 |
| **プレオーダー** | 機能提供前にサインアップ受付 | サインアップ率 |

### 先進的メトリクス（2025年）

| メトリクス | 意味 |
|-----------|------|
| **ユニーク vs 合計クリック** | 繰り返しクリック = 強い関心の指標 |
| **クリックまでの時間** | 即時 = 強い関心、遅延 = 探索による発見 |
| **クリック後の行動** | 即離脱 = 軽い好奇心、継続 = 本物の需要 |

### Spark 提案への組み込み

```markdown
## Pre-validation Plan

### Fake Door Test
- **配置場所**: ___
- **CTA テキスト**: ___
- **成功基準**: CTR ≥ ___% (期間: ___ 日間)
- **サンプルサイズ**: ___ ユニークユーザー
- **結果が基準未満の場合**: 提案を再検討 / ピボット
```

---

## 3. Wizard of Oz プロトタイピング

### 概要

完全に機能する製品機能をテクノロジーを使わずにシミュレート。すべての入出力を人間が手動で実行するが、顧客はそれを知らない。

### 活用シナリオ

| シナリオ | 人間が行う操作 | ユーザーが見るもの |
|---------|-------------|---------------|
| **AI レコメンド** | 手動で推薦リスト作成 | 「AI による推薦」表示 |
| **自動分類** | 手動でカテゴリ分類 | 「自動分類済み」表示 |
| **チャットボット** | 人間がリアルタイム応答 | チャット UI |
| **データ分析** | 手動でレポート作成 | 「自動生成レポート」表示 |

### メリットとリスク

| メリット | リスク |
|---------|-------|
| 技術投資前に需要検証 | スケールしない（人的コスト） |
| ユーザーの自然な行動を観察 | 倫理的考慮（透明性） |
| 構築前に UX インサイト獲得 | 応答速度の制約 |

### Spark との関連

- VERIFY フェーズで「Wizard of Oz テスト可能か？」を評価
- 技術的に複雑な提案（AI 機能等）の事前検証に特に有効
- テスト結果を Experiment エージェントとの連携で構造化

---

## 4. Concierge MVP

### Wizard of Oz との違い

| 観点 | Wizard of Oz | Concierge MVP |
|------|------------|---------------|
| 透明性 | ユーザーは自動化と認識 | ユーザーは人間のサービスと認識 |
| スケール | 限定的 | さらに限定的（1対1） |
| 検証対象 | UX・体験 | 価値・ワークフロー全体 |
| 期間 | 短期 | 中期（反復学習） |

### 活用例

- **Zappos**: 靴の在庫を持たず、注文が入ったら小売店で購入して発送
- **Food on the Table**: 創業者が1人の顧客の食料品店に同行してレシピを推薦
- **Aardvark**: Q&Aサービスを人間が手動で回答してからAI化

---

## 5. 軽量 PRD フォーマット

### 現代 PRD の進化

| 従来の PRD | 現代の PRD |
|-----------|-----------|
| 大量のウォーターフォール文書 | ブログ記事のように読みやすい |
| 開発前にすべて詳細化 | イテレーション前提の柔軟構造 |
| スペック重視 | ユーザーデータとインサイト重視 |
| Word/Confluence | Notion/FigJam/Linear |

### Amazon 6-Pager / 1-Pager

**6-Pager**（Jeff Bezos, 2004年）:
- PowerPoint 禁止。会議冒頭30分の黙読
- 箇条書きなし、グラフィックなし。密度の高いナラティブ6ページ
- データ・グラフは付録（Appendix）
- **構成**: Introduction → Goals → Tenets → State of Business → Lessons Learned → Strategic Priorities

**1-Pager**:
- 重要な詳細を1ページに凝縮
- ビジネスインパクトと戦略的整合性に焦点
- ステークホルダーの迅速な整合に最適

### RFC + ADR の二層構造（2025年推奨）

| ドキュメント | 目的 | タイミング |
|------------|------|----------|
| **RFC** | フィードバック収集 | 変更が他者に影響しバイインが必要な場合 |
| **ADR** | 決定の記録 | RFC の結果として実装戦略を記録 |

**ベストプラクティス**:
- ADR は短く保つ（参照文書であり、エッセイではない）
- Git にバージョン管理し変更を経時的に追跡
- RFC レビュー期間は2〜3日（非同期コメント）
- プロセスは可能な限り軽量に

---

## 6. Spec-Driven Development (SDD)

### 概要（Thoughtworks Technology Radar 2025）

仕様書を第一級オブジェクトとして扱い、AI コーディングエージェントへの入力とするパラダイム。

```
Spark 提案仕様 → 構造化スペック → AI エージェント → 実行可能コード
```

### ツール比較

| ツール | アプローチ |
|--------|----------|
| **Amazon Kiro** | 要件 → 設計 → タスクの3段階 |
| **GitHub spec-kit** | 3ステップ + constitution（不変原則） |
| **Tessl** | 仕様自体が保守対象アーティファクト |

### Spark への示唆

- 提案仕様の構造化レベルが AI コード生成品質に直結
- **技術制約の明示化**がより重要に（「何を作るか」+「どう作るか」の境界）
- Builder へのハンドオフ時に SDD 対応フォーマットを検討

---

## 7. バリデーション手法の Spark フェーズ統合

| Spark フェーズ | バリデーション手法 | 目的 |
|-------------|---------------|------|
| IGNITE | Discovery Cadence | 機会の継続的発見 |
| SYNTHESIZE | Opportunity Score (ODI) | 機会の定量評価 |
| SPECIFY | 軽量 PRD / RFC | 仕様の迅速な文書化 |
| VERIFY | Fake Door / Wizard of Oz | 構築前の需要検証 |
| PRESENT | 1-Pager / SDD スペック | ステークホルダー整合 + AI 実装入力 |

**Source:** [Fake Door Testing - Amplitude](https://amplitude.com/explore/experiment/fake-door-testing) · [Painted Door Test - ProdPad](https://www.prodpad.com/blog/painted-door-test/) · [Wizard of Oz - NN/g](https://www.nngroup.com/articles/wizard-of-oz/) · [Wizard of Oz - LearningLoop](https://learningloop.io/plays/wizard-of-oz) · [Amazon 6-Pager - Visme](https://visme.co/blog/amazon-6-pager/) · [PRD Guide - Product School](https://productschool.com/blog/product-strategy/product-template-requirements-document-prd) · [ADR vs RFC - candost.blog](https://candost.blog/adrs-rfcs-differences-when-which/) · [SDD - Thoughtworks](https://www.thoughtworks.com/en-us/radar/techniques/spec-driven-development)
