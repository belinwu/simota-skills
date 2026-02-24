#!/bin/bash
# skill-improve loop runner — drives autonomous skill improvement via claude CLI
# Based on orbit/references/script-templates.md runner template
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# shellcheck source=lib/common.sh
source "${SCRIPT_DIR}/lib/common.sh"
# shellcheck source=lib/scoring.sh
source "${SCRIPT_DIR}/lib/scoring.sh"

#--- Configuration ---
LOOP_DIR="${SKILLS_DIR}/.nexus-loop/skill-improve"
MAX_ITERATIONS="${MAX_ITERATIONS:-15}"
RETRY_LIMIT="${RETRY_LIMIT:-2}"
RETRY_BACKOFF_BASE="${RETRY_BACKOFF_BASE:-3}"
EXEC_CMD="${EXEC_CMD:-claude}"
EXEC_TIMEOUT="${EXEC_TIMEOUT:-300}"
AUTOCOMMIT="${AUTOCOMMIT:-true}"
COMMIT_MSG_PREFIX="${COMMIT_MSG_PREFIX:-feat(skill)}"
MAX_LOG_SIZE="${MAX_LOG_SIZE:-5242880}"
BRANCH_ISOLATION="${BRANCH_ISOLATION:-true}"
THRESHOLD="${THRESHOLD:-6.0}"

#--- Pre-flight ---
if ! preflight_check "${LOOP_DIR}"; then
  echo "[ABORT] Pre-flight check failed"
  exit 1
fi

# Acquire lock
echo $$ > "${LOOP_DIR}/.run-loop.lock"

#--- Graceful shutdown ---
SHUTDOWN=0
cleanup() {
  echo "[SIGNAL] Caught signal — writing state and exiting"
  SHUTDOWN=1
  atomic_state_write "${LOOP_DIR}" "${ITER}" "CONTINUE" "${ORIGIN_BRANCH:-}" "${ITER_BRANCH:-}"
  rm -f "${LOOP_DIR}/.run-loop.lock"
  exit 130
}
trap cleanup SIGINT SIGTERM

#--- Load state.env ---
ITER=1
STATUS="READY"
ORIGIN_BRANCH=""
ITER_BRANCH=""
if [[ -f "${LOOP_DIR}/state.env" ]]; then
  if ! validate_state_checksum "${LOOP_DIR}"; then
    echo "[RECOVERY] Checksum mismatch — running recover.sh"
    if [[ -f "${SCRIPT_DIR}/recover.sh" ]]; then
      bash "${SCRIPT_DIR}/recover.sh"
    fi
  fi
  # shellcheck disable=SC1091
  source "${LOOP_DIR}/state.env"
  ITER="${NEXT_ITERATION:-1}"
  STATUS="${LAST_STATUS:-READY}"
  ORIGIN_BRANCH="${ORIGIN_BRANCH:-}"
  ITER_BRANCH="${ITER_BRANCH:-}"
fi

#--- Branch isolation ---
if [[ "${BRANCH_ISOLATION}" == "true" ]] && [[ "${AUTOCOMMIT}" == "true" ]]; then
  branch_info=$(setup_branch_isolation "${LOOP_DIR}")
  ORIGIN_BRANCH="${branch_info%%|*}"
  ITER_BRANCH="${branch_info##*|}"
  echo "[BRANCH] Working on ${ITER_BRANCH} (origin: ${ORIGIN_BRANCH})"
fi

#--- Dirty baseline ---
if [[ "${AUTOCOMMIT}" == "true" ]]; then
  snapshot_dirty_baseline "${LOOP_DIR}"
fi

rotate_log "${LOOP_DIR}"

