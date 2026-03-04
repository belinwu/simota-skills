# Claude Code Skills API Reference

> SKILL.md フロントマター仕様、動的コンテキスト注入、引数パッシング、スキル配置優先度、description 最適化

## 1. フロントマター完全仕様

### 必須フィールド

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `name` | string | スキル表示名（ルーティングに使用） |
| `description` | string | スキルの説明（AI ルーティング判定に最重要） |

### オプションフィールド

| フィールド | 型 | デフォルト | 説明 |
|-----------|-----|----------|------|
| `user-invocable` | boolean | false | `/skill-name` でユーザーが直接呼び出し可能 |
| `allowed-tools` | string[] | all | スキル内で使用可能なツールを制限 |
| `disable-model-invocation` | boolean | false | LLM呼び出しなしでプロンプトを直接展開 |
| `model` | string | — | 使用モデルを指定（`sonnet`, `opus`, `haiku`） |
| `agent` | boolean | false | バックグラウンドエージェントとして起動 |
| `argument-hint` | string | — | 引数のプレースホルダー表示（`"<URL>"` 等） |
| `context` | string | — | コンテキスト管理（`fork` で分離コンテキスト） |

### フロントマター例

```yaml
---
name: deploy
description: 本番環境へのデプロイメント手順を実行する
user-invocable: true
argument-hint: "<environment>"
allowed-tools:
  - Bash
  - Read
  - Glob
---
```

---

## 2. 動的コンテキスト注入

### `!`command`` 構文

SKILL.md 内でシェルコマンドの出力を動的に注入:

```markdown
現在のブランチ: !`git branch --show-current`
最新コミット: !`git log --oneline -5`
パッケージ情報: !`cat package.json | jq '.dependencies'`
```

**実行タイミング**: スキル読み込み時に即座に実行され、結果がプロンプトに挿入。

**注意点:**
- 重い処理はスキル起動を遅延させる
- 失敗時はエラーメッセージが挿入される
- セキュリティ上、信頼できるコマンドのみ使用

### 引数パッシング

| 変数 | 説明 |
|------|------|
| `$ARGUMENTS` | ユーザーが渡した全引数（文字列） |
| `$0` | スキル名 |
| `$1`, `$2`, ... | 位置引数 |

```markdown
---
name: review-pr
user-invocable: true
argument-hint: "<PR番号>"
---

PR #$1 をレビューしてください。
!`gh pr view $1 --json title,body,files`
```

---

## 3. スキル配置と優先度

### 配置場所（優先度順）

| 優先度 | 場所 | スコープ |
|--------|------|---------|
| 1（最高） | Enterprise Policy | 組織全体（管理者設定） |
| 2 | `~/.claude/skills/` | ユーザー個人（全プロジェクト共有） |
| 3 | `.claude/skills/` | プロジェクト固有 |
| 4 | Plugin/Extension | プラグイン提供 |

**衝突解決**: 同名スキルは高優先度が勝つ。

### ディレクトリ構造

```
.claude/skills/
├── my-skill/
│   ├── SKILL.md          # メインプロンプト
│   └── references/       # 参照ドキュメント
│       ├── patterns.md
│       └── examples.md
└── simple-skill.md       # 単一ファイル（Micro Skill）
```

---

## 4. description 最適化

### 重要性

`description` はスキルのルーティング判定に**最も影響する**フィールド。Claude が「このスキルを使うべきか」を判断する際の主要な手がかり。

### 最適化パターン

| パターン | 例 | 効果 |
|---------|-----|------|
| **トリガーワード列挙** | 「バグ調査、根本原因分析、再現手順の特定」 | 発火率向上 |
| **否定条件の明示** | 「コードは書かない。修正はBuilderに委譲」 | 誤発火防止 |
| **使用タイミングの明示** | 「〜が必要な時に使用」 | コンテキスト判断精度向上 |
| **他スキルとの差別化** | 「Sentinelの静的分析を補完」 | ルーティング衝突回避 |

### アンチパターン

| アンチパターン | 問題 |
|-------------|------|
| 「汎用的なヘルパー」 | 曖昧すぎて発火しない |
| 過度に長い説明（5行以上） | ノイズが増え判定精度低下 |
| 技術用語のみ | ユーザーの自然言語と乖離 |
| 他スキルと類似した表現 | ルーティング衝突 |

### 実績データ

- **活性化率の改善事例**: description を「汎用ヘルパー」→ トリガーワード列挙 + 使用タイミング明示に変更で **20% → 84%** に向上（フック付き）
- **最適な長さ**: 1-3文、50-150文字が最も効果的

---

## 5. context: fork

`context: fork` を設定すると、スキル実行時に**分離されたコンテキスト**で動作:

- 親会話のコンテキストを汚染しない
- 長時間実行タスクに適する
- `agent: true` と組み合わせてバックグラウンド実行

```yaml
---
name: long-analysis
description: 大規模コードベースの分析
context: fork
agent: true
---
```

---

## 6. allowed-tools によるサンドボックス

スキルの安全性を確保するためにツールアクセスを制限:

```yaml
# 読み取り専用スキル
allowed-tools:
  - Read
  - Glob
  - Grep

# 実行可能だが編集不可
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash

# 完全アクセス（デフォルト）
# allowed-tools を省略
```

**Sigil での活用**: 生成するスキルの安全性レベルに応じて `allowed-tools` を設定。調査系スキルは読み取り専用、実装系スキルはフルアクセス。

---

## 7. disable-model-invocation

`disable-model-invocation: true` に設定すると、SKILL.md の内容が**LLM を経由せず直接展開**される:

- テンプレート的なプロンプト注入に使用
- 動的コンテキスト（`!`command``）は引き続き実行される
- コスト削減・レイテンシ削減に有効

**ユースケース**: プロジェクト規約の注入、定型的なチェックリスト展開

**Source:** [Claude Code Skills Documentation](https://docs.anthropic.com/en/docs/claude-code/skills) · [Claude Code Custom Slash Commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands) · [Anthropic Cookbook - Skills](https://github.com/anthropics/anthropic-cookbook/tree/main/misc/prompt_caching)
