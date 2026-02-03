# Implementation Patterns

Playwright implementation patterns for demo video recording.

---

## Basic Test Structure

### Standard Demo Test

```typescript
// demos/specs/demo-login.spec.ts
import { test, expect } from '@playwright/test';
import { showOverlay, waitForTransition } from '../helpers/overlay';
import { prepareAuthState } from '../helpers/auth';
import { DemoData } from '../helpers/data';

test.describe('Demo: Login Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Start from clean state
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('shows complete login experience', async ({ page }) => {
    // === Scene 1: Opening ===
    await showOverlay(page, 'Let\'s log in', 2000);

    // === Scene 2: Form Input ===
    await page.getByRole('link', { name: 'Login' }).click();
    await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();
    await page.waitForTimeout(500);

    // Email input
    await page.getByLabel('Email').fill(DemoData.user.email);
    await page.waitForTimeout(300);

    // Password input
    await page.getByLabel('Password').fill(DemoData.user.password);
    await page.waitForTimeout(300);

    // === Scene 3: Submit ===
    await showOverlay(page, 'Click login button', 1500);
    await page.getByRole('button', { name: 'Login' }).click();

    // === Scene 4: Result Display ===
    await expect(page.getByTestId('dashboard')).toBeVisible();
    await showOverlay(page, 'Login complete!', 2000);
  });
});
```

---

## Authentication Patterns

### Pattern 1: API-based Pre-authentication

```typescript
// demos/helpers/auth.ts
import { Page, BrowserContext } from '@playwright/test';

export async function loginViaApi(context: BrowserContext): Promise<void> {
  const response = await context.request.post('/api/auth/login', {
    data: {
      email: 'demo@example.com',
      password: 'DemoPass123',
    },
  });

  if (!response.ok()) {
    throw new Error('Demo login failed');
  }
}

// Usage
test.beforeEach(async ({ context, page }) => {
  await loginViaApi(context);
  await page.goto('/dashboard');
});
```

### Pattern 2: LocalStorage-based

```typescript
// demos/helpers/auth.ts
export async function setAuthState(page: Page, token: string): Promise<void> {
  await page.evaluate((t) => {
    localStorage.setItem('auth_token', t);
  }, token);
}

// Usage
test.beforeEach(async ({ page }) => {
  await page.goto('/');
  await setAuthState(page, 'demo-jwt-token');
  await page.reload();
});
```

### Pattern 3: Storage State File

```typescript
// demos/auth.setup.ts
import { test as setup } from '@playwright/test';
import path from 'path';

const authFile = path.join(__dirname, '.auth/demo-user.json');

setup('authenticate demo user', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('demo@example.com');
  await page.getByLabel('Password').fill('DemoPass123');
  await page.getByRole('button', { name: 'Login' }).click();
  await page.waitForURL('**/dashboard');
  await page.context().storageState({ path: authFile });
});

// Use in playwright.config.demo.ts
projects: [
  { name: 'setup', testMatch: /.*\.setup\.ts/ },
  {
    name: 'demo-authenticated',
    use: { storageState: '.auth/demo-user.json' },
    dependencies: ['setup'],
  },
]
```

---

## File Upload Pattern

### Image Upload Demo

```typescript
// demos/specs/demo-upload.spec.ts
import { test, expect } from '@playwright/test';
import path from 'path';

test('shows profile image upload', async ({ page }) => {
  await page.goto('/profile/edit');

  // Focus on upload button
  await showOverlay(page, 'Changing profile image', 2000);

  // File selection
  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles(path.join(__dirname, '../fixtures/avatar.png'));

  // Wait for preview display
  await expect(page.getByAltText('Preview')).toBeVisible();
  await page.waitForTimeout(1000);

  // Save
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Saved')).toBeVisible();

  await showOverlay(page, 'Image updated!', 2000);
});
```

---

## Smooth Scroll Pattern

### Natural Scroll Behavior

```typescript
// demos/helpers/scroll.ts
import { Page } from '@playwright/test';

export async function smoothScrollTo(
  page: Page,
  selector: string,
  options: { duration?: number; position?: 'center' | 'start' | 'end' } = {}
): Promise<void> {
  const { duration = 500, position = 'center' } = options;

  await page.evaluate(
    ({ sel, dur, pos }) => {
      const element = document.querySelector(sel);
      if (!element) return;

      const block = pos === 'center' ? 'center' : pos === 'start' ? 'start' : 'end';

      element.scrollIntoView({
        behavior: 'smooth',
        block,
      });

      return new Promise((resolve) => setTimeout(resolve, dur));
    },
    { sel: selector, dur: duration, pos: position }
  );

  await page.waitForTimeout(duration);
}

// Usage
test('shows long page scroll', async ({ page }) => {
  await page.goto('/features');
  await page.waitForTimeout(1000);

  await showOverlay(page, 'Let\'s look at the main features', 1500);

  // Smooth scroll to feature sections
  await smoothScrollTo(page, '#feature-1', { duration: 800 });
  await page.waitForTimeout(1000);

  await smoothScrollTo(page, '#feature-2', { duration: 800 });
  await page.waitForTimeout(1000);

  await smoothScrollTo(page, '#feature-3', { duration: 800 });
  await page.waitForTimeout(1000);
});
```

---

## Overlay Helper Functions

### Complete Overlay System

```typescript
// demos/helpers/overlay.ts
import { Page } from '@playwright/test';

interface OverlayOptions {
  position?: 'top' | 'center' | 'bottom';
  style?: 'info' | 'success' | 'warning' | 'error';
  duration?: number;
}

const styleColors = {
  info: 'rgba(0, 0, 0, 0.85)',
  success: 'rgba(16, 185, 129, 0.9)',
  warning: 'rgba(245, 158, 11, 0.9)',
  error: 'rgba(239, 68, 68, 0.9)',
};

const positionStyles = {
  top: 'top: 20px; left: 50%; transform: translateX(-50%);',
  center: 'top: 50%; left: 50%; transform: translate(-50%, -50%);',
  bottom: 'bottom: 20px; left: 50%; transform: translateX(-50%);',
};

export async function showOverlay(
  page: Page,
  message: string,
  options: OverlayOptions | number = {}
): Promise<void> {
  // If number is passed, treat as duration
  const opts: OverlayOptions =
    typeof options === 'number' ? { duration: options } : options;

  const { position = 'bottom', style = 'info', duration = 2000 } = opts;

  await page.evaluate(
    ({ msg, pos, styleColor, dur }) => {
      // Remove existing overlay
      const existing = document.getElementById('demo-overlay');
      if (existing) existing.remove();

      const overlay = document.createElement('div');
      overlay.id = 'demo-overlay';
      overlay.style.cssText = `
        position: fixed;
        ${pos}
        background: ${styleColor};
        color: white;
        padding: 16px 32px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 500;
        z-index: 99999;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        animation: demoFadeIn 0.3s ease-out;
      `;

      // Animation definition
      const styleSheet = document.createElement('style');
      styleSheet.textContent = `
        @keyframes demoFadeIn {
          from { opacity: 0; transform: translateX(-50%) translateY(10px); }
          to { opacity: 1; transform: translateX(-50%) translateY(0); }
        }
        @keyframes demoFadeOut {
          from { opacity: 1; }
          to { opacity: 0; }
        }
      `;
      document.head.appendChild(styleSheet);

      overlay.textContent = msg;
      document.body.appendChild(overlay);

      // Fade out and remove
      setTimeout(() => {
        overlay.style.animation = 'demoFadeOut 0.3s ease-out forwards';
        setTimeout(() => {
          overlay.remove();
          styleSheet.remove();
        }, 300);
      }, dur - 300);
    },
    { msg: message, pos: positionStyles[position], styleColor: styleColors[style], dur: duration }
  );

  await page.waitForTimeout(duration);
}

// Convenient shortcuts
export async function showSuccess(page: Page, message: string, duration = 2000): Promise<void> {
  await showOverlay(page, message, { style: 'success', duration });
}

export async function showError(page: Page, message: string, duration = 2000): Promise<void> {
  await showOverlay(page, message, { style: 'error', duration });
}

export async function showStep(page: Page, step: number, total: number, message: string): Promise<void> {
  await showOverlay(page, `Step ${step}/${total}: ${message}`, {
    position: 'top',
    duration: 2500,
  });
}
```

