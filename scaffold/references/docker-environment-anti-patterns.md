# Docker / Dev Environment Anti-Patterns

> Docker Compose設計、コンテナ構成、ローカル開発環境、シークレット管理の失敗パターン

## 1. コンテナ設計 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **DC-01** | **Multi-Concern Container（多責務コンテナ）** | 1コンテナにDB+App+Nginx+SSHを同梱 | プロセス管理の複雑化、スケーリング不能、障害切り分け困難 | 1コンテナ=1プロセス原則、docker-composeでサービス分離 |
| **DC-02** | **Dev-Prod Same Image（開発=本番同一イメージ）** | 開発ツール（git/compiler/test fw）入りイメージを本番使用 | 本番イメージの肥大化、攻撃面の拡大 | multi-stage build: dev stageとprod stageを分離 |
| **DC-03** | **Different Images Per Env（環境別イメージ）** | dev/staging/prodで異なるDockerfileからビルド | 環境間の挙動差異、「stagingで動いたが prod で動かない」 | 単一イメージ+環境変数/configで挙動切替 |
| **DC-04** | **Fat Image（肥大イメージ）** | 不要なパッケージ・キャッシュ・ビルド成果物が残留 | イメージサイズ1GB超、pull遅延、ストレージ浪費 | .dockerignore徹底、multi-stage build、alpine/distroless使用 |
| **DC-05** | **Latest Tag Dependency（latestタグ依存）** | FROM image:latest でベースイメージ未固定 | ビルドの再現性なし、突然の破壊的変更 | 具体的なバージョンタグまたはdigestでpin |
| **DC-06** | **Root User Default（rootユーザーデフォルト）** | コンテナ内プロセスがroot権限で実行 | コンテナエスケープ時の被害拡大、セキュリティ監査失敗 | USER命令で非rootユーザー指定、rootlessモード活用 |
| **DC-07** | **Secrets in Image Layer（イメージ層のシークレット）** | DockerfileのENVやCOPYでシークレットを埋め込み | docker historyで秘密鍵が閲覧可能 | BuildKit --mount=type=secret、実行時マウント |

---

## 2. Docker Compose設計の罠

```
Compose設計の失敗:

  ❌ Hardcoded Secrets in YAML（YAMLにシークレット直書き）:
    → docker-compose.ymlにDB_PASSWORD等を記述
    → GitコミットでシークレットがVCSに露出
    → 対策: .env + docker secrets + .gitignore

  ❌ No Health Checks（ヘルスチェックなし）:
    → depends_onだけでサービス起動順序を制御
    → DBが起動途中でアプリが接続失敗
    → 対策: healthcheck + depends_on: condition: service_healthy

  ❌ Bind Mount Everything（全ディレクトリバインドマウント）:
    → ホストの / やプロジェクトルート全体をマウント
    → node_modules衝突、.git/secret漏洩、パフォーマンス低下
    → 対策: 必要なディレクトリのみマウント、node_modulesはnamed volume

  ❌ No Resource Limits（リソース制限なし）:
    → memory/CPU制限を設定しない
    → 1コンテナがホストリソースを占有、OOM Killer発動
    → 対策: deploy.resources.limits で memory/cpus を設定

  ❌ Network Default Bridge（デフォルトブリッジ依存）:
    → カスタムネットワークを定義しない
    → 全コンテナが相互通信可能、セキュリティ境界なし
    → 対策: サービス群ごとにカスタムネットワーク定義

  ❌ YAML Complexity Spiral（YAML複雑化スパイラル）:
    → override、extends、環境変数展開の多重化
    → YAML解読困難、変更時のデバッグに時間浪費
    → 対策: compose.yaml + compose.override.yaml の2層構成に限定
```

---

## 3. シークレット管理のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **SE-01** | **Environment Variable Secrets（環境変数シークレット）** | 機密情報をENVで注入 | `docker inspect`で閲覧可能、プロセスリストに露出 | Docker secrets (file-based mount to /run/secrets/) |
| **SE-02** | **Committed .env Files（.envコミット）** | .envファイルをGitにコミット | リポジトリにDBパスワード・APIキーが残留 | .gitignore + .env.example（ダミー値） |
| **SE-03** | **Build-time Secrets（ビルド時シークレット）** | ARGでシークレットを渡しイメージ層に残存 | docker historyでシークレット閲覧可能 | BuildKit --mount=type=secret (layerに残らない) |
| **SE-04** | **No Rotation（ローテーションなし）** | シークレットを一度設定して永続使用 | 長期間同一の認証情報、侵害時の影響範囲拡大 | 定期ローテーション + Vault/Secrets Manager連携 |

