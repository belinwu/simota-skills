# Gemini CLI Review Usage

Operational reference for using Google's Gemini CLI as a review engine. This file is the authoritative "how to run a Gemini-based review" guide. For Codex CLI, see `codex-review-usage.md`. For output interpretation (severity mapping, false-positive filtering), see `codex-integration.md` — those rules apply across engines.

Gemini is one of the three engines in Judge's default tri-engine parallel review (Codex + Gemini + Claude Code subagents, fanned out in a single `Agent` tool message — see `tri-engine-review.md`). This file is consumed by the `review-gemini` subagent during that fan-out. Use it directly as a single-engine review only when: the user explicitly requests a Gemini-only review, two of the three engines are unavailable, cross-verification against an already-run engine is needed, or the repository's GitHub Actions use the `gemini-cli` extension and local parity is desired.

---

## Prerequisites

| Item | Requirement | Notes |
|------|-------------|-------|
| Binary | `gemini` on `$PATH` | `gemini --version` must succeed. The `code-review` extension runs on current `0.38.x` CLI builds; upgrade to the latest release (`npm i -g @google/gemini-cli@latest`) if `gemini extensions install` returns "unknown command" |
| Authentication | Google account login (OAuth browser flow) | Subscription-backed login; **do not** set `GEMINI_API_KEY`, `GOOGLE_API_KEY`, or Vertex env vars for this flow |
| Model | Default (no `-m` / `--model` flag) | Always rely on the CLI default — never override |
| Extension | `code-review` extension installed | `gemini extensions install https://github.com/gemini-cli-extensions/code-review` |
| Working directory | Git repository root | Review commands operate on the current git worktree |
| Approval mode | `--yolo` for headless runs | Required for non-interactive automation; use `--approval-mode plan` for read-only reasoning |

**Never** pass `-m`, `--model`, set `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `GOOGLE_CLOUD_PROJECT`, or `GOOGLE_CLOUD_LOCATION` for this flow. Authentication is managed by the user's Google subscription login.

Verify the extension once:

```bash
gemini extensions list | grep code-review
# If absent:
gemini extensions install https://github.com/gemini-cli-extensions/code-review
```

---

## Command Reference

### Syntax

```
gemini [OPTIONS] [QUERY]
gemini -p "<prompt>" [OPTIONS]
```

Non-interactive review always uses `-p` (prompt) plus `--yolo` and typically `-e code-review`.

### Flag Matrix

| Flag | Purpose | Required for review? |
|------|---------|----------------------|
| `-p, --prompt <STR>` | Headless prompt — runs once and exits | Yes |
| `--yolo` | Auto-approve all tool actions (needed for headless) | Yes for headless |
| `--approval-mode plan` | Read-only mode, no writes | Use for pure analysis |
| `-e, --extensions <LIST>` | Load only the listed extensions | Recommended: `-e code-review` |
| `--include-directories <LIST>` | Extra workspace dirs beyond cwd | When review spans multiple repos |
| `-o, --output-format json` | Structured JSON output | For CI / scripted parsing |
| `-w, --worktree [NAME]` | Run inside a fresh git worktree | For isolated reviews |
| `--policy <PATH>` | Load additional policy files | When repo has review policies |

Omit `-m` / `--model`. Authentication is resolved from the Google login session — do not supply API keys.

### Canonical Commands

```bash
# Headless review of the current branch using the code-review extension
gemini -p "Activate the code review skill and review all code changes on the current branch. Report bugs, security issues, logic errors, and intent misalignment with severity." --yolo -e code-review

# Write the review to a file for downstream processing
gemini -p "Activate the code review skill, review the current branch diff, and write the findings to code-review.md." --yolo -e code-review

# Structured JSON output (for CI pipelines)
gemini -p "Review the current branch diff. Return findings as JSON with fields: severity, file, line, issue, suggested_fix." --yolo -e code-review -o json

# Plan mode (read-only, no writes to disk)
gemini -p "Review the current branch diff and summarize risks; do not modify any files." --approval-mode plan -e code-review
```

---

## Use Case Cookbook

Pick the recipe that matches the user's request. Every recipe uses Google login + default model — only the prompt and flags change. Keep `--yolo` + `-e code-review` unless noted.

### 1. Current-Branch Review (PR-equivalent)

Use when the user says "review this branch", "review my PR with Gemini", or wants an alternative to Codex PR review.

```bash
gemini -p "Activate the code review skill. Review all diffs on the current branch vs its upstream base. Focus on correctness, security, logic errors, and edge cases. Report findings with severity (CRITICAL/HIGH/MEDIUM/LOW/INFO), file:line, evidence, and suggested fix." --yolo -e code-review
```

### 2. Pre-Commit / Uncommitted Changes

Use when the user has uncommitted work and wants a Gemini pre-commit check.

```bash
gemini -p "Activate the code review skill. Review staged, unstaged, and untracked changes in the working tree. Identify bugs, security issues, missing error handling, and logic errors before commit. Severity-rank findings." --yolo -e code-review
```

### 3. Specific Commit Review

Use when the user passes a SHA.

```bash
gemini -p "Activate the code review skill. Review only the changes introduced by commit <SHA>. Report bugs, regressions, and logic errors with severity and line references." --yolo -e code-review
```

Substitute `<SHA>` with the actual commit hash.

### 4. Pull Request Review (GitHub MCP-backed)

Use when the user provides a PR URL and the repo has the GitHub MCP server enabled. The extension exposes `/pr-code-review`.

```bash
# Via env vars
REPOSITORY=owner/repo PULL_REQUEST_NUMBER=1234 \
  gemini -p "/pr-code-review" --yolo -e code-review

