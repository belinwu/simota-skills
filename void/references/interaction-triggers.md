# Interaction Triggers — ON_* トリガー別 AskUserQuestion テンプレート

Void が `AskUserQuestion` ツールを使用するべき7つのトリガー。

---

## ON_AUDIT_SCOPE

**発動条件:** 監査スコープが不明確な場合（プロジェクト全体 vs 特定モジュール vs 単一機能）。

**タイミング:** BEFORE_START

```yaml
questions:
  - question: "監査のスコープを確認します。どの範囲を評価しますか？"
    header: "監査スコープ"
    options:
      - label: "プロジェクト全体の監査（推奨: 初回）"
        description: "全機能・全依存・全設定を対象に包括的なYAGNI検証を実施します。Batch Subtraction Planを出力。"
      - label: "特定モジュール/ディレクトリのみ"
        description: "指定したモジュール内のコード・抽象化・依存を評価します。"
      - label: "単一機能/要素の評価"
        description: "特定の1機能または1要素に対してSingle Feature Evaluationを実施します。"
      - label: "その他（指定してください）"
        description: "上記以外のスコープを指定。"
    multiSelect: false
```

---

## ON_REVENUE_FEATURE

**発動条件:** 評価対象の機能に直接的な収益影響または契約上の義務がある場合。

**タイミング:** ON_RISK

```yaml
questions:
  - question: "[機能名]は収益に直接影響する可能性があります。どのように進めますか？"
    header: "収益影響確認"
    options:
      - label: "収益影響を確認した上で評価を継続（推奨）"
        description: "収益データを考慮しつつ、Cost-of-Keeping Scoreに収益価値を補正値として加算します。"
      - label: "この機能を評価対象から除外"
        description: "収益関連機能は今回の監査スコープから除外し、他の対象に集中します。"
      - label: "Magiにエスカレーション"
        description: "収益影響の判断をMagi（意思決定エージェント）に委ねます。"
    multiSelect: false
```

---

## ON_ACTIVE_WORK

**発動条件:** 評価対象のコードが他のチームメンバーによって現在開発中である場合。

**タイミング:** ON_DECISION

```yaml
questions:
  - question: "[対象名]は現在開発中のようです（直近のコミット: [日付]）。どう処理しますか？"
    header: "開発中コード"
    options:
      - label: "評価を一時保留し、開発完了後に再評価（推奨）"
        description: "DEFERとして記録し、次回の監査サイクルで再評価します。"
      - label: "現状で評価を実施"
        description: "開発中であることを考慮しつつ、現時点のコードに基づいて評価します。"
      - label: "開発者に確認を依頼"
        description: "開発者に完了見込みと機能の必要性を確認した上で判断します。"
    multiSelect: false
```

---

## ON_PUBLIC_API

**発動条件:** 削減提案が公開API（外部クライアントが利用するインターフェース）に影響する場合。

**タイミング:** ON_RISK

```yaml
questions:
  - question: "[API/インターフェース名]の削減は外部クライアントに影響します。どう進めますか？"
    header: "公開API影響"
    options:
      - label: "Breaking Change として段階的廃止プランを策定（推奨）"
        description: "Feature Sunset パターンを適用し、ANNOUNCE→DEPRECATE→MIGRATE→REMOVEの段階的プランを作成します。"
      - label: "この対象を評価スコープから除外"
        description: "公開APIは今回の監査から除外します。"
      - label: "Magiにエスカレーション"
        description: "公開APIの廃止判断をMagiに委ねます。"
    multiSelect: false
```

---

## ON_DATA_ABSENT

**発動条件:** 使用率データが利用できず、ヒューリスティック分析のみに依存する場合。

**タイミング:** BEFORE_START

```yaml
questions:
  - question: "使用率データが利用できません。どのように評価を進めますか？"
    header: "データ不在"
    options:
      - label: "ヒューリスティック分析で進行し、confidence を下方修正（推奨）"
        description: "コード分析・git履歴・構造的手がかりから推定します。confidence上限を70%に制限。"
      - label: "Pulseにデータ収集を依頼してから再開"
        description: "Pulseエージェントに使用率データの収集を依頼し、データ取得後に評価を再開します。"
      - label: "データなしで通常通り評価"
        description: "ヒューリスティックのみで通常のconfidence計算を行います。（精度リスクあり）"
    multiSelect: false
```

---

## ON_HIGH_CONFIDENCE_CUT

**発動条件:** Cost-of-Keeping >= 8 かつ confidence >= 80% の対象が検出された場合。

**タイミング:** ON_DECISION

```yaml
questions:
  - question: "[対象名]は高コスト(CoK: X.X)かつ高確信度(X%)です。自動ルーティングしますか？"
    header: "高確信度カット"
    options:
      - label: "Sweepに自動ルーティング（推奨）"
        description: "高確信度の削除対象としてSweepに直接ルーティングし、削除を実行します。"
      - label: "Magiの承認を経由"
        description: "高確信度であっても、Magiの意思決定プロセスを経由してから削除を進めます。"
      - label: "提案のみ（自動ルーティングなし）"
        description: "REMOVEの推奨を記録しますが、ルーティングは行いません。"
    multiSelect: false
```

---

## ON_SUBTRACTION_COMPLETE

**発動条件:** 完全な監査が完了し、バッチ判断のためにMagiへルーティングする準備ができた場合。

**タイミング:** AFTER_COMPLETE

```yaml
questions:
  - question: "監査が完了しました（対象: X件、REMOVE: X、SIMPLIFY: X）。バッチ承認をMagiに送信しますか？"
    header: "監査完了"
    options:
      - label: "Magiにバッチ承認を送信（推奨）"
        description: "全提案をまとめてMagiに送信し、一括で承認/却下の判断を求めます。"
      - label: "個別にルーティング"
        description: "各提案を個別に適切なエージェント（Sweep/Zen/Scribe）にルーティングします。"
      - label: "レポートのみ出力（ルーティングなし）"
        description: "Full Audit Reportを出力しますが、後続エージェントへのルーティングは行いません。"
    multiSelect: false
```

---

## トリガー発動チェックリスト

QUESTION フェーズ開始前に確認：

| チェック | 確認内容 | トリガー |
|---------|---------|---------|
| ☐ スコープ明確性 | 監査範囲が明確か | ON_AUDIT_SCOPE |
| ☐ データ可用性 | 使用率データが利用可能か | ON_DATA_ABSENT |

WEIGH/SUBTRACT フェーズ中に確認：

| チェック | 確認内容 | トリガー |
|---------|---------|---------|
| ☐ 収益影響 | 評価対象が収益に直結するか | ON_REVENUE_FEATURE |
| ☐ 開発中コード | 対象が現在開発中か | ON_ACTIVE_WORK |
| ☐ 公開API | 削減が外部インターフェースに影響するか | ON_PUBLIC_API |
| ☐ 高確信度カット | CoK >= 8 かつ confidence >= 80% か | ON_HIGH_CONFIDENCE_CUT |

PROPOSE フェーズ完了後に確認：

| チェック | 確認内容 | トリガー |
|---------|---------|---------|
| ☐ バッチ送信 | 全評価が完了し、Magiへの一括送信が適切か | ON_SUBTRACTION_COMPLETE |
