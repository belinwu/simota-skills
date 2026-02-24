#!/bin/bash
# 6-dimension quality scoring for SKILL.md files
# All scoring is deterministic (grep/wc based, no LLM required)
#
# Dimensions & Weights:
#   Structural Completeness  25%  (frontmatter, Boundaries, Collaboration, Operational, References)
#   AUTORUN Readiness        25%  (AUTORUN Support, Nexus Hub Mode, _STEP_COMPLETE)
#   Collaboration Clarity    15%  (Collaboration section, Receives/Sends, partners)
#   Reference Completeness   15%  (References section, table format, file count)
#   Language Consistency     10%  (Japanese description in frontmatter)
#   Process Definition       10%  (Daily Process, structured format)

#--- Individual dimension scorers (return 0-10) ---

# Structural Completeness (25%)
# Checks: frontmatter, H1, Boundaries, Collaboration, Operational, References, closing line
score_structure() {
  local file="$1"
  local score=0
  local content
  content=$(cat "$file")

  # frontmatter (---\nname:...\ndescription:...\n---)
  if echo "$content" | head -5 | grep -q "^---"; then
    score=$((score + 1))
  fi
  if grep -q "^name:" "$file"; then
    score=$((score + 1))
  fi
  if grep -q "^description:" "$file"; then
    score=$((score + 1))
  fi

  # H1 heading
  if grep -q "^# " "$file"; then
    score=$((score + 1))
  fi

  # Key sections
  if grep -q "^## Boundaries" "$file"; then
    score=$((score + 1))
  fi
  if grep -q "^## Collaboration" "$file"; then
    score=$((score + 1))
  fi
  if grep -q "^## Operational" "$file"; then
    score=$((score + 1))
  fi
  if grep -q "^## References" "$file"; then
    score=$((score + 1))
  fi

  # Closing line (> Remember... or > You... or similar blockquote ending)
  if grep -q "^> " "$file"; then
    score=$((score + 1))
  fi

  # Principles or identity statement
  if grep -qE "^## Principles|^\*\*Principles" "$file"; then
    score=$((score + 1))
  fi

  echo "${score}"
}

# AUTORUN Readiness (25%)
# Checks: ## AUTORUN Support, ## Nexus Hub Mode, _STEP_COMPLETE, NEXUS_ROUTING, NEXUS_HANDOFF
score_autorun() {
  local file="$1"
  local score=0

  if grep -q "^## AUTORUN Support" "$file"; then
    score=$((score + 3))
  elif grep -qi "AUTORUN" "$file"; then
    score=$((score + 1))
  fi

  if grep -q "^## Nexus Hub Mode" "$file"; then
    score=$((score + 3))
  elif grep -qi "Nexus Hub" "$file"; then
    score=$((score + 1))
  fi

  if grep -q "_STEP_COMPLETE" "$file"; then
    score=$((score + 2))
  fi

  if grep -q "NEXUS_ROUTING" "$file"; then
    score=$((score + 1))
  fi

  if grep -q "NEXUS_HANDOFF" "$file"; then
    score=$((score + 1))
  fi

  # Cap at 10
  if [[ "${score}" -gt 10 ]]; then
    score=10
  fi
  echo "${score}"
}

# Collaboration Clarity (15%)
# Checks: ## Collaboration, **Receives:**, **Sends:**, partner count
score_collaboration() {
  local file="$1"
  local score=0

  if grep -q "^## Collaboration" "$file"; then
    score=$((score + 3))
  fi

  if grep -q "\*\*Receives:\*\*" "$file"; then
    score=$((score + 2))
  fi

  if grep -q "\*\*Sends:\*\*" "$file"; then
    score=$((score + 2))
  fi

  # Count unique partner references in Collaboration section
  local partners=0
  if grep -q "^## Collaboration" "$file"; then
    partners=$(sed -n '/^## Collaboration/,/^## /p' "$file" | grep -oE '[A-Z][a-z]+' | sort -u | wc -l | tr -d ' ')
  fi
  if [[ "${partners}" -ge 4 ]]; then
    score=$((score + 3))
  elif [[ "${partners}" -ge 2 ]]; then
    score=$((score + 2))
  elif [[ "${partners}" -ge 1 ]]; then
    score=$((score + 1))
  fi

  if [[ "${score}" -gt 10 ]]; then
    score=10
  fi
  echo "${score}"
}

# Reference Completeness (15%)
# Checks: ## References, table format, file count
score_references() {
  local file="$1"
  local score=0

  if grep -q "^## References" "$file"; then
    score=$((score + 2))
  fi

  # Table format (| ... | ... |)
  local ref_section
  ref_section=$(sed -n '/^## References/,/^## /p' "$file" 2>/dev/null)
  if echo "$ref_section" | grep -q "^|"; then
    score=$((score + 2))
  fi

  # Count reference file entries (lines starting with | that contain references/ or a .md link)
  local ref_count=0
  if [[ -n "$ref_section" ]]; then
    ref_count=$(echo "$ref_section" | grep -cE '^\|.*`references/' 2>/dev/null || true)
    ref_count=$(echo "${ref_count}" | tr -d '[:space:]')
    ref_count="${ref_count:-0}"
  fi
  if [[ "${ref_count}" -ge 7 ]]; then
    score=$((score + 6))
  elif [[ "${ref_count}" -ge 5 ]]; then
    score=$((score + 5))
  elif [[ "${ref_count}" -ge 3 ]]; then
    score=$((score + 4))
  elif [[ "${ref_count}" -ge 2 ]]; then
    score=$((score + 3))
  elif [[ "${ref_count}" -ge 1 ]]; then
    score=$((score + 2))
  fi

  if [[ "${score}" -gt 10 ]]; then
    score=10
  fi
  echo "${score}"
}

