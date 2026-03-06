# Reusable Patterns & Maintenance Anti-Patterns

> Reusable Workflow/Composite Action設計、ワークフロー保守、モノレポCI、デプロイメントパイプラインの失敗パターン

## 1. Reusable Workflow/Composite Action 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **RW-01** | **Copy-Paste Workflows（コピペワークフロー）** | 同一パイプラインを複数リポジトリに丸コピー | 修正がN箇所、バージョンの乖離、セキュリティパッチ漏れ | Reusable Workflow（3+同一パイプライン→統合） |
| **RW-02** | **Copy-Paste Setup Steps（コピペセットアップ）** | checkout+setup-node+cacheを全ワークフローに重複 | 設定変更のたびに10+ファイル修正 | Composite Action（3+同一セットアップ→抽出） |
| **RW-03** | **Reusable Workflow Chaining（チェーン制限無視）** | Reusable Workflowから別のReusable Workflowを呼び出し | GH制限: Reusable WF→Reusable WFの直接呼び出し不可 | フラット構成、Composite Actionで共通部品化 |
| **RW-04** | **@main Reference（mainブランチ参照）** | `uses: org/workflows/.github/workflows/ci.yml@main` | mainへの変更が即座に全利用者に影響、破壊的変更のリスク | セマンティックバージョニングタグ（@v1, @v1.2.0）使用 |
| **RW-05** | **Composite Action Secret Limitation Ignorance（シークレット制限無視）** | Composite Actionでsecrets直接参照を試みる | Composite Actionはsecretsにアクセス不可（GH制限） | secrets不要な処理→Composite、secrets必要→Reusable Workflow |
| **RW-06** | **Over-Abstraction（過度な抽象化）** | 2箇所の類似ステップで即座にComposite Action作成 | 管理コスト増、柔軟性低下、理解の複雑化 | DRY閾値: 3+箇所で初めて抽象化を検討 |
| **RW-07** | **No Input Validation（入力バリデーションなし）** | Reusable Workflowのinputs/secrets未検証 | 不正な入力で予期しない動作、空文字列でデプロイ | required/default設定、ifガードでバリデーション |

---

## 2. ワークフロー保守の罠

```
保守性の失敗:

  ❌ No Workflow Testing（ワークフローテストなし）:
    → ワークフロー変更をmainに直接push
    → 本番CIが壊れて開発者全員に影響
    → 対策: workflow_dispatchでテスト、act toolでローカル検証

  ❌ No Actionlint（静的解析なし）:
    → YAML構文・式エラーを実行時に初めて発見
    → デバッグサイクルの浪費（push→待機→失敗→修正→push）
    → 対策: actionlintをpre-commit hookとCIに統合

  ❌ Zombie Workflows（ゾンビワークフロー）:
    → 使われなくなったワークフローが.github/workflows/に残留
    → cronで無駄に実行、セキュリティリスク
    → 対策: 定期棚卸し、disable設定、workflow_dispatchのみのアーカイブ

  ❌ No Documentation（ドキュメントなし）:
    → ワークフローの目的・依存関係・必要なsecrets未記載
    → 新メンバーが理解不能、修正時に意図せず破壊
    → 対策: ワークフロー先頭にコメント（目的/トリガー/必要secrets/依存）

  ❌ Workflow Sprawl（ワークフロー散乱）:
    → 20+個のワークフローファイルが無秩序に存在
    → 命名規約なし、依存関係が不明
    → 対策: 命名規約（ci-*.yml, deploy-*.yml, auto-*.yml）、READMEに一覧
```

---

