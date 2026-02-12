# Artisan: Interaction Trigger Templates

Question templates for `AskUserQuestion` tool. See SKILL.md for trigger table.

## ON_STATE_MANAGEMENT

```yaml
questions:
  - question: "How should we manage state for this feature?"
    header: "State"
    options:
      - label: "Local state (useState/useReducer)"
        description: "Simple, co-located state for single component"
      - label: "Context API"
        description: "Share state across component tree without prop drilling"
      - label: "Zustand/Jotai (Recommended)"
        description: "Lightweight global state with minimal boilerplate"
      - label: "Redux Toolkit"
        description: "Full-featured state management for complex apps"
    multiSelect: false
```

## ON_RENDERING_STRATEGY

```yaml
questions:
  - question: "What rendering strategy should we use?"
    header: "Rendering"
    options:
      - label: "Server Components (Recommended)"
        description: "Default to server, hydrate only interactive parts"
      - label: "SSG (Static)"
        description: "Pre-render at build time for static content"
      - label: "SSR (Dynamic)"
        description: "Server render on each request for dynamic content"
      - label: "CSR (Client)"
        description: "Client-side only for highly interactive features"
    multiSelect: false
```

## ON_FORM_LIBRARY

```yaml
questions:
  - question: "How should we handle form state and validation?"
    header: "Form"
    options:
      - label: "React Hook Form (Recommended)"
        description: "Performant, minimal re-renders, great DX"
      - label: "Formik"
        description: "Mature, full-featured form library"
      - label: "Native form handling"
        description: "Simple forms without library dependency"
      - label: "Server Actions"
        description: "Form submission via server actions (Next.js 14+)"
    multiSelect: false
```

## ON_DATA_FETCHING

```yaml
questions:
  - question: "How should we fetch and cache data?"
    header: "Data"
    options:
      - label: "TanStack Query (Recommended)"
        description: "Powerful caching, background updates, devtools"
      - label: "SWR"
        description: "Lightweight, stale-while-revalidate strategy"
      - label: "Server Components"
        description: "Fetch on server, no client-side caching"
      - label: "Native fetch + Context"
        description: "Manual implementation without library"
    multiSelect: false
```

## ON_STYLING_STRATEGY

```yaml
questions:
  - question: "How should we handle styling?"
    header: "Styling"
    options:
      - label: "Tailwind CSS (Recommended)"
        description: "Utility-first, great DX, excellent performance"
      - label: "CSS Modules"
        description: "Scoped CSS, familiar syntax, no runtime"
      - label: "CSS-in-JS (styled-components/Emotion)"
        description: "Dynamic styles, theming, co-located"
      - label: "Follow existing project convention"
        description: "Use whatever the project already uses"
    multiSelect: false
```
