# Communication Patterns

Rally's intra-team communication templates.
Standardized message formats and SendMessage tool usage guidelines.

---

## Message Type Usage Guide

| Type | SendMessage type | Use Case | Cost | Frequency |
|------|-----------------|----------|------|-----------|
| Direct message | `message` | Instructions/questions/reports to a specific teammate | Low | High |
| Broadcast | `broadcast` | Emergency notifications to all teammates | High (N×) | Very low |
| Shutdown request | `shutdown_request` | Teammate termination request | Low | Once/person |
| Plan approval | `plan_approval_response` | Approve/reject plan_mode teammate | Low | As needed |

### Decision Criteria: DM vs Broadcast

```
Who is the message for?
  ├── One person → DM (type: message)
  ├── Some members → DM each individually
  └── Everyone affected → Is it truly needed by everyone?
       ├── Yes (emergency) → broadcast
       └── No → DM each individually
```

**Cases where broadcast is justified:**
- Shared file (type definitions, etc.) has been changed
- A blocking bug has been discovered
- Team-wide policy change
- Emergency stop instruction

---

## Rally → Teammate Templates

### Task Start Instruction

```
SendMessage:
  type: "message"
  recipient: "[teammate_name]"
  content: |
    ## Task Start Instruction

    Please begin work on task "[task_name]".

    ### Overview
    [Specific task description]

    ### File Ownership
    - exclusive_write: [pattern list]
    - shared_read: [pattern list]

    ### Completion Criteria
    1. [Criterion 1]
    2. [Criterion 2]

    ### Notes
    - [Any notes]

    When done, mark your task as completed via TaskUpdate.
  summary: "Start instruction for [task_name]"
```

### Blocker Resolved Notification

```
SendMessage:
  type: "message"
  recipient: "[teammate_name]"
  content: |
    Blockers for task "[task_name]" have been resolved.

    Prerequisite task results:
    - [Summary of prerequisite results]
    - Reference files: [file paths]

    Please begin work. Set your task to in_progress via TaskUpdate.
  summary: "Blocker resolved, start work"
```

### Additional Context

```
SendMessage:
  type: "message"
  recipient: "[teammate_name]"
  content: |
    Sharing additional information.

    [Additional context content]

    Please continue work with this information in mind.
  summary: "Additional context provided"
```

### Progress Check

```
SendMessage:
  type: "message"
  recipient: "[teammate_name]"
  content: |
    Please report progress on task "[task_name]".
    Share your current status and remaining estimate.
  summary: "Progress check request"
```

### Policy Change Notification

```
SendMessage:
  type: "message"
  recipient: "[teammate_name]"
  content: |
    Policy change notification.

    Before: [previous policy]
    After: [new policy]
    Reason: [change reason]

    If this impacts your current work, please report back.
  summary: "Policy change notification"
```

---

## Teammate → Rally Templates

Message templates for teammates to send to Rally.
Include these formats in teammate prompts to ensure consistent reporting.

### Completion Report

```
## Task Completion Report

**Task:** [task name]
**Status:** Complete

### Changed Files
- [file path 1]: [change description]
- [file path 2]: [change description]

### Test Results
- [test result summary]

### Notes
- [anything noteworthy]
```

### Failure Report

```
## Failure Report

**Task:** [task name]
**Status:** Blocked

### Problem
[Problem details]

### What Was Tried
1. [Attempt 1]
2. [Attempt 2]

### Help Needed
[What is required]
```

### Question

```
## Question

**Task:** [task name]

### Question
[The question]

### Options (if determinable)
A: [Option A]
B: [Option B]

### Recommendation
[If any]
```

---

## Broadcast Templates

### Shared File Update Notification

```
SendMessage:
  type: "broadcast"
  content: |
    [SHARED FILE UPDATE]

    The following shared files have been updated:
    - [file path]: [change description]

    Please reference the latest version and continue your work.
    Report to Rally if this impacts your work.
  summary: "Shared file update notification"
```

### Emergency Stop

```
SendMessage:
  type: "broadcast"
  content: |
    [EMERGENCY STOP]

    Due to [reason], please temporarily halt all work.
    Save your current work state and stand by until further notice.
  summary: "Emergency stop instruction"
```

---

## Nexus/Sherpa Handoff Integration

### Sherpa → Rally Handoff

When Sherpa's task decomposition includes `parallel_group`, delegate to Rally:

```
## SHERPA_TO_RALLY_HANDOFF
- Epic: [epic name]
- Parallel Groups:
  - Group A: [task list]
    - Files: [file list]
  - Group B: [task list]
    - Files: [file list]
- Dependencies:
  - Group B depends on Group A: [reason]
- Constraints:
  - [constraint details]
```

### Rally → Nexus Handoff

Rally returns results to Nexus after parallel execution:

```
## RALLY_TO_NEXUS_HANDOFF
- Team: [team name]
- Teammates: [count]
- Tasks Completed: [completed]/[total]
- Files Changed:
  - [file list]
- Build Status: PASS/FAIL
- Test Status: PASS/FAIL
- Risks:
  - [risk list]
- Next Recommended: [next agent] (reason)
```

### Nexus → Rally Handoff

Nexus invokes Rally for a parallel phase:

```
## NEXUS_TO_RALLY_HANDOFF
- Task: [task to parallelize]
- Scope:
  - [scope details]
- File Restrictions:
  - [file restrictions]
- Max Team Size: [limit]
- Expected Output: [expected deliverables]
```

---

## plan_approval_response Usage

When a teammate is spawned with `mode: "plan"`, they send an approval request to Rally when calling ExitPlanMode.

### Approve

```
SendMessage:
  type: "plan_approval_response"
  request_id: "[request ID]"
  recipient: "[teammate_name]"
  approve: true
```

### Reject (with feedback)

```
SendMessage:
  type: "plan_approval_response"
  request_id: "[request ID]"
  recipient: "[teammate_name]"
  approve: false
  content: |
    Please address the following:
    1. [Fix point 1]
    2. [Fix point 2]

    Please resubmit your plan after corrections.
```
