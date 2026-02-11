# Prompt Catalog

NotebookLMのステアリングプロンプト集。ユーザーがそのまま貼り付けて使えるテンプレート。

---

## How to Use This Catalog

1. 目的とオーディエンスに合うセクションを選ぶ
2. テンプレートの `[括弧]` 部分をユーザー固有の情報に置き換える
3. そのままNotebookLMのステアリングプロンプト欄に貼り付ける
4. 生成結果を評価し、必要に応じて調整する

**Tips:**
- プロンプトは150語以内が最も効果的
- 指示は8つ以下に絞る
- 「何を含めるか」より「何を省くか」が差を生む

---

## Audio Overview Prompts

### Deep Dive: Technical Audience

```
Target audience: Software engineers with 3-5 years of experience.
Focus heavily on: [architecture/pattern/technology name].
Tone: Conversational but technically precise. Use code-level terminology freely.
Make sure to discuss: trade-offs, real-world gotchas, and when NOT to use this approach.
Duration: aim for 15-20 minutes.
Skip: basic definitions the audience already knows.
Include at least one concrete example comparing this to alternative approaches.
```

**使い分け:** 技術的な深い理解が必要な場合。開発チーム向けの知識共有に最適。

### Deep Dive: Business Leaders

```
Target audience: Business leaders and product managers who make strategic decisions.
Focus on: business impact, ROI, competitive positioning, and market implications.
Tone: Engaging and data-driven, with concrete examples from recognizable companies.
Emphasize: actionable takeaways they can use in the next quarter.
Duration: 12-15 minutes.
Avoid: deep technical implementation details — use analogies instead.
End with: a clear "so what" section with 3 strategic recommendations.
```

**使い分け:** 経営層・PM向けの戦略的知識共有。意思決定を支援する情報提供。

### Deep Dive: Learners & Students

```
Target audience: Students or professionals new to [topic].
Assume: no prior knowledge of [specific domain].
Tone: Patient, encouraging, and filled with relatable analogies.
Structure: Start with "why this matters," then build concepts one by one.
Duration: 20-25 minutes.
Include: real-world examples for every abstract concept.
Use: the Feynman technique — explain as if teaching a curious 12-year-old.
Pause points: suggest moments where the listener should reflect or take notes.
```

**使い分け:** 教育・研修コンテンツ。初学者が段階的に理解を深められる構成。

### Deep Dive: General Audience

```
Target audience: Curious, intelligent adults with no specialized background in [topic].
Focus on: the human story behind the topic — why it matters to everyday life.
Tone: Like a great dinner conversation — engaging, surprising, and memorable.
Duration: 15-18 minutes.
Include: at least 2 surprising facts or counterintuitive insights.
Avoid: jargon. If a technical term is essential, explain it immediately.
End with: one clear takeaway the listener will remember tomorrow.
```

**使い分け:** ポッドキャスト的な一般向けコンテンツ。幅広い層への知識普及。

---

### The Brief: Executive Summary

```
Target audience: Busy executives who need the essence in under 10 minutes.
Tone: Crisp, confident, no filler.
Structure:
- Open with the single most important insight (30 seconds).
- Cover 3-5 key points, each in 1-2 minutes.
- Close with: "Here's what this means for your business."
Duration: 5-8 minutes maximum.
Skip: background context, methodology details, caveats.
Priority: clarity over completeness.
```

**使い分け:** 経営会議の前準備。時間のない意思決定者への要約。

### The Brief: Social Share

```
Target audience: Social media audience — short attention span, high curiosity.
Tone: Energetic, hook-driven, conversational.
Structure:
- Start with a provocative question or surprising stat.
- Cover the 2-3 most shareable insights.
- End with a cliffhanger or call-to-action that makes people want to learn more.
Duration: 3-5 minutes.
Make it: quotable. Every sentence should feel tweetable.
Avoid: nuance that slows momentum. Save depth for the Deep Dive version.
```

**使い分け:** SNSでの拡散を意図したショートコンテンツ。ティーザーとしても有効。

---

### The Critique: Research & Paper Analysis

