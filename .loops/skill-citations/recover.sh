#!/usr/bin/env bash
# recover.sh — Reversible recovery for the skill-update loop.
# Use cases:
#   --reset-circuit    : clear circuit-breaker state
#   --rebuild-state    : regenerate state.env from skills-pending.txt
#   --clear-lock       : remove stale .run-loop.lock
#   --rotate-log       : rotate runner.log to runner.log.prev
#   --diagnose         : print health snapshot only (no mutation)
#   --rehash           : recompute state.env.sha256

set -euo pipefail

LOOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_DIR="${LOOP_DIR}/state"
STATE_ENV="${STATE_DIR}/state.env"
STATE_SHA="${STATE_DIR}/state.env.sha256"
PENDING="${STATE_DIR}/skills-pending.txt"
PROCESSED="${STATE_DIR}/skills-processed.txt"
LOCK_FILE="${LOOP_DIR}/.run-loop.lock"
RUNNER_LOG="${LOOP_DIR}/runner.log"
CIRCUIT_FILE="${STATE_DIR}/.circuit-state"

ts()   { date -u +%Y-%m-%dT%H:%M:%SZ; }
info() { printf '[recover %s] %s\n' "$(ts)" "$1" >&2; }

# Portable SHA-256 hash (BSD/GNU compatible)
sha256_hash() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$@"
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$@"
  else
    echo "[ERROR] sha256sum/shasum not found" >&2
    return 1
  fi
}

# Portable file mtime epoch (BSD/GNU compatible)
file_mtime() {
  stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null || echo 0
}

usage() {
  awk '/^# recover\.sh/,/^$/' "$0" | sed 's/^# //'
  exit 64
}

[[ $# -eq 0 ]] && usage

action_reset_circuit() {
  rm -f "${CIRCUIT_FILE}" "${CIRCUIT_FILE}.fails"
  info "circuit breaker reset"
}

action_clear_lock() {
  if [[ -d "${LOCK_FILE}" ]]; then
    local pid; pid="$(cat "${LOCK_FILE}/pid" 2>/dev/null || echo 0)"
    if [[ "${pid}" -gt 0 ]] && kill -0 "${pid}" 2>/dev/null; then
      info "REFUSE: live process holds lock (pid=${pid}); kill it manually first"
      exit 75
    fi
    rm -rf "${LOCK_FILE}"
    info "stale lock cleared (was pid=${pid})"
  else
    info "no lock to clear"
  fi
}

action_rotate_log() {
  if [[ -f "${RUNNER_LOG}" ]]; then
    mv -- "${RUNNER_LOG}" "${RUNNER_LOG}.prev"
    info "rotated runner.log -> runner.log.prev"
  fi
}

action_rebuild_state() {
  [[ ! -f "${PENDING}" ]] && { info "ERROR: ${PENDING} not found; run bootstrap.sh first"; exit 65; }
  local remaining total
  remaining=$(wc -l <"${PENDING}" | tr -d ' ')
  total=$(( remaining + $(wc -l <"${PROCESSED}" 2>/dev/null | tr -d ' ' || echo 0) ))
  cat > "${STATE_ENV}.tmp" <<EOF
NEXT_ITERATION=1
LAST_STATUS=READY
LAST_RUN_AT=
SKILLS_REMAINING=${remaining}
SKILLS_TOTAL=${total}
BATCH_SIZE=5
EOF
  mv -- "${STATE_ENV}.tmp" "${STATE_ENV}"
  sha256_hash "${STATE_ENV}" | awk '{print $1}' > "${STATE_SHA}.tmp"
  mv -- "${STATE_SHA}.tmp" "${STATE_SHA}"
  info "rebuilt state.env (remaining=${remaining}, total=${total})"
}

action_rehash() {
  [[ ! -f "${STATE_ENV}" ]] && { info "ERROR: state.env missing"; exit 65; }
  sha256_hash "${STATE_ENV}" | awk '{print $1}' > "${STATE_SHA}.tmp"
  mv -- "${STATE_SHA}.tmp" "${STATE_SHA}"
  info "rehashed state.env"
}

action_diagnose() {
  printf '\n=== diagnose %s ===\n' "$(ts)"
  printf 'loop_dir   : %s\n' "${LOOP_DIR}"
  printf 'state.env  : %s\n' "$([[ -f "${STATE_ENV}" ]] && echo present || echo MISSING)"
  printf 'pending    : %s\n' "$([[ -f "${PENDING}" ]] && wc -l <"${PENDING}" | tr -d ' ' || echo MISSING)"
  printf 'processed  : %s\n' "$([[ -f "${PROCESSED}" ]] && wc -l <"${PROCESSED}" | tr -d ' ' || echo 0)"
  printf 'lock       : %s\n' "$([[ -d "${LOCK_FILE}" ]] && echo "present (pid=$(cat "${LOCK_FILE}/pid" 2>/dev/null || echo ?))" || echo absent)"
  printf 'circuit    : %s\n' "$([[ -f "${CIRCUIT_FILE}" ]] && cat "${CIRCUIT_FILE}" || echo CLOSED)"
  if [[ -f "${STATE_ENV}" && -f "${STATE_SHA}" ]]; then
    local got want
    got=$(sha256_hash "${STATE_ENV}" | awk '{print $1}')
    want=$(cat "${STATE_SHA}")
    if [[ "${got}" == "${want}" ]]; then
      printf 'state hash : OK\n'
    else
      printf 'state hash : MISMATCH (got=%s expected=%s)\n' "${got:0:12}" "${want:0:12}"
    fi
  fi
  if [[ -f "${RUNNER_LOG}" ]]; then
    printf 'log size   : %s bytes\n' "$(wc -c <"${RUNNER_LOG}" | tr -d ' ')"
  fi
  printf 'disk free  : %s KB\n' "$(df -k "${LOOP_DIR}" | awk 'NR==2 {print $4}')"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --reset-circuit) action_reset_circuit ;;
    --clear-lock)    action_clear_lock ;;
    --rotate-log)    action_rotate_log ;;
    --rebuild-state) action_rebuild_state ;;
    --rehash)        action_rehash ;;
    --diagnose)      action_diagnose ;;
    -h|--help)       usage ;;
    *) info "unknown option: $1"; usage ;;
  esac
  shift
done

info "done"
