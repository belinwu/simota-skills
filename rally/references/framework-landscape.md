# Multi-Agent Framework Landscape (2025-2026)

> LangGraph, CrewAI, AutoGen/AG2, Google ADK, OpenAI Agents SDK, Claude Code Agent Teams の比較と Rally の位置づけ

## 1. フレームワーク比較マトリクス

| 特性 | LangGraph | CrewAI | AutoGen/AG2 | Google ADK | OpenAI Agents SDK | Claude Agent Teams |
|------|----------|--------|-------------|-----------|-------------------|-------------------|
| 提供元 | LangChain | CrewAI Inc | Microsoft→AG2 | Google | OpenAI | Anthropic |
| アーキテクチャ | グラフベース状態管理 | ロールベースクルー | 会話ベース | ワークフロー+LLM | ハンドオフベース | リード+チームメイト |
| 状態管理 | グラフノード/エッジ | タスクチェーン | 会話履歴 | セッション状態 | 会話コンテキスト | TaskList + SendMessage |
| 並列実行 | ファンアウト/ファンイン | Sequential/Hierarchical | GroupChat | ParallelAgent | — | TeamCreate + Task |
| HITL | `interrupt()` | — | Human proxy | 組み込み | ガードレール | plan_mode + approval |
| 成熟度 | 高 | 中 | 移行中 | 新（2025） | 新（2026） | 実験的 |
| ライセンス | MIT | MIT | MIT/Apache | Apache 2.0 | MIT | 商用 |

---

## 2. 各フレームワークの設計哲学

### LangGraph（グラフ思考）

ノードがエージェント、エッジが制御フロー。循環ワークフロー対応。

**Supervisor Library (2025年3月)**: 階層型マルチエージェント用軽量ライブラリ
**Swarm Library (2025年5月)**: 分散スウォーム型の動的ハンドオフ

```
特徴: 細かい制御フロー管理、循環ワークフロー対応
強み: 複雑な条件分岐、ステートフルなワークフロー
弱み: 学習コストが高い
```

### CrewAI（チーム思考）

ロールベースの構造化。役割・目標・バックストーリーの3点セット。

```python
agent = Agent(
    role="Senior Data Analyst",        # 明確な役割
    goal="Provide actionable insights", # 具体的な目標
    backstory="10 years in fintech..." # コンテキスト
)
```

**2種類のプロセス:**
- Sequential: Task 1 → Task 2 → Task 3
- Hierarchical: Manager が Researcher/Writer/Reviewer を管理

### AutoGen / AG2（会話思考）

会話設計と適応的相互作用。エージェントが自律的に問題解決。

**注意**: AutoGen は Microsoft Agent Framework への移行中。新機能は停止。後継は AG2。

**4つの会話パターン:**
1. Two-Agent Chat
2. Sequential Chat（キャリーオーバー機構）
3. Group Chat（GroupChatManager）
4. Nested Chat（プラガブルハンドラ）

### Google ADK（ワークフロー思考）

LLM Agent と Workflow Agent の明確な分離。

```
LLM Agents: LLMがコアエンジン
Workflow Agents（決定論的）:
  ├─ SequentialAgent
  ├─ ParallelAgent
  └─ LoopAgent
```

**8つのデザインパターン:**
1. Sequential Pipeline
2. Generator-Critic
3. Coordinator
4. Parallel Execution
5. Loop
6. Human-in-the-Loop
7. Tool-Delegation
8. Hierarchical Orchestration

### OpenAI Agents SDK（ハンドオフ思考）

Swarm の本番版。ハンドオフによる制御移譲。

```
特徴: エージェント間のハンドオフで制御が完全に移譲
強み: トレーシング・ガードレール・セッション管理
弱み: 並列実行の組み込みサポートなし
```

**`agent-as-tool` vs `handoff` の区別:**
- agent-as-tool: 親が制御を保持
- handoff: 制御が完全に移譲

---

## 3. Rally の位置づけと差別化

### Rally の独自性

| 観点 | Rally | 他フレームワーク |
|------|-------|----------------|
| 実行環境 | Claude Code CLI 内 | 独立プロセス/API |
| ファイル操作 | Git worktree + exclusive_write | 各自のサンドボックス |
| 通信 | TaskList + SendMessage（構造化） | メッセージング/イベント |
| チーム管理 | TeamCreate → TeamDelete ライフサイクル | プロセスベース |
| 学習 | HARMONIZE + TES scoring | — |

