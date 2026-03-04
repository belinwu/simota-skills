# Frontend Performance Optimization

> Core Web Vitals、画像最適化、バンドル削減、レンダリング最適化、パフォーマンスバジェット

## 1. Core Web Vitals ターゲット

| メトリクス | 目標 | 測定対象 |
|-----------|------|---------|
| **LCP** (Largest Contentful Paint) | < 2.5s | メインコンテンツの表示速度 |
| **INP** (Interaction to Next Paint) | < 200ms | インタラクション応答性 (FID後継) |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 視覚的安定性 |

---

## 2. 画像最適化

```tsx
import Image from 'next/image';

// LCP画像: priority で即座にロード（lazy loading は使わない）
<Image src="/hero.jpg" alt="Hero" width={1200} height={600} priority />

// 通常画像: 自動 lazy loading
<Image src="/product.jpg" alt="Product" width={400} height={300} />

// 外部画像
<Image src={user.avatar} alt={user.name} width={48} height={48}
  sizes="48px" quality={75} />
```

| ルール | 理由 |
|--------|------|
| LCP要素に `loading="lazy"` を使わない | LCP が悪化する |
| LCP画像に `fetchpriority="high"` | 優先的にロード |
| `width`/`height` を必ず指定 | CLS 防止 |
| WebP/AVIF 使用 | JPEG比 25-35% 圧縮改善 |
| `sizes` で適切なサイズ配信 | 不要な大画像を防止 |

---

## 3. バンドルサイズ削減

### コード分割

```tsx
import { lazy, Suspense } from 'react';

// ルートベース分割（最も効果的: 初期ロード 40-60% 削減）
const AdminDashboard = lazy(() => import('./AdminDashboard'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>
    </Suspense>
  );
}
```

### ChunkLoadError 対応

```tsx
class ChunkErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };
  static getDerivedStateFromError(error: Error) {
    if (error.name === 'ChunkLoadError') return { hasError: true };
    throw error;
  }
  render() {
    if (this.state.hasError) {
      return <button onClick={() => window.location.reload()}>Reload</button>;
    }
    return this.props.children;
  }
}
```

### バンドル分析チェックリスト

- [ ] `bundle-analyzer` で定期的に構成を確認
- [ ] Tree Shaking が有効 (`sideEffects: false`)
- [ ] 大きなライブラリの部分インポート (`import { debounce } from 'lodash-es'`)
- [ ] `next/dynamic` でクライアント専用コンポーネントを遅延ロード
- [ ] サードパーティスクリプトに `strategy="lazyOnload"` 適用

---

## 4. レンダリング最適化

| 手法 | 効果 | 適用場面 |
|------|------|---------|
| Server Components をデフォルトに | JSバンドルに含まれない | 全てのデータ表示コンポーネント |
| Suspense ストリーミング | 段階的コンテンツ表示 | 遅いデータフェッチ |
| React Compiler (React 19) | 自動メモ化 | 新規コード全般 |
| `@tanstack/react-virtual` | 長リストの仮想化 | 100+アイテムのリスト |

### リソースヒント

```html
<!-- クリティカルリソース -->
<link rel="preload" href="/fonts/inter.woff2" as="font" crossorigin />

<!-- 次のナビゲーション先 -->
<link rel="prefetch" href="/dashboard" />

<!-- DNS 事前解決 -->
<link rel="dns-prefetch" href="https://api.example.com" />
```

---

## 5. パフォーマンスバジェット

| 項目 | 推奨上限 |
|------|---------|
| 総ページ重量 | < 1.5MB |
| JavaScript バンドル | < 300KB |
| Time to Interactive | < 3.5s |
| HTTP リクエスト数 | < 50 |

---

## 6. アンチパターン

| # | アンチパターン | 問題 | 修正 |
|---|------------|------|------|
| 1 | LCP要素に `loading="lazy"` | LCP スコア悪化 | `priority` / `fetchpriority="high"` |
| 2 | 画像に width/height 未指定 | CLS 発生 | 明示的にサイズ指定 |
| 3 | 過剰なプリフェッチ | コード分割の利点を相殺 | 重要パスのみ |
| 4 | Lab テストのみ依存 | 実ユーザー環境と乖離 | RUM で計測 |
| 5 | サードパーティスクリプト野放し | CWV の最大脅威 | `lazyOnload` + 影響監視 |
| 6 | モバイル最適化の軽視 | Google はモバイルで CWV 評価 | モバイルファースト |

**Source:** [Frontend Performance 2026](https://vofoxsolutions.com/front-end-performance-in-2026) · [Top CWV Improvements (web.dev)](https://web.dev/articles/top-cwv) · [React Bundle 62% Reduction](https://medium.com/@jaivalsuthar/how-i-reduced-our-react-bundle-by-62-a-junior-developers-optimization-journey-e0f5a2ca6ee6)
