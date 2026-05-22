# Severity Rubric

How Hex translates raw findings into a single tier (`T1 Veil` → `T5 Calamity`). Used during the `SCORE` phase. Never assign tier by gut feel — always run the formula.

## Per-Category Score

For each of the 10 categories:

```
CategoryScore =  Weight  ×  Magnitude  ×  RecencyFactor
```

Where:

- `Weight`: category importance (table below)
- `Magnitude`: 0.0 (clean) → 1.0 (catastrophic), set during `SCAN`
- `RecencyFactor`: how active the affected code is. `1.5` if touched in last 30 days, `1.0` if 30–180 days, `0.6` if older than 180 days. Stale debt is still debt, but active debt bleeds.

## Category Weights

| # | Category | Weight | Rationale |
|---|----------|--------|-----------|
| 1 | Code Smells | 1.0 | Surface-level; visible but rarely critical alone |
| 2 | Duplication | 1.2 | Multiplies fix cost across copies |
| 3 | Cyclomatic Complexity | 1.3 | Drives bug density |
| 4 | Outdated Dependencies | 1.4 | Compounds with security debt |
| 5 | Test Coverage Gap | 1.5 | Gates safe refactor |
| 6 | TODO/FIXME/HACK | 0.8 | Self-reported; honesty signal |
| 7 | Architectural Violations | 1.8 | Hardest to remediate |
| 8 | Security Debt | 2.0 | Risk weighted highest |
| 9 | Performance Hotspots | 1.2 | User-visible but localized |
| 10 | Documentation Gap | 0.7 | Slows velocity, rarely breaks |

## Total Score and Tier

```
TotalScore = Σ CategoryScore
```

| Tier | Name | Score Range | Visual cue |
|------|------|-------------|------------|
| `T1` | Veil | < 1.0 | Translucent, faint |
| `T2` | Shade | 1.0 – 2.5 | Half-formed humanoid |
| `T3` | Wraith | 2.5 – 5.0 | Armored revenant |
| `T4` | Revenant | 5.0 – 8.0 | Hulking cursed body |
| `T5` | Calamity | > 8.0 | Deity-class composite |

## Override Rules

Tier may shift up by exactly **one** step when any of the following hold. Stack is not permitted (a single override max):

- **Critical CVE present** (CVSS ≥ 9.0): minimum `T3`
- **Active production incident** linked to a finding: minimum `T4`
- **Coverage < 30%** combined with weekly active changes: tier +1
- **Circular dependency in core module**: tier +1

Never downgrade tier from formula. Only upgrade.

## Dominant Category

Identify the single category contributing the most to `TotalScore` (highest `CategoryScore`). Record as `dominant_category` in the report — it drives the dominant motif in the character (e.g., security-dominant → toxic aura is the silhouette's primary feature).

## Per-Category Salience for Trait Surface

A trait gets rendered on the character only if its `CategoryScore ≥ 0.3`. Below that threshold the category is mentioned in the report but not visualized — keeps the character readable rather than a checklist of every minor smell.

## Output of SCORE

```yaml
score:
  total: 4.7
  tier: T3
  dominant_category: security_debt
  per_category:
    code_smells: 0.4
    duplication: 0.5
    cyclomatic_complexity: 0.6
    outdated_dependencies: 0.7
    test_coverage_gap: 0.6
    todo_fixme: 0.3
    architectural_violations: 0.0
    security_debt: 1.4   # dominant
    performance_hotspots: 0.2
    documentation_gap: 0.0
  overrides_applied: ["critical_cve_minimum_t3"]
  visualizable_categories: ["code_smells", "duplication", "cyclomatic_complexity", "outdated_dependencies", "test_coverage_gap", "todo_fixme", "security_debt"]
```

## Interpreting Edge Tiers

- **T1 Veil**: do not over-style. Many young codebases land here legitimately. The image is a small, hopeful spirit, not a dramatic one.
- **T5 Calamity**: confirm with the user before publishing. The visual is alarming and may overshoot if executive stakeholders see it without context. Include a short framing note in the report.

## Industry Calibration Anchors (2026-05)

When justifying a tier in a stakeholder report, cite calibrated industry baselines rather than gut feel:

- **CodeScene CodeHealth™**: 1–10 scale where 10 is healthy; SonarQube/CodeScene benchmarking on public maintainability datasets shows CodeHealth is roughly 6× more accurate than SonarQube's Maintainability Rating at matching expert-developer judgment. Research notes a ~60% defect-risk lift when AI generates code into already-unhealthy files. Use as cross-reference when justifying T3+. Source: <https://codescene.com/product/code-health>.
- **SIG Sigrid (ISO 25010 Maintainability)**: TÜViT-certified model, refreshed annually (2024 iteration current); five-star scale where 4★ is industry-average maintainability. Map Sigrid 1–2★ ≈ Hex T4–T5, 3★ ≈ T3, 4★ ≈ T2, 5★ ≈ T1. Source: <https://www.softwareimprovementgroup.com/blog/maintainability-model-2024-update/>.
- **SonarQube 10.x Maintainability Rating**: A = remediation cost ≤ 5% of development cost, B ≤ 10%, C ≤ 20%, D ≤ 50%, E > 50%. Hex tier override does not replace this rating; it is a complementary anthropomorphization layer. Source: <https://docs.sonarsource.com/sonarqube-server/10.8/user-guide/code-metrics/metrics-definition>.
- **McKinsey tech debt baseline**: CIOs estimate tech debt at 20–40% of the value of the technology estate before depreciation; 10–20% of new-product budget is diverted to debt remediation. Use as a business-impact framing for T4–T5 reports. Source: <https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/tech-debt-reclaiming-tech-equity>.
