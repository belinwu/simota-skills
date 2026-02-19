# Hook Recipes

Proven, ready-to-use hook configurations for common workflows. Each recipe includes the settings.json snippet, explanation, and customization notes.

---

## Security Recipes

### S1: File Write Security Validation

Block writes to sensitive files and system directories.

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "File path: $TOOL_INPUT.file_path. Verify: 1) Not in /etc or system directories 2) Not .env, credentials, or key files 3) Path doesn't contain '..' traversal 4) Not overwriting critical config without reason. Return 'approve' or 'deny' with reason.",
          "timeout": 15
        }
      ]
    }
  ]
}
```

**Risk level:** Low (non-blocking by default, prompt-based)
**Customization:** Add project-specific protected paths to the prompt.

### S2: Bash Command Safety Validation

Detect and block dangerous shell commands.

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Command: $TOOL_INPUT.command. Check for: 1) rm -rf with broad paths 2) Destructive database commands (DROP, DELETE without WHERE) 3) Permission changes (chmod 777) 4) Network operations to unknown hosts 5) Package installs from untrusted sources. Return 'approve', 'deny', or 'ask' for user confirmation.",
          "timeout": 15
        }
      ]
    }
  ]
}
```

**Risk level:** Medium (may use 'ask' to pause)
**Customization:** Add approved command patterns for your project.

### S3: Secret Leak Prevention

Detect secrets in file writes using command hook.

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/check-secrets.sh",
          "timeout": 10
        }
      ]
    }
  ]
}
```

**Script (`~/.claude/hooks/check-secrets.sh`):**
```bash
#!/bin/bash
set -euo pipefail
input=$(cat)
content=$(echo "$input" | jq -r '.tool_input.content // empty')

if [ -z "$content" ]; then
  exit 0
fi

# Check for common secret patterns
if echo "$content" | grep -qiE '(api[_-]?key|password|secret|token|private[_-]?key)\s*[:=]\s*["\x27]?[A-Za-z0-9+/]{20,}'; then
  echo '{"hookSpecificOutput":{"permissionDecision":"deny"},"systemMessage":"Potential secret detected in content. Remove secrets before writing."}' >&2
  exit 2
fi

# ...
```

### S4: MCP Delete Operation Guard

Require confirmation for all MCP delete operations.

```json
{
  "PreToolUse": [
    {
      "matcher": "mcp__.*__delete.*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "MCP deletion detected. Tool: $TOOL_INPUT. Verify: Is deletion intentional? Can it be undone? Are there backups? Return 'ask' to confirm with user unless clearly safe.",
          "timeout": 15
        }
      ]
    }
  ]
}
```

---

## Quality Recipes

### Q1: Test Execution Enforcement (Stop)

Block stopping if code was changed but tests weren't run.

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Review the session transcript. If code was modified (Write/Edit tools used), verify that tests were executed (test commands in Bash). If no tests were run after code changes, block with reason 'Tests must be run after code changes'. If no code was changed or tests passed, approve.",
          "timeout": 30
        }
      ]
    }
  ]
}
```

**Risk level:** Medium (blocks completion)
**Note:** This is a blocking hook — Claude will be asked to run tests before stopping.

### Q2: Auto Lint After Edit (PostToolUse)

Run linter automatically after file edits.

```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/auto-lint.sh",
          "timeout": 30
        }
      ]
    }
  ]
}
```

**Script (`~/.claude/hooks/auto-lint.sh`):**
```bash
#!/bin/bash
set -euo pipefail
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

if [ -z "$file_path" ] || [ ! -f "$file_path" ]; then
  exit 0
fi

# Run appropriate linter
case "$file_path" in
  *.ts|*.tsx|*.js|*.jsx)
    npx eslint "$file_path" --fix 2>&1 || true
    ;;
  *.py)
# ...
```

### Q3: Type Check Enforcement

Ensure TypeScript type checking passes after code changes.

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/check-types.sh",
          "timeout": 60
        }
      ]
    }
  ]
}
```

**Script (`~/.claude/hooks/check-types.sh`):**
```bash
#!/bin/bash
cd "$CLAUDE_PROJECT_DIR" || exit 0

# Only run if TypeScript project
if [ ! -f "tsconfig.json" ]; then
  exit 0
fi

result=$(npx tsc --noEmit 2>&1)
if [ $? -ne 0 ]; then
  echo "{\"decision\":\"block\",\"reason\":\"TypeScript errors found\",\"systemMessage\":\"$result\"}" >&2
  exit 2
fi

