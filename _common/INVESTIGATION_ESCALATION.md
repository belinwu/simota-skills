# Investigation Escalation Protocol

調査系スキルクラスター（Scout, Lens, Rewind, Specter）間のエスカレーション標準。

## Escalation Flow

```
[Vague Report / Unknown Issue]
    │
    ▼
  Lens (SCOPE→SURVEY) ─── 把握で十分 ─── DONE
    │
    ▼ 異常パターン・潜在バグ発見
  Scout (TRIAGE→TRACE) ─── バグ特定 ─── Builder handoff
    │                         │
    │ 履歴調査必要             │ 並行性疑い
    ▼                         ▼
  Rewind (bisect/archaeology)  Specter (SCAN→ANALYZE→SCORE)
    │                         │
    ▼ リソース系変更発見       ▼ 開始時期特定必要
    └───→ Specter             └───→ Rewind
```

## Ownership Rule

1バグ＝1リーダースキル。他は支援ロール。リーダーは最初に TRIAGE/SCOPE を完了したスキルが担当する。

## Unified Confidence Scale

| Level | Score | Evidence Threshold | Reporting Rule |
|-------|-------|--------------------|----------------|
| `HIGH` | ≥ 0.8 | 3+ independent evidence | Report as confirmed |
| `MEDIUM` | 0.5–0.79 | 2 independent evidence | Report as estimated; add verification steps |
| `LOW` | < 0.5 | ≤1 evidence | Report as hypothesis; list missing information |

## Cross-Cluster Handoff Formats

### LENS_TO_SCOUT_HANDOFF

```yaml
LENS_TO_SCOUT_HANDOFF:
  investigation_id: "[unique-id]"
  discovery_type: "[anomaly_pattern | potential_bug | dead_code_risk | comprehension_debt_hotspot]"
  location: "[file:line references]"
  evidence: "[what was observed during comprehension]"
  severity_estimate: "[HIGH | MEDIUM | LOW]"
  suggested_investigation_mode: "[Focused Hunt | History-Led | Observability-Led | Multi-Engine | Cascading Failure]"
```

### SCOUT_TO_LENS_HANDOFF

```yaml
SCOUT_TO_LENS_HANDOFF:
  investigation_id: "[unique-id]"
  request_type: "[context_needed | flow_trace_needed | dependency_map_needed]"
  bug_context: "[what is known so far]"
  specific_questions: "[what Scout needs to understand]"
  scope_hint: "[files/modules to focus on]"
```

### REWIND_TO_SPECTER_HANDOFF

```yaml
REWIND_TO_SPECTER_HANDOFF:
  investigation_id: "[unique-id]"
  bisect_result: "[commit hash and change summary]"
  change_type: "[resource_management | concurrency_modification | lock_change | async_pattern_change]"
  evidence: "[what the commit changed]"
  suggested_scan_focus: "[race_condition | memory_leak | resource_leak | deadlock]"
```

### SPECTER_TO_REWIND_HANDOFF

```yaml
SPECTER_TO_REWIND_HANDOFF:
  investigation_id: "[unique-id]"
  issue_type: "[race_condition | memory_leak | resource_leak | deadlock]"
  request: "[onset_identification | change_history | blame_analysis]"
  suspected_components: "[files/modules]"
  evidence: "[current analysis findings]"
```

## Stall Protocol (Cross-Cluster)

1. Probe 3回 → 仮説切替
2. 全仮説消費 → 隣接スキルにエスカレーション
3. 2スキル間で 3+ 往復 → Nexus に昇格（Agent Tennis 防止）

## Duplicate Investigation Prevention

- 同一バグに対して複数スキルが同時調査を開始しない
- エスカレーション時は Investigation_ID を引き継ぎ、重複を防止
- リーダースキルが全エスカレーション結果を集約し、最終レポートに統合
