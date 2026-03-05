# Design Token Anti-Patterns

> トークン命名・階層設計・管理の落とし穴、過剰/過少トークン化、トークンスプロール防止

## 1. トークン設計 8 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **DT-01** | **過剰トークン化** | 単一コンポーネント用にトークンを大量定義 | トークン数 > コンポーネント数 × 3、発見困難 | コンポーネントグループ単位でトークン化、再利用なしは定数 |
| **DT-02** | **過少トークン化** | Primitive トークンのみでセマンティック層なし | `blue-500` を直接使用、テーマ変更で全箇所修正 | Semantic 層を必ず設け、用途ベースの命名を徹底 |
| **DT-03** | **見た目ベースの命名** | `color-grey-10` のように値を名前に含む | ブランド変更時に名前と値が乖離 | 用途ベース命名: `color-text-secondary` |
| **DT-04** | **過剰修飾名** | `color-text-feedback-error-enabled-on_light` | 名前が長すぎて使用困難、タイポ増加 | 3-4 セグメント以内: `--{category}-{element}-{variant}` |
| **DT-05** | **モード不適切適用** | Typography トークンに dark/light モードを適用 | モード切替で意図しないフォントサイズ変更 | モード対象を Color/Shadow に限定、Typography は除外 |
| **DT-06** | **一回限りトークン** | 単一箇所でしか使わない値をトークン化 | トークンファイル肥大、メンテ負荷増 | 2+ コンポーネントで使う値のみトークン化 |
| **DT-07** | **ソース不一致** | Figma と Code で異なるトークン値/名前 | デザインと実装の乖離、手動同期忘れ | 単一ソース（Git or Figma）+ 自動 CI/CD 同期 |
| **DT-08** | **バージョン未管理** | トークンの変更履歴が追えない | 破壊的変更の影響範囲不明、ロールバック不可 | Semantic Versioning + CHANGELOG 必須 |

---

## 2. トークン命名のベストプラクティス

```
命名パターン: --{category}-{element}-{variant}-{state}

推奨例:
  --color-bg-primary          # 主要背景色
  --color-text-secondary      # 二次テキスト
  --color-border-focus        # フォーカス時ボーダー
  --space-padding-card        # カード内余白
  --font-size-heading-lg      # 大見出しサイズ

アンチパターン:
  ❌ --blue-500               # 値ベース → テーマ変更不可
  ❌ --color-grey-10           # 見た目ベース → ブランド変更で破綻
  ❌ --primary                 # カテゴリなし → 衝突リスク
  ❌ --card-specific-padding   # 単一用途 → トークン化不要
  ❌ --color-text-feedback-error-enabled-on_light  # 過剰修飾

命名規則のチーム合意:
  - 全員が理解し一貫して適用できること
  - ドキュメント化して新メンバーも参照可能に
  - Linter ルールで命名規則を自動チェック
```

---

## 3. トークン階層の設計指針

```
2 層構成（安定したデザインシステム向け）:
  Primitive → Semantic
  - メンテナンス軽量、明確
  - テーマ変更は Semantic 層のマッピング変更のみ

3 層構成（進化するデザインシステム向け、推奨）:
  Primitive → Semantic → Component
  - 開発者に明確な指針を提供
  - デザイナーが Semantic 層を変更しても Component は安定

よくある失敗:
  ❌ Primitive のみで運用 → テーマ変更で全ファイル修正
  ❌ 全トークンを public 公開 → 開発者が Primitive を直接使用
  ❌ Component 層を全コンポーネントに適用 → トークンスプロール

公開範囲の制御:
  - Primitive: 内部のみ（hidden from publishing）
  - Semantic: 公開（開発者が使用）
  - Component: 必要なもののみ公開
```

---

## 4. トークン管理の落とし穴

```
管理失敗パターン:

  Export-and-Forget:
    問題: Figma からエクスポート後、同期なし
    結果: デザインとコードの乖離が時間とともに拡大
    対策: CI/CD パイプラインで自動同期（Style Dictionary + GitHub Actions）

  ドキュメント腐敗:
    問題: トークン値は更新されるがドキュメントが古いまま
    結果: 開発者が誤った値を参照
    対策: トークンファイルからドキュメントを自動生成

  2D グリッドの欠如:
    問題: 色×状態の組み合わせを場当たり的に追加
    結果: 数百のトークンが無秩序に増殖
    対策: Static（変化しない）と Dynamic（状態変化する）の 2 軸で整理

  マジックナンバー（z-index）:
    問題: z-index を 999, 1000, 9999 と場当たり的に設定
    結果: スタッキングコンテキストの崩壊
    対策: z-index もトークン化（--z-dropdown: 100, --z-modal: 200）
```

---

## 5. Muse との連携

```
Muse での活用:
  1. SCAN フェーズで DT-01〜08 のスクリーニング
  2. 新規トークン提案時に命名規則チェック
  3. トークン監査で公開範囲の適切性を検証
  4. CI/CD 同期パイプラインの健全性確認

品質ゲート:
  - Primitive トークンの直接使用 → Semantic 層経由に修正（DT-02 防止）
  - 同一値の 3+ トークン → 統合を提案（DT-01 防止）
  - 値ベースの命名 → 用途ベースに変更（DT-03 防止）
  - 単一箇所のトークン → 定数化またはトークン削除（DT-06 防止）
  - Figma/Code 間のトークン差異 → 同期修正（DT-07 防止）
```

**Source:** [Good Practices Design: Design Tokens](https://goodpractices.design/articles/design-tokens) · [Contentful: Design Token System](https://www.contentful.com/blog/design-token-system/) · [Martin Fowler: Design Token-Based UI Architecture](https://martinfowler.com/articles/design-token-based-ui-architecture.html)