#--- Load audit data for skill selection ---
load_audit_scores() {
  cd "${SKILLS_DIR}"
  declare -gA SKILL_SCORE_MAP=()
  for skill_name in $(list_skill_dirs "${SKILLS_DIR}"); do
    local skill_file="${SKILLS_DIR}/${skill_name}/SKILL.md"
    if [[ ! -f "${skill_file}" ]]; then continue; fi
    local result
    result=$(compute_skill_score "${skill_file}")
    local total
    IFS='|' read -r total _ <<< "${result}"
    SKILL_SCORE_MAP["${skill_name}"]="${total}"
  done
}

#--- Select next skill (lowest score, not yet completed) ---
select_next_skill() {
  local completed_skills=""
  if [[ -f "${LOOP_DIR}/progress.md" ]]; then
    completed_skills=$(grep -oE 'Improved: [a-z-]+' "${LOOP_DIR}/progress.md" | sed 's/Improved: //' || true)
  fi

  local min_score=999
  local min_skill=""

  for skill_name in $(list_skill_dirs "${SKILLS_DIR}"); do
    # Skip already completed
    if echo "${completed_skills}" | grep -q "^${skill_name}$"; then
      continue
    fi

    local score="${SKILL_SCORE_MAP[${skill_name}]:-10.0}"
    local score_cmp
    score_cmp=$(echo "${score}" | sed 's/\.//')
    local threshold_cmp
    threshold_cmp=$(echo "${THRESHOLD}" | sed 's/\.//')

    # Only target skills below threshold
    if [[ "${score_cmp}" -ge "${threshold_cmp}" ]]; then
      continue
    fi

    if [[ "${score_cmp}" -lt "${min_score}" ]]; then
      min_score="${score_cmp}"
      min_skill="${skill_name}"
    fi
  done

  echo "${min_skill}"
}