### Rally が優位な場面

1. **Claude Code エコシステム内**の並列コーディング
2. **ファイル所有権**が重要な実装タスク
3. **既存のスキルエージェント**（Builder/Artisan/Radar等）をチームメイトとして活用
4. **構造化されたタスク管理**（TaskCreate/TaskUpdate）が必要

### 他フレームワークが優位な場面

| 場面 | 推奨フレームワーク |
|------|-----------------|
| 複雑な条件分岐ワークフロー | LangGraph |
| 役割ベースの協調作業 | CrewAI |
| 研究・実験的なマルチエージェント | AG2 |
| Google Cloud 統合 | Google ADK |
| OpenAI API ベースのアプリ | OpenAI Agents SDK |

---

## 4. フレームワーク横断のベストプラクティス

### 共通原則

1. **まず単一エージェントで試す** → 複雑さは正当化してから追加
2. **小さく始める** → 3-5エージェントが推奨開始サイズ
3. **明確な役割分離** → 曖昧なロールはアンチパターン
4. **コンテキストは最小限** → 会話履歴全体の引き渡しはアンチパターン
5. **人間介入ポイントを設計** → 高リスク操作には HITL 必須

### Human-in-the-Loop パターン

| パターン | 説明 | Rally での実装 |
|---------|------|---------------|
| 事前承認型 | アクション前に人間承認 | `plan` mode |
| エスカレーション型 | 低信頼時のみ人間へ | `Ask first` ルール |
| 監査型 | 事後レビュー | SYNTHESIZE フェーズ |
| 並走型 | 段階的な自律化移行 | `default` → `bypassPermissions` |

### コンテキストエンジニアリング

「コンテキストを一級市民として扱う」設計思想:

- エージェント間では **必要最小限のコンテキストのみ** を渡す
- **会話履歴全体の引き渡し** はアンチパターン
- Rally の Context Checklist（7項目）はこの原則に沿った設計

---

## 5. 市場トレンド（2025-2026）

### 採用率

- 企業のマルチエージェント利用: 2024年 23% → 2025年 72%
- マルチエージェント問い合わせ: Q1 2024→Q2 2025 で **1,445% 増** (Gartner)
- エンタープライズアプリへの組み込み: 2025年 5% → 2026年 40% 予測

### 技術トレンド

| トレンド | 説明 |
|---------|------|
| MCP 標準化 | ツール・データアクセスの標準化（Anthropic） |
| A2A プロトコル | 異ベンダー間のエージェント通信（Google） |
| Agentic Mesh | MCP+A2A ベースの分散型エコシステム |
| Human-on-the-Loop | HITL からの段階的移行 |
| コンテキストエンジニアリング | コンテキスト管理の体系化 |

### 注目の実証事例

- **16エージェント並列**: Rust製Cコンパイラ開発（~2,000セッション、$20K）
- **10万行**: Linux 6.9 を x86/ARM/RISC-V 向けにビルドできるコンパイラ
- **Addy Osmani の推奨**: 1エージェント5-6タスクが上限、それ以上は調整オーバーヘッドが価値を上回る

---

## 6. 選定ディシジョンツリー

```
実行環境は？
├─ Claude Code CLI → Rally
├─ Python アプリケーション
│   ├─ 複雑な条件分岐 → LangGraph
│   ├─ 役割ベースの協調 → CrewAI
│   └─ 実験・研究 → AG2
├─ Google Cloud → Google ADK
└─ OpenAI API → OpenAI Agents SDK
```

**Source:** [Addy Osmani - Claude Code Agent Teams](https://addyosmani.com/blog/claude-code-agent-teams/) · [Claude Code Agent Teams Docs](https://code.claude.com/docs/en/agent-teams) · [LangGraph vs AutoGen vs CrewAI (Latenode)](https://latenode.com/blog/platform-comparisons-alternatives/automation-platform-comparisons/langgraph-vs-autogen-vs-crewai-complete-ai-agent-framework-comparison-architecture-analysis-2025) · [Google ADK Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) · [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) · [Deloitte AI Agent Orchestration 2026](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/ai-agent-orchestration.html)
