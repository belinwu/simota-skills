#!/usr/bin/env bash
# bootstrap.sh — Initialize the skill-citations loop from citations-todo.md.
# Idempotent. Use --reset to wipe state.

set -euo pipefail

LOOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_DIR="${LOOP_DIR}/state"
REPORTS_DIR="${LOOP_DIR}/reports"
BATCHES_DIR="${LOOP_DIR}/batches"
TODO_FILE="${LOOP_DIR}/citations-todo.md"

mkdir -p "${STATE_DIR}" "${REPORTS_DIR}" "${BATCHES_DIR}"

reset_mode=false
for arg in "$@"; do
  case "${arg}" in
    --reset) reset_mode=true ;;
    *) echo "[bootstrap] unknown arg: ${arg}" >&2; exit 64 ;;
  esac
done

if "${reset_mode}"; then
  echo "[bootstrap] --reset: clearing state, reports, batches"
  rm -f "${STATE_DIR}"/* "${REPORTS_DIR}"/* "${BATCHES_DIR}"/*
fi

[[ -f "${TODO_FILE}" ]] || { echo "[bootstrap] FATAL: ${TODO_FILE} missing"; exit 65; }

# --- 1. Generate skills-pending.txt from citations-todo.md ------------------
PENDING="${STATE_DIR}/skills-pending.txt"
if [[ ! -s "${PENDING}" ]]; then
  grep -E '^## ' "${TODO_FILE}" | sed -E 's/^## //' | sort -u > "${PENDING}"
  count=$(wc -l <"${PENDING}" | tr -d ' ')
  echo "[bootstrap] ${count} skills enqueued from citations-todo.md"
fi

# --- 2. Initialize state.env ------------------------------------------------
STATE_ENV="${STATE_DIR}/state.env"
if [[ ! -f "${STATE_ENV}" ]]; then
  cat > "${STATE_ENV}.tmp" <<EOF
# Auto-generated — do not hand-edit while loop is running.
NEXT_ITERATION=1
LAST_STATUS=READY
LAST_RUN_AT=
SKILLS_REMAINING=$(wc -l <"${PENDING}" | tr -d ' ')
SKILLS_TOTAL=$(wc -l <"${PENDING}" | tr -d ' ')
BATCH_SIZE=4
EOF
  mv -- "${STATE_ENV}.tmp" "${STATE_ENV}"
fi

shasum -a 256 "${STATE_ENV}" | awk '{print $1}' > "${STATE_DIR}/state.env.sha256.tmp"
mv -- "${STATE_DIR}/state.env.sha256.tmp" "${STATE_DIR}/state.env.sha256"

# --- 3. Initialize progress.md and reports ----------------------------------
PROGRESS="${LOOP_DIR}/progress.md"
[[ -f "${PROGRESS}" ]] || cat > "${PROGRESS}" <<'EOF'
# Citation Loop Progress

| Iter | Started | Finished | Batch | Skills | Status | Notes |
|------|---------|----------|-------|--------|--------|-------|
EOF

[[ -f "${REPORTS_DIR}/citations-applied.md" ]] || \
  printf '# Citations Applied\n\n' > "${REPORTS_DIR}/citations-applied.md"

echo "[bootstrap] ready"
echo "  loop_dir : ${LOOP_DIR}"
echo "  todo     : ${TODO_FILE}"
echo "  pending  : $(wc -l <"${PENDING}" | tr -d ' ')"
echo "  next     : run-loop.sh"
