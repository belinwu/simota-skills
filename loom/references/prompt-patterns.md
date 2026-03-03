# Figma Make Prompt Patterns

Figma Make プロンプトの効果的パターン、分割戦略、Before/After 例、アンチパターン集。

---

## Core Principles

1. **Atomic Decomposition** — 1プロンプト1責務。ページ全体を一度に生成しない
2. **Progressive Detail** — 粗→細の段階的詳細化。骨格→レイアウト→スタイル→インタラクション
3. **Token Reference** — Guidelines.md で定義したトークン名を明示的に参照する
4. **Constraint Specification** — Auto Layout 制約、Min/Max サイズ、レスポンシブ挙動を明示
5. **Anti-Pattern Avoidance** — 曖昧な形容詞、暗黙の前提、過度な一括指示を避ける

---

## Prompt Complexity Tiers

### Tier 1: Simple (1-3 screens)

Single-pass with Guidelines 参照。

```
Strategy: 1 prompt per screen/component
Prompt count: 1-3
Guidelines dependency: Reference tokens + 1-2 component patterns
```

**Example:**
```
Create a login form with:
- Email input field (label: "メールアドレス", placeholder: "name@example.com")
- Password input field (label: "パスワード", type: password)
- Primary button "ログイン" (full width, size: Large)
- Link "パスワードをお忘れの方" below button (body-sm, text-secondary)
- Card container with shadow-md, radius-md, padding space-8
- All elements use Auto Layout vertical, gap space-4
```

### Tier 2: Medium (4-7 screens)

Component-first → Assembly パターン。

```
Strategy:
  Phase 1: Generate shared components (2-4 prompts)
  Phase 2: Assemble screens using components (2-6 prompts)
Prompt count: 5-10
Guidelines dependency: Full token set + component catalog
```

**Prompt sequence example:**
```
Prompt 1: Create reusable NavHeader component
Prompt 2: Create reusable SidebarNav component
Prompt 3: Create reusable DataTable component
Prompt 4: Assemble Dashboard screen using NavHeader + SidebarNav + MetricCards
Prompt 5: Assemble List screen using NavHeader + SidebarNav + DataTable
Prompt 6: Assemble Detail screen using NavHeader + SidebarNav + DetailPanel
```

### Tier 3: Complex (8-15 screens)

System → Pattern → Screen → Polish の4段階。

```
Strategy:
  Phase 1: Design system foundations (2-3 prompts)
  Phase 2: Pattern library (3-5 prompts)
  Phase 3: Screen assembly (4-8 prompts)
  Phase 4: Polish & states (2-4 prompts)
Prompt count: 12-25
Guidelines dependency: Comprehensive Guidelines.md required
```

### Tier 4: Large (15+ screens)

Module 分割 → 段階統合。**Ask first** (要ユーザー確認)。

```
Strategy:
  Phase 1: Module decomposition (define 3-5 feature modules)
  Phase 2: Per-module component generation
  Phase 3: Per-module screen assembly
  Phase 4: Cross-module integration screens
  Phase 5: Global polish
Prompt count: 25+
Guidelines dependency: Versioned Guidelines + module-specific supplements
```

---

## Effective Prompt Patterns

### Pattern 1: Structure-First

骨格を先に定義し、詳細を後で追加。

```
# Step 1: Structure
Create a product listing page layout:
- Header: full width, height 64px, fixed top
- Sidebar: left, width 240px, full height below header
- Main content: fills remaining space, padding space-6
- Footer: full width, below main content

All containers use Auto Layout. Main content scrollable.

# Step 2: Populate (subsequent prompt)
In the main content area of the product listing page:
- Filter bar: horizontal Auto Layout, gap space-3, items: category dropdown, price range, sort select, "Clear" ghost button
- Product grid: 4 columns, gap space-4, responsive to 2 columns on smaller width
- Each grid cell: ProductCard component
- Pagination: centered below grid, space-8 top margin
```

### Pattern 2: Component Definition

コンポーネントを独立して定義。

