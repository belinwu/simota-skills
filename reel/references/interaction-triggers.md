# Interaction Trigger Templates

Question templates for `AskUserQuestion` at key decision points.
See `_common/INTERACTION.md` for standard formats.

---

## ON_SCENARIO_DESIGN

```yaml
questions:
  - question: "録画のシナリオを確認します。この構成で進めてよいですか？"
    header: "Scenario"
    options:
      - label: "このシナリオで進める（推奨）"
        description: "提案された構成で.tapeファイルを生成し録画を開始します"
      - label: "シナリオを調整"
        description: "コマンドやタイミングを変更します"
      - label: "別の機能をデモ"
        description: "録画対象の機能を変更します"
    multiSelect: false
```

## ON_TOOL_SELECTION

```yaml
questions:
  - question: "録画ツールを選択してください。"
    header: "Tool"
    options:
      - label: "VHS（推奨）"
        description: "宣言的な.tapeファイルで再現可能な録画を生成"
      - label: "terminalizer"
        description: "インタラクティブセッションを録画しYAMLで後編集"
      - label: "asciinema"
        description: "軽量な.castファイルでWeb埋め込みプレイヤー対応"
    multiSelect: false
```

## ON_OUTPUT_FORMAT

```yaml
questions:
  - question: "出力フォーマットを選択してください。"
    header: "Format"
    options:
      - label: "GIF（推奨）"
        description: "最も互換性が高い。README・ドキュメント埋め込みに最適"
      - label: "MP4"
        description: "高画質で小さいファイルサイズ。プレゼンテーション向け"
      - label: "WebM"
        description: "Web最適化フォーマット。ブラウザ再生向け"
      - label: "SVG（asciinema経由）"
        description: "無限にスケーラブル。テキスト検索可能"
    multiSelect: false
```

## ON_SENSITIVE_CONTENT

```yaml
questions:
  - question: "録画にシークレットや個人情報が含まれる可能性があります。どう対応しますか？"
    header: "Security"
    options:
      - label: "ダミーデータに置換（推奨）"
        description: "すべてのトークン・パスワードをダミー値に置換"
      - label: "Hideで非表示にする"
        description: "機密部分をVHSのHideコマンドで録画から除外"
      - label: "問題なし、続行"
        description: "機密データが含まれないことを確認済み"
    multiSelect: false
```

## ON_LONG_RECORDING

```yaml
questions:
  - question: "録画が30秒を超える見込みです。どう対応しますか？"
    header: "Duration"
    options:
      - label: "シナリオを分割（推奨）"
        description: "複数の短い録画に分割して個別に作成"
      - label: "そのまま続行"
        description: "長い録画として1本で作成"
      - label: "重要部分のみ録画"
        description: "Hideを使って不要部分をスキップ"
    multiSelect: false
```