# Or inline
gemini -p "/pr-code-review https://github.com/owner/repo/pull/1234" --yolo -e code-review

# With focus areas
REPOSITORY=owner/repo PULL_REQUEST_NUMBER=1234 \
ADDITIONAL_CONTEXT="Focus on authentication and session handling." \
  gemini -p "/pr-code-review" --yolo -e code-review
```

If the GitHub MCP server is not configured, fall back to recipe 1 (current-branch review) after checking out the PR branch locally.

### 5. Security-Focused Review

```bash
gemini -p "Activate the code review skill. Security focus: injection (SQL/NoSQL/command), XSS, SSRF, auth bypass, authorization gaps, hardcoded secrets, unsafe deserialization, missing input validation, insecure crypto, and sensitive data in logs. Severity-rank findings." --yolo -e code-review
```

Route CRITICAL/HIGH findings to Sentinel per SKILL.md collaboration.

### 6. Intent-Alignment Review

```bash
gemini -p "Activate the code review skill. Verify code changes on the current branch match the stated intent. Flag unrelated changes, scope creep, and missing changes implied by the description. Intent: <paste PR title + description here>." --yolo -e code-review
```

### 7. AI-Generated Code Scrutiny

```bash
gemini -p "Activate the code review skill. Elevated scrutiny for AI-generated code. Check (1) logic errors in boundary/edge cases, (2) missing input validation and sanitization, (3) hallucinated imports/APIs/classes — verify every imported symbol exists in the codebase, (4) security shortcuts (hardcoded values, permissive CORS, credential exposure), (5) absent defenses, (6) performance anti-patterns." --yolo -e code-review
```

### 8. Framework-Specific Review

Append framework focus to any recipe. Keep `--yolo -e code-review`.

```bash
# React / Next.js
gemini -p "Activate the code review skill. React/Next.js focus: hook dependency arrays, effect cleanup, server/client boundary ('use client'), data fetching in server components, hydration mismatches, memoization correctness." --yolo -e code-review

# TypeScript
gemini -p "Activate the code review skill. TypeScript focus: unsafe 'as' casts, 'any' escapes, discriminated union exhaustiveness, nullability, generic constraints." --yolo -e code-review

# Go
gemini -p "Activate the code review skill. Go focus: error wrapping, goroutine leaks, channel close semantics, context propagation, race conditions." --yolo -e code-review
```

### 9. Consistency Audit

```bash
gemini -p "Activate the code review skill. Consistency audit across files: error handling patterns, null-safety style, async patterns, naming, imports, error types. Report outliers when a dominant pattern (≥70%) exists." --yolo -e code-review
```

### 10. Test Quality Review

```bash
gemini -p "Activate the code review skill. Test quality focus: isolation, flakiness risk, edge case coverage, mock fidelity, readability. Flag tests that depend on ordering, shared state, time, or network." --yolo -e code-review
```

### 11. Project-Guideline-Gated Review

```bash
# REVIEW.md (Judge convention) piped via stdin
cat REVIEW.md | gemini -p "Activate the code review skill. Apply the guidelines from stdin to the current branch diff." --yolo -e code-review

