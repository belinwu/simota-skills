# Visual Verification

**Purpose:** Playwright screenshot capture and mockup-vs-implementation comparison methodology.
**Read when:** You need to verify the visual fidelity of generated code against the original mockup.

## Contents
- Verification Workflow
- Playwright Screenshot Setup
- Comparison Strategy
- Difference Report Format
- Iteration Rules

---

## Verification Workflow

```
Generate Code → Serve Locally → Capture Screenshot → Compare with Mockup → Report Differences
     │                                                                           │
     │                              ┌──────────────┐                             │
     └──────────────────────────────│  Max 3 Loops  │─────────────────────────────┘
                                    └──────────────┘
```

### Prerequisites

- Node.js installed
- Playwright available (`npx playwright install chromium` if needed)
- Generated HTML file ready to serve

---

## Playwright Screenshot Setup

### Basic Screenshot Script

```javascript
// capture-screenshot.js
const { chromium } = require('playwright');
const path = require('path');

async function captureScreenshot(htmlPath, outputPath, options = {}) {
  const {
    width = 1440,
    height = 900,
    fullPage = true,
    deviceScaleFactor = 2,
  } = options;

  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor,
  });
  const page = await context.newPage();

  // Load the HTML file
  await page.goto(`file://${path.resolve(htmlPath)}`);

  // Wait for fonts and images to load
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(500); // Allow render stabilization

  // Capture
  await page.screenshot({
    path: outputPath,
    fullPage,
  });

  await browser.close();
  console.log(`Screenshot saved: ${outputPath}`);
}

// Usage
captureScreenshot(
  process.argv[2] || './index.html',
  process.argv[3] || './screenshot.png'
);
```

### Multi-Viewport Capture

```javascript
// capture-responsive.js
const { chromium } = require('playwright');
const path = require('path');

const VIEWPORTS = [
  { name: 'mobile', width: 375, height: 812 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1440, height: 900 },
];

async function captureAllViewports(htmlPath, outputDir) {
  const browser = await chromium.launch();

  for (const vp of VIEWPORTS) {
    const context = await browser.newContext({
      viewport: { width: vp.width, height: vp.height },
      deviceScaleFactor: 2,
    });
    const page = await context.newPage();
    await page.goto(`file://${path.resolve(htmlPath)}`);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(500);

    await page.screenshot({
      path: path.join(outputDir, `screenshot-${vp.name}.png`),
      fullPage: true,
    });

    await context.close();
    console.log(`Captured: ${vp.name} (${vp.width}x${vp.height})`);
  }

  await browser.close();
}

captureAllViewports(
  process.argv[2] || './index.html',
  process.argv[3] || './'
);
```

### Section-Level Capture

```javascript
// capture-section.js
const { chromium } = require('playwright');

async function captureSection(htmlPath, selector, outputPath) {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2,
  });

  await page.goto(`file://${require('path').resolve(htmlPath)}`);
  await page.waitForLoadState('networkidle');

  const element = await page.$(selector);
  if (element) {
    await element.screenshot({ path: outputPath });
    console.log(`Section captured: ${selector} -> ${outputPath}`);
  } else {
    console.error(`Selector not found: ${selector}`);
  }

  await browser.close();
}
```

---

## Comparison Strategy

### Dual Approach: Programmatic + AI Vision

Use both programmatic pixel comparison and AI vision analysis for comprehensive verification.

#### 1. Programmatic Comparison (pixelmatch)

Generate a diff image to visually highlight discrepancies:

```javascript
// compare-images.js
const pixelmatch = require('pixelmatch');
const { PNG } = require('pngjs');
const fs = require('fs');

function compareImages(mockupPath, screenshotPath, diffPath) {
  const mockup = PNG.sync.read(fs.readFileSync(mockupPath));
  const screenshot = PNG.sync.read(fs.readFileSync(screenshotPath));

  // Images must be same dimensions — resize screenshot to match mockup if needed
  const { width, height } = mockup;
  const diff = new PNG({ width, height });

  const mismatchedPixels = pixelmatch(
    mockup.data, screenshot.data, diff.data,
    width, height,
    { threshold: 0.1 }  // 0 = strict, 1 = lenient
  );

  fs.writeFileSync(diffPath, PNG.sync.write(diff));
  const totalPixels = width * height;
  const matchRatio = 1 - (mismatchedPixels / totalPixels);
  console.log(`Match: ${(matchRatio * 100).toFixed(1)}% (${mismatchedPixels} pixels differ)`);
  return { mismatchedPixels, matchRatio, totalPixels };
}
```

#### 2. AI Vision Comparison

Feed the diff image + originals to Claude Vision for semantic analysis:

```
以下の3つの画像を比較してください:
1枚目: オリジナルのモックアップ画像
2枚目: 実装から撮影したスクリーンショット
3枚目: pixelmatchで生成した差分画像（赤い部分が差異箇所）

以下の観点で差異を特定してください:
1. レイアウト（要素の配置、サイズ、間隔）
2. 色（背景色、テキスト色、アクセント色）
3. タイポグラフィ（フォントサイズ、ウェイト、行間）
4. コンポーネント（ボタン、カード、アイコンの形状）
5. 全体的な印象

差分画像の赤い部分に注目し、各差異にCSSの修正方法を具体的に提示してください。

各差異に優先度を付けてください:
- CRITICAL: 明らかに異なる（レイアウト崩れ、色違い）
- MODERATE: 目立つ差異（余白の違い、フォントサイズ）
- MINOR: 微細な差異（1-2pxの違い、わずかな色味差）

