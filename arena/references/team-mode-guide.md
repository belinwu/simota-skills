# Team Mode Guide

Guide for running Arena in Team Mode using the Agent Teams API for true parallel execution of external AI engines.

---

## Core Concept

In Team Mode, Arena acts as the **team leader** and spawns subagents (Claude Code `general-purpose` agents) that serve as **proxies** for external AI engines. Each subagent's sole job is to invoke an external CLI (`codex exec` or `gemini`) via the Bash tool — the subagent does NOT implement code itself.

```
Arena (Team Leader)
├── variant-codex (subagent) → Bash: codex exec ...
├── variant-gemini (subagent) → Bash: gemini -p ...
└── [optional: variant-codex-2, variant-gemini-2, ...]
```

**Key principle:** Subagents are remote hands, not brains. They delegate all implementation work to external engines.

---

## Arena vs Rally: Competition vs Cooperation

| Aspect | Arena Team Mode | Rally |
|--------|----------------|-------|
| **Purpose** | Competition — same spec, different engines/approaches | Cooperation — different tasks, all results integrated |
| **Subagent tasks** | All do the SAME task differently | Each does a DIFFERENT task |
| **Result handling** | Compare → select best → discard rest | Collect all → integrate all |
| **Typical use** | "Which engine produces better auth code?" | "Build frontend + backend + tests in parallel" |
| **Evaluation** | 5-criteria scoring, winner selection | Completeness check, integration validation |

---

## When to Use Team Mode vs Solo Mode

| Condition | Solo Mode | Team Mode |
|-----------|-----------|-----------|
| Variant count | 2 | 3+ |
| Parallelism | Sequential | True parallel |
| Cost | Low (single session) | Higher (N sessions) |
| Complexity | Low-Medium | High |
| Best for | codex vs gemini 2-way comparison | Multi-approach, engine mixing |

**Default to Solo Mode.** Use Team Mode when:
- 3+ variants are needed
- Time is a bottleneck and parallel execution matters
- Multiple approach hints need to be tested with the same engine

---

## Team Design Patterns

### Pattern 1: Engine Competition

Two subagents, each using a different engine to implement the same spec.

```
Arena Leader
├── variant-codex  → codex exec "{spec}"
└── variant-gemini → gemini -p "{spec}"
```

### Pattern 2: Multi-Approach

Multiple subagents using the same or different engines with different approach hints.

```
Arena Leader
├── variant-codex-iterative → codex exec "{spec} Use an iterative approach"
├── variant-codex-recursive → codex exec "{spec} Use a recursive approach"
└── variant-gemini-novel    → gemini -p "{spec} Propose a novel approach"
```

### Pattern 3: Engine + Review

Combine implementation and automated review in parallel.

```
Arena Leader
├── variant-codex  → codex exec "{spec}" → git commit
├── variant-gemini → gemini -p "{spec}" → git commit
└── reviewer       → (waits for completion) → codex review on both branches
```

---

## Lifecycle

```
SPEC → DESIGN → SPAWN → COMPETE → REVIEW → EVALUATE → ADOPT → CLEANUP
```

### Phase 1: SPEC

Arena leader validates or creates the specification (same as Solo Mode).

### Phase 2: DESIGN

Arena leader decides:
- How many variants
- Which engines
- Which approach hints
- Branch naming

### Phase 3: SPAWN (with git worktree isolation)

Arena leader creates **isolated working directories** via `git worktree` BEFORE spawning subagents. This prevents all parallel execution conflicts (`.git/index.lock` contention, filesystem write conflicts, cross-contamination).

```python
# 1. Prepare worktrees (Arena leader via Bash)
# git stash push -m "arena: pre-session stash"
# BASE_COMMIT=$(git rev-parse HEAD)
# SESSION_ID="arena-$(date +%s)"
# mkdir -p /tmp/$SESSION_ID

# 2. Create branches and worktrees
# git branch arena/variant-codex $BASE_COMMIT
# git branch arena/variant-gemini $BASE_COMMIT
# git worktree add /tmp/$SESSION_ID/variant-codex arena/variant-codex
# git worktree add /tmp/$SESSION_ID/variant-gemini arena/variant-gemini

# 3. Create team
TeamCreate(team_name="arena-{task_id}")

# 4. Create tasks
TaskCreate(subject="Implement spec via codex exec", ...)
TaskCreate(subject="Implement spec via gemini", ...)

# 5. Spawn subagents — each receives its worktree path
Task(
  subagent_type="general-purpose",
  team_name="arena-{task_id}",
  name="variant-codex",
  prompt="...see Teammate Prompt Template below..."
  # Include: worktree_path="/tmp/$SESSION_ID/variant-codex"
)

Task(
  subagent_type="general-purpose",
  team_name="arena-{task_id}",
  name="variant-gemini",
  prompt="...see Teammate Prompt Template below..."
  # Include: worktree_path="/tmp/$SESSION_ID/variant-gemini"
)
```

