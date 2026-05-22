# Debt Detection

Per-category detection methods, tools, and thresholds. Run during the `SCAN` phase. Collect findings from at least 3 categories before scoring — single-category scans yield ungrounded characters.

## Output of SCAN

A flat finding list with the following shape:

```yaml
findings:
  - id: F-001
    category: cyclomatic_complexity   # one of the 10 categories below
    magnitude: 0.6                    # 0.0 (clean) → 1.0 (catastrophic)
    evidence:
      - path: src/checkout/process.ts
        line: 142
        excerpt: "function processOrder(...)"
        metric: "cyclomatic=24 (threshold=10)"
    notes: "Long branch chain with nested switch"
```

Every finding must carry at least one `path:line` citation. No citation → finding is rejected by `SCORE`.

## 10 Categories

### 1. Code Smells

- **Detection**: long function (>60 LOC), deep nesting (>4), large file (>400 LOC), large class (>300 LOC), parameter list >5
- **Tooling hints**: `eslint`/`tslint`, `pylint`, `rubocop`, `ktlint`, `golangci-lint`, generic line counters
- **Magnitude scale**: ratio of offending units to total units in the module
- **Maps to**: body distortion (humped back, twisted limbs)

### 2. Duplication

- **Detection**: token-level clone detection
- **Tooling hints**: `jscpd`, `simian`, `pmd-cpd`, `pylint --disable=all --enable=duplicate-code`
- **Magnitude scale**: duplicated-line ratio (duplicated LOC / total LOC); 0.05 = T2 territory, 0.20+ = T4
- **Maps to**: doppelgängers, mirrored limbs, conjoined twins

### 3. Cyclomatic Complexity

- **Detection**: per-function complexity metric
- **Tooling hints**: `radon` (Python), `lizard` (multi-language), `eslint complexity` rule, `gocyclo`
- **Threshold**: `>10` flagged, `>20` severe
- **Magnitude scale**: max(complexity) / 50, capped at 1.0
- **Maps to**: extra arms, branching tendrils, multi-jointed fingers

### 4. Outdated Dependencies

- **Detection**: lockfile age vs current major version, deprecated packages, EOL runtimes
- **Tooling hints**: `npm outdated`, `pip list --outdated`, `bundle outdated`, `cargo outdated`, `renovate` reports
- **Magnitude scale**: weighted by major-version gap and direct vs transitive
- **Maps to**: rusted armor, cracked weapons, moss-covered relics

### 5. Test Coverage Gap

- **Detection**: line/branch coverage vs project target
- **Tooling hints**: `coverage.py`, `nyc/c8`, `jest --coverage`, `simplecov`, `go test -cover`
- **Magnitude scale**: `(target − actual) / target`; 80%-target codebase at 50% coverage = 0.375
- **Maps to**: translucent regions, missing limbs, hollow torso

### 6. TODO / FIXME / HACK Comments

- **Detection**: regex over comment annotations; weight by age (git blame)
- **Tooling hints**: `rg "TODO|FIXME|HACK|XXX"`, `git blame` for age
- **Magnitude scale**: count × age factor (>180 days doubles weight)
- **Maps to**: bandages, chains, gags, locked manacles

### 7. Architectural Violations

- **Detection**: circular dependencies, god class (high fan-in × fan-out), layer violations
- **Tooling hints**: `madge` (JS), `pydeps`, `dependency-cruiser`, `arch-unit`, `Atlas` handoff
- **Magnitude scale**: graph metrics; circular dep count and god-class severity
- **Maps to**: tumors, conjoined growths, twisted spinal columns

### 8. Security Debt

- **Detection**: known CVEs in deps, hardcoded secrets, missing auth/validation patterns
- **Tooling hints**: `npm audit`, `pip-audit`, `bandit`, `semgrep`, `gitleaks`, `Sentinel` handoff
- **Magnitude scale**: weighted by CVSS (critical = 1.0, high = 0.7, medium = 0.4)
- **Maps to**: toxic aura, dripping sigils, glowing wounds

### 9. Performance Hotspots

- **Detection**: profiler hot paths, N+1 query patterns, sync work on UI thread
- **Tooling hints**: profiler exports, `Bolt` handoff, ORM N+1 detectors
- **Magnitude scale**: relative time spent in hottest path
- **Maps to**: burning regions, freezing limbs, smoking joints

### 10. Documentation Gap

- **Detection**: public API surface lacking docstrings/JSDoc; outdated README markers
- **Tooling hints**: `pydocstyle`, `eslint-plugin-jsdoc`, custom AST scanners
- **Magnitude scale**: undocumented public symbols / total public symbols
- **Maps to**: eyeless face, sewn mouth, blank tablets

## Scan Orchestration

If `Atlas`, `Sweep`, `Fossil`, `Sentinel`, or `Trail` have already produced reports for the target repo, prefer their handoff packets over re-running detectors. Hex aggregates; it does not re-litigate.

When running fresh:

1. Pick at most 3 detectors to run inline (small repo) or 5 (large repo).
2. Cap scan time at 90 seconds wall-clock; otherwise emit a `PARTIAL` status and proceed with what was collected.
3. Always run categories 6 (TODO grep) and 5 (coverage) — they are cheap and high-signal.
4. Categories 7, 8 require specialist data — request handoff if not pre-supplied rather than approximate.

## Edge Cases

- **Greenfield repo (<1k LOC)**: most categories will be empty. Default to `T1 Veil` and emit a "young codebase" note rather than fabricating debt.
- **Mono-repo**: scope the scan to one package per invocation. A character per package is preferable to a Frankenstein composite.
- **Generated code directories**: exclude `dist/`, `build/`, `node_modules/`, `vendor/`, `.next/`, similar by default.
- **Lockfiles and snapshots**: never include in line-count or duplication metrics.
- **AI-assisted codebases (2026 context)**: heavy LLM-generated code raises Duplication and TODO categories disproportionately. GitClear's 2025 report on 211M changed lines found copy/pasted lines rose from 8.3% (2021) to 12.3% (2024) and "moved" (refactored) lines fell from 24.1% to 9.5%; treat AI-heavy repos with cloned-block ratios > 0.10 as expected, not anomalous. Source: <https://www.gitclear.com/ai_assistant_code_quality_2025_research>.
- **Outdated dependency baseline**: Sonatype's 2026 State of the Software Supply Chain found ~95% of vulnerable component downloads already had a safer version available, and ~28% of LLM-assisted dependency upgrades across Maven/npm/PyPI/NuGet were hallucinations. When category 4 (Outdated Dependencies) magnitude appears low, double-check transitive lockfile entries before downgrading the score. Source: <https://www.sonatype.com/state-of-the-software-supply-chain/2026/vulnerability-management>.
