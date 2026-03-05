# Animation Performance Anti-Patterns

> レイアウトスラッシング、GPU vs レイアウトプロパティ、フレームバジェット、Core Web Vitals への影響

## 1. アニメーションパフォーマンス 7 大アンチパターン

| # | アンチパターン | 問題 | ユーザーへの影響 | 対策 |
|---|-------------|------|---------------|------|
| **AP-01** | **レイアウトプロパティのアニメーション** | `width`, `height`, `margin`, `padding`, `top`, `left` をアニメーション | 毎フレームでレイアウト再計算 → ジャンク発生 | `transform: translate/scale` で置換 |
| **AP-02** | **強制リフロー（Layout Thrashing）** | JS で読み取り→書き込みを交互に繰り返す | レイアウト計算が毎回強制実行 | 読み取りをバッチ化、書き込みを rAF で一括 |
| **AP-03** | **過剰な同時アニメーション** | 10+ 要素が同時にアニメーション | CPU/GPU 過負荷、フレームドロップ | `stagger` で時間差実行、viewport 内のみ |
| **AP-04** | **box-shadow / filter の連続変更** | `box-shadow`, `blur()`, `drop-shadow()` をアニメーション | ペイント領域が毎フレーム再描画 | `opacity` 切替でシャドウ表示、`will-change` 限定使用 |
| **AP-05** | **will-change の濫用** | `will-change: transform` を全要素に指定 | GPU メモリ過剰消費、逆にパフォーマンス低下 | アニメーション開始直前に追加、終了後に削除 |
| **AP-06** | **無限ループアニメーション** | `animation: spin 1s infinite` を多用 | 常時 GPU レイヤー保持、バッテリー消耗 | スピナー以外は避ける、viewport 外で `paused` |
| **AP-07** | **メインスレッドブロッキング** | JS アニメーション内で同期処理 | アニメーションがカクつく、INP 悪化 | Web Animations API / CSS アニメーション優先 |

---

## 2. CSS プロパティのコストティア

```
ティアリスト（パフォーマンスコスト順）:

  ✅ Tier S（Composite のみ — GPU 安全）:
    transform, opacity, filter (GPU), clip-path
    → レイアウト・ペイント不要、最高パフォーマンス

  ⚠️ Tier A（Paint のみ — 条件付き安全）:
    color, background-color, box-shadow, border-color
    → レイアウト不要だがペイント発生
    → will-change でレイヤー昇格すれば改善

  ❌ Tier B（Layout 発生 — 避けるべき）:
    width, height, padding, margin, border-width
    → レイアウト → ペイント → コンポジット全段階実行

  ❌ Tier C（Layout + 影響範囲大 — 禁止）:
    top, left, right, bottom（position: absolute/relative）
    font-size, line-height
    → 周囲の要素にも影響、大規模再計算
```

---

## 3. 強制リフローの回避

```
強制リフローが発生する読み取りプロパティ:
  offsetTop, offsetLeft, offsetWidth, offsetHeight
  scrollTop, scrollLeft, scrollWidth, scrollHeight
  clientTop, clientLeft, clientWidth, clientHeight
  getComputedStyle(), getBoundingClientRect()

❌ アンチパターン: 読み書き交互実行
  elements.forEach(el => {
    const height = el.offsetHeight;      // 読み取り → 強制リフロー
    el.style.height = height + 10 + 'px'; // 書き込み → 次の読み取りで再リフロー
  });

✅ 推奨: バッチ読み取り → バッチ書き込み
  // 1. 全読み取り
  const heights = elements.map(el => el.offsetHeight);
  // 2. 全書き込み（rAF 内で）
  requestAnimationFrame(() => {
    elements.forEach((el, i) => {
      el.style.height = heights[i] + 10 + 'px';
    });
  });

✅ 推奨: fastdom ライブラリ使用
  fastdom.measure(() => { /* 読み取り */ });
  fastdom.mutate(() => { /* 書き込み */ });
```

---

## 4. フレームバジェットと測定

