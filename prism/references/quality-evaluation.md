# Quality Evaluation Framework

NotebookLM生成物の品質評価ルーブリックと改善手法。

---

## Universal Evaluation Criteria

すべてのフォーマットに共通する5つの評価軸:

| Criterion | Weight | Score 5 (Excellent) | Score 3 (Acceptable) | Score 1 (Poor) |
|-----------|--------|-------------------|---------------------|----------------|
| **Accuracy** | 30% | ソースに完全に忠実、事実誤認なし | 概ね正確だが軽微な不正確さあり | 明らかな事実誤認や捏造あり |
| **Audience Fit** | 25% | ターゲットの知識レベルに完璧にフィット | 概ね適切だが一部レベルのズレあり | 対象者に合っていない |
| **Engagement** | 20% | 最後まで引き込まれる魅力がある | 標準的な品質、退屈はしない | 途中で離脱したくなる |
| **Completeness** | 15% | 重要ポイントが過不足なく網羅 | 主要ポイントはカバー | 重要な情報が欠落 |
| **Actionability** | 10% | 次のアクションが明確に分かる | アクションを推測できる | 「で、何をすればいい？」 |

**Total Score Interpretation:**
- 4.5-5.0: Excellent — そのまま使用可能
- 3.5-4.4: Good — 軽微な調整で改善可能
- 2.5-3.4: Acceptable — プロンプト調整が必要
- 1.0-2.4: Poor — ソース品質の見直しから再設計が必要

---

## Format-Specific Rubrics

### Audio Overview Rubric

| Criterion | Evaluation Points |
|-----------|------------------|
| **Flow & Pacing** | 対話が自然に流れているか。唐突な話題転換がないか。沈黙や繰り返しがないか |
| **Voice Balance** | 2人の話者が均等に貢献しているか。一方的な独白になっていないか |
| **Depth vs Breadth** | ステアリングで指定した深さ/広さが実現されているか |
| **Opening Hook** | 最初の30秒で興味を引けているか |
| **Closing Impact** | 明確なまとめと次のアクションで終わっているか |
| **Source Fidelity** | ソースにない情報を追加していないか |
| **Tone Match** | 指定したトーン（カジュアル/フォーマル等）に合っているか |

**Audio-Specific Red Flags:**
- 同じポイントを3回以上繰り返す
- ソースにない「事実」を創作する
- 片方の話者が80%以上話している
- 突然トピックが変わる（「ところで...」の多用）
- 結論なく終わる

---

### Video Overview Rubric

| Criterion | Evaluation Points |
|-----------|------------------|
| **Visual Clarity** | 映像が内容を効果的に補強しているか。ビジュアルと音声が一致しているか |
| **Style Consistency** | 選択したビジュアルスタイルが一貫しているか |
| **Pacing** | 各ビジュアルの表示時間が適切か（早すぎ/遅すぎ） |
| **Text Readability** | 画面上のテキストが読みやすいか |
| **Visual Hierarchy** | 重要な情報がビジュアル的に強調されているか |
| **Narrative Arc** | 開始→展開→結末の構造があるか |

**Video-Specific Red Flags:**
- 音声とビジュアルがずれている
- テキストが小さすぎて読めない
- ビジュアルの切り替えが早すぎて理解が追いつかない
- スタイルが途中で変わる
- 情報が詰め込みすぎ

---

### Slide Deck Rubric

| Criterion | Evaluation Points |
|-----------|------------------|
| **Slide Structure** | 1スライド1メッセージの原則が守られているか |
| **Text Density** | Presenter Slides: 6語以下/Detailed: 適切な情報量 |
| **Visual Design** | レイアウトが一貫し、視覚的に洗練されているか |
| **Flow Logic** | スライド間の論理的なつながりが明確か |
| **Data Presentation** | グラフ・表が正確で読みやすいか |
| **Speaker Notes** | (Presenter) 話すべき内容が十分に記載されているか |

**Slide-Specific Red Flags:**
- 壁のようなテキスト（text wall）
- スライド間の論理的飛躍
- グラフのラベルが欠落
- 冗長なスライド（同じメッセージの繰り返し）
- 結論・CTA スライドの欠如

---

### Infographic Rubric

| Criterion | Evaluation Points |
|-----------|------------------|
| **Visual Hierarchy** | 最重要情報が最も目立つ位置にあるか |
| **Scannability** | 60秒以内で要点を把握できるか |
| **Data Accuracy** | 数値・統計が正確か |
| **Design Consistency** | カラー・フォント・アイコンが統一されているか |
| **Information Density** | 情報量が適切か（多すぎ/少なすぎ） |

**Infographic-Specific Red Flags:**
- データの出典が不明
- 色使いが多すぎて視覚的に混乱
- 文字が小さすぎる
- レイアウトの流れが不明確

---

## Common Quality Problems & Solutions

### Problem 1: 内容が浅い / 表面的

**症状:** 重要なトピックに深く踏み込まない。一般論に終始する。

**原因と対策:**
| Likely Cause | Solution |
|-------------|----------|
| ソースが浅い | より専門的なソースを追加 |
| プロンプトが曖昧 | Focus Laser パターンで特定トピックを指定 |
| オーディエンスレベルが未指定 | Audience Anchor パターンで専門性を明示 |

