# Hearth Handoff Formats

Standardized handoff templates for agent collaboration.

---

## Input Handoffs (→ Hearth)

### SCAFFOLD_TO_HEARTH_HANDOFF

```markdown
## SCAFFOLD_TO_HEARTH_HANDOFF

**Environment Provisioned**: [Description — e.g., "Ubuntu 22.04 dev server"]
**Platform**: [macOS / Linux distro / WSL]
**Installed Tools**: [List of tools already provisioned]

**Personal Setup Needed**:
- Shell: [zsh/fish/bash — if preference known]
- Editor: [neovim/vim — if preference known]
- Terminal: [ghostty/alacritty/kitty — if preference known]
- Profile level: [minimal/standard/power]

**Request**: Configure personal development environment on newly provisioned machine
```

### SENTINEL_TO_HEARTH_HANDOFF

```markdown
## SENTINEL_TO_HEARTH_HANDOFF

**Security Audit Findings**: [Description]
**Config Files Reviewed**:
| File | Issue | Severity |
|------|-------|----------|
| [path] | [finding] | [High/Medium/Low] |

**Recommendations**:
- [Fix 1 — e.g., "Remove hardcoded token from .zshrc"]
- [Fix 2 — e.g., "Set file permission to 600 for .gitconfig"]
- [Fix 3 — e.g., "Add .env to global gitignore"]

**Request**: Remediate security issues in personal config files
```

### ANVIL_TO_HEARTH_HANDOFF

```markdown
## ANVIL_TO_HEARTH_HANDOFF

**CLI Tool Created**: [Tool name and description]
**Shell Integration Needed**:
- Completion scripts: [bash/zsh/fish]
- PATH setup: [binary location]
- Aliases: [suggested aliases]

**XDG Compliance**:
- Config: [XDG_CONFIG_HOME/tool-name/]
- Data: [XDG_DATA_HOME/tool-name/]
- Cache: [XDG_CACHE_HOME/tool-name/]

**Request**: Integrate new CLI tool into shell environment
```

### NEXUS_TO_HEARTH_HANDOFF

```markdown
## NEXUS_TO_HEARTH_HANDOFF

**Config Task**: [Description]
**Target Tool**: [zsh/neovim/tmux/ghostty/etc.]
**Profile Level**: [minimal/standard/power]

**Context**:
- Platform: [macOS/Linux]
- Current shell: [current $SHELL]
- Existing config: [yes/no — path if yes]
- Specific requirements: [user preferences]

**Request**: [Specific configuration deliverable]
```

---

## Output Handoffs (Hearth →)

### HEARTH_TO_GEAR_HANDOFF

```markdown
## HEARTH_TO_GEAR_HANDOFF

**Personal Config Complete**: [What was configured]
**Environment Details**:
| Tool | Version | Config Path |
|------|---------|-------------|
| [tool] | [version] | [path] |

**Project-Level Setup Needed**:
- Linter/Formatter: [ESLint/Prettier/Biome — per project requirements]
- Git hooks: [Husky/Lefthook — if not yet configured]
- CI/CD: [pipeline needs based on project type]

**Notes**:
- Shell: [configured shell and plugin manager]
- Editor LSP: [configured language servers — may overlap with project config]

**Request**: Set up project-level development tooling
```

### HEARTH_TO_ANVIL_HANDOFF

```markdown
## HEARTH_TO_ANVIL_HANDOFF

**Shell Environment Ready**: [Shell and version]
**Integration Patterns**:
- Completion framework: [zsh-completions / built-in]
- Plugin system: [sheldon / zinit / none]
- XDG paths: [configured XDG directories]

**CLI Integration Needed**:
- Tool: [CLI tool name]
- Completion: [generate completion script for configured shell]
- Alias suggestions: [based on user's alias patterns]

**Request**: Generate shell integration for CLI tool
```

---

## Collaboration Patterns