---

## Element Highlight Pattern

### Emphasize Specific Element

```typescript
// demos/helpers/highlight.ts
import { Page } from '@playwright/test';

export async function highlightElement(
  page: Page,
  selector: string,
  options: { duration?: number; color?: string; label?: string } = {}
): Promise<void> {
  const { duration = 2000, color = '#3b82f6', label } = options;

  await page.evaluate(
    ({ sel, dur, col, lbl }) => {
      const element = document.querySelector(sel);
      if (!element) return;

      const rect = element.getBoundingClientRect();

      // Highlight box
      const highlight = document.createElement('div');
      highlight.id = 'demo-highlight';
      highlight.style.cssText = `
        position: fixed;
        top: ${rect.top - 4}px;
        left: ${rect.left - 4}px;
        width: ${rect.width + 8}px;
        height: ${rect.height + 8}px;
        border: 3px solid ${col};
        border-radius: 8px;
        z-index: 99998;
        pointer-events: none;
        animation: demoPulse 1s ease-in-out infinite;
      `;

      // Label (optional)
      if (lbl) {
        const labelEl = document.createElement('div');
        labelEl.style.cssText = `
          position: fixed;
          top: ${rect.top - 30}px;
          left: ${rect.left}px;
          background: ${col};
          color: white;
          padding: 4px 12px;
          border-radius: 4px;
          font-size: 14px;
          z-index: 99999;
        `;
        labelEl.textContent = lbl;
        document.body.appendChild(labelEl);

        setTimeout(() => labelEl.remove(), dur);
      }

      const styleSheet = document.createElement('style');
      styleSheet.textContent = `
        @keyframes demoPulse {
          0%, 100% { box-shadow: 0 0 0 0 ${col}40; }
          50% { box-shadow: 0 0 0 10px ${col}00; }
        }
      `;
      document.head.appendChild(styleSheet);

      document.body.appendChild(highlight);

      setTimeout(() => {
        highlight.remove();
        styleSheet.remove();
      }, dur);
    },
    { sel: selector, dur: duration, col: color, lbl: label }
  );

  await page.waitForTimeout(duration);
}

// Usage
test('highlight button with explanation', async ({ page }) => {
  await page.goto('/dashboard');

  await highlightElement(page, '[data-testid="create-button"]', {
    label: 'Click here!',
    duration: 2500,
  });
});
```

---

## Mouse Cursor Simulation

### Visual Mouse Movement

```typescript
// demos/helpers/cursor.ts
import { Page } from '@playwright/test';

export async function showCursor(page: Page): Promise<void> {
  await page.evaluate(() => {
    const cursor = document.createElement('div');
    cursor.id = 'demo-cursor';
    cursor.style.cssText = `
      position: fixed;
      width: 20px;
      height: 20px;
      background: rgba(59, 130, 246, 0.5);
      border: 2px solid #3b82f6;
      border-radius: 50%;
      z-index: 99999;
      pointer-events: none;
      transform: translate(-50%, -50%);
      transition: all 0.1s ease-out;
    `;
    document.body.appendChild(cursor);

    document.addEventListener('mousemove', (e) => {
      cursor.style.left = e.clientX + 'px';
      cursor.style.top = e.clientY + 'px';
    });

    document.addEventListener('mousedown', () => {
      cursor.style.transform = 'translate(-50%, -50%) scale(0.8)';
      cursor.style.background = 'rgba(59, 130, 246, 0.8)';
    });

    document.addEventListener('mouseup', () => {
      cursor.style.transform = 'translate(-50%, -50%) scale(1)';
      cursor.style.background = 'rgba(59, 130, 246, 0.5)';
    });
  });
}

export async function hideCursor(page: Page): Promise<void> {
  await page.evaluate(() => {
    const cursor = document.getElementById('demo-cursor');
    if (cursor) cursor.remove();
  });
}

// Usage
test('demo with cursor display', async ({ page }) => {
  await page.goto('/');
  await showCursor(page);

  // Cursor displayed for subsequent operations
  await page.click('#login-button');
  // ...
});
```

---

## Visual Interaction Feedback System

Visual feedback for user interactions during demo recording. These helpers enhance the viewer's understanding of what's happening on screen by providing clear visual cues for clicks, taps, swipes, and keyboard input.

### Overview

| Effect | Use Case | Default Duration |
|--------|----------|------------------|
| Click Ripple | Desktop click visualization | 600ms |
| Tap Indicator | Mobile/tablet touch feedback | 500ms |
| Swipe Trail | Swipe gesture visualization | 800ms |
| Keystroke Overlay | Keyboard shortcut display | 1500ms |

### Click Ripple Effect

Material Design-inspired ripple effect for mouse clicks.

```typescript
// demos/helpers/interaction-feedback.ts
import { Page } from '@playwright/test';

interface ClickRippleOptions {
  duration?: number;
  color?: string;
  maxRadius?: number;
}

export async function showClickRipple(
  page: Page,
  x: number,
  y: number,
  options: ClickRippleOptions = {}
): Promise<void> {
  const { duration = 600, color = 'rgba(59, 130, 246, 0.6)', maxRadius = 50 } = options;

  await page.evaluate(
    ({ x, y, dur, col, radius }) => {
      const ripple = document.createElement('div');
      ripple.id = 'demo-click-ripple';
      ripple.style.cssText = `
        position: fixed;
        left: ${x}px;
        top: ${y}px;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: radial-gradient(circle, ${col} 0%, transparent 70%);
        transform: translate(-50%, -50%);
        pointer-events: none;
        z-index: 99998;
      `;

      const styleSheet = document.createElement('style');
      styleSheet.id = 'demo-ripple-style';
      styleSheet.textContent = `
        @keyframes demoRippleExpand {
          0% {
            width: 0;
            height: 0;
            opacity: 1;
          }
          100% {
            width: ${radius * 2}px;
            height: ${radius * 2}px;
            opacity: 0;
          }
        }
      `;
      document.head.appendChild(styleSheet);

      ripple.style.animation = `demoRippleExpand ${dur}ms ease-out forwards`;
      document.body.appendChild(ripple);

      setTimeout(() => {
        ripple.remove();
        styleSheet.remove();
      }, dur);
    },
    { x, y, dur: duration, col: color, radius: maxRadius }
  );

  await page.waitForTimeout(duration);
}

// Usage
test('demo with click ripple', async ({ page }) => {
  await page.goto('/dashboard');

  const button = page.getByRole('button', { name: 'Submit' });
  const box = await button.boundingBox();
  if (box) {
    const centerX = box.x + box.width / 2;
    const centerY = box.y + box.height / 2;

    await showClickRipple(page, centerX, centerY);
    await button.click();
  }
});
```

