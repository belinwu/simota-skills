# Core Web Vitals Optimization Details

## LCP Optimization

### Issue: Large hero image
Fix:
- Add `loading="eager"` and `fetchpriority="high"`
- Use next/image with priority prop
- Preload critical images
```html
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">
```

### Issue: Unoptimized image format
Fix:
- Serve AVIF with WebP and JPEG fallback via `<picture>` — AVIF is ~40–60% smaller than JPEG (~95% browser support, 2026)
- Caution: AVIF decode is CPU-heavy; on low-end mobile devices, WebP may yield better LCP due to faster decode
```html
<picture>
  <source srcset="/hero.avif" type="image/avif">
  <source srcset="/hero.webp" type="image/webp">
  <img src="/hero.jpg" alt="..." width="1200" height="630"
       loading="eager" fetchpriority="high">
</picture>
```

### Issue: Render-blocking CSS/JS
Fix:
- Inline critical CSS
- Defer non-critical JavaScript
- Use `<link rel="preload">` for critical resources

### Issue: Slow server response (TTFB)
Fix:
- Enable caching (CDN, HTTP cache)
- Optimize backend queries
- Use edge computing (Vercel Edge, Cloudflare Workers)

### Issue: Client-side rendering delay
Fix:
- Use SSR/SSG for above-the-fold content
- Stream HTML with React Suspense
- Avoid hydration waterfalls

---

## INP Optimization

### Issue: Long JavaScript tasks
Fix:
- Break long tasks with `yield` or `scheduler.yield()`
- Use Web Workers for heavy computation
- Debounce/throttle event handlers

### Issue: Slow event handlers
Fix:
- Use `useTransition` for non-urgent updates
- Virtualize long lists
- Memoize expensive components

### Issue: Layout thrashing
Fix:
- Batch DOM reads/writes
- Use `requestAnimationFrame` for animations
- Avoid forced synchronous layouts

### Measurement

```javascript
// INP measurement with web-vitals
import { onINP } from 'web-vitals';

onINP((metric) => {
  console.log('INP:', metric.value);
  // Report to analytics
});
```

---

## CLS Optimization

### Issue: Images without dimensions
Fix:
```jsx
// Always specify dimensions
<img src="..." width={800} height={600} alt="..." />

// Or use aspect-ratio CSS
<div style={{ aspectRatio: '16/9' }}>
  <img src="..." style={{ width: '100%', height: '100%' }} />
</div>
```

### Issue: Ads/embeds causing shifts
Fix:
- Reserve space with min-height
- Use contain-intrinsic-size CSS
- Lazy load below the fold only

### Issue: Web fonts causing FOUT
Fix:
```css
/* Fallback font with similar metrics */
font-family: 'Custom Font', system-ui, sans-serif;
font-display: swap;
```

### Issue: Dynamic content insertion
Fix:
- Reserve space for dynamic content
- Use skeleton loaders with fixed dimensions
- Avoid inserting content above existing content

---

## Web Vitals Monitoring

```typescript
// web-vitals integration
import { onLCP, onINP, onCLS } from 'web-vitals';

function sendToAnalytics(metric: Metric) {
  // Send to your analytics provider
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating,
    delta: metric.delta,
    id: metric.id,
  });

  // Use sendBeacon for reliability
  navigator.sendBeacon('/api/vitals', body);
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```
