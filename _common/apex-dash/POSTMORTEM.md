# apex-dash — Postmortem & Lore Handoff

Defines how a completed apex run is converted into a markdown postmortem and forwarded to Lore as training data.

---

## 1. Purpose

A finished apex run is rich with signals (phase durations, agent costs, Risk Gate verdicts, orbit convergence, errors) that are valuable beyond the moment of viewing. The postmortem turns one run's transient log into:

- An attachable summary for the apex PR
- A learning corpus row for Lore (`METAPATTERNS.md` updates, agent-decay detection)
- An archive entry for trend analysis (Pulse, Beacon)

## 2. Trigger

| Trigger | Behaviour |
|---------|-----------|
| `run_end` event arrives | Server emits a `note` event referencing the generated postmortem path |
| `GET /api/postmortem/:run` | Synchronous generation, returned as `text/markdown` |
| `bun run scripts/postmortem.ts --run=<run-id>` | CLI generation, useful for archival batches |

Generation is **idempotent**: re-running rewrites `postmortem.md` based on the current events.jsonl.

## 3. Output

Path: `<repo>/.agents/apex/<run-id>/postmortem.md`

### Structure

```
---
run_id: apex-YYYYMMDD-HHMMSS-xxx
goal: <text>
mode: AUTORUN_FULL | AUTORUN | GUIDED | INTERACTIVE
scope: Lite | Standard | Full
status: completed | aborted | error
started_at: <ISO8601>
ended_at: <ISO8601>
duration: hh:mm:ss
final_engine: claude_code | codex_cli
verdict: Go | Conditional-Go | No-Go | (none)
spec_version: <hash>
---

# Postmortem: <goal>

## Outcome
- 1-3 line narrative summary

## Phase Breakdown
| Phase | Status | Duration |

## Agents Executed
| Agent | Phase | Engine | Status | Duration |

## Risk Gate
- Verdict, omen / ripple / echo axes

## Orbit (Phase 6)
- Iteration count
- Final convergence
- Total cost (cost_per_task summed)
- Circuit transitions

## Engine Boundary Crossings
| From | To | At | Reason |

## Bottleneck
- Top time-consuming agent
- Top time-consuming phase
- Recommendation hint

## Errors / Warnings
| Severity | Source | Message | At |

## Lore Handoff Candidates
- Patterns surfaced in this run (anti-patterns, novel sequences)
- Agent decay signals (>2σ slowdowns vs history)
```

## 4. Generation Algorithm

```
1. Read events.jsonl line by line
2. Fold events through the same reducer used by the dashboard client
3. Compute aggregates:
     phase_durations[p]   = phase_exit.ts - phase_enter.ts
     agent_durations[a]   = agent_end.ts - agent_start.ts
     bottleneck_agent     = argmax(agent_durations)
     bottleneck_phase     = argmax(phase_durations)
     orbit_total_cost     = sum(iter.cost_per_task) over orbit_iter events
     final_convergence    = last orbit_iter.convergence
     engine_history       = engine_switch events in order
     errors               = error events with severity >= warn
4. Render markdown using the template above
5. Write atomically (write tmp + rename)
6. Emit a "note" event referencing the path: meta.text="postmortem at <path>"
```

## 5. Lore Handoff

When `LORE_HANDOFF=1` is set in the server env:

1. Append a single-line summary to `<repo>/.agents/lore/apex-history.md`:
   ```
   - 2026-04-30 apex-... goal="passkey login" status=completed duration=29:32 verdict=Go bottleneck=accord(P4)
   ```
2. Emit a `note` event with `meta.lore_handoff=true` and `meta.path` pointing to the postmortem
3. Lore consumes both:
   - Cross-run pattern extraction → `METAPATTERNS.md`
   - Agent decay detection → propose evolution actions to Darwin

Lore handoff is **opt-in** to keep the local-tool default truly local.

## 6. Privacy

- Snippets in events are already capped at 280 chars (`EVENTS.md §2`); the postmortem inherits the same constraint
- Source code, file paths, and shell commands appear by reference (`output_ref`), never inline contents
- No environment variables or secrets are read during generation

## 7. Related

- `EVENTS.md` — schema being read
- `INTEGRATION.md §2.4` — emit points that feed the reducer
- `DESIGN.md §10` — extensibility surface
- `sample/server/postmortem.ts` — reference implementation
- `sample/events/apex-20260430-120000-a3f/postmortem.md` — generated example
