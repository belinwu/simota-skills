# Proposal Templates Reference — Void

Subtraction Proposalテンプレート、severity x confidence マトリクス。

---

## Severity × Confidence Matrix

提案の優先度を severity（影響度）と confidence（確信度）の2軸で分類する。

```
              Confidence
              High(80-100%)  Med(60-79%)   Low(<60%)
Severity
Critical(8-10)  ACT NOW        VERIFY FIRST   DO NOT PROPOSE*
High(6-7)       PRIORITIZE     SCHEDULE       DEFER
Medium(4-5)     BATCH          BATCH          SKIP
Low(0-3)        OPPORTUNISTIC  SKIP           SKIP

* confidence < 60% では提案しない（Never ルール）
```

---

## Recommendation Classification

| Recommendation | Criteria | Next Agent |
|---------------|----------|------------|
| **REMOVE** | CoK >= 7, Risk <= 5, Confidence >= 80% | → Sweep（削除実行）→ Magi（承認） |
| **SIMPLIFY** | CoK 4-8, Risk 3-7 | → Zen（リファクタリング実行） |
| **DEFER** | Risk >= 7 or Data不足 | → 定期レビューにスケジュール |
| **KEEP-WITH-WARNING** | CoK >= 5 but 正当な理由あり | → 警告を記録、次回監査で再評価 |

---

## Template 1: Full Audit Report

プロジェクト全体 or モジュール/プロセス単位の包括的監査。

```markdown
# Void: Subtraction Audit Report

**Audit Scope:** [プロジェクト名 / モジュール名 / プロセス名]
**Date:** YYYY-MM-DD
**Targets Evaluated:** X

---

## Executive Summary

| Metric | Value |
|--------|-------|
| 評価対象数 | X |
| REMOVE推奨 | X |
| SIMPLIFY推奨 | X |
| DEFER | X |
| KEEP-WITH-WARNING | X |
| 推定メンテナンス/運用コスト削減 | X% |
| 推定認知負荷削減 | X% |

---

## Findings

### [対象名 1]

| Item | Value |
|------|-------|
| Domain | Code / Feature / Process / Document / Design / Dependency / Configuration / Specification |
| Category | Feature / Abstraction / Scope / Dependency / Configuration / Process / Document / Design_Spec |
| CoK Score | X.X / 10 |
| Removal Risk | X.X / 10 |
| Confidence | X% |
| Recommendation | REMOVE / SIMPLIFY / DEFER / KEEP-WITH-WARNING |

**5 Questions Summary:**
1. **Who uses it?** [回答]
2. **What breaks?** [回答]
3. **Last changed?** [日付 + staleness]
4. **Why built?** [回答]
5. **Keeping cost?** [回答]

**Blast Radius:** [artifacts affected: X, verification affected: X, users: X]
**Subtraction Pattern:** [適用パターン名]
**Routing:** → [次のエージェント]

---

## Batch Subtraction Plan

| Priority | Target | Domain | Recommendation | CoK | Risk | Pattern | Agent |
|----------|--------|--------|---------------|-----|------|---------|-------|
| 1 | [名前] | Feature | REMOVE | X.X | X.X | Sunset | Sweep |
| 2 | [名前] | Code | SIMPLIFY | X.X | X.X | Collapse | Zen |
| ... | | | | | | | |

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| [リスク] | HIGH/MED/LOW | HIGH/MED/LOW | [対策] |
```

---

## Template 2: Single Target Evaluation

単一対象のYAGNI検証（任意ドメイン対応）。

```markdown
# Void: Target Evaluation — [対象名]

**Domain:** [Code / Feature / Process / Document / Design / Dependency / Configuration / Specification]

## 5 Existence Questions

### Q1: Who uses it?
[詳細回答]
**Confidence:** HIGH / MEDIUM / LOW

### Q2: What breaks if removed?
[詳細回答]
**Blast Radius:** NONE / LOCAL / CROSS_MODULE / PUBLIC_API / DATA

### Q3: When was it last meaningfully changed?
[日付]
**Staleness:** FRESH / AGING / STALE / FOSSILIZED

### Q4: Why was it built?
[詳細回答]
**Still Valid:** YES / PARTIALLY / NO

### Q5: What does keeping it cost?
[詳細回答]

## Cost-of-Keeping Score

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Upkeep | X/10 | [根拠] |
| Verification | X/10 | [根拠] |
| Cognitive Load | X/10 | [根拠] |
| Entanglement | X/10 | [根拠] |
| Replaceability | X/10 | [根拠] |
| **Weighted Total** | **X.X/10** | |

## Removal Risk: X.X/10

## Recommendation: REMOVE / SIMPLIFY / DEFER / KEEP-WITH-WARNING
**Confidence:** X%
**Pattern:** [適用パターン]
**Routing:** → [次のエージェント]
```

---

## Template 3: Scope Cut Proposal

機能/プロセス/ドキュメントのスコープ縮小提案。

```markdown
# Void: Scope Cut Proposal — [対象名]

## Current Scope
[現在の対応範囲の説明]

## Usage Analysis

| Variation | Usage% | Maintenance Cost | Recommendation |
|-----------|--------|-----------------|---------------|
| [バリエーションA] | X% | LOW | KEEP |
| [バリエーションB] | X% | LOW | KEEP |
| [バリエーションC] | X% | HIGH | CUT |
| [バリエーションD] | X% | CRITICAL | CUT |

## Proposed Scope
[縮小後の対応範囲]

## Impact
- **Coverage retained:** X%
- **Maintenance/operation reduction:** X%
- **Artifacts affected:** X
- **Verification affected:** X
```

---

## Template 4: Quick YAGNI Check

軽量な存在確認（5分以内）。

```markdown
# Void: Quick YAGNI Check — [対象名]

**Domain:** [Code / Feature / Process / Document / Design / Dependency / Configuration / Specification]

| Question | Answer | Signal |
|----------|--------|--------|
| Who uses it? | [1文] | GREEN / YELLOW / RED |
| What breaks? | [1文] | GREEN / YELLOW / RED |
| Last changed? | [日付] | GREEN / YELLOW / RED |
| Why built? | [1文] | GREEN / YELLOW / RED |
| Keeping cost? | [1文] | GREEN / YELLOW / RED |

**Quick Verdict:** KEEP / INVESTIGATE FURTHER / LIKELY REMOVE
**CoK Estimate:** LOW / MODERATE / HIGH
```

---

## Template 5: Batch Subtraction Plan

複数対象の一括削減計画。

```markdown
# Void: Batch Subtraction Plan

**Scope:** [対象範囲]
**Targets:** X items

## Priority Queue

| # | Target | Domain | Category | CoK | Risk | Conf% | Rec | Pattern | Agent |
|---|--------|--------|----------|-----|------|-------|-----|---------|-------|
| 1 | [名前] | Feature | Feature | X.X | X.X | X% | REMOVE | Sunset | Sweep |
| 2 | [名前] | Code | Abstraction | X.X | X.X | X% | SIMPLIFY | Collapse | Zen |
| 3 | [名前] | Process | Process | X.X | X.X | X% | REMOVE | Pruning | Magi |
| ... | | | | | | | | | |

## Execution Order
1. [最初に実行すべき項目と理由]
2. [次に実行すべき項目]
3. ...

## Aggregate Impact
- Total artifacts affected: X
- Total verification affected: X
- Estimated maintenance/operation reduction: X%
- Estimated cognitive load reduction: X%

## Route to Magi
[バッチ承認が必要な場合のMagiへの要約]
```
