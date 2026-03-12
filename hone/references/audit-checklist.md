# Audit Checklist

**Purpose:** Category-based audit checklist with PASS/WARN/FAIL criteria for Codex CLI and Gemini CLI configuration.
**Read when:** Running the AUDIT phase on `~/.codex/` or `~/.gemini/` configuration files.

---

## Checklist Overview

| ID | Category | Check | Priority |
|----|----------|-------|----------|
| M1 | Model | Model identifier is current and available | P0 |
| M2 | Model | `reasoning_effort` matches typical use pattern | P2 |
| M3 | Model | `verbose` is not permanently enabled | P3 |
| T1 | Trust | No stale paths (non-existent directories) | P1 |
| T2 | Trust | No over-trusted sensitive projects | P0 |
| T3 | Trust | No unnecessary untrust on personal projects | P2 |
| T4 | Trust | No overly broad wildcard patterns | P1 |
| T5 | Trust | Total trust count is manageable (< 100) | P3 |
| F1 | Features | All available flags are reviewed | P1 |
| F2 | Features | No deprecated flags present | P0 |
| F3 | Features | New stable features are enabled | P2 |
| C1 | MCP | Server binaries exist and are executable | P0 |
| C2 | MCP | No unused/orphaned server configs | P1 |
| C3 | MCP | No plaintext secrets in server config | P0 |
| C4 | MCP | Server versions are current | P2 |
| R1 | Rules | No duplicate rules across files | P1 |
| R2 | Rules | Glob patterns are valid and specific | P2 |
| R3 | Rules | No stale rules referencing removed tools/patterns | P1 |
| A1 | AGENTS.md | Instructions are clear and non-contradictory | P1 |
| A2 | AGENTS.md | Priority hierarchy is defined | P2 |
| A3 | AGENTS.md | No redundant/overlapping directives | P2 |
| I1 | Instructions | `instructions.md` exists and is non-empty | P1 |
| I2 | Instructions | Content is current and actionable | P2 |
| N1 | Notice | Migration/deprecation prompts are addressed | P1 |

---

## Judgment Criteria

### PASS
- Configuration meets the check requirement completely.
- No action needed.

### WARN
- Configuration partially meets the requirement or has minor issues.
- Improvement suggested but not urgent.
- Applies to: P2-P3 items with minor deviations.

### FAIL
- Configuration does not meet the requirement.
- Action recommended (P0-P1) or improvement needed (P2-P3).
- Applies to: Missing items, security issues, broken paths.

---

## Priority Definitions

| Priority | Label | Meaning | Action |
|----------|-------|---------|--------|
| P0 | Critical | Security risk or broken configuration | Fix immediately |
| P1 | Recommended | Functional improvement, hygiene | Fix in current session |
| P2 | Improvement | Optimization, best practice alignment | Fix when convenient |
| P3 | Informational | Minor suggestion, cosmetic | Note for future |

---

## Safety Classification

| Label | Meaning | Application |
|-------|---------|-------------|
| `safe` | Can apply without risk | Removing stale paths, adding comments |
| `ask-first` | Needs user confirmation | Changing trust levels, model, features |
| `risky` | May break workflow | Removing MCP servers, changing approval_mode |

---

## Category-Specific Audit Procedures

### Model Audit (M1-M3)

1. Read `model` value from config.toml
2. WebSearch for latest Codex CLI supported models
3. Compare and classify (PASS if current, WARN if one version behind, FAIL if deprecated)
4. Check `reasoning_effort` against user's typical task complexity
5. Verify `verbose` is not permanently enabled

### Trust Audit (T1-T5)

1. Extract all paths from `[project_trust]`
2. Check each path exists on disk (T1)
3. Flag sensitive-looking paths (auth, finance, secrets) that are trusted (T2)
4. Count total entries and flag if excessive (T5)
5. Check for wildcard patterns and assess specificity (T4)

### Feature Audit (F1-F3)

