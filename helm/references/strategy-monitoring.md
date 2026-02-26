# Strategy Monitoring (absorbed from Compass)

Strategy execution monitoring, assumption tracking, and OKR cascading methodology. Previously a standalone agent (Compass), now integrated as a Helm capability.

---

## When to Apply

Use after Helm produces a strategy/roadmap:
- Track execution progress against plan
- Monitor assumption validity over time
- Cascade strategy into team-level OKRs
- Detect strategic drift early

---

## Framework: ANCHOR → TRACK → ALERT → CASCADE

| Phase | Purpose | Key Actions |
|-------|---------|-------------|
| **ANCHOR** | 戦略基準点の確立 | Map assumptions to measurable metrics, set baseline KPIs |
| **TRACK** | 進捗・前提の追跡 | Monitor milestones, KPI actuals vs targets, assumption validity |
| **ALERT** | 乖離の早期検知 | Drift detection, assumption breach alerts, health reporting |
| **CASCADE** | OKR展開 | Strategy → Company OKR → Team OKR → Individual KR |

---

## Assumption Monitoring

### Assumption → Metric Mapping

```markdown
| Assumption | Metric | Threshold | Status |
|-----------|--------|-----------|--------|
| "Market grows 15%/yr" | Industry revenue data | <10% = WATCH, <5% = BREACH | VALID |
| "Users prefer mobile" | Mobile usage % | <50% = WATCH | VALID |
| "Competitor doesn't enter" | Competitor announcements | Any entry = BREACH | VALID |
```

### Assumption States

```
VALID → WATCH → BREACH
  ↑               │
  └───────────────┘ (can recover if conditions improve)
```

| State | Meaning | Action |
|-------|---------|--------|
| **VALID** | Assumption holds | Continue as planned |
| **WATCH** | Warning threshold crossed | Prepare contingency |
| **BREACH** | Assumption invalidated | Trigger strategy revision |

---

## Alert Levels

| Level | Trigger | Response |
|-------|---------|----------|
| 🟢 **GREEN** | All KPIs on track, assumptions valid | Continue, monitor |
| 🟡 **YELLOW** | 1-2 KPIs off by <20%, assumption in WATCH | Investigate, prepare contingency |
| 🔴 **RED** | Major KPI miss (>20%), assumption BREACH | Escalate to Magi for decision |
| ⚫ **BLACK** | Multiple BREACH, strategy fundamentally invalid | Full strategy revision needed |

---

## OKR Cascading

### Top-Down Decomposition

```
Company Objective: "Be the market leader in X"
├── Company KR1: Revenue $10M (measurable)
│   ├── Sales Team OKR: Close 200 deals
│   │   └── Individual KR: 20 demos/month
│   └── Product Team OKR: Launch feature Y
│       └── Individual KR: Ship by Q2
├── Company KR2: NPS > 50
│   └── Support Team OKR: MTTR < 4hrs
└── Company KR3: 95% retention
    └── Product Team OKR: Reduce churn triggers
```

### Alignment Score

```
Alignment = (KRs with clear parent link / Total KRs) × 100

Target: > 80%
Warning: < 60% (orphan KRs suggest misalignment)
```

---

## Strategy Health Report Template

```markdown
## Strategy Health Report — [Period]

### Overall Status: [🟢/🟡/🔴/⚫]

### KPI Dashboard
| KPI | Target | Actual | Trend | Status |
|-----|--------|--------|-------|--------|
| [KPI] | [target] | [actual] | [↑↓→] | [🟢🟡🔴] |

### Assumption Monitor
| Assumption | Status | Last Checked | Notes |
|-----------|--------|-------------|-------|
| [assumption] | [VALID/WATCH/BREACH] | [date] | [context] |

### Drift Analysis
- Strategy drift score: [0-100]
- Areas of concern: [list]
- Recommended actions: [list]

### Next Review: [date]
```
