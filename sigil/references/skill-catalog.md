# Skill Catalog

Framework-specific skill recommendations organized by technology. Use during DISCOVER phase to identify high-value skill opportunities.

---

## JavaScript / TypeScript Ecosystem

### Next.js (App Router)

| Skill | Type | Description |
|-------|------|-------------|
| `new-page` | Micro | App Router ページ作成（metadata, Server Component） |
| `new-api-route` | Micro | Route Handler 作成（GET/POST/PUT/DELETE） |
| `new-component` | Micro | React コンポーネント作成（Props型、テスト） |
| `new-server-action` | Micro | Server Action 作成（バリデーション、エラーハンドリング） |
| `data-fetching` | Full | データ取得パターン（fetch, cache, revalidation） |
| `auth-pattern` | Full | 認証パターン（middleware, session, protected routes） |
| `form-handling` | Full | フォーム処理（RHF + Zod + Server Action） |

### Next.js (Pages Router)

| Skill | Type | Description |
|-------|------|-------------|
| `new-page` | Micro | Pages Router ページ作成（getServerSideProps/getStaticProps） |
| `new-api-route` | Micro | API Route 作成（req/res パターン） |

### React (Vite / CRA)

| Skill | Type | Description |
|-------|------|-------------|
| `new-component` | Micro | コンポーネント作成（Props型、テスト） |
| `new-hook` | Micro | カスタムHook作成（テスト、型定義） |
| `new-context` | Micro | React Context 作成（Provider, hook） |
| `state-management` | Full | 状態管理パターン（Zustand/Jotai/Redux Toolkit） |

### Vue.js / Nuxt

| Skill | Type | Description |
|-------|------|-------------|
| `new-component` | Micro | SFC作成（script setup, Props定義） |
| `new-composable` | Micro | Composable作成（リアクティブ、テスト） |
| `new-store` | Micro | Pinia Store作成 |
| `new-page` | Micro | Nuxt ページ作成（definePageMeta） |

### Express / Fastify

| Skill | Type | Description |
|-------|------|-------------|
| `new-route` | Micro | ルート作成（バリデーション、エラーハンドリング） |
| `new-middleware` | Micro | ミドルウェア作成 |
| `new-controller` | Micro | コントローラ作成（Service層との接続） |
| `error-handling` | Full | エラーハンドリングパターン（ErrorClass、レスポンス） |
| `auth-middleware` | Full | 認証ミドルウェア（JWT/Session, ロールベース） |

### NestJS

| Skill | Type | Description |
|-------|------|-------------|
| `new-module` | Micro | Module + Controller + Service 一括作成 |
| `new-guard` | Micro | Guard作成（認証、認可） |
| `new-pipe` | Micro | Validation Pipe作成 |
| `new-interceptor` | Micro | Interceptor作成（ログ、変換） |

---

## Python Ecosystem

### FastAPI

| Skill | Type | Description |
|-------|------|-------------|
| `new-router` | Micro | APIRouter作成（Pydantic model、依存性注入） |
| `new-model` | Micro | SQLAlchemy/Tortoise モデル作成 |
| `new-schema` | Micro | Pydantic スキーマ作成 |
| `crud-pattern` | Full | CRUD操作パターン（リポジトリ、サービス、ルーター） |
| `auth-pattern` | Full | 認証パターン（OAuth2, JWT, dependency injection） |

### Django

| Skill | Type | Description |
|-------|------|-------------|
| `new-app` | Micro | Django app作成（models, views, urls, admin） |
| `new-model` | Micro | Model作成（フィールド、マイグレーション） |
| `new-view` | Micro | View作成（Class-based / Function-based） |
| `new-serializer` | Micro | DRF Serializer作成 |
| `new-command` | Micro | Management Command作成 |

### Flask

| Skill | Type | Description |
|-------|------|-------------|
| `new-blueprint` | Micro | Blueprint作成（ルート、テンプレート） |
| `new-model` | Micro | SQLAlchemy Model作成 |

---

## Go Ecosystem

### Go (stdlib / Chi / Echo)

| Skill | Type | Description |
|-------|------|-------------|
| `new-handler` | Micro | HTTPハンドラ作成（リクエスト解析、レスポンス） |
| `new-middleware` | Micro | ミドルウェア作成（ログ、認証、CORS） |
| `new-model` | Micro | 構造体 + リポジトリ作成 |
| `new-service` | Micro | サービス層作成（インターフェース、実装） |
| `error-handling` | Full | エラーハンドリングパターン（sentinel errors、wrapping） |
| `testing-pattern` | Full | テストパターン（table-driven、mock、integration） |

### Gin

| Skill | Type | Description |
|-------|------|-------------|
| `new-handler` | Micro | Gin ハンドラ作成（binding、レスポンス） |
| `new-middleware` | Micro | Gin ミドルウェア作成 |

---

## Ruby Ecosystem

### Rails

| Skill | Type | Description |
|-------|------|-------------|
| `new-model` | Micro | ActiveRecord モデル作成（バリデーション、アソシエーション） |
| `new-controller` | Micro | コントローラ作成（strong params、before_action） |
| `new-migration` | Micro | マイグレーション作成 |
| `new-service` | Micro | Service Object作成 |
| `new-job` | Micro | ActiveJob 作成 |
| `api-endpoint` | Full | API エンドポイント作成（serializer、認証、テスト） |

---

## Rust Ecosystem

### Actix-web / Axum

| Skill | Type | Description |
|-------|------|-------------|
| `new-handler` | Micro | ハンドラ作成（extractor、レスポンス） |
| `new-middleware` | Micro | ミドルウェア作成 |
| `error-handling` | Full | エラー型定義（thiserror、anyhow、レスポンス変換） |

---

## Cross-Framework Skills

These skills apply regardless of specific framework:

| Skill | Type | Description |
|-------|------|-------------|
| `naming-rules` | Micro | プロジェクト命名規則一覧 |
| `pr-template` | Micro | PR作成テンプレート（説明、チェックリスト） |
| `env-setup` | Micro | 環境変数設定手順 |
| `deploy-flow` | Full | デプロイフロー（CI/CD手順、チェックリスト） |
| `incident-response` | Full | 障害対応手順（エスカレーション、復旧） |
| `onboarding` | Full | 新メンバーオンボーディング手順 |
| `code-review` | Micro | コードレビュー観点リスト |
| `testing-guide` | Full | テスト戦略ガイド（ユニット、統合、E2E） |

---

## Discovery Priority

When analyzing a project, prioritize skill generation in this order:

1. **High frequency** — Actions performed multiple times daily (new component, new test)
2. **High complexity** — Actions with many steps or decision points (deploy, incident response)
3. **High risk** — Actions where mistakes are costly (migration, security config)
4. **Onboarding value** — Skills that help new team members (conventions, setup)
5. **Consistency value** — Skills that enforce project standards (naming, patterns)
