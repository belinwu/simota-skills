# Page & Flow UX Patterns Reference

Comprehensive page-level and flow-level UX patterns for Palette.

## Page States

### Empty States

**When to Use:** Any view that can contain zero items (lists, tables, dashboards, search results).

**Decision Matrix:**

| Scenario | Illustration | Message | CTA | Example |
|----------|-------------|---------|-----|---------|
| First-use (no data yet) | Welcome graphic | Explain value | Primary action | "Create your first project" |
| Search no results | Search icon | Acknowledge query | Suggest alternatives | "No results for 'xyz'. Try different keywords." |
| Filter no results | Filter icon | Explain cause | Clear filters | "No items match your filters." |
| Data deleted/archived | Folder icon | Explain state | Navigate or undo | "All items archived. View archive?" |
| Permission denied | Lock icon | Explain access | Request access | "You don't have access. Request from admin." |

**First-Use Empty State:**

```tsx
// Use when: User sees a section for the first time with no data
function FirstUseEmptyState({
  title,
  description,
  actionLabel,
  onAction,
  illustration: Illustration,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      {Illustration && (
        <div className="mb-6 text-gray-300" aria-hidden>
          <Illustration className="h-24 w-24" />
        </div>
      )}
// ...
```

**Search No Results:**

```tsx
// Use when: Search query returns zero matches
function SearchNoResults({
  query,
  suggestions,
  onClearSearch,
}: SearchNoResultsProps) {
  return (
    <div className="text-center py-12 px-4">
      <SearchIcon className="h-12 w-12 text-gray-300 mx-auto mb-4" aria-hidden />
      <h3 className="text-lg font-medium text-gray-900 mb-2">
        No results for &ldquo;{query}&rdquo;
      </h3>
      <p className="text-sm text-gray-500 mb-4">
        Try different keywords or check for typos.
      </p>
// ...
```

**Filter No Results:**

```tsx
// Use when: Active filters exclude all items
function FilterNoResults({
  activeFilterCount,
  onClearFilters,
}: FilterNoResultsProps) {
  return (
    <div className="text-center py-12 px-4">
      <FilterIcon className="h-12 w-12 text-gray-300 mx-auto mb-4" aria-hidden />
      <h3 className="text-lg font-medium text-gray-900 mb-2">
        No items match your filters
      </h3>
      <p className="text-sm text-gray-500 mb-4">
        {activeFilterCount} active filter{activeFilterCount > 1 ? "s" : ""} applied.
        Try adjusting or clearing filters.
      </p>
// ...
```

**Empty State Anti-Patterns:**

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Blank screen | User thinks page is broken | Add illustration + message + CTA |
| "No data" with no action | User doesn't know what to do | Always provide a next step |
| Technical message ("null", "[]") | Confuses non-technical users | Use friendly, plain language |
| Same empty state for all scenarios | Misses context-specific guidance | Customize per scenario |

---

### Error Pages

**Error Page Decision Matrix:**

| Error | User Message | Recovery Action |
|-------|-------------|-----------------|
| 404 Not Found | "We couldn't find that page" | Search, go home, go back |
| 403 Forbidden | "You don't have access" | Request access, contact admin |
| 500 Server Error | "Something went wrong on our end" | Retry, go home, contact support |
| Network Error | "You appear to be offline" | Retry when connected |
| Timeout | "This is taking longer than expected" | Retry, check status |

**404 Page:**

```tsx
// Use when: Page or resource not found
function NotFoundPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] px-4 text-center">
      <p className="text-6xl font-bold text-gray-200 mb-4" aria-hidden>
        404
      </p>
      <h1 className="text-xl font-semibold text-gray-900 mb-2">
        Page not found
      </h1>
      <p className="text-sm text-gray-500 max-w-md mb-6">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <div className="flex gap-3">
        <button
// ...
```

**500 Error Page:**