```
Target audience: [Researchers / practitioners / students] in [field].
Analyze this source material as a critical reviewer would.
Structure:
- Summarize the core thesis in 2-3 sentences.
- Evaluate: methodology, evidence quality, logical consistency.
- Identify: strengths (what is convincing) and weaknesses (what is lacking).
- Compare: how this relates to established knowledge in [field].
- Conclude: with an overall assessment — is this worth building upon?
Tone: Fair but rigorous. Praise where earned, critique where needed.
Duration: 12-18 minutes.
```

**使い分け:** 論文レビュー、研究分析。批判的思考を促す学術的な評価。

### The Critique: Product & Service Evaluation

```
Target audience: Potential users or buyers evaluating [product/service category].
Analyze from the perspective of: [use case / user persona].
Structure:
- What problem does this solve? (2 minutes)
- Key strengths — what does it do well? (3-4 minutes)
- Weaknesses and limitations — what falls short? (3-4 minutes)
- Competitive comparison — how does it stack up against [alternatives]? (3 minutes)
- Verdict — who should use this, and who should look elsewhere?
Tone: Honest and practical. Like advice from a knowledgeable friend.
Duration: 12-15 minutes.
```

**使い分け:** プロダクトレビュー、サービス比較。購買決定を支援する評価。

---

### The Debate: Balanced Discussion

```
Present a balanced debate on [topic] with genuine intellectual tension.
Target audience: [specify].
Structure:
- Frame the central question clearly (1-2 minutes).
- Present Position A with its strongest evidence (5-7 minutes).
- Present Position B with its strongest evidence (5-7 minutes).
- Explore the nuances and edge cases where both positions have merit (3-5 minutes).
- Do NOT declare a winner. Let the listener form their own conclusion.
Tone: Respectful, intellectually honest. Steel-man both sides.
Duration: 18-22 minutes.
```

**使い分け:** 賛否が分かれるトピック。多角的な視点を公平に提示したい場合。

### The Debate: Guided Perspective

```
Discuss [topic] from multiple angles, but ultimately guide toward [position/recommendation].
Target audience: [specify].
Structure:
- Present the question and why it matters (2 minutes).
- Acknowledge the opposing view fairly — show you understand it (4-5 minutes).
- Build the case for [position] with evidence and logic (8-10 minutes).
- Address the strongest counterarguments head-on (3-4 minutes).
- Close with a clear recommendation and call to action.
Tone: Persuasive but not preachy. Respectful of the listener's intelligence.
Duration: 18-22 minutes.
```

**使い分け:** 特定の立場を支持しつつ、公平さを保ったい場合。提案型のコンテンツ。

---

### Lecture Mode: Tutorial

```
Teach [topic] as a hands-on tutorial.
Target audience: [specify skill level].
Prerequisites: [what the listener should already know].
Learning objectives:
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]
Structure: Concept → Example → Practice prompt → Concept → Example → Practice prompt.
Tone: Like a patient, expert mentor walking alongside the learner.
Duration: 20-25 minutes.
Include: "Try this yourself" moments where you describe exercises.
End with: a summary of what was learned and suggested next steps.
```

**使い分け:** 実践的なスキル習得。ハンズオン形式の教育コンテンツ。

### Lecture Mode: Academic Lecture

```
Deliver a structured academic lecture on [topic].
Target audience: [University level / Graduate / Professional].
Tone: Scholarly but accessible. Cite sources where relevant.
Structure:
- Introduce the topic and its significance in the broader field (3 minutes).
- Historical context and key developments (5 minutes).
- Core concepts and theoretical framework (8-10 minutes).
- Current state of research and open questions (5 minutes).
- Implications and future directions (3 minutes).
Duration: 25-30 minutes.
Include: references to key researchers and seminal works mentioned in the sources.
Avoid: oversimplification. Trust the audience's intelligence.
```

**使い分け:** 大学講義風のフォーマルな教育コンテンツ。学術的な深みを重視。

---

## Video Overview Prompts

### Explainer: Technical Concept

```
Visual style: Whiteboard
Create a visual explanation of [technical concept] for [audience].
Start with: the problem this solves — show the pain point visually.
Then show: the solution step by step with diagrams and flow arrows.
Pace: Allow 2-3 seconds per visual transition for comprehension.
Use: progressive disclosure — build complexity gradually on screen.
End with: a clear summary screen showing 3 key takeaways.
Keep text on screen: minimal. Let visuals carry the explanation.
```

