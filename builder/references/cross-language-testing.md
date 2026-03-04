# Cross-Language Testing Patterns

> テスト設計原則、モック戦略、プロパティベーステスト、統合テスト、言語別パターン比較

## 1. テスト設計原則

### Testing Trophy (2025 推奨)

```
    ╱ E2E ╲           少数: ユーザージャーニー検証
   ╱ 統合テスト ╲       多数: コンポーネント間の接続検証
  ╱ ユニットテスト ╲     中程度: ビジネスロジック検証
 ╱  静的解析  ╲         常時: 型チェック, lint
```

| レベル | 比率 | フォーカス |
|--------|------|-----------|
| 静的解析 | 常時 | TypeScript strict, mypy, Go vet |
| ユニット | 中 | 純粋関数、ビジネスロジック |
| 統合 | **多** | API境界、DB操作、サービス連携 |
| E2E | 少 | クリティカルユーザーフロー |

### AAA パターン (Arrange-Act-Assert)

全言語共通の基本構造。各テストで1つの振る舞いのみ検証。

---

## 2. 言語別テストパターン比較

### TypeScript (Vitest / Jest)

```typescript
describe("UserService", () => {
    it("should create user with valid email", async () => {
        // Arrange
        const repo = { save: vi.fn().mockResolvedValue({ id: "1" }) };
        const service = new UserService(repo);

        // Act
        const result = await service.create({ email: "a@b.com" });

        // Assert
        expect(result.isOk()).toBe(true);
        expect(repo.save).toHaveBeenCalledOnce();
    });
});
```

### Go (testing)

```go
func TestUserService_Create(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid", "a@b.com", false},
        {"invalid", "invalid", true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            svc := NewUserService(&mockRepo{})
            _, err := svc.Create(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("wantErr=%v, got %v", tt.wantErr, err)
            }
        })
    }
}
```

### Python (pytest)

```python
class TestUserService:
    def test_create_with_valid_email(self, mock_repo):
        service = UserService(repo=mock_repo)
        result = service.create(email="a@b.com")
        assert result.id is not None
        mock_repo.save.assert_called_once()
```

---

## 3. モック戦略

### 原則

| 原則 | 説明 |
|------|------|
| インターフェースでモック | 具象クラスではなくインターフェースをモック |
| 自分のものだけモック | 外部ライブラリは薄いラッパー経由 |
| 実装ではなく振る舞いをテスト | メソッド呼び出し順序ではなく結果を検証 |

### 言語別モック比較

| 言語 | ツール | 特徴 |
|------|--------|------|
| TypeScript | vi.fn() / jest.fn() | 柔軟、型推論あり |
| Go | 手動モック (インターフェース実装) | 外部依存なし、明示的 |
| Python | unittest.mock + autospec | `autospec=True` でシグネチャ検証 |

### アンチパターン

```typescript
// BAD: 実装詳細をテスト
expect(service.internalMethod).toHaveBeenCalled();

// GOOD: 外部から見える振る舞いをテスト
expect(result).toEqual(expectedOutput);
```

---

## 4. プロパティベーステスト

入力値をランダム生成し、プロパティ（不変条件）が成立するか検証。

### 言語別ツール

| 言語 | ツール | 例 |
|------|--------|-----|
| TypeScript | fast-check | `fc.assert(fc.property(fc.array(fc.integer()), ...))` |
| Go | testing/quick, gopter | `quick.Check(func(xs []int) bool { ... })` |
| Python | hypothesis | `@given(st.lists(st.integers()))` |

### 検証すべきプロパティ

| プロパティ | 例 |
|-----------|-----|
| ラウンドトリップ | `decode(encode(x)) == x` |
| 冪等性 | `f(f(x)) == f(x)` |
| 要素保存 | `Counter(sort(x)) == Counter(x)` |
| 不変条件 | `0 <= normalize(x) <= 1` |

---

## 5. 統合テスト パターン

### テストコンテナ (推奨)

本物のDB/サービスを Docker コンテナで起動してテスト。

```typescript
// TypeScript (testcontainers)
const container = await new PostgreSqlContainer().start();
const db = new PrismaClient({ datasources: { db: { url: container.getConnectionUri() } } });
```

```python
# Python (testcontainers-python)
with PostgresContainer("postgres:16") as pg:
    engine = create_engine(pg.get_connection_url())
```

```go
// Go (testcontainers-go)
container, _ := postgres.Run(ctx, "postgres:16")
connStr, _ := container.ConnectionString(ctx)
```

### API テスト

| 言語 | ツール |
|------|--------|
| TypeScript | supertest + Express/Fastify |
| Go | httptest.NewServer |
| Python | httpx.AsyncClient + ASGI/WSGI |

---

## 6. テスト品質指標

| 指標 | 目標 | 説明 |
|------|------|------|
| カバレッジ | 80%+ | 行カバレッジよりブランチカバレッジ重視 |
| ミューテーション | 70%+ | テストの「殺傷力」を測定 |
| フレーキー率 | < 1% | 不安定テストは即修正 or 隔離 |
| 実行速度 | ユニット < 1s | 遅いテストは `@slow` でマーク |

---

## 7. テストアンチパターン

| # | パターン | 問題 | 修正 |
|---|---------|------|------|
| 1 | テスト間の依存 | 実行順序で結果が変わる | 各テスト独立 (共有状態なし) |
| 2 | 実装詳細のテスト | リファクタでテスト壊れる | 振る舞いをテスト |
| 3 | 過度なモック | テストが実装と乖離 | 統合テストで補完 |
| 4 | フレームワーク機能のテスト | ORM/ルーター自体をテスト | ビジネスロジックに集中 |
| 5 | スナップショット乱用 | 大きなスナップショットで変更が見えない | 小さく焦点を絞った assertion |
| 6 | テストでの `sleep` | CI で不安定、実行時間増大 | イベント/ポーリングで待機 |

**Source:** [Testing Trophy (Kent C. Dodds)](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications) · [Go Testing Excellence](https://dasroot.net/posts/2026/01/go-testing-excellence-table-driven-tests-mocking/) · [Python Testing 2025](https://danielsarney.com/blog/python-testing-best-practices-2025-building-reliable-applications/) · [Property-Based Testing (Hypothesis)](https://semaphore.io/blog/property-based-testing-python-hypothesis-pytest)
