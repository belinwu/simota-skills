# Test Artifact Formats

**Purpose:** Format-specific parser selection and schema notes for ingesting raw test artifacts.
**Read when:** You are at INGEST or PARSE phase and need to choose the right parser or know format-specific quirks.

## Contents
- Format Discovery
- Parser Selection Matrix
- JUnit XML
- Allure Results
- Playwright Report
- Jest / Vitest JSON
- LCOV
- Cobertura XML
- JaCoCo XML
- Python coverage.xml
- CI Run Aggregation
- Parse Error Handling

---

## Format Discovery

Discovery order at INGEST:

1. **User-provided path** — always wins.
2. **Conventional locations**:
   - `coverage/lcov.info` (lcov)
   - `coverage/coverage-final.json` (jest)
   - `coverage/cobertura-coverage.xml` (cobertura)
   - `coverage.xml` (Python `coverage`)
   - `target/site/jacoco/jacoco.xml` (Java)
   - `playwright-report/results.json`, `test-results/results.xml` (Playwright)
   - `allure-results/` (Allure raw)
   - `junit.xml`, `test-results/junit.xml`, `reports/junit/*.xml`
3. **CI fetch** — when only run IDs are given, pull artifacts via `gh run download` (GitHub) or platform API.

If no artifacts are discoverable, **stop and refuse**. Do not synthesize a report.

---

## Parser Selection Matrix

| Source | File / Folder | Parser ID | Notes |
|--------|---------------|-----------|-------|
| JUnit-style runners | `*.xml` with `<testsuites><testsuite>` | `junit-xml-v5` | Treat both Surefire and modern variants |
| Allure | `allure-results/` (json files per test) | `allure-2.x` | Each file is one test case; aggregate |
| Playwright | `playwright-report/results.json` | `playwright-1.49+` | Includes traces, attachments, retries |
| Jest | `coverage/coverage-final.json` | `jest-coverage-1.x` | Per-file path → branch/line/statement |
| Vitest | `--reporter=json` output | `vitest-1.x` | Compatible with jest schema for coverage |
| LCOV | `coverage/lcov.info` | `lcov-1.16` | Plaintext sections per file |
| Cobertura | `cobertura-coverage.xml` | `cobertura-2.x` | Branch coverage included |
| JaCoCo | `jacoco.xml` | `jacoco-0.8.x` | Includes counter types (INSTRUCTION/BRANCH/LINE/METHOD/CLASS) |
| Python coverage | `coverage.xml` | `coverage.py-7.x` | Cobertura-compatible |
| Go test | `go test -json` output | `go-test-json` | Stream of events; reduce to per-test outcome |
| pytest | `--junitxml=...` | `junit-xml-v5` | Use junit parser |
| Cypress | `cypress/results/*.json` (mochawesome) | `mochawesome-7.x` | Convert to junit-equivalent shape |

Always **declare the parser ID and version** in the output Source block. Consumers must be able to reproduce the parse.

---

## JUnit XML

### Schema essentials

```xml
<testsuites name="..." tests="..." failures="..." errors="..." skipped="..." time="...">
  <testsuite name="..." tests="..." failures="..." time="...">
    <testcase classname="..." name="..." time="...">
      <failure message="..." type="...">stack trace</failure>
      <skipped message="..."/>
      <system-out>...</system-out>
    </testcase>
  </testsuite>
</testsuites>
```

### Quirks

- Surefire/Failsafe (Java): single `<testsuite>` root without `<testsuites>` wrapper.
- pytest: `classname` encodes module path (`pkg.module.TestClass`). Split on `.` for hierarchy.
- Some runners emit `<error>` instead of `<failure>` for infrastructure failures — treat both as failed for results, but separate the cluster.
- `time` is float seconds; sum per suite is not always equal to `<testsuite time>` due to setup/teardown.

### What Vista extracts

- Test ID: `classname#name`
- Outcome: pass | fail | error | skipped
- Duration
- Failure message + first 5 lines of stack (after redaction confirmation)
- Suite hierarchy

---

## Allure Results

Each test produces `<uuid>-result.json` plus optional attachments. Aggregate by reading all files in `allure-results/`.

### Key fields

```json
{
  "uuid": "...",
  "fullName": "package.Class.method",
  "labels": [{"name": "feature", "value": "checkout"}, {"name": "epic", "value": "..."}],
  "status": "passed | failed | broken | skipped",
  "statusDetails": {"message": "...", "trace": "..."},
  "start": 1700000000000, "stop": 1700000001234,
  "steps": [...],
  "parameters": [...]
}
```

### Quirks

- `broken` = setup/infrastructure failure; treat distinctly from `failed`.
- `feature` / `story` / `epic` labels are the canonical traceability tags Vista uses for `trace` Recipe.
- History (`history.json`) optional; needed for FLAKE detection.

---

## Playwright Report

`playwright-report/results.json` is the structured summary. The HTML report's `data/test-results.json` is also valid input.

### Key fields

```json
{
  "stats": {"expected": ..., "unexpected": ..., "flaky": ..., "skipped": ..., "duration": ...},
  "suites": [
    {
      "title": "...", "file": "...",
      "specs": [
        {
          "title": "...",
          "tests": [
            {
              "expectedStatus": "passed",
              "results": [
                {"status": "passed | failed | timedOut", "duration": ..., "retry": 0, "attachments": [...]}
              ]
            }
          ]
        }
      ],
      "suites": [...recursive...]
    }
  ]
}
```

