# Component Patterns

Cross-framework patterns for accessibility, error handling, loading states, and form validation.

---

## Accessibility Patterns

### Semantic HTML First

```tsx
// DO: Use semantic elements
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/home">Home</a></li>
    <li><a href="/about" aria-current="page">About</a></li>
  </ul>
</nav>

// DON'T: Use divs for everything
<div class="nav">
  <div onclick="navigate('/home')">Home</div>
</div>
```

### ARIA Attributes

```tsx
// Live regions for dynamic content
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Dialog/Modal
<dialog
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-description"
>
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-description">Are you sure you want to proceed?</p>
</dialog>

// Toggle button
<button
  aria-pressed={isActive}
  aria-label="Toggle dark mode"
  onClick={() => setIsActive(!isActive)}
>
  {isActive ? 'On' : 'Off'}
</button>
```

### Keyboard Navigation

```tsx
function useKeyboardNavigation(items: HTMLElement[]) {
  const handleKeyDown = (e: KeyboardEvent, currentIndex: number) => {
    let nextIndex: number;

    switch (e.key) {
      case 'ArrowDown':
      case 'ArrowRight':
        e.preventDefault();
        nextIndex = (currentIndex + 1) % items.length;
        items[nextIndex]?.focus();
        break;
      case 'ArrowUp':
      case 'ArrowLeft':
        e.preventDefault();
        nextIndex = (currentIndex - 1 + items.length) % items.length;
        items[nextIndex]?.focus();
        break;
      case 'Home':
        e.preventDefault();
        items[0]?.focus();
        break;
      case 'End':
        e.preventDefault();
        items[items.length - 1]?.focus();
        break;
    }
  };

  return { handleKeyDown };
}
```

### Focus Management

```tsx
// Trap focus within modal
function useFocusTrap(containerRef: React.RefObject<HTMLElement>) {
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const focusableElements = container.querySelectorAll(
      'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );

    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

    firstElement?.focus();

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement?.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement?.focus();
        }
      }
    };

    container.addEventListener('keydown', handleKeyDown);
    return () => container.removeEventListener('keydown', handleKeyDown);
  }, [containerRef]);
}
```

---

## Error State Patterns

### Error Boundary with Recovery

```tsx
function ErrorFallback({
  error,
  resetErrorBoundary,
}: {
  error: Error;
  resetErrorBoundary: () => void;
}) {
  return (
    <div role="alert" className="error-container">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

// Usage
<ErrorBoundary
  FallbackComponent={ErrorFallback}
  onReset={() => queryClient.clear()}
>
  <MyComponent />
</ErrorBoundary>
```

### Inline Error Display

```tsx
interface FieldErrorProps {
  error?: string;
  fieldId: string;
}

function FieldError({ error, fieldId }: FieldErrorProps) {
  if (!error) return null;

  return (
    <p
      id={`${fieldId}-error`}
      role="alert"
      className="text-sm text-destructive mt-1"
    >
      {error}
    </p>
  );
}

// Usage
<input
  id="email"
  aria-invalid={!!errors.email}
  aria-describedby={errors.email ? 'email-error' : undefined}
/>
<FieldError error={errors.email} fieldId="email" />
```

---

## Loading State Patterns

### Skeleton Loading

```tsx
interface SkeletonProps {
  width?: string;
  height?: string;
  className?: string;
}

function Skeleton({ width, height, className }: SkeletonProps) {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-muted", className)}
      style={{ width, height }}
      aria-hidden="true"
    />
  );
}

// Card skeleton
function CardSkeleton() {
  return (
    <div className="space-y-3" aria-busy="true" aria-label="Loading content">
      <Skeleton height="200px" />
      <Skeleton height="20px" width="80%" />
      <Skeleton height="16px" width="60%" />
    </div>
  );
}
```

### Async State Component

```tsx
interface AsyncContentProps<T> {
  data: T | null | undefined;
  isLoading: boolean;
  error: Error | null;
  skeleton: React.ReactNode;
  empty?: React.ReactNode;
  children: (data: T) => React.ReactNode;
}

function AsyncContent<T>({
  data,
  isLoading,
  error,
  skeleton,
  empty,
  children,
}: AsyncContentProps<T>) {
  if (isLoading) return <>{skeleton}</>;
  if (error) return <ErrorDisplay error={error} />;
  if (!data || (Array.isArray(data) && data.length === 0)) {
    return <>{empty ?? <EmptyState />}</>;
  }
  return <>{children(data)}</>;
}

// Usage
<AsyncContent
  data={users}
  isLoading={isLoading}
  error={error}
  skeleton={<UserListSkeleton />}
  empty={<p>No users found</p>}
>
  {(users) => <UserList users={users} />}
</AsyncContent>
```

---

## Form Validation Patterns

### Field-Level Validation with Accessible Feedback

```tsx
interface FormFieldProps {
  label: string;
  name: string;
  type?: string;
  required?: boolean;
  error?: string;
  helpText?: string;
}

function FormField({
  label,
  name,
  type = 'text',
  required,
  error,
  helpText,
}: FormFieldProps) {
  const inputId = `field-${name}`;
  const errorId = `${inputId}-error`;
  const helpId = `${inputId}-help`;

  const describedBy = [
    error ? errorId : null,
    helpText ? helpId : null,
  ].filter(Boolean).join(' ') || undefined;

  return (
    <div className="form-field">
      <label htmlFor={inputId}>
        {label}
        {required && <span aria-hidden="true"> *</span>}
        {required && <span className="sr-only"> (required)</span>}
      </label>

      <input
        id={inputId}
        name={name}
        type={type}
        required={required}
        aria-invalid={!!error}
        aria-describedby={describedBy}
      />

      {helpText && (
        <p id={helpId} className="text-sm text-muted">
          {helpText}
        </p>
      )}

      {error && (
        <p id={errorId} role="alert" className="text-sm text-destructive">
          {error}
        </p>
      )}
    </div>
  );
}
```
