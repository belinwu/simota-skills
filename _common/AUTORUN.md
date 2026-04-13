# AUTORUN Protocol

This document defines the platform-agnostic automatic execution protocol for Nexus orchestration.

---

## Overview

AUTORUN mode enables Nexus to execute agent chains automatically without manual copy-paste handoffs.
This protocol works across different AI platforms (Claude Code, Codex CLI, Gemini, etc.).

---

## Execution Modes

| Mode | Trigger | Behavior | Platform |
|------|---------|----------|----------|
| AUTORUN_FULL | `## NEXUS_AUTORUN_FULL` | Execute all steps including COMPLEX tasks | All |
| AUTORUN | `## NEXUS_AUTORUN` | Execute SIMPLE tasks only | All |
| GUIDED | `## NEXUS_GUIDED` | Manual agent invocation | All |
| INTERACTIVE | `## NEXUS_INTERACTIVE` | Confirm each step | All |

---

## Agent Spawn Execution

In AUTORUN mode, Nexus spawns each agent as an independent Claude session via the Agent tool:

```
## Nexus Execution: [Goal]
- Chain: Agent1 → Agent2 → Agent3
- Mode: AUTORUN_FULL

### Spawning Step [X/Y]: [AgentName]

Agent(
  name: "[agent-name]-[task-slug]"
  description: "[Short task description]"
  subagent_type: general-purpose
  mode: bypassPermissions
  model: [sonnet|opus|haiku]
  prompt: |
    あなたは [AgentName] エージェントです。
    まず ~/.claude/skills/[agent-name]/SKILL.md を読み、その指示に従ってください。

    タスク: [task_description]
    前ステップからのコンテキスト: [handoff_context]
    制約: [constraints]

    完了時、以下のフォーマットで結果を出力してください:
    _STEP_COMPLETE:
      Agent: [AgentName]
      Status: SUCCESS | PARTIAL | BLOCKED | FAILED
      Output: [成果物]
      Next: [推奨次エージェント or DONE]
)
```

### Execution Layers

#### Claude Code

| Layer | Method | When | API |
|-------|--------|------|-----|
| **L1: Direct Spawn** | Agent tool (foreground) | 1-4 step sequential chains | `Agent(prompt, mode)` |
| **L2: Parallel Spawn** | Agent tool (background) | 2-3 independent branches | `Agent(prompt, run_in_background: true)` |
| **L3: Rally Delegation** | Spawn Rally as Agent | 4+ workers, complex ownership | `Agent(prompt="You are Rally...")` |

#### Codex CLI

| Layer | Method | When | API |
|-------|--------|------|-----|
| **L1: Direct Spawn** | `spawn_agent` → `wait_agent` | 1-4 step sequential chains | `spawn_agent(prompt)` → `wait_agent(id)` |
| **L2: Parallel Spawn** | Multiple `spawn_agent` → `wait_agent` all | 2-3 independent branches | `spawn_agent` × N → `wait_agent` × N |
| **L3: Rally Delegation** | `spawn_agent` with Rally prompt | 4+ workers, complex ownership | `spawn_agent(prompt="You are Rally...")` |

**Codex Subagent Tools:**
- `spawn_agent` — 新しいサブエージェントをスポーン
- `send_input` — 実行中のサブエージェントに追加指示を送信
- `wait_agent` — サブエージェントの完了を待機
- `resume_agent` — 一時停止したサブエージェントを再開
- `close_agent` — サブエージェントのスレッドを閉じる

### Layer Selection

```
Steps <= 4 AND sequential?     → L1: Direct Spawn (foreground / spawn_agent)
2-3 independent branches?      → L2: Parallel Spawn (background / spawn_agent × N)
4+ workers OR complex ownership? → L3: Rally Delegation
```

### Model Selection

| Agent Role | model | Context Strategy | Rationale |
|-----------|-------|-----------------|-----------|
| Investigation / read-only (Scout, Lens, Rewind) | sonnet | reset | Cost-efficient; focused context |
| Standard implementation (Builder, Artisan, Radar) | sonnet | hybrid | Balanced; receives handoff context |
| High-complexity design (Sentinel, Atlas) | opus | continuous | Precision-critical; deep reasoning |
| Lightweight tasks (Quill, Morph) | haiku | reset | Minimal cost; fresh context |
| Evaluator (Judge, Voyager, Warden in eval mode) | sonnet | reset | Evaluators need only contract + output |
| Generator (revision iteration) | sonnet | continuous | Benefits from feedback accumulation |

