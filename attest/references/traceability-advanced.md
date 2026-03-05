# Advanced Traceability Techniques

> 双方向トレーサビリティ、自動化、ギャップ分析、カバレッジ最適化

## 1. 双方向トレーサビリティ（BDTM）

### 概要

```
Forward Traceability:
  要件 → 設計 → 実装 → テスト
  「すべての要件が実装されているか？」

Backward Traceability:
  テスト → 実装 → 設計 → 要件
  「すべてのテスト/コードに要件根拠があるか？」

Bidirectional = Forward + Backward:
  - 未実装の要件を検出（Forward Gap）
  - 要件のないコード/テストを検出（Backward Gap = Gold Plating）
```

### Attest における双方向マッピング

| 方向 | マッピング | 検出する問題 |
|------|----------|------------|
| **Forward** | AC-ID → 実装ファイル:行 → テストファイル:行 | 未実装の基準（FAIL） |
| **Backward** | 実装ファイル → AC-ID | 要件のない実装（Gold Plating） |
| **Test Forward** | AC-ID → テストケース | テストされていない基準 |
| **Test Backward** | テストケース → AC-ID | 基準のないテスト（Orphan Test） |

### 出力フォーマット

```yaml
BIDIRECTIONAL_TRACEABILITY:
  forward:
    total_criteria: 12
    mapped_to_implementation: 10
    mapped_to_tests: 8
    gaps:
      - criterion_id: AC-LOGIN-007
        type: FORWARD_GAP
        description: "実装マッピングなし"
      - criterion_id: AC-LOGIN-003
        type: TEST_GAP
        description: "実装あり、テストなし"
  backward:
    orphan_implementations:
      - file: src/utils/legacyAuth.ts
        description: "どの基準にもマッピングされない実装"
    orphan_tests:
      - file: test/deprecated.test.ts
        description: "どの基準にもマッピングされないテスト"
  coverage:
    implementation: 83%  # 10/12
    test: 67%           # 8/12
    full_chain: 67%     # 要件→実装→テスト完全チェーン
```

---

## 2. ギャップ分析

### 4 種類のギャップ

| ギャップタイプ | 定義 | リスク | 検出方法 |
|--------------|------|--------|---------|
| **Implementation Gap** | 基準に対応する実装がない | 高 | Forward トレース |
| **Test Gap** | 実装はあるがテストがない | 中-高 | Forward トレース |
| **Specification Gap** | 実装があるが基準がない | 中 | Backward トレース |
| **Coverage Gap** | テストはあるが不十分 | 中 | カバレッジ分析 |

### ギャップ優先度マトリクス

```
       基準あり     基準なし
実装あり  [正常]      [Spec Gap]
         テストあり   → 仕様追加を推奨
         テストなし
         [Test Gap]

実装なし  [Impl Gap]  [N/A]
         → 実装追加    対象外
```

### AUDIT モードでのギャップ検出

```
AUDIT モードの追加分析:
  1. 基準 → 実装の Forward マッピング構築
  2. 実装 → テストの Forward マッピング構築
  3. テスト → 基準の Backward マッピング構築
  4. 各ギャップタイプを分類
  5. カバレッジ率を算出
  6. ギャップレポートを生成
```

---

## 3. トレーサビリティ自動化

### 自動マッピング手法

| 手法 | 説明 | 精度 | 適用場面 |
|------|------|------|---------|
| **命名規約ベース** | ファイル名/テスト名から AC-ID を推定 | 高 | テスト名に AC-ID を含む場合 |
| **コメント/タグベース** | `@covers AC-LOGIN-001` タグを検索 | 高 | タグ付けが徹底されている場合 |
| **パターンマッチ** | ルート/ハンドラ名と基準のキーワードを照合 | 中 | 命名規約が一貫している場合 |
| **コード検索** | 基準キーワードで grep | 中-低 | フォールバック手法 |
| **LLM 推論** | AI がコードの意図と基準を照合 | 中 | 他手法で不明な場合 |

### 推奨タグ規約

```
コード側:
  // @requirement AC-LOGIN-001
  // @covers AC-LOGIN-001, AC-LOGIN-002

テスト側:
  describe('AC-LOGIN-001: Valid credentials grant access', () => { ... })
  // @criterion AC-LOGIN-001

Gherkin 側:
  @AC-LOGIN-001
  Scenario: Successful login with valid credentials
```

---

## 4. カバレッジ最適化

### カバレッジレベル

| レベル | 定義 | 計算式 |
|-------|------|--------|
| **L1: 要件カバレッジ** | 実装にマッピングされた基準の割合 | 実装あり基準 / 全基準 |
| **L2: テストカバレッジ** | テストにマッピングされた基準の割合 | テストあり基準 / 全基準 |
| **L3: 完全チェーンカバレッジ** | 基準→実装→テストの完全チェーン | 完全チェーン基準 / 全基準 |
| **L4: 結果カバレッジ** | テストが PASS の基準の割合 | PASS 基準 / 全基準 |

### カバレッジ閾値

| レベル | CERTIFIED | CONDITIONAL | REJECTED |
|-------|-----------|-------------|----------|
| L1 | ≥ 90% | ≥ 70% | < 70% |
| L2 | ≥ 80% | ≥ 60% | < 60% |
| L3 | ≥ 70% | ≥ 50% | < 50% |

---

## 5. 規制対応トレーサビリティ

### 規制業界の要件

| 規格 | トレーサビリティ要件 | Attest の対応 |
|------|-------------------|-------------|
| **FDA 21 CFR Part 11** | 要件→テスト→結果の完全トレース | AUDIT モード + 完全チェーン |
| **ISO 26262** | ASIL レベル別の双方向トレース | 優先度マッピング |
| **DO-178C** | 要件→設計→コード→テストの 4 層 | 拡張トレーサビリティ |
| **ISO 29148** | 要件品質特性の検証 | specification-quality.md 連携 |

### コンプライアンスレポート拡張

```yaml
REGULATORY_TRACEABILITY:
  standard: "FDA 21 CFR Part 11"
  bidirectional: true
  chain_coverage: 92%
  gaps:
    forward: 1  # 基準→実装なし
    backward: 0  # 要件のない実装なし
    test: 2     # テストなし
  audit_trail:
    - timestamp: "2025-03-05T10:30:00Z"
      action: "Initial compliance verification"
      result: "CONDITIONAL — 2 test gaps remain"
```

---

## 6. トレーサビリティのアンチパターン

| アンチパターン | 症状 | 対策 |
|--------------|------|------|
| **Manual-Only RTM** | Excel で手動管理、すぐに陳腐化 | タグベース自動マッピング |
| **One-Way Only** | Forward のみで Backward を無視 | 双方向トレース必須化 |
| **Snapshot RTM** | プロジェクト開始時のみ作成 | 継続的更新（AUDIT モード定期実行） |
| **Over-Granular** | 全変数・全行をマッピング | 基準レベルの粒度を維持 |
| **Orphan Tolerance** | 要件のないコードを許容 | Backward Gap を MEDIUM 以上で報告 |

**Source:** [Perforce: Requirements Traceability Matrix](https://www.perforce.com/resources/alm/requirements-traceability-matrix) · [Parasoft: Requirements Traceability](https://www.parasoft.com/solutions/requirements-traceability/) · [aqua cloud: AI Requirement Traceability](https://aqua-cloud.io/ai-requirement-traceability/) · [TestRail: RTM How-To Guide](https://www.testrail.com/blog/requirements-traceability-matrix/) · [Softacus: RVTM](https://softacus.com/blog/requirements-verification-traceability-matrix-rvtm)
