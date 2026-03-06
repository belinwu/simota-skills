# Agent Teams API Quick Reference

> Purpose: Read this when Rally needs exact tool syntax, parameter names, or API-level constraints.

## Table of Contents

1. Tool Overview
2. Team Tools
3. Task Tools
4. Messaging
5. Data Structures
6. Constraints and Notes

## Tool Overview

| Tool | Use for |
|------|---------|
| `TeamCreate` | create the team context and task directory |
| `Task` | spawn a teammate into the team |
| `TaskCreate` | create work items |
| `TaskUpdate` | assign owners, statuses, and dependencies |
| `TaskList` | inspect all tasks |
| `TaskGet` | inspect one task |
| `SendMessage` | DM, `broadcast`, shutdown, or plan approval |
| `TeamDelete` | delete the team after shutdown |

## Team Tools

### `TeamCreate`

```yaml
TeamCreate:
  team_name: string      # required team name
  description: string    # optional team description
  agent_type: string     # optional lead type
```

Creates:
- `~/.claude/teams/{team-name}/config.json`
- `~/.claude/tasks/{team-name}/`

### `Task` (spawn teammate)

```yaml
Task:
  subagent_type: string      # required teammate type
  team_name: string          # required team name
  name: string               # unique name inside the team
  description: string        # required 3-5 word summary
  prompt: string             # required task and context
  mode: string               # optional permission mode
  model: string              # optional model id
  run_in_background: boolean # optional async spawn flag
  max_turns: integer         # optional turn cap
```

#### `subagent_type`

| Type | Tools |
|------|-------|
| `general-purpose` | full toolset |
| `Explore` | read-only |
| `Plan` | read-only |
| `Bash` | shell only |

#### `mode`

| Mode | Meaning |
|------|---------|
| `bypassPermissions` | auto-approve tools for low-risk work |
| `plan` | teammate must request plan approval |
| `default` | ask the user when approval is needed |
| `acceptEdits` | auto-approve file edits |
| `dontAsk` | run without asking |
| `delegate` | delegation mode |

#### `model`

| Model | Meaning |
|-------|---------|
| `sonnet` | default |
| `opus` | highest capability |
| `haiku` | lightest option |

## Task Tools

### `TaskCreate`

```yaml
TaskCreate:
  subject: string        # required imperative title
  description: string    # required task details
  activeForm: string     # recommended in-progress label
```

### `TaskUpdate`

```yaml
TaskUpdate:
  taskId: string         # required task id
  status: string         # pending | in_progress | completed | deleted
  subject: string        # optional title update
  description: string    # optional description update
  activeForm: string     # optional active label update
  owner: string          # teammate name
  addBlockedBy: [string] # task ids that block this task
  addBlocks: [string]    # task ids blocked by this task
  metadata: object       # optional metadata
```

### `TaskList`

```yaml
TaskList: {}
```

Expected fields:
- `id`
- `subject`
- `status`
- `owner`
- `blockedBy`

### `TaskGet`

```yaml
TaskGet:
  taskId: string
```

## Messaging

### Direct message

```yaml
SendMessage:
  type: "message"
  recipient: string
  content: string
  summary: string
```

### Broadcast

```yaml
SendMessage:
  type: "broadcast"
  content: string
  summary: string
```

### Shutdown request

```yaml
SendMessage:
  type: "shutdown_request"
  recipient: string
  content: string
```

### Shutdown response

```yaml
SendMessage:
  type: "shutdown_response"
  request_id: string
  approve: boolean
  content: string
```

### Plan approval response

```yaml
SendMessage:
  type: "plan_approval_response"
  request_id: string
  recipient: string
  approve: boolean
  content: string
```

### `TeamDelete`

```yaml
TeamDelete: {}
```

`TeamDelete` fails if active members remain.

## Data Structures

### `config.json`

```json
{
  "team_name": "feature-auth",
  "description": "Parallel implementation team for auth",
  "members": [
    {
      "name": "backend-impl",
      "agentId": "abc-123",
      "agentType": "general-purpose"
    }
  ]
}
```

Always reference teammates by `name`, not `agentId`.

### Task directory

`~/.claude/tasks/{team-name}/` stores the team task list. Manage it through `TaskList`, `TaskGet`, `TaskCreate`, and `TaskUpdate`.

## Constraints and Notes

### Team size

- Recommended: `2-4`
- Hard maximum: `10`
- `5+` requires user confirmation

### Cost

- Every teammate is a separate Claude instance.
- `broadcast` costs `N x` direct messages.
- Use `haiku` aggressively for lightweight work.

### Message delivery

- Teammate messages are delivered automatically.
- Teammates become `idle` at the end of a turn; this is normal.
- You can message an idle teammate and wake it back up.

### Hub-spoke rule

- Rally is the hub.
- Teammates do not communicate directly.
- All team communication flows through Rally.

### File operations

- `Explore` and `Plan` cannot edit files.
- Use `general-purpose` for implementation.
- Ownership is enforced by prompt discipline, not by the API itself.

### Display modes

- `in-process`: shown inside the main process
- `split-pane`: shown in an IDE-integrated split view

Display mode is currently chosen by the system.