exit 0
```

### Q4: Build Verification

Ensure build succeeds before stopping.

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Check if code was modified during this session. If Write/Edit tools were used, verify the project was built successfully (npm run build, cargo build, go build, etc). If not built, block and request a build step.",
          "timeout": 30
        }
      ]
    }
  ]
}
```

---

## Context Recipes

### C1: Project Context Auto-Load (SessionStart)

Automatically detect project type and load relevant context.

```json
{
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/load-project-context.sh",
          "timeout": 10
        }
      ]
    }
  ]
}
```

**Script (`~/.claude/hooks/load-project-context.sh`):**
```bash
#!/bin/bash
cd "$CLAUDE_PROJECT_DIR" || exit 0

context=""

# Detect project type
if [ -f "package.json" ]; then
  context="Node.js project."
  echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"

  # Detect package manager
  if [ -f "pnpm-lock.yaml" ]; then
    context="$context Uses pnpm."
    echo "export PKG_MANAGER=pnpm" >> "$CLAUDE_ENV_FILE"
  elif [ -f "bun.lockb" ]; then
# ...
```

### C2: PreCompact Critical Info Preservation

Save important context before compaction.

```json
{
  "PreCompact": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/preserve-context.sh",
          "timeout": 10
        }
      ]
    }
  ]
}
```

**Script (`~/.claude/hooks/preserve-context.sh`):**
```bash
#!/bin/bash
# Read PROJECT.md and inject as system message for context preservation
project_file="$CLAUDE_PROJECT_DIR/.agents/PROJECT.md"

if [ -f "$project_file" ]; then
  content=$(head -50 "$project_file")
  echo "{\"systemMessage\":\"Critical project context (preserve through compaction): $content\"}"
fi

exit 0
```

---

## Workflow Recipes

### W1: Notification Logging

Log all Claude notifications for audit.

```json
{
  "Notification": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/log-notification.sh",
          "timeout": 5
        }
      ]
    }
  ]
}
```

**Script (`~/.claude/hooks/log-notification.sh`):**
```bash
#!/bin/bash
input=$(cat)
timestamp=$(date -Iseconds)
echo "$timestamp | notification | $input" >> ~/.claude/logs/notifications.log
exit 0
```

### W2: Temporary Hook (Flag File Control)

Hook that only runs when a flag file exists.

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/strict-bash-check.sh",
          "timeout": 10
        }
      ]
    }
  ]
}
```

**Script (`~/.claude/hooks/strict-bash-check.sh`):**
```bash
#!/bin/bash
FLAG_FILE="$CLAUDE_PROJECT_DIR/.enable-strict-validation"

# Quick exit if not enabled
if [ ! -f "$FLAG_FILE" ]; then
  exit 0
fi

# Strict validation when enabled
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# Block all rm commands in strict mode
if echo "$command" | grep -qE '\brm\b'; then
  echo '{"hookSpecificOutput":{"permissionDecision":"deny"},"systemMessage":"Strict mode: rm commands blocked. Remove .enable-strict-validation to disable."}' >&2
# ...
```

**Usage:**
```bash
# Enable strict mode
touch .enable-strict-validation

# Disable strict mode
rm .enable-strict-validation
# Restart Claude Code for changes to take effect
```

### W3: Session Audit Trail

Log session start and end for tracking.

```json
{
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash -c 'echo \"$(date -Iseconds) | session_start | $CLAUDE_PROJECT_DIR\" >> ~/.claude/logs/sessions.log'",
          "timeout": 5
        }
      ]
    }
  ],
  "SessionEnd": [
    {
// ...
```

---

## Tech Stack Recommended Sets

### Node.js / TypeScript

```json
{
  "hooks": {
    "SessionStart": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "bash ~/.claude/hooks/load-project-context.sh", "timeout": 10}]}
    ],
    "PreToolUse": [
      {"matcher": "Write|Edit", "hooks": [{"type": "prompt", "prompt": "Validate file write: not .env, not node_modules, not dist/. Return 'approve' or 'deny'.", "timeout": 10}]},
      {"matcher": "Bash", "hooks": [{"type": "prompt", "prompt": "Check bash command safety. Block: rm -rf node_modules (use package manager), npm publish without --dry-run. Return 'approve' or 'ask'.", "timeout": 10}]}
    ],
    "PostToolUse": [
      {"matcher": "Write|Edit", "hooks": [{"type": "command", "command": "bash ~/.claude/hooks/auto-lint.sh", "timeout": 30}]}
    ],
    "Stop": [
      {"matcher": "*", "hooks": [{"type": "prompt", "prompt": "If code was changed, verify: 1) Tests run 2) TypeScript compiles 3) No console.log left in production code. Approve or block.", "timeout": 30}]}
    ]
