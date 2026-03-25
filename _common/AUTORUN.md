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