**Context Strategy**: `reset` = file-based handoff (fresh context per agent), `continuous` = in-context handoff (accumulated context), `hybrid` = Nexus continuous + spawned agents reset. See `nexus/references/context-strategy.md` for details.

### Advanced Spawn Options

Agent tool (v2.1.63+) supports additional frontmatter fields for fine-grained control:

| Option | Description | When to Use |
|--------|-------------|-------------|
| `maxTurns` | Maximum agentic turns before stopping | コスト管理、暴走防止。調査系: 20-30、実装系: 50-80 |
| `effort` | Reasoning effort (`low`/`medium`/`high`/`max`) | Haiku+low で超軽量タスク、Opus+max で最高精度 |
| `isolation: worktree` | Git worktree で隔離実行 | L2並列時のファイル競合防止。各ブランチが独立コピーで作業 |
| `resume` (agent ID) | 既存サブエージェントを再開 | 失敗リトライ、追加作業の継続。フル履歴を保持 |
| `skills` | Skill content を事前注入 | SKILL.md を prompt 内で「読め」と言う代わりに直接注入 |
| `memory` | Persistent memory (`user`/`project`/`local`) | ルーティング学習、パターン蓄積のクロスセッション永続化 |

**Worktree isolation for L2:**
```
# L2 並列スポーン時に worktree を使うと、ファイル競合リスクがゼロになる
Agent(
  name: "builder-feature-a"
  isolation: worktree          # 独立した git worktree で実行
  run_in_background: true
  ...
)
Agent(
  name: "builder-feature-b"
  isolation: worktree
  run_in_background: true
  ...
)
# 両者が完了後、worktree の変更をマージ
```

### Custom Subagent Definitions

`.claude/agents/` (project) or `~/.claude/agents/` (user) に Markdown ファイルを配置することで、カスタム subagent_type を事前定義できる。これにより spawn 時のプロンプトが簡潔になり、ツール制限・モデル選択・スキル注入が確実に効く。

```yaml
# ~/.claude/agents/scout-agent.md
---
name: scout-agent
description: Bug investigation and root cause analysis. Use proactively for bug reports.
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet
maxTurns: 30
memory: project
skills:
  - scout
---
あなたは Scout エージェントです。バグの根本原因を調査し、再現手順と影響範囲を特定してください。
コードは変更しません。完了時は _STEP_COMPLETE フォーマットで報告してください。
```

定義済みエージェントは `subagent_type: "scout-agent"` で直接参照可能。

---

## Agent Context Injection

When spawning an agent, Nexus provides context through the prompt:

1. **SKILL.md Path**: Tell the agent to read its own SKILL.md first
2. **Task Description**: Clear, specific task with acceptance criteria
3. **Handoff Context**: Results from previous steps in the chain
4. **Constraints**: Guardrail level, file ownership, scope limits
5. **Output Format**: Request `_STEP_COMPLETE` format in the response

The spawned agent reads its own SKILL.md and follows its own methodology autonomously. Nexus does not need to simulate the agent's personality or process.

### Example: Spawning Scout

```
Agent(
  name: "scout-login-bug"
  description: "Investigate login bug root cause"
  subagent_type: general-purpose
  mode: bypassPermissions
  model: sonnet
  prompt: |
    あなたは Scout エージェントです。
    まず ~/.claude/skills/scout/SKILL.md を読み、その指示に従ってください。

    タスク: ログインバグの根本原因を調査してください。
    症状: ユーザーがログインできない
    制約: コードは変更しない（調査のみ）

    完了時、以下のフォーマットで結果を出力してください:
    _STEP_COMPLETE:
      Agent: Scout
      Status: SUCCESS | PARTIAL | BLOCKED | FAILED
      Output: [調査結果]
      Next: [推奨次エージェント or DONE]
)
```

Scout returns:
```
_STEP_COMPLETE:
  Agent: Scout
  Status: SUCCESS
  Output: Root cause identified - token refresh timing issue in auth middleware
```