---

## 4. ローカル開発環境の罠

```
開発環境の失敗:

  ❌ Works On My Machine（自分の環境では動く）:
    → Docker化されていない依存（nativeバイナリ、OS固有ライブラリ）
    → チームメンバー間でビルド失敗、CI/CDとの挙動差異
    → 対策: 全依存をDockerfile内で管理、Dev Containers活用

  ❌ No Hot Reload（ホットリロードなし）:
    → コード変更のたびにイメージ再ビルド
    → 開発サイクル遅延（30秒→5分）
    → 対策: volume mount + watchモード、Docker Compose develop.watch

  ❌ Missing Seed Data（シードデータ欠如）:
    → 開発DB起動後にデータなし
    → 毎回手動でデータ投入、テスト再現性なし
    → 対策: init-scripts/ で自動シード、volume永続化

  ❌ Platform Inconsistency（プラットフォーム不整合）:
    → M1/M2 Mac でamd64イメージが遅い
    → Rosettaエミュレーション、ビルド失敗
    → 対策: multi-platform build (--platform linux/amd64,linux/arm64)

  ❌ Docker Compose as Production Orchestrator:
    → docker-compose.ymlをそのまま本番で使用
    → HA/スケーリング/ローリングデプロイなし
    → 対策: 開発=Compose、本番=ECS/K8s/Cloud Run（ツール分離）
```

---

## 5. Dockerfile最適化のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **DF-01** | **No .dockerignore（.dockerignore欠如）** | .git、node_modules、.envがコンテキストに含まれる | ビルドコンテキスト送信が遅い、シークレット漏洩リスク | .dockerignore に .git/.env/node_modules/test/ 等を明記 |
| **DF-02** | **Poor Layer Ordering（レイヤー順序不良）** | COPYソースコード→RUN npm install の順序 | コード変更のたびに依存も再インストール | 依存ファイル(package.json)を先にCOPY→install→ソースCOPY |
| **DF-03** | **No Cache Optimization（キャッシュ未最適化）** | 変更頻度の高いレイヤーが先にある | ビルドキャッシュが毎回無効化、ビルド時間増大 | 変更頻度低→高の順序でレイヤー構成 |
| **DF-04** | **Multiple RUN Chains（過剰なRUN連鎖）** | 各コマンドを個別のRUN命令で実行 | レイヤー数増大、中間キャッシュ浪費 | &&で連結、apt-get update && install && clean を1RUNに |

---

## 6. Scaffold との連携

```
Scaffold での活用:
  1. ASSESS フェーズで DC-01〜07 のコンテナ設計スクリーニング
  2. DESIGN フェーズで Compose 構成の品質チェック
  3. IMPLEMENT フェーズで SE-01〜04 のシークレット管理確認
  4. VERIFY フェーズで DF-01〜04 の Dockerfile 最適化確認

品質ゲート:
  - 1コンテナ複数プロセス → サービス分離提案（DC-01 防止）
  - FROM :latest 検出 → バージョンpin提案（DC-05 防止）
  - docker-compose.yml にシークレット直書き → secrets移行（SE-01 防止）
  - .env が .gitignore に未登録 → 追加提案（SE-02 防止）
  - healthcheck 未設定 → depends_on condition追加（Health Check 防止）
  - .dockerignore 欠如 → テンプレート提供（DF-01 防止）
  - COPY . . が依存installの前 → 順序最適化（DF-02 防止）
```

**Source:** [Codefresh: Docker Anti-Patterns](https://codefresh.io/blog/docker-anti-patterns/) · [Docker Docs: Secrets in Compose](https://docs.docker.com/compose/how-tos/use-secrets/) · [Docker Docs: Environment Variables Best Practices](https://docs.docker.com/compose/how-tos/environment-variables/best-practices/) · [GitGuardian: 4 Ways to Securely Store Secrets in Docker](https://blog.gitguardian.com/how-to-handle-secrets-in-docker/)
