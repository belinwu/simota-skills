# Token Alignment Guide

Figma Variables と コードトークンの比較手法、差分レポートテンプレート。

---

## Overview

トークン整合性監査は以下の4軸で実施する：

| Axis | What to Compare | Priority |
|------|----------------|----------|
| **Name** | トークン名の一致・対応関係 | High |
| **Value** | 実際の値（色コード、px値等）の一致 | High |
| **Semantics** | セマンティックな意味の一致 | Medium |
| **Hierarchy** | グループ/コレクション構造の対応 | Low |

---

## Token Source Identification

### Code Side Sources

| Source Type | Location Pattern | Extraction Method |
|------------|-----------------|-------------------|
| **CSS Custom Properties** | `--token-name: value` in `:root` / `[data-theme]` | Grep for `--` prefix patterns |
| **Tailwind Config** | `tailwind.config.{js,ts}` → `theme.extend` | Parse config object |
| **Tailwind v4** | `@theme { }` blocks in CSS | Parse `@theme` declarations |
| **Panda CSS** | `panda.config.{ts,js}` → `tokens` / `semanticTokens` | Parse config |
| **Style Dictionary** | `tokens/**/*.json` (W3C DTCG format) | Parse `$value` / `$type` |
| **CSS-in-JS** | Theme objects in `theme.{ts,js}` | Parse exported objects |
| **SCSS Variables** | `$token-name: value` in `_variables.scss` | Grep for `$` prefix |

### Figma Side Sources

| Source | Access Method | Data Format |
|--------|-------------|-------------|
| **Figma Variables** | Frame → `get_variable_defs` MCP | Collections → Modes → Variables |
| **Local Styles** | Frame → `get_design_context` MCP | Color/Text/Effect styles |
| **Design System Rules** | Frame → `create_design_system_rules` MCP | Structured rules JSON |

---

## Comparison Process

### Step 1: Inventory

コード側とFigma側のトークンを一覧化する。

```markdown
### Code Token Inventory

| Token Name | Value (Light) | Value (Dark) | Category | Source File |
|-----------|---------------|--------------|----------|-------------|
| `--color-primary` | `#3B82F6` | `#60A5FA` | Color | `globals.css` |
| `--space-4` | `16px` | — | Spacing | `globals.css` |
| ... | ... | ... | ... | ... |

### Figma Variables Inventory

| Variable Name | Value (Light) | Value (Dark) | Collection | Mode |
|--------------|---------------|--------------|------------|------|
| `color/primary` | `#3B82F6` | `#60A5FA` | Primitives | Light/Dark |
| `space/4` | `16` | — | Spacing | Default |
| ... | ... | ... | ... | ... |
```

### Step 2: Name Mapping

名前の対応関係を確立する。

```markdown
### Name Mapping Rules

| Code Pattern | Figma Pattern | Status |
|-------------|--------------|--------|
| `--color-{name}` | `color/{name}` | Mapped |
| `--space-{n}` | `space/{n}` | Mapped |
| `--font-size-{name}` | `typography/{name}/size` | Mapped (restructured) |
| `--shadow-{name}` | `elevation/{name}` | Mapped (renamed) |
| `--radius-{name}` | (none) | Missing in Figma |
```

### Step 3: Value Comparison

値の差異を検出する。

**Color comparison tolerance:**
- Exact match: `#3B82F6` === `#3B82F6` → OK
- Near match (ΔE < 3): Visually indistinguishable → WARNING
- Mismatch (ΔE >= 3): Noticeable difference → ERROR

**Spacing comparison:**
- Exact match: `16px` === `16` → OK (unit normalization)
- Off-grid: value not on 4px/8px grid → WARNING
- Mismatch: different value → ERROR

**Typography comparison:**
- Font size: exact match required
- Font weight: exact match required
- Line height: ±0.05 tolerance (e.g., 1.5 vs 1.5 → OK)
- Font family: name match (ignore format differences)

### Step 4: Diff Classification

差分をカテゴリ分類する。

| Category | Code | Definition | Priority |
|----------|------|------------|----------|
| **MISSING_IN_FIGMA** | MIF | コードに存在するがFigma Variableにない | High |
| **MISSING_IN_CODE** | MIC | Figma Variableに存在するがコードにない | Medium |
| **VALUE_MISMATCH** | VM | 同名だが値が異なる | High |
| **NAME_DRIFT** | ND | 異なる名前だが同じ意味・値 | Medium |
| **SEMANTIC_GAP** | SG | 同じ primitive だが異なる semantic 使用 | Medium |
| **ORPHANED** | OR | 片方にしかなく、対応候補もない | Low |
| **STRUCTURE_DIFF** | SD | グループ/コレクション構造の違い | Low |

