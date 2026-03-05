# Motion System Design Patterns

> モーショントークン体系、duration/easing スケール設計、アニメーションカタログ化、モーション監査、デザインシステム統合

## 1. モーションシステム設計の 6 大原則

| # | 原則 | 説明 | 実践 |
|---|------|------|------|
| **MS-01** | **トークン駆動** | 全 duration/easing を変数化 | `--duration-fast: 100ms` で一元管理 |
| **MS-02** | **スケール設計** | 離散的な段階（5-7 段階）でトークン定義 | t1(50ms)〜t5(400ms) の 5 段階 |
| **MS-03** | **用途紐付け** | 各トークンに用途を明示 | `--duration-fast` = ボタン/チェックボックス |
| **MS-04** | **reduced-motion 統合** | トークンレベルで reduced-motion 対応 | `prefers-reduced-motion: reduce` で全トークン 0ms |
| **MS-05** | **カタログ化** | 全アニメーションを分類・文書化 | 図解スペック + テキストスペック |
| **MS-06** | **監査可能** | トークン使用率・逸脱を計測 | 定期監査でハードコード値検出 |

---

## 2. モーショントークンスケール設計

```
Duration スケール（5 段階推奨）:

  t1: 50ms   — instant    — マイクロフィードバック（色変化、ハイライト）
  t2: 100ms  — fast       — ボタンプレス、チェックボックス、トグル
  t3: 200ms  — normal     — フェードイン/アウト、ドロップダウン展開
  t4: 300ms  — slow       — モーダル開閉、パネルスライド、カード展開
  t5: 400ms  — slower     — ページ遷移、複雑なシーケンス

  ❌ アンチパターン: 連続スケール
    --duration-100: 100ms;
    --duration-150: 150ms;
    --duration-200: 200ms;
    --duration-250: 250ms;
    → 選択に迷う、一貫性なし

  ✅ 推奨: 離散的スケール
    --duration-fast: 100ms;
    --duration-normal: 200ms;
    --duration-slow: 300ms;
    → 明確な選択肢、一貫した使用

Easing スケール（2-3 カーブで十分）:

  ease-out:    cubic-bezier(0, 0, 0.2, 1)     — 入場、ユーザー応答
  ease-in:     cubic-bezier(0.4, 0, 1, 1)     — 退場、消失
  ease-in-out: cubic-bezier(0.4, 0, 0.2, 1)   — 状態変化、トグル

  ❌ アンチパターン: 過剰なイージング定義
    10+ のカスタムベジェカーブ
    → 開発者が混乱、意図が不明確

  ✅ 推奨: 3 カーブ + 例外
    標準 3 カーブで 90% をカバー
    Spring は JS のみ、特殊用途（ドラッグ等）
```

---

## 3. 主要デザインシステムのモーション比較

| システム | Duration スケール | Easing | 特徴 |
|---------|-----------------|--------|------|
| **Material Design 3** | 50/100/150/200/250/300/350/400/500ms | Standard/Emphasized/Standard decelerate/Emphasized decelerate | 3 種の Emphasis レベル |
| **IBM Carbon** | 70/110/150/240/400ms | Productive/Expressive × Standard/Entrance/Exit | Productive（機能的）/ Expressive（感情的）の 2 軸 |
| **Salesforce Lightning** | 100/200/400ms | Ease-in/Ease-out/Ease-in-out | シンプル 3 段階 |
| **Ant Design** | 100/200/300ms | Standard/Deceleration/Acceleration/Linear | 4 イージング |

```
設計指針:
  - 小規模プロジェクト: Salesforce 方式（3 段階）で十分
  - 中規模プロジェクト: 5 段階 duration + 3 easing（推奨）
  - 大規模プロジェクト: IBM 方式（Productive/Expressive 軸追加）
```

---

## 4. アニメーションカタログの構造

```
カタログのフォーマット（各アニメーションに必要な情報）:

  図解スペック（Visual Spec）:
    - Before → After のスクリーンショット
    - アニメーションの軌道（矢印/パス表示）
    - タイミングダイアグラム（開始・終了・オーバーラップ）

  テキストスペック（Text Spec）:
    - 名前: slide-up-enter
    - カテゴリ: Entry / Exit / Micro / Page / Gesture
    - Duration: var(--duration-normal) = 200ms
    - Easing: var(--ease-out)
    - Properties: transform(translateY), opacity
    - Trigger: ユーザーアクション / スクロール / ページ遷移
    - Reduced-motion: opacity 0.15s のみ
    - 使用箇所: Card展開、リスト項目追加、通知表示

カテゴリ分類:
  ├── Entry（入場）: fade-in, slide-up, scale-in, expand
  ├── Exit（退場）: fade-out, slide-down, scale-out, collapse
  ├── Micro（マイクロ）: press, toggle, shake, pulse, ripple
  ├── State（状態変化）: color-change, border-focus, active-state
  ├── Scroll（スクロール）: reveal, parallax, progress, sticky
  ├── Page（ページ遷移）: crossfade, slide-lateral, shared-element
  └── Gesture（ジェスチャー）: drag, swipe, snap, pinch, long-press
```