### Touch Tap Indicator

Pulsing circular indicator for mobile touch interactions.

```typescript
// demos/helpers/interaction-feedback.ts

interface TapIndicatorOptions {
  duration?: number;
  radius?: number;
  color?: string;
}

export async function showTapIndicator(
  page: Page,
  x: number,
  y: number,
  options: TapIndicatorOptions = {}
): Promise<void> {
  const { duration = 500, radius = 30, color = 'rgba(59, 130, 246, 0.8)' } = options;

  await page.evaluate(
    ({ x, y, dur, rad, col }) => {
      const tap = document.createElement('div');
      tap.id = 'demo-tap-indicator';
      tap.style.cssText = `
        position: fixed;
        left: ${x}px;
        top: ${y}px;
        width: ${rad * 2}px;
        height: ${rad * 2}px;
        border: 3px solid ${col};
        border-radius: 50%;
        transform: translate(-50%, -50%) scale(0.8);
        pointer-events: none;
        z-index: 99998;
        box-sizing: border-box;
      `;

      const styleSheet = document.createElement('style');
      styleSheet.id = 'demo-tap-style';
      styleSheet.textContent = `
        @keyframes demoTapPulse {
          0% {
            transform: translate(-50%, -50%) scale(0.8);
            opacity: 1;
          }
          50% {
            transform: translate(-50%, -50%) scale(1.2);
            opacity: 0.8;
          }
          100% {
            transform: translate(-50%, -50%) scale(1.0);
            opacity: 0;
          }
        }
      `;
      document.head.appendChild(styleSheet);

      tap.style.animation = `demoTapPulse ${dur}ms ease-out forwards`;
      document.body.appendChild(tap);

      setTimeout(() => {
        tap.remove();
        styleSheet.remove();
      }, dur);
    },
    { x, y, dur: duration, rad: radius, col: color }
  );

  await page.waitForTimeout(duration);
}

// Usage for mobile demos
test('mobile tap demo', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 }); // iPhone 14 Pro

  const menuButton = page.getByTestId('mobile-menu');
  const box = await menuButton.boundingBox();
  if (box) {
    await showTapIndicator(page, box.x + box.width / 2, box.y + box.height / 2);
    await menuButton.tap();
  }
});
```

### Swipe Trail Visualization

SVG-based arrow line showing swipe direction.

```typescript
// demos/helpers/interaction-feedback.ts

interface SwipeTrailOptions {
  duration?: number;
  color?: string;
  strokeWidth?: number;
  showArrow?: boolean;
}

export async function showSwipeTrail(
  page: Page,
  startX: number,
  startY: number,
  endX: number,
  endY: number,
  options: SwipeTrailOptions = {}
): Promise<void> {
  const {
    duration = 800,
    color = 'rgba(59, 130, 246, 0.8)',
    strokeWidth = 4,
    showArrow = true,
  } = options;

  await page.evaluate(
    ({ sx, sy, ex, ey, dur, col, sw, arrow }) => {
      // Calculate dimensions
      const padding = 20;
      const minX = Math.min(sx, ex) - padding;
      const minY = Math.min(sy, ey) - padding;
      const width = Math.abs(ex - sx) + padding * 2;
      const height = Math.abs(ey - sy) + padding * 2;

      // Adjust coordinates relative to SVG
      const x1 = sx - minX;
      const y1 = sy - minY;
      const x2 = ex - minX;
      const y2 = ey - minY;

      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.id = 'demo-swipe-trail';
      svg.setAttribute('width', String(width));
      svg.setAttribute('height', String(height));
      svg.style.cssText = `
        position: fixed;
        left: ${minX}px;
        top: ${minY}px;
        pointer-events: none;
        z-index: 99998;
        overflow: visible;
      `;

      // Arrow marker definition
      if (arrow) {
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
        marker.setAttribute('id', 'demo-arrow');
        marker.setAttribute('markerWidth', '10');
        marker.setAttribute('markerHeight', '10');
        marker.setAttribute('refX', '9');
        marker.setAttribute('refY', '3');
        marker.setAttribute('orient', 'auto');
        marker.setAttribute('markerUnits', 'strokeWidth');

        const arrowPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        arrowPath.setAttribute('d', 'M0,0 L0,6 L9,3 z');
        arrowPath.setAttribute('fill', col);

        marker.appendChild(arrowPath);
        defs.appendChild(marker);
        svg.appendChild(defs);
      }

      // Line element
      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', String(x1));
      line.setAttribute('y1', String(y1));
      line.setAttribute('x2', String(x2));
      line.setAttribute('y2', String(y2));
      line.setAttribute('stroke', col);
      line.setAttribute('stroke-width', String(sw));
      line.setAttribute('stroke-linecap', 'round');
      if (arrow) {
        line.setAttribute('marker-end', 'url(#demo-arrow)');
      }

      svg.appendChild(line);

      const styleSheet = document.createElement('style');
      styleSheet.id = 'demo-swipe-style';
      styleSheet.textContent = `
        @keyframes demoSwipeFade {
          0% { opacity: 1; }
          70% { opacity: 1; }
          100% { opacity: 0; }
        }
        #demo-swipe-trail {
          animation: demoSwipeFade ${dur}ms ease-out forwards;
        }
      `;
      document.head.appendChild(styleSheet);

      document.body.appendChild(svg);

      setTimeout(() => {
        svg.remove();
        styleSheet.remove();
      }, dur);
    },
    { sx: startX, sy: startY, ex: endX, ey: endY, dur: duration, col: color, sw: strokeWidth, arrow: showArrow }
  );

  await page.waitForTimeout(duration);
}

// Usage
test('swipe gesture demo', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/gallery');

  // Show swipe trail then perform swipe
  const startX = 300;
  const startY = 400;
  const endX = 90;
  const endY = 400;

  await showSwipeTrail(page, startX, startY, endX, endY);

  // Perform actual swipe gesture
  await page.mouse.move(startX, startY);
  await page.mouse.down();
  await page.mouse.move(endX, endY, { steps: 10 });
  await page.mouse.up();
});
```

### Keystroke Overlay

Badge-style display for keyboard shortcuts and key presses.