**使い分け:** 技術概念の視覚的説明。ホワイトボードスタイルで段階的に理解を促す。

### Explainer: Product/Service

```
Visual style: Corporate
Create a product overview video for [product/service].
Target audience: [potential customers / stakeholders].
Structure:
- Hook: The problem your audience faces (10 seconds).
- Solution: What [product] does, shown visually (30 seconds).
- Key features: Top 3 differentiators with visual examples (60 seconds).
- Social proof: Mention results or adoption if available in sources.
- CTA: Clear next step for the viewer.
Tone: Professional, confident, benefit-focused.
Keep it: under 3 minutes total.
```

**使い分け:** プロダクト紹介・営業資料用のビデオ。機能より価値を伝える。

### Brief: Social Media Short

```
Visual style: Casual
Create a short, attention-grabbing video for social media.
Target audience: [specify platform — LinkedIn / YouTube / Twitter].
Hook: Open with the most surprising or counterintuitive insight within first 5 seconds.
Body: Deliver 2-3 key points with punchy visuals.
Pace: Fast cuts, no more than 5 seconds per visual.
End with: a question or statement that encourages engagement.
Total length: Under 90 seconds.
Tone: Energetic, direct, visually bold.
```

**使い分け:** SNS向けショートビデオ。スクロールを止めるフック重視。

### Brief: Teaser

```
Visual style: Cinematic
Create a teaser video that builds curiosity about [topic].
Goal: Make the viewer want to explore the full content.
Structure:
- Open with an intriguing visual or provocative question.
- Reveal 1-2 fascinating details without giving everything away.
- Build tension: "But there's something most people don't realize..."
- End with: a clear prompt to explore more.
Total length: 30-60 seconds.
Mood: Intriguing, high-production-feel, mysterious.
```

**使い分け:** フルコンテンツへの導線。好奇心を刺激するティーザー。

---

### Video Visual Style Selection Guide

| Style | Best For | Audience | Tone |
|-------|----------|----------|------|
| **Whiteboard** | 概念説明、プロセス | 学習者・技術者 | 教育的 |
| **Classroom** | 講義、トレーニング | 学生・研修受講者 | フォーマル |
| **Abstract** | 哲学的トピック、アート | クリエイティブ層 | 感覚的 |
| **Corporate** | ビジネスプレゼン、PR | 経営者・顧客 | プロフェッショナル |
| **Casual** | SNS、カジュアル解説 | 一般層 | フレンドリー |
| **Cinematic** | ストーリー、ブランド | 幅広い層 | ドラマチック |
| **Academic** | 研究発表、論文紹介 | 研究者・専門家 | 学術的 |
| **News** | 時事分析、トレンド | 情報収集層 | 客観的 |

---

## Slide Deck Prompts

### Presenter Slides: TED-style

```
Create a presentation for a [X-minute] talk.
Audience: [specify].
Structure:
- Title slide with a compelling hook (not a boring title).
- Problem statement: make the audience feel the problem (1-2 slides).
- Key insights: one idea per slide (3-5 slides).
- Supporting evidence: data or stories that make insights memorable.
- "So what?" implications: why this matters to THIS audience.
- Call to action: one clear thing the audience should do next.
Style: Minimal text — maximum 6 words per slide. Powerful visual cues.
Speaker notes: Include what the presenter should SAY, not what's on the slide.
```

**使い分け:** TED Talk/カンファレンス登壇。聴衆の感情を動かすプレゼン。

### Presenter Slides: Internal Presentation

```
Create slides for an internal [team/department/company] presentation.
Audience: [colleagues / leadership / cross-functional team].
Context: [meeting type — sprint review / strategy session / project update].
Structure:
- Context: Why we're here, what's changed (1 slide).
- Key findings or progress: Data-driven insights (3-5 slides).
- Recommendations or next steps: Clear actions with owners (1-2 slides).
- Discussion points: Questions for the group (1 slide).
Style: Clean, professional, data-rich. Charts and tables welcome.
Text level: More text than TED-style, but still scannable.
```

**使い分け:** 社内報告・レビュー。データと次のアクションを明確に伝える。

