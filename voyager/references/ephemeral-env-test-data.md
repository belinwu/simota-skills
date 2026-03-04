# Ephemeral Environments & Test Data Strategy

> エフェメラル/プレビュー環境、テストデータ管理、テスト分離、API ファーストセットアップ

## 1. エフェメラル環境（Ephemeral Environments）

### 定義

PR ごとに自動生成・破棄されるフルスタック環境。テストの一貫性と並列開発を実現。

### 従来の共有環境 vs エフェメラル環境

| 観点 | 共有ステージング | エフェメラル環境 |
|------|---------------|---------------|
| **環境数** | 1-3（共有） | PR ごとに自動生成 |
| **データ汚染** | 高（チーム間干渉） | なし（独立） |
| **待ち時間** | 他チームの使用待ち | ゼロ（即時利用） |
| **テスト信頼性** | 低（環境要因のフレーキー） | 高（クリーンスレート） |
| **コスト** | 常時稼働 | 使用時のみ（PR 期間） |
| **フィードバック速度** | マージ後 | PR 作成直後 |

### エフェメラル環境のライフサイクル

```
PR 作成
  → 環境自動プロビジョニング
    → DB マイグレーション + シードデータ
      → E2E テスト自動実行
        → レビュアーがプレビュー URL で確認
          → PR マージ or クローズ
            → 環境自動破棄
```

### 実装パターン

| パターン | ツール例 | 特徴 |
|---------|---------|------|
| **Container-based** | Docker Compose + CI | ローカル再現可能、低コスト |
| **Kubernetes-based** | Namespace per PR | スケーラブル、本番に近い |
| **PaaS-based** | Vercel Preview, Bunnyshell | ゼロ設定、高速デプロイ |
| **Hybrid** | フロントエンド PaaS + バックエンド Container | 柔軟性と速度のバランス |

### GitHub Actions 統合例

```yaml
name: E2E Tests on Preview
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  preview-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # エフェメラル環境の起動
      - name: Start preview environment
        run: docker compose -f docker-compose.test.yml up -d

      # DB シード
      - name: Seed database
        run: npm run db:seed:test

      # E2E テスト実行
      - name: Run E2E tests
        run: npx playwright test --tag @smoke

      # 環境の破棄
      - name: Cleanup
        if: always()
        run: docker compose -f docker-compose.test.yml down -v
```

---

## 2. テストデータ管理戦略

### テストデータの原則

```
1. 各テストが自分のデータを作成・破棄する（自己完結）
2. API ファーストでデータを作成する（UI 操作は遅い + フレーキー）
3. ファクトリパターンで一貫性のあるデータを生成する
4. 本番データは使わない（匿名化された場合を除く）
5. テスト間でデータを共有しない
```

### データセットアップパターン

| パターン | 速度 | 信頼性 | 使用場面 |
|---------|------|--------|---------|
| **API 直接呼び出し** | 高速 | 高 | ユーザー作成、データ準備 |
| **DB 直接操作** | 最速 | 中（スキーマ依存） | 大量データ、特殊状態 |
| **UI 操作** | 低速 | 低（フレーキー） | **避けるべき** |
| **フィクスチャファイル** | 高速 | 高 | 静的テストデータ |
| **シードスクリプト** | 中速 | 高 | 環境初期化 |

### テストデータファクトリ

```typescript
// helpers/test-data-factory.ts
import { APIRequestContext } from '@playwright/test';

export class TestDataFactory {
  constructor(private api: APIRequestContext) {}

  async createUser(overrides: Partial<User> = {}): Promise<User> {
    const user = {
      email: `test-${Date.now()}@example.com`,
      name: 'Test User',
      password: 'TestPassword123!',
      ...overrides,
    };

    const response = await this.api.post('/api/test/users', { data: user });
    return response.json();
  }

  async createProduct(overrides: Partial<Product> = {}): Promise<Product> {
    const product = {
      name: `Product ${Date.now()}`,
      price: 1999,
      stock: 100,
      ...overrides,
    };

    const response = await this.api.post('/api/test/products', { data: product });
    return response.json();
  }

  async cleanup(userId: string): Promise<void> {
    await this.api.delete(`/api/test/users/${userId}`);
  }
}
```

### Playwright フィクスチャとの統合

