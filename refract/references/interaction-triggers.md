# Interaction Triggers — ON_* トリガー別 AskUserQuestion テンプレート

Refract が `AskUserQuestion` ツールを使用するべき4つのトリガー。

---

## ON_ROTATION_OVERFLOW

**発動条件:** 入力に5つ以上の独立した問題・テーマが含まれており、全てを1セッションで処理すると視点マップが過剰に複雑になる場合。

**タイミング:** BEFORE_START

```yaml
questions:
  - question: "入力に複数の独立した問題が含まれています。どのように進めますか？"
    header: "スコープ"
    options:
      - label: "最重要の1-2問題に絞る（推奨）"
        description: "最も意思決定・行動に影響する問題を選び、深い視点マップを生成します。残りは別セッションで処理。"
      - label: "全問題を浅く扱う（ミニマル版）"
        description: "全問題に対してミニマルテンプレートで視点マップを生成。深さより広さを優先。"
      - label: "問題をグループ化して処理"
        description: "共通テーマでグループ化し、グループごとに視点マップを生成。"
    multiSelect: false
```

---

## ON_SCOPE_SELECTION

**発動条件:** 全3軸（視野/視座/視点）を適用すべきか、特定の軸のみに集中すべきか、ユーザーの意図が不明な場合。

**タイミング:** BEFORE_START

```yaml
questions:
  - question: "どの軸に重点を置いてリフレーミングを行いますか？"
    header: "適用軸"
    options:
      - label: "全3軸で完全分析（推奨）"
        description: "視野・視座・視点の全軸を適用。最も包括的な視点マップを生成します。（目安: 10-15分）"
      - label: "視野（スケール）のみ"
        description: "Zoom Out/In、Cross-Domain、Temporal Zoomに特化。スケールと時間軸の盲点を探します。"
      - label: "視座（立場）のみ"
        description: "Role/Hierarchy/Timeline/Adversarial Shiftに特化。ステークホルダー視点の盲点を探します。"
      - label: "視点（フレーム）のみ"
        description: "Systems/Inversion/First Principles/Narrative Lensに特化。思考フレームの盲点を探します。"
    multiSelect: false
```

---

## ON_SENSITIVE_STANDPOINT

**発動条件:** 視座の回転において、実在する個人・組織の機密的な立場（内部情報、個人の思惑等）を推定する必要が生じた場合。

**タイミング:** ON_DECISION

```yaml
questions:
  - question: "この視座の変換では、[組織/個人名]の内部的な動機・立場を推定する必要があります。どう処理しますか？"
    header: "機密視座"
    options:
      - label: "公開情報のみから推定（推奨）"
        description: "公開されている情報・発言・行動パターンから立場を推定します。機密情報は使用しません。"
      - label: "一般的なステークホルダータイプとして扱う"
        description: "特定の個人/組織を特定せず、「同立場のステークホルダー一般」として視座変換を行います。"
      - label: "この視座変換をスキップ"
        description: "機密性の懸念があるため、この特定の視座変換は省略して他の視点で補います。"
    multiSelect: false
```

---

## ON_HIGH_STAKES_REFRAME

**発動条件:** 視点マップが高リスクな意思決定（人事・法的判断・重大な戦略的転換等）に直接使用される文脈が確認された場合。

**タイミング:** ON_RISK

```yaml
questions:
  - question: "この視点マップは高リスクな意思決定に直接使用されるようです。適切な注意事項を付記しますか？"
    header: "リスク対応"
    options:
      - label: "注意事項を付記して続行（推奨）"
        description: "「このマップは探索的な洞察であり、最終的な意思決定は専門家の判断を要する」旨を明記した上で視点マップを生成します。"
      - label: "Magiへの移送を優先"
        description: "視点マップ生成を省略し、直接Magi（意思決定エージェント）への移送を推奨します。RefractはMagiの後に使用が適切です。"
      - label: "注意事項なしで続行"
        description: "通常の視点マップを生成します。リスク判断はユーザーが行います。"
    multiSelect: false
```

---

## トリガー発動チェックリスト

Refract が DECODE フェーズを開始する前に確認：

| チェック | 確認内容 | トリガー |
|---------|---------|---------|
| ☐ 入力テーマ数 | 5つ以上の独立した問題があるか | ON_ROTATION_OVERFLOW |
| ☐ 軸の指定 | 全3軸 vs 特定軸の希望が不明か | ON_SCOPE_SELECTION |
| ☐ 用途の確認 | 高リスク意思決定に直接使用されるか | ON_HIGH_STAKES_REFRAME |

ROTATE フェーズ中に確認：

| チェック | 確認内容 | トリガー |
|---------|---------|---------|
| ☐ 視座の対象 | 実在個人/組織の機密的立場の推定が必要か | ON_SENSITIVE_STANDPOINT |
