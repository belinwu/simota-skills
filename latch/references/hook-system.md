# Claude Code Hook System Reference

## Overview

Claude Code hooks are event-driven automation scripts that execute in response to Claude Code lifecycle events. They enable validation, policy enforcement, context injection, and workflow automation without modifying Claude Code itself.

**Two configuration formats:**
- **settings.json** (primary for end users): `~/.claude/settings.json` — direct event keys at top level
- **hooks.json** (for plugins): `hooks/hooks.json` — wrapped in `{"hooks": {...}}` container

Latch primarily manages settings.json format.

---

## Hook Events (9 Events)

| # | Event | Trigger Timing | Primary Use |
|---|-------|---------------|-------------|
| 1 | **PreToolUse** | Before any tool executes | Approve, deny, or modify tool calls |
| 2 | **PostToolUse** | After tool completes | React to results, provide feedback, log |
| 3 | **UserPromptSubmit** | When user submits a prompt | Add context, validate, or block prompts |
| 4 | **Stop** | When main agent considers stopping | Validate task completeness |
| 5 | **SubagentStop** | When subagent considers stopping | Ensure subagent task completion |
| 6 | **SessionStart** | When Claude Code session begins | Load context, set environment |
| 7 | **SessionEnd** | When session ends | Cleanup, logging, state preservation |
| 8 | **PreCompact** | Before context compaction | Preserve critical information |
| 9 | **Notification** | When Claude sends notifications | React to notifications, logging |

### Event Details

#### PreToolUse
- **Prompt hooks supported:** Yes
- **Can block:** Yes (permissionDecision: "deny")
- **Can modify input:** Yes (updatedInput field)
- **Input fields:** `tool_name`, `tool_input`
- **Output format:**
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow|deny|ask",
    "updatedInput": {"field": "modified_value"}
  },
  "systemMessage": "Explanation for Claude"
}
```

#### PostToolUse
- **Prompt hooks supported:** Yes
- **Can block:** No (informational only)
- **Input fields:** `tool_name`, `tool_input`, `tool_result`
- **Output behavior:** Exit 0 → stdout in transcript; Exit 2 → stderr fed to Claude; systemMessage in context

#### UserPromptSubmit
- **Prompt hooks supported:** Yes
- **Can block:** Yes
- **Input fields:** `user_prompt`

#### Stop / SubagentStop
- **Prompt hooks supported:** Yes
- **Can block:** Yes (decision: "block")
- **Input fields:** `reason`
- **Output format:**
```json
{
  "decision": "approve|block",
  "reason": "Explanation",
  "systemMessage": "Additional context"
}
```

#### SessionStart
- **Prompt hooks supported:** No (command only)
- **Special capability:** Environment variable persistence via `$CLAUDE_ENV_FILE`
```bash
echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"
```

#### SessionEnd
- **Prompt hooks supported:** No (command only)
- **Use for:** Cleanup, final logging, state save

#### PreCompact
- **Prompt hooks supported:** No (command only)
- **Use for:** Inject critical context to preserve through compaction

#### Notification
- **Prompt hooks supported:** No (command only)
- **Use for:** External notification forwarding, audit logging

---

## Hook Types

### Prompt-Based Hooks (Recommended for complex logic)

```json
{
  "type": "prompt",
  "prompt": "Evaluate if this tool use is appropriate: $TOOL_INPUT",
  "timeout": 30
}
```

- Uses LLM reasoning for context-aware decisions
- Supported on: PreToolUse, PostToolUse, UserPromptSubmit, Stop, SubagentStop
- Default timeout: 30 seconds
- Access input via: `$TOOL_INPUT`, `$TOOL_RESULT`, `$USER_PROMPT`

**When to use:** Complex validation logic, context-dependent decisions, natural language policy enforcement

### Command Hooks (For fast deterministic checks)

```json
{
  "type": "command",
  "command": "bash /path/to/script.sh",
  "timeout": 60
}
```

- Executes bash commands, receives JSON via stdin
- Supported on: All 9 events
- Default timeout: 60 seconds

**When to use:** Fast checks, file operations, external tool integration, performance-critical validation

---

## Settings.json Configuration Structure

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Validate file write safety.",
            "timeout": 15
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/validate-bash.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verify task completion: tests run, build succeeded."
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/load-context.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

**Key structure rules:**
- `hooks` key at top level of settings.json
- Each event key contains an array of matcher groups
- Each matcher group has `matcher` (string) and `hooks` (array)
- Each hook has `type`, `command`/`prompt`, and optional `timeout`

---

## Matcher Patterns

### Exact Match
```json
"matcher": "Write"
```

### OR Combination (Multiple tools)
```json
"matcher": "Read|Write|Edit"
```

### Wildcard (All tools/events)
```json
"matcher": "*"
```

### Regex Pattern
```json
"matcher": "mcp__.*__delete.*"
```

### Common Matcher Examples

| Pattern | Matches |
|---------|---------|
| `"Write"` | Write tool only |
| `"Write\|Edit"` | Write or Edit |
| `"Read\|Write\|Edit"` | All file operations |
| `"Bash"` | Bash commands |
| `"mcp__.*"` | All MCP tools |
| `"mcp__plugin_asana_.*"` | Specific plugin's MCP tools |
| `"mcp__.*__delete.*"` | MCP delete operations |
| `"*"` | Everything |

**Note:** Matchers are case-sensitive.

---

## Hook Input Format (stdin JSON)

All hooks receive JSON via stdin with common fields:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.txt",
  "cwd": "/current/working/dir",
  "permission_mode": "ask|allow",
  "hook_event_name": "PreToolUse"
}
```

