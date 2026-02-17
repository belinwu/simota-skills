# Skill Catalog

Framework-specific skill recommendations organized by technology. Use during DISCOVER phase to identify high-value skill opportunities.

---

## JavaScript / TypeScript Ecosystem

### Next.js (App Router)

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-page` | Micro | App Router ページ作成（metadata, Server Component） | Pages Router → App Router migration |
| `new-api-route` | Micro | Route Handler 作成（GET/POST/PUT/DELETE） | API Routes → Route Handlers |
| `new-component` | Micro | React コンポーネント作成（Props型、テスト） | Class → Functional → Server Component |
| `new-server-action` | Micro | Server Action 作成（バリデーション、エラーハンドリング） | — (App Router native) |
| `data-fetching` | Full | データ取得パターン（fetch, cache, revalidation） | getServerSideProps → Server Component fetch |
| `auth-pattern` | Full | 認証パターン（middleware, session, protected routes） | — |
| `form-handling` | Full | フォーム処理（RHF + Zod + Server Action） | Client-only → Server Action hybrid |

### Next.js (Pages Router)

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-page` | Micro | Pages Router ページ作成（getServerSideProps/getStaticProps） | → App Router `new-page` |
| `new-api-route` | Micro | API Route 作成（req/res パターン） | → App Router `new-api-route` |

### React (Vite / CRA)

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-component` | Micro | コンポーネント作成（Props型、テスト） | CRA → Vite migration |
| `new-hook` | Micro | カスタムHook作成（テスト、型定義） | — |
| `new-context` | Micro | React Context 作成（Provider, hook） | Context → Zustand/Jotai |
| `state-management` | Full | 状態管理パターン（Zustand/Jotai/Redux Toolkit） | Redux → Redux Toolkit → Zustand |

### Vue.js / Nuxt

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-component` | Micro | SFC作成（script setup, Props定義） | Options API → Composition API |
| `new-composable` | Micro | Composable作成（リアクティブ、テスト） | Mixin → Composable |
| `new-store` | Micro | Pinia Store作成 | Vuex → Pinia |
| `new-page` | Micro | Nuxt ページ作成（definePageMeta） | Nuxt 2 → Nuxt 3 |

### Remix

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-route` | Micro | Remix ルート作成（loader, action, component） | — |
| `new-loader` | Micro | Loader関数作成（データ取得、エラーハンドリング） | — |
| `new-action` | Micro | Action関数作成（フォーム処理、バリデーション） | — |
| `error-boundary` | Micro | ErrorBoundary + CatchBoundary 作成 | — |
| `auth-pattern` | Full | 認証パターン（session, cookie, protected routes） | — |

### Express / Fastify

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-route` | Micro | ルート作成（バリデーション、エラーハンドリング） | Express → Fastify migration |
| `new-middleware` | Micro | ミドルウェア作成 | — |
| `new-controller` | Micro | コントローラ作成（Service層との接続） | — |
| `error-handling` | Full | エラーハンドリングパターン（ErrorClass、レスポンス） | — |
| `auth-middleware` | Full | 認証ミドルウェア（JWT/Session, ロールベース） | — |

### Hono

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-route` | Micro | Honoルート作成（型安全、バリデーション） | Express → Hono migration |
| `new-middleware` | Micro | Honoミドルウェア作成 | — |
| `new-validator` | Micro | Zod/Valibot バリデーション統合 | — |
| `api-pattern` | Full | REST APIパターン（OpenAPI統合、エラーハンドリング） | — |

### tRPC

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-router` | Micro | tRPCルーター作成（procedure定義） | REST → tRPC migration |
| `new-procedure` | Micro | Query/Mutation/Subscription作成 | — |
| `new-middleware` | Micro | tRPCミドルウェア作成（認証、ログ） | — |
| `trpc-pattern` | Full | tRPCフルスタックパターン（client + server + types） | — |

### NestJS

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-module` | Micro | Module + Controller + Service 一括作成 | — |
| `new-guard` | Micro | Guard作成（認証、認可） | — |
| `new-pipe` | Micro | Validation Pipe作成 | — |
| `new-interceptor` | Micro | Interceptor作成（ログ、変換） | — |

### Bun

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-server` | Micro | Bun.serve サーバー作成 | Node.js → Bun migration |
| `new-test` | Micro | Bun テスト作成（bun:test） | Jest → Bun test |
| `new-script` | Micro | Bun スクリプト作成（Shell, File I/O） | — |

---

## Python Ecosystem

