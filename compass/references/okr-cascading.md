# OKR Cascading Reference — Compass

戦略目標からOKRへの展開アルゴリズム、Alignment Score計算、OKR Tree構造。

---

## OKR Cascade Structure

### 3層カスケード

```
Strategy Objective (from Helm)
  └─ Company OKR
       ├─ Key Result 1
       ├─ Key Result 2
       └─ Key Result 3
            └─ Team OKR
                 ├─ Key Result 1-a
                 ├─ Key Result 1-b
                 └─ Key Result 1-c
```

### Layer Definitions

| Layer | Owner | Scope | Cycle | Alignment To |
|-------|-------|-------|-------|-------------|
| **Strategy Objective** | 経営層（Helm定義） | 全社方向性 | 年次〜中期 | ビジョン・ミッション |
| **Company OKR** | CxO / VP | 全社レベル成果 | 四半期 | Strategy Objective |
| **Team OKR** | チームリード | チームレベル成果 | 四半期 | Company OKR |

---

## Cascade Algorithm

### Step 1: Strategy Objective の分解

Helm の戦略目標を受け取り、以下の基準で Company OKR に分解する:

```yaml
decomposition_rules:
  - rule: "1 Strategy Objective → 1-3 Company Objectives"
    rationale: "フォーカスを維持するため3つ以下に制限"
  - rule: "各 Company Objective → 2-5 Key Results"
    rationale: "測定可能性と管理可能性のバランス"
  - rule: "Key Result は SMART 基準に準拠"
    criteria:
      specific: "具体的に何を達成するか"
      measurable: "数値で計測可能"
      achievable: "野心的だが達成可能（60-70%確率）"
      relevant: "Strategy Objective に直接貢献"
      time_bound: "期限が明確（四半期内）"
```

### Step 2: Company OKR → Team OKR への展開

```yaml
cascade_rules:
  - rule: "1 Company Key Result → 1-3 Team Objectives"
    rationale: "チーム間の責任分担を明確化"
  - rule: "Team Objective の達成が Company KR の進捗に直接貢献"
    validation: "Contribution Score >= 0.3 (30%以上)"
  - rule: "Team OKR 間の依存関係を明示"
    format: "dependency_map"
```

### Step 3: Alignment Validation

展開されたOKR Treeの整合性を検証する:

```yaml
validation_checks:
  - check: "Orphan Check"
    description: "Strategy Objective に紐付かない Team OKR がないか"
    action: "孤立OKRは削除 or 紐付けを追加"
  - check: "Gap Check"
    description: "Strategy Objective に対応するOKRが不足していないか"
    action: "カバーされていない領域に対してOKRを追加"
  - check: "Conflict Check"
    description: "Team OKR 間で矛盾するKRがないか"
    action: "ON_OKR_CONFLICT トリガーで確認"
  - check: "Overload Check"
    description: "1チームに過剰なOKRが割り当てられていないか"
    action: "5 OKR 超はリスク警告"
```

---

## Alignment Score Calculation

### Formula

```
Alignment Score = (Linked_OKRs / Total_OKRs) × Coverage_Score × Consistency_Score

Where:
  Linked_OKRs    = Strategy Objective に紐付くOKR数
  Total_OKRs     = 全OKR数（孤立含む）
  Coverage_Score  = カバーされたStrategy Objective数 / 全Strategy Objective数
  Consistency_Score = 矛盾なしKRペア数 / 全KRペア数
```

### Score Interpretation

| Score Range | Status | Interpretation | Action |
|-------------|--------|---------------|--------|
| **90-100%** | GREEN | 高アライメント | 維持・微調整 |
| **70-89%** | YELLOW | 部分的ギャップあり | ギャップ分析→OKR調整 |
| **50-69%** | RED | 重大なミスアライメント | OKR再設計→Helm相談 |
| **< 50%** | BLACK | アライメント崩壊 | 戦略→OKR全面再構築 |

### Detailed Score Breakdown

```yaml
alignment_report:
  overall_score: "XX%"
  breakdown:
    linkage_rate: "XX%"       # 紐付き率
    coverage_rate: "XX%"      # カバレッジ率
    consistency_rate: "XX%"   # 一貫性率
  gaps:
    orphan_okrs:
      - { team: "...", objective: "...", reason: "Strategy Objectiveに紐付かない" }
    uncovered_strategies:
      - { strategy: "...", reason: "対応するOKRが存在しない" }
    conflicts:
      - { team_a: "...", kr_a: "...", team_b: "...", kr_b: "...", conflict: "..." }
```

---

## OKR Tree Output Format

```markdown
### OKR Cascade Tree — [四半期]

#### Strategy Objective: [Helm戦略目標]

**Company OKR 1: [Objective文]**
| KR# | Key Result | Target | Current | Progress | Owner |
|-----|-----------|--------|---------|----------|-------|
| KR1 | [...] | [...] | [...] | XX% | [...] |
| KR2 | [...] | [...] | [...] | XX% | [...] |
| KR3 | [...] | [...] | [...] | XX% | [...] |

  **→ Team OKR 1-1: [Team A Objective]** (← KR1)
  | KR# | Key Result | Target | Current | Progress |
  |-----|-----------|--------|---------|----------|
  | KR1-a | [...] | [...] | [...] | XX% |
  | KR1-b | [...] | [...] | [...] | XX% |

  **→ Team OKR 1-2: [Team B Objective]** (← KR2)
  | KR# | Key Result | Target | Current | Progress |
  |-----|-----------|--------|---------|----------|
  | KR2-a | [...] | [...] | [...] | XX% |

---
**Alignment Score: XX%**
- Linkage: XX% | Coverage: XX% | Consistency: XX%
```

---

## OKR Anti-Patterns

| Anti-Pattern | 症状 | 対策 |
|-------------|------|------|
| **Sandbagging** | 達成率が常に100%超 | 目標の野心度を引き上げ（60-70%達成確率に） |
| **Orphan OKR** | 戦略目標と紐付かないOKR | Alignment Checkで検出→紐付け or 削除 |
| **Waterfall KR** | タスクリストをKRとして記述 | 成果（Outcome）ベースに書き換え |
| **Too Many OKRs** | 1チーム6+個のOKR | 優先度で3-5に絞る |
| **Cascade Disconnect** | Company KR と Team KR の論理断絶 | Contribution Score検証（>=0.3） |
| **Metric Fixation** | KRの数値だけ追い、目的を見失う | Objectiveとの定性的整合性を四半期レビュー |
| **Copy-Paste Cascade** | Company OKR をそのままTeam OKRにコピー | チーム固有の貢献に翻訳する |

---

## Contribution Score

Team OKR が Company KR にどの程度貢献するかの定量指標。

```
Contribution Score = Σ (Team KR Progress × Weight) / Company KR Target

Where:
  Weight = Team KR が Company KR に占める貢献割合（合計 = 1.0）
```

| Score | 判定 | 意味 |
|-------|------|------|
| >= 0.5 | Strong | 主要貢献者 |
| 0.3 - 0.5 | Moderate | 有意な貢献 |
| 0.1 - 0.3 | Weak | 補助的貢献 |
| < 0.1 | Negligible | 紐付け見直し推奨 |
