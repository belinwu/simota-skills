# Workflow Design Anti-Patterns

> GHAワークフロー構造、YAML設計、トリガー設定、実行フローの失敗パターン

## 1. ワークフロー構造 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **WD-01** | **Monolithic Workflow（モノリスワークフロー）** | 1ファイルにlint+test+build+deploy全ステップ | 500行超YAML、変更のたびに全体再テスト必要 | ジョブ分割+needs依存グラフ、Reusable Workflowで分離 |
| **WD-02** | **YAML Indentation Trap（YAMLインデント罠）** | インデントミスでステップ/ジョブのスコープがずれる | サイレント失敗、ステップが実行されない | actionlintでCI時に検証、エディタYAMLプラグイン使用 |
| **WD-03** | **ubuntu-latest Dependency（latestランナー依存）** | `runs-on: ubuntu-latest`でランナーバージョン未固定 | ランナー更新で突然ビルドが壊れる | `ubuntu-24.04`等の具体的バージョン指定 |
| **WD-04** | **No Concurrency Control（並行制御なし）** | concurrencyグループ未設定 | 同一PRに複数ワークフローが同時実行、リソース浪費 | `concurrency: group: ${{ github.workflow }}-${{ github.ref }}` + `cancel-in-progress: true` |
| **WD-05** | **Trigger Overfire（トリガー過剰発火）** | `on: push`のみでブランチ/パスフィルターなし | 全ブランチの全pushで実行、請求額増大 | ブランチフィルター + pathsフィルター + `dorny/paths-filter` |
| **WD-06** | **workflow_run Chain Depth（チェーン深度超過）** | workflow_runを3段以上チェーン | デバッグ困難、失敗時の原因特定が複雑 | 最大2段まで、複雑な依存はReusable Workflowで統合 |
| **WD-07** | **Workflow File Change Trap（ワークフロー変更トラップ）** | ワークフローファイル自体の変更が他ワークフローをトリガー | 意図しないワークフロー実行（GitHub仕様: ワークフロー定義変更時に再評価） | pathsフィルターにこの仕様を考慮、テスト時にworkflow_dispatch使用 |

---

## 2. トリガー設計の罠

```
トリガー設計の失敗:

  ❌ pull_request_target Misuse（pull_request_target誤用）:
    → フォークのPRコードをcheckoutし高権限で実行
    → 攻撃者がPRタイトル/コードで任意コード実行可能
    → 対策: pull_request_targetでは絶対にPR headをcheckoutしない、ラベルゲート使用

  ❌ Cron Without Path Guard（パスガードなしcron）:
    → schedule cronが全コードに対して定期実行
    → 不要なビルド実行、無駄なコスト
    → 対策: cronワークフローは最小限のチェック、変更検出ステップを先行

  ❌ No Event Filtering（イベントフィルタリングなし）:
    → pull_request全activityタイプで実行
    → ラベル追加/アサイン変更でもCI実行
    → 対策: types: [opened, synchronize, reopened]で明示指定

  ❌ repository_dispatch Without Auth（認証なしrepository_dispatch）:
    → クロスリポジトリ呼び出しの認証トークン管理が不適切
    → 意図しないワークフロー実行
    → 対策: client_payloadでソース検証、event_typeの命名規約

  ❌ merge_group Ignorance（merge_group無視）:
    → Merge Queue有効化時にmerge_groupイベント未対応
    → Required checksが合わないためMerge Queueが機能しない
    → 対策: merge_groupイベントをワークフロートリガーに追加
```

---

## 3. 実行フローのアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **EF-01** | **Serial Everything（全直列実行）** | 全ジョブをneeds連鎖で直列化 | CI所要時間がジョブ時間の合計、15分超のフィードバック待ち | 独立ジョブは並列化、diamondパターンで最小のneeds |
| **EF-02** | **No Fail-Fast Strategy（早期失敗なし）** | bash scriptでset -e未使用、continue-on-error乱用 | 失敗が後続ステップに伝播、カスケード失敗 | `set -eo pipefail`、`continue-on-error`は意図的な場合のみ |
| **EF-03** | **Matrix Explosion（マトリクス爆発）** | OS×Node×DB×Browserの全組み合わせ実行 | 100+ジョブ生成、実行時間・コスト膨大 | `include`/`exclude`で必要組み合わせのみ、`fail-fast: false`で独立 |
| **EF-04** | **Conditional Logic Mess（条件ロジック混乱）** | 複雑なif条件のネスト | 可読性崩壊、条件の見落としで意図しないスキップ | 条件をenv変数に事前計算、パスフィルターで分離 |

---

## 4. YAML品質の罠

```
YAML品質の失敗:

  ❌ Case Sensitivity Bug（大文字小文字バグ）:
    → environment: Production vs environment: production
    → 環境名が一致せず、environment protectionが適用されない
    → 対策: 全環境名を小文字に統一、actionlintで検証

  ❌ Expression Injection（式インジェクション）:
    → ${{ github.event.issue.title }}をrun:内で直接使用
    → タイトルに`;malicious_command`が含まれると実行される
    → 対策: 環境変数経由で渡す: env: TITLE: ${{ ... }} → "$TITLE"

  ❌ No Shell Specification（シェル未指定）:
    → run:ステップでshellを指定しない
    → OS依存のデフォルトシェル、Windows/Linuxで挙動差異
    → 対策: defaults.run.shellを設定（bash推奨）

  ❌ Magic Strings（マジック文字列）:
    → ブランチ名・環境名・タグパターンをハードコード
    → 複数箇所の修正漏れ
    → 対策: env:で定義し参照、またはReusable Workflowのinputsで管理
```

---

## 5. Pipe との連携

```
Pipe での活用:
  1. Recon フェーズで WD-01〜07 のワークフロー構造スクリーニング
  2. Orchestrate フェーズでトリガー設計の品質チェック
  3. Test フェーズで EF-01〜04 の実行フロー最適化確認
  4. Evolve フェーズで YAML品質の静的検証

品質ゲート:
  - 1ワークフロー500行超 → 分割提案（WD-01 防止）
  - ubuntu-latest使用 → 具体バージョン指定（WD-03 防止）
  - concurrency未設定 → グループ追加（WD-04 防止）
  - pull_request_targetでcheckout → 即座に警告（trigger 防止）
  - 全ジョブ直列 → 並列化提案（EF-01 防止）
  - ${{}}のrun:直接使用 → env経由に変更（Expression Injection 防止）
```

**Source:** [Arctiq: Top 10 GitHub Actions Security Pitfalls](https://arctiq.com/blog/top-10-github-actions-security-pitfalls-the-ultimate-guide-to-bulletproof-workflows) · [MoldStud: Common Mistakes in GitHub Actions](https://moldstud.com/articles/p-avoid-these-common-pitfalls-in-github-actions-key-tips-for-success) · [Wiz: Hardening GitHub Actions](https://www.wiz.io/blog/github-actions-security-guide) · [ZXTech: Workflow File Changes Trigger](https://zxtech.wordpress.com/2025/08/24/changes-to-github-actions-workflow-file-changes-always-trigger-workflows/)
