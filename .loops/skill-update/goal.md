# Goal: Skills Ecosystem Audit and Improvement

## Objective

Continuously audit and propose improvements for the 136 skill agents in `/Users/simota/.claude/skills/`, focusing on freshness, reference integrity, and consistency between `SKILL.md` and `references/`.

## Why

The skills repository has grown to 136 agents + 24 common protocols. Manual auditing is no longer tractable. Reference rot, stale `CAPABILITIES_SUMMARY` blocks, and dead links accumulate silently. This loop runs the Claude Code CLI as an executor to surface and propose fixes in batches.

## Scope

- Target root: `/Users/simota/.claude/skills/`
- Per iteration: 5 skills (alphabetical, resumable from `state/skills-pending.txt`)
- Read-only audit; **no automatic edits**. All changes are recorded as proposals in `reports/improvements.md` for human review.
- Out of scope: `_common/` (audited separately by Hone/Void), `_templates/`, `.agents/`, `.loops/`, `index.html`, hidden files.

## Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| AC1 | All `_common/` references in every SKILL.md point to existing files (zero dead links) | `verify.sh check-common-refs` |
| AC2 | Every Reference Map row in SKILL.md points to an existing `references/*.md` | `verify.sh check-reference-map` |
| AC3 | `CAPABILITIES_SUMMARY` reflects the SKILL body's actual capabilities | sampled human review against `reports/capabilities-drift.md` |
| AC4 | Bidirectional cross-references between SKILL.md and `references/` are consistent | `verify.sh check-bidir-refs` |
| AC5 | `reports/audit.md` covers all 136 skills (one section per skill) | `verify.sh check-audit-coverage` |
| AC6 | `reports/improvements.md` lists prioritized actionable proposals (HIGH / MID / LOW) for every audited skill that has at least one finding | `verify.sh check-improvements` |

## Verification Command

```bash
bash /Users/simota/.claude/skills/.loops/skill-update/verify.sh all
```

Exit 0 = all ACs pass. Non-zero = failure code per AC ID.

## Out of Scope (do NOT modify in this loop)

- `_common/*.md` content (separate concern)
- `_templates/*`
- Any `.agents/` journal files
- `.gitignore` or repo-level config
- Skill renames or directory moves

## DONE Definition

`DONE` is claimed when:
1. `state/skills-pending.txt` is empty (all 136 skills processed),
2. `verify.sh all` returns exit code 0,
3. `reports/audit.md` and `reports/improvements.md` both exist and pass schema validation,
4. The latest iteration's footer reads `NEXUS_LOOP_STATUS: DONE`.

## Rollback

The loop never modifies SKILL.md or references/. Rollback is `rm -rf .loops/skill-update/reports/*` to discard reports and `bootstrap.sh --reset` to restart from scratch.