**CRITICAL:** The Arena leader MUST create all branches and worktrees BEFORE spawning subagents. Subagents receive the worktree path and operate within it — they do NOT create branches, checkout, or switch directories outside their assigned worktree.

### Phase 4: COMPETE (parallel-safe)

Subagents work in **true parallel** with full filesystem isolation:
- Each `cd`s into its pre-created worktree directory
- Each invokes its assigned engine CLI within its isolated directory
- Each `git add -A && git commit` only affects files in its own worktree
- No `.git/index.lock` contention — worktrees share the repo but have independent index files
- Each commits results and marks task complete

Arena leader monitors via TaskList and waits for all tasks to complete.

### Phase 5: REVIEW (Mandatory Quality Gate)

After all subagents complete, the Arena leader runs a **mandatory review** on each variant. This is a quality gate — no variant proceeds to EVALUATE without passing review.

For each variant branch, the Arena leader:

1. **Scope Check** — `git diff --name-only $BASE_COMMIT..arena/variant-{engine}` and verify only allowed files were modified
2. **Test Execution** — Checkout or use worktree to run the project's test command (`npm test`, `pytest`, etc.)
3. **Build Verification** — Run the project's build command to confirm the variant compiles/builds
4. **Automated Code Review** — `codex review --uncommitted` for code quality and security signals
5. **Acceptance Criteria Check** — Read implementation files and verify each acceptance criterion from the spec is met

**Review result per variant:**

```yaml
review_result:
  variant: "arena/variant-{engine}"
  scope_check: PASS | FAIL   # Were only allowed files modified?
  test_result: PASS | FAIL | SKIP  # Did tests pass?
  build_result: PASS | FAIL | SKIP  # Did build succeed?
  codex_review_summary: "[Key findings]"
  acceptance_criteria:
    - criterion: "[Criterion 1]"
      met: true | false
    - criterion: "[Criterion 2]"
      met: true | false
  overall: PASS | FAIL | WARN
  notes: "[Any issues or observations]"
```

**Disqualification rules:**
- **Scope FAIL** → Attempt to revert unauthorized files and re-check; if core logic is in forbidden files, disqualify
- **Test FAIL** → Variant is penalized in Correctness score but NOT automatically disqualified (may still be the best option)
- **Build FAIL** → Variant is disqualified (cannot be adopted)
- **All criteria unmet** → Variant is disqualified

### Phase 6: EVALUATE

Arena leader uses **review results as primary input** for scoring:
1. Reads implementation files
2. Runs `git diff` between variants
3. Applies 5-criteria scoring (see `evaluation-framework.md`) informed by review results
4. Selects winner from variants that passed review

### Phase 7: ADOPT

Arena leader merges winning branch into base branch.

### Phase 7: CLEANUP

**IMPORTANT:** Remove worktrees BEFORE deleting branches. `git branch -D` will fail if a worktree still references the branch.

```python
# 1. Shutdown subagents
SendMessage(type="shutdown_request", recipient="variant-codex", ...)
SendMessage(type="shutdown_request", recipient="variant-gemini", ...)

# 2. Delete team
TeamDelete()

# 3. Remove worktrees (MUST be done before branch deletion)
# git worktree remove /tmp/$SESSION_ID/variant-codex
# git worktree remove /tmp/$SESSION_ID/variant-gemini
# rm -rf /tmp/$SESSION_ID

# 4. Clean up branches
# git branch -D arena/variant-codex arena/variant-gemini

# 5. Restore stashed work
# git stash pop
```

---

## Teammate Prompt Templates

**CRITICAL**: Arena leader MUST construct the full engine prompt (with scope lock, constraints, and acceptance criteria) BEFORE spawning subagents. The `{engine_prompt}` below is the complete prompt built via `references/engine-cli-guide.md` "Prompt Construction Protocol".

### variant-codex

