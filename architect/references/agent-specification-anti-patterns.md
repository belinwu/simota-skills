# Agent Specification Anti-Patterns

> エージェント仕様設計の落とし穴、システムプロンプト設計ミス、ツール設計失敗、役割定義の罠

## 1. エージェント仕様設計 8 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **AS-01** | **タスク過負荷** | 単一エージェントに多数の異なるタスクを詰め込む | ハルシネーション増加、タスク漏れ、品質低下 | 1 エージェント 1 責務、責務が多い場合は分割 |
| **AS-02** | **曖昧な指示** | 解釈の余地がある指示を与える | 出力のばらつき、意図しない動作 | 具体的かつ明示的な指示、制約条件の明記 |
| **AS-03** | **安全策の欠如** | ガードレール・停止条件なしで自律動作させる | カスケードエラー、暴走実行 | 各ステップでバリデーション、max_iterations 設定 |
| **AS-04** | **ツール文書不足** | ツールの名前・説明・パラメータが不十分 | 誤ったツール選択、セマンティック不整合 | 例示付きの詳細なツール仕様、エッジケース明記 |
| **AS-05** | **生 API 露出** | REST API をそのままツールとして公開 | モデルが API の内部構造を理解できない | ビジネスタスク指向のツール設計（例: `POST /calendar/v1/events` → `Schedule Meeting`） |
| **AS-06** | **冗長プロンプト** | 2000+ ワードの過剰に詳細なプロンプト | 処理速度低下、注意力分散、遵守率低下 | 本質的指示のみ、詳細は references/ に分離 |
| **AS-07** | **コンテキスト不提供** | モデルが背景知識を持っていると仮定する | 不適切な推測、ドメインエラー | 必要な全コンテキストを明示的に提供 |
| **AS-08** | **静的プロンプト固着** | フィードバックループなしで初回プロンプトを維持 | 繰り返し同じ失敗、改善停滞 | 反復的改良サイクル、失敗パターンの分析と反映 |

---

## 2. システムプロンプト設計のベストプラクティス

```
効果的なシステムプロンプトの構造:

  1. 役割定義（Role）:
     ✅ "You are Architect - the creative meta-designer who..."
     ❌ "You are a helpful assistant"（汎用的すぎ）
     → 明確なペルソナ、専門領域、他エージェントとの差別化

  2. 知識ベース（Knowledge）:
     ✅ ドメイン固有の知識を構造化して提供
     ❌ モデルの事前知識に依存
     → RAG、references/、コンテキスト注入

  3. 応答ガイドライン（Response Guidelines）:
     ✅ フォーマット、トーン、制約を明示
     ❌ "適切に回答してください"
     → 出力形式、禁止事項、品質基準を具体的に

  4. タスク定義（Task Definition）:
     ✅ 段階的なワークフロー定義
     ❌ "タスクを完了してください"
     → フェーズ分離、チェックポイント、成功基準

  5. 制約事項（Constraints）:
     ✅ Always / Ask first / Never の 3 層
     ❌ 制約なし or 過剰制約
     → 自律性と安全性のバランス

Ma/間 の適用:
  - Primacy（最初の 15%）: 最も重要な役割定義と原則
  - Recency（最後の 15%）: 記憶に残る行動指針
  - Middle Sag（中間 70%）: 構造化で注意力低下を補償
```

---

## 3. ツール設計の原則

```
ACI（Agent-Computer Interface）Excellence:

  設計原則（Anthropic 推奨）:

  1. 明確性（Clarity）:
     → 「モデルの立場に立って考える」
     → ツールの使い方が一目でわかるか？
     → 例示、エッジケース、使用範囲を含める

  2. フォーマット選択:
     → モデルが「自然に見たことのある」形式に近づける
     → 十分なトークンで思考する余地を残す
     → 行番号カウントや文字列エスケープなどの摩擦を排除

  3. ポカヨケ:
     → ミスを「困難にする」引数設計
     → 曖昧なパラメータ名の排除
     → デフォルト値の適切な設定

  4. 反復テスト:
     → 多数の入力例でテスト
     → モデルがどんなミスをするか観察
     → ミスパターンに基づいてツール仕様を改善

ツール設計アンチパターン:

  ❌ 類似名ツール:
    schedule_meeting と create_meeting が共存
    → セマンティック不整合でモデルが混乱

  ❌ 過剰なツール数:
    50+ ツールを単一エージェントに提供
    → 選択精度低下、意図しないツール使用
    → 10-15 ツール以下に制限、または段階的ロード

  ❌ 未検証ツール出力:
    ツール結果をそのまま次のステップに使用
    → 不正データの伝播、カスケードエラー
    → ツール出力のバリデーション必須化
```

