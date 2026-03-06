# Figma Make Prompt Patterns

Figma Make プロンプトの効果的パターン、分割戦略、Before/After 例、アンチパターン集。

---

## Core Principles

1. **Atomic Decomposition** — 1プロンプト1責務。ページ全体を一度に生成しない
2. **Progressive Detail** — 粗→細の段階的詳細化。骨格→レイアウト→スタイル→インタラクション
3. **Token Reference** — Guidelines.md で定義したトークン名を明示的に参照する
4. **Constraint Specification** — Auto Layout 制約、Min/Max サイズ、レスポンシブ挙動を明示
5. **Anti-Pattern Avoidance** — 曖昧な形容詞、暗黙の前提、過度な一括指示を避ける
6. **Cost Awareness** — 詳細プロンプトと曖昧プロンプトのクレジット消費はほぼ同じ（~25-45 credits）。曖昧なプロンプトは 3-4 回のフォローアップを生み、各回がクレジットを消費するため、最初から詳細に書く方が経済的

---

## TC-EBC Framework (Figma Official)

Figma 公式ブログ「Cooking with Constraints」で推奨されるプロンプト構造化フレームワーク。**PRIME フェーズのプロンプト設計における標準テンプレートとして使用する。**

| Element | Role | Example |
|---------|------|---------|
| **T**ask | 何を作るか | "Create a dashboard page" |
| **C**ontext | 背景情報 | "For a SaaS analytics tool targeting enterprise users" |
| **E**lements | UIの構成要素 | "Line chart, KPI cards, filter bar, data table" |
| **B**ehavior | インタラクション | "Chart click opens detail modal; filters apply instantly" |
| **C**onstraints | 制約条件 | "Mobile-first, dark mode support, WCAG AA contrast" |

### TC-EBC Template

```
[Task] Create a [component/screen] for [purpose].

[Context] This is part of [project type] targeting [user persona].
The design follows [Design System Name] conventions.

[Elements]
- [Element 1]: [specification]
- [Element 2]: [specification]
- [Element 3]: [specification]

[Behavior]
- [Interaction 1]: [trigger → result]
- [Interaction 2]: [trigger → result]

[Constraints]
- Layout: Auto Layout [direction], gap [token], padding [token]
- Tokens: Use [token names] from Guidelines
- Responsive: [breakpoint behavior]
- Accessibility: [specific a11y requirements]
```

---

## Prompt Complexity Tiers

### Tier 1: Simple (1-3 screens)

Single-pass with Guidelines 参照。

```
Strategy: 1 prompt per screen/component
Prompt count: 1-3
Guidelines dependency: Reference tokens + 1-2 component patterns
Credit cost: ~25-135 credits
```

**Example:**
```
[Task] Create a login form.
[Context] SaaS application using our design system.
[Elements]
- Email input (label: "メールアドレス", placeholder: "name@example.com")
- Password input (label: "パスワード", type: password)
- Primary button "ログイン" (full width, size: Large)
- Link "パスワードをお忘れの方" (body-sm, text-secondary)
- Card container (shadow-md, radius-md, padding space-8)
[Constraints]
- Auto Layout vertical, gap space-4
- All spacing uses tokens from Guidelines
```

### Tier 2: Medium (4-7 screens)

Component-first → Assembly パターン。

```
Strategy:
  Phase 1: Generate shared components (2-4 prompts)
  Phase 2: Assemble screens using components (2-6 prompts)
Prompt count: 5-10
Guidelines dependency: Full token set + component catalog
Credit cost: ~125-450 credits
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
Guidelines dependency: Comprehensive multi-file Guidelines required
Credit cost: ~300-1,125 credits
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
Credit cost: 625+ credits — verify user's plan has sufficient budget
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
- Filter bar: horizontal Auto Layout, gap space-3
- Product grid: 4 columns, gap space-4
- Pagination: centered below grid, space-8 top margin
```

### Pattern 2: Component Definition

コンポーネントを独立して定義。

```
Create a component called "MetricCard" with these specifications:

Structure:
- Container: 280px width, Auto Layout vertical, padding space-6, radius-md, shadow-sm, bg-primary
- Row 1: icon (24px, accent-primary) + label (body-sm, text-secondary), horizontal, gap space-2
- Row 2: value (heading-2, text-primary), left aligned
- Row 3: trend icon (16px) + percentage (body-sm), green positive / red negative

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
- Error: border status-error, helper text status-error, error icon appears
- Disabled: bg-secondary, text-secondary 50% opacity
- Filled: same as default, text-primary value displayed

Create each state as a separate frame in a row for reference.
```

### Pattern 4: Responsive Specification

レスポンシブ挙動を明確に指示。

```
Create a pricing section that is responsive:

Desktop (>1024px):
- 3 pricing cards in a row, equal width, gap space-6
- Featured card: scale 1.05, shadow-lg, accent border top 4px

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
- Main content area: vertical sections with heading-3 titles
- Sections: Profile, Notifications, Security, Billing
- Each section: card with form fields, save button bottom-right

Match spacing, typography, and color usage from Guidelines.
```