### Example: Spawning Scout (Codex CLI)

```
# Step 1: Spawn Scout
scout_id = spawn_agent(
  prompt: |
    あなたは Scout エージェントです。
    まず ~/.claude/skills/scout/SKILL.md を読み、その指示に従ってください。

    タスク: ログインバグの根本原因を調査してください。
    症状: ユーザーがログインできない
    制約: コードは変更しない（調査のみ）

    完了時、_STEP_COMPLETE フォーマットで結果を出力してください。
)

# Step 2: Wait for completion
result = wait_agent(scout_id)

# Step 3: Use result to spawn Builder
builder_id = spawn_agent(
  prompt: |
    あなたは Builder エージェントです。
    まず ~/.claude/skills/builder/SKILL.md を読み、その指示に従ってください。
    前ステップからのコンテキスト: {result}
    ...
)
wait_agent(builder_id)

# Step 4: Cleanup
close_agent(scout_id)
close_agent(builder_id)
  Next: Builder
```

---

## Step Transitions

### Automatic Transition (AUTORUN)

After receiving `_STEP_COMPLETE` from a spawned agent, Nexus automatically:
1. Records the completed step and captures the agent's output
2. Extracts handoff context from the result
3. Spawns the next agent in the chain with accumulated context

### Manual Transition (GUIDED)

After receiving the agent's result, Nexus:
1. Outputs the `## NEXUS_HANDOFF` block to the user
2. Waits for user to confirm continuation
3. Spawns the next agent when confirmed

---

## Error Handling in AUTORUN

| Error | Level | Action |
|-------|-------|--------|
| Minor issue | L1 | Log and continue |
| Test failure <20% | L2 | Auto-fix attempt |
| Test failure >50% | L3 | Rollback and retry |
| Critical error | L4 | Abort and report |

---

## Platform Compatibility

### Tool Abstraction

The protocol uses semantic descriptions instead of platform-specific tool names:

| Action | Description | Claude Code | Codex CLI | Gemini |
|--------|-------------|-------------|-----------|--------|
| Ask user | Request user input | AskUserQuestion | prompt() | input() |
| Run command | Execute shell | Bash | shell() | execute() |
| Read file | Load file content | Read | read() | file.read() |
| Edit file | Modify file | Edit | edit() | file.write() |
| Search code | Find in codebase | Grep/Glob | search() | find() |

### Agent Invocation

Instead of platform-specific agent calls, use semantic triggers:

```yaml
# Platform-agnostic
## NEXUS_AUTORUN_FULL
Add user authentication

# Nexus interprets and executes as:
# 1. Scout (investigate requirements)
# 2. Builder (implement)
# 3. Sentinel (security check)
# 4. Radar (tests)
```

---

## Completion Format

### AUTORUN Completion

```
## NEXUS_COMPLETE
Task: [Task name]
Mode: AUTORUN_FULL
Chain: [Executed chain]

### Summary
- Steps completed: [N]
- Files changed: [List]
- Tests: [PASS/FAIL]

### Results
[Final deliverables]

### Verification
1. [How to verify step 1]
2. [How to verify step 2]
```

### GUIDED Completion

```
## NEXUS_COMPLETE
Task: [Task name]
Mode: GUIDED
Chain: [Executed chain]

### Summary
[Results from manual execution]
```

---

## Design Principles

### Context Externalization

> Context is an external interrogable object, not embedded state. [Source: Anthropic Managed Agents]

Do not embed the full chain history into each agent's prompt. Instead, treat the session as an append-only event log that agents can query:

| Anti-pattern | Pattern |
|---|---|
| Paste all prior step outputs into prompt | Store in `.agents/PROJECT.md`; pass summary + file path reference |
| Irreversible context trimming (discard tokens permanently) | Keep full log external; selectively retrieve what the current step needs |
| Growing prompt with every step | Pass only the state delta from the previous step |

**Practical implementation:**
- `_STEP_COMPLETE` outputs serve as the event log entries
- Each agent receives: task description + previous step's key output + file references
- Full history is always recoverable from `.agents/PROJECT.md` + agent journals
- When a step needs earlier context, it reads the journal file — not the prompt