```typescript
// demos/helpers/interaction-feedback.ts

interface KeystrokeOverlayOptions {
  duration?: number;
  position?: 'top' | 'bottom';
  size?: 'small' | 'medium' | 'large';
  theme?: 'dark' | 'light';
}

const keySizes = {
  small: { fontSize: '12px', padding: '4px 8px', gap: '4px' },
  medium: { fontSize: '16px', padding: '8px 12px', gap: '8px' },
  large: { fontSize: '20px', padding: '12px 16px', gap: '10px' },
};

export async function showKeystrokeOverlay(
  page: Page,
  keys: string[],
  options: KeystrokeOverlayOptions = {}
): Promise<void> {
  const { duration = 1500, position = 'bottom', size = 'medium', theme = 'dark' } = options;
  const sizeStyle = keySizes[size];

  const bgColor = theme === 'dark' ? 'rgba(0, 0, 0, 0.85)' : 'rgba(255, 255, 255, 0.95)';
  const textColor = theme === 'dark' ? '#ffffff' : '#1f2937';
  const borderColor = theme === 'dark' ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.15)';

  await page.evaluate(
    ({ keys, dur, pos, sizeStyle, bgColor, textColor, borderColor }) => {
      const container = document.createElement('div');
      container.id = 'demo-keystroke-overlay';
      container.style.cssText = `
        position: fixed;
        ${pos === 'top' ? 'top: 20px' : 'bottom: 20px'};
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: ${sizeStyle.gap};
        z-index: 99998;
        pointer-events: none;
      `;

      keys.forEach((key) => {
        const badge = document.createElement('div');
        badge.style.cssText = `
          background: ${bgColor};
          color: ${textColor};
          border: 1px solid ${borderColor};
          border-radius: 6px;
          padding: ${sizeStyle.padding};
          font-size: ${sizeStyle.fontSize};
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace;
          font-weight: 600;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
          display: flex;
          align-items: center;
          justify-content: center;
          min-width: 2em;
        `;
        badge.textContent = key;
        container.appendChild(badge);
      });

      const styleSheet = document.createElement('style');
      styleSheet.id = 'demo-keystroke-style';
      styleSheet.textContent = `
        @keyframes demoKeystrokeFadeIn {
          from { opacity: 0; transform: translateX(-50%) translateY(10px); }
          to { opacity: 1; transform: translateX(-50%) translateY(0); }
        }
        @keyframes demoKeystrokeFadeOut {
          from { opacity: 1; }
          to { opacity: 0; }
        }
        #demo-keystroke-overlay {
          animation: demoKeystrokeFadeIn 0.2s ease-out;
        }
      `;
      document.head.appendChild(styleSheet);

      document.body.appendChild(container);

      setTimeout(() => {
        container.style.animation = 'demoKeystrokeFadeOut 0.3s ease-out forwards';
        setTimeout(() => {
          container.remove();
          styleSheet.remove();
        }, 300);
      }, dur - 300);
    },
    { keys, dur: duration, pos: position, sizeStyle, bgColor, textColor, borderColor }
  );

  await page.waitForTimeout(duration);
}

// Usage
test('keyboard shortcut demo', async ({ page }) => {
  await page.goto('/editor');

  // Show the shortcut being pressed
  await showKeystrokeOverlay(page, ['⌘', 'Shift', 'S']);
  await page.keyboard.press('Meta+Shift+s');

  await page.waitForTimeout(500);

  // Show Escape key
  await showKeystrokeOverlay(page, ['Esc'], { size: 'small', position: 'top' });
  await page.keyboard.press('Escape');
});
```

### Unified Configuration System

Enable automatic interaction feedback with a single configuration call.

```typescript
// demos/helpers/interaction-feedback.ts

interface InteractionFeedbackConfig {
  showCursor?: boolean;
  showClickRipple?: boolean;
  showTapIndicator?: boolean;
  showSwipeTrail?: boolean;
  showKeystrokeOverlay?: boolean;
  colors?: {
    cursor?: string;
    ripple?: string;
    tap?: string;
    swipe?: string;
  };
  keystrokePosition?: 'top' | 'bottom';
}

export async function enableInteractionFeedback(
  page: Page,
  config: InteractionFeedbackConfig = {}
): Promise<void> {
  const {
    showCursor = true,
    showClickRipple = true,
    showTapIndicator = false,
    showSwipeTrail = false,
    showKeystrokeOverlay = true,
    colors = {},
    keystrokePosition = 'bottom',
  } = config;

  const cursorColor = colors.cursor || 'rgba(59, 130, 246, 0.5)';
  const rippleColor = colors.ripple || 'rgba(59, 130, 246, 0.6)';
  const tapColor = colors.tap || 'rgba(59, 130, 246, 0.8)';
  const swipeColor = colors.swipe || 'rgba(59, 130, 246, 0.8)';

  await page.evaluate(
    ({
      showCursor,
      showClickRipple,
      showTapIndicator,
      cursorColor,
      rippleColor,
      tapColor,
      keystrokePosition,
      showKeystrokeOverlay,
    }) => {
      // Inject styles
      const styleSheet = document.createElement('style');
      styleSheet.id = 'demo-interaction-styles';
      styleSheet.textContent = `
        @keyframes demoRippleExpand {
          0% { width: 0; height: 0; opacity: 1; }
          100% { width: 100px; height: 100px; opacity: 0; }
        }
        @keyframes demoTapPulse {
          0% { transform: translate(-50%, -50%) scale(0.8); opacity: 1; }
          50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.8; }
          100% { transform: translate(-50%, -50%) scale(1.0); opacity: 0; }
        }
      `;
      document.head.appendChild(styleSheet);

      // Cursor
      if (showCursor) {
        const cursor = document.createElement('div');
        cursor.id = 'demo-auto-cursor';
        cursor.style.cssText = `
          position: fixed;
          width: 20px;
          height: 20px;
          background: ${cursorColor};
          border: 2px solid ${cursorColor.replace('0.5', '1')};
          border-radius: 50%;
          z-index: 99999;
          pointer-events: none;
          transform: translate(-50%, -50%);
          transition: transform 0.1s ease-out, background 0.1s ease-out;
        `;
        document.body.appendChild(cursor);

        document.addEventListener('mousemove', (e) => {
          cursor.style.left = e.clientX + 'px';
          cursor.style.top = e.clientY + 'px';
        });
      }

      // Click/tap handlers
      const handleClick = (e: MouseEvent) => {
        if (showClickRipple) {
          const ripple = document.createElement('div');
          ripple.className = 'demo-auto-ripple';
          ripple.style.cssText = `
            position: fixed;
            left: ${e.clientX}px;
            top: ${e.clientY}px;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: radial-gradient(circle, ${rippleColor} 0%, transparent 70%);
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 99998;
            animation: demoRippleExpand 600ms ease-out forwards;
          `;
          document.body.appendChild(ripple);
          setTimeout(() => ripple.remove(), 600);
        }
      };

      const handleTouch = (e: TouchEvent) => {
        if (showTapIndicator && e.touches.length > 0) {
          const touch = e.touches[0];
          const tap = document.createElement('div');
          tap.className = 'demo-auto-tap';
          tap.style.cssText = `
            position: fixed;
            left: ${touch.clientX}px;
            top: ${touch.clientY}px;
            width: 60px;
            height: 60px;
            border: 3px solid ${tapColor};
            border-radius: 50%;
            transform: translate(-50%, -50%) scale(0.8);
            pointer-events: none;
            z-index: 99998;
            box-sizing: border-box;
            animation: demoTapPulse 500ms ease-out forwards;
          `;
          document.body.appendChild(tap);
          setTimeout(() => tap.remove(), 500);
        }
      };

      document.addEventListener('click', handleClick);
      document.addEventListener('touchstart', handleTouch);

      // Keyboard handler
      if (showKeystrokeOverlay) {
        const activeKeys = new Set<string>();
        let keystrokeTimeout: ReturnType<typeof setTimeout> | null = null;

        const formatKey = (key: string): string => {
          const keyMap: Record<string, string> = {
            Meta: '⌘',
            Control: 'Ctrl',
            Alt: '⌥',
            Shift: '⇧',
            Enter: '↵',
            Escape: 'Esc',
            ArrowUp: '↑',
            ArrowDown: '↓',
            ArrowLeft: '←',
            ArrowRight: '→',
            Backspace: '⌫',
            Tab: '⇥',
            ' ': 'Space',
          };
          return keyMap[key] || key.toUpperCase();
        };

        const showKeys = () => {
          // Remove existing
          const existing = document.getElementById('demo-auto-keystroke');
          if (existing) existing.remove();

          if (activeKeys.size === 0) return;

          const container = document.createElement('div');
          container.id = 'demo-auto-keystroke';
          container.style.cssText = `
            position: fixed;
            ${keystrokePosition === 'top' ? 'top: 20px' : 'bottom: 20px'};
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 8px;
            z-index: 99998;
            pointer-events: none;
          `;

          activeKeys.forEach((key) => {
            const badge = document.createElement('div');
            badge.style.cssText = `
              background: rgba(0, 0, 0, 0.85);
              color: white;
              border: 1px solid rgba(255, 255, 255, 0.2);
              border-radius: 6px;
              padding: 8px 12px;
              font-size: 16px;
              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace;
              font-weight: 600;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            `;
            badge.textContent = formatKey(key);
            container.appendChild(badge);
          });

          document.body.appendChild(container);
        };

        document.addEventListener('keydown', (e) => {
          activeKeys.add(e.key);
          showKeys();

          if (keystrokeTimeout) clearTimeout(keystrokeTimeout);
          keystrokeTimeout = setTimeout(() => {
            activeKeys.clear();
            const existing = document.getElementById('demo-auto-keystroke');
            if (existing) existing.remove();
          }, 1500);
        });

        document.addEventListener('keyup', (e) => {
          // Keep showing for modifier combos
          if (!e.metaKey && !e.ctrlKey && !e.altKey && !e.shiftKey) {
            if (keystrokeTimeout) clearTimeout(keystrokeTimeout);
            keystrokeTimeout = setTimeout(() => {
              activeKeys.clear();
              const existing = document.getElementById('demo-auto-keystroke');
              if (existing) existing.remove();
            }, 1500);
          }
        });
      }
    },
    {
      showCursor,
      showClickRipple,
      showTapIndicator,
      cursorColor,
      rippleColor,
      tapColor,
      keystrokePosition,
      showKeystrokeOverlay,
    }
  );
}

export async function disableInteractionFeedback(page: Page): Promise<void> {
  await page.evaluate(() => {
    // Remove all feedback elements
    const elements = [
      'demo-auto-cursor',
      'demo-auto-keystroke',
      'demo-interaction-styles',
    ];
    elements.forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.remove();
    });

    // Remove ripples and taps
    document.querySelectorAll('.demo-auto-ripple, .demo-auto-tap').forEach((el) => el.remove());
  });
}
```