1. Extract all feature flags from config
2. WebSearch for current available flags in latest version
3. Identify missing new flags (F1), deprecated flags (F2), stable but disabled flags (F3)

### MCP Audit (C1-C4)

1. Extract MCP server configs
2. Check each binary path exists and is executable (C1)
3. Check for unused servers (C2)
4. Scan for plaintext secrets in args/env (C3)
5. Check server versions against latest (C4)

### Rules Audit (R1-R3)

1. Read all files in `~/.codex/rules/`
2. Compare rules for duplicates across files (R1)
3. Validate glob patterns (R2)
4. Check for references to removed or changed tools (R3)

### AGENTS.md Audit (A1-A3)

1. Read `~/.codex/AGENTS.md`
2. Check for clarity and contradiction (A1)
3. Verify priority hierarchy exists (A2)
4. Check for redundant directives (A3)

### Instructions Audit (I1-I2)

1. Check `~/.codex/instructions.md` exists and is non-empty (I1)
2. Review content for relevance and actionability (I2)

---

## Gemini CLI Checklist

| ID | Category | Check | Priority |
|----|----------|-------|----------|
| GM1 | Gemini Model | `selectedModel` is current and available | P0 |
| GM2 | Gemini Model | Model is compatible with API tier | P1 |
| GM3 | Gemini Model | Model supports required capabilities (code, multimodal) | P2 |
| GS1 | Gemini Safety | Safety settings are not overly permissive | P0 |
| GS2 | Gemini Safety | Safety settings are not overly restrictive for dev use | P2 |
| GE1 | Gemini Extensions | Extension paths/binaries are valid | P0 |
| GE2 | Gemini Extensions | No unused extensions detected | P1 |
| GE3 | Gemini Extensions | No plaintext secrets in extension config | P0 |
| GE4 | Gemini Extensions | Extension versions are current | P2 |
| GI1 | Gemini Instructions | `GEMINI.md` exists and is non-empty | P1 |
| GI2 | Gemini Instructions | Content is current and actionable | P2 |
| GA1 | Gemini Auth | Authentication method is configured | P0 |
| GA2 | Gemini Auth | `GEMINI_API_KEY` is not hardcoded in files | P0 |

---

## Gemini Category-Specific Audit Procedures

### Gemini Model Audit (GM1-GM3)

1. Read `selectedModel` value from settings.json
2. WebSearch for latest Gemini CLI supported models
3. Compare and classify (PASS if current, WARN if one version behind, FAIL if deprecated)
4. Check model compatibility with the user's API tier (free vs paid)
5. Verify model supports required capabilities (code generation, multimodal input)

### Gemini Safety Audit (GS1-GS2)

1. Read `safetySettings` array from settings.json
2. Check for `BLOCK_NONE` on all categories without justification (GS1: FAIL)
3. Check for `BLOCK_HIGH_AND_ABOVE` on all categories blocking legitimate dev use (GS2: WARN)
4. Verify all harm categories are configured (missing categories inherit defaults)
5. Assess consistency of threshold levels across categories

### Gemini Extensions Audit (GE1-GE4)

1. Extract extension configs from settings.json
2. Check each binary path exists and is executable (GE1)
3. Check for unused extensions (GE2)
4. Scan for plaintext secrets in args/env (GE3)
5. Check extension versions against latest (GE4)

### Gemini Instructions Audit (GI1-GI2)

1. Check `~/.gemini/GEMINI.md` exists and is non-empty (GI1)
2. Check project-level `GEMINI.md` if applicable
3. Review content for relevance and actionability (GI2)
4. Check for contradictions between global and project-level instructions

### Gemini Auth Audit (GA1-GA2)

1. Check that `selectedAuthType` is configured or `GEMINI_API_KEY` env var is set (GA1)
2. Scan project files and shell configs for hardcoded `GEMINI_API_KEY` values (GA2)
3. Never read actual auth tokens or OAuth session files
