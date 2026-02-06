# Lifecycle Management

Rally's team lifecycle management.
Seven phases from TeamCreate to TeamDelete, plus error scenario handling.

---

## Phase 1: ASSESS (Task Analysis)

### Purpose
Evaluate the task's parallelizability and determine whether Rally is the right agent.

### Checklist
- [ ] Does the task have parallelizable independent units?
- [ ] Have file-level dependencies been identified?
- [ ] Are 2+ teammates needed? (1 teammate = Nexus/Sherpa is sufficient)
- [ ] Does estimated time exceed parallelization overhead?

### Decision Criteria

| Condition | Verdict |
|-----------|---------|
| 2+ independent units, no file overlap | Rally is appropriate ✅ |
| Dependencies exist but staged parallelism possible | Rally is appropriate (control via blockedBy) ✅ |
| All tasks depend on the same files | Delegate to Nexus/Sherpa ❌ |
| Only one task | Execute directly or delegate to Nexus ❌ |

---

## Phase 2: DESIGN (Team Design)

### Purpose
Determine the optimal team composition and declare file ownership.

### Steps

1. **Select pattern**: Choose from `references/team-design-patterns.md`
2. **Define teammates**:
   ```yaml
   teammates:
     - name: "backend-impl"
       subagent_type: "general-purpose"
       model: "sonnet"  # optional
       mode: "bypassPermissions"
     - name: "frontend-impl"
       subagent_type: "general-purpose"
       model: "sonnet"
       mode: "bypassPermissions"
   ```
3. **Map ownership**: Follow `references/file-ownership-protocol.md`
4. **Confirm with user**: Present team composition via ON_TEAM_DESIGN trigger

---

## Phase 3: SPAWN (Team Creation)

### Steps

**Step 3.1: TeamCreate**

```
TeamCreate:
  team_name: "feature-xyz"
  description: "Parallel implementation team for XYZ feature"
```

**Step 3.2: Spawn teammates (Task tool)**

Spawn each teammate via the Task tool:

```
Task:
  subagent_type: "general-purpose"
  team_name: "feature-xyz"
  name: "backend-impl"
  description: "Backend API implementation"
  mode: "bypassPermissions"
  run_in_background: true
  prompt: |
    You are backend-impl on the feature-xyz team.
    [Context injection - see SKILL.md §3 for details]
```

**Notes:**
- Use `run_in_background: true` for async spawning
- All teammates can be spawned in parallel
- After spawning, teammates are automatically registered in the team config

**Step 3.3: Context Injection Checklist**

Verify prompt includes:
- [ ] Team name and role
- [ ] Specific task description
- [ ] File ownership (exclusive_write / shared_read)
- [ ] Tech stack, coding conventions
- [ ] Dependencies, prerequisites
- [ ] Completion criteria
- [ ] Reporting instructions via TaskUpdate

---

## Phase 4: ASSIGN (Task Assignment)

### Steps

**Step 4.1: Create tasks via TaskCreate**

```
TaskCreate:
  subject: "Implement auth API endpoints"
  description: |
    Implement POST /api/auth/login and POST /api/auth/register.
    Include JWT token generation/validation middleware.
    Files: src/api/auth/**, src/services/auth/**
  activeForm: "Implementing auth API endpoints"
```

**Step 4.2: Set dependencies**

```
TaskUpdate:
  taskId: "3"
  addBlockedBy: ["1", "2"]
```

**Step 4.3: Assign owner**

```
TaskUpdate:
  taskId: "1"
  owner: "backend-impl"
  status: "in_progress"
```

**Step 4.4: Notify teammates**

When blockedBy is resolved for a task, notify the owner via DM:

```
SendMessage:
  type: "message"
  recipient: "frontend-impl"
  content: "Blockers for task 3 have been resolved. Please begin work."
  summary: "Blocker resolved notification"
```

---

## Phase 5: MONITOR (Progress Monitoring)

### Monitoring Loop

```
while (incomplete tasks remain):
  1. Check all task states via TaskList
  2. Handle each task state:
     - completed → Prepare for Phase 6
     - in_progress → Normal (process idle notifications)
     - pending + unblocked → Nudge or assign owner
     - blocked → Help resolve blocker
  3. Receive idle notifications → respond as needed
  4. Receive error/failure messages → enter failure handling flow
```

### Handling Idle Notifications

| Idle Context | Response |
|-------------|----------|
| Idle after task completion | Normal. Assign next task |
| Idle after sending message | Normal. Waiting for reply |
| Extended idle (no progress) | DM to check status |
| Idle after error report | Enter failure handling flow |

---

## Phase 6: SYNTHESIZE (Output Integration)

### Steps

1. **Collect outputs**: Check completed tasks via TaskList
2. **Gather file change list**: Collect files_changed from each task description/report
3. **Conflict check**: Verify no changes to the same file
4. **Integration verification**:
   - Build check
   - Test execution
   - Lint check
5. **Conflict resolution**: Fire ON_RESULT_CONFLICT trigger if needed

---

## Phase 7: CLEANUP

### Steps

**Step 7.1: Confirm all tasks completed**

Verify all tasks show completed in TaskList.

**Step 7.2: Send shutdown_request**

Send to each teammate sequentially:

```
SendMessage:
  type: "shutdown_request"
  recipient: "backend-impl"
  content: "All tasks complete. Please shut down."
```

**Step 7.3: Wait for shutdown_response**

Confirm `approve: true` from each teammate.

**Step 7.4: TeamDelete**

After all shutdown confirmations:

```
TeamDelete
```

**Step 7.5: Report results**

Report final results to user:
- Team composition summary
- Completed task list
- Changed files list
- Build/test results
- Remaining risks

---

## Error Scenarios

### Teammate Hang

**Symptom:** Remains in_progress with no response, no idle notifications

**Response:**
1. DM to check status (up to 2 attempts)
2. No response → send shutdown_request
3. No shutdown_response → force terminate via TaskStop
4. Reassign task to a new teammate

### Teammate Failure

**Symptom:** Task status FAILED, error message received

**Response:**
1. Confirm with user via ON_TEAMMATE_FAILURE trigger
2. Retry → provide additional context via DM
3. Replace → shutdown_request → spawn new teammate
4. Skip → change task to manual handling

### All Teammates Failed

**Symptom:** All tasks FAILED or BLOCKED

**Response:**
1. Send shutdown_request to all teammates
2. TeamDelete
3. Report situation to user with alternatives:
   - Sequential execution via Nexus/Sherpa
   - Reduce task scope
   - Review prerequisites

### Shutdown Rejected

**Symptom:** Teammate returns `approve: false`

**Response:**
1. Check rejection reason
2. If remaining tasks → wait for completion
3. If unclear reason → report to user
