# React Patterns

Production-quality React patterns for components, hooks, error boundaries, React 19 hooks, and form handling.

---

## 1. Component Structure

### Compound Component Pattern

```tsx
interface CardProps {
  children: React.ReactNode;
  className?: string;
}

interface CardComponent extends React.FC<CardProps> {
  Header: typeof CardHeader;
  Body: typeof CardBody;
  Footer: typeof CardFooter;
}

const Card: CardComponent = ({ children, className }) => (
  <div className={cn("rounded-lg border", className)}>{children}</div>
);

const CardHeader: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="border-b p-4 font-semibold">{children}</div>
);

const CardBody: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="p-4">{children}</div>
);

const CardFooter: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="border-t p-4">{children}</div>
);

Card.Header = CardHeader;
Card.Body = CardBody;
Card.Footer = CardFooter;

// Usage
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
</Card>
```

---

## 2. Custom Hooks

```tsx
// Encapsulate complex logic in custom hooks
function useAsync<T>(asyncFn: () => Promise<T>, deps: unknown[] = []) {
  const [state, setState] = useState<{
    data: T | null;
    error: Error | null;
    isLoading: boolean;
  }>({
    data: null,
    error: null,
    isLoading: true,
  });

  useEffect(() => {
    let cancelled = false;

    setState(prev => ({ ...prev, isLoading: true }));

    asyncFn()
      .then(data => {
        if (!cancelled) setState({ data, error: null, isLoading: false });
      })
      .catch(error => {
        if (!cancelled) setState({ data: null, error, isLoading: false });
      });

    return () => { cancelled = true; };
  }, deps);

  return state;
}
```

---

## 3. Error Boundaries

```tsx
interface ErrorBoundaryProps {
  fallback: React.ReactNode;
  children: React.ReactNode;
}

class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}
```

---

## 4. Form Handling (React Hook Form + Zod)

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type FormData = z.infer<typeof schema>;

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    await login(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} aria-invalid={!!errors.email} />
      {errors.email && <span role="alert">{errors.email.message}</span>}

      <input type="password" {...register('password')} />
      {errors.password && <span role="alert">{errors.password.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Log in'}
      </button>
    </form>
  );
}
```

---

## 5. React 19 新フック

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

### use()

Promise や Context をレンダリング中に読み取る新フック。条件分岐内でも呼び出し可能（従来のフックルールの例外）。

```tsx
import { use, Suspense } from 'react';

// Promise を読み取る
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise); // Suspense boundary が必要
  return <h1>{user.name}</h1>;
}

// Context を読み取る（条件付きも可）
function ThemeText({ showTheme }: { showTheme: boolean }) {
  if (showTheme) {
    const theme = use(ThemeContext); // 条件分岐内で OK
    return <p>Current theme: {theme}</p>;
  }
  return <p>Theme hidden</p>;
}

// Usage
<Suspense fallback={<Loading />}>
  <UserProfile userPromise={fetchUser(id)} />
</Suspense>
```

---

## 6. React Compiler

React 19 の Compiler は自動メモ化を行い、安定版として推奨。

| 従来 | React Compiler (安定版) |
|------|-------------------|
| 手動 `useMemo` / `useCallback` | **自動メモ化** — 原則不要 |
| `React.memo` ラッパー | Compiler が判断 |
| 依存配列の管理 | Compiler が追跡 |

**ガイドライン:** 新規コードでは `useMemo`/`useCallback` は不要。既存コードの手動メモ化はそのまま残しても害はない。

---

## 7. フォームハンドリング選択ガイド

| 基準 | React Hook Form | React 19 ネイティブ | Conform | TanStack Form |
|------|:---:|:---:|:---:|:---:|
| 大規模・複雑フォーム | ✅ | — | — | ✅ |
| Server Actions ファースト | △ (ワークアラウンド) | ✅ | ✅ | — |
| JS無効でも動作 | — | ✅ | ✅ | — |
| 動的フィールド配列 | ✅ | 手動 | ○ | ✅ |
| ネストされたフォーム構造 | ○ | 手動 | ○ | ✅ |
| UIライブラリ統合 | ✅ | — | — | ✅ |
| バンドルサイズ | +8.6KB | 0KB | 軽量 | +12KB |

**推奨:** 複雑フォーム → RHF + Zod / シンプル + Server Actions → React 19 ネイティブ / Remix/Next.js PE重視 → Conform / 動的・ネストフォーム → TanStack Form

---

## 8. Hooks アンチパターン

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
