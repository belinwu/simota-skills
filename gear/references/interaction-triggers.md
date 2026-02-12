# Gear: Interaction Trigger Templates

Question templates for `AskUserQuestion` tool. See SKILL.md for trigger table.

## ON_INFRA_CHANGE

```yaml
questions:
  - question: "Infrastructure configuration will be changed. What scope would you like to apply?"
    header: "Infra Change"
    options:
      - label: "Minimal changes (Recommended)"
        description: "Modify only necessary parts, leave other settings untouched"
      - label: "Optimize including related settings"
        description: "Improve surrounding settings as well"
      - label: "Review impact scope first"
        description: "Display list of affected files before making changes"
    multiSelect: false
```

## ON_DEPENDENCY_UPDATE

```yaml
questions:
  - question: "Dependencies will be updated. Which approach would you like to use?"
    header: "Dep Update"
    options:
      - label: "Patch/Minor only (Recommended)"
        description: "Update within safe range, avoid breaking changes"
      - label: "Include major versions"
        description: "Follow latest versions, migration work required"
      - label: "Security fixes only"
        description: "Address only vulnerabilities detected by audit"
    multiSelect: false
```

## ON_CI_CHANGE

```yaml
questions:
  - question: "CI/CD pipeline will be modified. How would you like to proceed?"
    header: "CI/CD Change"
    options:
      - label: "Apply incrementally (Recommended)"
        description: "Verify on one job first, deploy after success"
      - label: "Apply all at once"
        description: "Update all workflows simultaneously"
      - label: "Dry run review"
        description: "Display changes only, defer execution"
    multiSelect: false
```

## ON_ENV_CHANGE

```yaml
questions:
  - question: "Environment variables or secrets management will be modified. How would you like to handle this?"
    header: "Env Config"
    options:
      - label: "Update .env.example only (Recommended)"
        description: "Update template, do not touch actual values"
      - label: "Review secrets management"
        description: "Include GitHub Secrets and other settings"
      - label: "Documentation only"
        description: "Document changes in README, defer implementation"
    multiSelect: false
```

## ON_BUILD_TOOL_CHANGE

```yaml
questions:
  - question: "Build toolchain change is being considered. How would you like to proceed?"
    header: "Build Tools"
    options:
      - label: "Optimize existing tools (Recommended)"
        description: "Improve current tool configuration"
      - label: "Gradual migration"
        description: "Set up parallel operation period and switch gradually"
      - label: "PoC verification"
        description: "Try new tool in separate branch and report results"
    multiSelect: false
```

## ON_MONOREPO_CHANGE

```yaml
questions:
  - question: "Monorepo configuration will be changed. How would you like to proceed?"
    header: "Monorepo"
    options:
      - label: "Workspace settings only (Recommended)"
        description: "Change only pnpm-workspace.yaml or package.json workspaces"
      - label: "Include build pipeline"
        description: "Include Turborepo / NX settings changes"
      - label: "Impact analysis first"
        description: "Confirm scope of impact before making changes"
    multiSelect: false
```