```tsx
// Use when: Server-side error occurred
function ServerErrorPage({ onRetry }: { onRetry?: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] px-4 text-center">
      <AlertCircleIcon className="h-16 w-16 text-red-300 mb-4" aria-hidden />
      <h1 className="text-xl font-semibold text-gray-900 mb-2">
        Something went wrong
      </h1>
      <p className="text-sm text-gray-500 max-w-md mb-6">
        We're having trouble loading this page. Please try again or come back later.
      </p>
      <div className="flex gap-3">
        {onRetry && (
          <button
            onClick={onRetry}
// ...
```

**Inline Error Boundary:**

```tsx
// Use when: A section of the page fails but the rest still works
function SectionErrorFallback({
  error,
  onRetry,
}: {
  error: Error;
  onRetry: () => void;
}) {
  return (
    <div className="flex items-center justify-between p-4 bg-red-50 border border-red-100 rounded" role="alert">
      <div className="flex items-center gap-3">
        <AlertCircleIcon className="h-5 w-5 text-red-500 flex-shrink-0" aria-hidden />
        <p className="text-sm text-red-700">
          Failed to load this section.
        </p>
// ...
```

---

### Loading States

**Full Page Skeleton:**

```tsx
// Use when: Loading an entire page with known layout structure
function PageSkeleton() {
  return (
    <div className="animate-pulse space-y-6 p-6" aria-busy="true" aria-label="Loading page">
      {/* Header skeleton */}
      <div className="space-y-2">
        <div className="h-8 bg-gray-200 rounded w-1/3" />
        <div className="h-4 bg-gray-200 rounded w-1/2" />
      </div>
      {/* Content skeleton */}
      <div className="grid grid-cols-3 gap-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-32 bg-gray-200 rounded" />
        ))}
      </div>
// ...
```

**Content Placeholder (Skeleton for Cards):**

```tsx
// Use when: Loading a grid of cards
function CardGridSkeleton({ count = 6 }: { count?: number }) {
  return (
    <div
      className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
      aria-busy="true"
      aria-label="Loading content"
    >
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="animate-pulse border rounded-lg p-4 space-y-3">
          <div className="h-4 bg-gray-200 rounded w-3/4" />
          <div className="h-3 bg-gray-200 rounded w-full" />
          <div className="h-3 bg-gray-200 rounded w-2/3" />
          <div className="flex gap-2 mt-4">
            <div className="h-6 bg-gray-200 rounded w-16" />
// ...
```

**Skeleton Design Rule:** Match the skeleton shape to the actual content layout. Users should recognize the UI before it loads.

---

### Offline States

```tsx
// Use when: User loses network connectivity
function OfflineBanner() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);
    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

// ...
```

**Reconnection Pattern:**

```tsx
// Use when: Showing reconnection state after offline period
function ReconnectionNotice({ isReconnecting }: { isReconnecting: boolean }) {
  if (!isReconnecting) return null;

  return (
    <div
      role="status"
      aria-live="polite"
      className="fixed top-0 inset-x-0 z-50 bg-green-500 text-white text-sm text-center py-2 px-4"
    >
      <RefreshIcon className="inline h-4 w-4 mr-2 animate-spin" aria-hidden />
      Reconnecting... Syncing your changes.
    </div>
  );
}
```

---

## Navigation & Wayfinding

### Breadcrumbs

```tsx
// Use when: Pages deeper than 2 levels in hierarchy
function Breadcrumbs({ items }: { items: BreadcrumbItem[] }) {
  return (
    <nav aria-label="Breadcrumb" className="mb-4">
      <ol className="flex items-center gap-1 text-sm text-gray-500">
        {items.map((item, index) => (
          <li key={item.href} className="flex items-center gap-1">
            {index > 0 && (
              <ChevronRightIcon className="h-3 w-3 text-gray-400" aria-hidden />
            )}
            {index === items.length - 1 ? (
              <span aria-current="page" className="text-gray-900 font-medium">
                {item.label}
              </span>
            ) : (
// ...
```

**Breadcrumb with Overflow (Mobile):**

```tsx
// Use when: Breadcrumb trail is too long for mobile screens
function CollapsibleBreadcrumbs({ items }: { items: BreadcrumbItem[] }) {
  const showCollapsed = items.length > 3;

  return (
    <nav aria-label="Breadcrumb" className="mb-4">
      <ol className="flex items-center gap-1 text-sm text-gray-500">
        {/* Always show first item */}
        <BreadcrumbItem item={items[0]} />

        {showCollapsed && (
          <>
            <ChevronRightIcon className="h-3 w-3 text-gray-400" aria-hidden />
            <li>
              <DropdownMenu>
// ...
```

