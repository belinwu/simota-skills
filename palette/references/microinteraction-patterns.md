# Microinteraction Patterns

Implementation patterns for common UX improvements. Each includes when to use and code guidance.

---

## Button Feedback Pattern

```
States: idle → hover → pressed → loading → success/error → idle
Use when: Any async operation triggered by button click
```

```tsx
// Pattern: Button with loading + success feedback
<Button
  onClick={handleSubmit}
  disabled={isLoading}
  aria-busy={isLoading}
  className={cn(
    "transition-all duration-200",
    isSuccess && "bg-green-500",
    isError && "bg-red-500 animate-shake"
  )}
>
  {isLoading && <Spinner className="mr-2" aria-hidden />}
  {isSuccess && <CheckIcon className="mr-2" aria-hidden />}
  {isError && <XIcon className="mr-2" aria-hidden />}
  {isLoading ? "Processing..." : isSuccess ? "Done!" : "Submit"}
</Button>
```

---

## Form Validation Patterns

See also `form-patterns.md` for comprehensive form patterns including multi-step forms, field affordances, and inline help.

### Real-time Validation (recommended for formats)
```tsx
// Use when: Email, phone, URL, password strength
<Input
  type="email"
  onChange={(e) => {
    setValue(e.target.value);
    setError(validateEmail(e.target.value) ? null : "Invalid email");
  }}
  aria-invalid={!!error}
  aria-describedby={error ? "email-error" : undefined}
/>
{error && <p id="email-error" role="alert">{error}</p>}
```

### On-blur Validation (recommended for most fields)
```tsx
// Use when: Name, address, general text inputs
<Input
  onBlur={() => setTouched(true)}
  aria-invalid={touched && !!error}
/>
{touched && error && <p role="alert">{error}</p>}
```

### Submit-time Validation (use sparingly)
```tsx
// Use when: Cross-field validation, complex rules
// Always scroll to first error and focus it
```

---

## Loading State Patterns

### Skeleton Screen (recommended for content loading)
```tsx
// Use when: Loading known content structure
<div className="animate-pulse">
  <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
  <div className="h-4 bg-gray-200 rounded w-1/2" />
</div>
```

### Spinner (use for actions)
```tsx
// Use when: Button actions, form submissions
<div className="flex items-center justify-center">
  <Spinner aria-label="Loading..." />
</div>
```

### Progressive Loading (use for large lists)
```tsx
// Use when: Infinite scroll, paginated content
// Show skeleton for incoming items only
```

### Optimistic Update (use for fast feedback)
```tsx
// Use when: Toggle, like, bookmark actions
// Update UI immediately, rollback on error
const handleLike = async () => {
  setLiked(true); // Optimistic
  try {
    await api.like(id);
  } catch {
    setLiked(false); // Rollback
    toast.error("Failed to like");
  }
};
```

---

## Notification Patterns

| Type | Duration | Use When |
|------|----------|----------|
| Toast (success) | 3s auto-dismiss | Action completed successfully |
| Toast (error) | 5s or manual | Action failed, needs attention |
| Toast (undo) | 5s with action | Destructive action completed |
| Inline alert | Persistent | Form errors, field warnings |
| Banner | Until dismissed | System-wide announcements |

```tsx
// Toast with undo action
<Toast duration={5000}>
  Item deleted.
  <Button variant="link" onClick={handleUndo}>Undo</Button>
</Toast>
```

---

## Destructive Action Patterns

### Confirmation Dialog (recommended)
```tsx
// Use when: Delete, permanent changes
<AlertDialog>
  <AlertDialogTrigger>Delete</AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogTitle>Delete this item?</AlertDialogTitle>
    <AlertDialogDescription>
      This action cannot be undone.
    </AlertDialogDescription>
    <AlertDialogCancel>Cancel</AlertDialogCancel>
    <AlertDialogAction onClick={handleDelete}>
      Delete
    </AlertDialogAction>
  </AlertDialogContent>
</AlertDialog>
```

### Soft Delete with Undo (preferred when possible)
```tsx
// Use when: Items can be recovered
const handleDelete = () => {
  hideItem(id); // Visual removal
  toast({
    message: "Item deleted",
    action: { label: "Undo", onClick: () => restoreItem(id) },
    onClose: () => permanentDelete(id), // After toast dismissed
  });
};
```

---

## UX Coding Standards

### Good UX Code
```tsx
// GOOD: Clear feedback states + accessible
<button
  aria-label="Delete project"
  className="hover:bg-red-50 focus-visible:ring-2"
  disabled={isDeleting}
>
  {isDeleting ? <Spinner /> : <TrashIcon />}
</button>

// GOOD: Inline validation with helpful guidance
<div>
  <label htmlFor="password">Password</label>
  <input id="password" type="password" aria-describedby="password-hint" />
  <p id="password-hint" className="text-sm text-muted">
    At least 8 characters with one number
  </p>
</div>

// GOOD: Optimistic UI with undo option
<Toast>
  Item archived. <button onClick={undo}>Undo</button>
</Toast>
```

### Bad UX Code
```tsx
// BAD: No loading state, no disabled state, no feedback
<button onClick={handleDelete}><TrashIcon /></button>

// BAD: Silent failure, user doesn't know what happened
try { await saveData(); } catch (e) { console.error(e); }

// BAD: Destructive action with no confirmation
<button onClick={() => deleteAllData()}>Reset</button>

// BAD: Form validates only on submit
<form onSubmit={validateAndSubmit}>...</form>
```
