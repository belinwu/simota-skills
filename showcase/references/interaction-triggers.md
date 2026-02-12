# Showcase Interaction Triggers

Question templates for `AskUserQuestion` at key decision points.
See `_common/INTERACTION.md` for standard formats.

---

## ON_STORY_SCOPE

```yaml
questions:
  - question: "What scope should the stories cover?"
    header: "Scope"
    options:
      - label: "Single component (Recommended)"
        description: "Cover all variants of one component"
      - label: "Feature group"
        description: "Document related components together"
      - label: "Page level"
        description: "Create stories for entire page compositions"
    multiSelect: false
```

## ON_TOOL_SELECTION

```yaml
questions:
  - question: "Which component catalog tool should we use?"
    header: "Tool"
    options:
      - label: "Storybook (Recommended)"
        description: "Rich docs, addons, visual regression - best for design systems"
      - label: "React Cosmos"
        description: "Lightweight, fast iteration, fixture-based - best for dev speed"
      - label: "Both (Cosmos + Storybook)"
        description: "Cosmos for dev iteration, Storybook for docs and visual testing"
      - label: "Histoire (Vue/Svelte)"
        description: "Native Vue/Svelte integration with built-in controls"
    multiSelect: false
```

## ON_VISUAL_TEST_SETUP

```yaml
questions:
  - question: "How would you like to set up Visual Regression Testing?"
    header: "Visual Test"
    options:
      - label: "Chromatic (Recommended)"
        description: "Cloud-based, by Storybook maintainers, seamless integration"
      - label: "Playwright snapshots"
        description: "Local, free, requires CI setup"
      - label: "Lost Pixel"
        description: "Open source, GitHub Action integration"
      - label: "Skip for now"
        description: "Set up visual testing later"
    multiSelect: false
```

## ON_A11Y_CRITICAL

```yaml
questions:
  - question: "Critical accessibility issue detected. How should we proceed?"
    header: "A11y"
    options:
      - label: "Fix now (Recommended)"
        description: "Address the accessibility violation before continuing"
      - label: "Add to backlog"
        description: "Document the issue and continue with story creation"
      - label: "Suppress with rationale"
        description: "Disable the rule with documented justification"
    multiSelect: false
```

## ON_ADDON_ADD

```yaml
questions:
  - question: "Should we add this Storybook addon?"
    header: "Addon"
    options:
      - label: "Install addon (Recommended)"
        description: "Add the addon and configure it for the project"
      - label: "Skip addon"
        description: "Proceed without the addon functionality"
      - label: "Use alternative"
        description: "Implement the functionality with a different approach"
    multiSelect: false
```

## ON_CSF_MIGRATION

```yaml
questions:
  - question: "How should we handle CSF 2 → CSF 3 migration?"
    header: "Migration"
    options:
      - label: "Migrate incrementally (Recommended)"
        description: "Convert files one at a time, verify each migration"
      - label: "Bulk migration"
        description: "Convert all stories at once using codemod"
      - label: "New files only"
        description: "Use CSF 3 for new stories, leave existing as-is"
    multiSelect: false
```