---

## Scenario Recording System

Automatic documentation of demo actions for reproducibility.

### Scenario Recorder Helper

```typescript
// demos/helpers/scenario-recorder.ts
import { Page } from '@playwright/test';

interface RecordedAction {
  timestamp: number;
  elapsed: number;
  type: 'navigate' | 'click' | 'fill' | 'select' | 'check' | 'wait' | 'overlay' | 'scroll';
  selector?: string;
  value?: string;
  description?: string;
}

interface ScenarioRecording {
  startTime: number;
  actions: RecordedAction[];
  stop: () => Promise<RecordedAction[]>;
}

interface ScenarioDocOptions {
  title: string;
  author?: string;
  audience?: string;
  includeTimestamps?: boolean;
}

export async function enableScenarioRecording(page: Page): Promise<ScenarioRecording> {
  const startTime = Date.now();
  const actions: RecordedAction[] = [];

  // Intercept page actions
  page.on('framenavigated', (frame) => {
    if (frame === page.mainFrame()) {
      actions.push({
        timestamp: Date.now(),
        elapsed: Date.now() - startTime,
        type: 'navigate',
        value: frame.url(),
        description: `Navigate to ${new URL(frame.url()).pathname}`,
      });
    }
  });

  // Create action logger
  const logAction = (action: Omit<RecordedAction, 'timestamp' | 'elapsed'>) => {
    actions.push({
      ...action,
      timestamp: Date.now(),
      elapsed: Date.now() - startTime,
    });
  };

  // Expose logger for manual annotations
  await page.exposeFunction('__recordAction', (type: string, description: string) => {
    logAction({ type: type as RecordedAction['type'], description });
  });

  return {
    startTime,
    actions,
    stop: async () => {
      return [...actions];
    },
  };
}

export function generateScenarioDoc(
  actions: RecordedAction[],
  options: ScenarioDocOptions
): string {
  const { title, author = 'Director', audience, includeTimestamps = true } = options;
  const duration = actions.length > 0
    ? Math.round(actions[actions.length - 1].elapsed / 1000)
    : 0;

  let doc = `# Scenario: ${title}\n\n`;
  doc += `> Auto-generated by ${author}\n\n`;
  doc += `| Property | Value |\n`;
  doc += `|----------|-------|\n`;
  doc += `| Generated | ${new Date().toISOString()} |\n`;
  doc += `| Duration | ${duration}s |\n`;
  doc += `| Total Steps | ${actions.length} |\n`;
  if (audience) {
    doc += `| Audience | ${audience} |\n`;
  }
  doc += `\n---\n\n`;
  doc += `## Steps\n\n`;

  actions.forEach((action, index) => {
    const time = includeTimestamps
      ? `**${formatTime(action.elapsed)}** `
      : '';
    const desc = action.description || formatActionDescription(action);
    doc += `${index + 1}. ${time}${desc}\n`;
  });

  return doc;
}

