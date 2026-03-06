# Figma Make Constraints

Figma Make の既知制約、プラットフォーム制限、挙動上の quirks、および回避パターン集。

---

## Platform Constraints

| Constraint | Detail | Impact |
|-----------|--------|--------|
| **React only** | Figma Make のコード生成は React のみ対応。Vue, Angular, Svelte 等は非対応 | 非 React プロジェクトでは Guidelines はデザイン出力のみに活用。コード生成は利用不可 |
| **Per-file Guidelines** | Guidelines.md はファイルごとに存在。グローバル共有は不可 | マルチファイルプロジェクトでは各ファイルに Guidelines を設定する必要がある |
| **GitHub main only** | GitHub Push は main ブランチのみ。ブランチ作成・選択は不可 | PR ワークフローとの統合に制約。手動でブランチ管理が必要 |
| **Prompt length** | 実効的な文字数制限あり（~500文字程度で UX 設計の文脈を十分に伝えられない場合がある） | TC-EBC フレームワークで構造化し、最重要情報を優先 |

---

## Credit System

| Plan | Monthly Credits (Full Seat) | Monthly Credits (Other) | Daily Cap |
|------|---------------------------|------------------------|-----------|
| Starter | 500 | 500 | 150/day |
| Professional | 3,000 | 500 | — |
| Organization | 3,500 | 500 | — |
| Enterprise | 4,250 | 500 | — |

**Key facts:**
- Credits reset monthly, no carry-over
- ~25-45 credits per Make prompt (detailed ≈ vague in cost)
- Add-on: +5,000 credits = $120 / +7,500 = $180 / +10,000 = $240
- Vague prompts waste 3-4x credits via follow-up iterations
- **Optimization rule:** front-load detail in prompts to minimize iterations

### Credit-Aware Prompt Strategy

| Tier | Prompts | Est. Credits | Budget Check |
|------|---------|-------------|-------------|
| Simple (1-3 screens) | 1-3 | 25-135 | Any plan OK |
| Medium (4-7 screens) | 5-10 | 125-450 | Professional+ |
| Complex (8-15 screens) | 12-25 | 300-1,125 | Organization+ |
| Large (15+ screens) | 25+ | 625+ | Enterprise or add-on |

---

## New Capabilities (Schema 2025+)

| Feature | Status | Impact on Loom |
|---------|--------|---------------|
| **Make Kits** | Early Access | Import Figma Design libraries into Make. When available, Guidelines can reference kit components instead of re-documenting them |
| **DS Packages** | Available | Import NPM design system packages for production-quality React generation. Reduces what Guidelines must manually document |
| **Check Designs** | Early Access | AI linter detecting hardcoded values and suggesting correct variables. Complements Loom's VALIDATE phase |
| **Extended Collections** | Enterprise | Multi-brand design systems with inheritance. Affects token hierarchy in Guidelines |
| **Variable Modes** | Available | Professional: 10 modes/collection, Organization: 20 modes. Enables richer Light/Dark/Brand theming |

### When DS Package Is Available

If the project has a published design system package:
1. Guidelines.md references package components by name instead of re-specifying structure
2. Focus Guidelines on composition rules, layout conventions, and prohibitions
3. Token documentation can be lighter (package provides the source of truth)

---

## Auto Layout Constraints

| Constraint | Detail | Workaround |
|-----------|--------|------------|
| **Nesting depth** | 4+ levels of nested Auto Layout may not resolve correctly | Limit to 3 levels. Split deep structures into separate generation steps |
| **Mixed direction** | H/V direction mixing in same frame is unstable | Separate frames per direction, explicit `direction: HORIZONTAL` / `VERTICAL` |
| **Space between** | `Space between` mode calculations unreliable | Use explicit `gap` values, avoid `Space between` |
| **Absolute position** | Absolute positioning inside AL may be ignored | Separate absolute elements into own layer, or specify position explicitly in prompt |
| **Padding asymmetry** | Individual padding per side may collapse to uniform | Write `padding: 16 24 16 24` (4 explicit values) |

---

## Token & Variable Reference