### Pattern A: Post-Provision Personal Setup
```
Scaffold (provision) → SCAFFOLD_TO_HEARTH → Hearth (personal config) → HEARTH_TO_GEAR → Gear (project config)
```

### Pattern B: Security Remediation
```
Sentinel (audit) → SENTINEL_TO_HEARTH → Hearth (fix configs) → Sentinel (re-verify)
```

### Pattern C: CLI Integration
```
Anvil (CLI created) → ANVIL_TO_HEARTH → Hearth (shell integration) → HEARTH_TO_ANVIL → Anvil (verify)
```

### Pattern D: Full Environment Setup
```
Scaffold → Hearth (personal) → HEARTH_TO_GEAR → Gear (project) → Sentinel (security audit)
```

### Pattern E: Tool-Config Coordination
```
Hearth (personal git config) → HEARTH_TO_GEAR → Gear (git hooks, CI config)
```

---

## AUTORUN Handoff Formats

### _AGENT_CONTEXT (Input)

```yaml
_AGENT_CONTEXT:
  Role: Hearth
  Task: "Configure zsh environment with sheldon plugin manager"
  Mode: AUTORUN
  Chain: Scaffold → Hearth → Gear
  Input:
    platform: macOS
    shell: zsh
    profile: standard
    existing_config: false
  Constraints:
    - Use sheldon for plugin management
    - XDG compliant paths
    - Startup time < 200ms
  Expected_Output:
    - ~/.config/zsh/.zshrc
    - ~/.config/sheldon/plugins.toml
    - Verification results (syntax check, startup time)
```

### _STEP_COMPLETE (Output)

```yaml
_STEP_COMPLETE:
  Agent: Hearth
  Status: SUCCESS
  Output:
    configs_generated:
      - ~/.config/zsh/.zshrc
      - ~/.config/zsh/aliases.zsh
      - ~/.config/zsh/functions.zsh
      - ~/.config/sheldon/plugins.toml
    backups_created:
      - ~/.zshrc.bak.20250115
    files_changed:
      - path: ~/.config/zsh/.zshrc
        type: created
        changes: "Modular zsh config with sheldon plugin management"
      - path: ~/.config/sheldon/plugins.toml
        type: created
        changes: "sheldon config with autosuggestions, syntax-highlighting, completions"
    verification:
      - tool: zsh
        check: syntax
        result: PASS
      - tool: zsh
        check: startup_time
        result: "142ms (target: <200ms)"
  Handoff:
    Format: HEARTH_TO_GEAR_HANDOFF
    Content: |
      Personal zsh environment configured with sheldon plugin manager.
      Shell startup time: 142ms. XDG compliant paths.
      Ready for project-level tool configuration.
  Artifacts:
    - "~/.config/zsh/ (4 files)"
    - "~/.config/sheldon/plugins.toml"
    - "~/.zshrc.bak.20250115 (backup)"
  Risks:
    - "Existing shell aliases may conflict with new aliases"
  Next: Gear
  Reason: "Personal config complete, project-level setup needed"
```

---

## NEXUS_HANDOFF Format

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: Hearth
- Summary: [1-3 line summary of what was configured]
- Key findings / decisions:
  - [Tool and version detected]
  - [Profile level chosen]
  - [Merge/overwrite decision for existing configs]
- Artifacts (files/commands/links):
  - [Config file 1]
  - [Config file 2]
  - [Backup file 1]
- Risks / trade-offs:
  - [Potential conflicts with existing setup]
  - [Startup time impact]
- Open questions (blocking/non-blocking):
  - [Any unresolved config decisions]
- Pending Confirmations:
  - Trigger: ON_EXISTING_CONFIG
  - Question: 既存の設定ファイルが検出されました。どう処理しますか？
  - Options: マージ / 上書き / スキップ
  - Recommended: マージ
- User Confirmations:
  - Q: どのプロファイルレベルで設定しますか？ → A: Standard
- Suggested next agent: Gear (project-level configuration)
- Next action: CONTINUE | VERIFY | DONE
```
