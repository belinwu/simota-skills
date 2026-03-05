# Requirements Traceability Pitfalls

> トレーサビリティの 8 大落とし穴、4 方向追跡、RTM 品質改善ガイド

## 1. トレーサビリティ 8 大落とし穴

| # | 落とし穴 | 問題 | 対策 |
|---|---------|------|------|
| **RT-01** | **不完全な要件** | 曖昧な要件 → テストケース/検証ステップ作成不能 | 要件は Atomic · Unambiguous · Testable · Attributed |
| **RT-02** | **変更未同期** | 要件変更時にマトリクス未更新 → リンク切れ | 変更発生時に即座にマトリクス更新 · CI ゲート統合 |
| **RT-03** | **命名不統一** | ID 形式がバラバラ → 検索・追跡・監査が困難 | 統一 ID 規約（REQ-XXX, AC-XXX）の厳守 |
| **RT-04** | **依存関係の見落とし** | 設計/要件収集段階で仮定・依存を記録しない | L1 に仮定リスト · L2-Dev に依存関係セクション |
| **RT-05** | **過度な構造化** | 不要な列・詳細を追加 → 維持コスト増大 | スコープに応じた必要最小限の構造（Full/Standard/Lite） |
| **RT-06** | **手動管理** | Excel/Word での手動 RTM → エラー多発・陳腐化 | 自動化ツール · ID リンクの自動検証 |
| **RT-07** | **片方向追跡のみ** | 前方追跡のみ → 変更の影響分析が不完全 | 双方向トレーサビリティ（Forward + Backward）必須 |
| **RT-08** | **孤立アイテム** | リンクなしの REQ/AC が存在 → 検証漏れ | Orphan 検出チェック · マトリクス完全性検証 |

---

## 2. 4 方向追跡（Four Types of Traceability）

### 概要

```
4 方向追跡モデル:
  1. Forward FROM requirements: 要件 → 設計・実装（要件が実装されているか）
  2. Backward TO requirements: 設計・実装 → 要件（実装が要件に紐付いているか）
  3. Forward FROM test cases: テスト → 要件（テストが要件をカバーしているか）
  4. Backward TO test cases: 要件 → テスト（要件にテストが存在するか）

最低限必須:
  - Forward FROM requirements（要件 → 実装の追跡）
  - Backward TO test cases（要件 → テストの追跡）

フル（推奨）:
  - 4 方向全て → 変更影響分析 · カバレッジ保証 · 監査対応
```

### Accord のレベル別対応

| スコープ | Forward (Req→Design) | Backward (Design→Req) | Forward (Test→Req) | Backward (Req→Test) |
|---------|:---:|:---:|:---:|:---:|
| **Full** | 必須 | 必須 | 必須 | 必須 |
| **Standard** | 必須 | 推奨 | 推奨 | 必須 |
| **Lite** | — | — | — | 必須（REQ→AC のみ） |

---

## 3. 良い要件の SMART 基準

```
高品質な要件の 5 属性:
  S — Specific（具体的）: 曖昧さなし、1つの解釈のみ
  M — Measurable（測定可能）: 検証可能な基準・数値を含む
  A — Attributed（帰属明確）: オーナー、優先度、出典が記録されている
  R — Referenceable（参照可能）: 一意の ID を持つ（REQ-XXX）
  T — Testable（テスト可能）: 定義されたテストまたは検査で検証可能

チェックリスト:
  □ 1つの要件 = 1つの事項（Atomic）
  □ 標準用語で記述（Unambiguous）
  □ テストで検証可能（Testable）
  □ 出典と優先度が記録されている（Attributed）
  □ 一意の ID がある（Uniquely Identified）
```

---

## 4. RTM メンテナンスのベストプラクティス

### 更新タイミング

| イベント | アクション |
|---------|----------|
| 新規 REQ 追加 | マトリクスに行を追加 · 対応する AC を仮作成 |
| REQ 変更 | 影響を受ける Design/API/AC を特定し更新 |
| REQ 削除 | 関連する Design/AC を Deprecated に · 孤立チェック |
| AC 追加/変更 | 対応 REQ とのリンクを確認 |
| 設計変更 | 影響を受ける REQ/AC を逆方向追跡で特定 |
| Sprint 完了 | Status フィールドを更新（Draft → Review → Approved） |

### 整合性スコア

```
Traceability_Score = (Linked_Items / Total_Items) × 100

目標:
  Full スコープ:     ≥ 95%
  Standard スコープ:  ≥ 85%
  Lite スコープ:     ≥ 70%（REQ→AC のみ）

スコア低下時のアクション:
  < 70%: 即時対応 — Orphan アイテムの棚卸し
  70-85%: 次回レビューで対応 — リンク追加
  > 85%: 良好 — 定期メンテナンス継続
```

---

## 5. Accord との連携

```
Accord での活用:
  1. BRIDGE フェーズで 4 方向追跡の検証を実行
  2. VERIFY フェーズで Traceability_Score を計算
  3. RT-01〜08 のチェックリストを ELABORATE 中に適用
  4. SMART 基準を L1 の REQ 品質チェックに統合
  5. UNIFY で Traceability_Completeness のトレンドを追跡

品質ゲート:
  - Full スコープで Traceability_Score < 95% → 警告
  - Orphan REQ（AC なし）を検出 → AC 追加を要求
  - Orphan AC（REQ なし）を検出 → REQ 追加 or AC 削除を提案
  - 要件が SMART 基準を満たさない場合 → リファインメント提案
```

**Source:** [TestRail: Requirements Traceability Matrix Guide](https://www.testrail.com/blog/requirements-traceability-matrix/) · [Security Compass: Four Types of Requirements Traceability](https://www.securitycompass.com/blog/four-types-of-requirements-traceability/) · [PTC: 8 Tips for Writing Better Requirements](https://www.ptc.com/en/blogs/alm/8-tips-for-writing-requirements) · [LambdaTest: RTM Comprehensive Guide](https://www.lambdatest.com/learning-hub/requirements-traceability-matrix) · [Inflectra: Requirements Traceability](https://www.inflectra.com/Ideas/Topic/Requirements-Traceability.aspx) · [Qualityze: Requirements Traceability](https://www.qualityze.com/blogs/requirements-traceability)
