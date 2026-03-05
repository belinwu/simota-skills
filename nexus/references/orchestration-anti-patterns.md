# Orchestration Anti-Patterns

> オーケストレーション設計の落とし穴、パターン選択ミス、過剰設計、ボトルネック、制御フロー障害

## 1. オーケストレーション設計 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **OA-01** | **早すぎるマルチエージェント化** | 単一エージェント＋ツールで十分な問題に複数エージェントを導入 | デバッグ困難、コスト爆発、レイテンシ増大 | まず単一エージェントで最適化、限界に達してから分割 |
| **OA-02** | **過剰オーケストレーション** | 決定的ワークフローにAIオーケストレーターを使用 | 不要なモデルコール、予測不能な動作 | 決定的フローは固定パイプライン、動的フローのみAI判断 |
| **OA-03** | **オーケストレーターボトルネック** | 全タスクが中央オーケストレーターを経由 | レイテンシスパイク、コンテキスト枯渇 | 階層化またはピアツーピアパターンで分散 |
| **OA-04** | **パターン不一致** | タスク特性を無視して同一パターンを適用 | 一部タスクで著しい性能低下 | タスク特性に応じたパターン選択（下表参照） |
| **OA-05** | **無限ループ** | 終了条件の未定義または到達不能 | コスト消費、システムハング、リソース枯渇 | 明示的終了条件 + イテレーション上限 + タイムアウト |
| **OA-06** | **コスト盲目** | モデルコールの累積コストを無視した設計 | 月次請求の急増、予算超過 | コスト監視 + 予算制限 + 安価モデルの階層的活用 |
| **OA-07** | **プロンプティングの誤謬** | 構造的な協調失敗をプロンプト改善で解決しようとする | 同じ失敗の繰り返し、プロンプト肥大化 | アーキテクチャ自体の見直し（構造問題は構造で解決） |

---

## 2. パターン選択の判断フレームワーク

```
パターン選択の 3 つの質問:

  Q1: ワークフローは決定的か動的か？
    決定的 → Sequential / Parallel / Iterative Refinement（AIオーケストレーター不要）
    動的   → Coordinator / Hierarchical / Swarm

  Q2: タスク間の依存関係は？
    独立   → Parallel（同時実行でレイテンシ削減）
    直列依存 → Sequential / Pipeline
    相互依存 → Coordinator / Swarm

  Q3: 品質要件はどの程度か？
    標準   → Single pass
    高品質  → Review & Critique / Iterative Refinement
    最高品質 → Swarm（ただし最高コスト）
```

| パターン | 最適な用途 | リスク | Nexus での対応 |
|----------|-----------|--------|---------------|
| **Sequential** | 構造的・反復的プロセス | ステップスキップ不可、累積レイテンシ | Pattern A |
| **Parallel** | 独立タスクの同時実行 | リソース競合、統合の複雑性 | Pattern B |
| **Coordinator** | 適応的ルーティング | ルーティングエラー、コスト増大 | CHAIN_SELECT |
| **Hierarchical** | 複雑な多段分解 | コンテキスト損失、デバッグ困難 | Multi-level chains |
| **Review & Critique** | 高精度要件 | レビューアーボトルネック、コスト蓄積 | Pattern F |
| **Swarm** | 創造的協調問題 | 合意不到達、極端なコスト | Rally 連携 |
| **ReAct** | 動的適応タスク | エラー伝播、無限推論ループ | 単一エージェント内 |

---

## 3. コスト最適化戦略

```
Plan-and-Execute パターン（推奨）:
  → 高性能モデルが戦略を策定
  → 安価なモデルが実行
  → フロンティアモデル全面使用比で 90% コスト削減

コスト階層設計:
  Tier 1（フロンティア）: 計画・複雑推論・オーケストレーション
  Tier 2（中間）: 標準タスク実行
  Tier 3（軽量）: 高頻度実行・ルーティング判断

  ❌ アンチパターン: 全エージェントにフロンティアモデル
  ❌ アンチパターン: コスト監視なしの本番デプロイ
  ✅ 推奨: リアルタイムコスト監視 + 閾値アラート
```

---

## 4. 制御フロー設計の原則

```
分散システムとしてのエージェント設計:
  1. 障害を前提とした設計（Design for Failure First）
  2. 全エージェント境界でのバリデーション
  3. アクション制約 → エージェント追加の順序
  4. 中間状態のログ記録
  5. リトライと部分失敗の想定
  6. チャットフローではなく分散システムとして扱う

  ❌ アンチパターン: エージェントを「会話」として設計
    → 実態は分散システム、状態管理が必須

  ❌ アンチパターン: 楽観的実行
    → 全ステップ成功を前提とした設計
    → 部分失敗時のリカバリパスが未定義

  ✅ 推奨: 各ステップに検証ゲート + フォールバック
```

---

## 5. Nexus との連携

```
Nexus での活用:
  1. CHAIN_SELECT フェーズで OA-01〜07 のスクリーニング
  2. パターン選択時に Q1-Q3 の判断フレームワーク適用
  3. コスト最適化戦略を EXECUTE フェーズに反映
  4. routing-learning.md の CES 評価にアンチパターン検出を統合

品質ゲート:
  - 単一エージェント＋ツールで解決可能 → マルチエージェント却下（OA-01 防止）
  - 決定的ワークフロー → 固定パイプライン使用（OA-02 防止）
  - 全ルートが Nexus 経由 → 階層化/分散の検討（OA-03 防止）
  - プロンプト改善 3 回以上 → アーキテクチャ見直し（OA-07 防止）
  - ループパターン → 終了条件＋上限必須（OA-05 防止）
```

**Source:** [Google Cloud: Choose a Design Pattern for Your Agentic AI System](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) · [Microsoft: AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) · [GitHub Blog: Multi-Agent Workflows](https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/) · [StackAI: 2026 Guide to Agentic Workflow Architectures](https://www.stackai.com/blog/the-2026-guide-to-agentic-workflow-architectures)
