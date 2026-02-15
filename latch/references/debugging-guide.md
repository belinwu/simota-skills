# Hook Debugging Guide

## Debug Mode

### Enable Debug Logging

```bash
claude --debug
```

Debug mode shows:
- Hook registration at startup
- Hook execution logs (which hooks fire, when)
- Input/output JSON for each hook
- Timing information (execution duration)
- Error details and stack traces

### Review Loaded Hooks

Use the `/hooks` command inside Claude Code to see all currently loaded hooks:
- Which events have hooks registered
- Matcher patterns per event
- Hook type (prompt/command) for each

---

## Manual Testing

### Test Command Hook Scripts

Test hooks outside Claude Code by piping JSON to stdin:

```bash
# Test a PreToolUse hook for Write
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/test.txt","content":"hello"},"session_id":"test","cwd":"/tmp","hook_event_name":"PreToolUse"}' | bash ~/.claude/hooks/your-hook.sh

echo "Exit code: $?"
```

### Test with Realistic Input

```bash
# PreToolUse for Bash
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /tmp/old"},"session_id":"test","cwd":"/home/user/project","hook_event_name":"PreToolUse"}' | bash ~/.claude/hooks/validate-bash.sh

# PostToolUse for Write
echo '{"tool_name":"Write","tool_input":{"file_path":"src/main.ts"},"tool_result":"File written successfully","hook_event_name":"PostToolUse"}' | bash ~/.claude/hooks/auto-lint.sh

# SessionStart
CLAUDE_PROJECT_DIR=/home/user/project CLAUDE_ENV_FILE=/tmp/test-env bash ~/.claude/hooks/load-project-context.sh
```

### Validate JSON Output

Ensure hook scripts output valid JSON:

```bash
output=$(echo '{"tool_name":"Write","tool_input":{"file_path":"/test"}}' | bash ~/.claude/hooks/your-hook.sh)
echo "$output" | jq .
```

If `jq` fails to parse, the hook output is malformed.

---

## Common Errors and Solutions

### Error 1: Hook Not Executing

**Symptoms:** Hook seems to be ignored, no effect observed.

**Causes & fixes:**
1. **Session not restarted** — Hooks load at session start. Restart Claude Code after editing settings.json.
2. **JSON syntax error in settings.json** — Validate: `jq . ~/.claude/settings.json`
3. **Matcher doesn't match** — Check case sensitivity. `"write"` does not match `Write`.
4. **Hook nested incorrectly** — Ensure hooks are under `"hooks"` key in settings.json.

### Error 2: JSON Parse Error in Hook Output

**Symptoms:** `claude --debug` shows JSON parse errors.

**Causes & fixes:**
1. **Script outputs non-JSON** — Ensure only JSON goes to stdout. Use `>&2` for debug prints.
2. **Unescaped characters** — Escape quotes and newlines in JSON strings.
3. **Mixed stdout/stderr** — Blocking hooks (exit 2) should write JSON to stderr, not stdout.

**Fix pattern:**
```bash
# BAD: debug output mixed with JSON
echo "Debug: checking file..."
echo '{"decision": "approve"}'

# GOOD: debug to stderr, JSON to stdout
echo "Debug: checking file..." >&2
echo '{"decision": "approve"}'
```

### Error 3: Hook Timeout

**Symptoms:** Hook execution takes too long and gets killed.

**Causes & fixes:**
1. **No timeout set** — Add explicit `"timeout": N` (seconds).
2. **Script does heavy I/O** — Optimize: cache results, minimize file reads.
3. **Network calls** — Add timeouts to curl/wget: `curl --max-time 5`.
4. **Waiting for input** — Ensure `input=$(cat)` is only called once and data is consumed.

### Error 4: Exit Code Mismatch

**Symptoms:** Hook blocks when it shouldn't, or doesn't block when it should.

**Causes & fixes:**
1. **Wrong exit code** — `exit 0` = success, `exit 2` = block, other = non-blocking error.
2. **`set -e` causing early exit** — A failing command in the script causes `exit 1` (non-blocking error, not a block). Use explicit error handling.
3. **Piped commands** — `set -o pipefail` can cause unexpected exit codes.

**Fix pattern:**
```bash
#!/bin/bash
set -uo pipefail  # Note: -e omitted intentionally for control

input=$(cat)
# ... validation logic ...

if [ "$should_block" = "true" ]; then
  echo '{"decision":"deny","reason":"Blocked"}' >&2
  exit 2  # Explicit block
fi

exit 0  # Explicit success
```

### Error 5: Parallel Execution Issues

**Symptoms:** Hooks produce inconsistent results, race conditions.

**Causes & fixes:**
1. **Shared state** — Hooks within a matcher group run in parallel. Don't share temp files between parallel hooks.
2. **Order dependency** — Never assume hook execution order.
3. **Resource contention** — Use unique temp file names (include `$$` PID).

**Fix pattern:**
```bash
# BAD: shared temp file
echo "result" > /tmp/hook-state

# GOOD: PID-scoped temp file
echo "result" > "/tmp/hook-state-$$"
```

---

## Troubleshooting Checklist

When a hook isn't working:

1. **Verify settings.json is valid JSON:** `jq . ~/.claude/settings.json`
2. **Restart Claude Code** after any settings change
3. **Check `/hooks`** to confirm hook is loaded
4. **Run `claude --debug`** to see hook execution details
5. **Test script manually** with `echo '{...}' | bash script.sh`
6. **Check exit code:** `echo $?` after manual test
7. **Validate output JSON:** pipe to `jq .`
8. **Check file permissions:** `chmod +x script.sh`
9. **Check shebang line:** First line should be `#!/bin/bash`
10. **Review stderr vs stdout:** Blocking output goes to stderr
