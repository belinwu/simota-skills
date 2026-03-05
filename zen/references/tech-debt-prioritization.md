# Technical Debt Prioritization & Safe Refactoring Strategies

> 技術的負債の計測・優先順位付け、ホットスポット分析、安全なリファクタリング戦略

## 1. 技術的負債の分類

### 5 つの負債タイプ

| タイプ | 説明 | 検出方法 |
|--------|------|---------|
| **Complex Hot Code** | 高複雑度 × 高変更頻度 | Hotspot 分析 |
| **Decaying Code** | 時間とともに品質が悪化 | Code Health トレンド |
| **Coordination Problems** | 組織構造がコードに反映 | 開発者フラグメンテーション分析 |
| **Excess Coupling** | 過度な依存関係 | 依存グラフ分析 |
| **Developer Fragmentation** | 特定コードへの散漫なチーム関与 | バージョン管理データ |

---

## 2. ホットスポット分析

### 基本原理

```
ホットスポット = 高変更頻度 × 低コード品質

研究知見:
  - 開発活動はコードベースの小さな部分に集中
  - ホットスポットはコード全体の 2-3% のみ
  - しかし全コミットの 11-16% を占める
  - 全報告・解決バグの 25-70% がホットスポットに集中
  - 不健全なコードは健全なコードの 15 倍の欠陥を持つ
```

### 優先順位マトリクス

```
          変更頻度 高
              │
    ┌─────────┼─────────┐
    │ 監視     │ 最優先   │
    │ (低品質  │ (低品質  │
    │  低頻度) │  高頻度) │
    ├─────────┼─────────┤
    │ 放置可   │ 維持     │
    │ (高品質  │ (高品質  │
    │  低頻度) │  高頻度) │
    └─────────┼─────────┘
              │
          変更頻度 低
    低品質 ←──────→ 高品質
```

### Zen での適用

```
Atlas → Zen の連携（Pattern E: Complexity Hotspot Fix）:
  1. Atlas がホットスポットを特定
  2. Zen が最優先ゾーンから順にリファクタリング
  3. 1 ホットスポット = 1 Focused scope リファクタリング
  4. Before/After メトリクスで改善を確認
```

---

## 3. Code Health スコアリング

### CodeScene Code Health（参考指標）

```
スコア範囲: 1（深刻な品質問題）〜 10（健全なコード）

25+ のコンテキスト要因を統合:
  - 関数の長さ・複雑度
  - ネスト深度
  - 引数の数
  - コードの重複
  - 命名の明瞭さ
  - モジュール結合度
  ...

影響:
  Score 1-3: 不健全 → 2x 遅い開発、15x の欠陥
  Score 4-6: 要注意 → 改善の余地あり
  Score 7-10: 健全 → 維持すべき状態
```

### Zen の内部品質指標

```
Zen が Before/After で計測するもの:
  □ Cyclomatic Complexity (CC)
  □ Cognitive Complexity
  □ Nesting Depth
  □ Function Length (LOC)
  □ Parameter Count
  □ Code Duplication %

目標:
  - CC: 15-25% 削減
  - Cognitive: 対象関数を threshold 以下に
  - Nesting: ≤ 3 に削減
  - Function LOC: ≤ 50
  - Parameters: ≤ 5
```

---

## 4. 安全なリファクタリング戦略

### Strategy 1: Strangler Fig Pattern

```
定義: レガシーコードを新しいコードで段階的に包み込み、最終的に置き換える

手順:
  1. Assessment: 低依存・高ビジネス価値のコンポーネントを特定
  2. Routing Layer: ファサード/ゲートウェイで新旧を切り替え
  3. First Service: 小さな非クリティカルコンポーネントから開始
  4. Shadow Validation: 本番トラフィックで新旧の出力を比較
  5. Gradual Migration: 段階的にトラフィックを移行（10% → 50% → 100%）
  6. Decommission: 完全移行後にレガシーコードを削除

利点:
  - ダウンタイムなし
  - 各段階で独立したロールバック可能
  - インクリメンタルな検証

適用場面:
  - 大規模なモジュール置換
  - フレームワーク移行
  - API バージョニング
```

### Strategy 2: Branch by Abstraction

```
定義: 抽象化レイヤーを導入し、新旧の実装を共存させる

手順:
  1. 既存コードに抽象インターフェースを導入
  2. 既存実装をインターフェース経由で呼び出すよう変更
  3. 新しい実装を同一インターフェースで作成
  4. Feature flag で新旧を切り替え
  5. 新実装が安定したら旧実装を削除

利点:
  - メインブランチ上で段階的に移行
  - 長期ブランチを避けられる
  - 既存コードとの共存が可能

Strangler Fig との違い:
  - Strangler Fig: コンポーネント全体の置換
  - Branch by Abstraction: 内部実装の段階的置換
```

### Strategy 3: Parallel Change (Expand-Contract)

```
手順:
  1. Expand: 新しいインターフェース/実装を追加（旧は残す）
  2. Migrate: 呼び出し元を段階的に新インターフェースへ移行
  3. Contract: 全移行完了後に旧インターフェースを削除

Zen での適用:
  - public API のリネーム時に使用
  - 後方互換性を維持しながらの改善
  - 「Ask first」の変更を安全に実行
```

---

## 5. ROI 測定フレームワーク

### 3 軸の測定

| 軸 | メトリクス | 例 |
|----|-----------|-----|
| **技術** | コード品質、負債削減、パフォーマンス | CC 20% 削減 |
| **ビジネス** | 開発速度、欠陥率、Time-to-Market | デプロイ頻度 2x |
| **コスト** | 総所有コスト削減、メンテナンス節約 | メンテナンス工数 30% 削減 |

### IT 予算の現実

```
組織は IT 予算の 60-80% を既存システムの維持に使用
→ 戦略的リファクタリングで新機能開発の余地を確保
→ 全てをリファクタリングするのではなく、ホットスポットに集中
```

---

## 6. Zen の優先順位付けガイドライン

```
判断フロー:

1. ホットスポットか？（変更頻度 高 × 品質 低）
   → Yes: 最優先でリファクタリング
   → No: 次の判断へ

2. 直近で変更予定があるか？
   → Yes: Boy Scout Rule で改善
   → No: 次の判断へ

3. バグの温床になっているか？
   → Yes: 重点的にリファクタリング
   → No: 放置可（技術的負債として記録）

原則:
  - 全てを直そうとしない（Perfectionism アンチパターン回避）
  - ROI の高い箇所から着手
  - 1 回の改善は Scope tier 内に収める
```

**Source:** [CodeScene: Prioritize Technical Debt](https://codescene.com/blog/tech-debt-examples-prioritize-technical-debt-with-codescene) · [CodeScene: Code Health Metric](https://codescene.com/product/code-health) · [CodeScene: Behavioral Code Analysis](https://codescene.com/product/behavioral-code-analysis) · [Gocodeo: Strangler Fig Pattern](https://www.gocodeo.com/post/how-the-strangler-fig-pattern-enables-safe-and-gradual-refactoring) · [AWS: Branch by Abstraction](https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-decomposing-monoliths/branch-by-abstraction.html) · [Martin Fowler: Strangler Fig](https://martinfowler.com/bliki/StranglerFigApplication.html)
