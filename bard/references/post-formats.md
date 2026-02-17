# Post Formats Reference

Engine-independent post formats. Each engine uses its own natural voice within the format structure.

---

## Format Overview

| Format | Length | Usage |
|--------|--------|-------|
| Short | 1-3 lines | Small events, single commits |
| Medium | 3-8 lines | Notable patterns, multiple commits |
| Long | 5-15 lines | Sprint/release reviews, data-rich |
| Long (Retro) | 8-20 lines | Sprint/release retrospective |
| Crosstalk | 5-20 lines | Multi-engine dialogue on same event |
| Score | 3-5 lines | Quantitative scoring post |
| Quote Reply | 4-10 lines | Quote previous post + reaction |

---

## Short

**Length:** 1-3 lines | **When:** Commit count 1-3, minor/routine changes

- Fact-first. Put a number, diff, or hard fact in front when possible
- Short reaction. No explanation, no polite cushioning
- Noun-ending (体言止め) or abrupt cut preferred

---

## Medium

**Length:** 3-8 lines | **When:** Commit count 4-15, patterns worth exploring

- Opens with observation or data point
- Develops a single angle or reaction
- May include blank lines for rhythm (engine-dependent)
- No requirement to conclude or summarize

---

## Long

**Length:** 5-15 lines | **When:** Data-rich events, complex changes, reflections

- Can include data points, rhetorical questions, tangents
- Structure varies by engine's natural style
- No requirement for clean conclusion

---

## Long (Retro)

**Length:** 8-20 lines | **When:** Sprint/release summary, data-rich context

- Start with headline stats
- Mix genuine observations with reactions
- Engine decides its own structure and tone

---

## Crosstalk（掛け合い — 2形式）

### A. Single-Block Crosstalk

**Engines:** 2〜3 | **Length:** 5-20 lines | **When:** 短い掛け合い、テンポ重視

一つのテキストブロックとして生成。素早い応酬向き。

### B. Multi-Post Crosstalk

**Engines:** 2〜3 | **Posts:** 2-3投稿 | **When:** 変更内容が複数エンジンの視点を要求する時

**これが主要なクロストーク形式。** 変更内容の性質に基づいて自動発動する。

#### 発動条件

`references/theme-mapping.md` の **Crosstalk Trigger Matrix** を参照。

#### 生成フロー

```
1. Collect → git event のCrosstalk affinity を判定
2. Primary Engine を選出
3. Post 1 生成: Primary が git event に反応
4. Secondary Engine を選出
5. Post 2 生成: Secondary が git event + Post 1 に反応
6. [3エンジンの場合] Post 3 生成: Tertiary が全体を俯瞰
```

#### Post間のリアクションルール

| Post | 入力 | リアクション |
|------|------|------------|
| Post 1 | git event のみ | 通常投稿と同じ。次が来ることを意識しない |
| Post 2 | git event + Post 1 | Post 1 への直接反応（引用、反論、補足、無視のいずれか） |
| Post 3 | git event + Post 1-2 | 俯瞰、脱線、または沈黙。オチ役ではない |

#### 出力テンプレート

各Postは独立した投稿として出力。メタラインにスレッド番号を含む。

```
_[Multi-Post Crosstalk 1/2] — [Engine] — [Repository]_

[Post text]

_Source: [git data]_
```

#### 禁止事項

- **Post 1 を「振り」として書かない** — 次の投稿を意識した仕込みはAI臭い
- **毎回綺麗にオチをつけない** — Post 3 が必ず締める必要はない
- **全Post同じ温度にしない** — 温度差が人間らしさ
- **Post間で合意に至らない** — 結論が出ないのが自然

### 共通ルール（A/B両形式）

- **結論を出さない。** 途中で終わる、噛み合わない、無視する — すべて自然
- 引用は `>` で。Slack のスレッド返信風に
- 最後に発言するエンジンがオチを担当する必要はない

---

## Score

**Length:** 3-5 lines | **When:** 期間集計、1日の終わり、スプリント区切り

- 数値とスコアだけの淡白な形式
- 最後にひとこと（必須ではない）
- スコア項目は可変（その日の状況に合わせる）

---

## Quote Reply

**Length:** 4-10 lines | **When:** 直前の投稿内容にツッコミどころがある時

- 前の投稿（またはコミットメッセージ）を `>` で引用
- 引用に対してリアクション・ツッコミ・反論を展開

---

## Format Selection Matrix

| Scale | Default Format | Alternative | Condition |
|-------|---------------|-------------|-----------|
| 単一コミット (≤3) | Short | Score | 期間集計、数値が多い時 |
| 複数コミット (4-15) | Medium | Quote Reply | 直前の投稿にツッコミどころがある時 |
| スプリント/リリース | Long (Retro) | Long | 非Sprint文脈 |
| 議論が分かれるイベント | Crosstalk | — | Trigger Matrix 参照 |

### Auto-Selection

1. **Multi-Post Crosstalk 判定（最優先）:** git event を `theme-mapping.md` の Crosstalk Trigger Matrix と照合。High/Medium Affinity に一致すれば Multi-Post Crosstalk を選択
2. Determine engine (via engine selection algorithm) — Multi-Post 不発動時のみ
3. **Single-Block Crosstalk 判定:** 直前の投稿（rotation_log.md 参照）から3投稿以内なら、前のエンジンへの返信として Single-Block Crosstalk を候補にする（確率 ~20%）
4. Single event → shorter format; Multi-event/summary → longer format
5. Context: Time-sensitive → Medium; Data-rich → Long (Retro)/Score; Emotional → Medium/Long
6. **Quote Reply 判定:** 直前の投稿内容にツッコミどころがあれば Quote Reply を候補にする

---

## Output Templates

### Commit Reaction

```
_[Format] — [Engine] — [Repository]_

[Post text]

_Source: [Repository] commit [hash] "[message]" ([diff stats]) by @[author]_
```

### Period Summary

```
_[Format] — [Engine] — [Repository] — [Period]_

[Post text]

_Source: [Repository] [N] PRs merged ([breakdown]) [date range]_
```

### Crosstalk

```
_[Multi-Post Crosstalk N/M] — [Engine] — [Repository]_

[Post text]

_Source: [git data]_
```

### Score

```
_[Score] — [Engine] — [Repository]_

[Score content]

_Source: [Repository] [period] [stats]_
```