function formatTime(ms: number): string {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

function formatActionDescription(action: RecordedAction): string {
  switch (action.type) {
    case 'navigate':
      return `Navigate to \`${action.value}\``;
    case 'click':
      return `Click on \`${action.selector}\``;
    case 'fill':
      return `Fill \`${action.selector}\` with "${action.value}"`;
    case 'select':
      return `Select "${action.value}" in \`${action.selector}\``;
    case 'check':
      return `Check \`${action.selector}\``;
    case 'wait':
      return `Wait ${action.value}ms`;
    case 'overlay':
      return `Show overlay: "${action.value}"`;
    case 'scroll':
      return `Scroll to \`${action.selector}\``;
    default:
      return action.description || 'Unknown action';
  }
}
```

### Enhanced Demo Test with Recording

```typescript
// demos/specs/demo-checkout-recorded.spec.ts
import { test, expect } from '@playwright/test';
import { enableScenarioRecording, generateScenarioDoc } from '../helpers/scenario-recorder';
import { showOverlay } from '../helpers/overlay';
import fs from 'fs/promises';
import path from 'path';

test.describe('Demo: Checkout Flow (Recorded)', () => {
  test('complete checkout with auto-documentation', async ({ page }, testInfo) => {
    const recorder = await enableScenarioRecording(page);

    // === Scene 1: Product Page ===
    await page.goto('/products/sample-a');
    await page.waitForLoadState('networkidle');

    await showOverlay(page, 'Adding product to cart', 2000);
    // Manual annotation
    await page.evaluate(() => {
      (window as any).__recordAction('overlay', 'Show: Adding product to cart');
    });

    await page.getByRole('button', { name: 'Add to Cart' }).click();
    await page.evaluate(() => {
      (window as any).__recordAction('click', 'Click "Add to Cart" button');
    });

    // ... more actions ...

    // === Generate Documentation ===
    const actions = await recorder.stop();
    const markdown = generateScenarioDoc(actions, {
      title: 'Checkout Flow Demo',
      audience: 'New users',
    });

    // Save alongside video
    const scenarioDir = path.join(__dirname, '../scenarios');
    await fs.mkdir(scenarioDir, { recursive: true });
    await fs.writeFile(
      path.join(scenarioDir, `${testInfo.title.replace(/\s+/g, '_')}.md`),
      markdown
    );
  });
});
```

### Wrapper Functions for Auto-Logging

```typescript
// demos/helpers/recorded-actions.ts
import { Page, Locator } from '@playwright/test';

export function createRecordedActions(page: Page) {
  return {
    async click(locator: Locator, description?: string) {
      const selector = await locator.evaluate(el => {
        // Get a readable selector
        return el.getAttribute('data-testid')
          || el.getAttribute('aria-label')
          || el.tagName.toLowerCase();
      });
      await page.evaluate(
        ({ sel, desc }) => (window as any).__recordAction?.('click', desc || `Click ${sel}`),
        { sel: selector, desc: description }
      );
      await locator.click();
    },

    async fill(locator: Locator, value: string, description?: string) {
      const label = await locator.evaluate(el => {
        const id = el.getAttribute('id');
        if (id) {
          const label = document.querySelector(`label[for="${id}"]`);
          return label?.textContent || id;
        }
        return el.getAttribute('name') || 'field';
      });
      await page.evaluate(
        ({ lbl, val, desc }) =>
          (window as any).__recordAction?.('fill', desc || `Fill "${lbl}" with "${val}"`),
        { lbl: label, val: value, desc: description }
      );
      await locator.fill(value);
    },

    async navigate(url: string, description?: string) {
      await page.evaluate(
        ({ url, desc }) => (window as any).__recordAction?.('navigate', desc || `Navigate to ${url}`),
        { url, desc: description }
      );
      await page.goto(url);
    },
  };
}

// Usage
test('demo with recorded actions', async ({ page }) => {
  const recorder = await enableScenarioRecording(page);
  const actions = createRecordedActions(page);

  await actions.navigate('/dashboard', 'Open dashboard');
  await actions.click(page.getByRole('button', { name: 'Create' }), 'Click create button');
  await actions.fill(page.getByLabel('Title'), 'My Document', 'Enter document title');

  const recorded = await recorder.stop();
  // All actions are automatically documented
});
```

---

### Device-Specific Presets

Pre-configured settings for common demo scenarios.

```typescript
// demos/helpers/interaction-presets.ts
import { Page } from '@playwright/test';
import { enableInteractionFeedback, InteractionFeedbackConfig } from './interaction-feedback';

export const InteractionPresets: Record<string, InteractionFeedbackConfig> = {
  desktop: {
    showCursor: true,
    showClickRipple: true,
    showTapIndicator: false,
    showSwipeTrail: false,
    showKeystrokeOverlay: true,
    keystrokePosition: 'bottom',
  },
  mobile: {
    showCursor: false,
    showClickRipple: false,
    showTapIndicator: true,
    showSwipeTrail: true,
    showKeystrokeOverlay: false,
  },
  tablet: {
    showCursor: false,
    showClickRipple: false,
    showTapIndicator: true,
    showSwipeTrail: true,
    showKeystrokeOverlay: true,
    keystrokePosition: 'top',
  },
};

export async function enableDesktopFeedback(page: Page): Promise<void> {
  await enableInteractionFeedback(page, InteractionPresets.desktop);
}

export async function enableMobileFeedback(page: Page): Promise<void> {
  await enableInteractionFeedback(page, InteractionPresets.mobile);
}

export async function enableTabletFeedback(page: Page): Promise<void> {
  await enableInteractionFeedback(page, InteractionPresets.tablet);
}
```

### Usage Examples

#### Desktop Demo Example

```typescript
// demos/specs/demo-desktop-workflow.spec.ts
import { test, expect } from '@playwright/test';
import { enableDesktopFeedback, disableInteractionFeedback } from '../helpers/interaction-presets';
import { showOverlay } from '../helpers/overlay';

test.describe('Demo: Desktop Workflow with Visual Feedback', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/dashboard');
    await enableDesktopFeedback(page);
  });

  test.afterEach(async ({ page }) => {
    await disableInteractionFeedback(page);
  });

  test('file management with keyboard shortcuts', async ({ page }) => {
    await showOverlay(page, 'Let\'s create a new document', 2000);

    // Keyboard shortcut - auto-displayed by feedback system
    await page.keyboard.press('Meta+n');
    await expect(page.getByRole('dialog', { name: 'New Document' })).toBeVisible();

    // Click interaction - auto-ripple displayed
    await page.getByRole('textbox', { name: 'Title' }).fill('My Document');
    await page.getByRole('button', { name: 'Create' }).click();

    await showOverlay(page, 'Document created!', 2000);

    // Save with shortcut
    await page.keyboard.press('Meta+s');
    await expect(page.getByText('Saved')).toBeVisible();
  });
});
```

#### Mobile Demo Example

```typescript
// demos/specs/demo-mobile-gestures.spec.ts
import { test, expect, devices } from '@playwright/test';
import { enableMobileFeedback, disableInteractionFeedback } from '../helpers/interaction-presets';
import { showSwipeTrail, showTapIndicator } from '../helpers/interaction-feedback';
import { showOverlay } from '../helpers/overlay';

test.describe('Demo: Mobile App with Touch Feedback', () => {
  test.use({ ...devices['iPhone 14 Pro'] });

  test.beforeEach(async ({ page }) => {
    await page.goto('/mobile/gallery');
    await enableMobileFeedback(page);
  });

  test.afterEach(async ({ page }) => {
    await disableInteractionFeedback(page);
  });

  test('swipe through image gallery', async ({ page }) => {
    await showOverlay(page, 'Swipe to browse images', 2000);

    // Get viewport dimensions
    const viewport = page.viewportSize();
    if (!viewport) return;

    const centerY = viewport.height / 2;
    const startX = viewport.width * 0.8;
    const endX = viewport.width * 0.2;

    // Show swipe trail then perform gesture
    await showSwipeTrail(page, startX, centerY, endX, centerY);

    // Perform swipe
    await page.mouse.move(startX, centerY);
    await page.mouse.down();
    await page.mouse.move(endX, centerY, { steps: 20 });
    await page.mouse.up();

    await page.waitForTimeout(500);

    // Tap on image to view full screen
    const image = page.getByTestId('gallery-image-2');
    const box = await image.boundingBox();
    if (box) {
      await showTapIndicator(page, box.x + box.width / 2, box.y + box.height / 2);
      await image.tap();
    }

    await expect(page.getByTestId('fullscreen-viewer')).toBeVisible();
    await showOverlay(page, 'Full screen view', 1500);
  });
});
```

---

## Page Transition Wait Pattern

### Stable Transition Wait

```typescript
// demos/helpers/navigation.ts
import { Page, expect } from '@playwright/test';