### Pattern 6: Checkpoint Prompt

生成前に理解度を確認し、ハルシネーションを防止。

```
Before generating, tell me your understanding of:
1. Which components from the Guidelines you will use
2. The Auto Layout structure you plan to apply
3. Which tokens you will reference

Do NOT generate the design yet. Just confirm your approach.
```

### Pattern 7: Scenario-Based Framing

AIに特定の役割を与えて文脈を強化。

```
Imagine you are designing for a healthcare app used by elderly patients (65+).
The UI must prioritize:
- Large touch targets (minimum 48x48px)
- High contrast text (7:1 ratio)
- Simple, linear navigation flow

Create a medication reminder screen with:
[Elements and constraints follow...]
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
[Task] Create a dashboard page.
[Context] SaaS analytics tool for marketing teams.
[Elements]
- Left sidebar: 240px, bg-secondary, vertical Auto Layout
  - Logo: height 64px, centered
  - Nav items: icon (20px) + label (body-md), padding-y space-2, padding-x space-4
  - Active item: bg-primary, accent-primary left border 3px
- Top bar: height 56px, bg-primary, shadow-sm
  - Search: width 320px, left
  - Avatar (32px circle) + bell icon, right, gap space-4
- Main: padding space-6
  - Row 1: 4 MetricCards, horizontal, gap space-4, Fill container
  - Row 2: 2 chart containers (60%/40%), height 320px, radius-md, shadow-sm
  - Row 3: DataTable, full width
[Constraints] All spacing uses Guidelines tokens. Auto Layout throughout.
```

### Example 2: Missing States → Explicit States

**Before (Bad):**
```
Create a button component with different styles
```

**After (Good):**
```
Create a Button component:

Property "variant": Primary | Secondary | Ghost | Danger
Property "size": Small (32px) | Medium (40px) | Large (48px)
Property "state": Default | Hover | Active | Disabled | Loading
Property "hasIcon": true | false

Primary/Default: bg accent-primary, text white, radius-sm
Primary/Hover: bg accent-primary darkened 10%
Primary/Disabled: bg accent-primary 40% opacity
Primary/Loading: spinner icon replaces text, same bg

Generate the full variant matrix as a component set.
```

---

## Anti-Patterns

### 1. Kitchen Sink Prompt

**Problem:** 1つのプロンプトに全てを詰め込む

```
# DON'T
Create a complete e-commerce website with header, product grid,
filters, cart, checkout, user profile, and admin panel.
```

**Fix:** Tier 3/4 の段階的分割戦略を使用。

### 2. Vague Adjectives

**Problem:** 主観的で測定不能な記述

```
# DON'T
Make it look modern and clean with a nice color scheme

# DO
Use bg-primary background, space-8 padding, shadow-sm for cards,
heading-2 for titles, body-md for content, accent-primary for CTAs
```

### 3. Implicit Assumptions

**Problem:** 暗黙の前提を記述しない

```
# DON'T
Add a navigation menu

# DO
Add a horizontal navigation bar:
- Position: top, full width, height 64px, sticky
- Logo: left, 32px height
- Nav links: center, gap space-6, body-md, text-primary
- Active link: accent-primary, bottom border 2px
- CTA: right, Primary/Small button
- Mobile: hamburger icon, slide-out drawer
```

### 4. Missing Auto Layout

**Problem:** Auto Layout の使用を明示しない

```
# DON'T
Place the title at the top and buttons at the bottom

# DO
Card: Auto Layout vertical, gap space-4, padding space-6
- Children alignment: stretch (full width)
- Title: heading-4, top of stack
- Content: body-md, Hug contents height
- Button group: horizontal, gap space-2, right-aligned
```

### 5. Context Overload

**Problem:** 過剰な詳細でLLMを混乱させる

```
# DON'T
[20+ rules, edge cases, exceptions, and conditional logic in a single prompt]

# DO
Focus on the 5-7 most critical rules. Move edge cases to component sub-files.
Reference Guidelines files instead of repeating their content.
```

---

## Prompt Sequencing Strategy

### Dependency Graph

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

### Prompt Quality Checklist

- [ ] TC-EBC 構造に従っている（Task/Context/Elements/Behavior/Constraints）
- [ ] 具体的な数値がトークン名で指定されている
- [ ] Auto Layout の direction, gap, padding, resizing が明示されている
- [ ] コンポーネントの全 variants が列挙されている
- [ ] インタラクション状態（hover, focus, disabled 等）が含まれている
- [ ] 1プロンプトの責務が明確で、複数責務が混在していない
- [ ] Guidelines のトークン・ルールと矛盾がない
- [ ] クレジット消費がユーザーの予算内に収まる見通しがある
