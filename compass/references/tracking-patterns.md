# Tracking Patterns Reference — Compass

マイルストーン進捗計算、Drift Score、トレンド分析の詳細ロジック。

---

## Milestone Progress Calculation

### Method 1: Weighted Progress（重み付き進捗）

各マイルストーンに戦略的重要度で重みを付けて進捗率を算出する。

```
Weighted Progress = Σ (Milestone_i Progress × Weight_i) / Σ Weight_i

Where:
  Weight: HIGH=3, MEDIUM=2, LOW=1
  Progress: 0-100%
```

**Example:**

| Milestone | Weight | Progress | Weighted |
|-----------|--------|----------|----------|
| MVP Launch | 3 (HIGH) | 80% | 240 |
| Hiring Plan | 2 (MED) | 50% | 100 |
| Documentation | 1 (LOW) | 100% | 100 |
| **Total** | **6** | — | **440 / 600 = 73.3%** |

### Method 2: Time-Weighted Progress（時間加重進捗）

期限までの残り時間を考慮した進捗率。期限が近いマイルストーンの遅延をより重く評価する。

```
Time-Adjusted Progress = Progress / Expected_Progress_at_Today

Where:
  Expected_Progress = (Days_Elapsed / Total_Duration) × 100

Interpretation:
  >= 1.0: 予定通りまたは前倒し
  0.8 - 1.0: 概ね順調
  0.5 - 0.8: 遅延リスク（YELLOW）
  < 0.5: 重大遅延（RED）
```

### Method 3: Earned Value Analysis (EVA)

大規模プロジェクト向けのアーンドバリュー分析。

```yaml
eva_metrics:
  planned_value: "PV — 計画上の進捗価値"
  earned_value: "EV — 実際に達成した進捗価値"
  actual_cost: "AC — 実際に投入したコスト"

derived_metrics:
  schedule_variance: "SV = EV - PV"  # 正 = 前倒し, 負 = 遅延
  cost_variance: "CV = EV - AC"      # 正 = 予算内, 負 = 超過
  schedule_performance_index: "SPI = EV / PV"  # >1 = 前倒し
  cost_performance_index: "CPI = EV / AC"      # >1 = 予算内

interpretation:
  spi_green: ">= 0.95"
  spi_yellow: "0.8 - 0.95"
  spi_red: "< 0.8"
```

---

## Drift Score Calculation

戦略ドリフトを定量化する複合スコア（0-10スケール）。

### Formula

```
Drift Score = Σ (Component_i Score × Weight_i) / Σ Weight_i

Components:
  1. KPI Drift (Weight: 3)
  2. Milestone Drift (Weight: 3)
  3. Assumption Drift (Weight: 4)
```

### Component Scores

**1. KPI Drift Score (0-10)**

```
KPI_Drift = Average( |Actual_i - Target_i| / Target_i × 10 )

Capped at 10.0
```

| Gap% | Score | Interpretation |
|------|-------|---------------|
| 0-5% | 0-0.5 | 正常（GREEN） |
| 5-10% | 0.5-1.0 | 軽微な偏差 |
| 10-25% | 1.0-2.5 | 注意（YELLOW） |
| 25-50% | 2.5-5.0 | 危険（RED） |
| >50% | 5.0-10.0 | 致命的（BLACK） |

**2. Milestone Drift Score (0-10)**

```
Milestone_Drift = (Delayed_Milestones / Total_Milestones) × 10
                  + Average_Delay_Days / 30  (bonus penalty)

Capped at 10.0
```

**3. Assumption Drift Score (0-10)**

```
Assumption_Drift = (BREACH_Count × 3 + WATCH_Count × 1) / Total_Assumptions × 10

Capped at 10.0
```

### Overall Drift Interpretation