```
You are variant-codex on the arena-{task_id} team.

## Your Role
You are a PROXY for the codex CLI tool. You do NOT implement code yourself.
Your sole job is to invoke `codex exec` via the Bash tool in your assigned worktree directory.

## ABSOLUTE PROHIBITIONS
- NEVER write, edit, or generate implementation code yourself
- NEVER use Edit, Write, or NotebookEdit tools
- NEVER attempt to fix, improve, or adjust engine output
- NEVER modify files that the engine did not touch
- NEVER install, add, or remove dependencies
- NEVER modify config files (tsconfig, eslint, webpack, docker, CI/CD, etc.)
- NEVER create or checkout branches — your worktree is already on the correct branch
- NEVER operate outside your assigned worktree directory
- If codex exec fails or produces errors, REPORT the error to the team leader — do NOT attempt to fix it yourself

## ALLOWED ACTIONS (exhaustive list)
- Bash: `cd {worktree_path}` (move to your assigned worktree — do this FIRST)
- Bash: `codex exec --full-auto "..."` (one invocation, within your worktree)
- Bash: `git add`, `git commit`, `git diff` (within your worktree)
- Bash: `git diff --name-only` (scope validation)
- Bash: `git checkout -- {file}` (revert unauthorized file changes)
- TaskUpdate: mark task as completed
- SendMessage: report results to team leader

## Your Worktree
Your assigned working directory is: {worktree_path}
This directory is an isolated copy of the repository on branch `arena/variant-codex`.
The branch was already created by the team leader. Do NOT create or switch branches.
All your commands MUST run inside this directory.

## Execution Steps

### 1. Move to your assigned worktree
```bash
cd {worktree_path}
```
Verify you are on the correct branch:
```bash
git branch --show-current
# Expected output: arena/variant-codex
```

### 2. Run codex with the EXACT prompt below (do not modify it)
```bash
codex exec --full-auto "{engine_prompt}"
```

### 3. Validate scope — check which files were changed
```bash
git diff --name-only
```
Compare against the allowed files list below.
If ANY file outside the allowed list was modified, revert it:
```bash
git checkout -- {unauthorized_file}
```

### 4. Commit only authorized changes
```bash
git add -A && git commit -m "arena: variant-codex implementation"
```

### 5. Report to team leader
Send a message with:
- Files changed: `git diff --stat HEAD~1`
- Scope violations: list any files that were reverted
- Engine errors/warnings: any output issues from codex
- Completeness assessment: does the diff cover the spec?

### 6. Mark task as completed via TaskUpdate

## Allowed Files (engine may ONLY touch these)
{allowed_files_list}

## Forbidden Files (revert if engine touches these)
{forbidden_files_list}

## Engine Prompt (pass to codex exec exactly as-is)
{engine_prompt}
```

### variant-gemini

```
You are variant-gemini on the arena-{task_id} team.

## Your Role
You are a PROXY for the gemini CLI tool. You do NOT implement code yourself.
Your sole job is to invoke `gemini` via the Bash tool in your assigned worktree directory.

## ABSOLUTE PROHIBITIONS
- NEVER write, edit, or generate implementation code yourself
- NEVER use Edit, Write, or NotebookEdit tools
- NEVER attempt to fix, improve, or adjust engine output
- NEVER modify files that the engine did not touch
- NEVER install, add, or remove dependencies
- NEVER modify config files (tsconfig, eslint, webpack, docker, CI/CD, etc.)
- NEVER create or checkout branches — your worktree is already on the correct branch
- NEVER operate outside your assigned worktree directory
- If gemini fails or produces errors, REPORT the error to the team leader — do NOT attempt to fix it yourself

## ALLOWED ACTIONS (exhaustive list)
- Bash: `cd {worktree_path}` (move to your assigned worktree — do this FIRST)
- Bash: `gemini -p "..." --yolo` (one invocation, within your worktree)
- Bash: `git add`, `git commit`, `git diff` (within your worktree)
- Bash: `git diff --name-only` (scope validation)
- Bash: `git checkout -- {file}` (revert unauthorized file changes)
- TaskUpdate: mark task as completed
- SendMessage: report results to team leader

## Your Worktree
Your assigned working directory is: {worktree_path}
This directory is an isolated copy of the repository on branch `arena/variant-gemini`.
The branch was already created by the team leader. Do NOT create or switch branches.
All your commands MUST run inside this directory.

## Execution Steps

### 1. Move to your assigned worktree
```bash
cd {worktree_path}
```
Verify you are on the correct branch:
```bash
git branch --show-current
# Expected output: arena/variant-gemini
```

### 2. Run gemini with the EXACT prompt below (do not modify it)
```bash
gemini -p "{engine_prompt}" --yolo
```

### 3. Validate scope — check which files were changed
```bash
git diff --name-only
```
Compare against the allowed files list below.
If ANY file outside the allowed list was modified, revert it:
```bash
git checkout -- {unauthorized_file}
```

### 4. Commit only authorized changes
```bash
git add -A && git commit -m "arena: variant-gemini implementation"
```

### 5. Report to team leader
Send a message with:
- Files changed: `git diff --stat HEAD~1`
- Scope violations: list any files that were reverted
- Engine errors/warnings: any output issues from gemini
- Completeness assessment: does the diff cover the spec?

### 6. Mark task as completed via TaskUpdate

## Allowed Files (engine may ONLY touch these)
{allowed_files_list}

## Forbidden Files (revert if engine touches these)
{forbidden_files_list}

## Engine Prompt (pass to gemini exactly as-is)
{engine_prompt}
```

