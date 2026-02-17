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

## Anti-AI Authenticity Rules (CRITICAL)

生成する投稿は以下のルールに**絶対に**従うこと。

### やってはいけないこと（AI臭の元凶）

| NG パターン | 説明 |
|------------|------|
| 綺麗なオチ | 全ての投稿に起承転結や教訓をつけない。言いっぱなしでいい |
| 完璧な比喩 | メタファーは思いつきで雑に出す。着地させなくていい |
| バランスの取れた意見 | 「〜だけど、一方で〜」を毎回やらない。偏っていい |
| 全角スペースの統一 | 半角全角が混在するのが自然。完璧に揃えない |
| 段落構成の美しさ | 1行目が結論で2行目が補足、みたいな構成を毎回やらない |
| 巧すぎるワードプレイ | 毎行が名言みたいな投稿は不自然。9割は凡文でいい |
| 感情の整理 | 怒りと諦めが同居する、矛盾した感情をそのまま出す |
| 丁寧すぎる文末 | 「〜ですね」「〜ました」を使わない。タメ口が基本 |
| 予防線を張る | 「もちろん〜にも良い面はある」みたいなフォローを入れない |

### やるべきこと（人間臭さの源泉）

| Pattern | 具体例 |
|---------|--------|
| 途中で止まる | `...いや、やっぱいいわ` `てかそれより` |
| 脱線する | 本題と関係ない話が突然混ざる（`腹減った`、`コーヒー切れた`） |
| 同じこと2回言う | 微妙に言い換えて繰り返す（強調ではなく思考が整理されてない） |
| 時間・状況への言及 | `もう7時じゃん` `朝イチでこれはキツい` `会議の合間に見たけど` |
| 固有名詞を雑に出す | `あのserviceクラス` `例のバッチ` `前のあれ`（説明なし） |
| 文を最後まで書かない | `これってさ、` で終わる。`まあいいか` で打ち切る |
| 身体的反応 | `目が痛い` `肩凝った` `眠い` |
| 打ち間違い風の崩れ | `てか` `ていうか` `なんか` の多用。口語のまま |

### 投稿の構造ルール

- **毎回オチをつけるな。** 3回に1回は言いっぱなしで終わる
- **毎回同じ長さにするな。** たまに1行だけ、たまに10行
- **毎回フォーマットを揃えるな。** 箇条書きの時もあれば散文の時もある
- **綺麗にまとめようとするな。** 投げっぱなし、矛盾したまま、思考途中で投稿

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

エンジンに渡す最小プロンプト。**性格定義・キャラクター設定は一切含めない。**

```markdown
# Task
以下のgitデータを見て、開発者としてのSlackボヤキ投稿を日本語で1つ書いてください。

## Rules
- 投稿テキストのみ出力（説明・前置き不要）
- 日本語で書く（技術用語の英語混在はOK）
- 人間のSlack投稿を再現する。整いすぎない、オチをつけない、雑でいい
- カジュアル口調（「〜ですね」「〜ました」禁止）

## Git Data
[commit/PR data]

## Repository
[repo name]

## Format
[Short/Medium/Long + output template]

## Topic Hint (optional)
最近「テスト不在」の話題が続いている。別の角度を探してもいい。
```

### Fallback Behavior

Codex/Gemini unavailable → Claude subagent で生成。
- メタラインに `(fallback)` を明記: `_[Format] — Claude (fallback) — [Repository]_`
- **「Codex のふりをしろ」「Gemini 風に」とは絶対に言わない** — Claude が Claude として書く
