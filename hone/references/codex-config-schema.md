# Codex Config Schema

**Purpose:** Comprehensive reference for all Codex CLI configuration keys, default values, and recommended settings.
**Read when:** Auditing `~/.codex/config.toml` or proposing configuration changes.

---

## Config File Location

Primary: `~/.codex/config.toml`

---

## Core Settings

| Key | Type | Default | Description | Recommendation |
|-----|------|---------|-------------|----------------|
| `model` | string | `"o4-mini"` | Model identifier for completions | Use latest stable model; verify availability |
| `provider` | string | `"openai"` | API provider | Match to model availability |
| `reasoning_effort` | string | `"medium"` | Reasoning depth: `"low"`, `"medium"`, `"high"` | `"medium"` for general use; `"high"` for complex tasks |
| `approval_mode` | string | `"suggest"` | Permission level: `"suggest"`, `"auto-edit"`, `"full-auto"` | Start with `"suggest"`, escalate per project |

## Behavior Settings

| Key | Type | Default | Description | Recommendation |
|-----|------|---------|-------------|----------------|
| `notify` | boolean | `true` | Desktop notifications on completion | Keep `true` for long tasks |
| `verbose` | boolean | `false` | Verbose output mode | Enable for debugging only |

## Trust Levels

```toml
[project_trust]
"/path/to/project" = "trust"     # full-auto allowed
"/path/to/project2" = "untrust"  # suggest only
```

| Level | Behavior | Use when |
|-------|----------|----------|
| `"trust"` | Allows `full-auto` mode | Personal projects, well-tested repos |
| `"untrust"` | Forces `suggest` mode | Third-party code, sensitive repos |

### Trust Level Audit Criteria

- **Stale paths**: Projects that no longer exist on disk
- **Over-trust**: Sensitive repos (financial, auth) marked as trusted
- **Under-trust**: Personal projects unnecessarily restricted
- **Wildcard paths**: Overly broad trust patterns

## Feature Flags

```toml
[features]
flag_name = true
```

### Known Feature Flags

| Flag | Default | Description | Recommendation |
|------|---------|-------------|----------------|
| `stream` | `true` | Streaming output | Keep enabled |
| `memory` | `false` | Conversation memory | Enable if available |
| `mcp` | `true` | MCP server support | Keep enabled if using MCP |
| `file_opener` | `true` | Open files in editor | Keep enabled |

> **Note:** Feature flags evolve rapidly. Always verify against the latest Codex CLI release notes.

## MCP Server Configuration

```toml
[[mcp_servers]]
name = "server-name"
command = "/path/to/server"
args = ["--flag", "value"]
env = { KEY = "value" }
```

### MCP Audit Criteria

- **Accessibility**: Server binary exists and is executable
- **Version**: Server is up-to-date
- **Necessity**: Server is actively used
- **Security**: No secrets in plaintext args/env

## Other Configuration Files

| File | Purpose | Audit focus |
|------|---------|-------------|
| `~/.codex/instructions.md` | Global instructions for Codex | Non-empty, clear, up-to-date |
| `~/.codex/AGENTS.md` | Agent behavior definitions | Priority clarity, no redundancy |
| `~/.codex/rules/` | Rule files (glob-scoped) | No duplicates, valid globs |

---

## Version History

| Date | Change | Source |
|------|--------|--------|
| Initial | Schema documented from Codex CLI v0.1 | T2: openai/codex GitHub |

> This schema should be refreshed when major Codex CLI versions are released. Check `references/web-sources.md` for staleness thresholds.