```typescript
// fixtures/test-fixtures.ts
import { test as base } from '@playwright/test';
import { TestDataFactory } from '../helpers/test-data-factory';

type TestFixtures = {
  factory: TestDataFactory;
  testUser: User;
};

export const test = base.extend<TestFixtures>({
  factory: async ({ request }, use) => {
    await use(new TestDataFactory(request));
  },

  testUser: async ({ factory }, use) => {
    const user = await factory.createUser();
    await use(user);
    await factory.cleanup(user.id);  // 自動クリーンアップ
  },
});
```

---

## 3. テスト分離パターン

### 分離レベル

| レベル | 手法 | コスト | 信頼性 |
|--------|------|--------|--------|
| **L1: ブラウザコンテキスト** | テストごとに新コンテキスト | 低 | 中 |
| **L2: データ分離** | テストごとにユニークデータ | 低 | 高 |
| **L3: DB トランザクション** | テスト後にロールバック | 中 | 高 |
| **L4: 環境分離** | テストごとに別コンテナ | 高 | 最高 |

### 認証状態の分離

```typescript
// ❌ Anti-pattern: 全テストで同じアカウント
const SHARED_USER = { email: 'test@example.com', password: 'test123' };

// ✅ Pattern: テストごとにユニークユーザー
test('user can update profile', async ({ page, factory }) => {
  const user = await factory.createUser();
  const storageState = await authenticateUser(user);

  const context = await browser.newContext({ storageState });
  const page = await context.newPage();
  // ... テスト実行
});
```

### 並列実行との整合性

```
並列実行時のデータ衝突防止:
  1. テストデータにタイムスタンプ/UUID を含める
  2. テスト専用の DB スキーマ/テナントを使用
  3. ネットワークインターセプトで外部依存を排除
  4. グローバル状態を変更するテストは serial モードで実行
```

---

## 4. ネットワークインターセプト戦略

### 用途別パターン

| 用途 | 手法 | 例 |
|------|------|-----|
| **外部 API の排除** | route.fulfill() | 決済 API、メール送信 |
| **遅延シミュレーション** | route.continue() + delay | スロー API のテスト |
| **エラー状態の再現** | route.fulfill({ status: 500 }) | サーバーエラー |
| **レスポンス固定** | route.fulfill({ body }) | 一貫したテストデータ |

### 実装例

```typescript
// 外部 API のモック
await page.route('**/api/payment/**', async route => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      success: true,
      transactionId: 'test-txn-001'
    }),
  });
});

// 遅延レスポンスのシミュレーション
await page.route('**/api/search**', async route => {
  await new Promise(resolve => setTimeout(resolve, 3000));
  await route.continue();
});
```

---

## 5. テスト環境のアンチパターン

### AWS Well-Architected DevOps Guidance

| アンチパターン | 症状 | 対策 |
|-------------|------|------|
| **Snowflake 環境** | 手動構築で再現不可能 | IaC で環境を定義 |
| **共有環境の汚染** | テスト間でデータが干渉 | エフェメラル環境の採用 |
| **本番データの直接使用** | プライバシーリスク + 不安定 | シードデータ + ファクトリ |
| **環境ドリフト** | テスト環境が本番と乖離 | Docker / K8s で統一 |
| **テスト環境の待ち行列** | チーム間で環境を奪い合い | PR ごとのエフェメラル環境 |

### Voyager での環境戦略マッピング

| Voyager モード | 環境タイプ | テストデータ |
|--------------|----------|------------|
| Plan | 設計のみ | — |
| Automate | ローカル Docker | ファクトリ + シード |
| Stabilize | エフェメラル（CI） | API ファーストセットアップ |
| Scale | 並列エフェメラル | 完全分離データ |

**Source:** [Bunnyshell: E2E Testing Best Practices 2025](https://www.bunnyshell.com/blog/best-practices-for-end-to-end-testing-in-2025/) · [Bunnyshell: E2E Testing for Microservices 2025](https://www.bunnyshell.com/blog/end-to-end-testing-for-microservices-a-2025-guide/) · [AWS: Anti-patterns for Test Environment Management](https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/anti-patterns-for-test-environment-management.html) · [Cypress: Preview Environments Webinar](https://www.cypress.io/blog/webinar-preview-environments) · [Perforce: Ephemeral Test Environments](https://www.perforce.com/blog/pdx/ephemeral-test-environments)
