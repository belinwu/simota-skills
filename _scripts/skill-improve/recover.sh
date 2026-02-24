#!/bin/bash
# skill-improve recovery — rebuild state.env from progress.md evidence
# Based on orbit/references/script-templates.md recovery template
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
LOOP_DIR="${SKILLS_DIR}/.nexus-loop/skill-improve"

echo "=== Skill-Improve Recovery ==="

if [[ ! -d "${LOOP_DIR}" ]]; then
  echo "[ERROR] Loop directory not found: ${LOOP_DIR}"
  echo "[HINT] Run bootstrap.sh first"
  exit 1
fi

if [[ ! -f "${LOOP_DIR}/progress.md" ]]; then
  echo "[ERROR] progress.md not found — cannot recover"
  exit 1
fi

#--- Parse latest iteration from progress.md ---
LATEST_ITER=$(grep -oE 'Iteration [0-9]+' "${LOOP_DIR}/progress.md" | grep -oE '[0-9]+' | tail -1)
if [[ -z "${LATEST_ITER}" ]]; then
  echo "[WARN] No iteration found in progress.md — resetting to 1"
  LATEST_ITER=0
fi

#--- Determine STATUS from last 20 lines ---
TAIL_CONTENT=$(tail -20 "${LOOP_DIR}/progress.md")
if echo "${TAIL_CONTENT}" | grep -qiE '(DONE|completed|finished)'; then
  RECOVERED_STATUS="DONE"
elif echo "${TAIL_CONTENT}" | grep -qiE '(BLOCKED|FAIL|TOOL_FAILURE)'; then
  RECOVERED_STATUS="BLOCKED"
else
  RECOVERED_STATUS="CONTINUE"
fi

NEXT_ITER=$((LATEST_ITER + 1))
echo "[INFO] Latest iteration: ${LATEST_ITER}"
echo "[INFO] Recovered status: ${RECOVERED_STATUS}"
echo "[INFO] Next iteration will be: ${NEXT_ITER}"

#--- Detect branch info ---
ORIGIN_BRANCH=""
ITER_BRANCH=""
if [[ -f "${LOOP_DIR}/state.env" ]]; then
  ORIGIN_BRANCH=$(grep "^ORIGIN_BRANCH=" "${LOOP_DIR}/state.env" | cut -d= -f2 || true)
  ITER_BRANCH=$(grep "^ITER_BRANCH=" "${LOOP_DIR}/state.env" | cut -d= -f2 || true)
fi

#--- Rebuild state.env (atomic write) ---
state_tmp=$(mktemp "${LOOP_DIR}/state.env.XXXXXX")
cat > "${state_tmp}" <<EOF
NEXT_ITERATION=${NEXT_ITER}
LAST_STATUS=${RECOVERED_STATUS}
LAST_UPDATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
RECOVERED_FROM=progress_evidence
ORIGIN_BRANCH=${ORIGIN_BRANCH}
ITER_BRANCH=${ITER_BRANCH}
EOF
mv "${state_tmp}" "${LOOP_DIR}/state.env"
shasum -a 256 "${LOOP_DIR}/state.env" | awk '{print $1}' > "${LOOP_DIR}/state.env.sha256"
echo "[OK] Rebuilt state.env"

#--- Append recovery note to progress.md ---
{
  echo ""
  echo "## Recovery — $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "- Recovered from progress.md evidence"
  echo "- Latest iteration found: ${LATEST_ITER}"
  echo "- Recovered status: ${RECOVERED_STATUS}"
  echo "- state.env rebuilt with NEXT_ITERATION=${NEXT_ITER}"
} >> "${LOOP_DIR}/progress.md"
echo "[OK] Appended recovery note to progress.md"

echo ""
echo "=== Recovery Complete ==="
echo "Next: run 'bash _scripts/skill-improve/run-loop.sh' to resume"
