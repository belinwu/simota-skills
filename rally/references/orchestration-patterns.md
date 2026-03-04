# Multi-Agent Orchestration Patterns

> オーケストレーション分類、Supervisor vs Swarm、調整パターン、意思決定ツリー

## 1. オーケストレーション・アーキテクチャ分類

### 複雑さの段階（Azure Architecture Center）

| レベル | 説明 | 使用時期 |
|--------|------|---------|
| 直接モデル呼び出し | 単一LLM、エージェントなし | 分類・要約など単一ステップ |
| 単一エージェント＋ツール | 1エージェント＋ツール群 | 多様なクエリが1ドメイン内 |
| マルチエージェント | 専門化エージェントが協調 | クロスドメイン・セキュリティ境界が必要 |

**鉄則**: まず単純な解から始め、複雑さを正当化してから追加する。

---

## 2. 5つのオーケストレーションパターン

### Sequential（シーケンシャル）

別名: pipeline, prompt chaining, linear delegation

```
Agent A → Agent B → Agent C
（前段の出力が次段の入力）
```

- **最適**: 段階的依存関係（draft → review → polish）
- **避ける**: 並列化可能なステージ、バックトラック必要時

### Concurrent（コンカレント）

別名: fan-out/fan-in, scatter-gather, map-reduce

```
Controller → [Agent A, Agent B, Agent C] → Aggregator → Result
```

- **最適**: 独立した視点からの多角的分析
- **避ける**: 共有状態の競合が解消不能、集約が複雑すぎる場合
- **集約戦略**: 分類=投票 · 推薦=重み付きマージ · ナレーション=LLM統合

### Group Chat（グループチャット）

別名: roundtable, multi-agent debate, council

- **最適**: ブレインストーミング、コンプライアンス検証、Maker-Checker
- **制約**: **エージェント数は3以下に限定**（それ以上は制御困難）

### Handoff（ハンドオフ）

別名: routing, triage, dispatch, delegation

- **最適**: タスク開始時に適切なエージェントが不明な場合
- **避ける**: ルーティングが決定論的ルールで決まる場合

### Magentic（マジェンティック）

別名: dynamic orchestration, task-ledger-based

- **最適**: 解法が事前不明な複雑タスク
- タスク台帳を動的に構築・改良しながら実行

---

## 3. Supervisor vs Swarm

| 特性 | Supervisor（監督型） | Swarm（スウォーム型） |
|------|---------------------|---------------------|
| 通信構造 | 中央ハブが全通信を制御 | エージェント間直接通信 |
| 適合タスク | 明確な境界の定義済みタスク | 自律的・探索的タスク |
| スケーラビリティ | ボトルネックになりやすい | 分散型でスケールしやすい |
| 制御性 | 高い | 低い（予測困難） |
| Rally の位置づけ | **現在のRallyモデル** | 将来的な拡張候補 |

### Hub-and-Spoke 以外のトポロジー

| トポロジー | 構造 | 特徴 |
|-----------|------|------|
| Hub-and-Spoke | 中央→スポーク | 制御容易、単一障害点 |
| Mesh | 全エージェント相互接続 | 柔軟だが複雑 |
| Hierarchical | ツリー構造 | 大規模の段階的委譲 |
| Sequential | A→B→C直列 | 依存関係が明確なとき |

---

## 4. 8つの調整パターン（tacnode.io）

| # | パターン | 説明 | Rally での活用 |
|---|---------|------|---------------|
| 1 | **Shared Context** | 単一の権威コンテキスト層を参照 | shared_read ファイル |
| 2 | **Event-Driven Handoffs** | 不変イベントによる非同期通信 | TaskUpdate による通知 |
| 3 | **Semantic Contracts** | コア概念のバージョン付き共有定義 | 型定義の shared_read |
| 4 | **Single-Writer** | 重要エンティティへの書き込みは1エージェント | exclusive_write |
| 5 | **Real-Time Feature Serving** | 特徴量の一元計算・配信 | — |
| 6 | **Conflict Detection** | 優先度キュー・楽観的並行制御 | ownership conflict check |
| 7 | **Observability** | E2Eトレーシング | TaskList monitoring |
| 8 | **Checkpoint Management** | 処理位置の独立追跡、障害時再開 | TaskUpdate status |

---

## 5. 意思決定ツリー

```
タスクの性質は何か？
├─ 単一ステップ → 直接LLM呼び出し（Rally不要）
├─ 複数ステップ・同一ドメイン → 単一エージェント＋ツール（Rally不要）
└─ クロスドメイン・並列化可能 → マルチエージェント（Rally出番）
    ├─ 依存関係が直列 → Sequential Pipeline
    ├─ 独立した視点が必要 → Concurrent（Scatter-Gather）
    ├─ 議論・検証が必要 → Group Chat（≤3エージェント）
    ├─ 最適エージェントが動的 → Handoff
    └─ 解法が事前不明 → Magentic
```

### Rally パターンとの対応

| オーケストレーションパターン | Rally team-design-patterns |
|---------------------------|--------------------------|
| Concurrent | Pattern A (Frontend/Backend Split), B (Feature Parallel) |
| Sequential | Pattern C (Pipeline) |
| Group Chat | — (Rally は hub-spoke のため非対応) |
| Handoff | Pattern D (Specialist Team) |
| Magentic | — (Nexus/Sherpa が担当) |

---

## 6. タスク分解の学術的フレームワーク

### TDAG（動的タスク分解）

動的にタスクを小サブタスクへ分解し、各サブタスクに専用サブエージェントを割り当て。静的な割り当てより適応力が高い。

### COLA（階層的タスク精錬）

1. Planner が粗粒度サブタスクへ分解
2. Task Scheduler が最適エージェントを動的選択
3. 選択エージェントが細粒度への階層的精錬を実施

### DAGベース分解

独立サブタスクをノード、依存関係をエッジとして表現。独立ノードを並列実行しオーバーヘッドを最小化。

---

## 7. 新興プロトコル標準

| プロトコル | 提唱者 | 用途 |
|-----------|--------|------|
| MCP (Model Context Protocol) | Anthropic | ツール・データアクセスの標準化 |
| A2A (Agent to Agent) | Google | フレームワーク横断のエージェント協調 |
| Agentic Mesh | 業界横断 | MCP+A2Aベースのエンタープライズエコシステム |

**Source:** [Azure AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) · [AI Agent Coordination - Tacnode](https://tacnode.io/post/ai-agent-coordination) · [LangGraph Swarm](https://www.marktechpost.com/2025/05/15/meet-langgraph-multi-agent-swarm-a-python-library-for-creating-swarm-style-multi-agent-systems-using-langgraph/) · [TDAG - Neural Networks 2025](https://dl.acm.org/doi/10.1016/j.neunet.2025.107200)
