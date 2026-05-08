#!/usr/bin/env bash
# run-all.sh — Drive the skill-update loop until DONE / BLOCKED / error,
# then run verify.sh.
#
# Usage:
#   bash run-all.sh                     # attended (claude asks for permission)
#   bash run-all.sh --unattended        # opt-in to --dangerously-skip-permissions
#   bash run-all.sh --sleep 5           # change inter-iteration sleep (default 2s)
#   bash run-all.sh --max-iter 50       # safety cap on while-loop iterations
#   bash run-all.sh --skip-verify       # skip verify.sh at the end
#
# Exit codes:
#   0  — DONE + verify passed
#   1  — verify failed
#   2  — run-loop.sh exited non-zero
#   3  — unexpected NEXUS_LOOP_STATUS (e.g. BLOCKED)
#   4  — outer iteration cap reached without DONE
#   64 — bad CLI usage

set -euo pipefail

LOOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${LOOP_DIR}"

# ----- defaults -------------------------------------------------------------
unattended=false
sleep_between=2
outer_max=60          # safety cap; run-loop.sh has its own MAX_ITERATIONS=50
skip_verify=false

# ----- arg parsing ----------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --unattended)  unattended=true ;;
    --sleep)       shift; sleep_between="$1" ;;
    --max-iter)    shift; outer_max="$1" ;;
    --skip-verify) skip_verify=true ;;
    -h|--help)
      sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    *)
      printf 'unknown option: %s\n' "$1" >&2
      exit 64 ;;
  esac
  shift
done

# ----- pretty helpers -------------------------------------------------------
ts()      { date -u +%Y-%m-%dT%H:%M:%SZ; }
section() { printf '\n===== %s =====\n' "$1"; }
note()    { printf '[run-all %s] %s\n' "$(ts)" "$1"; }

# ----- mode banner ----------------------------------------------------------
if "${unattended}"; then
  export CLAUDE_FLAGS="${CLAUDE_FLAGS:-}--print --dangerously-skip-permissions --output-format text"
  # Normalise: if user already exported CLAUDE_FLAGS, prefer theirs.
  if [[ "${CLAUDE_FLAGS}" != *"--dangerously-skip-permissions"* ]]; then
    export CLAUDE_FLAGS="--print --dangerously-skip-permissions --output-format text"
  fi
  note "mode: UNATTENDED (CLAUDE_FLAGS includes --dangerously-skip-permissions)"
else
  note "mode: ATTENDED (claude will prompt for tool permissions on first use)"
  note "  to run unattended: bash run-all.sh --unattended"
fi

# ----- environment summary --------------------------------------------------
remaining_start=$(wc -l <state/skills-pending.txt 2>/dev/null | tr -d ' ' || echo "?")
note "loop_dir : ${LOOP_DIR}"
note "remaining: ${remaining_start} skills"
note "started  : $(ts)"

# ----- main loop ------------------------------------------------------------
iter=0
final_status="UNKNOWN"

while (( iter < outer_max )); do
  iter=$((iter + 1))
  remaining=$(wc -l <state/skills-pending.txt 2>/dev/null | tr -d ' ' || echo "?")
  section "outer-iter ${iter} | remaining=${remaining}"

  # Capture run-loop.sh output without aborting on its non-zero exits.
  set +e
  out=$(bash run-loop.sh)
  rc=$?
  set -e

  printf '%s\n' "${out}"

  if (( rc != 0 )); then
    note "run-loop.sh exited rc=${rc} — see runner.log"
    final_status="ERROR_RC_${rc}"
    exit 2
  fi

  status=$(printf '%s\n' "${out}" | grep '^NEXUS_LOOP_STATUS:' | tail -1 | awk '{print $2}')
  case "${status:-}" in
    CONTINUE)
      sleep "${sleep_between}"
      ;;
    DONE)
      final_status=DONE
      note "all skills processed (${iter} outer iterations)"
      break
      ;;
    READY|BLOCKED|"")
      final_status="${status:-MISSING_FOOTER}"
      note "stopped: status=${final_status}"
      exit 3
      ;;
    *)
      final_status="${status}"
      note "unexpected status: ${status}"
      exit 3
      ;;
  esac
done

if (( iter >= outer_max )) && [[ "${final_status}" != "DONE" ]]; then
  note "outer iteration cap (${outer_max}) reached without DONE"
  exit 4
fi

# ----- verify ---------------------------------------------------------------
if "${skip_verify}"; then
  note "verify skipped (--skip-verify)"
else
  section "verify.sh all"
  if ! bash verify.sh all; then
    note "verify failed"
    exit 1
  fi
fi

note "finished : $(ts)"
note "result   : ${final_status}"