---

### Dead-End Prevention

Every page should have at least one clear next action. Check for these patterns:

| Page Type | Required Next Actions |
|-----------|----------------------|
| Detail page | Edit, Delete, Back to list |
| Success page | View item, Create another, Go to dashboard |
| Error page | Retry, Go back, Go home |
| Empty state | Create first item, Import data |
| Settings | Save, Cancel, Back |
| End of wizard | View result, Share, Go to dashboard |

```tsx
// Pattern: Page footer with contextual actions
function PageActions({
  primaryAction,
  secondaryActions,
}: PageActionsProps) {
  return (
    <div className="flex items-center justify-between border-t pt-4 mt-8">
      <div className="flex gap-2">
        {secondaryActions?.map((action) => (
          <button
            key={action.label}
            onClick={action.onClick}
            className="px-4 py-2 text-sm border rounded hover:bg-gray-50"
          >
            {action.label}
// ...
```

---

### Multi-Step Progress Indicator

```tsx
// Use when: Multi-step wizard or process with 3+ steps
function StepIndicator({
  steps,
  currentStep,
}: {
  steps: { label: string }[];
  currentStep: number;
}) {
  return (
    <nav aria-label="Progress">
      <ol className="flex items-center">
        {steps.map((step, index) => (
          <li key={step.label} className="flex items-center">
            <div
              className={cn(
// ...
```

---

## Search, Filter & Data Display

### Search Patterns

**Instant Search with Debounce:**

```tsx
// Use when: Searching a dataset client-side or with fast API
function SearchInput({
  onSearch,
  placeholder = "Search...",
}: SearchInputProps) {
  const [query, setQuery] = useState("");

  const debouncedSearch = useDebouncedCallback((value: string) => {
    onSearch(value);
  }, 300);

  return (
    <div className="relative">
      <SearchIcon
        className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400"
// ...
```

**Search with Suggestions:**

```tsx
// Use when: Predictive search helps users find results faster
function SearchWithSuggestions({ suggestions, onSelect }: Props) {
  const [query, setQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const filtered = suggestions.filter((s) =>
    s.label.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="relative" role="combobox" aria-expanded={isOpen}>
      <input
        type="search"
        value={query}
        onChange={(e) => {
// ...
```

---

### Filter Patterns

**Visible Filters with Active Indicators:**

```tsx
// Use when: Users need to narrow down a list with multiple criteria
function FilterBar({
  filters,
  activeFilters,
  onToggle,
  onClearAll,
}: FilterBarProps) {
  const activeCount = Object.values(activeFilters).flat().length;

  return (
    <div className="flex flex-wrap items-center gap-2 mb-4">
      {filters.map((filter) => (
        <DropdownMenu key={filter.id}>
          <DropdownMenuTrigger
            className={cn(
// ...
```

**Active Filter Tags:**

```tsx
// Use when: Showing removable tags for each active filter
function ActiveFilterTags({
  tags,
  onRemove,
  onClearAll,
}: ActiveFilterTagsProps) {
  if (tags.length === 0) return null;

  return (
    <div className="flex flex-wrap items-center gap-2 mb-4" role="list" aria-label="Active filters">
      {tags.map((tag) => (
        <span
          key={tag.id}
          role="listitem"
          className="inline-flex items-center gap-1 px-2 py-1 bg-gray-100 rounded text-sm"
// ...
```

---

### Data Tables

```tsx
// Use when: Displaying structured data with sorting and pagination
function DataTable<T>({
  columns,
  data,
  sortColumn,
  sortDirection,
  onSort,
}: DataTableProps<T>) {
  return (
    <div className="overflow-x-auto border rounded">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b bg-gray-50">
            {columns.map((col) => (
              <th
// ...
```

**Table with Row Actions:**

