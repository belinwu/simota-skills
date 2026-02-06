# Styling Strategy & Component Checklist

Styling approach selection guide and production component verification checklist.

---

## Styling Decision Guide

| Approach | Best For | Pros | Cons |
|----------|----------|------|------|
| **Tailwind CSS** | Rapid prototyping, utility-first | Fast, consistent, small bundle | Learning curve, verbose markup |
| **CSS Modules** | Component isolation | True scoping, familiar CSS | More files, no utilities |
| **CSS-in-JS** | Dynamic styles, theming | Full JS power, co-location | Runtime cost, SSR complexity |
| **Vanilla CSS** | Simple projects, performance | No dependencies, familiar | Global scope, manual organization |

---

## Tailwind CSS Patterns

```tsx
// Using cn() utility for conditional classes
import { cn } from '@/lib/utils';

interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  children: React.ReactNode;
}

const Button = ({ variant = 'primary', size = 'md', className, children }: ButtonProps) => (
  <button
    className={cn(
      // Base styles
      'inline-flex items-center justify-center rounded-md font-medium transition-colors',
      'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
      'disabled:pointer-events-none disabled:opacity-50',
      // Variant styles
      {
        'bg-primary text-primary-foreground hover:bg-primary/90': variant === 'primary',
        'bg-secondary text-secondary-foreground hover:bg-secondary/80': variant === 'secondary',
      },
      // Size styles
      {
        'h-8 px-3 text-sm': size === 'sm',
        'h-10 px-4 text-base': size === 'md',
        'h-12 px-6 text-lg': size === 'lg',
      },
      className
    )}
  >
    {children}
  </button>
);
```

---

## CSS Modules Patterns

```css
/* Button.module.css */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: background-color 0.2s;
}

.button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.primary {
  background: var(--color-primary);
  color: var(--color-primary-foreground);
}

.secondary {
  background: var(--color-secondary);
  color: var(--color-secondary-foreground);
}
```

```tsx
// Button.tsx
import styles from './Button.module.css';

const Button = ({ variant = 'primary', children }: ButtonProps) => (
  <button className={`${styles.button} ${styles[variant]}`}>
    {children}
  </button>
);
```

---

## Component Checklist

Before completing a component, verify:

### Functionality
- [ ] All props are typed with TypeScript
- [ ] Default props are sensible
- [ ] Edge cases handled (empty, loading, error states)
- [ ] Form validation provides clear feedback

### Accessibility
- [ ] Semantic HTML elements used
- [ ] ARIA attributes where needed
- [ ] Keyboard navigation works
- [ ] Focus management is correct
- [ ] Color contrast meets WCAG AA

### Performance
- [ ] No unnecessary re-renders
- [ ] Large lists are virtualized
- [ ] Images are optimized (next/image, lazy loading)
- [ ] Code splitting for large components

### Testing
- [ ] Component is testable in isolation
- [ ] Key interactions have test coverage
- [ ] Accessibility tests pass

### Code Quality
- [ ] No `any` types used
- [ ] Consistent naming conventions
- [ ] Props interface is well-documented
- [ ] Component follows single responsibility principle
