# Frontend Debugging Reference

ブラウザ・フロントエンドフレームワーク固有のバグ調査パターン。

## Browser DevTools Strategy

### Console Patterns
- Unhandled Promise rejection → async error handling 漏れ
- `[Violation]` warnings → 強制 reflow, long task, passive event listener
- CORS errors → API endpoint 設定ミスまたはプロキシ設定不備

### Network Tab Investigation
- Waterfall で遅延リクエスト特定 → リソース依存チェーンの問題
- Response diff（expected vs actual）→ API contract violation
- Preflight (OPTIONS) 失敗 → CORS 設定起因

### Performance Tab
- Long Task (>50ms) → メインスレッドブロッキング
- Layout Shift → CLS 問題の原因特定（画像サイズ未指定、動的コンテンツ挿入）
- Memory timeline → リーク検出（Specter 連携候補）

## React-Specific Patterns

### Hydration Mismatch
- 症状: `Text content does not match server-rendered HTML`
- 原因: SSR と CSR で異なる出力（Date, Math.random, window 参照）
- 調査: `suppressHydrationWarning` の不適切な使用をチェック
- 根本対策: `useEffect` 内でクライアント専用ロジックを分離

### Stale Closure
- 症状: イベントハンドラが古い state を参照
- 原因: useCallback/useEffect の依存配列不備
- 調査: ESLint `exhaustive-deps` 警告の有無確認
- パターン: `setState(prev => ...)` 関数型更新で回避可能か検証

### useEffect Cleanup Missing
- 症状: unmount 後の state 更新（メモリリーク）
- 原因: subscription, timer, AbortController の cleanup 忘れ
- 調査: `Can't perform a React state update on an unmounted component` 警告
- Specter 連携: メモリリーク疑いの場合 SCOUT_TO_SPECTER_HANDOFF

### Infinite Re-render Loop
- 症状: `Maximum update depth exceeded`
- 原因: useEffect 内での無条件 setState、オブジェクトリテラルの依存配列
- 調査: React DevTools Profiler で re-render 回数確認

## Vue-Specific Patterns

### Reactivity Lost
- 症状: データ変更が画面に反映されない
- 原因: Vue 2 の直接配列インデックス代入、Vue 3 の ref 未使用
- 調査: Vue Devtools で reactive state の追跡

### Computed Cache Invalidation
- 症状: computed が再計算されない
- 原因: 依存関係が reactive でないプロパティを参照
- 調査: computed の getter 内で参照しているプロパティの reactive 状態確認

## State Management Bugs

### Redux Selector Memoization Failure
- 症状: 不要な re-render
- 原因: createSelector の入力セレクタが毎回新しいオブジェクトを返す
- 調査: Redux DevTools で action dispatch ごとの state diff 確認
- パターン: `===` 参照比較のため、配列/オブジェクトの再生成に注意

### Zustand Stale State
- 症状: subscribe 内で古い state が読まれる
- 原因: クロージャのキャプチャ問題
- 調査: `getState()` と subscribe 内 state の値比較

## CSS Layout Bug Patterns

### Z-index Stacking Context
- 症状: 要素が他要素の下に隠れる
- 原因: 新しい stacking context の暗黙生成（transform, opacity, will-change）
- 調査: DevTools の Layers パネルで stacking context 可視化

### Flexbox/Grid Overflow
- 症状: コンテンツがコンテナからはみ出す
- 原因: `min-width: auto`（Flexbox デフォルト）、テキスト折り返し未設定
- 調査: `overflow: hidden` で問題箇所を特定 → `min-width: 0` で修正

### Container Query / @layer 問題
- 症状: スタイルが特定条件でのみ適用されない
- 原因: Container query のサイズ条件不一致、@layer の優先順位
- 調査: DevTools Styles パネルで適用/オーバーライドされたルール確認

## Mobile-Specific Patterns

### Touch Event vs Click Delay
- 症状: タップ後の 300ms 遅延
- 原因: ダブルタップズーム判定の待機
- 調査: `touch-action: manipulation` の設定有無

### Viewport Bug
- 症状: iOS Safari でアドレスバー表示/非表示時のレイアウト崩れ
- 原因: `100vh` が動的ビューポート高を含まない
- 調査: `dvh` (dynamic viewport height) の使用状況確認

## AI-Generated Frontend Code Patterns

AI 生成コードで頻出するフロントエンドバグ:
- 依存配列の不完全指定（ESLint suppressions の安易な使用）
- エラーバウンダリ未設置（happy path のみ実装）
- アクセシビリティ属性の欠落（aria-label, role, keyboard navigation）
- レスポンシブ対応の不完全さ（特定ブレークポイントのみ考慮）