```tsx
// Pattern: Row-level actions via dropdown menu
<td className="px-4 py-3 text-right">
  <DropdownMenu>
    <DropdownMenuTrigger asChild>
      <button
        aria-label={`Actions for ${row.name}`}
        className="p-1 hover:bg-gray-100 rounded"
      >
        <MoreHorizontalIcon className="h-4 w-4" />
      </button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end">
      <DropdownMenuItem onClick={() => onEdit(row.id)}>
        Edit
      </DropdownMenuItem>
// ...
```

---

### Pagination

```tsx
// Use when: Splitting large datasets across pages
function Pagination({
  currentPage,
  totalPages,
  onPageChange,
}: PaginationProps) {
  const pages = generatePageNumbers(currentPage, totalPages);

  return (
    <nav aria-label="Pagination" className="flex items-center justify-between mt-4">
      <p className="text-sm text-gray-500">
        Page {currentPage} of {totalPages}
      </p>
      <div className="flex items-center gap-1">
        <button
// ...
```

**Infinite Scroll vs Pagination Decision:**

| Factor | Pagination | Infinite Scroll |
|--------|-----------|-----------------|
| Content type | Structured data, tables | Social feeds, galleries |
| User intent | Find specific item | Browse / discover |
| SEO needs | Yes (URL per page) | No |
| Bookmarking | Easy (page number) | Hard (scroll position) |
| Performance | Predictable | Requires virtualization |
| Footer access | Always reachable | Blocked by loading |

---

### Result Feedback

```tsx
// Use when: Showing count and position within results
function ResultSummary({
  total,
  from,
  to,
  query,
}: ResultSummaryProps) {
  return (
    <p className="text-sm text-gray-500" role="status" aria-live="polite">
      {query ? (
        <>
          Showing {from}&ndash;{to} of {total} results for &ldquo;{query}&rdquo;
        </>
      ) : (
        <>
// ...
```

**Accessibility:** Use `role="status"` and `aria-live="polite"` so screen readers announce updated result counts after search or filter changes.

---

## Onboarding & First-Use

### Progressive Disclosure

```tsx
// Use when: Revealing features in stages to reduce overwhelm
function ProgressiveFeatureReveal({
  userLevel,
}: {
  userLevel: "new" | "intermediate" | "advanced";
}) {
  return (
    <div className="space-y-4">
      {/* Always visible */}
      <FeatureCard title="Create a project" description="Start organizing your work" />

      {/* Visible after first project */}
      {userLevel !== "new" && (
        <FeatureCard title="Invite teammates" description="Collaborate in real-time" />
      )}
// ...
```

**Progressive Disclosure Anti-Patterns:**

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Hiding everything | User cannot discover features | Show basic options always |
| Revealing too soon | Overwhelms new users | Gate by usage milestones |
| No "show all" escape hatch | Power users feel restricted | Provide "Advanced" toggle |

---

### Setup Wizard

```tsx
// Use when: Initial configuration requires multiple decisions
function SetupWizard({ onComplete }: { onComplete: (data: SetupData) => void }) {
  const [step, setStep] = useState(0);
  const [data, setData] = useState<Partial<SetupData>>({});

  const steps = [
    { id: "profile", label: "Profile", component: ProfileStep },
    { id: "workspace", label: "Workspace", component: WorkspaceStep },
    { id: "preferences", label: "Preferences", component: PreferencesStep },
  ];

  const CurrentStepComponent = steps[step].component;

  const handleNext = (stepData: Partial<SetupData>) => {
    const updatedData = { ...data, ...stepData };
// ...
```

---

### Feature Discovery

**Tooltip Coach Mark:**

```tsx
// Use when: Introducing a new feature to existing users
function CoachMark({
  title,
  description,
  onDismiss,
  step,
  totalSteps,
}: CoachMarkProps) {
  return (
    <div
      role="dialog"
      aria-label={title}
      className={cn(
        "absolute z-50 bg-blue-600 text-white rounded-lg shadow-xl p-4 max-w-xs",
        "after:content-[''] after:absolute after:border-8 after:border-transparent",
// ...
```

**Contextual Hint (Inline):**