#--- Build improvement prompt for claude ---
build_exec_prompt() {
  local skill_name="$1"
  local skill_file="${SKILLS_DIR}/${skill_name}/SKILL.md"
  local gaps
  gaps=$(identify_gaps "${skill_file}")
  local score="${SKILL_SCORE_MAP[${skill_name}]:-0.0}"

  local prompt="あなたはSKILL.md品質改善の専門家です。以下のスキルファイルを改善してください。

## 対象
${skill_file}

## 現在のスコア: ${score}/10.0
## 欠損セクション: ${gaps}

## 改善指示

以下の欠損セクションを追加してください。atlas/SKILL.md を模範として参照し、スキルのドメインに合わせた内容にしてください。

模範ファイル: ${SKILLS_DIR}/atlas/SKILL.md"

  # Add specific instructions per gap
  if echo "${gaps}" | grep -q "AUTORUN_SUPPORT"; then
    prompt="${prompt}

### ## AUTORUN Support の追加
以下の形式で追加（## Git Guidelines や ## Output Language の前、ファイル末尾付近に配置）:

## AUTORUN Support

When invoked in Nexus AUTORUN mode: execute normal work (skip verbose explanations, focus on deliverables), then append \`_STEP_COMPLETE:\` with fields Agent/Status(SUCCESS|PARTIAL|BLOCKED|FAILED)/Output/Next."
  fi

  if echo "${gaps}" | grep -q "NEXUS_HUB_MODE"; then
    prompt="${prompt}

### ## Nexus Hub Mode の追加
以下の形式で追加:

## Nexus Hub Mode

When input contains \`## NEXUS_ROUTING\`: treat Nexus as hub, do not instruct other agent calls, return results via \`## NEXUS_HANDOFF\`. Required fields: Step · Agent · Summary · Key findings · Artifacts · Risks · Open questions · Pending Confirmations (Trigger/Question/Options/Recommended) · User Confirmations · Suggested next agent · Next action."
  fi

  if echo "${gaps}" | grep -q "DAILY_PROCESS"; then
    prompt="${prompt}

### ## Daily Process の追加
以下の形式で追加（スキルのドメインに合わせた内容で）:

## Daily Process

| Phase | Focus | Key Actions |
|-------|-------|-------------|
| SURVEY | (ドメインに合った調査) | (具体的なアクション) |
| PLAN | (計画策定) | (具体的なアクション) |
| VERIFY | (検証) | (具体的なアクション) |
| PRESENT | (成果物提示) | (具体的なアクション) |"
  fi

  if echo "${gaps}" | grep -q "JAPANESE_DESCRIPTION"; then
    prompt="${prompt}

### frontmatter description の日本語化
frontmatter の description を日本語に翻訳してください。技術用語はそのまま使用可。"
  fi

  prompt="${prompt}

## 重要な注意
- 既存のセクション内容は変更しない（追加のみ）
- SKILL.mdの既存構造を維持する
- headingは正確に \`## AUTORUN Support\`, \`## Nexus Hub Mode\`, \`## Daily Process\` を使用
- ファイルの末尾に閉めの行（> で始まるブロッククォート）が既にある場合、新セクションはその前に挿入
- 出力は改善後の完全なファイル内容ではなく、編集操作のみ行ってください"

  echo "${prompt}"
}

#--- Main loop ---
echo ""
echo "=== Skill Improvement Loop ==="
echo "Max iterations: ${MAX_ITERATIONS}, Threshold: ${THRESHOLD}"
echo ""

load_audit_scores

while [[ "${STATUS}" != "DONE" ]] && [[ "${ITER}" -le "${MAX_ITERATIONS}" ]]; do
  [[ "${SHUTDOWN}" -eq 1 ]] && break

  ITER_START=$(date +%s)
  echo ""
  echo "=== Iteration ${ITER}/${MAX_ITERATIONS} ==="

  # Health check
  if ! iteration_health_check "${LOOP_DIR}"; then
    STATUS="BLOCKED"
    atomic_state_write "${LOOP_DIR}" "${ITER}" "BLOCKED" "${ORIGIN_BRANCH}" "${ITER_BRANCH}"
    break
  fi
  rotate_log "${LOOP_DIR}"

  # Select next skill
  CURRENT_SKILL=$(select_next_skill)
  if [[ -z "${CURRENT_SKILL}" ]]; then
    echo "[INFO] No more skills below threshold ${THRESHOLD} — checking done condition"
    # Verify all
    if bash "${SCRIPT_DIR}/verify.sh" --all --threshold "${THRESHOLD}" --skip-jp 2>&1 | tail -5; then
      STATUS="DONE"
      cat > "${LOOP_DIR}/done.md" <<DONE_EOF
# Done

All skills meet quality threshold ${THRESHOLD}.
Completed at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
Total iterations: ${ITER}
DONE_EOF
    else
      echo "[WARN] No candidate found but verify failed — refreshing scores"
      load_audit_scores
      CURRENT_SKILL=$(select_next_skill)
      if [[ -z "${CURRENT_SKILL}" ]]; then
        echo "[BLOCKED] Score refresh still finds no candidates"
        STATUS="BLOCKED"
        atomic_state_write "${LOOP_DIR}" "${ITER}" "BLOCKED" "${ORIGIN_BRANCH}" "${ITER_BRANCH}"
        break
      fi
    fi
  fi

  if [[ "${STATUS}" == "DONE" ]]; then
    break
  fi

  echo "[SELECT] Skill: ${CURRENT_SKILL} (score: ${SKILL_SCORE_MAP[${CURRENT_SKILL}]:-?})"

  # Build prompt
  EXEC_PROMPT=$(build_exec_prompt "${CURRENT_SKILL}")

  # Execute with retry
  EXEC_SUCCESS=false
  RETRY_COUNT=0
  while [[ "${RETRY_COUNT}" -lt "${RETRY_LIMIT}" ]]; do
    echo "[EXEC] Running ${EXEC_CMD} for ${CURRENT_SKILL} (attempt $((RETRY_COUNT + 1))/${RETRY_LIMIT})"
    if portable_timeout "${EXEC_TIMEOUT}" ${EXEC_CMD} -p "${EXEC_PROMPT}" --max-turns 5 --allowedTools Edit,Read,Glob,Grep 2>&1 | tee -a "${LOOP_DIR}/runner.log"; then
      EXEC_SUCCESS=true
      break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [[ "${RETRY_COUNT}" -lt "${RETRY_LIMIT}" ]]; then
      BACKOFF=$((RETRY_BACKOFF_BASE ** RETRY_COUNT))
      echo "[RETRY] Waiting ${BACKOFF}s before retry"
      sleep "${BACKOFF}"
    fi
  done

  if [[ "${EXEC_SUCCESS}" != "true" ]]; then
    echo "[BLOCKED] ${EXEC_CMD} failed after ${RETRY_LIMIT} retries for ${CURRENT_SKILL}" | tee -a "${LOOP_DIR}/runner.log"
    {
      echo ""
      echo "## Iteration ${ITER} — BLOCKED"
      echo "- Skill: ${CURRENT_SKILL}"
      echo "- TOOL_FAILURE: ${EXEC_CMD} failed after ${RETRY_LIMIT} retries"
      echo "- Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    } >> "${LOOP_DIR}/progress.md"
    STATUS="BLOCKED"
    atomic_state_write "${LOOP_DIR}" "${ITER}" "BLOCKED" "${ORIGIN_BRANCH}" "${ITER_BRANCH}"
    break
  fi

  # Verify improved skill
  VERIFY_RESULT="SKIP"
  if bash "${SCRIPT_DIR}/verify.sh" --skill "${CURRENT_SKILL}" --threshold "${THRESHOLD}" --skip-jp 2>&1 | tee -a "${LOOP_DIR}/runner.log"; then
    VERIFY_RESULT="PASS"
  else
    VERIFY_RESULT="FAIL"
  fi

  # Re-score
  local_score_result=$(compute_skill_score "${SKILLS_DIR}/${CURRENT_SKILL}/SKILL.md")
  local_new_score="${local_score_result%%|*}"
  SKILL_SCORE_MAP["${CURRENT_SKILL}"]="${local_new_score}"

  # Scoped auto-commit
  COMMIT_HASH="no-commit"
  if [[ "${AUTOCOMMIT}" == "true" ]]; then
    git add "${SKILLS_DIR}/${CURRENT_SKILL}/SKILL.md" 2>/dev/null || true
    if ! git diff --cached --quiet 2>/dev/null; then
      git commit -m "${COMMIT_MSG_PREFIX}: improve ${CURRENT_SKILL} quality (${local_new_score}/10) [verify=${VERIFY_RESULT}]"
      COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    fi
  fi

  # Progress update
  ITER_END=$(date +%s)
  ITER_DURATION=$((ITER_END - ITER_START))
  {
    echo ""
    echo "## Iteration ${ITER}"
    echo "- Improved: ${CURRENT_SKILL}"
    echo "- Score: ${SKILL_SCORE_MAP[${CURRENT_SKILL}]:-?} → ${local_new_score}"
    echo "- Verify: ${VERIFY_RESULT}"
    echo "- Commit: ${COMMIT_HASH}"
    echo "- Duration: ${ITER_DURATION}s"
    echo "- Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  } >> "${LOOP_DIR}/progress.md"

  STATUS="CONTINUE"
  NEXT_ITER=$((ITER + 1))
  atomic_state_write "${LOOP_DIR}" "${NEXT_ITER}" "${STATUS}" "${ORIGIN_BRANCH}" "${ITER_BRANCH}"

  echo "[ITER ${ITER}] skill=${CURRENT_SKILL} score=${local_new_score} verify=${VERIFY_RESULT} commit=${COMMIT_HASH} duration=${ITER_DURATION}s"
  ITER=${NEXT_ITER}
done

# Release lock
rm -f "${LOOP_DIR}/.run-loop.lock"

# Status footer
echo ""
echo "NEXUS_LOOP_STATUS: ${STATUS}"
echo "NEXUS_LOOP_SUMMARY: Iteration ${ITER}/${MAX_ITERATIONS}, status=${STATUS}"
