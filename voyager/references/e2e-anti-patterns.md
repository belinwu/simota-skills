# E2E Testing Anti-Patterns & Test Architecture

> E2E テストの失敗パターン、スケーラブルなテストアーキテクチャ、フレーキーテスト防止、テストスイート管理

## 1. E2E テスト・アンチパターン

### セレクタの脆弱性（Selector Fragility）

```typescript
// ❌ Anti-pattern: 位置ベース・CSS クラスセレクタ
await page.click('div:nth-child(3) > button');
await page.click('.btn-primary-v2');

// ✅ Pattern: data-testid / ARIA ロール
await page.getByRole('button', { name: 'Submit' });
await page.getByTestId('checkout-button');
```

**影響:** UI リファクタリングのたびにテスト破損 → メンテナンスコスト増大

### テスト間依存（Test Interdependence）

```
❌ Test A: ユーザー作成 → Test B: そのユーザーでログイン → Test C: プロフィール更新
  → Test A が失敗すると B, C も連鎖失敗

✅ 各テストが独立: 自分のデータを作成 → 操作 → クリーンアップ
```

**対策:** API ファーストなデータセットアップ、テストごとのフレッシュコンテキスト

### 過剰な待機（Excessive Waiting）

```typescript
// ❌ Anti-pattern: 任意のタイムアウト
await page.waitForTimeout(5000);

// ✅ Pattern: 条件付き待機
await page.waitForResponse(resp => resp.url().includes('/api/data'));
await expect(page.getByRole('heading')).toBeVisible();
```

**Playwright の auto-waiting を最大限活用。** 明示的待機は API レスポンス・特定要素の出現のみ。

### テスト肥大化（Test Bloat / The Giant）

```
❌ 1テストで 100ステップ:
   ログイン → プロフィール設定 → 商品検索 → カート追加 → 決済 → 注文確認

✅ ビジネス目的ごとに分割:
   - test: ユーザーがログインできる
   - test: ユーザーが商品をカートに追加できる
   - test: ユーザーが決済を完了できる
```

### E2E の乱用（Wrong Test Level）

| ❌ E2E で書くべきでないもの | ✅ 適切なレベル |
|--------------------------|--------------|
| 入力バリデーションロジック | Unit テスト |
| データ変換・フォーマット | Unit テスト |
| API レスポンス形式 | Integration / Contract テスト |
| 単一コンポーネントの表示 | Component テスト |

### テスト爆発（Test Explosion）

**2026年の新課題:** AI テスト生成により数百のテストが容易に作成可能 → どのテストが CI に属するか、冗長か、コスト高すぎるかの判断がボトルネックに。

**対策:**
- タグベースの優先度分類（`@critical` / `@smoke` / `@regression`）
- ビジネスクリティカルパスのみ CI 必須
- 冗長テストの定期的なプルーニング

---

## 2. フレーキーテスト防止戦略

### フレーキーの根本原因

| 原因 | 割合 | 対策 |
|------|------|------|
| **タイミング/非同期** | 40% | auto-waiting、条件付き待機 |
| **テストデータの汚染** | 25% | API ファーストデータ、テスト分離 |
| **環境の不整合** | 20% | エフェメラル環境、Docker |
| **共有状態** | 10% | フレッシュブラウザコンテキスト |
| **外部依存** | 5% | ネットワークインターセプト、モック |

### フレーキー防止チェックリスト

```markdown
## Flaky Prevention Checklist

### 設計時
- [ ] テストは完全に独立して実行可能か?
- [ ] テストデータは API で作成しているか?
- [ ] `waitForTimeout()` を使用していないか?
- [ ] 外部サービスをモック/インターセプトしているか?

### 実装時
- [ ] auto-waiting が機能するロケータを使用しているか?
- [ ] ネットワークレスポンスの待機が明示的か?
- [ ] アニメーション完了を適切に待機しているか?
- [ ] 日時/タイムゾーン依存がないか?

### CI 運用
- [ ] 同一テストを複数回実行してフレーキーを検出しているか?
- [ ] フレーキーレート < 1% を維持しているか?
- [ ] リトライは最大 2回に制限しているか?
- [ ] フレーキーテストの root cause を追跡しているか?
```

---

## 3. テストスイートアーキテクチャ

### テストピラミッド内の E2E 比率

```
E2E テスト: 5-10%（ビジネスクリティカルのみ）
  → 目標: 30分以内で完了
  → 並列実行 + シャーディング
  → タグベース優先実行

Integration: 20%
Unit: 70%
```

### ディレクトリ構造パターン

```
tests/
  e2e/
    auth/
      login.spec.ts
      signup.spec.ts
    checkout/
      cart.spec.ts
      payment.spec.ts
    settings/
      profile.spec.ts
  fixtures/
    auth.fixture.ts
    data.fixture.ts
  pages/
    LoginPage.ts
    CheckoutPage.ts
  helpers/
    api-client.ts
    test-data-factory.ts
```

### テスト分類とタグ戦略

| タグ | 実行タイミング | 含むテスト | 目標時間 |
|------|-------------|----------|---------|
| `@smoke` | 全 PR | ログイン、主要フロー | < 5分 |
| `@critical` | マージ前 | 決済、認証、データ操作 | < 15分 |
| `@regression` | Nightly | 全 E2E テスト | < 30分 |
| `@visual` | 週次 / 手動 | Visual regression | 可変 |

---

## 4. テストメンテナンスの原則

### テストコードは本番コードと同等に扱う

```
1. コードレビューの対象にする
2. リファクタリングを定期的に行う
3. 命名規則を統一する（should_verb_when_condition）
4. ヘルパー/ユーティリティを DRY にする
5. 不要なテストを定期的にプルーニングする
```

### メンテナンスコスト低減パターン

| パターン | 効果 |
|---------|------|
| Page Object Model | UI 変更の影響を 1箇所に集約 |
| テストデータファクトリ | データ作成の一元化 |
| カスタムフィクスチャ | セットアップの再利用 |
| ネットワークインターセプト | 外部依存の排除 |
| タグベース実行 | 必要なテストのみ実行 |

**Source:** [Thunders.ai: Modern E2E Test Architecture](https://www.thunders.ai/articles/modern-e2e-test-architecture-patterns-and-anti-patterns-for-a-maintainable-test-suite) · [Bunnyshell: E2E Testing Best Practices 2025](https://www.bunnyshell.com/blog/best-practices-for-end-to-end-testing-in-2025/) · [Playwright: Best Practices](https://playwright.dev/docs/best-practices) · [Momentic: Playwright E2E Best Practices](https://momentic.ai/blog/playwright-e2e-testing-best-practices)
