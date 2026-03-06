# Token Alignment Guide

Figma Variables と コードトークンの比較手法、差分レポートテンプレート。W3C Design Tokens 1.0 準拠。

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
| **W3C DTCG** | `tokens/**/*.json` (`$value` / `$type`) | Parse W3C Design Tokens 1.0 format (preferred standard) |
| **CSS Custom Properties** | `--token-name: value` in `:root` / `[data-theme]` | Grep for `--` prefix patterns |
| **Tailwind Config** | `tailwind.config.{js,ts}` → `theme.extend` | Parse config object |
| **Tailwind v4** | `@theme { }` blocks in CSS | Parse `@theme` declarations |
| **Panda CSS** | `panda.config.{ts,js}` → `tokens` / `semanticTokens` | Parse config |
| **Style Dictionary** | `tokens/**/*.json` | Parse `$value` / `$type` |
| **CSS-in-JS** | Theme objects in `theme.{ts,js}` | Parse exported objects |
| **SCSS Variables** | `$token-name: value` in `_variables.scss` | Grep for `$` prefix |

**W3C Design Tokens 1.0 note:** The W3C Design Tokens Community Group has finalized the 1.0 specification. Figma supports native import/export of this format. When a project uses DTCG format, treat it as the canonical source.

### Figma Side Sources

| Source | Access Method | Data Format |
|--------|-------------|-------------|
| **Figma Variables** | Frame → `get_variable_defs` MCP | Collections → Modes → Variables |
| **Local Styles** | Frame → `get_design_context` MCP | Color/Text/Effect styles |
| **Check Designs** | Figma AI linter (Early Access) | Detects hardcoded values, suggests variables |
| **Design System Rules** | Frame → `create_design_system_rules` MCP | Structured rules JSON |

### Emerging: Expression Tokens

Figma is rolling out Expression Tokens (late 2025/early 2026) enabling:
- Conditional logic in tokens (if/else based on context)
- Mathematical calculations (e.g., `base-spacing * 2`)
- Context-driven dynamic UI values

When available, the alignment audit should account for expression-based tokens that cannot be compared as simple key-value pairs.

---

## Comparison Process

### Step 1: Inventory

コード側とFigma側のトークンを一覧化する。

```markdown
### Code Token Inventory

| Token Name | Value (Light) | Value (Dark) | Category | Source File | Format |
|-----------|---------------|--------------|----------|-------------|--------|
| `--color-primary` | `#3B82F6` | `#60A5FA` | Color | `globals.css` | CSS vars |
| `--space-4` | `16px` | — | Spacing | `globals.css` | CSS vars |

### Figma Variables Inventory

| Variable Name | Value (Light) | Value (Dark) | Collection | Mode |
|--------------|---------------|--------------|------------|------|
| `color/primary` | `#3B82F6` | `#60A5FA` | Primitives | Light/Dark |
| `space/4` | `16` | — | Spacing | Default |
```

### Step 2: Name Mapping

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
- Line height: ±0.05 tolerance
- Font family: name match (ignore format differences)

### Step 4: Diff Classification

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

## Multi-Brand Considerations

Schema 2025 の Extended Collections (Enterprise) を使用するプロジェクトの場合：

- **Parent collection**: コアデザインシステム（全ブランド共通）
- **Child collections**: ブランド固有のオーバーライド
- 子コレクションは親の更新を継承しつつ独自値を保持

監査時は親→子の継承チェーンを追跡し、オーバーライドの意図的な差分と意図しないドリフトを区別する。

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
| 1-3 | **P3 — Low** | 記録のみ |

---

## Diff Report Template

```markdown
## Token Alignment Report

### Summary
- **Report date:** [YYYY-MM-DD]
- **Code source:** [commit hash / config file paths]
- **Figma source:** [file URL / variable collection names]
- **Token format:** [W3C DTCG | CSS vars | Tailwind | Panda CSS | other]
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

### Recommendations

1. **For Muse (token owner):** [Token changes to propose]
2. **For Guidelines.md:** [Rules to add/update]
3. **For Frame (Figma side):** [Variables to create/update]
4. **Check Designs linter:** [If available, run Check Designs to auto-detect hardcoded values]
```

---

## Automation Opportunities

| Step | Automation Level | Method |
|------|-----------------|--------|
| Code token extraction | High | AST parse / regex scan of config files |
| Figma Variables extraction | High | Frame → `get_variable_defs` MCP |
| Name matching | Medium | Fuzzy matching with naming rule transforms |
| Value comparison | High | Exact/tolerance-based comparison |
| Check Designs integration | High | Figma AI linter (when available) |
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
