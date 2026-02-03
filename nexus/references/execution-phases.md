# Nexus Execution Phases Reference

Detailed phase descriptions for AUTORUN modes.

---

## Phase 0: PROACTIVE_ANALYSIS (Optional)

`/Nexus` のみで呼び出された場合に自動発動。通常のタスク指示がある場合はスキップ。

### 0-A: Project State Scan
プロジェクトの現在状態を収集:

```bash
# Git status
git status --porcelain

# Recent commits
git log --oneline -10

# Activity Log (if exists)
.agents/PROJECT.md → Activity Log section
```

### 0-B: Health Assessment
4つの指標でプロジェクト健全性を評価:

| 指標 | チェック内容 | 評価 |
|------|-------------|------|
| `test_health` | テスト実行、カバレッジ | 🟢/🟡/🔴 |
| `security_health` | npm audit、依存関係 | 🟢/🟡/🔴 |
| `code_health` | lint、型チェック | 🟢/🟡/🔴 |
| `doc_health` | README更新日、JSDoc | 🟢/🟡/🔴 |

### 0-C: Recommendation Generation
優先度付きで推奨アクションを生成:

| 優先度 | 条件 |
|--------|------|
| 🔴 高 | セキュリティ問題、テスト失敗、ビルドエラー |
| 🟡 中 | lint警告、カバレッジ低下、ドキュメント不足 |
| 🟢 低 | リファクタリング機会、最適化提案 |

### Flow After Phase 0

```
Phase 0 Complete
    ↓
User Selection (ON_PROACTIVE_START)
    ↓
├─ 推奨アクション選択 → Phase 1: PLAN (AUTORUN_FULL)
├─ 前回作業継続 → Phase 1: PLAN (AUTORUN_FULL)
└─ 新規タスク指示 → 通常ルーティング → Phase 1
```

See `references/proactive-mode.md` for detailed specifications.

---

## AUTORUN_FULL (7 Phases)

### Phase 1: PLAN
Classify and analyze the task:

**Task Classification:**
- **BUG**: Error fix, defect response, "not working", "broken"
- **INCIDENT**: Production outage, service degradation, "down", "emergency", "SEV1/2/3/4"
- **API**: API design, endpoint creation, OpenAPI spec
- **FEATURE**: New feature, "I want to...", "add..."
- **REFACTOR**: Code cleanup (behavior unchanged)
- **OPTIMIZE**: Performance improvement
- **SECURITY**: Security response, vulnerability
- **DOCS**: Documentation
- **INFRA**: Infrastructure provisioning

**Complexity Assessment:**
- **SIMPLE**: 1-2 steps to complete
- **MEDIUM**: 3-5 steps
- **COMPLEX**: 6+ steps (decompose with Sherpa)

**Analysis:**
- Identify independent tasks (parallelizable)
- Identify dependent tasks (sequential required)
- Map file ownership per branch
- Determine guardrail requirements

### Phase 2: PREPARE
Set up execution environment:

1. **Context Snapshot Creation** - Capture initial goal and acceptance criteria
2. **Rollback Point Definition** - Create git stash or branch for recovery
3. **Guardrail Configuration** - Set appropriate levels per step
4. **Parallel Branch Preparation** - Split independent tasks, assign file ownership

### Phase 3: CHAIN_SELECT
Auto-select agent chain based on classification.

For parallel execution:
```
_PARALLEL_CHAINS:
  - branch_id: A
    chain: [Agent1, Agent2]
    files: [file1.ts, file2.ts]
  - branch_id: B
    chain: [Agent3, Agent4]
    files: [file3.ts, file4.ts]
  merge_point: Radar
```

### Phase 4: EXECUTE
Execute steps with guardrail checkpoints:

**Sequential:**
1. Execute agent role for current step
2. Perform work according to SKILL.md
3. Guardrail Check at configured checkpoints
4. Record result as `_STEP_COMPLETE`
5. Verify success conditions
6. Proceed to next step OR trigger recovery

**Parallel:**
1. Launch parallel branches simultaneously
2. Each branch executes independently
3. Monitor for conflicts
4. Wait for all branches at merge point

### Phase 5: AGGREGATE
Merge parallel results:

1. Collect Branch Results - Gather outputs, check for conflicts
2. Conflict Resolution - Resolve or escalate file conflicts
3. Context Consolidation - Update L1_GLOBAL, prepare unified state

### Phase 6: VERIFY
Verify acceptance criteria:

1. Run tests (Radar equivalent)
2. Confirm build passes
3. Security scan if applicable (Sentinel)
4. Final Guardrail Check (L2_CHECKPOINT minimum)

### Phase 7: DELIVER
Finalize and present results:

1. Integrate final output
2. Generate change summary
3. Present verification steps
4. Cleanup rollback points (on success)

---

## AUTORUN (5 Phases - Simple Tasks Only)

| Phase | Description |
|-------|-------------|
| **CLASSIFY** | Same as AUTORUN_FULL Phase 1 |
| **CHAIN_SELECT** | Auto-select agent chain |
| **EXECUTE_LOOP** | Execute each agent role, record _STEP_COMPLETE |
| **VERIFY** | Run tests, confirm build |
| **DELIVER** | Integrate output, generate summary |

COMPLEX tasks are downgraded to GUIDED mode.
