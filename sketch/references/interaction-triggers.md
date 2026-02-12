# Sketch — Interaction Trigger Templates

Use `AskUserQuestion` at decision points. See `_common/INTERACTION.md` for format conventions.

---

## ON_PERSON_GENERATION

```yaml
questions:
  - question: "人物を含む画像生成が必要です。どのように進めますか？"
    header: "Person Gen"
    options:
      - label: "人物なしで代替 (Recommended)"
        description: "シルエットやイラストで安全に代替"
      - label: "人物生成を許可"
        description: "プロンプトに人物を含めて生成を試行"
      - label: "プロンプトを調整"
        description: "人物を含まない方向にプロンプトを再構築"
    multiSelect: false
```

---

## ON_RESOLUTION_CHOICE

```yaml
questions:
  - question: "出力解像度を選択してください。"
    header: "Resolution"
    options:
      - label: "標準品質 (Recommended)"
        description: "Flash モデル — 高速・低コスト、Web/SNS向け"
      - label: "高品質"
        description: "プロンプトで高解像度指示 — 印刷物やバナー向け"
      - label: "最高品質"
        description: "Pro モデル検討 — プレミアム用途"
    multiSelect: false
```

---

## ON_BATCH_SIZE

```yaml
questions:
  - question: "大量画像生成（10枚超）を実行します。進め方を選んでください。"
    header: "Batch"
    options:
      - label: "3枚でプレビュー (Recommended)"
        description: "まず少数生成して品質を確認、その後拡大"
      - label: "全数生成"
        description: "指定数をすべて一括生成"
      - label: "段階的生成"
        description: "5枚ずつ段階的に生成し、各段階で確認"
    multiSelect: false
```

---

## ON_STYLE_DIRECTION

```yaml
questions:
  - question: "画像のスタイル方向性を選んでください。"
    header: "Style"
    options:
      - label: "フォトリアリスティック (Recommended)"
        description: "写真のようなリアルな表現"
      - label: "イラスト/アート"
        description: "手描き風、デジタルアート、ベクター風"
      - label: "3Dレンダリング"
        description: "3DCG風のクリーンな表現"
      - label: "抽象/コンセプチュアル"
        description: "抽象的、概念的なビジュアル"
    multiSelect: false
```

---

## ON_CONTENT_POLICY_RISK

```yaml
questions:
  - question: "プロンプト内容がコンテンツポリシーに抵触する可能性があります。どうしますか？"
    header: "Policy"
    options:
      - label: "プロンプトを修正 (Recommended)"
        description: "ポリシー準拠になるようプロンプトを調整"
      - label: "そのまま試行"
        description: "現在のプロンプトで生成を試み、ブロック時はフォールバック"
      - label: "代替アプローチ"
        description: "異なるコンセプトで目的を達成"
    multiSelect: false
```

---

## ON_MODEL_SELECTION

```yaml
questions:
  - question: "使用するモデルを選択してください。"
    header: "Model"
    options:
      - label: "Flash (Recommended)"
        description: "gemini-2.5-flash-image — 高速・低コスト、ほとんどの用途に最適"
      - label: "別モデルを検討"
        description: "利用可能な別モデルがあれば検討（SDK バージョン依存）"
    multiSelect: false
```
