# Cost Analysis Reference — Void

Cost-of-Keeping Score計算方法、5次元評価基準、Removal Risk Score。

---

## Cost-of-Keeping Score (0-10)

### Formula

```
CoK Score = Σ (Dimension_i Score × Weight_i)

Dimensions:
  1. Maintenance     (Weight: 0.25)
  2. Testing         (Weight: 0.20)
  3. Cognitive Load  (Weight: 0.25)
  4. Coupling        (Weight: 0.15)
  5. Replaceability  (Weight: 0.15)
```

---

## 5 Dimensions — Scoring Rubric

### 1. Maintenance (25%)

メンテナンスの頻度・難易度・コスト。

| Score | Label | Criteria |
|-------|-------|----------|
| 0-2 | **Stable** | 過去12ヶ月でバグ修正0-1件。変更不要で安定 |
| 3-4 | **Low** | 年に2-3回の軽微なメンテナンス。依存更新程度 |
| 5-6 | **Moderate** | 月1回程度のメンテナンス。定期的な修正が必要 |
| 7-8 | **High** | 週次でのメンテナンス。頻繁なバグ修正 |
| 9-10 | **Critical** | 常時メンテナンスが必要。壊れやすく修正困難 |

**Evidence sources:** Git log frequency, bug tracker tickets, on-call incidents

### 2. Testing (20%)

テストの複雑さ・実行コスト・信頼性。

| Score | Label | Criteria |
|-------|-------|----------|
| 0-2 | **Simple** | テストが簡潔で高速。セットアップ不要 |
| 3-4 | **Moderate** | テスト存在し安定。多少のセットアップ必要 |
| 5-6 | **Complex** | テストセットアップが複雑。外部依存あり |
| 7-8 | **Fragile** | フレーキーテストあり。CI時間に大きく影響 |
| 9-10 | **Untestable** | テスト困難 or テストなし。手動検証に依存 |

**Evidence sources:** Test suite runtime, flaky test reports, test setup complexity

### 3. Cognitive Load (25%)

理解・修正に必要な認知的コスト。

| Score | Label | Criteria |
|-------|-------|----------|
| 0-2 | **Self-evident** | コードが自明。新メンバーでも即理解 |
| 3-4 | **Clear** | 多少のドメイン知識が必要だが読めば分かる |
| 5-6 | **Contextual** | 関連コードの理解が必要。暗黙の前提あり |
| 7-8 | **Complex** | 深い文脈知識が必要。「分かる人にしか分からない」 |
| 9-10 | **Opaque** | 元の作者でも理解困難。トライバルナレッジ依存 |

**Evidence sources:** Code review time, onboarding feedback, "WTF per minute" count

### 4. Coupling (15%)

他コンポーネントとの結合度。

| Score | Label | Criteria |
|-------|-------|----------|
| 0-2 | **Isolated** | 完全に独立。変更が他に波及しない |
| 3-4 | **Loosely coupled** | 明確なインターフェース経由の依存のみ |
| 5-6 | **Moderately coupled** | 複数モジュールと相互依存 |
| 7-8 | **Tightly coupled** | 変更が広範囲に波及。Shotgun Surgery パターン |
| 9-10 | **Entangled** | 分離困難。変更すると予測不能な副作用 |

**Evidence sources:** Import/dependency graph, change coupling analysis, blast radius tests

### 5. Replaceability (15%)

代替手段の容易さ（逆スコア: 置換困難なほど高い）。

| Score | Label | Criteria |
|-------|-------|----------|
| 0-2 | **Trivially replaceable** | 標準ライブラリや1行で代替可能 |
| 3-4 | **Easily replaceable** | 既存の代替手段があり、移行コスト低い |
| 5-6 | **Replaceable with effort** | 代替手段はあるが、移行に数日〜1週間 |
| 7-8 | **Difficult to replace** | カスタム実装が必要。移行に数週間 |
| 9-10 | **Irreplaceable** | 代替手段なし。再構築に数ヶ月 |

**Evidence sources:** Alternative library search, migration effort estimate

---

## Score Interpretation

| CoK Score | Label | Recommendation |
|-----------|-------|---------------|
| 0.0 - 2.0 | **Low cost** | KEEP（維持コストは許容範囲） |
| 2.1 - 4.0 | **Moderate** | KEEP-WITH-WARNING（定期レビュー推奨） |
| 4.1 - 6.0 | **Elevated** | SIMPLIFY候補（コスト削減の余地あり） |
| 6.1 - 8.0 | **High** | REMOVE/SIMPLIFY強く推奨 |
| 8.1 - 10.0 | **Critical** | REMOVE最優先。即座にアクション |

---

## Removal Risk Score (0-10)

削除した場合のリスクを定量化する。CoK Scoreとの組み合わせで判断する。

### Formula

```
Removal Risk = Σ (Risk_Dimension_i × Weight_i)

Risk Dimensions:
  1. User Impact        (Weight: 0.30)
  2. Data Integrity     (Weight: 0.25)
  3. System Stability   (Weight: 0.25)
  4. Reversibility      (Weight: 0.20)
```

### Risk Dimensions

| Dimension | 0 (Low Risk) | 5 (Medium) | 10 (High Risk) |
|-----------|-------------|------------|----------------|
| **User Impact** | ユーザーなし | 少数の内部ユーザー | 多数の外部ユーザー |
| **Data Integrity** | データに影響なし | 移行で対応可 | データロスの可能性 |
| **System Stability** | 影響なし | 部分的な影響 | システムダウンの可能性 |
| **Reversibility** | 即座にロールバック可能 | 数時間で復旧可能 | 復旧困難/不可能 |

---

## Decision Matrix: CoK × Removal Risk

```
              Removal Risk
              Low(0-3)    Med(4-6)    High(7-10)
CoK Score
High(7-10)    REMOVE      SIMPLIFY    DEFER+PLAN
Med(4-6)      SIMPLIFY    DEFER       KEEP-WITH-WARNING
Low(0-3)      KEEP        KEEP        KEEP
```

---

## Score Calculation Template

```yaml
cost_of_keeping:
  target: "<対象名>"
  dimensions:
    maintenance:     { score: X, evidence: "string", weight: 0.25 }
    testing:         { score: X, evidence: "string", weight: 0.20 }
    cognitive_load:  { score: X, evidence: "string", weight: 0.25 }
    coupling:        { score: X, evidence: "string", weight: 0.15 }
    replaceability:  { score: X, evidence: "string", weight: 0.15 }
  total_score: "X.X"
  label: "LOW | MODERATE | ELEVATED | HIGH | CRITICAL"

removal_risk:
  dimensions:
    user_impact:     { score: X, evidence: "string", weight: 0.30 }
    data_integrity:  { score: X, evidence: "string", weight: 0.25 }
    system_stability: { score: X, evidence: "string", weight: 0.25 }
    reversibility:   { score: X, evidence: "string", weight: 0.20 }
  total_score: "X.X"

decision_matrix_result: "REMOVE | SIMPLIFY | DEFER | KEEP-WITH-WARNING | KEEP"
confidence: "X%"
next_phase: "→ SUBTRACT (削減パターン選択)"
```