---

## Monitoring & Error Handling

### Progress Monitoring

Arena leader checks progress via:

```python
# Check task status
TaskList()  # Shows all tasks with status

# Send message to check on slow subagent
SendMessage(type="message", recipient="variant-codex", content="Status update?")
```

### Error Recovery

| Situation | Action |
|-----------|--------|
| Subagent engine fails | Subagent reports error → Leader decides: retry, skip, or replace |
| Subagent times out | Leader sends status check → If unresponsive, shutdown and re-spawn |
| Branch conflict | Leader resolves by resetting branch from base commit |
| All variants fail | Leader falls back to Solo Mode with different prompts |

### Re-spawn Strategy

If a subagent fails:

```python
# 1. Shutdown failed subagent
SendMessage(type="shutdown_request", recipient="variant-codex", ...)

# 2. Clean up its worktree and branch
# git worktree remove /tmp/$SESSION_ID/variant-codex
# git branch -D arena/variant-codex

# 3. Recreate branch and worktree
# git branch arena/variant-codex $BASE_COMMIT
# git worktree add /tmp/$SESSION_ID/variant-codex arena/variant-codex

# 4. Create new task and spawn replacement
TaskCreate(subject="Re-implement spec via codex exec (retry)", ...)
Task(
  subagent_type="general-purpose",
  team_name="arena-{task_id}",
  name="variant-codex-retry",
  prompt="..."
  # Include worktree_path="/tmp/$SESSION_ID/variant-codex"
)
```

---

## Complete Team Mode Example

```python
# === PREPARE (Arena leader via Bash) ===
# git stash push -m "arena: pre-session stash"
# BASE_BRANCH=$(git branch --show-current)
# BASE_COMMIT=$(git rev-parse HEAD)
# SESSION_ID="arena-$(date +%s)"
# mkdir -p /tmp/$SESSION_ID

# === CREATE BRANCHES & WORKTREES (Arena leader via Bash) ===
# git branch arena/variant-codex $BASE_COMMIT
# git branch arena/variant-gemini $BASE_COMMIT
# git worktree add /tmp/$SESSION_ID/variant-codex arena/variant-codex
# git worktree add /tmp/$SESSION_ID/variant-gemini arena/variant-gemini

# === SETUP TEAM ===
TeamCreate(team_name="arena-auth-refactor")

TaskCreate(subject="Implement auth refactor via codex")
TaskCreate(subject="Implement auth refactor via gemini")

# === SPAWN (parallel — each subagent gets its isolated worktree path) ===
Task(
  subagent_type="general-purpose",
  team_name="arena-auth-refactor",
  name="variant-codex",
  prompt="""
  You are variant-codex on the arena-auth-refactor team.

  ## Your Worktree
  Your assigned working directory is: /tmp/$SESSION_ID/variant-codex
  [... full teammate prompt with spec, worktree_path, allowed_files, forbidden_files, engine_prompt ...]
  """
)

Task(
  subagent_type="general-purpose",
  team_name="arena-auth-refactor",
  name="variant-gemini",
  prompt="""
  You are variant-gemini on the arena-auth-refactor team.

  ## Your Worktree
  Your assigned working directory is: /tmp/$SESSION_ID/variant-gemini
  [... full teammate prompt with spec, worktree_path, allowed_files, forbidden_files, engine_prompt ...]
  """
)

# === WAIT & MONITOR ===
# TaskList() periodically to check completion
# Both subagents run in PARALLEL with full filesystem isolation

# === EVALUATE (Arena leader — after all subagents complete) ===
# git diff arena/variant-codex..arena/variant-gemini
# Read files from each branch for detailed review
# Score using 5-criteria evaluation

# === ADOPT ===
# git checkout $BASE_BRANCH
# git merge arena/variant-codex -m "arena: adopt variant-codex"

# === CLEANUP (order matters!) ===
# 1. Shutdown subagents
# SendMessage(type="shutdown_request", ...) for each subagent

# 2. Delete team
# TeamDelete()

# 3. Remove worktrees BEFORE deleting branches
# git worktree remove /tmp/$SESSION_ID/variant-codex
# git worktree remove /tmp/$SESSION_ID/variant-gemini
# rm -rf /tmp/$SESSION_ID

# 4. Delete branches
# git branch -D arena/variant-codex arena/variant-gemini

# 5. Restore stash
# git stash pop
```
