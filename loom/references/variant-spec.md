# Variant Specification for Figma Make

Reference for Loom's `variants` recipe. Define component variant matrix, Figma Variant property naming, and workarounds for Make's "1 variant per generated screen" constraint.

---

## 1. Variant Matrix Template

Per component, document the matrix in `Guidelines.md`:

```markdown
## Variants — Button

| Property | Values | Default |
|---|---|---|
| size | sm, md, lg | md |
| variant | primary, secondary, ghost, danger | primary |
| state | default, hover, active, disabled, loading | default |
| icon-position | none, leading, trailing, only | none |

Total combinations: 3 × 4 × 5 × 4 = 240 (filter to ≤ 24 generated)
```

Cap variants at **≤ 24 per Component Set** to stay within Make's rendering budget. Beyond 24, Make degrades or renders only a subset.

### Combinatorial pruning rules
- Drop combinations that don't make sense: `state=loading + icon-position=only`
- Skip rare combinations: `size=sm + variant=danger + state=disabled`
- Generate base set + delta variants (only changed states)

---

## 2. Figma Variant Property Naming

Figma convention: `kebab-case=value` per variant. Make follows this verbatim.

| Figma | TypeScript |
|---|---|
| `Button, size=md, variant=primary, state=hover` | `<Button size="md" variant="primary" state="hover" />` |

Naming alignment rules:
- Property names: kebab-case in Figma ↔ camelCase in TS
- Values: kebab-case or single-word in both
- Boolean property: `disabled=True` ↔ `disabled={true}` (Figma title-case → TS lowercase)

Document in Guidelines.md `## Variant API` section with both notations.

---

## 3. Default Variant Designation

Always declare default explicitly:

```markdown
### Default variant
- size: md
- variant: primary
- state: default
- icon-position: none

Rendered as: `<Button>Click me</Button>`
```

Make uses the default when generating "the first" variant. If unspecified, Make picks alphabetically — usually wrong.

---

## 4. Make's "1 Variant per Screen" Workaround

Make typically generates one variant per screen prompt. For a complete variant set, use staged prompts:

### Stage 1: Base variant
```
Generate Button component, size=md, variant=primary, state=default.
Use design system tokens: --color-brand, --space-md, --radius-md.
```

### Stage 2: Per-state delta (sequential)
```
Generate Button hover state: change background to var(--color-brand-hover),
keep all other properties identical to default.
```

### Stage 3: Per-size delta (parallel-safe)
```
Generate Button sm size: padding 0.25rem 0.5rem, font-size 0.875rem.
Generate Button lg size: padding 0.75rem 1.5rem, font-size 1.125rem.
```

### Stage 4: Per-variant delta (color theme swap)
```
Generate Button secondary: background transparent, border 1px solid var(--color-brand),
color var(--color-brand). Hover swaps to filled.
```

Document the staging plan in Guidelines.md `## Generation Plan`.

---

## 5. Component Set vs Single Component

**Component Set** (Figma Variant container):
- One set = one component with N variants
- Use when: states / sizes / themes vary
- Make picks variant via `<Component variant="x" state="y" />`

**Separate components**:
- One component per logical purpose
- Use when: structure differs significantly (Card vs CardWithImage)
- Make treats them independently

Rule of thumb: if HTML structure changes → separate component. If only CSS values change → variant in Component Set.

---

## 6. Verification

After generation, verify:
- All declared variants render correctly
- Default variant matches `Guidelines.md`
- Variant prop names match TS interface
- Boolean variants accept both `true` / `false`
- Disabled state has `aria-disabled="true"` and reduced contrast (still ≥ 3:1 for non-text)
- Loading state has `aria-busy="true"`

---

## 7. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Variant count > 24 → Make renders subset | Prune combinatorial explosion; generate deltas |
| Property names mismatched (Figma vs TS) | Document both; use codegen if possible |
| Default variant unspecified → Make picks wrong | Explicit `### Default variant` block |
| `disabled=True` confused with `True` text node | Boolean property: title-case in Figma, lowercase in TS |
| Loading state = visual only, no `aria-busy` | Always include a11y attributes per state |
| Variant API documented in code only, not Guidelines | Mirror in both for Make consumption |
| Generating all 24 in one prompt → degraded quality | Stage prompts; max 4 variants per call |

---

## 8. Decision Walkthrough Template

```
Component: ____________
Properties (≤ 4 recommended):
  - ____ : [____, ____, ____]  default: ____
  - ____ : [____, ____]  default: ____
  - ____ : [____, ____, ____, ____]  default: ____

Total combinations: ___
Filtered (after pruning): ___ (≤ 24)

Generation staging:
  Stage 1 — Base variant:        ____
  Stage 2 — Per-state delta:     ____ (states: hover, active, disabled, loading)
  Stage 3 — Per-size delta:      ____ (sizes: sm, md, lg)
  Stage 4 — Per-variant delta:   ____ (variants: secondary, ghost, danger)

Guidelines.md sections:
  □ ## Variants — <Component>
  □ ## Variant API
  □ ## Default variant
  □ ## Generation Plan

Verification:
  □ All variants render
  □ Default matches docs
  □ Prop names align
  □ a11y attributes per state
```

---

## 9. References
- Figma Variants documentation
- Figma Make package-aware generation guide
- W3C ARIA states (`aria-disabled`, `aria-busy`)
