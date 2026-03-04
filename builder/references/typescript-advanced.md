# TypeScript Advanced Patterns

> satisfies 演算子、branded types、as const パターン、TS 5.8 新機能、strict 設定、enum 代替、パフォーマンス最適化

## 1. satisfies 演算子

型適合を検証しつつ、推論された型情報を維持する。

```typescript
type Color = string | [number, number, number];
const colors = {
  red: [255, 0, 0],
  green: "#00FF00",
} satisfies Record<string, Color>;

// colors.red は [number, number, number] として推論 (Color ではなく)
colors.red.map(v => v * 2);  // OK: タプル操作が可能
```

### as const との組み合わせ

```typescript
type Point = { x: number; y: number };
const point = { x: 2, y: 5 } as const satisfies Point;
// point.x は 2 (number ではなく) として推論
```

### デフォルトエクスポート

```typescript
type StringCallback = (str: string) => string;
export default ((str) => str.toUpperCase()) satisfies StringCallback;
```

**`as` との違い**: `as` はキャストで型チェックを迂回。`satisfies` は完全な型チェック + 推論型保持。

---

## 2. Branded Types

構造的型付けでは区別できない値に「ラベル」を付ける。

```typescript
type Brand<T, B extends string> = T & { readonly __brand: B };

type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;
type Email = Brand<string, "Email">;

// バリデーション付きコンストラクタ
function createEmail(value: string): Email {
    if (!value.includes("@")) throw new Error("Invalid email");
    return value as Email;
}

function getUser(id: UserId): void { /* ... */ }
function getOrder(id: OrderId): void { /* ... */ }

const userId = "usr_123" as UserId;
const orderId = "ord_456" as OrderId;

getUser(userId);   // OK
getUser(orderId);  // コンパイルエラー!
```

---

## 3. as const パターン

### enum の代替 (推奨)

```typescript
// 避ける: ランタイムコード生成、バンドルサイズ増加
enum Status { Pending = "pending", Approved = "approved" }

// 推奨: as const オブジェクト
const Status = {
    Pending: "pending",
    Approved: "approved",
    Rejected: "rejected",
} as const;
type Status = (typeof Status)[keyof typeof Status];
// "pending" | "approved" | "rejected"
```

### リテラル型の保持

```typescript
const colors = ["red", "green", "blue"] as const;
// 型: readonly ["red", "green", "blue"] (string[] ではなく)

const config = { endpoint: "https://api.example.com", retries: 3 } as const;
// config.endpoint: "https://api.example.com" (string ではなく)
```

---

## 4. テンプレートリテラル型

```typescript
type Direction = `scroll-${"top" | "bottom" | "left" | "right"}`;
// "scroll-top" | "scroll-bottom" | "scroll-left" | "scroll-right"

type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type ApiEndpoint = "/users" | "/posts";
type FullEndpoint = `${HttpMethod} ${ApiEndpoint}`;
```

---

## 5. 型安全パターン

### 網羅性チェック

```typescript
type Shape = "circle" | "square" | "triangle";

function getArea(shape: Shape): number {
    switch (shape) {
        case "circle": return Math.PI;
        case "square": return 1;
        case "triangle": return 0.5;
        default:
            const _exhaustive: never = shape; // 新 Shape 追加時にエラー
            return _exhaustive;
    }
}
```

### 型ガード vs 型アサーション

```typescript
// 悪い: ランタイム安全性なし
const user = data as User;

// 良い: ランタイムチェック付き
function isUser(value: unknown): value is User {
    return typeof value === "object" && value !== null
        && "name" in value && typeof (value as any).name === "string";
}
```

### アサーション関数

```typescript
function assertAdmin(user: User): asserts user is AdminUser {
    if (user.role !== "admin") throw new Error("Not admin");
}

assertAdmin(user);
// 以降 user は AdminUser として推論
```

### ルックアップ型 (Single Source of Truth)

```typescript
// 悪い: 型のコピペ
function getUser(id: number): Response { ... }

// 良い: ソース型を参照
function getUser(id: Employee["departmentId"]): Response { ... }
```

---

## 6. TypeScript 5.8 新機能

| 機能 | 説明 |
|------|------|
| return 式の分岐チェック | 三項演算子の各分岐を厳密に型チェック |
| `--erasableSyntaxOnly` | Node.js 型消去モード対応 (enum/namespace/パラメータプロパティ禁止) |
| `import with` 構文強制 | `assert` を廃止、`with { type: "json" }` を使用 |
| ビルド高速化 | パス正規化の最適化 |

---

## 7. tsconfig.json 推奨設定

### Node.js バックエンド

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "skipLibCheck": true,
    "isolatedModules": true,
    "incremental": true,
    "verbatimModuleSyntax": true
  }
}
```

### フロントエンド (バンドラー使用)

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "lib": ["DOM", "DOM.Iterable", "ESNext"],
    "strict": true,
    "skipLibCheck": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true
  }
}
```

### 追加推奨オプション

| オプション | 目的 |
|-----------|------|
| `exactOptionalPropertyTypes` | optional プロパティの厳密な扱い |
| `forceConsistentCasingInFileNames` | クロスプラットフォーム互換 |
| `noUnusedLocals` / `noUnusedParameters` | 未使用コード検出 |

---

## 8. コンパイルパフォーマンス

| 手法 | 説明 |
|------|------|
| 交差型よりインターフェース | `interface Foo extends Bar, Baz {}` は `type Foo = Bar & Baz` より高速 |
| 明示的戻り値型 | コンパイラの推論負荷を軽減 |
| 大規模ユニオン回避 | ペアワイズ比較で二次コスト |
| 型チェックとトランスパイル分離 | `tsc --noEmit` + esbuild/swc |
| プロジェクト参照 | モノレポで 5-20 プロジェクトに分割 |

### 診断コマンド

```bash
tsc --extendedDiagnostics  # 各フェーズの時間測定
tsc --generateTrace output  # Chrome DevTools で分析
```

---

## 9. アンチパターン

| # | パターン | 修正 |
|---|---------|------|
| 1 | `any` 型の乱用 | `unknown` + 型ガード |
| 2 | `Function` 型 | 具体的な関数シグネチャ |
| 3 | 通常の `enum` | `as const` オブジェクト |
| 4 | forEach + async | `for...of` (逐次) / `Promise.all` (並列) |
| 5 | 型アサーション (`as`) 多用 | 型ガード / `satisfies` |
| 6 | ランタイムバリデーション不足 | Zod で外部データをパース |
| 7 | 不要なクラス | オブジェクトリテラル / 関数 |
| 8 | 型定義のコピペ | `Partial<T>`, `Pick<T>`, ルックアップ型 |
| 9 | 過度な抽象化 | サービスレイヤーは浅く |

**Source:** [satisfies (2ality)](https://2ality.com/2025/02/satisfies-operator.html) · [Total TypeScript Patterns](https://www.totaltypescript.com/four-essential-typescript-patterns) · [TS Performance Wiki](https://github.com/microsoft/Typescript/wiki/Performance) · [TS 5.8 Release](https://devblogs.microsoft.com/typescript/announcing-typescript-5-8/)
