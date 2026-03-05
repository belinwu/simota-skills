# Prototype-to-Production Handoff Guide

> プロトタイプから本番コードへの移行戦略、Throwaway vs Evolutionary、ハンドオフの落とし穴、Builder 連携

## 1. Throwaway vs Evolutionary プロトタイプ

### 比較マトリクス

| 特性 | Throwaway（使い捨て） | Evolutionary（進化型） |
|------|---------------------|---------------------|
| **目的** | 仮説検証・学習 | 段階的な本番構築 |
| **コード品質** | 低（速度優先） | 中〜高（構造化） |
| **寿命** | 検証後に破棄 | 本番まで進化 |
| **リスク** | 学びの喪失 | Lava Flow（古いコード残留） |
| **コスト** | 初期低・再構築高 | 初期高・再構築低 |
| **適用場面** | 不確実性が高い | 方向性が明確 |
| **Forge での頻度** | 70%（デフォルト） | 30%（明確な場合） |

### 判定フロー

```
要件の確実性は？
  │
  ├─ 不確実（仮説段階）→ Throwaway
  │   - 速度最優先
  │   - 本番とは別技術でも OK
  │   - 学びを forge-insights.md に記録
  │   - 検証後に DISCARD
  │
  ├─ やや確実（方向性は決定）→ Evolutionary
  │   - 本番と同じ技術スタック
  │   - 最低限の構造化を維持
  │   - 段階的に品質を向上
  │
  └─ 確実（仕様が明確）→ Forge 不要、直接 Builder へ
```

---

## 2. ハンドオフの 7 大落とし穴

| # | 落とし穴 | 問題 | 対策 |
|---|---------|------|------|
| **HO-01** | **暗黙知の消失** | プロトタイプ作成者の頭の中にある判断理由が伝わらない | forge-insights.md に意思決定と理由を記録 |
| **HO-02** | **プロトタイプ＝仕様の誤解** | ステークホルダーが「このまま出荷」と期待 | ステータスタグ（⚡ PROTOTYPE）を明示 |
| **HO-03** | **モックと実 API の乖離** | モックデータの構造が実 API と異なる → 大規模修正 | OpenAPI/型定義を先に合意 · MSW で契約準拠 |
| **HO-04** | **技術的負債の引き継ぎ** | プロトタイプの「仮実装」がそのまま本番に → Lava Flow | forge-insights.md に tech-debt セクション必須 |
| **HO-05** | **エッジケースの未考慮** | ハッピーパスのみ → 本番で想定外のエラー | 既知のエッジケースを forge-insights.md にリスト |
| **HO-06** | **デザイン意図の喪失** | なぜこの UI 構造にしたかが不明 → Artisan が再設計 | UI 判断の理由をコメント or insights に記録 |
| **HO-07** | **テスト戦略の不在** | プロトタイプにテストがない → 本番で何をテストすべきか不明 | テスト方針を forge-insights.md に記載 |

---

## 3. Forge → Builder ハンドオフ・チェックリスト

### 必須成果物

```
□ Feature.tsx（UI コンポーネント）
□ types.ts（型定義 — 本番で再利用可能な品質）
□ handlers.ts（MSW ハンドラー or API モック）
□ errors.ts（エラーケース定義）
□ forge-insights.md（ドメイン知識・判断記録）
```

### forge-insights.md 必須セクション

```markdown
## 検証した仮説
- [仮説の記述]
- 結果: CONFIRMED / REJECTED / NEEDS_MORE_DATA

## 意思決定ログ
- [日付] [決定内容] — 理由: [なぜ]

## 技術的負債
- [ ] [項目]: [理由と推奨対応]

## エッジケース（未対応）
- [ケース]: [発見経緯と想定影響]

## テスト方針
- ユニットテスト: [対象コンポーネント/関数]
- 統合テスト: [対象フロー]

## UI 判断メモ
- [判断]: [理由]
```

---

## 4. Evolutionary プロトタイプの段階的品質向上

### 品質レベル定義

| レベル | 段階 | 品質基準 | Forge フェーズ |
|--------|------|---------|--------------|
| **L0** | 概念実証 | 動けば良い · ハードコード OK | SCAFFOLD → STRIKE |
| **L1** | 検証可能 | 型定義あり · モック分離 · 基本構造 | COOL |
| **L2** | デモ可能 | エラー状態対応 · レスポンシブ · リアルデータ風 | PRESENT |
| **L3** | ハンドオフ可能 | Builder Integration 完了 · insights 完備 | → Builder |

### L0 → L3 の進め方

```
L0（2-4 時間）:
  - インラインモック、ハードコードデータ
  - 単一ファイルでも OK
  - console.log デバッグ

L1（+ 2-4 時間）:
  - types.ts を分離
  - モックを handlers.ts に分離
  - コンポーネントのファイル分割

L2（+ 4-8 時間）:
  - ローディング/エラー/空状態の対応
  - レスポンシブ対応（基本的な breakpoint）
  - リアルっぽいモックデータ（faker.js）

L3（+ 2-4 時間）:
  - forge-insights.md 作成
  - errors.ts 作成
  - ステータスタグとテスト手順の文書化
```

---

## 5. プロトタイプの技術的負債管理

### 負債の分類

| 種類 | 例 | 本番への影響 | 対応優先度 |
|------|---|-------------|----------|
| **意図的・記録済み** | 「ハードコードした認証トークン」 | 予測可能 | 計画的に対応 |
| **意図的・未記録** | 「とりあえず動かした部分」 | 見つかりにくい | 危険 — forge-insights 必須 |
| **非意図的** | 「知らずにアンチパターン使用」 | 発見が遅れる | レビューで検出 |

### 負債の記録ルール

```
forge-insights.md の tech-debt セクションに必ず記載:

形式:
  - [ ] [ファイル:行] [内容] — 理由: [なぜ仮実装か] · 推奨: [本番での対応方法]

例:
  - [ ] Feature.tsx:42 ハードコード認証トークン — 理由: 認証フローは検証対象外 · 推奨: AuthContext から取得
  - [ ] handlers.ts:15 固定遅延 300ms — 理由: リアルな遅延シミュレーション · 推奨: 実 API に置換
```

---

## 6. Forge との連携

```
Forge での活用:
  1. SCAFFOLD フェーズで Throwaway/Evolutionary の判定を実行
  2. Evolutionary の場合、L0→L3 の段階的品質向上を計画
  3. PRESENT フェーズで必須成果物チェックリストを適用
  4. ハンドオフ時に HO-01〜07 の落とし穴チェックを実施

品質ゲート:
  - forge-insights.md の tech-debt セクション空 → 警告（HO-04 防止）
  - ステータスタグなし → ハンドオフ前にブロック（HO-02 防止）
  - types.ts が未分離 → L1 未達の警告（段階的品質）
  - エッジケースセクション空 → 警告（HO-05 防止）
```

**Source:** [Budibase: Throwaway Prototyping](https://budibase.com/blog/inside-it/throwaway-prototyping/) · [Simplicable: Evolutionary vs Throwaway Prototype](https://simplicable.com/productivity/evolutionary-prototype-vs-throwaway-prototype) · [UXPin: Throwaway Prototyping](https://www.uxpin.com/studio/blog/throwaway-prototyping/)
