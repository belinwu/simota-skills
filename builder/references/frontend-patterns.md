# Frontend Patterns Reference

Builder agent's React frontend implementation patterns.

## React Server Components (RSC)

```typescript
// Server Component - Data fetching on server
// app/users/page.tsx
export default async function UsersPage() {
  const users = await userRepository.findAll(); // Direct DB access

  return (
    <div>
      <h1>Users</h1>
      <UserList users={users} />
      {/* Client Component only for interactive parts */}
      <AddUserButton />
    </div>
  );
}

// Client Component - Interactive parts only
// components/AddUserButton.tsx
'use client';

export function AddUserButton() {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <>
      <button onClick={() => setIsOpen(true)}>Add User</button>
      {isOpen && <AddUserModal onClose={() => setIsOpen(false)} />}
    </>
  );
}
```

## State Management Patterns

### Server State (TanStack Query)

```typescript
// hooks/useUser.ts
export function useUser(userId: string) {
  return useQuery({
    queryKey: ['users', userId],
    queryFn: () => userApi.getById(userId),
    staleTime: 5 * 60 * 1000, // 5 minute cache
    retry: 3,
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: userApi.update,
    onMutate: async (newUser) => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: ['users', newUser.id] });
      const previousUser = queryClient.getQueryData(['users', newUser.id]);
      queryClient.setQueryData(['users', newUser.id], newUser);
      return { previousUser };
    },
    onError: (err, newUser, context) => {
      // Rollback
      queryClient.setQueryData(['users', newUser.id], context?.previousUser);
    },
    onSettled: (data, error, variables) => {
      queryClient.invalidateQueries({ queryKey: ['users', variables.id] });
    },
  });
}
```

### Client State (Zustand)

```typescript
// stores/uiStore.ts
interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  theme: 'light',
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setTheme: (theme) => set({ theme }),
}));
```

## Form Design (React Hook Form + Zod)

```typescript
// schemas/userForm.ts
const userFormSchema = z.object({
  name: z.string().min(1, 'Name is required').max(100),
  email: z.string().email('Please enter a valid email address'),
  age: z.coerce.number().int().min(0).max(150).optional(),
});

type UserFormData = z.infer<typeof userFormSchema>;

// components/UserForm.tsx
export function UserForm({ onSubmit }: { onSubmit: (data: UserFormData) => void }) {
  const form = useForm<UserFormData>({
    resolver: zodResolver(userFormSchema),
    defaultValues: { name: '', email: '' },
  });

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <input {...form.register('name')} />
      {form.formState.errors.name && (
        <span className="error">{form.formState.errors.name.message}</span>
      )}

      <input {...form.register('email')} />
      {form.formState.errors.email && (
        <span className="error">{form.formState.errors.email.message}</span>
      )}

      <button type="submit" disabled={form.formState.isSubmitting}>
        {form.formState.isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```

## Error Boundary + Suspense

```typescript
// components/ErrorBoundary.tsx
'use client';

export function ErrorBoundary({
  children,
  fallback,
}: {
  children: React.ReactNode;
  fallback: React.ReactNode;
}) {
  return (
    <ErrorBoundaryPrimitive
      fallbackRender={({ error, resetErrorBoundary }) => (
        <div className="error-container">
          <h2>An error occurred</h2>
          <p>{error.message}</p>
          <button onClick={resetErrorBoundary}>Retry</button>
        </div>
      )}
    >
      {children}
    </ErrorBoundaryPrimitive>
  );
}

// app/users/page.tsx
export default function UsersPage() {
  return (
    <ErrorBoundary fallback={<ErrorFallback />}>
      <Suspense fallback={<UserListSkeleton />}>
        <UserList />
      </Suspense>
    </ErrorBoundary>
  );
}
```

## Optimistic UI Updates

```typescript
// hooks/useOptimisticUpdate.ts
export function useOptimisticLike(postId: string) {
  const queryClient = useQueryClient();
  const [optimisticLiked, setOptimisticLiked] = useState<boolean | null>(null);

  const mutation = useMutation({
    mutationFn: () => postApi.toggleLike(postId),
    onMutate: async () => {
      // Optimistically update UI
      const previousPost = queryClient.getQueryData<Post>(['posts', postId]);
      setOptimisticLiked(!previousPost?.liked);
      return { previousPost };
    },
    onError: (err, variables, context) => {
      // Rollback on error
      setOptimisticLiked(null);
      toast.error('Failed to like');
    },
    onSuccess: () => {
      setOptimisticLiked(null);
      queryClient.invalidateQueries({ queryKey: ['posts', postId] });
    },
  });

  const post = queryClient.getQueryData<Post>(['posts', postId]);
  const liked = optimisticLiked ?? post?.liked ?? false;

  return { liked, toggle: mutation.mutate, isLoading: mutation.isPending };
}
```
