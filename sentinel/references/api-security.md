# API Security & OWASP API Top 10

> OWASP API Security Top 10 (2023)、BOLA/BFLA、API 固有の脆弱性パターン、検出・緩和策

## 1. OWASP API Security Top 10 (2023)

| Rank | Category | 深刻度 | 頻度 |
|------|----------|--------|------|
| **API1** | Broken Object Level Authorization (BOLA) | Critical | 全 API 攻撃の 40% |
| **API2** | Broken Authentication | Critical | 高 |
| **API3** | Broken Object Property Level Authorization | High | 高 |
| **API4** | Unrestricted Resource Consumption | High | 中 |
| **API5** | Broken Function Level Authorization (BFLA) | Critical | 中 |
| **API6** | Unrestricted Access to Sensitive Business Flows | High | 中 |
| **API7** | Server-Side Request Forgery (SSRF) | High | 中 |
| **API8** | Security Misconfiguration | Medium | 非常に高 |
| **API9** | Improper Inventory Management | Medium | 高 |
| **API10** | Unsafe API Consumption | Medium | 中 |

---

## 2. 主要脆弱性の詳細

### API1: BOLA (Broken Object Level Authorization)

```
攻撃パターン:
  GET /api/users/123/orders  → 自分のオーダー
  GET /api/users/456/orders  → 他人のオーダー（ID を変更）

検出パターン:
  1. エンドポイントにオブジェクト ID が含まれている
  2. サーバーサイドで所有権チェックが欠如
  3. 予測可能な ID（連番 vs UUID）

緩和策:
  □ 全エンドポイントでオブジェクト所有権を検証
  □ 連番 ID → UUID への置換
  □ Row-Level Security の実装
  □ 認可チェックをミドルウェアで一元化
```

```typescript
// ❌ Anti-pattern: 所有権チェックなし
app.get('/api/orders/:id', async (req, res) => {
  const order = await Order.findById(req.params.id);
  res.json(order);
});

// ✅ Pattern: 所有権チェック付き
app.get('/api/orders/:id', async (req, res) => {
  const order = await Order.findOne({
    _id: req.params.id,
    userId: req.user.id,  // 所有権チェック
  });
  if (!order) return res.status(404).json({ error: 'Not found' });
  res.json(order);
});
```

### API3: Broken Object Property Level Authorization

```
旧名: Mass Assignment

攻撃パターン:
  PUT /api/users/123
  { "name": "Alice", "role": "admin" }  ← role を勝手に変更

検出パターン:
  1. リクエストボディがそのまま DB に保存される
  2. フィールドレベルのアクセス制御がない
  3. レスポンスに不要なフィールドが含まれる

緩和策:
  □ 明示的な allowlist でフィールドを制限
  □ JSON Schema で受付フィールドを定義
  □ DTO パターンで入出力を分離
  □ readOnly / writeOnly 制約の設定
```

```typescript
// ❌ Anti-pattern: 全フィールド受入
app.put('/api/users/:id', async (req, res) => {
  await User.findByIdAndUpdate(req.params.id, req.body);
});

// ✅ Pattern: 許可フィールドのみ受入
app.put('/api/users/:id', async (req, res) => {
  const { name, email, avatar } = req.body;  // allowlist
  await User.findByIdAndUpdate(req.params.id, { name, email, avatar });
});
```

### API5: BFLA (Broken Function Level Authorization)

```
攻撃パターン:
  POST /api/users       ← 通常ユーザーが利用可能
  DELETE /api/users/123  ← 管理者専用だが認可チェックなし

検出パターン:
  1. 管理者エンドポイントに認可チェックがない
  2. HTTP メソッドによる権限分離の不備
  3. /admin/ パスに追加の認証がない

緩和策:
  □ 集中型 Policy-as-Code で認可管理
  □ RBAC / ABAC でメソッドレベルの権限定義
  □ JWT claims（scope, groups）による関数レベル認可
  □ deny-by-default ポリシーの採用
```

---

## 3. API セキュリティスキャンチェックリスト

### 認証・認可

```
□ 全エンドポイントに認証が要求されているか?
□ オブジェクトアクセスに所有権チェックがあるか?（BOLA）
□ 管理者機能に関数レベル認可があるか?（BFLA）
□ JWT トークンの署名検証・有効期限チェック
□ API キーのスコープ制限
□ OAuth 2.0 の適切な実装（PKCE）
□ セッション管理の安全性
```

