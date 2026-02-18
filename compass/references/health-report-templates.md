# Health Report Templates — Compass

Strategy Health Report の出力テンプレート5種。

---

## Template 1: Strategy Health Report（標準出力）

毎サイクルの定期モニタリングレポート。最も頻繁に使用する。

```markdown
---
title: Strategy Health Report — [テーマ / 期間]
date: YYYY-MM-DD
cycle: [WEEKLY | MONTHLY | QUARTERLY]
generated_by: Compass
---

## Compass: Strategy Health Report — [テーマ / 期間]

### Overall Status: [GREEN | YELLOW | RED | BLACK]

> **[1文サマリー: 現在の戦略健全性の核心]**

---

### 1. Strategy Health Dashboard

| 領域 | Status | Score | Trend | Key Signal |
|------|--------|-------|-------|------------|
| Milestone Progress | G/Y/R/B | XX% complete | ↑↗→↘↓ | [最重要シグナル] |
| Assumption Validity | G/Y/R/B | X/Y valid | ↑↗→↘↓ | [最重要シグナル] |
| KPI vs Target | G/Y/R/B | XX% on-track | ↑↗→↘↓ | [最重要シグナル] |
| OKR Alignment | G/Y/R/B | XX% aligned | ↑↗→↘↓ | [最重要シグナル] |

**Drift Score:** X.X / 10.0 (前回: X.X)

---

### 2. Milestone Progress

| Phase | Milestone | Due | Status | Progress | Days ±0 |
|-------|-----------|-----|--------|----------|---------|
| Phase 1 | [...] | YYYY-MM-DD | On-track / At-risk / Delayed | XX% | +X / -X |

**Weighted Progress:** XX%（重み付き進捗率）

---

### 3. Assumption Monitor (Lookout)

| ID | Assumption | Category | Metric | Threshold | Actual | Status | Trend |
|----|-----------|----------|--------|-----------|--------|--------|-------|
| A-001 | [...] | MARKET | [...] | [...] | [...] | VALID/WATCH/BREACH | ↑↗→↘↓ |

**Summary:** X/Y assumptions VALID, Z on WATCH, W in BREACH

---

### 4. KPI Performance

| KPI | Target | Actual | Gap | Gap% | Status | Trend |
|-----|--------|--------|-----|------|--------|-------|
| [...] | [...] | [...] | [...] | X% | G/Y/R/B | ↑↗→↘↓ |

**Leading Indicators:**
- [...]: [値] — [解釈]

**Lagging Indicators:**
- [...]: [値] — [解釈]

---

### 5. OKR Alignment

**Alignment Score:** XX%

| Level | Objective | Key Results | Progress | Alignment |
|-------|----------|-------------|----------|-----------|
| Company | [...] | KR1: XX%, KR2: XX%, KR3: XX% | XX% | Aligned / Partial / Misaligned |
| Team A | [...] | KR1-a: XX%, KR1-b: XX% | XX% | Aligned / Partial / Misaligned |

---

### 6. Alerts & Routing

| # | Alert | Severity | Routing | Action Required |
|---|-------|----------|---------|-----------------|
| 1 | [...] | YELLOW/RED/BLACK | → [Agent] | [...] |

---

### 7. Recommended Actions

1. **[Severity]** → **[Agent]**: [具体的アクション]
2. **[Severity]** → **[Agent]**: [具体的アクション]

---

### 8. Next Monitoring Cycle

| 項目 | 内容 |
|------|------|
| 次回レポート | YYYY-MM-DD |
| 重点監視項目 | [...] |
| データ要求 | Pulse: [...], Compete: [...] |
```

---

## Template 2: Quarterly Strategy Review

四半期レビュー用の包括的レポート。