```
Create a component called "MetricCard" with these specifications:

Structure:
- Container: 280px width, Auto Layout vertical, padding space-6, radius-md, shadow-sm, bg-primary
- Row 1: icon (24px, accent-primary) + label (body-sm, text-secondary), horizontal Auto Layout, gap space-2
- Row 2: value (heading-2, text-primary), left aligned
- Row 3: trend indicator — icon (16px) + percentage (body-sm), colored green for positive, red for negative
- Optional Row 4: sparkline chart, height 40px, full width

Variants:
- trend: "up" | "down" | "neutral"
- hasSparkline: true | false

Auto Layout:
- Container gap: space-3
- Width: Fill container when placed in grid
- Min width: 200px
```

### Pattern 3: State Specification

状態ごとの見た目を明示。

```
Create a form input field with all states:

Base structure:
- Label: body-sm, text-primary, margin-bottom space-1
- Input container: height 40px, border 1px border-default, radius-sm, padding-x space-3
- Helper text: body-sm, text-secondary, margin-top space-1

States:
- Default: border-default, bg-primary
- Hover: border-default darker by 10%
- Focus: border accent-primary 2px, shadow-sm with accent-primary 20% opacity
- Error: border status-error, helper text changes to status-error color, error icon appears
- Disabled: bg-secondary, text-secondary 50% opacity, cursor not-allowed
- Filled: same as default, text-primary value displayed

Create each state as a separate frame in a row for reference.
```

### Pattern 4: Responsive Specification

レスポンシブ挙動を明確に指示。

```
Create a pricing section that is responsive:

Desktop (>1024px):
- 3 pricing cards in a row, equal width, gap space-6
- Cards: Auto Layout vertical, padding space-8
- Featured card: slightly larger (scale 1.05), shadow-lg, accent border top 4px

Tablet (768-1024px):
- 3 cards in a row, reduced padding space-6
- Featured card: same height, no scale

Mobile (<768px):
- Cards stack vertically, full width, gap space-4
- Featured card first in stack order
- Reduced padding space-4

Use Auto Layout with Min/Max width constraints for fluid behavior.
```

### Pattern 5: Reference by Example

既存画面を参照して類似を生成。

```
Create a user settings page following the same layout pattern as the Dashboard page:
- Same NavHeader and SidebarNav components
- Main content area: vertical sections with heading-3 section titles
- Sections: Profile, Notifications, Security, Billing
- Each section: card with form fields, save button bottom-right
- Section divider: 1px border-default, margin-y space-8

Match spacing, typography, and color usage from Guidelines.md.
```

---

## Before / After Examples

### Example 1: Vague → Precise

**Before (Bad):**
```
Create a nice dashboard with some charts and a sidebar
```

**After (Good):**
```
Create a dashboard page with:
- Left sidebar: 240px width, bg-secondary, vertical Auto Layout
  - Logo area: height 64px, centered
  - Nav items: icon (20px) + label (body-md), padding-y space-2, padding-x space-4
  - Active item: bg-primary, accent-primary left border 3px
- Top bar: height 56px, bg-primary, shadow-sm
  - Search input: width 320px, left aligned
  - Notification bell icon + avatar (32px circle), right aligned, gap space-4
- Main content: padding space-6
  - Row 1: 4 MetricCards in horizontal Auto Layout, gap space-4, Fill container
  - Row 2: 2 chart containers (60%/40% split), height 320px, radius-md, shadow-sm
  - Row 3: DataTable component, full width
```

### Example 2: Ambiguous States → Explicit States

**Before (Bad):**
```
Create a button component with different styles
```

**After (Good):**
```
Create a Button component with these exact variants:

Property "variant": Primary | Secondary | Ghost | Danger
Property "size": Small (32px) | Medium (40px) | Large (48px)
Property "state": Default | Hover | Active | Disabled | Loading
Property "hasIcon": true | false

Primary/Default: bg accent-primary, text white, radius-sm
Primary/Hover: bg accent-primary darkened 10%
Primary/Active: bg accent-primary darkened 20%
Primary/Disabled: bg accent-primary 40% opacity
Primary/Loading: spinner icon replaces text, same bg

Generate the full variant matrix as a component set.
```

### Example 3: Missing Constraints → Explicit Constraints