```tsx
// Use when: Providing inline guidance near a feature
function ContextualHint({
  id,
  children,
  onDismiss,
}: {
  id: string;
  children: React.ReactNode;
  onDismiss: (id: string) => void;
}) {
  return (
    <div className="flex items-start gap-3 p-3 bg-blue-50 border border-blue-100 rounded text-sm">
      <LightbulbIcon className="h-5 w-5 text-blue-500 flex-shrink-0 mt-0.5" aria-hidden />
      <div className="flex-1 text-blue-800">{children}</div>
      <button
// ...
```

---

## Dashboard & Overview Layouts

### Metric Card

```tsx
// Use when: Showing KPIs or summary metrics on dashboards
function MetricCard({
  label,
  value,
  change,
  changeDirection,
  icon: Icon,
}: MetricCardProps) {
  return (
    <div className="p-6 bg-white border rounded-lg">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-500">{label}</span>
        {Icon && (
          <div className="h-8 w-8 rounded bg-gray-50 flex items-center justify-center">
            <Icon className="h-4 w-4 text-gray-400" aria-hidden />
// ...
```

### Status Indicators

```tsx
// Use when: Showing item or system status at a glance
function StatusBadge({
  status,
}: {
  status: "active" | "warning" | "error" | "inactive";
}) {
  const config = {
    active: { label: "Active", className: "bg-green-50 text-green-700 border-green-200" },
    warning: { label: "Warning", className: "bg-yellow-50 text-yellow-700 border-yellow-200" },
    error: { label: "Error", className: "bg-red-50 text-red-700 border-red-200" },
    inactive: { label: "Inactive", className: "bg-gray-50 text-gray-500 border-gray-200" },
  };

  const { label, className } = config[status];

// ...
```

### Quick Actions

```tsx
// Use when: Providing shortcuts to frequently used operations
function QuickActions({ actions }: { actions: QuickAction[] }) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
      {actions.map((action) => (
        <button
          key={action.id}
          onClick={action.onClick}
          className={cn(
            "flex flex-col items-center gap-2 p-4 rounded-lg border",
            "hover:bg-gray-50 hover:border-gray-300 transition-colors",
            "focus-visible:ring-2 focus-visible:ring-blue-500"
          )}
        >
          <div className="h-10 w-10 rounded-full bg-blue-50 flex items-center justify-center">
// ...
```

---

## Accessibility Notes for Page Patterns

| Pattern | Accessibility Requirement |
|---------|--------------------------|
| Empty states | Informative text (not just images) for screen readers |
| Error pages | Focus the main heading on page load |
| Loading states | `aria-busy="true"` on loading container, `aria-label` for context |
| Breadcrumbs | Wrap in `<nav aria-label="Breadcrumb">`, current page uses `aria-current="page"` |
| Pagination | `aria-label="Pagination"`, `aria-current="page"` on active page |
| Sortable tables | `aria-sort` attribute on sorted column header |
| Search results | `aria-live="polite"` on result count for updates |
| Step indicators | `aria-current="step"` on current step, screen reader text for X of Y |
| Status badges | Do not rely on color alone; include text label |
| Coach marks | Use `role="dialog"` with `aria-label` |

---

## Anti-Pattern Summary

| Anti-Pattern | Category | Impact | Fix |
|-------------|----------|--------|-----|
| Blank page when empty | Empty State | User thinks page is broken | Add illustration + CTA |
| "Error" with no detail | Error Page | User cannot recover | Show cause + next step |
| Full-page spinner for 3+ seconds | Loading | User loses patience | Use skeleton matching layout |
| No offline indication | Offline | User confused by failures | Show banner + cached data |
| No breadcrumbs at depth > 2 | Navigation | User lost in hierarchy | Add breadcrumb trail |
| Dead-end pages | Navigation | User abandons flow | Always provide next action |
| Search with no "clear" button | Search | User manually erases query | Add clear (X) button |
| Filters with no count/indicator | Filter | User forgets active filters | Show active filter badges |
| Unsortable data tables | Data Display | User cannot find items | Add sort to key columns |
| All features shown to new users | Onboarding | Cognitive overload | Stage feature reveal |
