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

### Firing Examples

| Input | Fires? | Reason |
|-------|--------|--------|
| 「ランディングページのヒーロー画像に笑顔のビジネスマンを入れて」 | ✅ Yes | 「笑顔のビジネスマン」= 明示的な人物要求 |
| 「チームメンバーのポートレート風画像を生成」 | ✅ Yes | 「ポートレート」= 人物/顔の生成 |
| 「カフェのインテリア写真を生成」 | ❌ No | 人物への言及なし — 空間のみ |
| 「オフィスの風景、人々が働いている様子」 | ✅ Yes | 「人々が働いている」= 人物を含む |

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

### Firing Examples

| Input | Fires? | Reason |
|-------|--------|--------|
| 「印刷用の高解像度バナーを作成して」 | ✅ Yes | 「印刷用」「高解像度」= 高品質要求 |
| 「4Kクオリティのプロダクト写真が必要」 | ✅ Yes | 「4K」= 明示的な高解像度要求 |
| 「SNS用のサムネイルを作って」 | ❌ No | SNS = 標準品質で十分 |
| 「ブログ記事のアイキャッチ画像」 | ❌ No | Web用途 = 標準品質がデフォルト |

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

### Firing Examples

| Input | Fires? | Reason |
|-------|--------|--------|
| 「商品カタログ用に20枚の画像を生成して」 | ✅ Yes | 20枚 > 10枚の閾値 |
| 「SNS投稿用に30種類のバリエーションを作成」 | ✅ Yes | 30種類 > 10枚の閾値 |
| 「3つのスタイルでヒーロー画像を比較したい」 | ❌ No | 3枚 < 10枚の閾値 |
| 「ロゴのバリエーションを5つ作って」 | ❌ No | 5枚 < 10枚の閾値 |

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

### Firing Examples

| Input | Fires? | Reason |
|-------|--------|--------|
| 「ランディングページの画像を作って」 | ✅ Yes | スタイル未指定 — 曖昧 |
| 「いい感じのビジュアルを作って」 | ✅ Yes | 「いい感じ」= 曖昧なスタイル |
| 「写真風のプロダクト画像を生成して」 | ❌ No | 「写真風」= スタイル明示済み |
| 「水彩画風のイラストを作成」 | ❌ No | 「水彩画風」= スタイル明示済み |

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

### Firing Examples

| Input | Fires? | Reason |
|-------|--------|--------|
| 「有名人の〇〇さん風の画像を生成して」 | ✅ Yes | 実在人物の模倣 = ポリシーリスク |
| 「戦争シーンのリアルな描写」 | ✅ Yes | 暴力的コンテンツの可能性 |
| 「自然の風景写真を生成」 | ❌ No | ポリシーリスクなし |
| 「モダンなオフィス空間を生成」 | ❌ No | ポリシーリスクなし |

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

### Firing Examples

| Input | Fires? | Reason |
|-------|--------|--------|
| 「最高品質のプロダクション画像が必要、コストは問わない」 | ✅ Yes | コスト度外視 = Pro モデル検討の余地 |
| 「Vertex AI 環境で Imagen 3.0 を使いたい」 | ✅ Yes | 特定モデルの明示的要求 |
| 「サムネイル画像を生成して」 | ❌ No | 標準用途 = Flash がデフォルト |
| 「プロトタイプ用のプレースホルダー画像」 | ❌ No | プロトタイプ = Flash で十分 |
