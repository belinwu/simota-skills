# Frame Connection Setup

Figma MCP Server connection methods, configuration, and troubleshooting.

---

## Connection Methods

### Method 1: Remote MCP (API Key)

For Claude Desktop, Claude Code, or any MCP-compatible client.

**Prerequisites:**
- Figma Personal Access Token (Settings → Security → Personal access tokens)
- Node.js 18+ installed

**Setup:**

```json
// Claude Desktop: ~/Library/Application Support/Claude/claude_desktop_config.json
// Claude Code: .mcp.json or settings
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "figma-developer-mcp", "--stdio"],
      "env": {
        "FIGMA_API_KEY": "<YOUR_PERSONAL_ACCESS_TOKEN>"
      }
    }
  }
}
```

**Token Permissions Required:**
- File content (read)
- File metadata (read)
- Variables (read)
- Code Connect (read/write — if managing mappings)

---

### Method 2: Desktop Plugin (WebSocket)

For Figma Desktop app with real-time selection access.

**Prerequisites:**
- Figma Desktop app installed
- Figma Developer MCP plugin installed

**Setup:**
1. Open Figma Desktop
2. Install "Developer MCP" plugin from Community
3. Run plugin → Copy WebSocket URL
4. Configure MCP client with WebSocket transport

```json
{
  "mcpServers": {
    "figma": {
      "transport": "websocket",
      "url": "ws://localhost:3845"
    }
  }
}
```

**Advantages over Remote:**
- Access to current selection
- Real-time file state (no API delay)
- No rate limiting on local operations
- Variable resolution across files

---

## Connection Verification

Always verify connection in CONNECT phase:

```
# Step 1: Check MCP server availability
# (MCP client should list figma tools)

# Step 2: Verify identity and permissions
whoami()
# Expected: User info, plan type, team/org

# Step 3: Test basic operation
get_metadata(file_url="https://figma.com/file/KNOWN_FILE")
# Expected: File name, last modified, version
```

---

## Troubleshooting

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| "Tool not found" | MCP server not started | Restart MCP server, check config |
| "401 Unauthorized" | Token expired/invalid | Regenerate Personal Access Token |
| "403 Forbidden" | Insufficient permissions | Check token scopes, file access |
| "429 Too Many Requests" | Rate limit exceeded | Wait and retry, reduce scope |
| "File not found" | Invalid URL or no access | Verify URL, check sharing settings |
| "Node not found" | Invalid node_id | Use metadata to discover valid node IDs |
| WebSocket connection failed | Plugin not running | Open Figma Desktop, start plugin |
| Timeout on large files | File too complex | Extract by page/section, not whole file |

### Rate Limit Recovery

```
# When 429 received:
# 1. Stop all pending requests
# 2. Wait for rate window reset (typically 60 seconds)
# 3. Resume with reduced scope
# 4. Consider switching to page-by-page extraction
```

### Token Refresh

```
# Figma Personal Access Tokens don't expire by default
# But can be revoked. If auth fails:
# 1. Go to Figma → Settings → Security → Personal access tokens
# 2. Generate new token
# 3. Update MCP server config
# 4. Restart MCP server
```

---

## Security Best Practices

- **Never** hardcode Figma API keys in committed files
- Use environment variables or secret management
- Rotate tokens periodically (quarterly recommended)
- Use minimum required token scopes
- For CI/CD: use service account tokens, not personal tokens
- Audit token usage via Figma Admin (Organization/Enterprise plans)

---

## Environment-Specific Notes

### Claude Code

```bash
# Via environment variable
export FIGMA_API_KEY="figd_xxxxx"

# Or in .mcp.json at project root
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "figma-developer-mcp", "--stdio"],
      "env": {
        "FIGMA_API_KEY": "${FIGMA_API_KEY}"
      }
    }
  }
}
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Extract Figma context
  env:
    FIGMA_API_KEY: ${{ secrets.FIGMA_API_KEY }}
  run: |
    npx figma-developer-mcp extract --file $FIGMA_FILE_URL
```
