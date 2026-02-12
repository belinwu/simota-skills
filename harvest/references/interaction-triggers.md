# Interaction Trigger YAML Templates

Use `AskUserQuestion` tool to confirm with user at these decision points.
See `_common/INTERACTION.md` for standard formats.

---

## ON_REPORT_SCOPE

```yaml
questions:
  - question: "レポートの期間を選択してください。"
    header: "期間"
    options:
      - label: "過去7日間（推奨）"
        description: "直近1週間のPR活動をレポート"
      - label: "過去30日間"
        description: "直近1ヶ月のPR活動をレポート"
      - label: "カスタム期間"
        description: "開始日と終了日を指定"
    multiSelect: false
```

---

## ON_REPORT_FORMAT

```yaml
questions:
  - question: "どの形式のレポートを生成しますか？"
    header: "形式"
    options:
      - label: "サマリーレポート（推奨）"
        description: "統計とカテゴリ分布の概要"
      - label: "詳細一覧"
        description: "全PRの表形式リスト"
      - label: "個人作業報告"
        description: "特定メンバーの活動詳細"
      - label: "リリースノート"
        description: "Changelog形式"
    multiSelect: false
```

---

## ON_FILTER_SELECTION

```yaml
questions:
  - question: "フィルタ条件を選択してください。"
    header: "フィルタ"
    options:
      - label: "全てのPR（推奨）"
        description: "状態、著者を問わず全て取得"
      - label: "マージ済みのみ"
        description: "完了したPRのみ"
      - label: "特定のauthor"
        description: "指定ユーザーのPRのみ"
      - label: "特定のlabel"
        description: "指定ラベルのPRのみ"
    multiSelect: true
```

---

## ON_OUTPUT_DESTINATION

```yaml
questions:
  - question: "レポートの出力先を選択してください。"
    header: "出力先"
    options:
      - label: "ファイル出力（推奨）"
        description: "Markdownファイルとして保存"
      - label: "標準出力"
        description: "ターミナルに表示"
      - label: "クリップボード"
        description: "コピー可能な形式で出力"
    multiSelect: false
```

---

## ON_LARGE_DATASET

```yaml
questions:
  - question: "{count}件のPRが見つかりました。全て取得しますか？"
    header: "大量データ"
    options:
      - label: "全て取得"
        description: "時間がかかる可能性があります"
      - label: "最新100件のみ"
        description: "直近のPRに限定"
      - label: "期間を絞る"
        description: "日付範囲を再設定"
    multiSelect: false
```
