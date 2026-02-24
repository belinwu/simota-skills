#!/bin/bash
# skill-improve bootstrap — initialize loop directory and run initial audit
# Based on orbit/references/script-templates.md bootstrap template
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
LOOP_DIR="${SKILLS_DIR}/.nexus-loop/skill-improve"

echo "=== Skill-Improve Bootstrap ==="
echo "Skills dir: ${SKILLS_DIR}"
echo "Loop dir:   ${LOOP_DIR}"

mkdir -p "${LOOP_DIR}"

#--- goal.md (idempotent: skip if exists) ---
if [[ ! -f "${LOOP_DIR}/goal.md" ]]; then
  cat > "${LOOP_DIR}/goal.md" <<'GOAL'
# Goal: Phase 1 — Baseline Quality Lift

## Objective
品質スコア < 6.0 の15スキルに AUTORUN Support / Nexus Hub Mode / Daily Process を追加し、全スキルのスコアを 6.0 以上に引き上げる。

## Why
Nexus AUTORUN実行時の信頼性向上。現状15スキルが品質閾値を下回っており、AUTORUN/NexusHub/DailyProcess が欠損。Phase 1 では最も効果の大きいボトムアップ改善に集中する。

## Scope
Phase 1 のターゲット（スコア昇順）:
1. bard (4.9)
2. muse (5.0)
3. cast (5.3)
4. compass (5.3)
5. refract (5.3)
6. totem (5.3)
7. void (5.3)
8. builder (5.6)
9. magi (5.7)
10. canon (5.8)
11. anvil (5.9)
12. cipher (5.9)
13. researcher (5.9)
14. showcase (5.9)
15. warden (5.9)

## Acceptance Criteria

- AC1: 全スキルの品質スコア >= 6.0 (`verify.sh --all --threshold 6.0`)
- AC2: 上記15スキルに `## AUTORUN Support` が存在
- AC3: 上記15スキルに `## Daily Process` が存在
- AC4: 上記15スキルに `## Nexus Hub Mode` が存在

## Out of Scope (Phase 2 以降)
- Score >= 6.0 のスキルへのセクション追加
- frontmatter description の日本語化 (AC5)
- AUTORUN heading バリアント統一 (AC6)
- スキルのドメイン知識やreferencesの内容改善
- 新規スキルの追加
- _common/, _templates/, _scripts/ の変更

## Verification Command
```
bash _scripts/skill-improve/verify.sh --all --threshold 6.0
```

## Completion Estimate
MAX_ITERATIONS=15, THRESHOLD=6.0
GOAL
  echo "[OK] Created goal.md"
else
  echo "[SKIP] goal.md already exists"
fi

#--- progress.md (idempotent: skip if exists) ---
if [[ ! -f "${LOOP_DIR}/progress.md" ]]; then
  cat > "${LOOP_DIR}/progress.md" <<PROGRESS
# Progress — Phase 1: Baseline Quality Lift

## Iteration 0 — Bootstrap
- Initialized loop directory
- Created goal.md with AC1-AC4 (15 skills target)
- Target: all skills >= 6.0
- Status: READY
- Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
PROGRESS
  echo "[OK] Created progress.md"
else
  echo "[SKIP] progress.md already exists"
fi

#--- state.env (always regenerated) ---
cat > "${LOOP_DIR}/state.env" <<EOF
NEXT_ITERATION=1
LAST_STATUS=READY
LAST_UPDATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ORIGIN_BRANCH=
ITER_BRANCH=
EOF
shasum -a 256 "${LOOP_DIR}/state.env" | awk '{print $1}' > "${LOOP_DIR}/state.env.sha256"
echo "[OK] Created state.env"

#--- Run initial audit ---
echo ""
echo "=== Running Initial Audit ==="
bash "${SCRIPT_DIR}/audit.sh" --output "${LOOP_DIR}/audit-report.md"

echo ""
echo "=== Bootstrap Complete ==="
echo "Loop directory: ${LOOP_DIR}"
echo "Artifacts: goal.md, progress.md, state.env, audit-report.md"
echo ""
echo "Next steps:"
echo "  1. Review: cat ${LOOP_DIR}/audit-report.md"
echo "  2. Run:    bash ${SCRIPT_DIR}/run-loop.sh"