export async function waitForPageReady(page: Page): Promise<void> {
  // DOM load complete
  await page.waitForLoadState('domcontentloaded');
  // Network idle
  await page.waitForLoadState('networkidle');
  // Additional stabilization wait
  await page.waitForTimeout(300);
}

export async function navigateAndWait(
  page: Page,
  action: () => Promise<void>,
  expectedUrl: string | RegExp
): Promise<void> {
  await action();
  await page.waitForURL(expectedUrl);
  await waitForPageReady(page);
}

// Usage
test('flow with page transitions', async ({ page }) => {
  await page.goto('/');

  await navigateAndWait(
    page,
    () => page.click('[data-testid="login-link"]'),
    '**/login'
  );

  // Login form is fully displayed
  await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();
});
```

---

## Test Data Factory

### Preparing Demo Data

```typescript
// demos/helpers/data.ts
export const DemoData = {
  user: {
    email: 'demo@example.com',
    password: 'DemoPass123',
    name: 'Demo User',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Demo',
  },

  address: {
    postalCode: '150-0001',
    country: 'Japan',
    city: 'Tokyo',
    street: '1-2-3 Shibuya',
    building: 'Demo Building 101',
  },

  product: {
    name: 'Sample Product A',
    price: 39.80,
    description: 'High quality sample product.',
    image: '/fixtures/product-a.jpg',
  },

  creditCard: {
    number: '4242 4242 4242 4242',
    expiry: '12/25',
    cvc: '123',
    name: 'DEMO USER',
  },

  // Generate random but consistent data
  generateOrder(): { id: string; date: string; total: number } {
    return {
      id: 'ORD-2024-0001',
      date: 'January 15, 2024',
      total: 43.78, // Product price + tax
    };
  },
};

// Seed data setup
export async function seedDemoData(page: Page): Promise<void> {
  await page.evaluate((data) => {
    // Set demo data to LocalStorage
    localStorage.setItem('demo_user', JSON.stringify(data.user));
  }, DemoData);
}
```

---

## Persona-Aware Demo Recording

### Echo Integration Patterns

When Echo provides persona behavior profiles, use these patterns to create believable persona-specific demos.

#### Persona Configuration Helper

```typescript
// demos/helpers/persona.ts
import { Page } from '@playwright/test';

export interface PersonaBehavior {
  name: string;
  slowMo: number;
  readingMultiplier: number;
  hesitationPoints: string[];
  hesitationDuration: number;
  overlayDuration: number;
  typingSpeed: 'fast' | 'normal' | 'slow' | 'hunt-and-peck';
}

export const PersonaBehaviors: Record<string, PersonaBehavior> = {
  senior: {
    name: 'Senior',
    slowMo: 800,
    readingMultiplier: 1.5,
    hesitationPoints: ['form-submit', 'payment', 'terms', 'navigation'],
    hesitationDuration: 500,
    overlayDuration: 3000,
    typingSpeed: 'slow',
  },
  newbie: {
    name: 'Newbie',
    slowMo: 650,
    readingMultiplier: 1.3,
    hesitationPoints: ['navigation', 'form-fields', 'confirmation', 'unknown-icons'],
    hesitationDuration: 400,
    overlayDuration: 2500,
    typingSpeed: 'normal',
  },
  powerUser: {
    name: 'Power User',
    slowMo: 350,
    readingMultiplier: 0.8,
    hesitationPoints: [],
    hesitationDuration: 0,
    overlayDuration: 1500,
    typingSpeed: 'fast',
  },
  mobileUser: {
    name: 'Mobile User',
    slowMo: 500,
    readingMultiplier: 1.0,
    hesitationPoints: ['small-buttons', 'forms', 'dropdown'],
    hesitationDuration: 200,
    overlayDuration: 2000,
    typingSpeed: 'normal',
  },
  skeptic: {
    name: 'Skeptic',
    slowMo: 550,
    readingMultiplier: 1.4,
    hesitationPoints: ['payment', 'personal-info', 'permissions', 'terms'],
    hesitationDuration: 600,
    overlayDuration: 2500,
    typingSpeed: 'normal',
  },
  distracted: {
    name: 'Distracted User',
    slowMo: 600,
    readingMultiplier: 0.9,
    hesitationPoints: ['long-forms', 'multi-step'],
    hesitationDuration: 400,
    overlayDuration: 2000,
    typingSpeed: 'normal',
  },
};

// Get persona from environment or default
export function getPersona(name?: string): PersonaBehavior {
  const personaName = name || process.env.DEMO_PERSONA || 'newbie';
  return PersonaBehaviors[personaName.toLowerCase()] || PersonaBehaviors.newbie;
}
```

#### Persona-Aware Wait Helper

```typescript
// demos/helpers/persona-wait.ts
import { Page } from '@playwright/test';
import { PersonaBehavior, getPersona } from './persona';

export async function personaWait(
  page: Page,
  baseTime: number,
  persona?: PersonaBehavior
): Promise<void> {
  const p = persona || getPersona();
  const adjustedTime = Math.round(baseTime * p.readingMultiplier);
  await page.waitForTimeout(adjustedTime);
}

export async function hesitate(
  page: Page,
  action: string,
  persona?: PersonaBehavior
): Promise<void> {
  const p = persona || getPersona();

  // Check if this action triggers hesitation for this persona
  const shouldHesitate = p.hesitationPoints.some(
    (point) => action.toLowerCase().includes(point.toLowerCase())
  );

  if (shouldHesitate && p.hesitationDuration > 0) {
    await page.waitForTimeout(p.hesitationDuration);
  }
}