**プロンプト調整例:**
```
Before: "Explain [topic]"
After:  "Focus heavily on [specific subtopic]. Skip the introduction and basic concepts.
         Dive directly into the trade-offs and real-world implications for [audience]."
```

---

### Problem 2: ソースにない情報の創作

**症状:** ソースに記載されていない「事実」や「データ」が出力に含まれる。

**原因と対策:**
| Likely Cause | Solution |
|-------------|----------|
| ソースに情報不足 | 不足情報を含むソースを追加 |
| プロンプトの要求が広すぎ | スコープを明確に限定 |

**プロンプト調整例:**
```
Add: "Only discuss information that is directly supported by the provided sources.
      Do not add external examples or statistics not in the source material."
```

---

### Problem 3: トーンのミスマッチ

**症状:** カジュアルにしたいのにフォーマル、またはその逆。

**原因と対策:**
| Likely Cause | Solution |
|-------------|----------|
| Tone指示が不十分 | Tone Dial パターンで具体的に指定 |
| ソースのトーンに引きずられている | トーン指示を強調 |

**プロンプト調整例:**
```
Before: "Tone: casual"
After:  "Tone: Like two friends discussing this over coffee. Use humor where natural.
         Avoid: formal language, passive voice, academic phrasing."
```

---

### Problem 4: 構成が散漫

**症状:** トピックが行ったり来たり。明確な構造がない。

**原因と対策:**
| Likely Cause | Solution |
|-------------|----------|
| 構成指示なし | Structural Blueprint パターンで構成を明示 |
| ソースが構造化されていない | ソースを整理してから再投入 |

**プロンプト調整例:**
```
Add: "Structure: Follow this exact order:
      1. [Topic A] - 5 minutes
      2. [Topic B] - 5 minutes
      3. [Topic C] - 5 minutes
      Do not jump between topics."
```

---

### Problem 5: 長すぎる / 短すぎる

**症状:** 指定した時間・長さと大きくずれる。

**原因と対策:**
| Likely Cause | Solution |
|-------------|----------|
| Duration未指定 | Duration Target パターンで明示 |
| カバー範囲が広すぎ/狭すぎ | フォーカスを調整 |

**プロンプト調整例:**
```
Add: "Duration: strictly 10-12 minutes. No longer.
      Cover only the top 3 most important points. Sacrifice breadth for depth."
```

---

## A/B Prompt Testing Method

同じソースで2つのプロンプトを比較し、最適なプロンプトを見つける手法。

### Process

```
Step 1: ベースプロンプトで生成 (Version A)
Step 2: 1つの変数だけを変更 (Version B)
Step 3: 両方を評価ルーブリックで採点
Step 4: 高スコアの方をベースに次の変数をテスト
Step 5: 2-3回の反復で最適化
```

### Variables to Test (One at a Time)

| Variable | Version A | Version B |
|----------|-----------|-----------|
| **Audience level** | "experts" | "beginners" |
| **Tone** | "formal" | "conversational" |
| **Focus** | "broad overview" | "deep on 2 topics" |
| **Structure** | "free-form" | "strict section order" |
| **Duration** | "10 min" | "20 min" |
| **Negative space** | (no skip list) | "Skip: X, Y, Z" |

### Evaluation Template

```
## A/B Test Results

Source: [Same source for both]
Variable tested: [What changed between A and B]

### Version A
Prompt: [Full prompt text]
Score: Accuracy [X] / Audience [X] / Engagement [X] / Completeness [X] / Actionability [X]
Total: [Weighted average]
Notes: [Observations]

### Version B
Prompt: [Full prompt text]
Score: Accuracy [X] / Audience [X] / Engagement [X] / Completeness [X] / Actionability [X]
Total: [Weighted average]
Notes: [Observations]

### Result
Winner: [A or B]
Reason: [Why]
Next test: [What to change next]
```

---

## Iterative Improvement Workflow

### The REFINE Loop

```
┌──────────────┐
│  Generate    │ ← Initial prompt
└──────┬───────┘
       ↓
┌──────────────┐
│  Evaluate    │ ← Apply rubric
└──────┬───────┘
       ↓
┌──────────────┐     ┌──────────────┐
│  Score < 3.5 │ ──→ │ Reassess     │ ← Source or format change needed
│  (Poor)      │     │ Source/Format │
└──────────────┘     └──────────────┘
       ↓ Score ≥ 3.5
┌──────────────┐
│  Identify    │ ← Top 2-3 improvement areas
│  Gaps        │
└──────┬───────┘
       ↓
┌──────────────┐
│  Adjust      │ ← Change ONE prompt element
│  Prompt      │
└──────┬───────┘
       ↓
┌──────────────┐
│  Regenerate  │ ← Compare with previous
└──────┬───────┘
       ↓
┌──────────────┐
│  Score ≥ 4.0 │ ──→ DONE ✓
│  or 3 rounds │
└──────────────┘
```

### Guidelines

- **1回の調整で1つの要素だけ変更する** — 複数同時変更は効果の判別が困難
- **3ラウンドで改善が見られない場合** — ソース品質の問題を疑う
- **スコア4.0以上で十分** — 完璧を追求しすぎない
- **成功パターンを記録する** — 同じタイプのコンテンツに再利用

---

Remember: Quality evaluation is not about perfection — it's about knowing when your output is "good enough" and what specific adjustment will have the most impact.
