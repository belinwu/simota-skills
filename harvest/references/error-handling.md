# Error Handling Reference for Harvest

Harvestのデータ収集における信頼性を確保するためのエラーハンドリング戦略。

---

## Error Categories

| カテゴリ | エラー種別 | 復旧可能性 | 優先度 |
|---------|-----------|:----------:|:------:|
| **Authentication** | 401 Unauthorized, Token expired | ✅ High | P0 |
| **Rate Limiting** | 403 Rate limit exceeded | ✅ High | P0 |
| **Network** | Connection timeout, DNS failure | ✅ Medium | P1 |
| **API** | 500 Server error, 502 Bad Gateway | ✅ Medium | P1 |
| **Data** | Invalid JSON, Missing fields | ⚠️ Partial | P2 |
| **Permission** | 404 Not found, 403 Forbidden (repo) | ❌ Low | P3 |

---

## Detection Patterns

### Authentication Errors

```bash
# gh auth status でトークン状態を確認
check_auth() {
  if ! gh auth status &>/dev/null; then
    echo "ERROR: GitHub authentication failed"
    echo "ACTION: Run 'gh auth login' to re-authenticate"
    return 1
  fi
  return 0
}

# 使用例
if ! check_auth; then
  _STEP_COMPLETE:
    Agent: Harvest
    Status: BLOCKED
# ...
```

### Rate Limit Detection

```bash
# レート制限の事前チェック
check_rate_limit() {
  local remaining=$(gh api rate_limit --jq '.resources.core.remaining' 2>/dev/null)
  local reset=$(gh api rate_limit --jq '.resources.core.reset' 2>/dev/null)

  if [ -z "$remaining" ]; then
    echo "WARNING: Could not check rate limit"
    return 1
  fi

  if [ "$remaining" -lt 100 ]; then
    local reset_time=$(date -r "$reset" "+%H:%M:%S" 2>/dev/null || date -d "@$reset" "+%H:%M:%S")
    echo "WARNING: Rate limit low ($remaining remaining, resets at $reset_time)"
    return 2
  fi
# ...
```

### Timeout Detection

```bash
# タイムアウト付きコマンド実行
execute_with_timeout() {
  local timeout_sec=${1:-60}
  shift
  local cmd="$@"

  if command -v timeout &>/dev/null; then
    # GNU timeout (Linux)
    timeout "$timeout_sec" $cmd
  else
    # macOS alternative
    perl -e 'alarm shift @ARGV; exec @ARGV' "$timeout_sec" $cmd
  fi

  local exit_code=$?
# ...
```

---

## Recovery Strategies

### 1. Exponential Backoff Retry

```bash
# 指数バックオフ付きリトライ
retry_with_backoff() {
  local max_attempts=${1:-3}
  local base_delay=${2:-5}
  shift 2
  local cmd="$@"

  local attempt=1
  while [ $attempt -le $max_attempts ]; do
    echo "Attempt $attempt/$max_attempts: $cmd"

    if eval "$cmd"; then
      return 0
    fi

# ...
```

### 2. Rate Limit Wait and Retry

```bash
# レート制限時の待機とリトライ
wait_for_rate_limit() {
  local reset=$(gh api rate_limit --jq '.resources.core.reset' 2>/dev/null)
  local now=$(date +%s)
  local wait_sec=$((reset - now + 5))  # 5秒余裕を持たせる

  if [ $wait_sec -gt 0 ] && [ $wait_sec -lt 3600 ]; then
    echo "Waiting ${wait_sec}s for rate limit reset..."
    sleep $wait_sec
    return 0
  elif [ $wait_sec -ge 3600 ]; then
    echo "ERROR: Rate limit reset too far in future (${wait_sec}s)"
    return 1
  fi
  return 0
# ...
```

### 3. Partial Data Recovery

