#!/bin/bash
# Shared utilities for skill-improve scripts
# Sources: orbit/references/script-templates.md patterns

#--- Portable timeout (macOS + Linux) ---
portable_timeout() {
  local secs="$1"; shift
  if command -v timeout >/dev/null 2>&1; then
    timeout "${secs}" "$@"
  elif command -v gtimeout >/dev/null 2>&1; then
    gtimeout "${secs}" "$@"
  else
    perl -e '
      use POSIX ":sys_wait_h";
      my $timeout = shift @ARGV;
      my $pid = fork // die "fork: $!";
      if ($pid == 0) { exec @ARGV; die "exec: $!" }
      local $SIG{ALRM} = sub { kill "TERM", $pid; waitpid($pid, 0); exit 124 };
      alarm $timeout;
      waitpid($pid, 0);
      alarm 0;
      exit($? >> 8);
    ' "${secs}" "$@"
  fi
}

#--- Pre-flight checks ---
preflight_check() {
  local loop_dir="${1:-.nexus-loop/skill-improve}"

  # Disk space check (abort if < 100MB free)
  local avail_kb
  avail_kb=$(df -k "${loop_dir}" | awk 'NR==2{print $4}')
  if [[ "${avail_kb}" -lt 102400 ]]; then
    echo "[PREFLIGHT:FAIL] Disk space critically low: ${avail_kb}KB available (< 100MB)"
    return 1
  fi

  # Stale lock detection
  if [[ -f "${loop_dir}/.run-loop.lock" ]]; then
    local lock_pid
    lock_pid=$(cat "${loop_dir}/.run-loop.lock")
    if kill -0 "${lock_pid}" 2>/dev/null; then
      echo "[PREFLIGHT:FAIL] Active lock — PID ${lock_pid} is running"
      return 1
    else
      echo "[PREFLIGHT:WARN] Stale lock — PID ${lock_pid} dead, removing"
      rm -f "${loop_dir}/.run-loop.lock"
    fi
  fi

  # Git repository health
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "[PREFLIGHT:FAIL] Not inside a git repository"
    return 1
  fi
  if [[ -d .git/rebase-merge ]] || [[ -d .git/rebase-apply ]]; then
    echo "[PREFLIGHT:FAIL] Git rebase in progress — resolve before running"
    return 1
  fi

  echo "[PREFLIGHT] All checks passed"
  return 0
}

#--- Log rotation ---
rotate_log() {
  local loop_dir="${1:-.nexus-loop/skill-improve}"
  local max_size="${2:-5242880}"
  if [[ -f "${loop_dir}/runner.log" ]]; then
    local log_size
    log_size=$(wc -c < "${loop_dir}/runner.log" 2>/dev/null || echo 0)
    if [[ "${log_size}" -gt "${max_size}" ]]; then
      mv "${loop_dir}/runner.log" "${loop_dir}/runner.log.prev"
      echo "[LOG] Rotated runner.log (${log_size} bytes)"
    fi
  fi
}

#--- Iteration health check ---
iteration_health_check() {
  local loop_dir="${1:-.nexus-loop/skill-improve}"

  local avail_kb
  avail_kb=$(df -k "${loop_dir}" | awk 'NR==2{print $4}')
  if [[ "${avail_kb}" -lt 51200 ]]; then
    echo "[HEALTH:BLOCKED] Disk space low: ${avail_kb}KB (< 50MB)"
    return 1
  fi
  if [[ -d .git/rebase-merge ]] || [[ -d .git/rebase-apply ]]; then
    echo "[HEALTH:BLOCKED] Git rebase in progress"
    return 1
  fi
  return 0
}

#--- Atomic state write ---
atomic_state_write() {
  local loop_dir="$1"
  local next_iter="$2"
  local status="$3"
  local origin_branch="${4:-}"
  local iter_branch="${5:-}"

  local state_tmp
  state_tmp=$(mktemp "${loop_dir}/state.env.XXXXXX")
  cat > "${state_tmp}" <<STATE_EOF
NEXT_ITERATION=${next_iter}
LAST_STATUS=${status}
LAST_UPDATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ORIGIN_BRANCH=${origin_branch}
ITER_BRANCH=${iter_branch}
STATE_EOF
  mv "${state_tmp}" "${loop_dir}/state.env"
  shasum -a 256 "${loop_dir}/state.env" | awk '{print $1}' > "${loop_dir}/state.env.sha256"
}

#--- Validate state checksum ---
validate_state_checksum() {
  local loop_dir="${1:-.nexus-loop/skill-improve}"
  if [[ ! -f "${loop_dir}/state.env.sha256" ]]; then
    return 0  # No checksum file = skip validation
  fi
  local expected actual
  expected=$(cat "${loop_dir}/state.env.sha256")
  actual=$(shasum -a 256 "${loop_dir}/state.env" | awk '{print $1}')
  if [[ "${expected}" != "${actual}" ]]; then
    echo "[WARN] state.env checksum mismatch"
    return 1
  fi
  return 0
}

#--- Branch isolation setup ---
setup_branch_isolation() {
  local loop_dir="$1"
  local loop_name
  loop_name=$(basename "${loop_dir}" | sed 's/^\.//')
  local iter_branch="loop/iter-${loop_name}"

  # Determine origin branch
  local origin_branch
  if [[ -n "${ORIGIN_BRANCH:-}" ]]; then
    origin_branch="${ORIGIN_BRANCH}"
  else
    origin_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
  fi

  local current_branch
  current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
  if [[ "${current_branch}" != "${iter_branch}" ]]; then
    local stashed=false
    if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
      git stash push -m "skill-improve-branch-isolation"
      stashed=true
    fi
    if git rev-parse --verify "${iter_branch}" >/dev/null 2>&1; then
      git checkout "${iter_branch}"
    else
      git checkout -b "${iter_branch}"
    fi
    if [[ "${stashed}" == "true" ]]; then
      git stash pop || echo "[BRANCH:WARN] Stash pop conflict — manual resolution needed"
    fi
  fi

  echo "${origin_branch}|${iter_branch}"
}

#--- Dirty baseline snapshot ---
snapshot_dirty_baseline() {
  local loop_dir="$1"
  {
    git diff --name-only 2>/dev/null || true
    git diff --cached --name-only 2>/dev/null || true
    git ls-files --others --exclude-standard 2>/dev/null || true
  } | sort -u > "${loop_dir}/dirty-start-paths.txt"
}

#--- Resolve SKILLS_DIR from script location ---
resolve_skills_dir() {
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[1]:-$0}")" && pwd)"
  # _scripts/skill-improve/*.sh → go up 2 levels
  echo "$(cd "${script_dir}/../.." && pwd)"
}

#--- List all skill directories (excluding non-skill dirs) ---
SKIP_DIRS="_common|_templates|_scripts|\.nexus-loop"
list_skill_dirs() {
  local skills_dir="$1"
  for d in "${skills_dir}"/*/SKILL.md; do
    local name
    name=$(basename "$(dirname "$d")")
    if echo "${name}" | grep -qE "^(${SKIP_DIRS})$"; then
      continue
    fi
    echo "${name}"
  done | sort
}
