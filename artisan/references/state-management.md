# State Management Decision Guide

> 状態分類、ツール選定フレームワーク、アンチパターン

## 1. 状態の4分類

| 種類 | 説明 | 推奨ツール |
|------|------|-----------|
| **Remote State** | API/DBデータ。フェッチ・キャッシュ・同期が必要 | TanStack Query / SWR |
| **URL State** | URL パラメータに反映されるUI状態 | nuqs / searchParams |
| **Local State** | コンポーネント内に閉じた状態 | `useState` / `useReducer` |
| **Shared State** | 複数の離れたコンポーネント間で共有 | Context (少) → Zustand (多) |

---

## 2. 決定フローチャート

```
状態が必要？
├── サーバーデータ？ → TanStack Query / SWR
├── URL に反映すべき？ → nuqs / useSearchParams
├── 単一コンポーネント内？ → useState / useReducer
└── 複数コンポーネントで共有？
    ├── 2-3レベルの親子？ → Props Drilling (OK)
    ├── 1-2個の関心事？ → React Context
    └── 3個以上 or 高頻度更新？ → Zustand
```

---

## 3. ライブラリ選択

| ライブラリ | 適切な場面 | 不適切な場面 |
|-----------|-----------|------------|
| **Zustand** | 共有クライアント状態のデフォルト選択。軽量、セレクティブ再レンダリング | サーバーデータ管理 |
| **TanStack Query** | サーバー状態管理の標準。キャッシュ・重複排除・無効化を自動処理 | 純粋なクライアント状態 |
| **Jotai** | 細粒度リアクティビティ、多数の派生/計算状態 | 単純なグローバル状態 |
| **Redux Toolkit** | 大規模エンタープライズ、厳格なアーキテクチャ、DevTools必須 | 小中規模アプリ |
| **XState** | 複雑なステートマシン (Figma級) | 単純な on/off 状態 |
| **React Context** | テーマ・ロケール等の低頻度更新 | 高頻度更新する状態 |

---

## 4. Zustand ベストプラクティス

```tsx
import { create } from 'zustand';

// ストアは関心事ごとに分割
const useUIStore = create<UIState>()((set) => ({
  isSidebarOpen: false,
  theme: 'light' as const,
  toggleSidebar: () => set((s) => ({ isSidebarOpen: !s.isSidebarOpen })),
  setTheme: (theme) => set({ theme }),
}));

// セレクタで必要な値のみ購読（不要な再レンダリング防止）
function Sidebar() {
  const isOpen = useUIStore((s) => s.isSidebarOpen);
  // theme が変わっても再レンダリングされない
}
```

---

## 5. TanStack Query パターン

```tsx
// カスタムフックでクエリをカプセル化
function useProducts(category?: string) {
  return useQuery({
    queryKey: ['products', { category }],
    queryFn: () => fetchProducts(category),
    staleTime: 5 * 60 * 1000,
  });
}

// Optimistic Update 付きミューテーション
function useUpdateProduct() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateProduct,
    onMutate: async (updated) => {
      await queryClient.cancelQueries({ queryKey: ['products'] });
      const prev = queryClient.getQueryData(['products']);
      queryClient.setQueryData(['products'], (old) =>
        old.map(p => p.id === updated.id ? { ...p, ...updated } : p)
      );
      return { prev };
    },
    onError: (_err, _vars, ctx) => {
      queryClient.setQueryData(['products'], ctx?.prev);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
}
```

---

## 6. アンチパターン

| # | アンチパターン | 問題 | 修正 |
|---|------------|------|------|
| 1 | サーバーデータを Zustand/Redux で管理 | キャッシュ・同期・重複排除を手動実装 | TanStack Query に委譲 |
| 2 | モノリシック Context | 無関係な値の更新で全コンシューマが再レンダリング | 関心事ごとに Context を分離 |
| 3 | Providers Hell (5+ネスト) | 可読性低下、デバッグ困難 | Zustand で統合 or compose utility |
| 4 | ローカル状態の過剰グローバル化 | モーダル開閉等をグローバルストアで管理 | コンポーネント内 `useState` で十分 |
| 5 | `useState` + `useEffect` でURL同期 | 同期バグの温床 | nuqs / useSearchParams |
| 6 | RSC時代にクライアントで全データ管理 | サーバー側処理の利点を無視 | 読み取りはRSC、インタラクティブ部分のみクライアントストア |

**Source:** [React State Management 2025](https://www.developerway.com/posts/react-state-management-2025) · [State Management Trends](https://makersden.io/blog/react-state-management-in-2025) · [React State: Redux vs Zustand vs Jotai](https://inhaq.com/blog/react-state-management-2026-redux-vs-zustand-vs-jotai.html)
