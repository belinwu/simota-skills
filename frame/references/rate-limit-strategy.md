# Frame Rate Limit Strategy

Plan-specific rate limits, budgeting strategies, and optimization patterns.

---

## Plan Limits

| Plan | Requests/min | Daily Limit | Concurrent | Notes |
|------|-------------|-------------|------------|-------|
| **Starter** | 5 | 500 | 1 | Single component focus recommended |
| **Professional** | 20 | 2,000 | 3 | Batch by page, selective screenshots |
| **Organization** | 60 | 10,000 | 10 | Full file extraction feasible |
| **Enterprise** | 120 | Unlimited | 20 | No practical constraints |

---

## Request Cost by Tool

| Tool | Relative Cost | Info Density | Priority |
|------|--------------|-------------|----------|
| `get_design_context` | 1 request | **High** — full structure + styles | Extract first |
| `get_variable_defs` | 1 request | **High** — all variables in file | Extract early |
| `get_metadata` | 1 request | **Medium** — file-level info | Once per file |
| `get_screenshot` | 1 request | **Low** — visual only | Selective use |
| `whoami` | 1 request | **Low** — auth check | Once per session |
| `get_code_connect_map` | 1 request | **Medium** — mapping data | On demand |
| `get_code_connect_suggestions` | 1 request | **Medium** — AI suggestions | On demand |
| `add_code_connect_map` | 1 request | **Low** — single mapping | Per mapping |
| `send_code_connect_mappings` | 1 request | **Low** — batch send | Once per sync |
| `create_design_system_rules` | 1 request | **High** — system rules | On demand |
| `get_figjam` | 1 request | **High** — full board content | On demand |
| `generate_diagram` | 1 request | **Medium** — generated output | On demand |
| `generate_figma_design` | 1+ requests | **Low** — generative | Ask first |

---

## Budget Planning

### Per-Task Budget Estimates

| Task Type | Estimated Calls | Starter OK? | Pro OK? |
|-----------|----------------|-------------|---------|
| Single component analysis | 3-5 | ✅ | ✅ |
| Page-level extraction | 10-20 | ⚠️ Tight | ✅ |
| Full file extraction | 30-100+ | ❌ | ⚠️ |
| Variable/token extraction | 2-3 | ✅ | ✅ |
| Code Connect audit | 5-10 | ✅ | ✅ |
| Design system rules | 3-5 | ✅ | ✅ |
| FigJam extraction | 2-3 | ✅ | ✅ |

### Budget Allocation Strategy

```
Total Budget = Daily Limit - Safety Buffer (10%)

For a Professional plan (2,000/day):
  Available: 1,800 requests

  Allocation:
  - CONNECT phase: 2 (whoami + initial metadata)
  - SURVEY phase: 5 (metadata + shallow scans)
  - EXTRACT phase: ~1,750 (bulk of budget)
  - PACKAGE phase: 0 (local processing)
  - DELIVER phase: 0 (local processing)

  Reserve: 43 requests (buffer for retries/follow-ups)
```

---

## Optimization Patterns

### Pattern 1: Context-First (Default)

Maximize information per request by prioritizing `get_design_context`.

```
Strategy:
1. get_design_context (full structure) → 1 call, rich data
2. get_variable_defs (if tokens needed) → 1 call
3. get_screenshot (only for handoff) → selective calls

Avoid: Multiple get_screenshot calls when get_design_context provides sufficient detail.
```

### Pattern 2: Incremental Extraction

For large files, extract page by page to stay within limits.

```
Strategy:
1. get_metadata → identify pages
2. For each page (by priority):
   a. get_design_context (depth=1) → structure overview
   b. get_design_context (specific nodes) → deep extraction
   c. get_screenshot (key frames only)
3. Track budget between pages
4. Stop if budget < 10% remaining

Budget check between each page iteration.
```

### Pattern 3: Screenshot-Minimal

For Starter plans or low-budget situations.

```
Strategy:
1. get_design_context → structural data only
2. get_variable_defs → token data
3. Skip get_screenshot entirely
4. Describe visual layout from structural data in handoff

Trade-off: Downstream agents don't get visual reference.
Mitigation: Provide Figma URLs for manual reference.
```

### Pattern 4: Code Connect Focus

For Code Connect management tasks.

```
Strategy:
1. get_code_connect_map → current mappings
2. get_code_connect_suggestions → AI recommendations
3. add_code_connect_map → per new mapping
4. send_code_connect_mappings → batch sync

Minimal screenshot/context calls needed.
```

---

## Rate Limit Error Handling

| Scenario | Detection | Response |
|----------|-----------|----------|
| Approaching limit (>80% used) | Track request count | Reduce scope, skip optional screenshots |
| Soft limit hit (429 warning) | HTTP 429 response | Pause 60s, resume with reduced scope |
| Daily limit reached | Persistent 429 | Stop extraction, report partial results |
| Burst limit hit | Rapid 429 sequence | Implement 1-request-per-second throttle |

### Recovery Procedure

```markdown
## Rate Limit Recovery

1. **Immediate**: Stop all pending requests
2. **Assess**: Calculate remaining budget for the day
3. **Prioritize**: Identify minimum viable extraction
4. **Resume**: After rate window reset (60s for per-minute limits)
5. **Report**: Include rate usage in delivery report

If daily limit reached:
- Deliver partial results with clear gaps noted
- Suggest resuming extraction next day
- Provide Figma URLs for manual reference of unextracted content
```

---

## Monitoring Template

```markdown
## Rate Usage Report

**Session**: [YYYY-MM-DD HH:MM - HH:MM]
**Plan**: [Plan type]

| Metric | Value |
|--------|-------|
| Total requests | [N] |
| Budget used | [N%] |
| Remaining (daily) | [N] |
| Peak rate | [N/min] |
| Throttle events | [N] |

### Request Breakdown
| Tool | Calls | % of Total |
|------|-------|-----------|
| get_design_context | [N] | [%] |
| get_variable_defs | [N] | [%] |
| get_screenshot | [N] | [%] |
| get_metadata | [N] | [%] |
| Other | [N] | [%] |
```
