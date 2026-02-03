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
