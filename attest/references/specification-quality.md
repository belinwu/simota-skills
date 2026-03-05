# Specification Quality & Requirement Smells

> 仕様品質の評価、要件スメルの分類、曖昧性検出パターン、受入基準の品質改善

## 1. 要件スメル（Requirement Smells）分類

### 12 カテゴリ

| # | スメルタイプ | 定義 | 深刻度 | 頻度 |
|---|------------|------|--------|------|
| 1 | **Ambiguity** | 複数の解釈が可能な記述 | 高 (80%) | 高 (70%) |
| 2 | **Verifiability** | テスト・検証が不可能な記述 | 高 (80%) | 中 |
| 3 | **Consistency** | 他の要件と矛盾する記述 | 高 (60%) | 中 (40%) |
| 4 | **Completeness** | 必要な情報が欠落している | 中-高 | 中 |
| 5 | **Complexity** | 過度に複雑な記述 | 中 | 高 (70%) |
| 6 | **Correctness** | 事実と異なる記述 | 高 | 低 |
| 7 | **Traceability** | 上位要件との紐付けがない | 中 | 中 |
| 8 | **Understandability** | 読者が理解困難な記述 | 中 | 低 |
| 9 | **Redundancy** | 同一要件の重複記述 | 低 | 中 |
| 10 | **Reusability** | 再利用不可能な特化記述 | 低 | 低 |
| 11 | **Relevancy** | プロジェクトスコープ外の記述 | 低 | 低 |
| 12 | **Undefined** | 分類不能な品質問題 | 可変 | 低 |

深刻度・頻度は研究者調査（2025年）に基づく。

---

## 2. 曖昧性の具体パターン

### 危険な表現カタログ

| カテゴリ | 危険な表現例 | 問題 | 改善例 |
|---------|------------|------|--------|
| **主観的形容詞** | fast, easy, user-friendly, intuitive | 測定基準なし | "200ms 以内に応答" |
| **曖昧な副詞** | quickly, efficiently, seamlessly | 定量化不能 | "3 ステップ以内で完了" |
| **最上級表現** | best, most efficient, highest quality | 比較基準なし | "SLA 99.9% を満たす" |
| **比較表現** | better, faster, more reliable | 比較対象不明 | "現行比 50% の応答時間改善" |
| **抜け穴表現** | if possible, as appropriate, when feasible | 実装判断を曖昧に | "必ず実装する" or 削除 |
| **曖昧な代名詞** | it, they, the system | 参照先が不明 | 具体的なコンポーネント名 |
| **未定義参照** | "See related document", "As discussed" | 参照先が存在しない/不明 | 具体的なドキュメント名とセクション |
| **否定形** | "not slow", "not complex" | 肯定的な基準が不明 | "応答時間 500ms 以下" |
| **開放的基準** | "etc.", "and so on", "among others" | 範囲が無限 | 完全な列挙 |

### Attest での検出戦略

```
検出フロー:
  1. 仕様テキストから上記パターンをスキャン
  2. 該当箇所に AMBIGUOUS_FLAG を発行
  3. ambiguity_type を分類:
     - UNMEASURABLE: 測定基準なし
     - SUBJECTIVE: 主観的判断が必要
     - INCOMPLETE: 情報欠落
     - CONTRADICTORY: 矛盾あり
     - OPEN_ENDED: 範囲が不明確
  4. suggested_clarification で具体的な改善案を提示
  5. Scribe/Accord にハンドオフ
```

---

## 3. 受入基準の品質パターン

### よい受入基準の特徴（INVEST + SMART）

| 特性 | 説明 | チェック方法 |
|------|------|------------|
| **Independent** | 他の基準に依存しない | 単独で検証可能か |
| **Negotiable** | 実装方法が限定されない | HOW ではなく WHAT を記述 |
| **Valuable** | ユーザー/ビジネス価値がある | "So that" が明確か |
| **Estimable** | 実装工数が見積もれる | スコープが明確か |
| **Small** | 1 スプリント内で完了可能 | 分割が必要ないか |
| **Testable** | テストで検証可能 | PASS/FAIL を判定可能か |

### 受入基準の品質アンチパターン

| アンチパターン | 症状 | 影響 | 対策 |
|--------------|------|------|------|
| **曖昧な言語** | "高速に動作する" | テスト不能 | 数値基準を定義 |
| **過多な基準** | 1 ストーリーに 20+ 基準 | 複雑すぎて実装困難 | ストーリーを分割 |
| **過少な基準** | 1 ストーリーに 1 基準 | 仕様不足、暗黙の前提 | 最低 3 基準（正常/異常/境界） |
| **NFR の欠落** | パフォーマンス/セキュリティなし | 本番で問題発覚 | NFR を明示的に含める |
| **コンテキスト欠落** | ユーザー視点がない | 実装者が意図を推測 | "As a [role]" を必ず含める |
| **基準の重複** | ストーリー内容の繰り返し | 冗長、メンテナンス困難 | 基準はストーリーを補完 |
| **実装詳細の混入** | "React で実装する" | 技術選択を仕様で制約 | WHAT を記述、HOW は除外 |

---

## 4. 仕様品質メトリクス

### 計測すべき指標

| メトリクス | 説明 | 目標 |
|-----------|------|------|
| **Ambiguity Rate** | 全基準中の AMBIGUOUS の割合 | < 10% |
| **Testability Rate** | TESTABLE 基準の割合 | > 80% |
| **Completeness Rate** | NFR を含む全側面がカバーされている割合 | > 90% |
| **Defect Injection Rate** | 要件起因のバグ割合 | < 10% |
| **Clarification Round-trips** | 仕様確認の往復回数 | ≤ 2 回 |

### ビジネスインパクト

```
要件関連の欠陥が全ソフトウェア欠陥の約 50% を占める（業界統計）

修正コストの増大:
  要件フェーズで発見: 1x
  設計フェーズで発見: 5x
  実装フェーズで発見: 10x
  テストフェーズで発見: 20x
  本番で発見: 100x

→ Attest の EXTRACT モードで早期に仕様品質を評価することの価値
```

---

## 5. Attest における仕様品質評価フロー

```
INGEST 時の品質チェック:
  1. 危険表現スキャン → AMBIGUOUS_FLAG 発行
  2. テスタビリティ分類 → TESTABLE / PARTIALLY_TESTABLE / AMBIGUOUS
  3. 完全性チェック → 正常系/異常系/境界値の各基準があるか
  4. 一貫性チェック → 基準間の矛盾検出（Contradiction プローブ連動）
  5. NFR チェック → パフォーマンス/セキュリティ/アクセシビリティの基準有無

品質スコア:
  GOOD: Ambiguity < 10%, Testability > 80%, Completeness > 90%
  FAIR: Ambiguity < 20%, Testability > 60%, Completeness > 70%
  POOR: 上記を満たさない → Scribe/Accord に仕様改善を推奨
```

**Source:** [arXiv: Characterizing Requirements Smells (2024)](https://arxiv.org/html/2404.11106v1) · [Nature: Multi-label Requirement Smells Classification (2025)](https://www.nature.com/articles/s41598-025-86673-w) · [Parallel HQ: Given-When-Then Acceptance Criteria](https://www.parallelhq.com/blog/given-when-then-acceptance-criteria) · [LinkedIn: Common Mistakes in Acceptance Criteria](https://www.linkedin.com/advice/3/what-most-common-mistakes-when-writing-acceptance)
