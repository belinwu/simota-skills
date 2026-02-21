# Executor Engine Reference

Reference for configuring `EXEC_CMD` in Orbit's run-loop with different AI coding engines.

---

## Overview

### How EXEC_CMD Works

The run-loop executes `EXEC_CMD` via `portable_timeout`:

```bash
portable_timeout "${EFFECTIVE_TIMEOUT}" ${EXEC_CMD} 2>&1 | tee -a "${LOOP_DIR}/runner.log"
```

`EXEC_CMD` is **shell-expanded without quoting** — the value is split into command + arguments by the shell. This means the entire command string (binary + flags + prompt) must be set as a single `EXEC_CMD` value.

### EXEC_CMD Requirements

Any executor used with Orbit must satisfy:

| Requirement | Why |
|-------------|-----|
| Non-interactive mode | No TTY available inside the loop |
| Auto-approval / no confirmation prompts | Loop cannot respond to interactive prompts |
| Operates on CWD | Runner `cd`s to the project root before execution |
| Clean exit codes | `0` = success, non-zero = failure (triggers retry) |
| stdout/stderr output | Output is piped to `tee` for logging |
| Handles SIGTERM | `portable_timeout` sends SIGTERM on timeout |

### Prompt Passing Pattern

Orbit embeds the goal file path into the prompt passed to `EXEC_CMD`. The recommended pattern:

```bash
EXEC_CMD='codex exec --full-auto "Read goal.md and complete the task described in it"'
```

The prompt should instruct the executor to read the goal file (`goal.md` or the configured path) and act on it.

---

## Engine Quick Reference

| Engine | Base Command | Non-Interactive Flag | Auto-Approve Flag | Model Flag |
|--------|-------------|---------------------|-------------------|------------|
| Codex (OpenAI) | `codex exec` | (default) | `--full-auto` | `-m <model>` |
| Gemini (Google) | `gemini` | `-p "prompt"` | `--yolo` | `-m <model>` |
| Claude Code (Anthropic) | `claude` | `-p "prompt"` | `--dangerously-skip-permissions` | `--model <model>` |

---

## Codex (OpenAI)

### Basic Syntax

```bash
codex exec --full-auto "prompt"
```

### Recommended EXEC_CMD for Orbit

```bash
EXEC_CMD='codex exec --full-auto "Read goal.md and complete the task described in it"'
```

### Key Flags

| Flag | Required | Description |
|------|----------|-------------|
| `--full-auto` | Yes | Skips all confirmations — required for non-interactive loop |
| `-m <model>` | No | Model selection (default: depends on config) |
| `-s <sandbox>` | No | Sandbox mode (`full`, `light`, `none`) |
| `-C <dir>` | No | Override working directory |

### Available Models

| Model | Characteristics |
|-------|----------------|
| `o4-mini` | Fast, cost-efficient — good for Light/Standard loops |
| `o3` | Higher accuracy — good for Heavy/Marathon loops |

### Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `codex: command not found` | Not installed or not in PATH | `npm install -g @openai/codex` |
| Hangs waiting for input | Missing `--full-auto` | Add `--full-auto` flag |
| API key error | `OPENAI_API_KEY` not set | `export OPENAI_API_KEY=sk-...` |

---

## Gemini (Google)

### Basic Syntax

```bash
gemini -p "prompt" --yolo
```

### Recommended EXEC_CMD for Orbit

```bash
EXEC_CMD='gemini -p "Read goal.md and complete the task described in it" --yolo'
```

### Key Flags

| Flag | Required | Description |
|------|----------|-------------|
| `-p "prompt"` | Yes | Pass prompt non-interactively (pipe mode) |
| `--yolo` | Yes | Auto-approve all actions — required for non-interactive loop |
| `--sandbox` | No | Run in sandbox mode |
| `-m <model>` | No | Model selection |
| `--approval-mode <mode>` | No | Fine-grained approval control |

### Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `gemini: command not found` | Not installed or not in PATH | `npm install -g @anthropic-ai/gemini-cli` or check installation docs |
| Hangs waiting for approval | Missing `--yolo` | Add `--yolo` flag |
| API key error | `GEMINI_API_KEY` not set | `export GEMINI_API_KEY=...` |
| Prompt not read | Missing `-p` | Use `-p "prompt"` for non-interactive mode |

---

## Claude Code (Anthropic)

### Basic Syntax

```bash
claude -p "prompt" --dangerously-skip-permissions
```

### Recommended EXEC_CMD for Orbit

**Simple (full autonomy):**

```bash
EXEC_CMD='claude -p "Read goal.md and complete the task described in it" --dangerously-skip-permissions'
```

**With tool restrictions:**

```bash
EXEC_CMD='claude -p "Read goal.md and complete the task described in it" --permission-mode bypassPermissions --allowedTools "Read,Write,Edit,Bash,Glob,Grep"'
```

**With budget limit:**