---

## Priority Calculation

```
Priority Score = Impact × Frequency × Visibility
```

| Factor | Scale | Description |
|--------|-------|-------------|
| **Impact** | 1-3 | 1: 装飾的, 2: 機能的, 3: ブランド/a11y |
| **Frequency** | 1-3 | 1: 1箇所, 2: 複数箇所, 3: 全体的 |
| **Visibility** | 1-3 | 1: 内部のみ, 2: 一部ユーザー, 3: 全ユーザー |

| Total Score | Priority | Action |
|------------|----------|--------|
| 18-27 | **P0 — Critical** | 即時対応。Guidelines生成をブロック |
| 9-17 | **P1 — High** | Guidelines生成可能だが、早期修正を推奨 |
| 4-8 | **P2 — Medium** | 次回更新時に対応 |
| 1-3 | **P3 — Low** | 記録のみ。必要に応じて対応 |

---

## Diff Report Template

```markdown
## Token Alignment Report

### Summary
- **Report date:** [YYYY-MM-DD]
- **Code source:** [commit hash / config file paths]
- **Figma source:** [file URL / variable collection names]
- **Total code tokens:** [count]
- **Total Figma variables:** [count]
- **Alignment rate:** [XX%]
- **Issues found:** [count] (P0: [n], P1: [n], P2: [n], P3: [n])

### Alignment Matrix

| Category | Code | Figma | Matched | Mismatched | Missing |
|----------|------|-------|---------|------------|---------|
| Colors | [n] | [n] | [n] | [n] | [n] |
| Spacing | [n] | [n] | [n] | [n] | [n] |
| Typography | [n] | [n] | [n] | [n] | [n] |
| Shadows | [n] | [n] | [n] | [n] | [n] |
| Borders | [n] | [n] | [n] | [n] | [n] |
| **Total** | **[n]** | **[n]** | **[n]** | **[n]** | **[n]** |

### Critical Issues (P0)

| # | Type | Code Token | Figma Variable | Code Value | Figma Value | Impact |
|---|------|-----------|---------------|-----------|-------------|--------|
| 1 | [VM/MIF/...] | [name] | [name] | [value] | [value] | [description] |

### High Priority Issues (P1)

| # | Type | Code Token | Figma Variable | Code Value | Figma Value | Recommendation |
|---|------|-----------|---------------|-----------|-------------|----------------|
| 1 | [type] | [name] | [name] | [value] | [value] | [action] |

### Medium Priority Issues (P2)

(Same format as P1)

### Low Priority Issues (P3)

(Same format, or summary count only)

### Recommendations

1. **For Muse (token owner):**
   - [Token changes to propose]
   - [New tokens to define]

2. **For Guidelines.md:**
   - [Rules to add/update based on alignment gaps]
   - [Mapping overrides to document]

3. **For Frame (Figma side):**
   - [Variables to request creation/update]
   - [Collections to reorganize]

### Name Mapping Table

| Code Token | Figma Variable | Status | Notes |
|-----------|---------------|--------|-------|
| `--color-primary` | `color/primary` | Matched | — |
| `--space-lg` | `space/6` | Name Drift | Same value (24px), different name |
| `--radius-md` | (none) | Missing | Create in Figma |
| (none) | `deprecated/old-blue` | Orphaned | Safe to remove from Figma |
```

---

## Automation Opportunities

トークン整合性チェックの一部は自動化可能：

| Step | Automation Level | Method |
|------|-----------------|--------|
| Code token extraction | High | AST parse / regex scan of config files |
| Figma Variables extraction | High | Frame → `get_variable_defs` MCP |
| Name matching | Medium | Fuzzy matching with naming rule transforms |
| Value comparison | High | Exact/tolerance-based comparison |
| Priority scoring | Medium | Heuristic based on usage frequency analysis |
| Report generation | High | Template-based markdown generation |

### When to Run

| Trigger | Scope | Depth |
|---------|-------|-------|
| New Guidelines.md generation | Full | All axes |
| Token definition change (code) | Incremental | Changed tokens only |
| Figma Variables update | Incremental | Changed variables only |
| Pre-release check | Full | All axes |
| On-demand audit request | Full or scoped | As specified |
