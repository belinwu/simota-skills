# Performance & Cost Anti-Patterns

> GHAパフォーマンス最適化、キャッシュ戦略、ランナー選択、課金コスト管理の失敗パターン

## 1. パフォーマンス 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **PF-01** | **No Dependency Caching（依存キャッシュなし）** | npm install/pip install を毎回フルで実行 | CI所要時間の40-60%が依存インストール | `setup-*`のcache機能 or `actions/cache`+lockfileハッシュ |
| **PF-02** | **Cache Key Mismatch（キャッシュキー不一致）** | lockfileを含まないキーや固定文字列のキー | キャッシュミス多発、またはstaleキャッシュ使用 | `hashFiles('**/package-lock.json')` + OSプレフィックス |
| **PF-03** | **Cache Size Explosion（キャッシュサイズ爆発）** | node_modules全体や不要なビルド成果物もキャッシュ | 10GB制限到達、古いキャッシュのeviction頻発 | 必要最小限のキャッシュ、定期的なキャッシュキーローテーション |
| **PF-04** | **No Docker Layer Cache（Dockerレイヤーキャッシュなし）** | Docker buildを毎回scratch（from scratch）実行 | コンテナビルドに10-15分 | `docker/build-push-action`+`type=gha`キャッシュ |
| **PF-05** | **Sequential Job Graph（直列ジョブグラフ）** | lint→test→build→deployを全直列needs連鎖 | 合計時間=各ジョブ時間の合計、15分→5分に短縮可能 | 独立ジョブ並列化、diamondパターン（lint∥test→build→deploy） |
| **PF-06** | **Full Matrix Every Push（全pushでフルマトリクス）** | 全OS×全バージョンをpushごとに実行 | 30+ジョブが毎push、コスト膨大 | pushは最小マトリクス、PRのみフルマトリクス |
| **PF-07** | **Large Artifact Upload（大容量アーティファクト）** | ビルド成果物を圧縮なしで全ジョブ間共有 | アーティファクトupload/downloadがボトルネック | 最小限のアーティファクト、`retention-days`設定、圧縮 |

---

## 2. コスト管理の罠

```
課金コストの失敗:

  ❌ Runner Oversize（ランナー過剰スペック）:
    → 全ジョブで大型ランナーを使用
    → 2-core 20分→8-core 12分だが、コスト4x→2.4x（ROI低い）
    → 対策: ジョブ特性に応じたランナー選択、CPUバウンドのみ大型

  ❌ macOS/Windows Overuse（高額ランナー過剰使用）:
    → テスト実行にmacOS（10xコスト）/Windows（2xコスト）を使用
    → Linux（1x）で代替可能なジョブでも高額ランナー
    → 対策: ubuntu-*をデフォルト、macOS/WindowsはOS固有テストのみ

  ❌ No Concurrency Cancellation（並行キャンセルなし）:
    → 同一PRで連続pushしても古いワークフローが走り続ける
    → 不要な実行に課金、ランナーキューイング
    → 対策: concurrency + cancel-in-progress: true

  ❌ Unnecessary Scheduled Runs（不要なスケジュール実行）:
    → cronで毎時/毎日ビルドするが変更がない
    → 変更なしでもフルビルド実行、無駄な課金
    → 対策: scheduleワークフローに変更検出ステップ、手動dispatch併用

  ❌ Self-Hosted Runner Tax Ignorance（self-hosted課金無視）:
    → 2026年からself-hostedランナーに$0.002/分のプラットフォーム課金
    → 「self-hosted=無料」の前提が崩壊
    → 対策: コスト計算にプラットフォーム料金を含める、大型ランナーで分数削減

  ❌ ARM Runner Ignorance（ARMランナー無視）:
    → 全ジョブをx86ランナーで実行
    → ARMランナーは37%安価で多くのワークロードに対応
    → 対策: ARMランナー（`ubuntu-24.04-arm`）をデフォルト検討
```

---

