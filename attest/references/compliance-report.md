# Compliance Report

Template and rules for generating specification compliance reports.

---

## Verdict Rules

### CERTIFIED

ALL of the following must be true:
- Every CRITICAL criterion: PASS
- Every HIGH criterion: PASS or NOT_TESTED (with runtime test plan)
- No CRITICAL adversarial probes open
- Traceability coverage ≥ 90%

### CONDITIONAL

ALL of the following must be true:
- No CRITICAL criterion: FAIL
- ≤3 HIGH criteria: PARTIAL
- Remediation plan attached for all non-PASS items
- Timeline for remediation specified
- No unresolved CONTRADICTION probes

### REJECTED

ANY of the following triggers REJECTED:
- Any CRITICAL criterion: FAIL
- >3 HIGH criteria: FAIL
- Unresolved CONTRADICTION adversarial probes
- Traceability coverage < 50%
- Specification has >5 AMBIGUOUS_FLAGs without clarification

---

## Report Template

```markdown
## Attest 適合レポート

### 概要

| 項目 | 値 |
|------|---|
| 仕様書 | [仕様書パス・名前] |
| 対象実装 | [ファイル/モジュール一覧] |
| 検証モード | FULL / EXTRACT / AUDIT / ADVERSARIAL |
| **判定** | **CERTIFIED** / **CONDITIONAL** / **REJECTED** |
| 検証日時 | YYYY-MM-DD |

### 基準サマリー

| 判定 | CRITICAL | HIGH | MEDIUM | LOW | 合計 |
|------|----------|------|--------|-----|------|
| PASS | X | X | X | X | X |
| PARTIAL | X | X | X | X | X |
| FAIL | X | X | X | X | X |
| NOT_TESTED | X | X | X | X | X |
| AMBIGUOUS | X | X | X | X | X |
| **合計** | X | X | X | X | **X** |

### トレーサビリティマトリクス

| 基準ID | 優先度 | 仕様セクション | 実装ファイル | テスト | 判定 |
|--------|--------|----------------|-------------|--------|------|
| AC-XXX-001 | CRITICAL | spec.md:L24 | src/xxx.ts:42 | test/xxx.test.ts:15 | PASS |
| AC-XXX-002 | HIGH | spec.md:L31 | — | — | FAIL |
| ... | | | | | |

**トレーサビリティカバレッジ:** XX% (基準→実装マッピング完了率)

### 検出事項（重大度順）

#### CRITICAL

**[F-001] AC-XXX-002: {基準の説明}**
- 判定: FAIL
- 検証手法: ABSENCE_CHECK
- エビデンス: {実装が見つからない旨の説明}
- 影響: {この違反の影響範囲}
- 推奨対応: Builder にて実装追加
- 対応エージェント: Builder

#### HIGH

**[F-002] AC-XXX-005: {基準の説明}**
- 判定: PARTIAL
- 検証手法: LOGIC_TRACE
- エビデンス: `src/xxx.ts:89` — {部分的に実装されている旨}
- ギャップ: {不足している部分の説明}
- 推奨対応: {具体的な修正内容}
- 対応エージェント: Builder

#### MEDIUM / LOW

[同形式で記載]

### 敵対的プローブ結果

| Probe ID | カテゴリ | 説明 | リスク | 仕様ギャップ |
|----------|---------|------|--------|-------------|
| PRB-001 | Boundary | {説明} | HIGH | {仕様に不足している内容} |
| PRB-002 | Omission | {説明} | MEDIUM | {仕様に不足している内容} |
| PRB-003 | Implicit | {説明} | LOW | {暗黙の前提} |

### 仕様品質フィードバック

| 問題 | 種別 | 影響 | 推奨改善 |
|------|------|------|---------|
| {曖昧な基準} | AMBIGUOUS | HIGH | {明確化の提案} |
| {欠落した要件} | OMISSION | MEDIUM | {追加すべき要件} |

### 改善計画（CONDITIONAL/REJECTEDの場合）

| # | 対応内容 | 対応エージェント | 優先度 | 見積もり |
|---|---------|----------------|--------|---------|
| 1 | AC-XXX-002 の実装追加 | Builder | CRITICAL | — |
| 2 | AC-XXX-005 のギャップ修正 | Builder | HIGH | — |
| 3 | BDDシナリオのテスト化 | Radar | HIGH | — |
| 4 | 仕様の曖昧性解消 | Scribe | MEDIUM | — |

### BDDシナリオ（生成済み）

合計: X シナリオ
- Happy Path: X
- Negative: X
- Boundary: X
- Edge Case: X

[シナリオファイルの参照先]
```

---

## Traceability Matrix Format

The traceability matrix maps: **Specification → Implementation → Tests**

```
Spec Criterion ──→ Implementation File:Line ──→ Test File:Line
   AC-XXX-001  →  src/handler.ts:42         →  test/handler.test.ts:15
```

### Coverage Calculation

```
Traceability Coverage = (Criteria with Implementation Mapping) / (Total Criteria) × 100

Example:
  Total criteria: 12
  Mapped to implementation: 10
  Mapped to tests: 8
  Coverage: 10/12 = 83% (implementation), 8/12 = 67% (test)
```

### Coverage Thresholds

| Coverage | Assessment |
|----------|-----------|
| ≥90% | Excellent — supports CERTIFIED |
| 70-89% | Good — supports CONDITIONAL |
| 50-69% | Insufficient — requires remediation |
| <50% | Unacceptable — triggers REJECTED |

---

## Handoff Formats

### To Builder (Violation Fixes)

```yaml
ATTEST_TO_BUILDER_HANDOFF:
  verdict: CONDITIONAL
  violations:
    - criterion_id: AC-XXX-002
      priority: CRITICAL
      gap: "Account lockout not implemented"
      spec_reference: "login-spec.md:L45"
      suggested_location: "src/controllers/auth.ts"
    - criterion_id: AC-XXX-005
      priority: HIGH
      gap: "Error message format doesn't match spec"
      current: "Generic error returned"
      expected: "Specific error with error code"
  bdd_scenarios: "generated/login.feature"
```

### To Radar (Test Generation)

```yaml
ATTEST_TO_RADAR_HANDOFF:
  bdd_scenarios:
    file: "generated/login.feature"
    total: 42
    by_priority:
      critical: 15
      high: 12
      medium: 10
      low: 5
  not_tested_criteria:
    - criterion_id: AC-XXX-003
      reason: "Requires runtime timing verification"
      suggested_test_type: "integration"
    - criterion_id: AC-XXX-008
      reason: "Requires browser rendering"
      suggested_test_type: "e2e"
```

### To Warden (Release Gate)

```yaml
ATTEST_TO_WARDEN_HANDOFF:
  verdict: CERTIFIED
  criteria_summary:
    total: 12
    pass: 10
    not_tested: 2
  traceability_coverage: 92%
  adversarial_probes:
    total: 18
    critical_open: 0
    high_open: 1
  spec_quality: GOOD
  recommendation: "Spec compliance verified. Proceed to V.A.I.R.E. evaluation."
```

### To Scribe (Spec Gap Report)

```yaml
ATTEST_TO_SCRIBE_HANDOFF:
  ambiguity_flags:
    - criterion_id: AC-XXX-005
      type: UNMEASURABLE
      suggestion: "Define response time threshold"
  omissions:
    - category: ERROR_HANDLING
      description: "No specification for rate limiting behavior"
    - category: EDGE_CASE
      description: "Behavior when session expires mid-action not specified"
  contradictions:
    - criteria: [AC-XXX-003, AC-XXX-009]
      description: "AC-003 says allow retry, AC-009 says lock immediately"
```