---

## 4. 役割定義の設計パターン

```
効果的な役割定義の要素:

  1. アイデンティティ:
     → 名前 + メタファー（"Motion creates emotion"）
     → 原則（3-5 個、記憶可能な量）
     → 他エージェントとの差別化ポイント

  2. 境界（Boundaries）:
     3 層構造が最も効果的:
     - Always: 自律的に実行すべきこと
     - Ask first: 確認が必要なこと
     - Never: 絶対にしないこと

  3. 能力の公開範囲:
     → CAPABILITIES_SUMMARY: ルーティング用（外部可視）
     → references/: 詳細知識（内部参照）
     → 全てを SKILL.md に詰め込まない

  4. 協調パターン:
     → INPUT/OUTPUT パートナーの明示
     → ハンドオフテンプレートの定義
     → 逆フィードバック経路の確保

役割定義アンチパターン:

  ❌ God Agent:
    1 つのエージェントが全責務を担う
    → 専門性の欠如、品質低下、スケール不能

  ❌ Phantom Agent:
    定義はあるが実際に使用されない
    → エコシステムの肥大化、メンテ負荷

  ❌ Clone Agent:
    既存エージェントとの重複が 30%+
    → 混乱、ルーティング曖昧性

  ❌ Orphan Agent:
    INPUT/OUTPUT パートナーが未定義
    → エコシステムから孤立、活用されない
```

---

## 5. 計画と実行の分離

```
Dual-Mode Architecture（推奨パターン）:

  Plan Mode（計画フェーズ）:
    - コンテキスト収集
    - 要件の明確化
    - アプローチの設計
    - ユーザー確認
    → 読み取り専用ツールのみ

  Act Mode（実行フェーズ）:
    - ステップバイステップ実行
    - 各ステップ後の検証
    - 問題発生時の適応
    → 全ツールアクセス

  ❌ アンチパターン: 計画なき実行
    → 前提の誤りが後工程で発覚
    → 手戻りコスト大

  ❌ アンチパターン: 過剰な計画
    → 実行前に全てを予測しようとする
    → 分析麻痺（analysis paralysis）

  ✅ 推奨: 計画 → 承認 → 実行 → 検証のサイクル
    → Architect のフレームワーク:
      UNDERSTAND → ENVISION → ANALYZE → DESIGN → GENERATE → VALIDATE
```

---

## 6. Architect との連携

```
Architect での活用:
  1. DESIGN フェーズで AS-01〜08 のスクリーニング
  2. SKILL.md 生成時にシステムプロンプト構造を検証
  3. ツール定義を含むエージェントは ACI 原則を適用
  4. 役割定義で God/Phantom/Clone/Orphan をチェック

品質ゲート:
  - 責務 3+ 個の CAPABILITIES → 分割を検討（AS-01 防止）
  - Always/Ask first/Never 未定義 → 3 層境界必須化（AS-03 防止）
  - references/ なし → 詳細を分離（AS-06 防止）
  - INPUT/OUTPUT パートナーなし → 協調パターン定義必須（Orphan 防止）
  - 既存エージェントと重複 30%+ → 差別化または統合（Clone 防止）
  - 使用実績なし → 削除を検討（Phantom 防止）
```

**Source:** [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) · [PromptHub: Prompt Engineering for AI Agents](https://www.prompthub.us/blog/prompt-engineering-for-ai-agents) · [Patronus AI: AI Agent Architecture](https://www.patronus.ai/ai-agent-development/ai-agent-architecture) · [Glaforge: AI Agentic Patterns and Anti-Patterns](https://glaforge.dev/talks/2025/12/02/ai-agentic-patterns-and-anti-patterns/)
