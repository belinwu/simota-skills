# Engine Reference

Three AI engines generate developer grumble posts. Each engine speaks in its own natural voice.
**No character definitions, no personality scripts — the engine's ego IS the voice.**

---

## Engine Dispatch Table

| Engine | CLI Command | Fallback |
|--------|-------------|----------|
| Codex  | `codex exec --full-auto` | Claude subagent |
| Gemini | `gemini -p --yolo`       | Claude subagent |
| Claude | Claude subagent (Task tool) | — |

---

## Authenticity Principle

**唯一のルール: 人間が書いたように見えること。**

AIが書いた文章は「整いすぎている」ことで見抜かれる。口調、文体、構成、長さ、感情表現 — これらの「どう人間らしくするか」はエンジン自身に委ねる。Bard側からの定義・指示はしない。

エンジンに伝えるのは:
- **人間のSlack投稿であること** — AI生成テキストではなく、実在の開発者の投稿に見えること
- **git データ** — 事実に基づくこと
- **フォーマット（長さの目安）** — Short/Medium/Long

それ以外（口調、文末表現、構成パターン、感情の出し方）はエンジンの自然な判断に任せる。

---

## Engine Selection Algorithm

1. `rotation_log.md` を読み、直前のエンジンを確認
2. 直前と同じエンジンを避ける（連続禁止）
3. 利用可能なエンジンから均等ランダム選択
4. `which codex` / `which gemini` で可用性チェック。unavailable → 候補除外
5. ユーザー指定は即採用
6. 7日以上未使用のエンジンに ×1.5 の重み

---

## Engine Prompt Template

エンジンに渡す最小プロンプト。**性格・口調・文体の指示は一切含めない。**

```markdown
# Task
以下のgitデータについて、開発者のSlack投稿を日本語で1つ書いてください。
人間が書いた投稿に見えること。投稿テキストのみ出力（説明・前置き不要）。

## Git Data
[commit/PR data]

## Repository
[repo name]

## Format
[Short (1-3行) / Medium (3-8行) / Long (5-15行)]

## Topic Hint (optional)
[saturation tracker からの回避ヒント]
```

### Fallback Behavior

Codex/Gemini unavailable → Claude subagent で生成。
- メタラインに `(fallback)` を明記: `_[Format] — Claude (fallback) — [Repository]_`
- **「Codex のふりをしろ」「Gemini 風に」とは絶対に言わない** — Claude が Claude として書く
