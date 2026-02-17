# Skill Templates

Micro Skill and Full Skill template specifications, frontmatter conventions, and format validation rules.

---

## Frontmatter Specification (Required)

Every generated skill MUST include YAML frontmatter:

```yaml
---
name: skill-name          # kebab-case, unique within project
description: One-line description of what this skill does  # Japanese
---
```

**Rules:**
- `name` — kebab-case, 2-4 words, descriptive of action
- `description` — Single sentence, starts with verb or noun, in Japanese

---

## Micro Skill Template (10-80 lines)

**Use when:** Single task, clear steps, 0-2 decision points, simple template.

```markdown
---
name: [skill-name]
description: [日本語の一行説明]
---

# [スキルタイトル]

## 目的
[このスキルをいつ・なぜ使うかの簡潔な説明]

## 手順

1. [ステップ1]
2. [ステップ2]
3. [ステップ3]
...

## テンプレート

\```[lang]
[コードテンプレート - プロジェクトの規約に準拠]
\```

## 規約
- [規約1: 命名規則等]
- [規約2: ファイル配置等]
- [規約3: テストパターン等]
```

### Micro Skill Examples by Category

#### Workflow Skill (手順型)

```markdown
---
name: new-page
description: App Router規約に従って新しいページを作成
---

# New Page Generator

## 目的
Next.js App Routerの規約に従い、新しいページコンポーネントを作成する。

## 手順

1. `src/app/[route]/page.tsx` を作成
2. Server Component をデフォルトに
3. `metadata` export を含める
4. 共通 Layout を使用
5. `__tests__/[route].test.tsx` にテスト追加

## テンプレート

\```tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: '[PageTitle]',
  description: '[Description]',
}

export default function [PageName]Page() {
  return (
    <main>
      <h1>[PageTitle]</h1>
    </main>
  )
}
\```

## 規約
- コンポーネント名: PascalCase + `Page` suffix
- ディレクトリ名: kebab-case
- データ取得: Server Component内でfetch
- メタデータ: 各ページで必ずexport
```

#### Convention Skill (規約型)

```markdown
---
name: naming-rules
description: プロジェクトの命名規則一覧
---

# 命名規則

## ファイル命名
- コンポーネント: `PascalCase.tsx` (例: `UserProfile.tsx`)
- ユーティリティ: `camelCase.ts` (例: `formatDate.ts`)
- テスト: `[name].test.ts` (コロケーション)

## 変数・関数命名
- React hooks: `use` prefix (例: `useAuth`)
- イベントハンドラ: `handle` prefix (例: `handleSubmit`)
- Boolean: `is`/`has`/`should` prefix (例: `isLoading`)

## ディレクトリ命名
- 機能モジュール: kebab-case (例: `user-profile/`)
- 共通コンポーネント: `components/` 直下
```

---

## Full Skill Template (100-400 lines)

**Use when:** Multi-step process, 3+ decision points, significant domain knowledge, complex templates with variations.

```markdown
---
name: [skill-name]
description: [日本語の一行説明]
---

# [スキルタイトル]

## 目的
[詳細な説明 - いつ使うか、前提条件、期待される成果]

## 設計原則
[プロジェクト固有の設計判断]
- [原則1]
- [原則2]
- [原則3]

## ワークフロー

### Step 1: [フェーズ名]
[詳細な手順]

### Step 2: [フェーズ名]
[詳細な手順]

### Step 3: [フェーズ名]
[詳細な手順]

## テンプレート

### パターンA: [シンプルケース]

\```[lang]
[テンプレートコード]
\```

### パターンB: [複雑ケース]

\```[lang]
[テンプレートコード]
\```

## エラーハンドリング
[プロジェクト固有のエラー処理パターン]

## テスト規約
[テストパターン、モック戦略、カバレッジ要件]

## チェックリスト
- [ ] [確認項目1]
- [ ] [確認項目2]
- [ ] [確認項目3]
```