### Lazy Provisioning (TTFT Optimization)

> Provision execution environments only when the brain actually needs them. [Source: Anthropic Managed Agents]

Delay agent spawning until the orchestrator has decided what to spawn:

```
CLASSIFY → CHAIN_SELECT → (first inference starts immediately)
                          → (agent spawn happens just-in-time for EXECUTE)
```

| Optimization | Effect |
|---|---|
| Start CLASSIFY/CHAIN_SELECT without waiting for agent readiness | Reduces time-to-first-token |
| Spawn agents only when their step is next | Avoids unnecessary resource allocation for steps that may be skipped |
| Use `model: haiku` for investigation steps, `model: opus` for critical steps | Right-size compute per step |

**In practice:** Nexus should complete CLASSIFY and CHAIN_SELECT in its own context before spawning any Agent. Do not pre-spawn agents "just in case."

## Best Practices

1. **Default to AUTORUN_FULL**: For most tasks, automatic execution is preferred
2. **Use GUIDED for learning**: When users want to understand the process
3. **Check guardrails**: AUTORUN_FULL includes safety checks at key points
4. **Preserve context**: Use `_STEP_COMPLETE` to maintain chain context
5. **Report progress**: Show clear step indicators during execution

---

## Migration from Copy-Paste

### Before (Manual)
```
/Nexus task → Copy $Agent prompt → Paste to Agent → Copy response → Paste to Nexus → Repeat
```

### After (Automatic)
```
## NEXUS_AUTORUN_FULL
task
```
→ Nexus spawns each agent via Agent tool → Each agent reads its own SKILL.md → Final result

**Key change**: Each agent runs as an independent Claude session with full access to its own expertise, rather than Nexus simulating the agent's role.

---

## Subagent Context Rules

Understanding context inheritance is critical for reliable chain execution:

| Aspect | Behavior |
|--------|----------|
| **会話履歴** | サブエージェントは親の会話履歴を引き継がない。プロンプトで明示的に渡す |
| **Skills** | サブエージェントは親のskillsを引き継がない。`skills` フィールドで明示注入が必要 |
| **権限** | 親の権限設定を継承。親が `bypassPermissions` なら子も同様（上書き不可） |
| **Auto mode** | 親が `auto` mode の場合、子の `permissionMode` は無視される |
| **Auto-compaction** | ~95%容量で自動発動。`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` で変更可能 |
| **トランスクリプト** | `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl` に保存 |
| **ネスト** | サブエージェントは他のサブエージェントをスポーンできない（1階層のみ） |

---

## Subagent Lifecycle Hooks

`settings.json` でサブエージェントのライフサイクルをモニタリングできる。Latch エージェントで設計・実装を推奨。

### チェーン実行モニタリング

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/log-agent-start.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/log-agent-stop.sh" }
        ]
      }
    ]
  }
}
```

### Agent Teams 品質ゲート (Rally L3)

| Hook Event | Matcher | 用途 |
|-----------|---------|------|
| `TeammateIdle` | — | チームメイトがアイドル直前。exit 2 で作業継続を強制 |
| `TaskCompleted` | — | タスク完了マーク時。exit 2 で完了を阻止しフィードバック送信 |

### サブエージェント内フック（frontmatter定義）

サブエージェント定義ファイル内で `hooks` を定義すると、そのサブエージェント実行中のみ有効なフックが設定される。

```yaml
---
name: safe-builder
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-safe-command.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

`Stop` フックは frontmatter 内で定義すると自動的に `SubagentStop` に変換される。

---

## Agent Teams Constraints (Rally L3)

Agent Teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` 必要) の制限事項:

| 制限 | 影響 |
|------|------|
| 実験的機能 | 設定で明示的に有効化が必要 |
| 1セッション1チーム | 複数チームの同時管理不可 |
| ネスト不可 | チームメイトは自チームを作れない |
| リーダー固定 | 作成セッションが永続リーダー（移譲不可） |
| セッション再開制限 | `/resume` で in-process チームメイトは復元されない |
| 権限はスポーン時に固定 | 全チームメイトがリーダーの権限モードを継承 |
| Split-pane | tmux または iTerm2 が必要（VS Code Terminal 非対応） |
