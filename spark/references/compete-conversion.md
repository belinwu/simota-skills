# Spark Compete-to-Spec Conversion Reference

競合分析から具体的な機能仕様への変換ガイド。

---

## Gap Type別の提案アプローチ

Competeエージェントから受け取るギャップタイプに応じた提案戦略。

### Gap Type Overview

| Gap Type | Definition | Strategy | Risk Level |
|----------|------------|----------|------------|
| **Parity Gap** | 競合にあって自社にない機能 | Catch-up | Low-Medium |
| **Blue Ocean** | どの競合にもない新機能 | Innovation | High |
| **Our Advantage** | 自社にあって競合にない機能 | Fortification | Low |
| **Threat Gap** | 競合が急速に追いついている領域 | Defensive | Medium-High |

---

## Parity Gap → Catch-up Proposal

競合にある機能を追加するアプローチ。

### When to Use

- ユーザーが競合機能を明確に期待している
- 機能がなければ商談を失うリスクがある
- 業界標準となっている機能

### Catch-up Proposal Template

```markdown
## CATCH_UP_PROPOSAL: [Feature Name]

**Gap Source**: COMPETE_TO_SPARK_HANDOFF [Date]
**Gap Type**: Parity Gap
**Competitors with Feature**: [Comp A, Comp B, ...]

### Market Context

**User Expectation Level**: [Essential / Expected / Nice-to-have]
**Lost Opportunity Evidence**:
- [Support ticket/feedback about missing feature]
- [Churned customer citing this gap]
- [Sales loss attributed to gap]

### Competitive Implementation Analysis
...
```

---

## Blue Ocean → Innovation Proposal

競合にない新機能でリードするアプローチ。

### When to Use

- 市場で未解決の問題を発見した
- 技術的優位性を活かせる
- 新しいユーザーセグメントを獲得できる

### Innovation Proposal Template

```markdown
## INNOVATION_PROPOSAL: [Feature Name]

**Gap Source**: COMPETE_TO_SPARK_HANDOFF [Date]
**Gap Type**: Blue Ocean
**Competitor Coverage**: None

### Market Opportunity

**Unmet Need**:
[Description of the problem no one is solving]

**Why Competitors Haven't Done This**:
- [Technical barrier they face]
- [Strategic focus elsewhere]
- [Market segment they're ignoring]
...
```

---

## Our Advantage → Fortification Proposal

既存の優位性を強化するアプローチ。

### When to Use

- 競合がこの領域を追っている兆候がある
- ユーザーがこの機能で自社を選んでいる
- さらなる差別化で競争優位を広げられる

### Fortification Proposal Template

```markdown
## FORTIFICATION_PROPOSAL: [Feature Name Enhancement]

**Gap Source**: COMPETE_TO_SPARK_HANDOFF [Date]
**Gap Type**: Our Advantage (Fortify)
**Current Status**: [Feature exists, competitors don't have]

### Current Advantage Analysis

**What We Have**:
[Current feature description]

**Why It's An Advantage**:
- User value: [What users love about it]
- Competitive moat: [Why competitors haven't copied]
- Usage metrics: [Adoption / satisfaction stats]
...
```

---

## Threat Gap → Defensive Proposal

競合が急速に追いついている領域への対応。

### When to Use

- 以前は優位だった領域で競合が追いついた
- 競合の新リリースで差が縮まった
- ユーザーが「もはや差がない」と言い始めた

### Defensive Proposal Template

```markdown
## DEFENSIVE_PROPOSAL: [Feature Area]

**Gap Source**: COMPETE_TO_SPARK_HANDOFF [Date]
**Gap Type**: Threat Gap
**Threat Level**: [Critical / High / Medium]

### Threat Analysis

**Previous Advantage**:
[What we used to have that they didn't]

**Current State**:
| Aspect | Us | Comp A | Comp B | Gap Remaining |
|--------|-----|--------|--------|---------------|
| [Aspect 1] | [✅] | [✅] | [❌] | Narrowed |
...
```

---

## Feature Matrix → User Story変換

競合機能マトリクスから具体的なUser Storyを生成するプロセス。

### Input: Compete Feature Matrix

