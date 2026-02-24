#!/bin/bash
# skill-improve audit — deterministic quality scoring for all SKILL.md files
# Outputs Markdown table report with scores and improvement candidates
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
OUTPUT_FILE=""

# shellcheck source=lib/common.sh
source "${SCRIPT_DIR}/lib/common.sh"
# shellcheck source=lib/scoring.sh
source "${SCRIPT_DIR}/lib/scoring.sh"

#--- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --output|-o)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    --help|-h)
      echo "Usage: audit.sh [--output FILE]"
      echo "  --output FILE  Write report to FILE (default: stdout)"
      exit 0
      ;;
    *)
      echo "[WARN] Unknown argument: $1"
      shift
      ;;
  esac
done

#--- Collect scores ---
declare -a SKILL_NAMES=()
declare -a SKILL_SCORES=()
declare -a SKILL_DETAILS=()

cd "${SKILLS_DIR}"

for skill_name in $(list_skill_dirs "${SKILLS_DIR}"); do
  skill_file="${SKILLS_DIR}/${skill_name}/SKILL.md"
  if [[ ! -f "${skill_file}" ]]; then
    continue
  fi

  result=$(compute_skill_score "${skill_file}")
  SKILL_NAMES+=("${skill_name}")
  SKILL_SCORES+=("${result}")

  gaps=$(identify_gaps "${skill_file}")
  SKILL_DETAILS+=("${gaps}")
done

#--- Generate report ---
generate_report() {
  local total_skills=${#SKILL_NAMES[@]}
  local above_threshold=0
  local below_threshold=0

  echo "# Skill Quality Audit Report"
  echo ""
  echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "Skills scanned: ${total_skills}"
  echo ""
  echo "## Scoring Dimensions"
  echo ""
  echo "| Dimension | Weight | Description |"
  echo "|-----------|--------|-------------|"
  echo "| Structural Completeness | 25% | frontmatter, Boundaries, Collaboration, Operational, References |"
  echo "| AUTORUN Readiness | 25% | AUTORUN Support, Nexus Hub Mode, _STEP_COMPLETE |"
  echo "| Collaboration Clarity | 15% | Receives/Sends, partner count |"
  echo "| Reference Completeness | 15% | Table format, file count |"
  echo "| Language Consistency | 10% | Japanese description in frontmatter |"
  echo "| Process Definition | 10% | Daily Process, phase coverage |"
  echo ""
  echo "## All Skills"
  echo ""
  echo "| Skill | Total | Struct | AUTORUN | Collab | Refs | Lang | Process | Gaps |"
  echo "|-------|-------|--------|---------|--------|------|------|---------|------|"

  for i in "${!SKILL_NAMES[@]}"; do
    local name="${SKILL_NAMES[$i]}"
    local scores="${SKILL_SCORES[$i]}"
    local gaps="${SKILL_DETAILS[$i]}"

    IFS='|' read -r total s_struct s_autorun s_collab s_ref s_lang s_proc <<< "${scores}"

    # Count threshold
    local total_num
    total_num=$(echo "${total}" | sed 's/\.//')
    if [[ "${total_num}" -ge 60 ]]; then
      above_threshold=$((above_threshold + 1))
    else
      below_threshold=$((below_threshold + 1))
    fi

    # Truncate gaps for table display
    local gaps_short="${gaps}"
    if [[ ${#gaps_short} -gt 40 ]]; then
      gaps_short="${gaps_short:0:37}..."
    fi

    echo "| ${name} | **${total}** | ${s_struct} | ${s_autorun} | ${s_collab} | ${s_ref} | ${s_lang} | ${s_proc} | ${gaps_short} |"
  done

  echo ""
  echo "## Summary"
  echo ""
  echo "- Total skills: ${total_skills}"
  echo "- Score >= 6.0: ${above_threshold} ($(( above_threshold * 100 / total_skills ))%)"
  echo "- Score < 6.0: ${below_threshold} ($(( below_threshold * 100 / total_skills ))%)"
  echo ""

  # Improvement candidates (sorted by score ascending)
  echo "## Improvement Candidates (score < 6.0)"
  echo ""
  echo "| Priority | Skill | Score | Top Issues |"
  echo "|----------|-------|-------|------------|"

  local priority=1
  # Sort by score ascending - collect name:score pairs, sort, output
  local sorted_candidates=()
  for i in "${!SKILL_NAMES[@]}"; do
    local scores="${SKILL_SCORES[$i]}"
    local total
    IFS='|' read -r total _ <<< "${scores}"
    local total_num
    total_num=$(echo "${total}" | sed 's/\.//')
    if [[ "${total_num}" -lt 60 ]]; then
      sorted_candidates+=("${total_num}|${i}")
    fi
  done

  # Sort numerically by score
  IFS=$'\n' sorted_candidates=($(printf '%s\n' "${sorted_candidates[@]}" | sort -t'|' -k1 -n))
  unset IFS

  for entry in "${sorted_candidates[@]}"; do
    local idx
    IFS='|' read -r _ idx <<< "${entry}"
    local name="${SKILL_NAMES[$idx]}"
    local scores="${SKILL_SCORES[$idx]}"
    local gaps="${SKILL_DETAILS[$idx]}"

    local total
    IFS='|' read -r total _ <<< "${scores}"

    echo "| ${priority} | ${name} | ${total} | ${gaps} |"
    priority=$((priority + 1))
  done

  echo ""
  echo "---"
  echo "End of audit report."
}

#--- Output ---
if [[ -n "${OUTPUT_FILE}" ]]; then
  generate_report > "${OUTPUT_FILE}"
  echo "[OK] Audit report written to ${OUTPUT_FILE}"
  echo "     Skills scanned: ${#SKILL_NAMES[@]}"

  # Quick summary to stdout
  above=0
  below=0
  for i in "${!SKILL_NAMES[@]}"; do
    IFS='|' read -r total _ <<< "${SKILL_SCORES[$i]}"
    total_num=$(echo "${total}" | sed 's/\.//')
    if [[ "${total_num}" -ge 60 ]]; then
      above=$((above + 1))
    else
      below=$((below + 1))
    fi
  done
  echo "     Score >= 6.0: ${above}"
  echo "     Score < 6.0:  ${below} (improvement candidates)"
else
  generate_report
fi