// ...
```

### Go

```json
{
  "hooks": {
    "SessionStart": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "bash ~/.claude/hooks/load-project-context.sh", "timeout": 10}]}
    ],
    "PreToolUse": [
      {"matcher": "Write|Edit", "hooks": [{"type": "prompt", "prompt": "Validate Go file write: proper package declaration, no vendor/ modifications. Return 'approve' or 'deny'.", "timeout": 10}]}
    ],
    "PostToolUse": [
      {"matcher": "Write|Edit", "hooks": [{"type": "command", "command": "bash -c 'input=$(cat); fp=$(echo \"$input\" | jq -r \".tool_input.file_path\"); [[ \"$fp\" == *.go ]] && gofmt -w \"$fp\" 2>&1 || true'", "timeout": 15}]}
    ],
    "Stop": [
      {"matcher": "*", "hooks": [{"type": "prompt", "prompt": "If Go code was changed, verify: 1) go build succeeds 2) go test passes 3) go vet clean. Approve or block.", "timeout": 30}]}
    ]
  }
// ...
```

### Rust

```json
{
  "hooks": {
    "SessionStart": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "bash ~/.claude/hooks/load-project-context.sh", "timeout": 10}]}
    ],
    "PreToolUse": [
      {"matcher": "Write|Edit", "hooks": [{"type": "prompt", "prompt": "Validate Rust file write: not modifying Cargo.lock directly, proper module structure. Return 'approve' or 'deny'.", "timeout": 10}]}
    ],
    "PostToolUse": [
      {"matcher": "Write|Edit", "hooks": [{"type": "command", "command": "bash -c 'input=$(cat); fp=$(echo \"$input\" | jq -r \".tool_input.file_path\"); [[ \"$fp\" == *.rs ]] && rustfmt \"$fp\" 2>&1 || true'", "timeout": 15}]}
    ],
    "Stop": [
      {"matcher": "*", "hooks": [{"type": "prompt", "prompt": "If Rust code was changed, verify: 1) cargo check passes 2) cargo test passes 3) No clippy warnings. Approve or block.", "timeout": 60}]}
    ]
  }
// ...
```

### Python

```json
{
  "hooks": {
    "SessionStart": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "bash ~/.claude/hooks/load-project-context.sh", "timeout": 10}]}
    ],
    "PreToolUse": [
      {"matcher": "Write|Edit", "hooks": [{"type": "prompt", "prompt": "Validate Python file write: not .env, not __pycache__, not venv/. Return 'approve' or 'deny'.", "timeout": 10}]},
      {"matcher": "Bash", "hooks": [{"type": "prompt", "prompt": "Check: pip install without --dry-run, dangerous subprocess calls, eval/exec usage. Return 'approve' or 'ask'.", "timeout": 10}]}
    ],
    "PostToolUse": [
      {"matcher": "Write|Edit", "hooks": [{"type": "command", "command": "bash -c 'input=$(cat); fp=$(echo \"$input\" | jq -r \".tool_input.file_path\"); [[ \"$fp\" == *.py ]] && python -m ruff check \"$fp\" --fix 2>&1 || true'", "timeout": 15}]}
    ],
    "Stop": [
      {"matcher": "*", "hooks": [{"type": "prompt", "prompt": "If Python code was changed, verify: 1) pytest passes 2) ruff/mypy clean 3) No breakpoint() left. Approve or block.", "timeout": 30}]}
    ]
// ...
```

---

## Combining Recipes

Recipes are composable. To combine multiple recipes, merge the event arrays:

```json
{
  "hooks": {
    "PreToolUse": [
      { "comment": "S1: File write security" },
      { "matcher": "Write|Edit", "hooks": [{"type": "prompt", "prompt": "..."}] },
      { "comment": "S2: Bash safety" },
      { "matcher": "Bash", "hooks": [{"type": "prompt", "prompt": "..."}] },
      { "comment": "S4: MCP guard" },
      { "matcher": "mcp__.*__delete.*", "hooks": [{"type": "prompt", "prompt": "..."}] }
    ],
    "Stop": [
      { "comment": "Q1: Test enforcement" },
      { "matcher": "*", "hooks": [{"type": "prompt", "prompt": "..."}] }
    ],
    "SessionStart": [
// ...
```

**Tip:** Start with 1-2 recipes and add gradually. Too many hooks can slow down the workflow.