# Language Consistency (10%)
# Checks: Japanese characters in frontmatter description
score_language() {
  local file="$1"
  local score=0

  # Extract description line from frontmatter
  local desc
  desc=$(sed -n '/^---$/,/^---$/p' "$file" | grep "^description:" | head -1)

  if [[ -z "$desc" ]]; then
    echo "0"
    return
  fi

  # Check for Japanese characters (Hiragana, Katakana, CJK)
  if echo "$desc" | grep -qP '[\x{3040}-\x{309F}\x{30A0}-\x{30FF}\x{4E00}-\x{9FFF}]' 2>/dev/null; then
    score=10
  elif echo "$desc" | grep -q '[ぁ-んァ-ヶ亜-熙]' 2>/dev/null; then
    score=10
  else
    # Fallback: check using LC_ALL for multibyte
    local jp_chars
    jp_chars=$(echo "$desc" | LC_ALL=C grep -c '[^[:ascii:]]' 2>/dev/null || echo 0)
    if [[ "${jp_chars}" -gt 0 ]]; then
      score=10
    else
      score=0
    fi
  fi

  echo "${score}"
}

# Process Definition (10%)
# Checks: ## Daily Process, table format, SURVEY/PLAN/VERIFY/PRESENT phases
score_process() {
  local file="$1"
  local score=0

  if grep -q "^## Daily Process" "$file"; then
    score=$((score + 4))
  fi

  # Table format in Daily Process section
  local proc_section
  proc_section=$(sed -n '/^## Daily Process/,/^## /p' "$file" 2>/dev/null)
  if echo "$proc_section" | grep -q "^|"; then
    score=$((score + 2))
  fi

  # Phase coverage
  local phase_count=0
  for phase in SURVEY PLAN VERIFY PRESENT; do
    if echo "$proc_section" | grep -qi "${phase}"; then
      phase_count=$((phase_count + 1))
    fi
  done
  if [[ "${phase_count}" -ge 4 ]]; then
    score=$((score + 4))
  elif [[ "${phase_count}" -ge 3 ]]; then
    score=$((score + 3))
  elif [[ "${phase_count}" -ge 2 ]]; then
    score=$((score + 2))
  elif [[ "${phase_count}" -ge 1 ]]; then
    score=$((score + 1))
  fi

  if [[ "${score}" -gt 10 ]]; then
    score=10
  fi
  echo "${score}"
}

#--- Weighted composite score (0.0 - 10.0) ---
# Returns: "total|struct|autorun|collab|ref|lang|proc"
compute_skill_score() {
  local file="$1"

  local s_struct s_autorun s_collab s_ref s_lang s_proc
  s_struct=$(score_structure "$file")
  s_autorun=$(score_autorun "$file")
  s_collab=$(score_collaboration "$file")
  s_ref=$(score_references "$file")
  s_lang=$(score_language "$file")
  s_proc=$(score_process "$file")

  # Weighted average: struct*25 + autorun*25 + collab*15 + ref*15 + lang*10 + proc*10
  # Multiply by 10 for integer arithmetic, then divide by 100
  local weighted_sum
  weighted_sum=$(( s_struct * 25 + s_autorun * 25 + s_collab * 15 + s_ref * 15 + s_lang * 10 + s_proc * 10 ))
  # Result in tenths: e.g. 65 = 6.5
  local total_tenths=$((weighted_sum / 10))
  local total_int=$((total_tenths / 10))
  local total_frac=$((total_tenths % 10))

  echo "${total_int}.${total_frac}|${s_struct}|${s_autorun}|${s_collab}|${s_ref}|${s_lang}|${s_proc}"
}

#--- Identify missing sections for improvement prompt ---
identify_gaps() {
  local file="$1"
  local gaps=""

  if ! grep -q "^## AUTORUN Support" "$file"; then
    gaps="${gaps}AUTORUN_SUPPORT,"
  fi
  if ! grep -q "^## Nexus Hub Mode" "$file"; then
    gaps="${gaps}NEXUS_HUB_MODE,"
  fi
  if ! grep -q "^## Daily Process" "$file"; then
    gaps="${gaps}DAILY_PROCESS,"
  fi
  if ! grep -q "_STEP_COMPLETE" "$file"; then
    gaps="${gaps}STEP_COMPLETE_MARKER,"
  fi
  if ! grep -q "NEXUS_ROUTING" "$file"; then
    gaps="${gaps}NEXUS_ROUTING,"
  fi
  if ! grep -q "NEXUS_HANDOFF" "$file"; then
    gaps="${gaps}NEXUS_HANDOFF,"
  fi

  # Check Japanese description
  local desc
  desc=$(sed -n '/^---$/,/^---$/p' "$file" | grep "^description:" | head -1)
  local has_jp=false
  if echo "$desc" | LC_ALL=C grep -q '[^[:ascii:]]' 2>/dev/null; then
    has_jp=true
  fi
  if [[ "${has_jp}" == "false" ]]; then
    gaps="${gaps}JAPANESE_DESCRIPTION,"
  fi

  if ! grep -q "^## Collaboration" "$file"; then
    gaps="${gaps}COLLABORATION_SECTION,"
  fi
  if ! grep -q "^## References" "$file"; then
    gaps="${gaps}REFERENCES_SECTION,"
  fi
  if ! grep -q "^## Boundaries" "$file"; then
    gaps="${gaps}BOUNDARIES_SECTION,"
  fi
  if ! grep -q "^## Operational" "$file"; then
    gaps="${gaps}OPERATIONAL_SECTION,"
  fi

  # Remove trailing comma
  echo "${gaps%,}"
}