```markdown
# Quarterly Strategy Review — [四半期] [年度]

## Executive Summary

| 項目 | Q結果 | 前Q比 | 年度目標比 |
|------|-------|-------|----------|
| Overall Status | G/Y/R/B | ↑↗→↘↓ | XX% |
| Milestone Progress | XX% | +X% | XX% of annual |
| Assumptions Valid | X/Y | ±X | — |
| OKR Alignment | XX% | ±X% | — |

## Quarter Highlights
1. [最大の進捗]
2. [最大のリスク]
3. [最重要な前提変化]

## Assumption Quarterly Review

| ID | Assumption | Q Start | Q End | Transition | Impact |
|----|-----------|---------|-------|------------|--------|
| A-001 | [...] | VALID | WATCH | Deteriorating | [影響評価] |

## KPI Trajectory

| KPI | Q Start | Q End | Q Target | Achievement | Annual Forecast |
|-----|---------|-------|----------|-------------|-----------------|
| [...] | [...] | [...] | [...] | XX% | On/Off track |

## Strategic Drift Analysis

**Drift Score Trend:** Q1: X.X → Q2: X.X → Q3: X.X → Q4: X.X

| Drift Factor | Contribution | Root Cause | Corrective Action |
|-------------|-------------|------------|-------------------|
| [...] | XX% | [...] | [...] |

## OKR Quarterly Scorecard

| Company OKR | Score | Cascade Health | Key Learnings |
|------------|-------|---------------|---------------|
| [...] | XX% | Healthy/At-risk/Broken | [...] |

## Next Quarter Priorities
1. [優先アクション1] → [Agent]
2. [優先アクション2] → [Agent]
```

---

## Template 3: Drift Alert（緊急通知）

RED/BLACK検知時に即時発行する短形式アラート。

```markdown
# DRIFT ALERT — [Severity: RED | BLACK]

**Detected:** YYYY-MM-DD HH:MM
**Source:** [トリガーとなった指標/前提]

## What Changed
- [変化の事実を1-3行で]

## Impact Assessment
| 影響領域 | 影響度 | 詳細 |
|---------|--------|------|
| [...] | HIGH/MEDIUM/LOW | [...] |

## Root Cause (Preliminary)
- [推定原因]

## Immediate Routing
→ **[Agent]**: [要請アクション]

## Context
- 関連前提: [A-XXX]
- 関連KPI: [...]
- 前回Status: [GREEN/YELLOW]
- ドリフト履歴: [...]

## Required Decision
[意思決定が必要な問い]
```

---

## Template 4: OKR Status Report

OKRカスケードの専用ステータスレポート。

```markdown
# OKR Cascade Status — [四半期]

## Alignment Score: XX%
| Component | Score | Status |
|-----------|-------|--------|
| Linkage Rate | XX% | G/Y/R/B |
| Coverage Rate | XX% | G/Y/R/B |
| Consistency Rate | XX% | G/Y/R/B |

## OKR Tree

### Strategy Objective: [Helm戦略目標]

**Company OKR 1: [Objective]**
| KR | Target | Current | Progress | Confidence |
|----|--------|---------|----------|------------|
| KR1 | [...] | [...] | XX% | High/Med/Low |

  → Team A: [Objective] (→ KR1)
  | KR | Target | Current | Progress |
  |----|--------|---------|----------|
  | KR1-a | [...] | [...] | XX% |

## Issues & Actions
| Issue | Type | Affected OKR | Action |
|-------|------|-------------|--------|
| [...] | Orphan/Conflict/Gap/Overload | [...] | [...] |
```

---

## Template 5: Executive Summary（1ページ版）

経営会議向け超要約版。

```markdown
# Strategy Health — Executive Summary

> **[1文: 戦略健全性の要旨]**

| 指標 | Status | Value | Trend |
|------|--------|-------|-------|
| Overall | G/Y/R/B | — | ↑↗→↘↓ |
| Milestones | G/Y/R/B | XX% | ↑↗→↘↓ |
| Assumptions | G/Y/R/B | X/Y valid | ↑↗→↘↓ |
| KPIs | G/Y/R/B | XX% on-track | ↑↗→↘↓ |
| OKR Alignment | G/Y/R/B | XX% | ↑↗→↘↓ |

## Top 3 Alerts
1. [Severity] [内容] → [Agent]
2. [Severity] [内容] → [Agent]
3. [Severity] [内容] → [Agent]

## Key Decision Needed
[最も優先度の高い意思決定事項]

---
*Generated by Compass | Next review: YYYY-MM-DD*
```