export async function showPersonaOverlay(
  page: Page,
  message: string,
  persona?: PersonaBehavior
): Promise<void> {
  const p = persona || getPersona();

  await page.evaluate(
    ({ msg, dur }) => {
      const overlay = document.createElement('div');
      overlay.id = 'demo-overlay';
      overlay.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.85);
        color: white;
        padding: 16px 32px;
        border-radius: 8px;
        font-size: 18px;
        z-index: 99999;
      `;
      overlay.textContent = msg;
      document.body.appendChild(overlay);
      setTimeout(() => overlay.remove(), dur);
    },
    { msg: message, dur: p.overlayDuration }
  );

  await page.waitForTimeout(p.overlayDuration);
}
```

#### Persona-Aware Typing Helper

```typescript
// demos/helpers/persona-typing.ts
import { Page } from '@playwright/test';
import { PersonaBehavior, getPersona } from './persona';

const typingSpeeds = {
  fast: 30,
  normal: 60,
  slow: 120,
  'hunt-and-peck': 250,
};

export async function personaFill(
  page: Page,
  selector: string,
  value: string,
  persona?: PersonaBehavior
): Promise<void> {
  const p = persona || getPersona();
  const charDelay = typingSpeeds[p.typingSpeed];

  // Clear first
  await page.locator(selector).clear();

  // Type character by character for realistic effect
  for (const char of value) {
    await page.locator(selector).pressSequentially(char, { delay: charDelay });
  }

  // Post-input pause (persona reads what they typed)
  await page.waitForTimeout(Math.round(200 * p.readingMultiplier));
}

// Label-based version
export async function personaFillByLabel(
  page: Page,
  label: string,
  value: string,
  persona?: PersonaBehavior
): Promise<void> {
  const p = persona || getPersona();
  const charDelay = typingSpeeds[p.typingSpeed];

  const input = page.getByLabel(label);
  await input.clear();

  for (const char of value) {
    await input.pressSequentially(char, { delay: charDelay });
  }

  await page.waitForTimeout(Math.round(200 * p.readingMultiplier));
}
```

### Persona Demo Test Example

```typescript
// demos/specs/demo-checkout-persona.spec.ts
import { test, expect } from '@playwright/test';
import { getPersona, PersonaBehavior } from '../helpers/persona';
import { hesitate, personaWait, showPersonaOverlay } from '../helpers/persona-wait';
import { personaFillByLabel } from '../helpers/persona-typing';
import { DemoData } from '../helpers/data';

test.describe('Demo: Checkout Flow (Persona-Aware)', () => {
  let persona: PersonaBehavior;

  test.beforeAll(() => {
    // Get persona from environment: DEMO_PERSONA=senior npx playwright test
    persona = getPersona(process.env.DEMO_PERSONA);
    console.log(`Recording demo for persona: ${persona.name}`);
  });

  test.beforeEach(async ({ page, context }) => {
    // Pre-authenticate
    await context.request.post('/api/auth/login', {
      data: { email: DemoData.user.email, password: DemoData.user.password },
    });
  });

  test('complete checkout with persona behavior', async ({ page }) => {
    // === Scene 1: Product Page ===
    await page.goto('/products/sample-a');
    await page.waitForLoadState('networkidle');

    await showPersonaOverlay(page, 'Let\'s complete a purchase', persona);
    await personaWait(page, 1000, persona);

    // === Scene 2: Add to Cart ===
    await hesitate(page, 'navigation', persona);
    await page.getByRole('button', { name: 'Add to Cart' }).click();

    await expect(page.getByText('Added to cart')).toBeVisible();
    await personaWait(page, 800, persona);

    // === Scene 3: Cart Review ===
    await page.getByTestId('cart-icon').click();
    await page.waitForURL('**/cart');

    await showPersonaOverlay(page, 'Checking cart items', persona);
    await personaWait(page, 1200, persona);

    // === Scene 4: Checkout ===
    await hesitate(page, 'form-submit', persona);
    await page.getByRole('button', { name: 'Proceed to Checkout' }).click();
    await page.waitForURL('**/checkout');

    // Shipping address - hesitation for form fields
    await hesitate(page, 'form-fields', persona);
    await personaFillByLabel(page, 'Address', DemoData.address.street, persona);
    await personaFillByLabel(page, 'City', DemoData.address.city, persona);

    // === Scene 5: Payment ===
    await showPersonaOverlay(page, 'Entering payment details', persona);

    // Significant hesitation at payment for seniors/skeptics
    await hesitate(page, 'payment', persona);
    await personaFillByLabel(page, 'Card Number', DemoData.creditCard.number, persona);
    await personaFillByLabel(page, 'Expiry', DemoData.creditCard.expiry, persona);
    await personaFillByLabel(page, 'CVV', DemoData.creditCard.cvc, persona);

    // === Scene 6: Terms & Submit ===
    await hesitate(page, 'terms', persona);
    await page.getByLabel('I agree to the terms').check();
    await personaWait(page, 500, persona);

    // Final submit hesitation
    await hesitate(page, 'form-submit', persona);
    await page.getByRole('button', { name: 'Confirm Order' }).click();

    // === Scene 7: Success ===
    await page.waitForURL('**/order/complete');
    await expect(page.getByText('Thank you for your order')).toBeVisible();

    await showPersonaOverlay(page, 'Purchase complete! 🎉', persona);
  });
});
```

### Playwright Config for Persona Demos

```typescript
// playwright.config.persona.ts
import { defineConfig, devices } from '@playwright/test';
import { PersonaBehaviors } from './demos/helpers/persona';

// Get persona from environment
const personaName = process.env.DEMO_PERSONA || 'newbie';
const persona = PersonaBehaviors[personaName.toLowerCase()];

export default defineConfig({
  testDir: './demos/specs',
  timeout: 180000, // 3 minutes for slow personas
  retries: 0,
  workers: 1,

  use: {
    launchOptions: {
      slowMo: persona?.slowMo || 500,
    },
    video: {
      mode: 'on',
      size: { width: 1280, height: 720 },
    },
    viewport: { width: 1280, height: 720 },
    trace: 'off',
  },

  projects: [
    {
      name: `demo-${personaName}`,
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  outputDir: `demos/output/${personaName}`,
});
```

### Running Persona Demos

```bash
# Record demo for different personas
DEMO_PERSONA=senior npx playwright test --config=playwright.config.persona.ts
DEMO_PERSONA=newbie npx playwright test --config=playwright.config.persona.ts
DEMO_PERSONA=powerUser npx playwright test --config=playwright.config.persona.ts

# Output files will be in:
# demos/output/senior/
# demos/output/newbie/
# demos/output/poweruser/
```

---

## Complete Demo Example

### E-Commerce Checkout Demo

```typescript
// demos/specs/demo-checkout.spec.ts
import { test, expect } from '@playwright/test';
import { showOverlay, showStep, showSuccess } from '../helpers/overlay';
import { smoothScrollTo } from '../helpers/scroll';
import { DemoData, seedDemoData } from '../helpers/data';

test.describe('Demo: Product Purchase Flow', () => {
  test.beforeEach(async ({ page, context }) => {
    // Login via API
    await context.request.post('/api/auth/login', {
      data: { email: DemoData.user.email, password: DemoData.user.password },
    });
    await seedDemoData(page);
  });

  test('add product to cart and complete purchase', async ({ page }) => {
    // === Scene 1: Product Page ===
    await page.goto('/products/sample-a');
    await page.waitForLoadState('networkidle');

    await showStep(page, 1, 5, 'Select product');
    await page.waitForTimeout(1500);

    // === Scene 2: Add to Cart ===
    await showOverlay(page, 'Adding to cart', 1500);
    await page.getByRole('button', { name: 'Add to Cart' }).click();

    await expect(page.getByText('Added to cart')).toBeVisible();
    await page.waitForTimeout(1000);

    // === Scene 3: Cart Confirmation ===
    await showStep(page, 2, 5, 'Check cart');
    await page.getByTestId('cart-icon').click();
    await page.waitForURL('**/cart');

    await expect(page.getByText(DemoData.product.name)).toBeVisible();
    await page.waitForTimeout(1500);

    // === Scene 4: Checkout ===
    await showStep(page, 3, 5, 'Proceed to checkout');
    await page.getByRole('button', { name: 'Proceed to Checkout' }).click();
    await page.waitForURL('**/checkout');

    // Shipping address confirmation
    await showStep(page, 4, 5, 'Confirm shipping address');
    await expect(page.getByText(DemoData.address.city)).toBeVisible();
    await page.waitForTimeout(1000);

    // Payment method
    await smoothScrollTo(page, '#payment-section');
    await page.getByLabel('Credit Card').check();
    await page.waitForTimeout(500);

    // === Scene 5: Order Confirmation ===
    await showStep(page, 5, 5, 'Confirm order');
    await page.getByRole('button', { name: 'Confirm Order' }).click();

    // Complete screen
    await page.waitForURL('**/order/complete');
    await expect(page.getByText('Thank you for your order')).toBeVisible();

    await showSuccess(page, 'Purchase complete! 🎉', 3000);
  });
});
```
