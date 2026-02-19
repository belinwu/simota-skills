# Cost Analysis Reference — Void

Cost-of-Keeping Score計算方法、5次元評価基準（ドメイン非依存）、Removal Risk Score。

---

## Cost-of-Keeping Score (0-10)

### Formula

```
CoK Score = Σ (Dimension_i Score × Weight_i)

Dimensions:
  1. Upkeep          (Weight: 0.25)
  2. Verification    (Weight: 0.20)
  3. Cognitive Load  (Weight: 0.25)
  4. Entanglement    (Weight: 0.15)
  5. Replaceability  (Weight: 0.15)
```

---

## 5 Dimensions — Scoring Rubric

### 1. Upkeep (25%)

維持・更新の頻度・難易度・コスト。

| Score | Label | Criteria |
|-------|-------|----------|
| 0-2 | **Stable** | 過去12ヶ月で修正/更新0-1件。変更不要で安定 |
| 3-4 | **Low** | 年に2-3回の軽微なメンテナンス |
| 5-6 | **Moderate** | 月1回程度のメンテナンス。定期的な修正/更新が必要 |
| 7-8 | **High** | 週次でのメンテナンス。頻繁な修正 |
| 9-10 | **Critical** | 常時メンテナンスが必要。壊れやすく修正困難 |

**Evidence by domain:**
- **Code:** Git log frequency, bug tracker tickets, on-call incidents
- **Process:** 手順書の更新頻度、例外対応の発生率
- **Document:** 内容の陳腐化速度、レビュー/更新周期
- **Dependency:** セキュリティパッチ頻度、breaking changes の頻度

### 2. Verification (20%)

正しく機能していることを検証するコスト。

| Score | Label | Criteria |
|-------|-------|----------|
| 0-2 | **Simple** | 検証が簡潔で高速。セットアップ不要 |
| 3-4 | **Moderate** | 検証手段が存在し安定。多少の準備が必要 |
| 5-6 | **Complex** | 検証のセットアップが複雑。外部依存あり |
| 7-8 | **Fragile** | 検証が不安定。結果にばらつき |
| 9-10 | **Unverifiable** | 検証困難 or 検証手段なし。手動確認に依存 |

**Evidence by domain:**
- **Code:** Test suite runtime, flaky test reports, test setup complexity
- **Process:** 品質チェックの手間、準拠確認のコスト
- **Document:** 正確性検証の難しさ、クロスリファレンスの手間
- **Configuration:** 設定変更の影響テストの複雑さ

### 3. Cognitive Load (25%)

理解・修正・運用に必要な認知的コスト。

| Score | Label | Criteria |
|-------|-------|----------|
| 0-2 | **Self-evident** | 自明。新メンバーでも即理解 |
| 3-4 | **Clear** | 多少のドメイン知識が必要だが理解可能 |
| 5-6 | **Contextual** | 関連コンテキストの理解が必要。暗黙の前提あり |
| 7-8 | **Complex** | 深い文脈知識が必要。「分かる人にしか分からない」 |
| 9-10 | **Opaque** | 元の作成者でも理解困難。トライバルナレッジ依存 |

**Evidence by domain:**
- **Code:** Code review time, onboarding feedback, "WTF per minute"
- **Process:** ルール/例外の覚えにくさ、新人が独力で実行できるまでの時間
- **Document:** 情報過多、矛盾、発見しにくさ、用語の不統一
- **Design:** ユーザーの迷い、サポート問い合わせ頻度

### 4. Entanglement (15%)

他の要素との結合度・依存関係の複雑さ。

| Score | Label | Criteria |
|-------|-------|----------|
| 0-2 | **Isolated** | 完全に独立。変更が他に波及しない |
| 3-4 | **Loosely coupled** | 明確なインターフェース経由の依存のみ |
| 5-6 | **Moderately coupled** | 複数要素と相互依存 |
| 7-8 | **Tightly coupled** | 変更が広範囲に波及 |
| 9-10 | **Entangled** | 分離困難。変更すると予測不能な副作用 |

**Evidence by domain:**
- **Code:** Import/dependency graph, change coupling analysis, blast radius tests
- **Process:** 他プロセスとの依存、ボトルネック発生頻度
- **Document:** 他文書との参照関係、更新連鎖の長さ
- **Configuration:** 設定間の暗黙の依存関係

### 5. Replaceability (15%)

代替手段の容易さ（逆スコア: 置換困難なほど高い）。

| Score | Label | Criteria |
|-------|-------|----------|
| 0-2 | **Trivially replaceable** | 標準的な方法で即代替可能 |
| 3-4 | **Easily replaceable** | 既存の代替手段があり、移行コスト低い |
| 5-6 | **Replaceable with effort** | 代替手段はあるが、移行に数日〜1週間 |
| 7-8 | **Difficult to replace** | カスタム対応が必要。移行に数週間 |
| 9-10 | **Irreplaceable** | 代替手段なし。再構築に数ヶ月 |

**Evidence by domain:**
- **Code:** Alternative library search, migration effort estimate
- **Process:** 代替ワークフローの存在、自動化の可能性
- **Document:** 代替情報源の有無、口頭伝承への依存度
- **Dependency:** 代替ライブラリ/サービスの成熟度

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
  domain: "<DOMAIN>"
  dimensions:
    upkeep:          { score: X, evidence: "string", weight: 0.25 }
    verification:    { score: X, evidence: "string", weight: 0.20 }
    cognitive_load:  { score: X, evidence: "string", weight: 0.25 }
    entanglement:    { score: X, evidence: "string", weight: 0.15 }
    replaceability:  { score: X, evidence: "string", weight: 0.15 }
  total_score: "X.X"
  label: "LOW | MODERATE | ELEVATED | HIGH | CRITICAL"

removal_risk:
  dimensions:
    user_impact:      { score: X, evidence: "string", weight: 0.30 }
    data_integrity:   { score: X, evidence: "string", weight: 0.25 }
    system_stability: { score: X, evidence: "string", weight: 0.25 }
    reversibility:    { score: X, evidence: "string", weight: 0.20 }
  total_score: "X.X"

decision_matrix_result: "REMOVE | SIMPLIFY | DEFER | KEEP-WITH-WARNING | KEEP"
confidence: "X%"
next_phase: "→ SUBTRACT (削減パターン選択)"
```
