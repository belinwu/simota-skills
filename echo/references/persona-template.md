# Echo Persona Template

このテンプレートを使用して、サービス特化ペルソナを定義します。

---

## Template

```markdown
---
name: [Persona Name]
service: [service-identifier]
type: custom
created: [YYYY-MM-DD]
source: [analyzed files/documents]
---

# [Persona Name]

## Profile

| 属性 | 値 |
|------|-----|
| 役割 | [ユーザーの役割・立場] |
| 技術レベル | [低/中/高] |
| 利用デバイス | [デバイス (割合%)] |
| 利用シーン | [典型的な利用状況] |
| 利用頻度 | [毎日/週数回/月数回/初回のみ] |

## Quote

> 「[このペルソナの典型的な発言・心の声]」

## Goals（達成したいこと）

1. [Functional Goal - 機能的なゴール]
2. [Emotional Goal - 感情的なゴール]
3. [Social Goal - 社会的なゴール]

## Frustrations（ストレス要因）

1. [主要なフラストレーション1]
2. [主要なフラストレーション2]
3. [主要なフラストレーション3]

## Key Behaviors（行動パターン）

- [典型的な行動1]
- [典型的な行動2]
- [典型的な行動3]

## Emotion Triggers

| 状態 | トリガー |
|------|---------|
| 😊 Delighted (+3) | [喜びを感じる瞬間] |
| 🙂 Satisfied (+2) | [満足する瞬間] |
| 😕 Confused (-1) | [混乱する瞬間] |
| 😤 Frustrated (-2) | [苛立つ瞬間] |
| 😡 Abandoned (-3) | [離脱する瞬間] |

## Echo Testing Focus

このペルソナでテストすべき重要フロー:

- [ ] [優先フロー1]
- [ ] [優先フロー2]
- [ ] [優先フロー3]

## Context Scenarios

このペルソナが遭遇する典型的な状況:

### シナリオ1: [シナリオ名]

```
Physical: [物理的状況]
Temporal: [時間的制約]
Social: [社会的状況]
Cognitive: [認知的状態]
Technical: [技術的環境]
```

## JTBD (Jobs-to-be-Done)

### Functional Job
[達成したい具体的なタスク]

### Emotional Job
[感じたい感情・状態]

### Social Job
[周囲からどう見られたいか]

## Source Analysis

このペルソナの根拠となったソース:

| ソース | 抽出した情報 |
|--------|-------------|
| [file1] | [抽出内容] |
| [file2] | [抽出内容] |

---

## Notes

[追加のメモ・観察事項]
```

---

## Field Descriptions

### Required Fields

| フィールド | 説明 | 例 |
|-----------|------|-----|
| `name` | ペルソナの名前（英語推奨） | `First-Time Buyer` |
| `service` | サービス識別子 | `ec-platform` |
| `type` | `custom`（サービス特化）または `base`（Echo標準） | `custom` |
| `created` | 作成日 | `2026-01-31` |
| `source` | 分析したファイル/ドキュメント | `[README.md, src/checkout/*]` |

### Profile Section

- **役割**: ユーザーの立場（顧客、管理者、ゲスト等）
- **技術レベル**: 低（初心者）/ 中（一般）/ 高（技術者）
- **利用デバイス**: 主要デバイスと割合
- **利用シーン**: いつ、どこで使うか
- **利用頻度**: サービスとの接触頻度

### Emotion Triggers

Echo の Emotion Score と連動:

| Score | State | 使用場面 |
|-------|-------|---------|
| +3 | Delighted | 期待を超えた体験 |
| +2 | Satisfied | スムーズな進行 |
| +1 | Relieved | 懸念が解消 |
| 0 | Neutral | 特に感情なし |
| -1 | Confused | 軽い迷い |
| -2 | Frustrated | 明確な問題 |
| -3 | Abandoned | 離脱 |

### Echo Testing Focus

ペルソナ固有の検証優先フロー。チェックボックス形式で進捗管理可能。

---

## Mapping to Echo Base Personas

サービス特化ペルソナは Echo の基本ペルソナと対応付けできます:

| Base Persona | 対応する特化ペルソナ例 |
|--------------|----------------------|
| Newbie | First-Time Buyer, New Employee |
| Power User | Heavy Buyer, Admin User |
| Skeptic | Price-Conscious Shopper |
| Mobile User | Commuter Shopper |
| Senior | Accessibility-Focused User |
| Accessibility User | Screen Reader User |
| Privacy Paranoid | Data-Conscious User |

この対応付けにより、Echo の既存分析フレームワーク（Mental Model Gap、Cognitive Load Index等）を活用できます。