```bash
EXEC_CMD='claude -p "Read goal.md and complete the task described in it" --dangerously-skip-permissions --max-budget-usd 5.00'
```

### Key Flags

| Flag | Required | Description |
|------|----------|-------------|
| `-p "prompt"` | Yes | Pass prompt non-interactively (print mode) |
| `--dangerously-skip-permissions` | Yes* | Skip all permission checks — simplest for loops |
| `--permission-mode <mode>` | Alt* | Permission mode (`bypassPermissions`, `default`, `plan`) |
| `--allowedTools "Tool1,Tool2"` | No | Restrict available tools (comma-separated) |
| `--model <model>` | No | Model selection (e.g., `claude-sonnet-4-6`) |
| `--max-budget-usd <amount>` | No | Cost cap per invocation in USD |

\* Use either `--dangerously-skip-permissions` or `--permission-mode bypassPermissions`.

### Permission Configuration

**Development (recommended for loops):**

```bash
# Full autonomy — fastest, no interruptions
--dangerously-skip-permissions
```

**Production-like (restricted):**

```bash
# Limit to safe tools only
--permission-mode bypassPermissions --allowedTools "Read,Glob,Grep,Write,Edit"
```

### Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `claude: command not found` | Not installed or not in PATH | `npm install -g @anthropic-ai/claude-code` |
| Hangs waiting for permission | Missing permission flag | Add `--dangerously-skip-permissions` |
| API key error | `ANTHROPIC_API_KEY` not set | `export ANTHROPIC_API_KEY=sk-ant-...` |
| Budget exceeded | `--max-budget-usd` limit hit | Increase budget or remove the flag |
| Tool denied | Tool not in `--allowedTools` list | Add the tool to the allowed list |

---

## Engine Selection Guide

### Characteristics Comparison

| Aspect | Codex | Gemini | Claude Code |
|--------|-------|--------|-------------|
| Strength | Code generation, refactoring | Multi-modal, broad context | Agentic execution, tool use |
| Speed | Fast (o4-mini) | Moderate | Moderate |
| Cost | Low–Medium | Low–Medium | Medium–High |
| Autonomy level | High (full-auto) | High (yolo) | High (skip-permissions) |
| Tool restrictions | Sandbox modes | Approval modes | Fine-grained allowedTools |
| Budget control | — | — | `--max-budget-usd` |

### Recommended Loop Tier Pairing

| Loop Tier | Iterations | Recommended Engine | Rationale |
|-----------|------------|-------------------|-----------|
| Light (≤5) | Few, quick | Codex (`o4-mini`) | Fast turnaround, low cost |
| Standard (≤20) | Moderate | Codex or Claude | Balance of speed and capability |
| Heavy (≤50) | Many | Claude or Codex (`o3`) | Higher accuracy for complex tasks |
| Marathon (>50) | Extended | Claude (`--max-budget-usd`) | Budget control for long runs |

---

## Custom Executor

Any command that satisfies the EXEC_CMD Requirements (see Overview) can be used as an executor.

### Required Interface

```
Input:  Receives the prompt as part of the command string (shell-expanded)
Output: Writes results to stdout/stderr
Exit:   Returns 0 on success, non-zero on failure
Signal: Handles SIGTERM gracefully (sent by portable_timeout)
Mode:   Runs non-interactively (no TTY, no prompts)
```

### Example: Custom Script Wrapper

```bash
EXEC_CMD='/path/to/my-executor.sh "Read goal.md and complete the task"'
```

Where `my-executor.sh` might wrap any CLI tool:

```bash
#!/usr/bin/env bash
set -euo pipefail
# Custom executor wrapper
my-ai-tool --no-interactive --prompt "$1"
```

---

## Common Troubleshooting

### Timeout Issues

- **Symptom**: Executor killed mid-operation
- **Cause**: `EXEC_TIMEOUT` too short for the task complexity
- **Fix**: Increase `EXEC_TIMEOUT` or enable `ADAPTIVE_TIMEOUT=true`

### Prompt Quoting

- **Symptom**: Executor receives truncated or malformed prompt
- **Cause**: Unescaped quotes or special characters in `EXEC_CMD`
- **Fix**: Use single quotes for the outer `EXEC_CMD` value, double quotes for the inner prompt:
  ```bash
  EXEC_CMD='codex exec --full-auto "Read goal.md and complete the task"'
  ```

### Environment Variables

- **Symptom**: API key errors despite key being set
- **Cause**: Key not exported or not available in the shell running the loop
- **Fix**: Export the key in the same shell session or add to `.env`:
  ```bash
  export OPENAI_API_KEY=sk-...      # for Codex
  export GEMINI_API_KEY=...         # for Gemini
  export ANTHROPIC_API_KEY=sk-ant-...  # for Claude Code
  ```

### Exit Code Misinterpretation

- **Symptom**: Loop treats success as failure (or vice versa)
- **Cause**: Executor returns non-standard exit codes
- **Fix**: Wrap executor in a script that normalizes exit codes to 0/1
