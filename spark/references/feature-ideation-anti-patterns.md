# Feature Ideation Anti-Patterns

> Feature Factory, HiPPO, Build Trap, Sunk Cost, Shiny Object Syndrome とその対策

## 1. Feature Factory（機能工場）

### 定義

John Cutler（2016年）命名。ディスカバリーよりデリバリーを優先し、影響を理解せずに機能を出荷する組織パターン。

**衝撃的データ**: エンタープライズソフトウェアの機能の **80% は、ほとんどまたは全く使用されていない**（Product Management Insights Report 2023）。

### 症状チェックリスト

| # | 症状 | 該当? |
|---|------|-------|
| 1 | 機能の出荷数が成功指標になっている | |
| 2 | 出荷後の機能利用率を測定していない | |
| 3 | バックログが肥大化し続けている | |
| 4 | チームが「何を作るか」で忙しく「なぜ作るか」を問わない | |
| 5 | ステークホルダーからの機能リクエストがそのまま開発に入る | |
| 6 | 四半期の業績が「リリースした機能数」で測られる | |

### 根本原因

- プロダクトチームの自律性の低さ
- エンパワーされていない PM
- 明確なプロダクトビジョンの欠如
- 短期的な四半期業績プレッシャー
- 「チームを忙しく保つ」ことへの過度の重視

### 脱出方法

- **OKR**: デリバリーではなく成果（Outcome）に焦点
- **データ駆動の優先順位付け**: RICE/ICE を政治的議論の代替に
- **出荷後メトリクス**: 採用率・リテンション・タスク完了率の追跡
- **Kill Criteria**: 提案時に「この機能を削除する条件」も定義

---

## 2. HiPPO Effect

### 定義

**HiPPO = Highest Paid Person's Opinion**（最も高い報酬を受ける人の意見）。上級管理職の信念がプロダクトディスカバリーを駆動する現象。

### Spark での対策

| 対策 | Spark での実装 |
|------|-------------|
| **データで議論** | RICE Score を提案に必須化（既存） |
| **実験で検証** | 仮説 + 成功基準を提案に含める（既存） |
| **匿名投票** | Multi-Engine Mode で複数 AI の独立提案を比較 |
| **ペルソナの声** | 「誰のための機能か」を明示し、HiPPO の主観を排除 |

---

## 3. Build Trap（構築の罠）

### 定義

プロダクトの成果ではなく構築そのものに焦点を当ててしまう罠。「何を作るか」にフォーカスし「なぜ作るのか」を見失う状態。

### Feature Factory との違い

| 観点 | Feature Factory | Build Trap |
|------|----------------|-----------|
| フォーカス | 出荷速度・出荷数 | 構築プロセス自体 |
| 問題 | 影響測定の欠如 | 目的意識の欠如 |
| 症状 | 使われない機能の山 | 意味のない忙しさ |
| 対策 | 出荷後メトリクス | アウトカム志向 |

### 脱出パターン

```
Build Trap: 「次に何を作ろう？」
    ↓ 転換
Outcome Focus: 「どの成果を改善しよう？」→「その成果に最も効く施策は？」
```

---

## 4. Sunk Cost Fallacy（埋没費用の誤謬）

### 定義

過去に投資した時間・労力のために、失敗した方向性に固執し続ける傾向。開発時間だけでなく、**調査・計画に費やした知的・感情的資本**も含む。

### 対策

| 対策 | 説明 |
|------|------|
| **Kill Criteria** | 提案時に「撤退条件」を事前定義 |
| **Time-boxed Experiments** | 投資を最小化し埋没コストを小さく保つ |
| **Pre-mortem** | 「この機能が失敗したとしたら、なぜか？」を事前に議論 |
| **定期レビュー** | 進行中の機能の ROI を四半期ごとに再評価 |

### Spark 提案への組み込み

```markdown
## Kill Criteria（撤退条件）

以下のいずれかに該当した場合、機能の撤退を検討:
- リリース後30日で採用率が ___% 未満
- 主要メトリクスが ___% 以上悪化
- 実験で統計的に有意な改善が確認できない
```

---

## 5. Shiny Object Syndrome（光り物症候群）

### 定義

新しくて目立つ機能やトレンドに飛びつく傾向。競合が持っているという理由だけで機能を追加する「追いかけっこ」パターン。

### 判定フレームワーク

```
新機能リクエスト受信
  ↓
Q1: 自社のプロダクトビジョンに合致するか? → No → 却下
  ↓ Yes
Q2: ターゲットペルソナのニーズに基づくか? → No → 却下
  ↓ Yes
Q3: RICE Score は基準値以上か? → No → バックログ
  ↓ Yes
Q4: 既存機能の強化で対応可能か? → Yes → 既存機能改善
  ↓ No
通常の提案プロセスへ
```

---

## 6. 追加アンチパターン（2025年）

### ユーザーの「解決策」をそのまま受け取る

```
❌ ユーザー「もっと良いレポートが欲しい」→ 即座にダッシュボード構築
✅ 「なぜレポートが必要？」→ 根本的ニーズを理解 → 最適な解決策を設計
```

### 未熟な MVP のローンチ

2025年の市場では消費者の期待が高騰。AI が新しい品質基準を設定した中で、未成熟な MVP は逆効果になることが多い。

**対策**: MVP の「V（Viable = 実行可能）」を再定義。最小限だが**使い物になる**品質を確保。

### Exploitative Discovery への偏り

| タイプ | 説明 | Spark での対応 |
|--------|------|-------------|
| **Exploit（活用）** | 既存の最適化 | Favorite Patterns（既存） |
| **Explore（探索）** | 新しい可能性の探索 | OST の Opportunity 層を拡大 |

**推奨比率**: Exploit 70% : Explore 30%

---

## 7. Spark のアンチパターン防止チェックリスト

### 提案前チェック

- [ ] 特定のペルソナが明確か?（「全員向け」は却下）
- [ ] ビジネス成果（Outcome）が定義されているか?
- [ ] RICE Score を算出したか?
- [ ] Kill Criteria を定義したか?
- [ ] 既存機能の強化で対応できないか確認したか?

### 提案中チェック

- [ ] HiPPO の意見ではなくデータに基づいているか?
- [ ] 競合追随ではなく自社ビジョンに合致するか?
- [ ] 仮説が測定可能か?
- [ ] Sunk Cost に引きずられていないか?

### 提案後チェック

- [ ] 出荷後の採用率を測定する計画があるか?
- [ ] Kill Criteria に基づく定期レビューが予定されているか?

**Source:** [Feature Factory - John Cutler](https://productdirection.co/4-reasons-why-product-teams-cant-avoid-the-feature-factory-trap/) · [Escaping the Feature Factory - Scrum.org](https://www.scrum.org/resources/blog/escaping-feature-factory) · [Product Discovery Anti-Patterns - Age of Product](https://age-of-product.com/product-discovery-anti-patterns/) · [Build Trap - LogRocket](https://blog.logrocket.com/product-management/build-trap-dangers-feature-factory-mindset/) · [Sunk Cost - Skedulo](https://medium.com/skedulo-engineering/avoiding-the-sunk-cost-fallacy-in-product-development-79dfeb4e7422) · [Shiny Object Syndrome - CareerFoundry](https://careerfoundry.com/en/blog/product-management/shiny-object-syndrome/) · [Product Mistakes 2026 - Ant Murphy](https://antmurphy.medium.com/product-mistakes-i-wont-repeat-in-2026-49533cfab6be) · [SVPG Anti-Patterns](https://www.svpg.com/product-discovery-anti-patterns/)