# AGENTS.md / GEMINI.md (Gemini native) — Gemini auto-discovers GEMINI.md and AGENTS.md in the workspace
gemini -p "Activate the code review skill. Review the current branch diff following project AGENTS.md and GEMINI.md conventions." --yolo -e code-review
```

### 12. Cross-Engine Verification

Use when the user wants dual-engine review (Codex + Gemini) to elevate confidence on findings.

```bash
# Run both sequentially, writing to distinct files for diffing
codex review --base main "Focus on bugs, security, and logic errors." > review-codex.md
gemini -p "Activate the code review skill. Review the current branch diff and write findings to review-gemini.md." --yolo -e code-review
```

Apply the multi-agent verification rules in `codex-integration.md` — findings flagged by both engines elevate to high-priority.

### 13. Structured JSON Output for CI

```bash
gemini -p "Activate the code review skill. Review the current branch diff. Return strict JSON: {\"findings\":[{\"severity\":\"CRITICAL|HIGH|MEDIUM|LOW|INFO\",\"file\":\"...\",\"line\":N,\"issue\":\"...\",\"evidence\":\"...\",\"suggested_fix\":\"...\"}]}" --yolo -e code-review -o json
```

---

## Prompt Structure (Recommended)

Align with the Codex 2026 best practice: structure every non-trivial review prompt with four elements. This applies identically to Gemini.

| Element | Purpose |
|---------|---------|
| **Goal** | What is being reviewed and why |
| **Context** | Relevant files, standards, prior decisions |
| **Constraints** | Architectural patterns, non-negotiables |
| **Done when** | Acceptance criteria for a clean review |

Gemini also auto-discovers `GEMINI.md` and `AGENTS.md` in the workspace — keep repo-wide review norms there rather than repeating them in every prompt.

---

## Interactive Slash Commands

Inside an active `gemini` TUI session (with `code-review` extension loaded), two slash commands are available:

| Command | Scope |
|---------|-------|
| `/code-review` | Review code changes on the current branch |
| `/pr-code-review [url\|env]` | Review a GitHub pull request (requires GitHub MCP server) |

Judge primarily uses the headless `-p` form. Mention slash commands to the user only when they are already inside a `gemini` TUI session.

---

## Decision Flow

```
User request → check environment →
  gemini binary present?                         → (if no) abort, suggest Codex
  code-review extension installed?               → (if no) suggest install command, ask to proceed
  PR URL given + GitHub MCP enabled?             → recipe 4 (/pr-code-review)
  uncommitted changes + pre-commit context?      → recipe 2
  SHA given?                                     → recipe 3
  branch review default?                         → recipe 1
  JSON required by CI?                           → add `-o json`
```

Always pair the prompt with `--yolo -e code-review` for headless runs unless the user explicitly asks for plan mode.

---

## Do / Don't

### Do

- Keep authentication implicit via Google login; never export `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `GOOGLE_CLOUD_PROJECT`, or `GOOGLE_CLOUD_LOCATION` for this flow.
- Omit `-m` / `--model`; always use the default model.
- Pair `-p` with `--yolo` for headless runs; tools require auto-approval in non-interactive mode.
- Scope to the extension with `-e code-review` to prevent unrelated tools from loading.
- Place repo-wide review conventions in `GEMINI.md` or `AGENTS.md` instead of restating them per prompt.
- Use `--output-format json` for CI-consumed output.
- Use `--approval-mode plan` when the user wants analysis-only with zero write risk.

### Don't

- Don't set any provider API key or cloud project env var — subscription login is already active.
- Don't override the model with `-m`, `--model`.
- Don't run headless without `--yolo`; tools will block awaiting approval and the run will hang.
- Don't rely on `/pr-code-review` unless the repo has the GitHub MCP server configured.
- Don't use Gemini when the user explicitly asked for Codex, or vice-versa. Fall back only on explicit unavailability.
- Don't run `gemini` with both `--yolo` and `--approval-mode plan` — they conflict; choose one.

---

## Troubleshooting

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| `command not found: gemini` | CLI not installed or not on `$PATH` | Ask the user to install/fix `$PATH`; fall back to Codex |
| Authentication prompt or failure | Google login session expired | Instruct the user to run `gemini` once interactively to re-login; do not supply API keys |
| Extension missing | `code-review` not installed | Run `gemini extensions install https://github.com/gemini-cli-extensions/code-review` and retry |
| Hang with no output | Missing `--yolo` in headless mode | Re-run with `--yolo`; tool approvals were blocking |
| `/pr-code-review` fails | GitHub MCP server not configured | Fall back to recipe 1 after checking out the PR branch locally |
| Empty or shallow findings | Prompt too vague or no GEMINI.md context | Structure prompt with goal/context/constraints/done-when; add a `GEMINI.md` or `AGENTS.md` if missing |
| JSON output malformed | Prompt did not specify strict schema | Restate the exact JSON schema in the prompt and retry |

---

## Cross-References

- Codex CLI review (default engine): `codex-review-usage.md`.
- Claude Code CLI review (alternative engine, subagent/plan-mode required): `claude-review-usage.md`.
- Output interpretation, severity mapping, override rules, false-positive filtering (engine-agnostic): `codex-integration.md`.
- Framework-specific review prompts: `framework-reviews.md`.
- AI-generated code review depth: `ai-review-patterns.md`.
- PR size cognitive-load thresholds: `review-effectiveness.md`.

### Official Sources (2026)

- Gemini CLI — <https://github.com/google-gemini/gemini-cli>
- Gemini CLI Code-Review Extension — <https://github.com/gemini-cli-extensions/code-review>
- Gemini CLI Codelab (Code Review & Security Analysis) — <https://codelabs.developers.google.com/gemini-cli-code-analysis>
- Gemini CLI — Gemini Code Assist docs — <https://developers.google.com/gemini-code-assist/docs/gemini-cli>
- Gemini CLI Plan Mode — <https://geminicli.com/docs/cli/plan-mode/>