### Detailed Deck: Handout / Leave-behind

```
Create a detailed slide deck that can stand alone without a presenter.
Audience: [specify].
Purpose: [reference material / decision document / training resource].
Structure:
- Executive summary slide (everything on one slide).
- Topic sections: Each with title slide → 2-3 detail slides.
- Data slides: Include source citations and methodology notes.
- Appendix: Supplementary data and references.
Text level: Detailed enough for self-study. Complete sentences where needed.
Design: Clean layouts with clear visual hierarchy. Use headers, bullets, and callout boxes.
```

**使い分け:** 配布用資料。プレゼンなしで内容が完全に伝わる自立型ドキュメント。

### Detailed Deck: Educational Material

```
Create educational slides for [course/workshop/training] on [topic].
Audience: [specify level].
Learning objectives:
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]
Structure:
- Introduction: Why learn this? Real-world relevance.
- Concept slides: One concept per slide with visual explanation.
- Example slides: Concrete examples for each concept.
- Practice slides: Exercises or reflection questions.
- Summary slide: Key takeaways mapped to learning objectives.
Include: Definitions, diagrams, and "Remember" callout boxes.
Avoid: Walls of text. Use visuals to carry the explanation.
```

**使い分け:** 研修・教育資料。学習目標に沿った体系的なスライド構成。

---

## Infographic Prompts

### Data Summary

```
Orientation: Vertical (optimized for web/mobile scrolling).
Detail level: Standard.
Focus on: the 3-5 most impactful data points from the source material.
Visual hierarchy: Most important finding at the top or center.
Color palette: [professional / vibrant / monochrome — specify].
Style: Clean, modern, scannable in under 60 seconds.
Include: source attribution for key statistics.
Typography: Large numbers for key metrics, minimal body text.
```

**使い分け:** 数値・統計の視覚化。データドリブンなインサイトを一枚で伝える。

### Process Flow

```
Orientation: Vertical.
Detail level: Detailed.
Visualize: the [process/workflow/procedure] from start to finish.
Structure: Numbered steps with clear directional flow (top to bottom).
For each step: Icon + short title + 1-sentence description.
Highlight: decision points, common pitfalls, and tips.
Color coding: Use different colors for phases or categories.
End with: success criteria or expected outcome.
```

**使い分け:** 手順・ワークフローの視覚化。オペレーションガイドやプロセス説明。

### Comparative Analysis

```
Orientation: Vertical.
Detail level: Standard.
Compare: [Option A] vs [Option B] (vs [Option C] if applicable).
Structure:
- Header: The comparison question.
- Side-by-side or matrix layout for features/criteria.
- Visual indicators: checkmarks, ratings, or color-coded scores.
- Bottom: Summary verdict or "best for" recommendations.
Criteria to compare: [list 5-8 most important criteria].
Tone: Objective. Let the data speak.
```

**使い分け:** 選択肢の比較。ツール選定、技術選択、サービス比較。

---

## Mind Map Prompts

### Topic Exploration

```
Central topic: [topic].
Depth: 3 levels (main topic → subtopics → details).
Breadth: 4-6 main branches from the central topic.
For each branch: Include key concepts, relationships, and examples.
Highlight: connections between branches where topics intersect.
Style: Organic, visually balanced.
Purpose: [brainstorming / knowledge mapping / study guide].
```

**使い分け:** トピックの全体像把握。ブレインストーミングや学習の整理に。

---

## Deep Research Prompts

### Fast Research

```
Research topic: [specific question or topic].
Scope: Focus on the most recent and authoritative sources.
Depth: Overview level — key findings and trends.
Output: Structured summary with clear sections.
Priority: Speed over exhaustiveness.
Include: Key statistics, notable experts or organizations, and recent developments.
Exclude: Historical background unless directly relevant.
```

**使い分け:** 素早い概要把握。会議前の準備や初期リサーチに。

### Deep Research

```
Research topic: [specific question or topic].
Scope: Comprehensive analysis across multiple perspectives.
Depth: Thorough — include methodology, evidence quality, and competing viewpoints.
Output: Detailed report with:
- Executive summary
- Key findings organized by theme
- Evidence assessment (strong/moderate/weak)
- Knowledge gaps and open questions
- Recommended further reading
Time frame: Focus on [last N years / all time / specific period].
Sources priority: [Academic / Industry / Government / Mixed].
```

