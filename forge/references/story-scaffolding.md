# Story Scaffolding Reference

Forge がプロトタイプ作成時にオプションで生成するプレビューストーリーの詳細。

---

## When to Generate Stories

| Scenario | Generate Story? |
|----------|-----------------|
| UI component prototype | ✅ Recommended |
| Backend PoC | ❌ Skip |
| Complex multi-component page | ⚠️ Main component only |
| API mock demonstration | ❌ Skip |

---

## Preview Story Template (Storybook)

Forge が生成するのは**最小限のプレビューストーリー**のみ。フルカバレッジは Showcase が担当。

```typescript
// ComponentName.stories.tsx (Forge generated - minimal preview)
import type { Meta, StoryObj } from '@storybook/react';
import { ComponentName } from './ComponentName';

const meta = {
  component: ComponentName,
  title: 'Prototypes/ComponentName', // Prototypes配下に配置
  tags: ['prototype'], // プロトタイプタグ
  parameters: {
    docs: {
      description: {
        component: '⚠️ Prototype - Full stories pending from Showcase',
      },
    },
  },
} satisfies Meta<typeof ComponentName>;

export default meta;
type Story = StoryObj<typeof meta>;

// Forgeはデフォルト状態のみ
export const Preview: Story = {
  args: {
    // デフォルトprops
  },
};

// TODO(showcase): Add variants (sizes, states, themes)
// TODO(showcase): Add interaction tests
// TODO(showcase): Add a11y configuration
```

---

## React Cosmos Fixture Template

React Cosmos を使用するプロジェクト向けの fixture 生成。

```typescript
// ComponentName.fixture.tsx (Forge generated - minimal)
import { ComponentName } from './ComponentName';

export default {
  // Default fixture
  default: <ComponentName />,

  // With props
  withProps: (
    <ComponentName
      variant="primary"
      // デフォルトpropsのみ
    />
  ),
};

// TODO(showcase): Add comprehensive fixtures
// TODO(showcase): Add decorators for theme/context
```

---

## Story Output Structure

プロトタイプ作成時の出力ファイル構成（ストーリー付き）：

```
feature/
├── ComponentName.tsx           # UI実装（必須）
├── ComponentName.stories.tsx   # プレビューストーリー（オプション）
├── ComponentName.fixture.tsx   # React Cosmos fixture（オプション）
├── types.ts                    # 型定義（必須）
├── handlers.ts                 # MSW ハンドラ（必須）
├── errors.ts                   # エラーケース（必須）
└── forge-insights.md           # ドメイン知識（必須）
```

---

## FORGE_TO_SHOWCASE Handoff

Forge がプレビューストーリーを作成した場合のハンドオフテンプレート：

```markdown
## FORGE_TO_SHOWCASE: Story Enhancement Request

### Prototype Info
- Component: `[path/to/ComponentName.tsx]`
- Preview Story: `[path/to/ComponentName.stories.tsx]`
- Fixture: `[path/to/ComponentName.fixture.tsx]` (if applicable)

### Current Coverage
- ✅ Default state preview
- ❌ Variants (sizes, colors, themes)
- ❌ State coverage (loading, error, disabled)
- ❌ Interaction tests
- ❌ A11y configuration
- ❌ MDX documentation

### Props to Cover
| Prop | Type | Values to Test |
|------|------|----------------|
| variant | string | primary, secondary, outline |
| size | string | sm, md, lg |
| disabled | boolean | true, false |

### Requested Enhancements
1. Move from `Prototypes/` to `Components/` hierarchy
2. Add all variant stories
3. Add interaction tests for: [click, hover, focus]
4. Configure a11y addon
5. Create MDX documentation

### Notes
[Any special considerations from prototyping]
```

---

## FORGE_TO_ARTISAN Handoff

```markdown
## ARTISAN_HANDOFF (from Forge)

### Prototype Summary
- **Components:** [List of prototyped components]
- **Tech stack:** [React/Vue + Tailwind/etc.]
- **Demo URL:** [Local dev URL if running]

### Production Requirements
- [ ] Replace mock data with real API calls
- [ ] Add proper error handling
- [ ] Implement responsive design edge cases
- [ ] Add loading/error states
- [ ] Write component tests

Suggested command: `/Artisan productionize [component]`
```

---

## Showcase Integration Flow

```
Forge: Prototype Creation
  Component (Required) + Preview Story (Optional) + Cosmos Fixture (Optional)
    ↓
Showcase: Story Enhancement
  Full variant coverage · Interaction tests · A11y · MDX docs · Visual regression
```

---

## Shared Tags Convention

| Tag | Meaning | Who Sets |
|-----|---------|----------|
| `prototype` | Forge-generated, not production-ready | Forge |
| `autodocs` | Auto-generate documentation | Showcase |
| `visual-test` | Include in visual regression | Showcase |
| `component` | Production component story | Showcase |

---

## ON_STORY_GENERATION Trigger

```yaml
questions:
  - question: "Should Forge generate preview stories with this prototype?"
    header: "Stories"
    options:
      - label: "Yes - Storybook (Recommended)"
        description: "Generate minimal Storybook story for immediate preview"
      - label: "Yes - React Cosmos"
        description: "Generate React Cosmos fixture"
      - label: "Yes - Both"
        description: "Generate both Storybook and React Cosmos"
      - label: "No - Skip"
        description: "Showcase will create stories from scratch"
    multiSelect: false
```
