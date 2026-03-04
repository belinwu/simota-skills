# React 19 Hooks & Anti-Patterns

> React 19 新フック、React Compiler、フック設計のベストプラクティスとアンチパターン

## 1. React 19 新フック

### useActionState

フォームアクションの結果と pending 状態を管理。`useReducer` の Server Actions 版。

```tsx
import { useActionState } from 'react';

function ContactForm() {
  const [state, formAction] = useActionState(
    async (prevState, formData: FormData) => {
      const name = formData.get('name') as string;
      const res = await submitContact({ name });
      if (!res.ok) return { error: 'Failed to submit' };
      return { success: true, message: `Thanks ${name}!` };
    },
    {} // initial state
  );

  return (
    <form action={formAction}>
      <input name="name" required />
      <SubmitButton />
      {state.error && <p role="alert">{state.error}</p>}
      {state.success && <p>{state.message}</p>}
    </form>
  );
}
```

### useFormStatus

フォームの送信状態を子コンポーネントから読み取る。**`<form>` の子孫でのみ動作。**

```tsx
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  );
}
```

### useOptimistic

非同期完了前にUIを即座に更新。失敗時は自動ロールバック。

```tsx
import { useOptimistic } from 'react';

function TodoList({ todos, addTodoAction }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo) => [...state, { ...newTodo, pending: true }]
  );

  return (
    <form action={async (formData) => {
      addOptimisticTodo({ text: formData.get('text'), id: crypto.randomUUID() });
      await addTodoAction(formData);
    }}>
      {optimisticTodos.map(todo => (
        <li key={todo.id} style={{ opacity: todo.pending ? 0.5 : 1 }}>
          {todo.text}
        </li>
      ))}
      <input name="text" />
      <button type="submit">Add</button>
    </form>
  );
}
```

---

## 2. React Compiler

React 19 の Compiler は自動メモ化を行う。

| 従来 | React Compiler 時代 |
|------|-------------------|
| 手動 `useMemo` / `useCallback` | **自動メモ化** — 原則不要 |
| `React.memo` ラッパー | Compiler が判断 |
| 依存配列の管理 | Compiler が追跡 |

**注意:** Compiler は段階的に導入。既存の `useMemo`/`useCallback` は害にならないが、新規コードでは不要。

---

## 3. フォームハンドリング選択ガイド

| 基準 | React Hook Form | React 19 ネイティブ | Conform |
|------|:---:|:---:|:---:|
| 大規模・複雑フォーム | ✅ | — | — |
| Server Actions ファースト | △ (ワークアラウンド) | ✅ | ✅ |
| JS無効でも動作 | — | ✅ | ✅ |
| 動的フィールド配列 | ✅ | 手動 | ○ |
| UIライブラリ統合 | ✅ | — | — |
| バンドルサイズ | +8.6KB | 0KB | 軽量 |

**推奨:** 複雑フォーム → RHF + Zod / シンプル + Server Actions → React 19 ネイティブ / Remix/Next.js PE重視 → Conform

---

## 4. Hooks アンチパターン

### AP-1: 派生状態を useEffect で同期

```tsx
// Bad: 不要な state + useEffect
const [items, setItems] = useState([]);
const [filteredItems, setFilteredItems] = useState([]);
useEffect(() => {
  setFilteredItems(items.filter(i => i.active));
}, [items]);

// Good: レンダリング中に直接計算
const [items, setItems] = useState([]);
const filteredItems = items.filter(i => i.active);
```

### AP-2: useEffect でデータフェッチ（クリーンアップなし）

```tsx
// Bad: メモリリーク、レースコンディション
useEffect(() => {
  fetch(`/api/user/${id}`).then(r => r.json()).then(setUser);
}, [id]);

// Good: TanStack Query に委譲
const { data: user } = useQuery({
  queryKey: ['user', id],
  queryFn: () => fetchUser(id),
});
```

### AP-3: 条件付きフック呼び出し

```tsx
// Bad: フックの順序が変わる
if (isLoggedIn) {
  const [user, setUser] = useState(null); // Rules of Hooks 違反
}

// Good: 常に呼び出し、条件分岐はレンダリングで
const [user, setUser] = useState(null);
if (!isLoggedIn) return <LoginPrompt />;
```

### AP-4: 不要な useCallback/useMemo

```tsx
// Bad: 小さな関数を全て useCallback（React Compiler 以前でも過剰）
const handleClick = useCallback(() => {
  console.log('clicked');
}, []);

// Good: パフォーマンス問題が計測されてから最適化
const handleClick = () => console.log('clicked');
```

### AP-5: `use` プレフィックスの誤用

```tsx
// Bad: フックを使わない関数に use プレフィックス
function useFormatDate(date: Date) { // 内部にフックなし
  return date.toLocaleDateString();
}

// Good: 通常の関数として定義
function formatDate(date: Date) {
  return date.toLocaleDateString();
}
```

---

## アンチパターン早見表

| # | パターン | 問題 | 代替 |
|---|---------|------|------|
| 1 | 派生状態を `useEffect` で同期 | 不要な再レンダリング | 直接計算 |
| 2 | `useEffect` で生の `fetch` | リーク、レースコンディション | TanStack Query |
| 3 | 条件付きフック呼び出し | Rules of Hooks 違反 | 常に呼び出し + 早期 return |
| 4 | 過剰な `useMemo`/`useCallback` | 複雑性増加、利点なし | React Compiler / 計測後に判断 |
| 5 | フックなし関数に `use` プレフィックス | 誤解を招く命名 | 通常の関数名 |

**Source:** [React 19 Official Blog](https://react.dev/blog/2024/12/05/react-19) · [React 19 New Hooks](https://manuelsanchezdev.com/blog/react-19-new-hooks-useoptimistic-useformstatus-useactionstate/) · [React Anti-Patterns](https://www.perssondennis.com/articles/react-anti-patterns-and-best-practices-dos-and-donts) · [React Hook Form vs React 19](https://blog.logrocket.com/react-hook-form-vs-react-19/)
