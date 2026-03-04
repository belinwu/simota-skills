# Server Components & App Router Patterns

> RSC Composition、Suspense Streaming、Server Actions、キャッシュ戦略、アンチパターン

## 1. RSC Composition: Server/Client 境界設計

### 原則: `'use client'` はリーフに押し下げる

```tsx
// Bad: 高レベルに 'use client' → 全子コンポーネントが Client Component 化
'use client';
export function Layout() {
  const [isOpen, setIsOpen] = useState(false);
  return <ServerHeavyComponent />; // サーバー実行の利点が消える
}

// Good: Composition パターンで Server Component を children として渡す
'use client';
export function InteractiveShell({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  return <div>{children}</div>;
}

// page.tsx (Server Component)
export default function Page() {
  return (
    <InteractiveShell>
      <ServerHeavyComponent /> {/* サーバーで実行される */}
    </InteractiveShell>
  );
}
```

### いつ Client Component にするか

| 条件 | Server Component | Client Component |
|------|:---:|:---:|
| DB/API 直接アクセス | ✅ | — |
| Props 表示のみ | ✅ | — |
| `onClick`/`onChange` | — | ✅ |
| `useState`/`useEffect` | — | ✅ |
| ブラウザ API (localStorage等) | — | ✅ |

---

## 2. Suspense Streaming

```tsx
// Bad: トップレベル await でシェル全体がブロック
export default async function Home() {
  const analytics = await getAnalytics(); // 遅いリクエスト
  return <div><Header /><AnalyticsWidget data={analytics} /></div>;
}

// Good: Suspense でシェルを即座に送信、遅い部分は段階的にストリーム
export default function Home() {
  return (
    <div>
      <Header />
      <Suspense fallback={<AnalyticsSkeleton />}>
        <AnalyticsWidget /> {/* 非同期 Server Component */}
      </Suspense>
    </div>
  );
}

// AnalyticsWidget.tsx (Server Component)
async function AnalyticsWidget() {
  const data = await getAnalytics(); // この await は Suspense 内でのみブロック
  return <Dashboard data={data} />;
}
```

---

## 3. Server Actions

```tsx
// app/actions.ts
'use server';
import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const TodoSchema = z.object({
  title: z.string().min(1, 'Title is required'),
});

export async function createTodo(prevState: any, formData: FormData) {
  const result = TodoSchema.safeParse({ title: formData.get('title') });
  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors };
  }
  await db.todo.create({ data: result.data });
  revalidatePath('/todos'); // キャッシュ無効化
  return { success: true };
}
```

```tsx
// app/todos/page.tsx
'use client';
import { useActionState } from 'react';
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? 'Adding...' : 'Add'}</button>;
}

export default function TodoForm() {
  const [state, formAction] = useActionState(createTodo, {});
  return (
    <form action={formAction}>
      <input name="title" />
      {state.errors?.title && <span role="alert">{state.errors.title}</span>}
      <SubmitButton />
    </form>
  );
}
```

### Server Actions vs Route Handlers

| 用途 | Server Actions | Route Handlers |
|------|:---:|:---:|
| フォームミューテーション | ✅ | — |
| UI からのデータ変更 | ✅ | — |
| 公開 API / Webhook | — | ✅ |
| 大容量アップロード | — | ✅ |
| 外部サービスからの呼び出し | — | ✅ |

---

## 4. キャッシュ & 再検証

```tsx
// 静的データ (ビルド時キャッシュ)
const data = await fetch(url, { cache: 'force-cache' });

// 動的データ (リクエスト毎)
const data = await fetch(url, { cache: 'no-store' });

// 時間ベース再検証 (ISR)
const data = await fetch(url, { next: { revalidate: 3600 } });

// タグベース再検証 (オンデマンド)
const data = await fetch(url, { next: { tags: ['products'] } });
// ミューテーション後:
revalidateTag('products');
```

---

## 5. アンチパターン集

| # | アンチパターン | 問題 | 修正 |
|---|------------|------|------|
| 1 | トップレベル `'use client'` | 全子が Client Component 化、バンドル肥大 | リーフに押し下げ + Composition |
| 2 | ページ最上位の `await` | シェル全体がブロック | Suspense で分離 |
| 3 | 直列データフェッチ | サーバーサイドウォーターフォール | `Promise.all` で並列化 |
| 4 | 境界越えの大量データ | HTMLペイロード肥大化 | 必要フィールドのみ渡す |
| 5 | `revalidate` 忘れ | ミューテーション後にUIが古いまま | `revalidatePath`/`revalidateTag` |
| 6 | レイアウトでの `await` | アプリ全体の遅延 | レイアウトは同期、データはページで取得 |

### パフォーマンス実績 (参考値)

- バンドルサイズ: 487KB → 183KB (62%削減)
- Time to Interactive: 3.2s → 1.1s (66%改善)

**Source:** [RSC Mental Models 2025](https://dev.to/eva_clari_289d85ecc68da48/the-complete-guide-to-react-server-components-mental-models-for-2025-390d) · [RSC Performance Pitfalls](https://blog.logrocket.com/react-server-components-performance-mistakes) · [Next.js Official Docs](https://nextjs.org/docs/app/getting-started/server-and-client-components)
