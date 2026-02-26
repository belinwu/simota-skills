# Cross-Reference & Traceability Guide

仕様パッケージ内の相互参照ルールとトレーサビリティマトリクスの構築・検証方法。

---

## ID Convention

| Level | Prefix | Example | Purpose |
|-------|--------|---------|---------|
| L1 | US-XXX | US-001 | ユーザーストーリー |
| L1 | REQ-XXX | REQ-001 | 機能要件 |
| L1 | NFR-XXX | NFR-001 | 非機能要件 |
| L2-Dev | API-XXX | API-001 | API仕様 |
| L2-Dev | DATA-XXX | DATA-001 | データモデル |
| L2-Design | DESIGN-XXX | DESIGN-001 | デザイン仕様 |
| L2-Design | FLOW-XXX | FLOW-001 | ユーザーフロー |
| L3 | AC-XXX | AC-001 | 受入基準（BDDシナリオ） |

### Cross-Reference Syntax

要件内で他IDを参照する場合:
```
**Linked:** REQ-001, DESIGN-002, AC-003
```

---

## Traceability Matrix

全IDの紐付けを一覧で管理。L3セクションに配置。

```markdown
| REQ | User Story | API | Data | Design | Flow | Acceptance | Status |
|-----|-----------|-----|------|--------|------|-----------|--------|
| REQ-001 | US-001 | API-001 | DATA-001 | DESIGN-001 | FLOW-001 | AC-001, AC-002 | Draft |
| REQ-002 | US-001 | API-002 | — | DESIGN-002 | FLOW-001 | AC-003 | Draft |
| REQ-003 | US-002 | — | DATA-002 | DESIGN-003 | FLOW-002 | AC-004, AC-005 | Draft |
```

### Matrix Completeness Rules

| Level | Required Links | Optional |
|-------|---------------|----------|
| Full | REQ → US, AC は必須 | API, DATA, DESIGN, FLOW |
| Standard | REQ → AC は必須 | US, API, DESIGN |
| Lite | REQ → AC のみ | 他すべて |

---

## Integrity Verification

仕様パッケージの整合性を検証するチェックリスト:

### 1. Forward Traceability（前方追跡）
- [ ] 全REQに少なくとも1つのACがリンクされているか
- [ ] 全USに少なくとも1つのREQがリンクされているか
- [ ] 孤立したREQ（どのUSにも属さない）がないか

### 2. Backward Traceability（後方追跡）
- [ ] 全ACが少なくとも1つのREQにリンクされているか
- [ ] 全DESIGN要素がREQに紐付いているか
- [ ] 全API仕様がREQに紐付いているか

### 3. Cross-Level Consistency（レベル間整合性）
- [ ] L0のスコープIn/Outが、L1のREQリストと一致しているか
- [ ] L1の非機能要件が、L2-Devの技術制約と矛盾しないか
- [ ] L2-DesignのフローがL1のユーザーストーリーを全てカバーしているか
- [ ] L3のBDDシナリオがL1の全Must REQをカバーしているか

### 4. Terminology Consistency（用語統一）
- [ ] 同じ概念に異なる名前を使っていないか
- [ ] 用語集が必要な場合、作成されているか
- [ ] チーム固有の略語に説明があるか

---

## Common Integrity Issues

| Issue | Detection | Fix |
|-------|----------|-----|
| Orphan REQ | REQがマトリクスにあるがACなし | AC追加 or REQ削除 |
| Orphan AC | ACがマトリクスにあるがREQなし | REQ追加 or AC削除 |
| Scope Drift | L1のREQがL0のスコープOutに含まれる | スコープ調整 or REQ削除 |
| Term Conflict | L2-BizとL2-Devで同じものに異なる名前 | 用語集で統一 |
| Level Gap | L2-Designにデザインがあるが対応REQなし | REQ追加（暗黙の要件の明示化） |

---

## Verification Timing

| Phase | Check |
|-------|-------|
| STRUCTURE後 | IDの採番規則が統一されているか |
| ELABORATE中 | 各セクション完了時に前方参照を確認 |
| BRIDGE | 全マトリクスの完全性検証（メインチェック） |
| VERIFY | 最終整合性チェック + 用語統一確認 |