忠実度スコア（0-100%）を推定してください。
```

The diff image from pixelmatch gives the AI model precise pixel-level guidance on where to look, significantly improving fix accuracy.

### Comparison Dimensions

| Dimension | Weight | What to Check |
|-----------|--------|---------------|
| Layout | 30% | Element positions, sizes, alignment, grid structure |
| Color | 25% | Background, text, accent, border colors |
| Typography | 20% | Font sizes, weights, line heights, letter spacing |
| Spacing | 15% | Margins, paddings, gaps between elements |
| Components | 10% | Button shapes, border radius, shadows, icons |

### Scoring Guide

| Score | Interpretation | Action |
|-------|---------------|--------|
| 95-100% | Excellent fidelity | Deliver, note any MINOR differences |
| 90-94% | Good fidelity | Fix CRITICAL items if any, deliver |
| 80-89% | Acceptable with issues | One refinement iteration |
| 70-79% | Needs improvement | Two refinement iterations |
| <70% | Major rework needed | Re-analyze mockup, restart COMPOSE |

---

## Difference Report Format

### Template

```markdown
## Visual Comparison Report

### Overview
- **Mockup**: [mockup filename]
- **Screenshot**: [screenshot filename]
- **Viewport**: [width x height]
- **Fidelity Score**: [X%]
- **Iteration**: [1/3]

### Differences Found

#### CRITICAL
| # | Area | Expected | Actual | Fix |
|---|------|----------|--------|-----|
| 1 | Hero background | Dark gradient | Solid color | Add gradient CSS |

#### MODERATE
| # | Area | Expected | Actual | Fix |
|---|------|----------|--------|-----|
| 1 | Section heading | ~36px | 30px | Increase font-size to 2.25rem |

#### MINOR
| # | Area | Expected | Actual | Fix |
|---|------|----------|--------|-----|
| 1 | CTA border-radius | ~12px | 8px | Adjust to border-radius: 0.75rem |

### Score Breakdown
| Dimension | Score | Notes |
|-----------|-------|-------|
| Layout | 95% | Grid structure matches |
| Color | 85% | Background gradient missing |
| Typography | 90% | Heading size slightly off |
| Spacing | 92% | Minor padding differences |
| Components | 88% | Button radius differs |

### Recommended Action
[DELIVER / REFINE / REWORK]
```

---

## Iteration Rules

### Maximum 3 Iterations

| Iteration | Focus | Stop Condition |
|-----------|-------|----------------|
| 1 | Fix all CRITICAL differences | Score ≥ 90% or no CRITICAL items |
| 2 | Fix MODERATE differences | Score ≥ 95% or no MODERATE items |
| 3 | Fine-tune MINOR differences | Best achievable score |

### Iteration Protocol

1. **Before each iteration**: Re-read the difference report from the previous comparison.
2. **Apply targeted fixes**: Only modify CSS properties identified in the report.
3. **Re-capture screenshot**: Use the same viewport and settings.
4. **Re-compare**: Generate a new difference report.
5. **Stop criteria**: Score ≥ 90%, or 3 iterations completed, or no actionable improvements remain.

### Diminishing Returns Rule

If the score improvement between iterations is less than 2%, stop iterating and document remaining differences as known limitations.

### What NOT to Fix in Iterations

- Font family mismatches (LOW confidence — needs designer input)
- Content differences (placeholder text vs real text)
- Animation/interaction differences (not visible in screenshots)
- Exact image asset matching (use placeholders, note in report)

---

## Playwright toHaveScreenshot() Advanced Configuration

For projects with Playwright test infrastructure, use the built-in visual comparison API:

### Recommended Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  expect: {
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.01,  // 1% tolerance — strict for mockup matching
      threshold: 0.15,           // Pixel color sensitivity (0=strict, 1=lenient)
      animations: 'disabled',   // Freeze CSS animations
    },
  },
});
```

### Full Parameter Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `threshold` | `0.2` | Per-pixel color difference tolerance (YIQ color space, 0-1) |
| `maxDiffPixels` | — | Absolute max differing pixels allowed |
| `maxDiffPixelRatio` | — | Max ratio of differing pixels to total (0-1) |
| `animations` | `"disabled"` | Freeze CSS animations/transitions during capture |
| `caret` | `"hide"` | Hide text cursor |
| `mask` | `[]` | Array of Locators to mask (covered with pink box) |
| `maskColor` | `"#FF00FF"` | Mask overlay color (v1.35+) |
| `scale` | `"css"` | `"device"` for high-DPI precision |
| `stylePath` | — | CSS file to inject (hide dynamic elements) (v1.41+) |
| `fullPage` | `false` | Capture full scrollable page |
| `clip` | — | `{x, y, width, height}` for partial capture |

### Dynamic Content Handling

```typescript
await expect(page).toHaveScreenshot('hero.png', {
  mask: [
    page.locator('.timestamp'),      // Dynamic dates
    page.locator('.user-avatar'),     // User-specific content
    page.locator('iframe'),           // Third-party embeds
  ],
  stylePath: './hide-dynamic.css',   // Additional hiding rules
});
```

### Environment Consistency

Screenshots differ across OS/browser/font rendering. Best practices:
- Use Docker containers for CI to ensure identical rendering
- Always capture with `deviceScaleFactor: 2` for retina quality
- Wait for `document.fonts.ready` before capturing
- Set consistent locale and timezone in browser context

---

## Verification Best Practices Summary

1. **Segment comparison**: Compare section-by-section, not just full page — easier to isolate issues
2. **Consistent environment**: Same browser, viewport, scale factor for all captures
3. **Font load waiting**: `await page.evaluate(() => document.fonts.ready)` before screenshot
4. **Anti-aliasing tolerance**: Set `threshold: 0.1-0.2` to avoid false positives from rendering differences
5. **Diff image feedback loop**: Pass the pixelmatch diff image back to the AI for targeted fixes — this is the single most effective technique for iterative refinement