```
60fps フレームバジェット:
  1000ms ÷ 60 = 16.67ms / フレーム
  ブラウザオーバーヘッド ≈ 6ms
  → JS + スタイル + レイアウト + ペイント = 10ms 以内

測定方法:
  1. Chrome DevTools → Performance パネル
     - Frame timing でフレームドロップ確認
     - Long Animation Frame (LoAF) で 50ms+ のフレーム検出

  2. Performance Observer API
     const observer = new PerformanceObserver((list) => {
       for (const entry of list.getEntries()) {
         if (entry.duration > 16.67) {
           console.warn('Frame budget exceeded:', entry.duration);
         }
       }
     });
     observer.observe({ type: 'long-animation-frame', buffered: true });

  3. requestAnimationFrame ベースの FPS 計測
     let lastTime = performance.now();
     let frames = 0;
     function checkFPS(now) {
       frames++;
       if (now - lastTime >= 1000) {
         console.log(`FPS: ${frames}`);
         frames = 0;
         lastTime = now;
       }
       requestAnimationFrame(checkFPS);
     }
```

---

## 5. Core Web Vitals への影響

| メトリクス | リスク | アニメーション起因 | 対策 |
|-----------|--------|----------------|------|
| **CLS** | High | レイアウトシフトを伴うアニメーション | `transform` のみ使用、初期サイズ確保 |
| **LCP** | Medium | クリティカルコンテンツの遅延表示 | Above-the-fold は即時表示、アニメーション後回し |
| **INP** | High | クリック後の重いアニメーション処理 | インタラクション応答 < 200ms、アニメーションは非同期 |

```
CLS 防止チェックリスト:
  ✅ width/height/margin/padding をアニメーションしていない
  ✅ 要素の挿入/削除でレイアウトシフトしない
  ✅ フォントローディングでレイアウトシフトしない
  ✅ 画像/動画に明示的なサイズ指定

INP 最適化:
  ✅ クリックハンドラ内の処理は最小限
  ✅ 重いアニメーション開始は requestAnimationFrame で分離
  ✅ CSS アニメーション / Web Animations API 優先（メインスレッド解放）
```

---

## 6. will-change の正しい使い方

```
❌ アンチパターン: 全要素に静的指定
  * { will-change: transform, opacity; }
  .card { will-change: transform; }  /* 常時指定 */

✅ 推奨: 動的に必要時のみ
  .card:hover { will-change: transform; }
  .card.animating { will-change: transform; }

  /* JS で制御 */
  el.addEventListener('mouseenter', () => {
    el.style.willChange = 'transform';
  });
  el.addEventListener('transitionend', () => {
    el.style.willChange = 'auto';
  });

注意事項:
  - will-change は「最後の手段」— まず transform/opacity を使う
  - 指定するとブラウザが専用レイヤーを作成 → メモリ消費
  - モバイルデバイスでは特にメモリ制約に注意
  - 1 ページ内で will-change 要素は 10 個以下を推奨
```

---

## 7. Flow との連携

```
Flow での活用:
  1. 実装前に CSS プロパティのティアを確認（Tier S 優先）
  2. 同時アニメーション数の制限チェック
  3. will-change の適切な使用パターン適用
  4. Core Web Vitals への影響を事前評価

品質ゲート:
  - width/height/margin アニメーション → transform 置換（AP-01 防止）
  - offsetHeight 読み取り + style 書き込みの交互 → バッチ化（AP-02 防止）
  - will-change 静的指定 → 動的制御に変更（AP-05 防止）
  - 無限アニメーション → viewport 外で paused（AP-06 防止）
  - JS 同期アニメーション → CSS / Web Animations API（AP-07 防止）
  - CLS 寄与アニメーション → transform のみに制限
  - INP > 200ms → アニメーション処理の非同期化
```

**Source:** [web.dev: Animations and Performance](https://web.dev/articles/animations-and-performance) · [MDN: CSS Performance Optimization](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance/CSS) · [Chrome DevTools: Long Animation Frames](https://developer.chrome.com/docs/devtools/performance/long-animation-frames)