### Full Skill Example

```markdown
---
name: webhook-handler
description: Stripe Webhook署名検証・冪等性・エラーハンドリングを含むハンドラ作成
---

# Webhook Handler Generator

## 目的
Stripe Webhookイベントを安全に処理するハンドラを作成する。
署名検証、冪等性保証、適切なエラーハンドリングを含む。

## 設計原則
- 署名検証は最初に行う（検証前にボディをパースしない）
- 冪等性キーでイベント重複を防ぐ
- 非同期処理は200レスポンス後に実行
- エラーはstructured loggingで記録

## ワークフロー

### Step 1: エンドポイント作成
`src/app/api/webhooks/stripe/route.ts` を作成

### Step 2: 署名検証ミドルウェア実装
raw bodyで署名を検証

### Step 3: イベントハンドラ分岐
event.typeでハンドラをルーティング

### Step 4: 冪等性チェック
event.idをDBに記録し重複を防ぐ

## テンプレート

### メインハンドラ

\```typescript
import { headers } from 'next/headers'
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function POST(request: Request) {
  const body = await request.text()
  const signature = headers().get('stripe-signature')!

  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err) {
    console.error('Webhook signature verification failed:', err)
    return new Response('Invalid signature', { status: 400 })
  }

  // Idempotency check
  const processed = await isEventProcessed(event.id)
  if (processed) {
    return new Response('Already processed', { status: 200 })
  }

  try {
    await handleEvent(event)
    await markEventProcessed(event.id)
  } catch (err) {
    console.error('Webhook handler error:', err)
    return new Response('Handler error', { status: 500 })
  }

  return new Response('OK', { status: 200 })
}
\```

## テスト規約
- stripe-event-types パッケージでイベントをモック
- 署名検証のテスト（正常・不正）
- 冪等性テスト（重複イベント送信）
- 各イベントタイプのハンドラテスト

## チェックリスト
- [ ] STRIPE_WEBHOOK_SECRET が環境変数に設定済み
- [ ] raw body パース設定（bodyParser無効化）
- [ ] 冪等性チェック用テーブル作成
- [ ] エラーログのアラート設定
- [ ] ローカルテスト用 stripe listen 設定
```

---

## Format Validation Rules

### Required Elements

| Element | Micro | Full | Check |
|---------|-------|------|-------|
| YAML frontmatter | ✅ | ✅ | `---` block at start |
| `name` field | ✅ | ✅ | kebab-case, non-empty |
| `description` field | ✅ | ✅ | Non-empty string |
| H1 title | ✅ | ✅ | Single `#` heading |
| Purpose/目的 section | ✅ | ✅ | Explains when/why |
| Steps/手順 or Workflow | ✅ | ✅ | Actionable instructions |
| Template/テンプレート | Optional | ✅ | Code blocks with lang |
| Conventions/規約 | ✅ | Optional | Project-specific rules |
| Error handling | — | ✅ | Error patterns |
| Testing section | — | ✅ | Test conventions |

### File Naming

- **Directory-based structure** (required for Claude Code skill recognition):
  - `project/.claude/skills/[skill-name]/SKILL.md`
  - `project/.agents/skills/[skill-name]/SKILL.md`
- Full Skills with references (synced):
  - `project/.claude/skills/[skill-name]/SKILL.md` + `project/.claude/skills/[skill-name]/references/[topic].md`
  - `project/.agents/skills/[skill-name]/SKILL.md` + `project/.agents/skills/[skill-name]/references/[topic].md`
- Skill directory names: `kebab-case` (e.g., `new-page/`, `webhook-handler/`)
- Skill file: always `SKILL.md` inside the skill directory
- Reference files (Full Skills): `references/[topic].md` inside the skill directory

### Size Guidelines

| Type | Lines | Sections | Templates |
|------|-------|----------|-----------|
| Micro | 10-80 | 3-5 | 0-1 |
| Full | 100-400 | 6-10 | 2-5 |
