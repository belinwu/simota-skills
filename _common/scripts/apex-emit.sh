#!/usr/bin/env bash
# apex-emit: append a structured event to <repo>/.agents/apex/<run-id>/events.jsonl
# Spec: _common/apex-dash/EVENTS.md and INTEGRATION.md
# Usage: apex-emit <kind> [key=value]...
#   examples:
#     apex-emit run_start goal="passkey login" mode=AUTORUN_FULL scope=Standard
#     apex-emit phase_enter phase=P1_Discovery
#     apex-emit agent_start agent=plea phase=P1_Discovery engine=claude_code
#     apex-emit agent_end   agent=plea status=done duration_ms=42000
#     apex-emit risk_gate   verdict=Conditional-Go omen=pass ripple=conditional echo=pass
#
# Contract:
#   - Never disrupts apex (errors are silenced; exit 0 unconditionally)
#   - No-op when APEX_RUN_ID is unset or APEX_DASH_DISABLED=1
#   - Fields ts/seq/run_id/kind always emitted; phase/agent/engine optional;
#     remaining key=value pairs nest under "meta"

{
  set -u

  [ -z "${APEX_RUN_ID:-}" ] && exit 0
  [ "${APEX_DASH_DISABLED:-0}" = "1" ] && exit 0
  [ "$#" -lt 1 ] && exit 0

  KIND="$1"; shift

  REPO_ROOT="${APEX_REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
  DASH_DIR="${APEX_DASH_DIR:-$REPO_ROOT/.agents/apex}"
  RUN_DIR="$DASH_DIR/$APEX_RUN_ID"
  EVENTS="$RUN_DIR/events.jsonl"
  SEQ_FILE="$RUN_DIR/.seq"

  mkdir -p "$RUN_DIR"

  # Atomic seq increment via mkdir lock (portable: macOS / Linux, no flock dep)
  LOCK="$RUN_DIR/.seq.lock"
  i=0
  while ! mkdir "$LOCK" 2>/dev/null; do
    i=$((i + 1))
    [ $i -gt 100 ] && break
    sleep 0.01
  done
  CURRENT=$(cat "$SEQ_FILE" 2>/dev/null || echo 0)
  SEQ=$((CURRENT + 1))
  printf '%s\n' "$SEQ" > "$SEQ_FILE"
  rmdir "$LOCK" 2>/dev/null

  # ISO8601 UTC. Prefer ms precision; fall back to whole seconds.
  TS=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ" 2>/dev/null)
  case "$TS" in
    *3NZ|"") TS=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z") ;;
  esac

  json_str() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\t'/\\t}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/\\r}"
    printf '"%s"' "$s"
  }

  json_value() {
    local v="$1"
    if [[ "$v" =~ ^-?[0-9]+$ ]] || [[ "$v" =~ ^-?[0-9]+\.[0-9]+$ ]]; then
      printf '%s' "$v"
    elif [[ "$v" == "true" || "$v" == "false" ]]; then
      printf '%s' "$v"
    else
      json_str "$v"
    fi
  }

  PHASE=""
  AGENT=""
  ENGINE=""
  META_KV=()

  for kv in "$@"; do
    case "$kv" in
      *=*)
        key="${kv%%=*}"
        val="${kv#*=}"
        case "$key" in
          phase)  PHASE="$val" ;;
          agent)  AGENT="$val" ;;
          engine) ENGINE="$val" ;;
          *)      META_KV+=("$key=$val") ;;
        esac
        ;;
    esac
  done

  J='{"ts":'
  J+="$(json_str "$TS")"
  J+=',"seq":'"$SEQ"
  J+=',"run_id":'"$(json_str "$APEX_RUN_ID")"
  J+=',"kind":'"$(json_str "$KIND")"
  [ -n "$PHASE" ]  && J+=',"phase":'"$(json_str "$PHASE")"
  [ -n "$AGENT" ]  && J+=',"agent":'"$(json_str "$AGENT")"
  [ -n "$ENGINE" ] && J+=',"engine":'"$(json_str "$ENGINE")"

  if [ ${#META_KV[@]} -gt 0 ]; then
    META='"meta":{'
    first=1
    for kv in "${META_KV[@]}"; do
      key="${kv%%=*}"
      val="${kv#*=}"
      if [ $first -eq 1 ]; then
        first=0
      else
        META+=','
      fi
      META+="$(json_str "$key"):$(json_value "$val")"
    done
    META+='}'
    J+=",${META}"
  fi
  J+='}'

  printf '%s\n' "$J" >> "$EVENTS"

  exit 0
} 2>/dev/null

exit 0