| Constraint | Detail | Workaround |
|-----------|--------|------------|
| **Variable name resolution** | Variable names may not map accurately | Use full path: `Primitives/color/primary/500` |
| **Alias chain** | Variable alias chains may break | Include both primitive value and alias in Guidelines |
| **Mode switching** | Light/Dark mode switching incomplete | Include mode-specific value table, declare default mode |
| **Numeric tokens** | Spacing/sizing tokens ignored for hardcoded values | Add actual value in parentheses: `space-4 (= 16px)` |

---

## Component Generation

| Constraint | Detail | Workaround |
|-----------|--------|------------|
| **Variant limit** | 5+ variants degrade quality | Generate 3-4 variants at a time, merge into component set |
| **Boolean property** | Boolean props may not set correctly | List explicitly: `hasIcon: true/false` |
| **Instance swap** | Instance swap slots not configured | List candidate component names explicitly |
| **Default variant** | Default selection may differ from intent | Write `Default variant: size=medium, style=primary` |
| **Nested components** | Child component props may flatten | Generate children first, reference in parent |

---

## Layout & Responsive

| Constraint | Detail | Workaround |
|-----------|--------|------------|
| **Min/Max width** | Auto-setting unreliable | Explicit px values: `min-width: 320px, max-width: 1440px` |
| **Breakpoint behavior** | Responsive layout changes are difficult | Generate desktop first, mobile as separate prompt |
| **Fill container** | May be ignored | Add clarification: `width: Fill container (100% of parent)` |
| **Fixed vs Hug** | Distinction may blur | Annotate each element: `sizing: Fixed(200px)` or `sizing: Hug` |

---

## Naming & Structure

| Constraint | Detail | Workaround |
|-----------|--------|------------|
| **Layer naming** | Default names (`Frame 1`, `Rectangle 2`) generated | Include naming rules with examples in Guidelines |
| **Page structure** | Multi-page ignored, collapsed to single page | Generate 1 page per prompt |
| **Group vs Frame** | Frame may become Group | State "Use Frame, not Group" in Guidelines |

---

## Known Quirks

| Quirk | Mitigation |
|-------|------------|
| Shadow spread/blur slightly off | Specify full values: `x: 0, y: 4, blur: 12, spread: 0, color: rgba(0,0,0,0.1)` |
| Large border-radius not applied | Combine px value + natural language: `border-radius: 12px (rounded corners)` |
| Text truncation not set | Specify `text-overflow: ellipsis, max-lines: 2` |
| Icon sizing differs from intent | Include dimensions + constraint: `24x24px, constraints: Scale` |
| Color opacity inaccurate | Use rgba format, avoid hex + separate opacity |
| Output design diversity low | Generated designs tend toward similar patterns — request specific differentiation |

---

## Prompt Complexity vs Reliability

| Screen Count | Reliability | Strategy |
|-------------|-------------|----------|
| **1 screen** | High (90%+) | Single prompt with full detail |
| **2-3 screens** | Good (80%+) | Sequential prompts, shared Guidelines |
| **4-7 screens** | Moderate (65%+) | Component-first → Assembly |
| **8-15 screens** | Variable (50-70%) | System → Pattern → Screen → Polish |
| **15+ screens** | Low (<50%) | Module decomposition, ask first |

> **Key insight:** Quality improves inversely with prompt scope. Fewer, more specific prompts yield better results.

---

## Constraint-Aware Checklist

When writing Guidelines or prompts, verify:

- [ ] React-only limitation is understood (non-React projects: design output only)
- [ ] Credit budget is sufficient for planned prompt count
- [ ] Auto Layout nesting is 3 levels or fewer
- [ ] Variable names use full paths
- [ ] Components have 4 or fewer variants per generation step
- [ ] Min/Max width uses explicit px values
- [ ] Layer naming rules include examples
- [ ] 1 prompt targets 1-2 screens maximum
- [ ] Fixed / Hug / Fill sizing modes are annotated
- [ ] Shadow / border-radius use concrete numeric values
- [ ] Light/Dark mode Variable tables are included
- [ ] "Use Frame, not Group" is stated
- [ ] DS package availability is checked (reduces manual documentation)