### FastAPI

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-router` | Micro | APIRouter作成（Pydantic model、依存性注入） | Flask → FastAPI migration |
| `new-model` | Micro | SQLAlchemy/Tortoise モデル作成 | — |
| `new-schema` | Micro | Pydantic スキーマ作成 | Pydantic v1 → v2 |
| `crud-pattern` | Full | CRUD操作パターン（リポジトリ、サービス、ルーター） | — |
| `auth-pattern` | Full | 認証パターン（OAuth2, JWT, dependency injection） | — |

### Django

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-app` | Micro | Django app作成（models, views, urls, admin） | — |
| `new-model` | Micro | Model作成（フィールド、マイグレーション） | — |
| `new-view` | Micro | View作成（Class-based / Function-based） | FBV → CBV migration |
| `new-serializer` | Micro | DRF Serializer作成 | — |
| `new-command` | Micro | Management Command作成 | — |

### Flask

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-blueprint` | Micro | Blueprint作成（ルート、テンプレート） | Flask → FastAPI migration |
| `new-model` | Micro | SQLAlchemy Model作成 | — |

---

## Go Ecosystem

### Go (stdlib / Chi / Echo)

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-handler` | Micro | HTTPハンドラ作成（リクエスト解析、レスポンス） | net/http → Chi/Echo |
| `new-middleware` | Micro | ミドルウェア作成（ログ、認証、CORS） | — |
| `new-model` | Micro | 構造体 + リポジトリ作成 | — |
| `new-service` | Micro | サービス層作成（インターフェース、実装） | — |
| `error-handling` | Full | エラーハンドリングパターン（sentinel errors、wrapping） | — |
| `testing-pattern` | Full | テストパターン（table-driven、mock、integration） | — |

### Gin

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-handler` | Micro | Gin ハンドラ作成（binding、レスポンス） | Gin → Chi/Echo |
| `new-middleware` | Micro | Gin ミドルウェア作成 | — |

---

## Ruby Ecosystem

### Rails

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-model` | Micro | ActiveRecord モデル作成（バリデーション、アソシエーション） | — |
| `new-controller` | Micro | コントローラ作成（strong params、before_action） | — |
| `new-migration` | Micro | マイグレーション作成 | — |
| `new-service` | Micro | Service Object作成 | — |
| `new-job` | Micro | ActiveJob 作成 | — |
| `api-endpoint` | Full | API エンドポイント作成（serializer、認証、テスト） | — |

---

## Rust Ecosystem

### Actix-web / Axum

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `new-handler` | Micro | ハンドラ作成（extractor、レスポンス） | Actix → Axum |
| `new-middleware` | Micro | ミドルウェア作成 | — |
| `error-handling` | Full | エラー型定義（thiserror、anyhow、レスポンス変換） | — |

---

## Cross-Framework Skills

These skills apply regardless of specific framework:

| Skill | Type | Description | Evolution Path |
|-------|------|-------------|---------------|
| `naming-rules` | Micro | プロジェクトの命名規則一覧 | — (project-specific, no migration) |
| `pr-template` | Micro | PR作成テンプレート（説明、チェックリスト） | — |
| `env-setup` | Micro | 環境変数設定手順 | — |
| `deploy-flow` | Full | デプロイフロー（CI/CD手順、チェックリスト） | Platform-specific evolution |
| `incident-response` | Full | 障害対応手順（エスカレーション、復旧） | — |
| `onboarding` | Full | 新メンバーオンボーディング手順 | — |
| `code-review` | Micro | コードレビュー観点リスト | — |
| `testing-guide` | Full | テスト戦略ガイド（ユニット、統合、E2E） | — |

---

## Discovery Priority

When analyzing a project, prioritize skill generation in this order:

1. **High frequency** — Actions performed multiple times daily (new component, new test)
2. **High complexity** — Actions with many steps or decision points (deploy, incident response)
3. **High risk** — Actions where mistakes are costly (migration, security config)
4. **Onboarding value** — Skills that help new team members (conventions, setup)
5. **Consistency value** — Skills that enforce project standards (naming, patterns)

---

## Evolution Path Usage

The Evolution Path column indicates known migration patterns. During Skill Evolution:

1. **Check current version** against Evolution Path
2. **If migration detected** (e.g., Pages Router → App Router), use the path to guide skill update
3. **If no path listed** (`—`), skill is framework-native and evolves with minor version updates
4. **Framework migration** (e.g., Express → Hono) triggers full skill replacement, not in-place update

→ Details: `evolution-patterns.md`
