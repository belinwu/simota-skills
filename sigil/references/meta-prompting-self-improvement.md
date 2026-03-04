# Meta-Prompting & Self-Improvement Patterns

> DSPy 最適化、TextGrad、Recursive Meta-Prompting、自己修正エージェント、Mistake Ledger、コンテキストエンジニアリング

## 1. プロンプト自動最適化フレームワーク

### DSPy（Declarative Self-improving Language Programs）

Stanford 発のプロンプト最適化フレームワーク。手動プロンプトエンジニアリングを**自動最適化**に置き換える。

| 要素 | 説明 |
|------|------|
| Signatures | 入出力の型定義（`question -> answer`） |
| Modules | プロンプトパターン（ChainOfThought, ReAct 等） |
| Optimizers | 自動プロンプト改善（BootstrapFewShot, MIPRO 等） |
| Metrics | 評価関数（正解率、品質スコア等） |

**成果**: 手動プロンプト 46.2% → DSPy 最適化 64.0%（+38% 改善）

**Sigil への適用可能性:**
- スキルの `description` を DSPy 的に自動最適化
- 生成されたスキルの効果を測定 → フィードバックループで改善
- ATTUNE フェーズでのスキル品質最適化に統合

### TextGrad（勾配ベースのテキスト最適化）

Nature 2025 掲載。テキストフィードバックを「勾配」として扱い、プロンプトを反復改善。

```
初期プロンプト → 実行 → 結果評価 → テキスト勾配（改善指示）→ プロンプト更新 → ...
```

**コア概念**: 数値勾配の代わりに自然言語フィードバックでプロンプトを最適化。

---

## 2. メタプロンプティングパターン

### Recursive Meta-Prompting

プロンプト自体を LLM に生成・改善させるパターン:

```
Level 0: タスク実行プロンプト
Level 1: タスク実行プロンプトを生成するプロンプト（メタプロンプト）
Level 2: メタプロンプトを改善するプロンプト
```

**実用的な適用**: Level 1 まで（Level 2 以上は収益逓減）。

### Skeleton-of-Thought (SoT)

回答の骨格を先に生成し、各セクションを並列に展開:

```
Step 1: 回答のアウトライン生成
Step 2: 各セクションを並列に詳細化
Step 3: 統合
```

**Sigil での活用**: スキル生成時に骨格（構造）→ 詳細（各セクション）の2段階生成。

---

## 3. 自己修正エージェントパターン

### Mistake Ledger パターン

過去の失敗を構造化して記録し、将来の生成品質を改善:

```markdown
## Mistake Ledger

| 日付 | 失敗パターン | 原因 | 修正策 | 再発防止ルール |
|------|------------|------|-------|-------------|
| 2025-01 | テストなしスキル生成 | 検証フェーズ省略 | VERIFY 必須化 | F1: テスト不在 |
| 2025-02 | 既存スキル重複 | SCAN 不十分 | dedup チェック強化 | F3: 重複 |
```

**効果**: 同じ失敗の再発率を大幅に低減（繰り返しパターンの排除）。

**Sigil での実装:**
- `skill-effectiveness.md` の ATTUNE フェーズに統合
- 生成失敗パターンを journal に蓄積
- 次回生成時に失敗パターンを回避

### Reflection パターン

生成後に自己レビューを実行:

```
Generate → Self-Review → Identify Issues → Regenerate
```

**3つのバリエーション:**

| バリエーション | 説明 | コスト |
|-------------|------|-------|
| Self-Refine | 同一モデルが生成→レビュー→修正 | 低 |
| Cross-Model | 異なるモデルがレビュー | 中 |
| Multi-Agent | 専用レビューエージェント | 高 |

**Sigil での適用**: VERIFY フェーズで Self-Refine を実行（12点ルーブリック適用）。

### Constitutional AI 的アプローチ

ルールセット（"憲法"）に基づいて出力を自己修正:

```
Principle 1: スキルは MUST プロジェクトの規約に従う
Principle 2: スキルは MUST NOT セキュリティリスクを導入する
Principle 3: スキルは SHOULD 10分以内で理解できる
```

---

## 4. コンテキストエンジニアリング

### Repomix（コードベースコンテキスト化）

リポジトリ全体を単一のコンテキストファイルに変換:

```bash
repomix --output context.txt
# → プロジェクト構造 + コード内容を単一ファイルに
```

**Sigil への示唆:**
- SCAN フェーズでの効率的なプロジェクト理解
- コンテキストサイズの見積もりと最適化
- 大規模プロジェクトでの選択的コンテキスト注入

### Addy Osmani の Spec-First ワークフロー

```
1. Spec 作成（仕様書を先に書く）
2. CLAUDE.md に規約を定義
3. AI に仕様 + 規約を注入
4. 生成 → レビュー → フィードバック
```

**Sigil への適用**: スキル生成前に「スキル仕様」を明確化するフェーズを追加。

### コンテキスト予算管理

| コンテキストウィンドウ | 推奨配分 |
|---------------------|---------|
| ~200K tokens | ルール: 5-10K, コード: 150-180K, 出力: 10-40K |
| ~1M tokens | ルール: 10-20K, コード: 800-900K, 出力: 80-100K |

**スキル生成への影響**: 生成するスキルが参照するコンテキスト量を最適化。大きすぎるスキルは分割。

---

## 5. 自動ルール生成パターン

### パターン1: コードから規約を抽出

```
既存コード → パターン分析 → ルール候補抽出 → 人間レビュー → CLAUDE.md 更新
```

**Sigil での実装**: SCAN → DISCOVER フェーズで暗黙の規約を検出し、スキル化。

### パターン2: 失敗から規約を生成

```
CI 失敗ログ → 失敗パターン分類 → 予防ルール生成 → スキル化
```

### パターン3: レビューコメントから規約を抽出

```
PR レビューコメント → 頻出指摘パターン → ルール化 → スキル/CLAUDE.md
```

---

## 6. 品質フィードバックループ

### 3段階フィードバック

```
Level 1: 構造的品質（フォーマット、必須フィールド）→ 自動検証
Level 2: 意味的品質（正確性、網羅性）→ Self-Refine
Level 3: 実用的品質（実際の使用効果）→ ATTUNE で長期追跡
```

### Sigil の既存フレームワークとの統合

| 既存フレームワーク | メタプロンプティング強化 |
|-----------------|---------------------|
| ATTUNE（OBSERVE→MEASURE→ADAPT→PERSIST） | + Mistake Ledger による失敗パターン回避 |
| 12点品質ルーブリック | + Self-Refine による自動改善 |
| skill-effectiveness 追跡 | + DSPy 的な定量最適化 |
| evolution-patterns | + 自動ルール生成パターン |

---

## 7. 実装ロードマップ（Sigil 向け）

### Phase 1: Mistake Ledger 導入（低コスト・高効果）

- 生成失敗パターンを journal に構造化記録
- CRAFT フェーズで過去の失敗を参照

### Phase 2: Self-Refine 統合（中コスト）

- VERIFY フェーズで自己レビューループを追加
- 12点ルーブリックを自動適用

### Phase 3: Description 最適化（中コスト）

- スキルの `description` 活性化率を追跡
- 低活性化スキルの description を自動改善提案

### Phase 4: コンテキスト最適化（高コスト）

- スキルのコンテキスト予算を計測・最適化
- 大規模スキルの自動分割提案

**Source:** [DSPy Documentation](https://dspy.ai/) · [TextGrad (Nature 2025)](https://www.nature.com/articles/s41586-025-08661-4) · [Repomix](https://github.com/yamadashy/repomix) · [Addy Osmani - AI Coding Workflow](https://addyosmani.com/blog/ai-coding-workflow/) · [Anthropic - Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) · [Mistake Ledger Pattern (Community)](https://simonwillison.net/2025/mistake-ledger/)