## 3. キャッシュ戦略のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **CA-01** | **No Restore Key（リストアキーなし）** | exactマッチのみでfallbackキーがない | lockfile変更で毎回フルインストール | `restore-keys: ${{ runner.os }}-node-`のprefix fallback |
| **CA-02** | **Cache Without Lockfile（lockfileなしキャッシュ）** | `hashFiles('**/*.js')`等の不安定なキー | コード変更でキャッシュ無効化、実質キャッシュ不使用 | lockfileハッシュのみをキーに使用 |
| **CA-03** | **Duplicate Caching（重複キャッシュ）** | `setup-node`のcacheと`actions/cache`を同時使用 | 同一内容を二重キャッシュ、容量浪費 | setup-*のbuilt-in cacheを優先、追加キャッシュは独自データのみ |
| **CA-04** | **Branch Cache Isolation Ignorance（ブランチキャッシュ分離無視）** | キャッシュのブランチスコープルールを理解していない | featureブランチでmainのキャッシュを使えない | mainでキャッシュを作成→PRブランチで再利用（GH仕様理解） |

---

## 4. ビルド最適化の罠

```
ビルド最適化の失敗:

  ❌ No Incremental Build（インクリメンタルビルドなし）:
    → 毎回クリーンビルド
    → 変更のないパッケージも再ビルド
    → 対策: turbo/nx のリモートキャッシュ、`.next/cache`キャッシュ

  ❌ Test All On Every Change（全変更で全テスト）:
    → パスフィルターなしで全テストスイート実行
    → フロントエンド変更でもバックエンドテスト実行
    → 対策: `dorny/paths-filter`でジョブレベル条件分岐

  ❌ No Test Splitting（テスト分割なし）:
    → 単一ジョブで全テスト実行
    → テストが増えるとCI時間が線形増加
    → 対策: テストファイル分割+matrix並列実行

  ❌ Docker Build Without Buildx（Buildxなしビルド）:
    → 標準`docker build`コマンドのみ使用
    → レイヤーキャッシュ/マルチプラットフォーム未対応
    → 対策: `docker/setup-buildx-action`+`docker/build-push-action`

  ❌ No Timeout（タイムアウト未設定）:
    → ワークフロー/ジョブにtimeout-minutes未設定
    → デッドロック/無限ループで6時間課金（デフォルト上限）
    → 対策: 全ジョブにtimeout-minutes設定（推奨: 想定時間の2倍）
```

---

## 5. 2026年 課金変更の影響

| 項目 | 変更前 | 変更後（2026年1月〜） |
|------|--------|---------------------|
| ランナー単価 | 従来価格 | 約40%値下げ |
| プラットフォーム課金 | なし | $0.002/分（self-hosted含む） |
| self-hosted課金 | 無料 | $0.002/分（プラットフォーム課金） |
| 96%のユーザー | — | 請求額変更なし |
| 大規模self-hosted利用者 | — | コスト増の可能性 |

---

## 6. Pipe との連携

```
Pipe での活用:
  1. Recon フェーズで PF-01〜07 のパフォーマンススクリーニング
  2. Orchestrate フェーズでキャッシュ戦略の品質チェック
  3. Test フェーズで実行時間・コストの計測
  4. Evolve フェーズでコスト最適化レビュー

品質ゲート:
  - 依存インストールがCI時間の40%超 → キャッシュ導入（PF-01 防止）
  - Docker buildが10分超 → Buildx+レイヤーキャッシュ（PF-04 防止）
  - 全ジョブ直列 → 並列化提案（PF-05 防止）
  - macOS/Windowsランナー → Linux代替可能か確認（Cost 防止）
  - concurrency未設定 → cancel-in-progress追加（Cost 防止）
  - timeout-minutes未設定 → 追加提案（Timeout 防止）
```

**Source:** [Marcus Felling: Optimizing GitHub Actions for Speed](https://marcusfelling.com/blog/2025/optimizing-github-actions-workflows-for-speed) · [WarpBuild: GitHub Actions Cost Reduction](https://www.warpbuild.com/blog/github-actions-cost-reduction) · [Blacksmith: Reduce Spend in GitHub Actions](https://www.blacksmith.sh/blog/how-to-reduce-spend-in-github-actions) · [GitHub: 2026 Pricing Changes](https://github.com/resources/insights/2026-pricing-changes-for-github-actions)
