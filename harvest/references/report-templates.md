# Report Templates for Harvest

レポート生成のテンプレート集。各形式の詳細な構造とサンプルを提供します。

---

## 1. Summary Report (サマリーレポート)

統計とカテゴリ分布の概要を提供するレポート。定期報告や状況確認に最適。

### Template

```markdown
# PR Summary Report

**Period:** {start_date} - {end_date}
**Repository:** {repository}
**Generated:** {generation_date}

---

## Overview

| Metric | Value |
|--------|-------|
| Total PRs | {total} |
| Merged | {merged} ({merged_percent}%) |
| Open | {open} ({open_percent}%) |
...
```

### Sample Output

```markdown
# PR Summary Report

**Period:** 2024-01-01 - 2024-01-31
**Repository:** org/project
**Generated:** 2024-02-01

---

## Overview

| Metric | Value |
|--------|-------|
| Total PRs | 45 |
| Merged | 38 (84.4%) |
| Open | 5 (11.1%) |
...
```

---

## 2. Detailed List (詳細一覧)

全PRの表形式一覧。監査やトラッキングに使用。

### Template

```markdown
# PR Detailed List

**Period:** {start_date} - {end_date}
**Repository:** {repository}
**Total:** {total_count} PRs

---

## Merged PRs ({merged_count})

| # | Title | Author | Labels | Created | Merged | Changes |
|---|-------|--------|--------|---------|--------|---------|
| {number} | {title} | @{author} | {labels} | {created} | {merged} | +{add}/-{del} |

## Open PRs ({open_count})
...
```

### Sample Output

```markdown
# PR Detailed List

**Period:** 2024-01-01 - 2024-01-31
**Repository:** org/project
**Total:** 45 PRs

---

## Merged PRs (38)

| # | Title | Author | Labels | Created | Merged | Changes |
|---|-------|--------|--------|---------|--------|---------|
| 150 | feat: add OAuth2 support | @alice | feat, auth | 2024-01-28 | 2024-01-30 | +1,234/-456 |
| 149 | fix: resolve login timeout | @bob | fix, urgent | 2024-01-27 | 2024-01-27 | +45/-12 |
| 148 | refactor: extract auth utils | @charlie | refactor | 2024-01-25 | 2024-01-26 | +234/-189 |
...
```

---

## 3. Individual Work Report (個人作業報告)

特定メンバーの活動詳細。1on1やパフォーマンスレビューに使用。

### Template

```markdown
# Individual Work Report

**Author:** @{username}
**Period:** {start_date} - {end_date}
**Repository:** {repository}

---

## Summary

| Metric | Value |
|--------|-------|
| PRs Created | {created_count} |
| PRs Merged | {merged_count} |
| PRs Open | {open_count} |
...
```

### Sample Output

```markdown
# Individual Work Report

**Author:** @alice
**Period:** 2024-01-01 - 2024-01-31
**Repository:** org/project

---

## Summary

| Metric | Value |
|--------|-------|
| PRs Created | 15 |
| PRs Merged | 14 |
| PRs Open | 1 |
...
```

---

## 4. Release Notes (リリースノート)

Changelog形式のリリースノート。リリース作業やユーザー告知に使用。

### Template

```markdown
# Release Notes

## {version}

**Release Date:** {release_date}
**Tag:** {tag}
**Commits:** {commit_range}

---

### Features

{features_list}

### Bug Fixes
...
```

### Sample Output

```markdown
# Release Notes

## v1.2.0

**Release Date:** 2024-02-01
**Tag:** v1.2.0
**Commits:** v1.1.0...v1.2.0

---

### Features

- Add OAuth2 authentication support (#150) - @alice
- Implement dashboard widgets (#146) - @alice
- Add user profile page (#144) - @bob
...
```

---

## Output File Naming Convention

| Report Type | Pattern | Example |
|-------------|---------|---------|
| Summary | `pr-summary-{YYYY-MM-DD}.md` | `pr-summary-2024-02-01.md` |
| Detailed | `pr-list-{YYYY-MM-DD}.md` | `pr-list-2024-02-01.md` |
| Individual | `work-report-{username}-{YYYY-MM-DD}.md` | `work-report-alice-2024-02-01.md` |
| Release Notes | `release-notes-v{X.Y.Z}.md` | `release-notes-v1.2.0.md` |

---

## Category Detection Rules

PR titleからカテゴリを自動検出するルール:

| Prefix | Category | Example |
|--------|----------|---------|
| `feat:` / `feature:` | feat | feat: add login |
| `fix:` / `bugfix:` | fix | fix: resolve crash |
| `refactor:` | refactor | refactor: extract utils |
| `docs:` / `doc:` | docs | docs: update README |
| `test:` / `tests:` | test | test: add unit tests |
| `chore:` | chore | chore: update deps |
| `perf:` | perf | perf: optimize query |
| `style:` | style | style: format code |
| `ci:` | ci | ci: add workflow |
| `build:` | build | build: update webpack |

ラベルからの検出も併用:

| Label | Category |
|-------|----------|
| `enhancement`, `feature` | feat |
| `bug`, `bugfix` | fix |
| `refactoring` | refactor |
| `documentation` | docs |

---

---

## 5. Quality Trends Report (品質トレンドレポート)

Code review quality analysis integrated with Judge feedback data.

### Template

```markdown
# Code Quality Trends Report

**Period:** {start_date} - {end_date}
**Repository:** {repository}
**Data Source:** Judge Feedback Integration

---

## Quality Overview

| Metric | Current | Previous | Trend |
|--------|:-------:|:--------:|:-----:|
| Average Quality Score | {avg_score}/100 | {prev_avg_score}/100 | {trend_icon} |
| PR Approval Rate | {approval_rate}% | {prev_approval_rate}% | {trend_icon} |
| Avg Review Cycles | {avg_cycles} | {prev_avg_cycles} | {trend_icon} |
...
```
Week    Score   Approval   Cycles
{week_1}   {s1}      {a1}%      {c1}
{week_2}   {s2}      {a2}%      {c2}
{week_3}   {s3}      {a3}%      {c3}
{week_4}   {s4}      {a4}%      {c4}
```

## Recommendations

### Immediate Actions
{immediate_recommendations}

### Process Improvements
{process_recommendations}

### Training Opportunities
{training_recommendations}

---

*Quality data provided by Judge Agent*
...
```

### Sample Output

```markdown
# Code Quality Trends Report

**Period:** 2024-01-01 - 2024-01-31
**Repository:** org/project
**Data Source:** Judge Feedback Integration

---

## Quality Overview

| Metric | Current | Previous | Trend |
|--------|:-------:|:--------:|:-----:|
| Average Quality Score | 85/100 | 82/100 | ⬆️ |
| PR Approval Rate | 88% | 84% | ⬆️ |
| Avg Review Cycles | 1.4 | 1.6 | ⬆️ |
...
```
Week         Score   Approval   Cycles
W1 (01-07)     82       84%       1.6
W2 (01-14)     84       86%       1.5
W3 (01-21)     86       88%       1.4
W4 (01-28)     88       90%       1.3
```

## Recommendations

### Immediate Actions
- Review payment processing PR (#142) with security focus
- Pair review for legacy auth refactoring (#138)
- Add test requirements for feature PRs

### Process Improvements
- Consider implementing mandatory test coverage checks
- Add security review checklist for payment-related changes
- Implement PR size limits to reduce review complexity

### Training Opportunities
- Security best practices workshop for the team
...
```

### Integration with Judge Feedback

When receiving `JUDGE_TO_HARVEST_FEEDBACK`, process as follows:

```bash
# Generate quality section from Judge feedback
generate_quality_section() {
  local feedback="$1"

  cat <<EOF
## Code Review Quality Trends

### Quality Metrics
$(jq -r '.quality_metrics | "- Approval Rate: \(.approval_rate * 100 | floor)%\n- Avg Review Cycles: \(.avg_review_cycles)\n- Avg Review Time: \(.avg_review_time_hours)h"' "$feedback")

### Common Issues
$(jq -r '.trends.common_issues | map("- **\(.type)**: \(.count) occurrences") | join("\n")' "$feedback")

### Improvement Suggestions
$(jq -r '.suggestions | map("- \(.)") | join("\n")' "$feedback")
# ...
```

---

## Localization

Header translation table for Japanese reports:

| English | Japanese |
|---------|----------|
| Summary Report | サマリーレポート |
| Detailed List | 詳細一覧 |
| Individual Work Report | 個人作業報告 |
| Release Notes | リリースノート |
| Period | 期間 |
| Repository | リポジトリ |
| Overview | 概要 |
| Total PRs | PR総数 |
| Merged | マージ済み |
| Open | オープン |
| ... | (11 more rows) |