**Before (Bad):**
```
Create a card grid layout
```

**After (Good):**
```
Create a responsive card grid:
- Grid container: Auto Layout, wrap, gap space-4
- Cards: min-width 280px, max-width 360px
- Desktop: 3 columns (cards Fill container equally)
- Tablet: 2 columns
- Mobile: 1 column (full width)
- Card height: Hug contents (not fixed)
- Card: Auto Layout vertical, padding space-6, radius-md, shadow-sm
- Last row alignment: left-aligned (not stretched)
```

---

## Anti-Patterns

### 1. Kitchen Sink Prompt

**Problem:** 1つのプロンプトに全てを詰め込む

```
# DON'T
Create a complete e-commerce website with header, product grid,
filters, cart, checkout, user profile, order history, and admin panel.
All pages should be responsive and use our design system.
```

**Fix:** Tier 3/4 の段階的分割戦略を使用。

### 2. Vague Adjectives

**Problem:** 主観的で測定不能な記述

```
# DON'T
Make it look modern and clean with a nice color scheme
```

**Fix:** 具体的なトークン・値・制約で記述。

```
# DO
Use bg-primary background, space-8 padding, shadow-sm for cards,
heading-2 for titles, body-md for content, accent-primary for CTAs
```

### 3. Implicit Assumptions

**Problem:** 暗黙の前提を記述しない

```
# DON'T
Add a navigation menu
```

**Fix:** 位置、構造、動作を明示。

```
# DO
Add a horizontal navigation bar:
- Position: top, full width, height 64px, sticky
- Logo: left aligned, 32px height
- Nav links: center aligned, gap space-6, body-md, text-primary
- Active link: accent-primary color, bottom border 2px
- CTA button: right aligned, Primary/Small
- Mobile: hamburger menu icon, slide-out drawer
```

### 4. Missing Auto Layout

**Problem:** Auto Layout の使用を明示しない

```
# DON'T
Place the title at the top and buttons at the bottom of the card
```

**Fix:** Auto Layout の direction, gap, alignment, resizing を指定。

```
# DO
Card uses Auto Layout vertical:
- Gap: space-4
- Padding: space-6
- Children alignment: stretch (full width)
- Title: heading-4, top of stack
- Content: body-md, middle, Hug contents height
- Button group: horizontal Auto Layout, gap space-2, bottom of stack, right-aligned
```

### 5. Ignoring States

**Problem:** デフォルト状態のみを記述

```
# DON'T
Create a text input field
```

**Fix:** Pattern 3 (State Specification) を使用。全状態を明示。

---

## Prompt Quality Checklist

プロンプト作成後に確認：

- [ ] 具体的な数値（サイズ、余白、色）がトークン名で指定されている
- [ ] Auto Layout の direction, gap, padding, resizing が明示されている
- [ ] コンポーネントの全 variants が列挙されている
- [ ] インタラクション状態（hover, focus, disabled 等）が含まれている
- [ ] レスポンシブ挙動が breakpoint ごとに指定されている
- [ ] 命名規約に従った layer/component 名が指定されている
- [ ] 1プロンプトの責務が明確で、複数責務が混在していない
- [ ] Guidelines.md のトークン・ルールと矛盾がない

---

## Prompt Sequencing Strategy

### Dependency Graph

プロンプト間の依存関係を事前に設計：

```
[Shared Components] ──→ [Screen Assembly] ──→ [States & Polish]
       ↑                       ↑                      ↑
  Independent            Depends on            Depends on
  (parallel OK)          components             screens
```

### Ordering Rules

1. **Foundation first** — トークン定義・基本コンポーネントが最初
2. **Shared before unique** — 複数画面で使うコンポーネントを先に生成
3. **Layout before content** — ページ骨格の後にコンテンツを埋める
4. **Default before variants** — デフォルト状態の後にバリアントを追加
5. **Desktop before responsive** — デスクトップレイアウト確定後にレスポンシブ対応

### Naming in Sequences

プロンプト内でのコンポーネント参照には一貫した名前を使用：

```
Prompt 1: "Create a component called 'NavHeader'..."
Prompt 3: "Using the 'NavHeader' component from earlier..."
```
