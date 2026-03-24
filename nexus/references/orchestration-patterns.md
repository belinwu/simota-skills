# Nexus Orchestration Patterns Reference

**Purpose:** Reference patterns for sequential, parallel, and gated execution.
**Read when:** You need to choose or explain an orchestration pattern.

## Contents
- Pattern A: Sequential Chain
- Pattern B: Parallel Branches (with Auto-Conflict Resolution)
- Pattern C: Conditional Routing
- Pattern D: Recovery Loop
- Pattern E: Escalation Path
- Pattern F: Verification Gate
- Hub Communication Protocol

Detailed patterns for agent chain execution.

---

## Pattern A: Sequential Chain (L1: Direct Spawn)

```
Nexus → Agent(Scout, foreground) → _STEP_COMPLETE
                                       ↓
Nexus → Agent(Builder, foreground) → _STEP_COMPLETE
              [with Scout context]         ↓
Nexus → Agent(Radar, foreground) → _STEP_COMPLETE
              [with Builder context]       ↓
Nexus → VERIFY → DELIVER
```

**Use when**: Steps have strict dependencies (output of one is input of next)

**Implementation**: Each agent is spawned via `Agent(foreground)`. Nexus extracts `_STEP_COMPLETE` output from the returned result and passes it as handoff context to the next agent's prompt.

```
# Step 1
result1 = Agent(
  name: "scout-investigation"
  description: "Root cause analysis"
  mode: bypassPermissions
  model: sonnet
  prompt: "あなたは Scout エージェントです。まず ~/.claude/skills/scout/SKILL.md を読み..."
)

# Step 2 - uses Step 1's output
result2 = Agent(
  name: "builder-fix"
  description: "Implement fix"
  mode: bypassPermissions
  model: sonnet
  prompt: "あなたは Builder エージェントです。まず ~/.claude/skills/builder/SKILL.md を読み...
    前ステップからのコンテキスト: {result1}"
)
```

---

## Pattern B: Parallel Branches (L2: Parallel Spawn)

```
Nexus → Agent(Builder-A, background) ──┐
      → Agent(Builder-B, background) ──┤
                                        ↓ (wait for all)
                            ┌───────────────────────┐
                            │ CONFLICT DETECTION    │
                            │ - Identify overlaps   │
                            │ - Classify conflicts  │
                            └───────────┬───────────┘
                                        │
                        ┌───────────────┴───────────────┐
                        ▼                               ▼
                   No Conflicts                    Has Conflicts
                        │                               │
                        │                   ┌───────────┴───────────┐
                        │                   ▼                       ▼
                        │              Auto-Resolvable         Needs User
                        │              (ADJACENT,              (SEMANTIC
                        │               FORMATTING,             unclear,
                        │               SEMANTIC clear)         STRUCTURAL)
                        │                   │                       │
                        │                   ▼                       ▼
                        │              Auto-Resolve            ESCALATE
                        │                   │                       │
                        └───────────┬───────┘                       │
                                    ▼                               │
                            AGGREGATE                               │
                                    │                               │
                                    ▼                               │
                              VERIFY (tests)                        │
                                    │                               │
                        ┌───────────┴───────────┐                   │
                        ▼                       ▼                   │
                      PASS                    FAIL                  │
                        │                       │                   │
                        ▼                       ▼                   │
                    DELIVER              RECOVERY ←─────────────────┘
```

**Use when**: 2-3 independent tasks can execute simultaneously (e.g., separate features)

**Implementation**: Each branch is spawned as a background Agent. Nexus waits for completion notifications, then aggregates results.

```
# Spawn both branches simultaneously in a single response
Agent(
  name: "builder-email"
  description: "Email validation"
  run_in_background: true
  mode: bypassPermissions
  model: sonnet
  prompt: "あなたは Builder エージェントです。まず ~/.claude/skills/builder/SKILL.md を読み...
    ファイル所有権: src/validators/email.ts, tests/validators/email.test.ts
    制約: 上記ファイルのみ変更可能..."
)

Agent(
  name: "builder-phone"
  description: "Phone validation"
  run_in_background: true
  mode: bypassPermissions
  model: sonnet
  prompt: "あなたは Builder エージェントです。まず ~/.claude/skills/builder/SKILL.md を読み...
    ファイル所有権: src/validators/phone.ts, tests/validators/phone.test.ts
    制約: 上記ファイルのみ変更可能..."
)

# Wait for both to complete (notifications arrive automatically)
# Then proceed to AGGREGATE → VERIFY → DELIVER
```

### Auto-Conflict Resolution Rules

| Conflict Type | Auto-Resolve? | Method |
|---------------|---------------|--------|
| ADJACENT | ✅ Always | Accept both, merge in order |
| FORMATTING | ✅ Always | Regenerate with formatter |
| SEMANTIC (owner clear) | ✅ If ownership >= 0.70 | Ownership priority |
| SEMANTIC (owner unclear) | ❌ | Escalate to user |
| STRUCTURAL | ❌ Never | Always escalate |

### Ownership Priority

When two branches modify the same code semantically:

```yaml
ownership_score:
  primary_agent_role: 0.40  # Domain specialist bonus
  change_volume: 0.30       # More changes = more ownership
  task_alignment: 0.30      # Is file central to task?

  auto_resolve_if: ownership_score >= 0.70
```

See `references/conflict-resolution.md` for detailed resolution strategies.

---

## Pattern C: Conditional Routing

```
Nexus → NEXUS_ROUTING → Agent1 → NEXUS_HANDOFF
                           ↓
Nexus → Analyze findings
           │
           ├─ [Security issue] → Sentinel → NEXUS_HANDOFF
           ├─ [Performance issue] → Bolt → NEXUS_HANDOFF
           └─ [No issues] → Continue to next step
```

**Use when**: Next agent depends on findings (e.g., Judge → Builder OR Sentinel)

---

## Pattern D: Recovery Loop

```
Nexus → NEXUS_ROUTING → Agent → NEXUS_HANDOFF
                           │
                           ├─ [SUCCESS] → Continue
                           │
                           └─ [FAILED] → Error Handler
                                    ↓
                              ┌─────────────────┐
                              │ Recovery Action │
                              │ - Retry (L1)    │
                              │ - Inject fix (L2)│
                              │ - Rollback (L3) │
                              └────────┬────────┘
                                       ↓
                              Re-execute or Escalate
```

**Use when**: Errors occur during execution (auto-recovery enabled)

---

## Pattern E: Escalation Path

```
Nexus → NEXUS_ROUTING → Agent → NEXUS_HANDOFF (Pending Confirmation)
                                        ↓
Nexus → Present to User (AskUserQuestion)
                                        ↓
User → Select option
                                        ↓
Nexus → NEXUS_ROUTING (with User Confirmation) → Agent continues
```

**Use when**: Agent encounters decision requiring user input (L4 guardrail or GUIDED mode)

---

## Pattern F: Verification Gate

```
Nexus → Chain execution complete
                   ↓
          ┌───────────────────┐
          │ VERIFICATION GATE │
          │ - Tests pass?     │
          │ - Build OK?       │
          │ - Security OK?    │
          └─────────┬─────────┘
                    │
          ┌────────┴────────┐
          ↓ PASS            ↓ FAIL
      DELIVER          RECOVERY
                           │
                    ┌──────┴──────┐
                    │ Rollback OR │
                    │ Re-execute  │
                    └─────────────┘
```

**Use when**: Critical verification before final delivery (always used in AUTORUN_FULL)

---

## Pattern G: Rally Delegation (L3)

```
Nexus → Agent(Rally, foreground) → Rally manages team
                                       ↓
                              ┌────────────────────┐
                              │ Rally Team Session  │
                              │ - TeamCreate        │
                              │ - Spawn teammates   │
                              │ - Monitor tasks     │
                              │ - Synthesize        │
                              │ - Cleanup           │
                              └────────┬───────────┘
                                       ↓
                              _STEP_COMPLETE (aggregated)
                                       ↓
                              Nexus → VERIFY → DELIVER
```

**Use when**: 4+ workers needed, complex file ownership, or multi-step parallel branches

**Implementation**: Nexus spawns Rally as a single Agent. Rally handles all team management internally using Agent Teams API.

```
Agent(
  name: "rally-feature-impl"
  description: "Parallel feature implementation"
  subagent_type: general-purpose
  mode: bypassPermissions
  model: sonnet
  prompt: |
    あなたは Rally エージェントです。
    まず ~/.claude/skills/rally/SKILL.md を読み、その指示に従ってください。

    タスク: 以下の機能を並列実装してください。
    ワーカー:
      1. Builder: ユーザー認証API (src/auth/)
      2. Builder: プロフィールAPI (src/profile/)
      3. Artisan: ログインUI (src/components/auth/)
      4. Artisan: プロフィールUI (src/components/profile/)
      5. Radar: 統合テスト (tests/)

    制約:
    - 各ワーカーは指定ディレクトリのみ変更可能
    - ビルド・テスト・型チェック通過を確認

    完了時、_STEP_COMPLETE フォーマットで結果を出力してください。
)
```

**Escalation from L2 to L3**: If L2 parallel spawn encounters ownership conflicts or requires more than 3 branches, escalate to L3 Rally delegation.

---

## Hub Communication Protocol

```
User Request
     ↓
  NEXUS (Classify & Design Chain)
     ↓
  ┌──────────────────────────────────────────────────────────────┐
  │                    NEXUS_ROUTING                             │
  │  (Context, Goal, Step, Constraints, Expected Output)         │
  └──────────────────────────────────────────────────────────────┘
     ↓
  Agent A executes
     ↓
  ┌──────────────────────────────────────────────────────────────┐
  │                    NEXUS_HANDOFF                             │
  │  (Summary, Artifacts, Risks, Suggested Next, _STEP_COMPLETE) │
  └──────────────────────────────────────────────────────────────┘
     ↓
  NEXUS (Aggregate, Route, or Verify)
     ↓
  Next Agent or DELIVER
```