| Drift Score | Status | Interpretation |
|-------------|--------|---------------|
| 0.0 - 1.5 | GREEN | 戦略は軌道上 |
| 1.5 - 3.0 | YELLOW | 軽度のドリフト、調整推奨 |
| 3.0 - 5.0 | RED | 重大なドリフト、戦略修正必要 |
| 5.0 - 10.0 | BLACK | 戦略の根本的見直しが必要 |

---

## Trend Analysis

### Trend Symbols

| Symbol | Meaning | 条件 |
|--------|---------|------|
| ↑ | 強い改善 | 3期連続改善 & 改善幅 > 10% |
| ↗ | 改善傾向 | 2期連続改善 or 改善幅 5-10% |
| → | 横ばい | 変動 < 5% |
| ↘ | 悪化傾向 | 2期連続悪化 or 悪化幅 5-10% |
| ↓ | 強い悪化 | 3期連続悪化 & 悪化幅 > 10% |

### Trend Calculation

```yaml
trend_analysis:
  data_points: "最低3期分のデータを使用"
  method: "移動平均 + 方向性判定"

  calculation:
    - step: "直近3期のデータを収集"
    - step: "期間間の変化率を算出"
    - step: "変化率の方向性（正/負）と大きさを評価"
    - step: "トレンドシンボルを割り当て"

  edge_cases:
    - "データ2期のみ → ↗ or ↘ まで（強いトレンドは判定しない）"
    - "データ1期のみ → → (判定不能)"
    - "V字回復 → 直近の方向性を採用"
```

---

## KPI vs Target Analysis

### Gap Analysis Structure

```yaml
kpi_gap_analysis:
  kpi_name: "[KPI名]"
  target: "[目標値]"
  actual: "[実績値]"
  gap: "[差分]"
  gap_percent: "X%"
  status: "GREEN | YELLOW | RED | BLACK"
  trend: "↑ | ↗ | → | ↘ | ↓"
  root_cause: "[推定原因]"
  corrective_action: "[是正措置案]"
  routing: "[担当Agent]"
```

### Leading vs Lagging Indicators

| Type | 特性 | 用途 | Example |
|------|------|------|---------|
| **Leading** | 将来の結果を予測する先行指標 | 早期警戒 | パイプライン金額、トライアル開始数、NPS |
| **Lagging** | 過去の結果を確認する遅行指標 | 結果確認 | MRR、チャーン率、売上高 |

Leading IndicatorがYELLOWのとき、対応するLagging IndicatorがまだGREENでも警戒を示す:

```
Leading YELLOW + Lagging GREEN → 予防的YELLOW（早期対応推奨）
Leading RED + Lagging GREEN → 警告RED（即時対応必要）
Leading GREEN + Lagging RED → 回復兆候（モニタリング継続）
```

---

## Monitoring Frequency Guidelines

| 指標カテゴリ | 推奨頻度 | 条件付き頻度引き上げ |
|------------|---------|------------------|
| Revenue KPIs | MONTHLY | YELLOW時 → WEEKLY |
| Customer KPIs | MONTHLY | WATCH前提あり → WEEKLY |
| Milestone Progress | WEEKLY | RED時 → DAILY |
| Assumption Validity | MONTHLY | WATCH → WEEKLY, BREACH → DAILY |
| OKR Progress | MONTHLY | 四半期末前1ヶ月 → WEEKLY |
| Drift Score | MONTHLY | RED以上 → WEEKLY |

---

## Historical Comparison Format

```markdown
### Trend History — [KPI名]

| Period | Value | Target | Gap% | Status | Drift |
|--------|-------|--------|------|--------|-------|
| T-3 | [...] | [...] | X% | G/Y/R/B | X.X |
| T-2 | [...] | [...] | X% | G/Y/R/B | X.X |
| T-1 | [...] | [...] | X% | G/Y/R/B | X.X |
| **Current** | **[...]** | **[...]** | **X%** | **G/Y/R/B** | **X.X** |

**Trend:** [↑↗→↘↓]
**Forecast (next period):** [線形外挿に基づく予測値]
```
