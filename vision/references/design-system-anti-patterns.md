# Design System Anti-Patterns

> トークンスプロール、命名ミス、コンポーネント設計の落とし穴、ガバナンス問題の検出と対策

## 1. デザインシステム 8 大アンチパターン

| # | アンチパターン | 問題 | 影響 | 対策 |
|---|-------------|------|------|------|
| **DS-01** | **トークンスプロール** | 管理外トークンの無秩序な増殖 | 一貫性崩壊、メンテナンス不能 | 3 層アーキテクチャ（Reference → Semantic → Component） |
| **DS-02** | **外観依存の命名** | `blue-button`, `color-red` 等の見た目ベース命名 | ブランド変更時に全命名崩壊 | Semantic 命名（`color.primary.default`, `color.error`） |
| **DS-03** | **ハードコード値** | トークン未使用で直接 HEX/px を記述 | Token Drift、デザイン-コード乖離 | Linter/CI で Token Drift 自動検出 |
| **DS-04** | **冗長トークン** | 同一値の複数トークン重複 | 混乱、メンテナンスコスト増 | 定期棚卸し、トークンマッピング監査 |
| **DS-05** | **コンポーネント命名不一致** | デザインとコードで異なるコンポーネント名 | チーム間コミュニケーション断絶 | 共通ボキャブラリー策定、Component Gallery 参照 |
| **DS-06** | **突然のトークン削除** | 非推奨プロセスなしでトークン廃止 | 下流コンポーネント破損、リグレッション | 段階的 Deprecation（警告 → 代替提示 → 削除） |
| **DS-07** | **テーマ非対応設計** | ライトモードのみ想定したトークン体系 | ダークモード/ブランド展開時に全面改修 | テーマ非依存コンポーネント + ランタイムテーマ注入 |
| **DS-08** | **ドキュメント不足** | トークンの用途・根拠が未記録 | 新メンバーが誤用、トークン目的喪失 | 各トークンに rationale + usage guidelines 必須 |

---

## 2. トークンアーキテクチャ（3 層モデル）

```
推奨アーキテクチャ:

  Layer 1: Reference Tokens（プリミティブ）
    - 生の値を保持（色: blue.500 = #0066cc、スペーシング: space.4 = 16px）
    - 外部に公開しない（Private）
    - 命名: カテゴリ.値

  Layer 2: Semantic Tokens（意味的）
    - 意図をマッピング（color.primary = ref.blue.500）
    - テーマ切り替えの接点
    - 命名: カテゴリ.用途.状態

  Layer 3: Component Tokens（コンポーネント固有）
    - コンポーネントに特化（button.bg = semantic.primary）
    - 最も具体的
    - 命名: コンポーネント.プロパティ.バリアント.状態

トークン命名規則:
  [namespace].[category].[concept].[property].[variant].[state].[scale]

  良い例:
    color.primary.default          → メインブランドカラー
    color.primary.hover            → ホバー時のブランドカラー
    text.heading.lg                → 大見出しサイズ
    space.layout.section           → セクション間余白

  悪い例:
    color.blue                     → 外観依存（DS-02）
    --color1                       → 意味不明
    button-blue-big                → 外観 + サイズ混在
    primary                        → カテゴリなし、曖昧
```

---

## 3. テーマ戦略

```
マルチテーマ設計:
  - 同一 Semantic Token が異なる Reference を参照
  - コンポーネントコードはテーマ非依存

  例:
    Light Mode:  color.background = ref.gray.100
    Dark Mode:   color.background = ref.gray.900
    Brand A:     color.primary = ref.blue.500
    Brand B:     color.primary = ref.green.500

  実装パターン:
    1. CSS Custom Properties + data-theme 属性切替
    2. ランタイムテーマ注入（Provider パターン）
    3. ビルド時プリプロセス（ブランド別ビルド）

  アクセシビリティテーマ:
    - high-contrast: コントラスト比強化
    - reduced-motion: アニメーション抑制
    - large-text: ベースフォントサイズ拡大
```

---

## 4. ガバナンスと CI/CD

```
トークンライフサイクル管理:
  1. 提案: 新トークンの RFC（用途・根拠・影響範囲）
  2. レビュー: デザイン + 開発の合意
  3. 実装: Figma Variables + コードトークン同期
  4. 公開: セマンティックバージョニング
  5. 非推奨: 警告期間 → 代替案提示 → 最終削除

CI/CD チェック:
  □ トークン命名規則準拠（Lint）
  □ ハードコード値の検出（Token Drift 防止）
  □ プラットフォーム別フォーマット生成（CSS/iOS/Android）
  □ Visual Regression テスト
  □ 未使用トークンの検出・レポート

効果:
  - トークン駆動パイプラインでデザイン QA 問題 50%+ 削減
  - ブランド展開時のコンポーネント重複ゼロ
```

---

## 5. Vision との連携

```
Vision での活用:
  1. NEW_PRODUCT モードでトークン 3 層設計の策定
  2. REVIEW モードで DS-01〜08 のスクリーニング
  3. REDESIGN モードでテーマ戦略の設計
  4. Muse 委譲時にトークンアーキテクチャ仕様を同梱

品質ゲート:
  - 新トークン追加時に 3 層のどこに属するか明示必須（DS-01 防止）
  - 外観依存名検出 → Semantic 命名への修正を要求（DS-02 防止）
  - ダークモード非対応 → テーマ対応設計を要求（DS-07 防止）
  - トークン削除時に Deprecation プロセス準拠を確認（DS-06 防止）
  - Figma Variables とコードトークンの同期確認
```

**Source:** [Smashing Magazine: Naming Best Practices](https://www.smashingmagazine.com/2024/05/naming-best-practices/) · [Material UI: Design Tokens & Theming 2025](https://materialui.co/blog/design-tokens-and-theming-scalable-ui-2025) · [Design Systems Collective: Figma Variables Playbook](https://www.designsystemscollective.com/design-system-mastery-with-figma-variables-the-2025-2026-best-practice-playbook-da0500ca0e66) · [design.dev: Design Systems Complete Guide](https://design.dev/guides/design-systems/)