### Quirks

- A single test can have multiple `results` entries when `retries > 0`. Vista uses retry count to compute flake signal.
- `flaky` stat = passed after retry. Use this to seed FLAKE-CLUSTER detection.
- Trace files (`trace.zip`) are large; reference path, do not embed.

---

## Jest / Vitest JSON

`coverage/coverage-final.json` is keyed by absolute file path:

```json
{
  "/abs/path/file.ts": {
    "path": "...",
    "statementMap": {...}, "s": {"0": 5, "1": 0, ...},
    "fnMap": {...}, "f": {...},
    "branchMap": {...}, "b": {...}
  }
}
```

### Vista derivation

- Statement coverage: `hit_count(s) / total(s)`
- Branch coverage: per `branchMap` entry, count covered sides; aggregate over file
- Line coverage: derive from `statementMap` line ranges
- Always render branch and statement separately. Do not collapse.

---

## LCOV

Plaintext, sections terminated by `end_of_record`:

```
TN:
SF:/abs/path/file.ts
FN:1,functionName
FNDA:5,functionName
DA:1,5
DA:2,0
BRDA:5,0,0,2
LF:50
LH:30
BRF:10
BRH:6
end_of_record
```

### Field meanings

| Tag | Meaning |
|-----|---------|
| `SF:` | Source file path |
| `DA:line,hits` | Line execution count |
| `BRDA:line,blockId,branchId,taken` | Branch taken count (`-` if not taken) |
| `LF:` / `LH:` | Lines found / hit (line coverage) |
| `BRF:` / `BRH:` | Branches found / hit (branch coverage) |
| `FNF:` / `FNH:` | Functions found / hit |

### Quirks

- Paths may be relative to the lcov generation directory; normalize against `cwd`.
- Some toolchains emit `BRDA:line,0,0,-` meaning branch not exercised — count as 0/1.

---

## Cobertura XML

```xml
<coverage line-rate="0.85" branch-rate="0.70" lines-covered="..." lines-valid="..." ...>
  <packages>
    <package name="..." line-rate="..." branch-rate="...">
      <classes>
        <class name="..." filename="..." line-rate="..." branch-rate="...">
          <methods>...</methods>
          <lines>
            <line number="1" hits="5" branch="false"/>
            <line number="5" hits="2" branch="true" condition-coverage="50% (1/2)"/>
          </lines>
        </class>
      </classes>
    </package>
  </packages>
</coverage>
```

### Quirks

- `line-rate` and `branch-rate` are floats (0..1), not percentages.
- `condition-coverage` is a string; parse with regex `(\d+)% \((\d+)/(\d+)\)`.

---

## JaCoCo XML

```xml
<report name="...">
  <package name="...">
    <class name="..." sourcefilename="...">
      <method name="..." desc="...">
        <counter type="INSTRUCTION" missed="..." covered="..."/>
        <counter type="BRANCH" missed="..." covered="..."/>
        <counter type="LINE" missed="..." covered="..."/>
      </method>
      <counter type="INSTRUCTION" missed="..." covered="..."/>
      ...
    </class>
    <sourcefile name="...">
      <line nr="..." mi="..." ci="..." mb="..." cb="..."/>
    </sourcefile>
  </package>
</report>
```

### Quirks

- Five counter types: INSTRUCTION, BRANCH, LINE, METHOD, CLASS. Vista visualizes BRANCH and LINE; keep INSTRUCTION as a tooltip detail.
- `mi`/`ci` = missed/covered instructions per line; `mb`/`cb` = same for branches.

---

## Python coverage.xml

Cobertura-compatible. Use the same parser as Cobertura with these notes:
- `filename` is module path with `.` separator; convert to filesystem path for treemap.
- Branch coverage requires `coverage run --branch`; without it, `branch-rate=0` is meaningless. Detect and warn.

---

## CI Run Aggregation

For `flake`, `timeline`, and `diff` Recipes, Vista pulls multiple runs.

### GitHub Actions

```bash
gh run list --workflow=<name> --limit 50 --json databaseId,headSha,conclusion,createdAt,updatedAt
gh run download <run-id> --name <artifact-name>
```

### GitLab CI

```bash
glab ci list --status all --paginate
glab ci artifacts <pipeline-id> <job-name>
```

### Aggregation rules

- Window: default 30 days, configurable; minimum 30 runs for `flake`.
- Correlate by commit SHA (`headSha` in GitHub, `sha` in GitLab) for `timeline`.
- Cache parsed artifacts under `.cache/vista/<sha>.json` to avoid re-parsing across Recipes.

---

## Parse Error Handling

When parsing fails:

1. **Quote the parser error verbatim** in the output's `Limitations` block.
2. **Continue partial parse** when individual files fail but others succeed; mark the partial scope explicitly.
3. **Refuse to render** if >20% of files failed to parse — the visualization would mislead.
4. **Never substitute zeros** for missing data. Show "N/A" or omit the file.

### Example failure output

```yaml
Limitations:
  - parser: lcov-1.16
    file: coverage/lcov.info
    line: 4523
    error: "Unexpected token: BRDA:5,0,0," (truncated branch entry)
    impact: "1 of 312 files skipped; coverage map shows 311 files"
```