## 3. モノレポCI のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **MR-01** | **Run Everything Always（常に全実行）** | パスフィルターなしで全パッケージのCI実行 | フロントエンド変更でバックエンドテストも実行、時間/コスト浪費 | `dorny/paths-filter`でパッケージ別ジョブ条件分岐 |
| **MR-02** | **Required Checks Incompatibility（必須チェック非互換）** | パスフィルターでジョブスキップ→Required checksが失敗 | PRマージ不能、「全ジョブ必須」と「選択実行」の矛盾 | `ci-gate`ジョブパターン: 常に実行する集約ジョブをRequired checksに |
| **MR-03** | **No Affected Package Detection（影響パッケージ未検出）** | 依存関係を無視して変更ファイルのみで判断 | 共通ライブラリ変更時に依存パッケージのテストが漏れ | `nx affected`/`turbo --filter`で依存グラフベースの検出 |
| **MR-04** | **Single Workflow for All Packages（全パッケージ単一WF）** | 1ワークフローでif条件分岐で全パッケージ管理 | 条件ロジック複雑化、1パッケージの問題で全体停止 | パッケージ/チーム単位でワークフロー分離 |

---

## 4. デプロイメントパイプラインの罠

```
デプロイの失敗:

  ❌ No Environment Protection（環境保護なし）:
    → productionデプロイにレビュー/承認なし
    → 誰でもmainへのpushで本番デプロイ
    → 対策: Environment protection rules: required reviewers + wait timer

  ❌ No Rollback Plan（ロールバック計画なし）:
    → デプロイ失敗時の復旧手順未定義
    → 障害時にパニック、手動復旧
    → 対策: rollbackジョブ/workflow_dispatch、前バージョンのアーティファクト保持

  ❌ Deploy From PR Branch（PRブランチからデプロイ）:
    → PRブランチのコードを直接staging/productionにデプロイ
    → 未レビューコードのデプロイ、セキュリティリスク
    → 対策: mainマージ後のみデプロイ、PRはプレビュー環境のみ

  ❌ No Smoke Test Post-Deploy（デプロイ後テストなし）:
    → デプロイ成功=サービス正常の前提
    → デプロイ成功だがアプリケーションエラー
    → 対策: デプロイ後のスモークテストジョブ、ヘルスチェック確認

  ❌ All-at-Once Deployment（一括デプロイ）:
    → 全インスタンスを同時にデプロイ
    → 問題発覚時に全サービスがダウン
    → 対策: カナリア/Blue-Green/ローリングデプロイ
```

---

## 5. 組織レベルのアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **OG-01** | **No Org-Level Templates（組織テンプレートなし）** | 各リポジトリが独自にワークフロー作成 | セキュリティ/品質のばらつき、ベストプラクティスの不浸透 | `.github`リポジトリでorganization-level starter workflows |
| **OG-02** | **No Action Governance（アクションガバナンスなし）** | 任意のMarketplaceアクションを自由に使用 | 未監査アクションによるサプライチェーンリスク | Organization allowlist + 承認プロセス |
| **OG-03** | **No Shared Secrets Strategy（共有シークレット戦略なし）** | リポジトリごとにシークレットを個別管理 | シークレット散在、ローテーション漏れ | Organization/Environment secrets + OIDC |

---

## 6. Pipe との連携

```
Pipe での活用:
  1. Recon フェーズで RW-01〜07 のDRY機会スクリーニング
  2. Unify フェーズで保守性の品質チェック
  3. Test フェーズで MR-01〜04 のモノレポCI検証
  4. Evolve フェーズでデプロイメント・組織パターン改善

品質ゲート:
  - 3+リポジトリで同一パイプライン → Reusable Workflow提案（RW-01 防止）
  - 3+ワークフローで同一セットアップ → Composite Action提案（RW-02 防止）
  - @main参照 → タグ参照に変更（RW-04 防止）
  - actionlint未導入 → CI統合提案（Testing 防止）
  - パスフィルターなしモノレポ → paths-filter導入（MR-01 防止）
  - required checks不整合 → ci-gateパターン提案（MR-02 防止）
  - production環境保護なし → protection rules追加（Deploy 防止）
```

**Source:** [SmartScope: Composite Action Patterns 2025](https://smartscope.blog/en/ai-development/github-actions-composite-action-patterns-2025/) · [DEV.to: Composite vs Reusable Workflows](https://dev.to/hkhelil/github-actions-composite-vs-reusable-workflows-4bih) · [GitHub Docs: Reusing Workflow Configurations](https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations) · [GitHub Community: Org Best Practices for Reusable Workflows](https://github.com/orgs/community/discussions/171037)