```bash
# 部分的なデータ取得失敗時の復旧
fetch_prs_with_fallback() {
  local limit=${1:-100}
  local fields="number,title,state,author,createdAt,mergedAt,additions,deletions"

  # 全フィールドで試行
  local result
  result=$(gh pr list --state all --limit "$limit" --json "$fields" 2>&1)

  if [ $? -ne 0 ]; then
    echo "WARNING: Full field fetch failed, trying minimal fields..."

    # 最小フィールドでリトライ
    local minimal_fields="number,title,state,author"
    result=$(gh pr list --state all --limit "$limit" --json "$minimal_fields" 2>&1)
# ...
```

---

## Error Response Templates

### For Nexus AUTORUN Mode

```yaml
# 認証エラー
_STEP_COMPLETE:
  Agent: Harvest
  Status: BLOCKED
  Output: Authentication failed - token expired or invalid
  Error:
    Code: AUTH_FAILED
    Message: "GitHub CLI not authenticated"
    Recovery: "User must run 'gh auth login'"
  Next: USER_ACTION

# レート制限
_STEP_COMPLETE:
  Agent: Harvest
  Status: PARTIAL
# ...
```

### For NEXUS_HANDOFF

```yaml
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: Harvest
- Summary: Data collection failed due to rate limiting
- Key findings:
  - Collected 50 PRs before rate limit
  - Rate limit resets at 10:30 UTC
- Artifacts:
  - Partial data: pr-list-partial-2024-01-15.json
- Risks:
  - Incomplete report if not retried
- Error details:
  - Code: RATE_LIMITED
  - Remaining: 0
  - Reset: 2024-01-15T10:30:00Z
# ...
```

---

## Health Check Protocol

収集開始前に実行する健全性チェック:

```bash
# 完全ヘルスチェック
harvest_health_check() {
  local errors=0

  echo "=== Harvest Health Check ==="

  # 1. gh CLI インストール確認
  if ! command -v gh &>/dev/null; then
    echo "❌ gh CLI not installed"
    ((errors++))
  else
    echo "✅ gh CLI installed ($(gh --version | head -1))"
  fi

  # 2. 認証確認
# ...
```

---

## Error Logging

エラーをジャーナルに記録する際のフォーマット:

```markdown
## 2024-01-15 - Rate Limit During Weekly Report

**Error:** RATE_LIMITED
**Context:** Weekly report generation for org/project
**Impact:** Only 50/200 PRs collected
**Resolution:** Waited 15 minutes, completed with full data
**Prevention:** Consider incremental collection for large repos
```

---

## Graceful Degradation

データ収集が部分的に失敗した場合の段階的縮退:

| 失敗レベル | 対応 | レポート品質 |
|-----------|------|:-----------:|
| **Full success** | 全フィールド取得 | 100% |
| **Missing additions/deletions** | 変更統計なしで続行 | 80% |
| **Missing dates** | 期間フィルタ不可、全件で続行 | 60% |
| **Missing author** | 貢献者分析スキップ | 50% |
| **Only PR numbers** | 件数のみのレポート | 20% |
| **Total failure** | エラーレポート出力 | 0% |

```bash
# 縮退レベルの判定
determine_degradation_level() {
  local data="$1"

  if echo "$data" | jq -e '.[0].additions' &>/dev/null; then
    echo "FULL"
  elif echo "$data" | jq -e '.[0].createdAt' &>/dev/null; then
    echo "NO_STATS"
  elif echo "$data" | jq -e '.[0].author' &>/dev/null; then
    echo "NO_DATES"
  elif echo "$data" | jq -e '.[0].number' &>/dev/null; then
    echo "MINIMAL"
  else
    echo "FAILED"
  fi
# ...
```

---

## Integration with Triage

重大なエラーが発生した場合、Triageへのエスカレーション:

```yaml
HARVEST_TO_TRIAGE_ESCALATION:
  trigger: "critical_error"
  error:
    code: "AUTH_REVOKED"
    message: "GitHub token has been revoked"
    timestamp: "2024-01-15T10:00:00Z"
  context:
    task: "Weekly PR report generation"
    repository: "org/project"
    user_impact: "All automated reports blocked"
  recommended_actions:
    - "Re-authenticate with 'gh auth login'"
    - "Verify token permissions in GitHub settings"
    - "Check for security alerts"
```
