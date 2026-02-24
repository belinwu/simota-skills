#!/bin/bash
# skill-improve verify — quality verification gate
# Usage: verify.sh --all | verify.sh --skill <name>
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# shellcheck source=lib/common.sh
source "${SCRIPT_DIR}/lib/common.sh"
# shellcheck source=lib/scoring.sh
source "${SCRIPT_DIR}/lib/scoring.sh"

PASS=0
FAIL=0
TARGET_SKILL=""
VERIFY_ALL=false
THRESHOLD="${THRESHOLD:-6.0}"
SKIP_JP="${SKIP_JP:-false}"

#--- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)
      VERIFY_ALL=true
      shift
      ;;
    --skill|-s)
      TARGET_SKILL="$2"
      shift 2
      ;;
    --threshold|-t)
      THRESHOLD="$2"
      shift 2
      ;;
    --skip-jp)
      SKIP_JP=true
      shift
      ;;
    --help|-h)
      echo "Usage: verify.sh [--all | --skill <name>] [--threshold N] [--skip-jp]"
      echo "  --all             Verify all skills"
      echo "  --skill <name>    Verify a specific skill"
      echo "  --threshold N     Minimum score (default: 6.0)"
      echo "  --skip-jp         Skip Japanese description check (Phase 1)"
      exit 0
      ;;
    *)
      echo "[WARN] Unknown argument: $1"
      shift
      ;;
  esac
done

if [[ "${VERIFY_ALL}" == "false" ]] && [[ -z "${TARGET_SKILL}" ]]; then
  echo "Error: specify --all or --skill <name>"
  exit 1
fi

#--- Check helpers ---
run_check() {
  local name="$1"
  shift
  if "$@" > /dev/null 2>&1; then
    echo "[PASS] ${name}"
    PASS=$((PASS + 1))
  else
    echo "[FAIL] ${name}"
    FAIL=$((FAIL + 1))
  fi
}

check_heading_exists() {
  local file="$1"
  local heading="$2"
  grep -q "^## ${heading}" "$file"
}

check_no_autorun_variants() {
  local file="$1"
  # Should have exactly "## AUTORUN Support", not variants like "## Autorun" or "## AUTORUN Mode"
  local variants
  variants=$(grep -ciE "^## autorun" "$file" 2>/dev/null || echo 0)
  local canonical
  canonical=$(grep -c "^## AUTORUN Support" "$file" 2>/dev/null || echo 0)
  # Pass if no AUTORUN at all (not yet added) or canonical matches total
  [[ "${variants}" -eq "${canonical}" ]]
}

check_japanese_description() {
  local file="$1"
  local desc
  desc=$(sed -n '/^---$/,/^---$/p' "$file" | grep "^description:" | head -1)
  echo "$desc" | LC_ALL=C grep -q '[^[:ascii:]]'
}

check_score_threshold() {
  local file="$1"
  local threshold="$2"
  local result
  result=$(compute_skill_score "$file")
  local total
  IFS='|' read -r total _ <<< "${result}"
  local total_int="${total%.*}"
  local total_frac="${total#*.}"
  local threshold_int="${threshold%.*}"
  local threshold_frac="${threshold#*.}"
  # Compare: total >= threshold
  local total_cmp=$((total_int * 10 + ${total_frac:-0}))
  local threshold_cmp=$((threshold_int * 10 + ${threshold_frac:-0}))
  [[ "${total_cmp}" -ge "${threshold_cmp}" ]]
}

check_frontmatter() {
  local file="$1"
  head -1 "$file" | grep -q "^---$"
}

check_h1_match() {
  local file="$1"
  local skill_name="$2"
  local h1
  h1=$(grep "^# " "$file" | head -1 | sed 's/^# //')
  # H1 should start with the skill name (case-insensitive first char)
  local first_char_h1
  first_char_h1=$(echo "${h1:0:1}" | tr '[:upper:]' '[:lower:]')
  local first_char_skill
  first_char_skill=$(echo "${skill_name:0:1}" | tr '[:upper:]' '[:lower:]')
  [[ "${first_char_h1}" == "${first_char_skill}" ]]
}

#--- Verify a single skill ---
verify_skill() {
  local skill_name="$1"
  local skill_file="${SKILLS_DIR}/${skill_name}/SKILL.md"

  if [[ ! -f "${skill_file}" ]]; then
    echo "[ERROR] ${skill_name}/SKILL.md not found"
    FAIL=$((FAIL + 1))
    return
  fi

  echo "--- ${skill_name} ---"

  run_check "${skill_name}: score >= ${THRESHOLD}" check_score_threshold "${skill_file}" "${THRESHOLD}"
  run_check "${skill_name}: ## AUTORUN Support exists" check_heading_exists "${skill_file}" "AUTORUN Support"
  run_check "${skill_name}: ## Daily Process exists" check_heading_exists "${skill_file}" "Daily Process"
  run_check "${skill_name}: ## Nexus Hub Mode exists" check_heading_exists "${skill_file}" "Nexus Hub Mode"
  if [[ "${SKIP_JP}" != "true" ]]; then
    run_check "${skill_name}: Japanese description" check_japanese_description "${skill_file}"
  else
    echo "[SKIP] ${skill_name}: Japanese description (--skip-jp)"
  fi
  run_check "${skill_name}: No AUTORUN heading variants" check_no_autorun_variants "${skill_file}"
  run_check "${skill_name}: frontmatter present" check_frontmatter "${skill_file}"
}

#--- Main ---
cd "${SKILLS_DIR}"

if [[ "${VERIFY_ALL}" == "true" ]]; then
  echo "=== Skill Quality Verification (all skills) ==="
  echo "Threshold: ${THRESHOLD}"
  echo ""
  for skill_name in $(list_skill_dirs "${SKILLS_DIR}"); do
    verify_skill "${skill_name}"
    echo ""
  done
else
  echo "=== Skill Quality Verification: ${TARGET_SKILL} ==="
  echo "Threshold: ${THRESHOLD}"
  echo ""
  verify_skill "${TARGET_SKILL}"
fi

#--- Summary ---
echo ""
TOTAL=$((PASS + FAIL))
echo "=== Verification: ${PASS}/${TOTAL} passed, ${FAIL} failed ==="

if [[ "${FAIL}" -gt 0 ]]; then
  exit 1
else
  exit 0
fi
