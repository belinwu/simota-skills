# Claude Code Config Schema

**Purpose:** Comprehensive reference for all Claude Code configuration keys, default values, and recommended settings.
**Read when:** Auditing `~/.claude/` or proposing configuration changes.

---

## Config File Locations

| File | Scope | Format |
|------|-------|--------|
| `~/.claude/settings.json` | Global | JSON |
| `<project>/.claude/settings.json` | Project | JSON |
| `~/.claude/CLAUDE.md` | Global instructions | Markdown |
| `<project>/CLAUDE.md` | Project instructions | Markdown |
| `<project>/.claude/commands/` | Custom slash commands | Markdown |

---

## Global Settings (`~/.claude/settings.json`)

```json
{
  "permissions": {
    "allow": ["Bash(npm test)", "Read"],
    "deny": ["Bash(rm -rf *)"]
  },
  "env": {
    "CLAUDE_MODEL": "claude-sonnet-4-6",
    "ANTHROPIC_API_KEY": "..."
  },
  "mcpServers": {
    "server-name": {
      "command": "/path/to/server",
      "args": ["--flag", "value"],
      "env": { "KEY": "value" }
    }
  }
}
```

### Permissions

| Key | Type | Description | Recommendation |
|-----|------|-------------|----------------|
| `permissions.allow` | string[] | Tool patterns permitted without confirmation | Use specific patterns (e.g., `Bash(npm test)`) rather than broad `Bash` |
| `permissions.deny` | string[] | Tool patterns always denied | Deny destructive commands explicitly |

#### Permission Pattern Syntax

| Pattern | Meaning | Safety |
|---------|---------|--------|
| `"Read"` | Allow all file reads | Generally safe |
| `"Edit"` | Allow all file edits | Moderate risk — consider project scope |
| `"Bash(command*)"` | Allow specific bash commands matching glob | Scope as narrowly as possible |
| `"Bash"` | Allow ALL bash commands | High risk — avoid in global settings |
| `"mcp__server__tool"` | Allow specific MCP tool | Scope per server and tool |

#### Permission Audit Criteria

- **Over-permissive global**: Broad `Bash` allow in global settings is risky
- **Missing deny rules**: No explicit deny for destructive operations
- **Redundant rules**: Same pattern in both allow and deny (deny wins)
- **Stale patterns**: References to tools/servers that no longer exist

### Environment Variables

| Variable | Description | Recommendation |
|----------|-------------|----------------|
| `CLAUDE_MODEL` | Override default model | Set only if you need a specific model |
| `ANTHROPIC_API_KEY` | API authentication key | Use env var, never hardcode in settings |

## Project Settings (`<project>/.claude/settings.json`)

Same structure as global settings, applied per-project. Project settings are merged with global settings (project takes precedence).

```json
{
  "permissions": {
    "allow": ["Bash(npm test)", "Bash(npm run lint)"],
    "deny": []
  },
  "mcpServers": {},
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Pre-tool hook'"
          }
        ]
      }
    ]
  }
}
```

### Hooks (Reference Only)

> **Note:** Detailed hook design and debugging is handled by the **Latch** agent. Hone audits hooks configuration only for structural validity and security concerns.

| Event | Trigger | Hone audit scope |
|-------|---------|-----------------|
| `PreToolUse` | Before a tool executes | Check matcher validity, no secrets in commands |
| `PostToolUse` | After a tool executes | Check matcher validity, no secrets in commands |
| `Notification` | When a notification is sent | Check command validity |
| `Stop` | When agent stops | Check command validity |
| `SubagentStop` | When a subagent stops | Check command validity |

#### Hook Audit Criteria (Structural Only)

- **Validity**: Hook commands are executable and paths exist
- **Security**: No plaintext secrets in hook commands or environment
- **Matcher validity**: Tool matchers reference existing tools
- **Delegation**: Complex hook logic should be reviewed by Latch

## MCP Server Configuration

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@scope/mcp-server"],
      "env": { "API_KEY": "${env:API_KEY}" }
    }
  }
}
```

### MCP Audit Criteria

- **Accessibility**: Server command exists and is executable
- **Version**: Server packages are up-to-date
- **Necessity**: Server is actively used (not orphaned)
- **Security**: No plaintext secrets in args/env — use `${env:VAR}` syntax
- **Scope**: Global vs project MCP placement is appropriate

## CLAUDE.md Instruction Files

| File | Scope | Purpose | Audit focus |
|------|-------|---------|-------------|
| `~/.claude/CLAUDE.md` | Global | Global instructions for all projects | Non-empty, clear, up-to-date, no secrets |
| `<project>/CLAUDE.md` | Project | Project-level instructions | Relevant to project, no contradictions with global |
| `<project>/.claude/CLAUDE.md` | Project (hidden) | Alternative project instructions location | Check for duplicates with root CLAUDE.md |

### CLAUDE.md Audit Criteria

- **Existence**: At least one instruction file exists (global recommended)
- **Currency**: Content reflects current project state and tool capabilities
- **No secrets**: No API keys, tokens, or credentials in instruction files
- **No contradictions**: Project and global instructions are consistent
- **Reasonable length**: Excessively long files may degrade performance

## Custom Slash Commands

Location: `<project>/.claude/commands/` (project) or `~/.claude/commands/` (global)

Each `.md` file in the commands directory defines a custom slash command.

### Command Audit Criteria

- **File format**: Each command file is valid Markdown
- **Naming**: File names use clear, descriptive kebab-case
- **No secrets**: No hardcoded secrets in command templates
- **Parameter usage**: `$ARGUMENTS` placeholder used correctly

## Model Configuration

| Method | Scope | Description |
|--------|-------|-------------|
| `CLAUDE_MODEL` env var | Session | Override model for current session |
| `/model` command | Session | Interactive model selection |
| `settings.json` env block | Persistent | Set via env vars in settings |

### Current Model Identifiers

| Model | ID | Recommendation |
|-------|-----|----------------|
| Claude Opus 4.6 | `claude-opus-4-6` | Most capable; complex tasks |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | Balanced performance and speed |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Fast; simple tasks |

### Model Audit Criteria

- **Currency**: Model ID is valid and current (not deprecated)
- **Appropriateness**: Model matches typical task complexity
- **Override clarity**: If overridden, the reason is documented

## Authentication

| Method | Configuration | Use when |
|--------|--------------|----------|
| API Key | `ANTHROPIC_API_KEY` env var | Direct API access |
| Claude Pro/Team | OAuth via `claude login` | Subscription-based access |

### Auth Audit Criteria

- **Configured**: Authentication method is set up and working
- **No hardcoded keys**: `ANTHROPIC_API_KEY` not hardcoded in settings.json or CLAUDE.md
- **Env var security**: API keys use environment variables, not file literals

> **NEVER read:** `~/.claude/credentials.json`, `~/.claude/statsig/`, or any auth/session files.

---

## Version History

| Date | Change | Source |
|------|--------|--------|
| Initial | Schema documented from Claude Code v1.x | T2: anthropics/claude-code GitHub |

> This schema should be refreshed when major Claude Code versions are released. Check `references/web-sources.md` for staleness thresholds.