### 入力・出力

```
□ リクエストボディの JSON Schema バリデーション
□ Mass Assignment の防止（allowlist パターン）
□ レスポンスに不要なフィールドが含まれていないか?
□ ページネーション/レート制限の実装
□ ファイルアップロードのサイズ・タイプ制限
□ パスパラメータのバリデーション（UUID 形式等）
```

### インフラ・設定

```
□ CORS ポリシーの適切な設定（* 禁止）
□ TLS の強制（HTTP → HTTPS リダイレクト）
□ API バージョニングの管理
□ 未使用/非推奨エンドポイントの無効化
□ エラーレスポンスに内部情報が含まれていないか?
□ レート制限の設定（API4 対策）
□ API ドキュメントの本番非公開
```

---

## 4. API セキュリティパターン集

### レート制限

> Rate limiting の実装パターンは `defensive-controls.md` § Rate Limiting を参照。
> Express rate-limit、Next.js API limiting、Redis 分散制限の詳細コード例を収録。

### レスポンスフィルタリング

```typescript
// ❌ Anti-pattern: モデル全体を返す
app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(user);  // password, internalId 等も含む
});

// ✅ Pattern: DTO で必要フィールドのみ返す
const toUserDTO = (user: User) => ({
  id: user.id,
  name: user.name,
  email: user.email,
  avatar: user.avatar,
});

app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(toUserDTO(user));
});
```

### SSRF 防止

```typescript
import { URL } from 'url';
import ipaddr from 'ipaddr.js';

function isAllowedUrl(urlString: string): boolean {
  const url = new URL(urlString);

  // プロトコル制限
  if (!['http:', 'https:'].includes(url.protocol)) return false;

  // 内部 IP の拒否
  const addr = ipaddr.parse(url.hostname);
  if (addr.range() !== 'unicast') return false;

  // 許可ドメインのホワイトリスト
  const allowedDomains = ['api.example.com', 'cdn.example.com'];
  if (!allowedDomains.includes(url.hostname)) return false;

  return true;
}
```

---

## 5. Sentinel での API セキュリティスキャン

### 検出パターン

```
Sentinel が検出すべき API セキュリティ問題:

Priority 1 (Critical):
  - BOLA: req.params.id の直接使用（所有権チェックなし）
  - BFLA: admin ルートの認可ミドルウェア欠如
  - Mass Assignment: req.body の直接 DB 保存

Priority 2 (High):
  - CORS: origin: '*' の設定
  - レート制限の未設定
  - JWT 署名未検証
  - SSRF: ユーザー入力 URL への fetch/axios

Priority 3 (Medium):
  - API レスポンスの過剰なフィールド
  - 非推奨エンドポイントの存在
  - エラーレスポンスのスタックトレース漏洩
```

---

## 6. GraphQL Security

### 主要リスクと対策

```
GraphQL 固有のセキュリティ課題:

□ Query Depth Limiting（深いネスト攻撃の防止）
□ Query Complexity Analysis（計算コスト制限）
□ Introspection 制御（本番での無効化）
□ Persisted Queries（任意クエリの禁止）
□ Field-Level Authorization（フィールド単位の認可）
□ Batching Attack 防止（バッチリクエスト制限）
```

```typescript
// Query depth limiting (graphql-depth-limit)
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(5)],  // 最大深度 5
});

// Disable introspection in production
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',
});
```

### OAuth 2.1 パターン

```
OAuth 2.1 主要変更点:
  - Authorization Code + PKCE が必須（Implicit Grant 廃止）
  - Refresh Token Rotation の必須化
  - mTLS クライアント認証の推奨

Sentinel チェック:
  □ PKCE (code_verifier/code_challenge) の実装確認
  □ Implicit Grant (response_type=token) の使用検出
  □ Refresh Token の適切なローテーション
```

**Source:** [Wiz: OWASP API Security Top 10](https://www.wiz.io/academy/api-security/owasp-api-security) · [OWASP: API Security Project](https://owasp.org/www-project-api-security/) · [Axway: OWASP API Security 2026](https://blog.axway.com/learning-center/digital-security/risk-management/owasps-api-security) · [42Crunch: OWASP API Top 10](https://42crunch.com/owasp-api-security-top-10/) · [CyCognito: OWASP API Top 10 2023](https://www.cycognito.com/learn/api-security/owasp-api-security/)
