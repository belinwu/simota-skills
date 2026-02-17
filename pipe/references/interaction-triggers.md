# Interaction Triggers

YAML question templates for Pipe's 6 interaction triggers. Use with `AskUserQuestion`.

---

## ON_TRIGGER_STRATEGY

When: Complex trigger design needed (multi-event, chaining, filtering).

```yaml
trigger: ON_TRIGGER_STRATEGY
timing: BEFORE_START
question: "このワークフローのトリガー戦略をどうしますか？"
options:
  - label: "push + pull_request（標準CI）"
    description: "mainブランチへのpushとPRで実行"
  - label: "workflow_dispatch（手動トリガー）"
    description: "手動実行のみ、パラメータ入力可能"
  - label: "workflow_run チェーン"
    description: "別ワークフロー完了後に実行（2段・3段）"
  - label: "schedule（定期実行）"
    description: "cron式で定期的に実行"
  - label: "推奨デフォルトで進める"
    description: "push(main) + pull_request で開始"
  - label: "その他"
    description: "カスタム設定を指定"
recommended: "push + pull_request（標準CI）"
```

---

## ON_RUNNER_SELECTION

When: Runner choice affects billing (larger runners, macOS, self-hosted).

```yaml
trigger: ON_RUNNER_SELECTION
timing: ON_DECISION
question: "どのランナーを使用しますか？（課金に影響します）"
options:
  - label: "ubuntu-latest（標準）"
    description: "最も安価。Linux CI/CDに最適。$0.008/min"
  - label: "ubuntu-latest + larger runner"
    description: "4-64 vCPU。ビルド時間短縮。$0.016-0.128/min"
  - label: "ARM runner"
    description: "コスト37%削減。ARM対応ビルド向け"
  - label: "macOS runner"
    description: "iOS/macOSビルド必須時。$0.08/min（10倍）"
  - label: "Self-hosted runner"
    description: "自前ランナー。固定コスト。セキュリティ要件あり"
  - label: "推奨デフォルトで進める"
    description: "ubuntu-latest を使用"
recommended: "ubuntu-latest（標準）"
```

---

## ON_SECURITY_PERMISSIONS

When: Permissions changes required beyond `contents: read`.

```yaml
trigger: ON_SECURITY_PERMISSIONS
timing: ON_RISK
question: "このワークフローに追加のpermissionsが必要です。承認しますか？"
context: |
  現在の設定: permissions: { contents: read }
  要求される追加権限:
  - pull-requests: write（PRコメント投稿のため）
  - id-token: write（OIDC認証のため）
options:
  - label: "承認（必要最小限を追加）"
    description: "要求された権限のみ追加。最小権限原則を維持"
  - label: "確認してから判断"
    description: "各権限の使用箇所を詳細に説明してから決定"
  - label: "拒否（代替手段を検討）"
    description: "追加権限なしで実現可能な代替アプローチを提案"
  - label: "その他"
    description: "カスタム権限設定を指定"
recommended: "承認（必要最小限を追加）"
```

---

## ON_THIRD_PARTY_ACTION

When: Introducing a new third-party action.

```yaml
trigger: ON_THIRD_PARTY_ACTION
timing: ON_DECISION
question: "サードパーティアクションを導入しますか？"
context: |
  アクション: {action_name}@{version}
  リポジトリ: {repo_url}
  Stars: {stars} / Last updated: {date}
  SHA: {sha}
  OpenSSF Scorecard: {score}/10
options:
  - label: "SHA固定で導入"
    description: "SHA固定 + Dependabot自動更新で安全に導入"
  - label: "代替を検討"
    description: "同等機能の別アクション、またはスクリプトで代替"
  - label: "評価情報を詳しく確認"
    description: "セキュリティスコア、メンテナンス状況、依存関係を詳細確認"
  - label: "見送り"
    description: "このアクションは導入しない"
recommended: "SHA固定で導入"
```

---

## ON_WORKFLOW_CHAIN

When: Building workflow_run chains (loop risk, complexity).

```yaml
trigger: ON_WORKFLOW_CHAIN
timing: ON_RISK
question: "workflow_runチェーンを構築します。以下のリスクを確認してください。"
context: |
  チェーン構成: {workflow_a} → {workflow_b} → {workflow_c}
  深さ: {depth}段
  リスク:
  - 無限ループの可能性（conclusion フィルタで防止済み）
  - デバッグの複雑化（チェーン全体のログ追跡が必要）
  - GITHUB_TOKEN制限（追加ワークフローのトリガー不可）
options:
  - label: "承認（フィルタ付きで構築）"
    description: "conclusion: success フィルタ + 最大深度制限で安全に構築"
  - label: "チェーンを短縮"
    description: "ジョブ依存（needs:）で1ワークフローに統合を検討"
  - label: "repository_dispatch で代替"
    description: "明示的なAPI呼び出しで制御（PAT/GitHub App必要）"
  - label: "設計を再確認"
    description: "チェーン構成を再検討してから判断"
recommended: "承認（フィルタ付きで構築）"
```

---

## ON_SELF_HOSTED_RUNNER

When: Self-hosted runner introduction or configuration change.

```yaml
trigger: ON_SELF_HOSTED_RUNNER
timing: ON_RISK
question: "Self-hosted runnerの設定を変更します。以下のリスクを確認してください。"
context: |
  変更内容: {change_description}
  影響範囲: {scope}
  リスク:
  - パブリックリポジトリでのself-hosted使用はセキュリティリスク
  - ランナーイメージの更新・パッチ管理が必要
  - 可用性の責任がチームに移る
options:
  - label: "承認（変更を実行）"
    description: "リスクを理解の上、設定変更を実行"
  - label: "エフェメラルランナーに変更"
    description: "ジョブ単位で作成・破棄するエフェメラル設定に変更"
  - label: "ARC（Kubernetes）で自動スケール"
    description: "Actions Runner Controllerによる自動スケーリングを検討"
  - label: "ホステッドランナーで代替"
    description: "GitHub-hostedのLarger runnerで要件を満たせるか確認"
recommended: "エフェメラルランナーに変更"
```