```markdown
| Feature | Us | Comp A | Comp B | Priority |
|---------|-----|--------|--------|----------|
| Export to PDF | ❌ | ✅ | ✅ | P1 |
| Team sharing | ✅ | ✅ | ❌ | - |
| AI suggestions | ❌ | ❌ | ❌ | P2 (Blue Ocean) |
| Offline mode | ❌ | ✅ | ❌ | P3 |
```

### Conversion Process

```
For each Gap (❌ for Us, ✅ for Competitor):
1. Identify Gap Type
2. Research competitor implementation
3. Identify target persona
4. Define benefit in our context
5. Generate User Story
6. Assess differentiation opportunity
```

### Output: User Story Set

```markdown
## FEATURE_MATRIX_CONVERSION

**Source**: Compete Feature Matrix [Date]
**Total Gaps Identified**: [N]
**Converted to Proposals**: [M]

### P1: Export to PDF (Parity Gap)

**Gap Type**: Parity
**Competitors**: Comp A, Comp B

**User Story**:
> As a **Project Manager**,
> I want to **export my project summary as a PDF**
> So that **I can share status with stakeholders who don't have app access**.
...
```

---

## 差別化ポイントの仕様への落とし込み

競合優位性を維持しながら機能仕様を作成するガイド。

### Differentiation Integration

```markdown
## DIFFERENTIATED_FEATURE_SPEC

**Feature**: [Feature name]
**Gap Type**: [Parity/Blue Ocean/Fortification/Defense]

### Baseline Requirements (Match Competition)

| Requirement | Competitor Benchmark | Our Implementation |
|-------------|---------------------|-------------------|
| [Req 1] | [How Comp A does it] | [Same approach] |
| [Req 2] | [How Comp B does it] | [Same approach] |

### Differentiation Requirements (Beat Competition)

| Differentiator | Why It's Better | Priority |
...
```

---

## 競合優位性検証ループ

提案した差別化が実際に優位性になるか検証するプロセス。

### Verification Loop

```
1. PROPOSE: Create differentiated spec
        ↓
2. VALIDATE_INTERNAL: Scout investigation
   - Is differentiation technically feasible?
   - What's the actual implementation cost?
        ↓
3. VALIDATE_USER: Echo persona walkthrough
   - Do users value this differentiation?
   - Is it noticeable / important to them?
        ↓
4. VALIDATE_MARKET: Experiment A/B test
   - Does differentiation drive adoption?
   - Are metrics better than competitor baseline?
        ↓
5. CONFIRM or ITERATE
...
```

### Verification Request Template

```markdown
## DIFFERENTIATION_VERIFICATION_REQUEST

**Feature**: [Feature name]
**Proposed Differentiator**: [Specific differentiation]

**Request to Scout**:
- Technical feasibility of [differentiator]
- Implementation complexity vs. matching competitor
- Any technical risks specific to our approach

**Request to Echo**:
- Persona reaction to [differentiator]
- Perceived value vs. competitor approach
- Any confusion or concerns

...
```

---

## Integration with Compete Agent

### Compete → Spark Full Flow

```
COMPETE Analysis Complete
        ↓
COMPETE_TO_SPARK_HANDOFF
        ↓
Spark Gap Classification
├── Parity Gap → Catch-up Proposal
├── Blue Ocean → Innovation Proposal
├── Our Advantage → Fortification Proposal
└── Threat Gap → Defensive Proposal
        ↓
Differentiated Spec Creation
        ↓
Verification Loop (Scout → Echo → Experiment)
        ↓
Final Proposal → Sherpa/Forge
```

### Maintaining Competitive Context

```markdown
## COMPETITIVE_CONTEXT (Include in Proposal)

**Competitive Landscape** (from Compete):
- [Comp A]: [Position / Threat level]
- [Comp B]: [Position / Threat level]

**This Proposal Addresses**:
- Gap type: [Parity/Blue Ocean/Fortification/Defense]
- Primary competitor concern: [Comp X]
- Expected competitive response: [Time to copy / Unlikely to copy]

**Ongoing Monitoring**:
- Signal to watch: [Competitor announcement / Feature launch]
- Re-evaluate if: [Competitor matches our approach]
- Escalate to Compete if: [Major competitive shift]
```
