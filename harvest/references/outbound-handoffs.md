# Outbound Collaboration Patterns (Harvest → Other Agents)

---

## Pattern A: Release Flow (Guardian → Harvest)

```
Guardian (リリース準備)
    ↓
Harvest (リリースノート生成)
    ↓
Release Notes (Markdown)
```

**Guardian → Harvest Handoff:**
```yaml
GUARDIAN_TO_HARVEST_HANDOFF:
  request: "release_notes"
  tag_range:
    from: "v1.1.0"
    to: "v1.2.0"
  version: "1.2.0"
  include_contributors: true
```

---

## Pattern B: Metrics Integration (Harvest → Pulse)

```
Harvest (PR統計収集)
    ↓
Pulse (メトリクス統合)
    ↓
Dashboard (KPI反映)
```

**Harvest → Pulse Handoff:**
```yaml
HARVEST_TO_PULSE_HANDOFF:
  metrics:
    - name: "weekly_merged_prs"
      value: 25
      period: "2024-01-01/2024-01-07"
    - name: "avg_merge_time_hours"
      value: 18.5
    - name: "pr_size_distribution"
      data: { xs: 10, s: 8, m: 5, l: 2 }
```

---

## Pattern C: Visual Reports (Harvest → Canvas)

```
Harvest (トレンドデータ)
    ↓
Canvas (可視化)
    ↓
Charts (Mermaid/ASCII)
```

**Harvest → Canvas Handoff:**
```yaml
HARVEST_TO_CANVAS_HANDOFF:
  visualization_type: "trend_chart"
  data:
    - week: "W1"
      merged: 12
      opened: 15
    - week: "W2"
      merged: 18
      opened: 14
  format: "mermaid_xychart"
```

---

## Pattern D: PR Quality Analysis (Harvest → Zen)

```
Harvest (PRタイトル収集)
    ↓
Zen (命名規則分析)
    ↓
Improvement Suggestions (改善提案)
```

**Harvest → Zen Handoff:**
```yaml
HARVEST_TO_ZEN_HANDOFF:
  request: "pr_title_analysis"
  prs:
    - number: 123
      title: "fix bug"
      # 規約違反: Conventional Commits形式でない
    - number: 124
      title: "feat: add user authentication with OAuth2 support"
      # 良好
  conventions:
    - "Conventional Commits"
    - "50文字以内"
```

---

## Pattern E: Large PR Detection (Harvest → Sherpa)

```
Harvest (PRサイズ分析)
    ↓
Sherpa (分割戦略立案)
    ↓
Split Recommendations (分割提案)
```

**Harvest → Sherpa Handoff:**
```yaml
HARVEST_TO_SHERPA_HANDOFF:
  request: "large_pr_analysis"
  large_prs:
    - number: 150
      title: "feat: complete user management system"
      additions: 2500
      deletions: 300
      files: 45
      # 分割候補
  threshold:
    lines: 1000
    files: 20
```

---

## Pattern F: Test Coverage Correlation (Harvest → Radar)

```
Harvest (PR/テスト情報)
    ↓
Radar (カバレッジ分析)
    ↓
Coverage Report (相関レポート)
```

**Harvest → Radar Handoff:**
```yaml
HARVEST_TO_RADAR_HANDOFF:
  request: "coverage_correlation"
  prs:
    - number: 123
      category: "feat"
      files_changed: ["src/auth.ts", "src/utils.ts"]
      test_files: ["tests/auth.test.ts"]
    - number: 124
      category: "fix"
      files_changed: ["src/cart.ts"]
      test_files: []  # テスト追加なし - 要確認
```

---

## Pattern G: Release Notes to Launch (Harvest → Launch)

```
Harvest (Release notes generated)
    ↓
Launch (Release execution)
    ↓
Published Release
```

**Harvest → Launch Handoff:**
```yaml
HARVEST_TO_LAUNCH_HANDOFF:
  type: "release_notes_generated"
  release:
    version: "1.2.0"
  output:
    file: "release-notes-v1.2.0.md"
  summary:
    total_prs: 25
    features: 10
    bugfixes: 12
    breaking_changes: 1
  status: "SUCCESS"
```
