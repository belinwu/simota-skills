# Output Formats

Templates for Titan's output artifacts.

---

## TITAN_COMPLETE

Final delivery output when the entire product lifecycle is complete.

```markdown
## TITAN_COMPLETE

### Product Summary
- **Goal**: [Original user goal, verbatim]
- **Scope**: [S/M/L/XL]
- **Phases Completed**: [N/Total]
- **Duration**: [Phases executed, with timestamps if available]

### SUCCESS_CRITERIA Evaluation
| Criteria | Target | Actual | Status |
|----------|--------|--------|--------|
| [Criteria 1] | [Target metric] | [Achieved metric] | ✅/❌ |

### Deliverables
| Category | Artifact | Location |
|----------|----------|----------|
| Code | [Feature/module name] | [File paths] |
| Tests | [Test suite name] | [File paths] |
| Docs | [Document name] | [File paths] |
| Config | [Config name] | [File paths] |

### Architecture Decisions Summary
| Decision | Choice | Risk Score | Rationale |
|----------|--------|------------|-----------|
| [DEC-001] | [Choice made] | [Score] | [Brief rationale] |

### Quality Metrics
- **Test coverage**: [N%]
- **Security audit**: PASS / FAIL (details: [summary])
- **Performance targets**: MET / UNMET (details: [summary])
- **Code quality gate**: PASS / FAIL (Warden verdict)

### Known Limitations
- [Limitation]: [Reason + mitigation]

### Recommended Next Steps (EVOLVE Phase)
1. [Action item with priority]

### Risk Log Summary
- **Total decisions logged**: [N]
- **High-risk decisions**: [N]
- **Final risk budget**: [N/100]
- **User escalations used**: [N/1]
- **Stall recoveries**: L1:[N] L2:[N] L3:[N] L4:[N]
```

---

## TITAN_PHASE_COMPLETE

Output at each phase transition.

```markdown
## TITAN_PHASE_COMPLETE: [PHASE_NAME]

### Phase Summary
- **Phase**: [Phase N of Total]
- **Epics completed**: [N/Total]
- **Agents deployed**: [Agent list]
- **Duration**: [Start → End]

### Key Decisions
| Decision | Choice | Risk |
|----------|--------|------|
| [DEC-NNN] | [Choice] | [Score] |

### Artifacts Produced
| Type | File | Description |
|------|------|-------------|
| [code/test/doc/config] | [path] | [what it is] |

### Exit Criteria Verification
| Criteria | Status | Notes |
|----------|--------|-------|
| [Criteria 1] | ✅/❌ | [Details if failed] |

### Velocity Report
- Epic completion rate: [N%]
- Stall count: [N]
- Rally usage: [N teams launched]

### Next Phase Preview
- **Phase**: [Next phase name]
- **Planned Epics**: [Count]
- **Key agents**: [Primary agents]
- **Expected challenges**: [Known risks]
```

---

## TITAN_STATE

Persisted state format (written to `.agents/titan-state.md`).

```markdown
## TITAN_STATE
- **Project**: [Project name]
- **Goal**: [Original user goal, verbatim]
- **Scope**: S / M / L / XL
- **Current Phase**: [Phase name]
- **Phase Progress**: [Current phase N / Total phases]
- **Epic Progress**: [Completed / Total in current phase]
- **Risk Budget**: [Cumulative score / 100]
- **Stall Budget**:
  - Tactical: [Used / Limit per phase] (Project: [Used / 10])
  - Operational: [Used / Limit per phase] (Project: [Used / 5])
  - Strategic: [Used / Limit per phase] (Project: [Used / 3])
- **SUCCESS_CRITERIA**:
  - [Criteria 1]: [Target] → [Current status]
- **Blockers**: [Current blockers or "None"]
- **Next Action**: [Specific next step]
- **Decision Log**: [Path to decision log file]
- **Last Updated**: [YYYY-MM-DD HH:MM]

### Phase Status
| Phase | Status | Entry Date | Exit Date | Epics |
|-------|--------|------------|-----------|-------|
| DISCOVER | ✅/🔄/⏳/⏭️ | [date] | [date] | [N/N] |
| DEFINE | ... | ... | ... | ... |
| ARCHITECT | ... | ... | ... | ... |
| BUILD | ... | ... | ... | ... |
| HARDEN | ... | ... | ... | ... |
| VALIDATE | ... | ... | ... | ... |
| LAUNCH | ... | ... | ... | ... |
| GROW | ... | ... | ... | ... |
| EVOLVE | ... | ... | ... | ... |

### Current Roadmap
#### [Phase name] — [Status]
- [x] Epic 1: [Description]
- [ ] Epic 2: [Description] ← CURRENT
- [ ] Epic 3: [Description]
```

---

## Decision Log

Decision Log format → `references/decision-matrix.md`

---

## AUTORUN Step Output

```
_STEP_COMPLETE: Agent: Titan | Status: SUCCESS | Output: Phase [N] complete — [summary] | Next: Phase [N+1] / DONE
```

```
_AGENT_CONTEXT:
  Role: Titan
  Phase: [Current phase]
  Task: [Phase objective]
  State: [TITAN_STATE summary]
```