**Event-specific additional fields:**

| Event | Additional Fields |
|-------|------------------|
| PreToolUse | `tool_name`, `tool_input` |
| PostToolUse | `tool_name`, `tool_input`, `tool_result` |
| UserPromptSubmit | `user_prompt` |
| Stop / SubagentStop | `reason` |

---

## Hook Output Format

### Standard Output (All hooks)
```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Message for Claude"
}
```

- `continue`: If false, halt processing (default true)
- `suppressOutput`: Hide output from transcript (default false)
- `systemMessage`: Message shown to Claude

### Exit Codes

| Code | Meaning | Behavior |
|------|---------|----------|
| 0 | Success | stdout shown in transcript |
| 2 | Blocking error | stderr fed back to Claude |
| Other | Non-blocking error | Logged but doesn't block |

---

## Environment Variables

Available in all command hooks:

| Variable | Description | Availability |
|----------|-------------|-------------|
| `$CLAUDE_PROJECT_DIR` | Project root path | All hooks |
| `$CLAUDE_PLUGIN_ROOT` | Plugin directory (for portable paths) | Plugin hooks |
| `$CLAUDE_ENV_FILE` | File to persist env vars | SessionStart only |
| `$CLAUDE_CODE_REMOTE` | Set if running remotely | All hooks |

---

## Lifecycle Constraints

### Hooks Load at Session Start
- Changes to hook configuration require restarting Claude Code
- Cannot hot-swap hooks during a session
- Editing settings.json won't affect current session

### Session Restart Required
1. Edit hook configuration
2. Exit Claude Code session
3. Restart: `claude` or `cc`
4. Verify with `/hooks` command

### Parallel Execution
- All matching hooks within a matcher group run in parallel
- Hooks don't see each other's output
- Non-deterministic ordering
- Design for independence — never rely on execution order

### Validation at Startup
- Invalid JSON causes loading failure
- Missing scripts cause warnings
- Syntax errors reported in `claude --debug` mode
- Use `/hooks` to review loaded hooks

### Timeout Defaults
- Command hooks: 60 seconds
- Prompt hooks: 30 seconds
- Always set explicit timeouts for production hooks