**使い分け:** 包括的な調査。意思決定や戦略立案の基盤となるリサーチ。

---

## Source Preparation Meta-Prompts

ステアリングプロンプトの効果を最大化するためのソース準備ガイド。

### Source Optimization Checklist

NotebookLMにソースを投入する前に確認:

```
□ テキストが機械読み取り可能か（スキャンPDFでないか）
□ 見出し構造が明確か（H1/H2/H3で整理されているか）
□ 不要なヘッダー/フッター/ページ番号を除去したか
□ 重複コンテンツを排除したか
□ 最重要情報がドキュメントの冒頭付近にあるか
□ ソース間で矛盾する情報がないか
□ 専門用語の定義がソース内に含まれているか（必要な場合）
□ ソースの言語が統一されているか
```

### Format-Specific Source Recommendations

**Audio Overview向け:**
- ソースは2-5本が最適（多すぎると焦点がぼやける）
- 対話で触れてほしいポイントを太字やハイライトで強調
- 議論の「種」となる対立する見解を含めると対話が豊かに

**Video Overview向け:**
- 図解可能なコンテンツを含むソースが効果的
- データ・統計を含むソースはビジュアル化されやすい
- ストーリーアークのあるソースが自然な動画構成を生む

**Slide Deck向け:**
- 構造化されたソースほど良いスライドになる
- 箇条書き・番号リストを多用したソースが効果的
- 図表やチャートの元データを含めると再現されやすい

**Infographic向け:**
- 数値データ・統計を含むソースが最も効果的
- 比較・ランキング情報は視覚化と好相性
- 1テーマに絞ったソースが最もクリーンな出力

---

## Prompt Customization Guide

### Audience Variable Substitution

テンプレートの `Target audience` を置き換える際の参考:

| Audience Type | Knowledge Assumption | Tone Modifier |
|---------------|---------------------|---------------|
| C-suite executives | Business strategy, no technical details | Decisive, bottom-line focused |
| Product managers | Cross-functional awareness | Practical, outcome-oriented |
| Senior engineers | Deep technical knowledge | Precise, pattern-aware |
| Junior developers | Basic concepts known | Encouraging, example-rich |
| Researchers | Domain expertise | Evidence-focused, nuanced |
| General public | No specialized knowledge | Accessible, analogy-driven |
| Students | Learning mindset | Structured, building-block approach |
| Sales teams | Customer-facing context | Benefit-focused, objection-aware |

### Duration Calibration

| Content Density | Audio | Video | Slides |
|----------------|-------|-------|--------|
| Overview / teaser | 3-5 min | 30-90 sec | 5-8 slides |
| Standard summary | 8-12 min | 2-3 min | 10-15 slides |
| Deep exploration | 15-25 min | 5-10 min | 20-30 slides |
| Comprehensive | 25-30 min | 10-15 min | 30+ slides |

---

## Template Composition Rules

上級ユーザー向け: 複数テンプレートの要素を組み合わせてカスタムプロンプトを作成する方法。

### Composition Process

1. **Base Template** を選ぶ（最も近いフォーマット×スタイル）
2. **Audience Layer** を別テンプレートから借用（必要な場合）
3. **Structure Directives** を目的に合わせて調整
4. **Tone Modifiers** を追加
5. **Negative Space** （除外指示）を追加
6. **Duration/Length** を指定

### Example: Custom Composition

Base: Deep Dive Technical + Audience: Business Leaders + Tone: Debate

```
Target audience: Technical leaders (CTOs, VPs of Engineering) who make architecture decisions.
Focus on: [technology] from both a technical merit AND business impact perspective.
Present this as a structured discussion between a technical advocate and a pragmatic skeptic.
For each point: Show the technical argument, then the business counter-argument.
Tone: Intellectually rigorous but grounded in real-world constraints.
Duration: 18-22 minutes.
Skip: Basic concepts. This audience knows their stack.
End with: A decision framework, not a single recommendation.
```

---

Remember: The best steering prompt is the one that makes the user say "this is exactly what I needed" — not the longest or most detailed one.
