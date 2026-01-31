# Forge Builder Integration

Required output formats for handing off prototypes to Builder.

---

## Required Output Structure

```
components/prototypes/
├── Feature.tsx          # UI実装（必須）
├── types.ts             # 型定義（必須）← Builder が Value Object に変換
├── Feature.test.tsx     # 簡易テスト（オプション）
└── README.md            # 使用方法（オプション）

mocks/
├── handlers.ts          # MSW ハンドラ（必須）← Builder が API Client に変換
└── errors.ts            # エラーケース（必須）← Builder が DomainError に変換

.agents/
└── forge-insights.md    # ドメイン知識（必須）← Builder がビジネスルールとして参照
```

---

## types.ts Template

```typescript
// types.ts - Builder が Value Object / Entity に変換する元データ

// Entity候補（IDを持つもの）
export interface User {
  id: string;           // → UserId Value Object
  email: string;        // → Email Value Object
  name: string;         // → UserName Value Object
  role: 'admin' | 'user' | 'guest';  // → UserRole Enum
  createdAt: string;    // → ISO date
}

// Value Object候補（IDを持たないもの）
export interface Address {
  street: string;
  city: string;
  postalCode: string;   // → 検証ルールが必要
  country: string;
}

// API Request/Response 型
export interface CreateUserRequest {
  email: string;
  name: string;
  password: string;     // → 検証ルールが必要（8文字以上など）
}

export interface CreateUserResponse {
  user: User;
  token: string;
}

// エラーレスポンス型
export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, string>;
}
```

---

## errors.ts Template

```typescript
// mocks/errors.ts - Builder が DomainError に変換する元データ

import { http, HttpResponse } from 'msw';

export const errorHandlers = [
  // バリデーションエラー
  http.post('/api/users', async ({ request }) => {
    const body = await request.json() as { email?: string; name?: string };

    if (!body.email) {
      return HttpResponse.json(
        { code: 'EMAIL_REQUIRED', message: 'メールアドレスは必須です' },
        { status: 400 }
      );
    }

    if (!body.email.includes('@')) {
      return HttpResponse.json(
        { code: 'INVALID_EMAIL', message: 'メールアドレスの形式が無効です' },
        { status: 400 }
      );
    }

    if (!body.name || body.name.length < 1) {
      return HttpResponse.json(
        { code: 'NAME_REQUIRED', message: '名前は必須です' },
        { status: 400 }
      );
    }

    return HttpResponse.json({ id: '1', ...body }, { status: 201 });
  }),

  // 認証エラー
  http.get('/api/protected', ({ request }) => {
    const token = request.headers.get('Authorization');
    if (!token) {
      return HttpResponse.json(
        { code: 'UNAUTHORIZED', message: '認証が必要です' },
        { status: 401 }
      );
    }
    return HttpResponse.json({ data: 'secret' });
  }),

  // 権限エラー
  http.delete('/api/admin/:id', () => {
    return HttpResponse.json(
      { code: 'FORBIDDEN', message: '権限がありません' },
      { status: 403 }
    );
  }),

  // 存在しないリソース
  http.get('/api/users/:id', ({ params }) => {
    if (params.id === '999') {
      return HttpResponse.json(
        { code: 'USER_NOT_FOUND', message: 'ユーザーが見つかりません' },
        { status: 404 }
      );
    }
    return HttpResponse.json({ id: params.id, name: 'Test' });
  }),

  // 競合エラー
  http.post('/api/users', async ({ request }) => {
    const body = await request.json() as { email: string };
    if (body.email === 'existing@example.com') {
      return HttpResponse.json(
        { code: 'EMAIL_ALREADY_EXISTS', message: 'このメールアドレスは既に使用されています' },
        { status: 409 }
      );
    }
    return HttpResponse.json({ id: '1', ...body }, { status: 201 });
  }),
];
```

---

## forge-insights.md Template

```markdown
# Forge Insights: [機能名]

## 発見したビジネスルール

### 検証済みルール
- [ ] ユーザーのメールアドレスは一意でなければならない
- [ ] パスワードは8文字以上で、大文字・小文字・数字を含む必要がある
- [ ] 管理者のみがユーザーを削除できる

### 推測したルール（Builder に確認を依頼）
- [ ] メールアドレス変更後24時間は再変更不可？
- [ ] 削除されたユーザーのデータは論理削除？物理削除？

## UI/UXで確認した挙動

### 成功パターン
- フォーム送信 → ローディング表示 → 成功メッセージ → リダイレクト

### エラーパターン
- バリデーションエラー → フィールド下にエラー表示
- サーバーエラー → トースト通知 + リトライボタン
- ネットワークエラー → オフライン表示

## パフォーマンス観点
- リストは50件程度でテスト済み
- 1000件以上の場合は仮想化が必要かも
- 画像アップロードは5MB制限をUIで設定

## 未解決の疑問
1. セッション有効期限は？
2. 同時編集時の競合処理は？
3. 削除確認ダイアログは必要？
```

---

## Builder Handoff Template

```markdown
## BUILDER_HANDOFF

### Prototype Info
- Location: `components/prototypes/[name].tsx`
- Types: `components/prototypes/types.ts`
- Mocks: `mocks/handlers.ts` + `mocks/errors.ts`
- Insights: `.agents/forge-insights.md`

### Validated Features
- [x] Feature 1: 基本機能実装済み
- [x] Feature 2: ユーザーフロー確認済み

### For Builder to Implement
- [ ] types.ts → Value Object / Entity に変換
- [ ] handlers.ts → API Client に変換
- [ ] errors.ts → DomainError に変換
- [ ] forge-insights.md → ビジネスルールとして実装

### Quick Reference
- API Base: `/api/v1`
- Auth: Bearer token in header
- Error format: `{ code: string, message: string }`
```

---

## Prototype-to-Production Checklist

### Code Quality
- [ ] Remove all `console.log` debugging
- [ ] Replace inline styles with proper CSS/styled-components
- [ ] Add proper TypeScript types (no `any`)
- [ ] Extract magic numbers to constants
- [ ] Remove TODO comments or create tickets

### Error Handling
- [ ] Add loading states
- [ ] Add error states with retry
- [ ] Handle edge cases (empty, null, undefined)
- [ ] Add form validation
- [ ] Implement error boundaries

### API Integration
- [ ] Replace mock data with API calls
- [ ] Add request/response types
- [ ] Handle API errors gracefully
- [ ] Add request caching if needed
- [ ] Implement optimistic updates if needed

### Testing
- [ ] Add unit tests for logic
- [ ] Add component tests
- [ ] Test error scenarios
- [ ] Test loading states

### Accessibility
- [ ] Add proper ARIA labels
- [ ] Ensure keyboard navigation
- [ ] Check color contrast
- [ ] Test with screen reader