---

## 5. モーション監査フレームワーク

```
Audit-First アプローチ（既存プロジェクト向け）:

  Step 1: 全アニメーションのインベントリ
    - CSS: transition, animation, @keyframes を全検索
    - JS: animate(), gsap, framer-motion 使用箇所を検索
    - 結果: スプレッドシートに一覧化

  Step 2: 分類と評価
    各アニメーションに対して:
    □ 目的は明確か？（機能的 / 装飾的）
    □ Duration は適切か？（ガイドライン範囲内）
    □ Easing は用途に合っているか？
    □ prefers-reduced-motion 対応済みか？
    □ GPU-safe プロパティのみ使用か？
    □ トークンを使用しているか？（ハードコード値でないか）

  Step 3: 優先度付け改善
    P0: a11y 違反（reduced-motion 未対応、閃光）
    P1: パフォーマンス問題（レイアウトアニメーション）
    P2: トークン未使用（ハードコード duration/easing）
    P3: 設計改善（タイミング調整、イージング最適化）

定量メトリクス:
  - トークンカバレッジ率: トークン使用 / 全アニメーション値
  - reduced-motion 対応率: 対応済み / 全アニメーション
  - GPU-safe 率: composite-only / 全アニメーションプロパティ
  - 目標: 全メトリクス 95%+
```

---

## 6. コンポジットアニメーションパターン

```
Stagger パターン（連続入場）:

  .list-item {
    opacity: 0;
    transform: translateY(8px);
    animation: enter var(--duration-normal) var(--ease-out) forwards;
  }

  .list-item:nth-child(1) { animation-delay: 0ms; }
  .list-item:nth-child(2) { animation-delay: 50ms; }
  .list-item:nth-child(3) { animation-delay: 100ms; }

  /* CSS Custom Property で動的制御 */
  .list-item {
    animation-delay: calc(var(--index) * 50ms);
  }

  ❌ アンチパターン: stagger 間隔が長すぎる
    delay: calc(var(--index) * 200ms);
    → 10 項目 = 2 秒待ち → ユーザーが離脱

  ✅ 推奨: 30-80ms 間隔、最大合計 500ms
    → 10 項目でも 50ms × 10 = 500ms

Choreography パターン（複合遷移）:

  ❌ アンチパターン: 全要素同時に同じアニメーション
    .modal * { animation: fade-in 200ms; }

  ✅ 推奨: 要素ごとの役割に応じた時間差
    .modal-overlay  { animation: fade-in 150ms; }           /* 1. 背景 */
    .modal-content  { animation: scale-in 200ms 50ms; }     /* 2. コンテンツ */
    .modal-title    { animation: slide-up 150ms 150ms; }    /* 3. タイトル */
    .modal-actions  { animation: fade-in 100ms 200ms; }     /* 4. アクション */
```

---

## 7. デザインシステム統合チェックリスト

```
Motion System 導入チェックリスト:

  トークン定義:
    □ Duration スケール定義済み（5 段階推奨）
    □ Easing スケール定義済み（3 カーブ推奨）
    □ reduced-motion オーバーライド定義済み
    □ Muse のトークン体系と整合

  カタログ:
    □ 全パターンにテキストスペック
    □ カテゴリ分類済み
    □ 使用箇所マッピング済み
    □ Storybook/デモで確認可能

  品質:
    □ GPU-safe プロパティのみ使用
    □ prefers-reduced-motion 全対応
    □ Core Web Vitals 影響なし
    □ 60fps 確認済み

  ガバナンス:
    □ 新アニメーション追加フロー定義
    □ 監査スケジュール設定（四半期推奨）
    □ トークンカバレッジ目標設定（95%+）
    □ 逸脱検出の Linter / CI 統合
```

---

## 8. Flow との連携

```
Flow での活用:
  1. 新プロジェクト: トークンスケール設計から開始
  2. 既存プロジェクト: Audit-First で現状把握 → 段階的トークン化
  3. 全アニメーション実装時にカタログエントリ追加
  4. Muse と協調してトークン体系を統一

品質ゲート:
  - ハードコード duration/easing → トークン置換（MS-01 防止）
  - 連続スケール（100/150/200/250...） → 離散スケールに統合（MS-02 防止）
  - 用途不明のトークン → 用途ドキュメント追加（MS-03 防止）
  - reduced-motion 未統合トークン → オーバーライド追加（MS-04 防止）
  - カタログ未登録アニメーション → エントリ追加（MS-05 防止）
  - トークンカバレッジ < 95% → ハードコード値のトークン化推進（MS-06 防止）
```

**Source:** [Smashing Magazine: Design System Motion](https://www.smashingmagazine.com/2023/11/design-system-motion/) · [Material Design 3: Motion](https://m3.material.io/styles/motion) · [IBM Carbon: Motion](https://carbondesignsystem.com/elements/motion/overview/) · [Salesforce Lightning: Motion](https://www.lightningdesignsystem.com/guidelines/motion/)
