# Go (Golang) Best Practices

> Go 1.22-1.24 新機能、エラーハンドリング、並行処理、プロジェクト構造、DI、テスト、slog、アンチパターン

## 1. Go 1.22-1.24 新機能

### Go 1.22: 強化されたルーティング & range over int

```go
// net/http.ServeMux がメソッド+ワイルドカードをサポート
mux := http.NewServeMux()
mux.HandleFunc("GET /users/{id}", getUser)
mux.HandleFunc("POST /users", createUser)
mux.HandleFunc("GET /files/{path...}", serveFile)

func getUser(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
}

// range over int
for i := range 10 {
    fmt.Println(i) // 0..9
}
```

ループ変数スコープ修正: 各イテレーションで独立した変数（クロージャバグ解消）。

### Go 1.23: Range Over Functions (イテレータ)

```go
func Backward[E any](s []E) func(func(int, E) bool) {
    return func(yield func(int, E) bool) {
        for i := len(s) - 1; i >= 0; i-- {
            if !yield(i, s[i]) { return }
        }
    }
}

for i, v := range Backward(s) { fmt.Println(i, v) }
```

標準ライブラリ: `iter.Seq[V]`, `iter.Seq2[K, V]`。

### Go 1.24: ジェネリック型エイリアス & ツール管理

```go
type Set[T comparable] = map[T]struct{}  // ジェネリック型エイリアス
```

```
// go.mod での tool ディレクティブ (tools.go ハック不要)
tool (
    golang.org/x/tools/cmd/stringer
    github.com/sqlc-dev/sqlc/cmd/sqlc
)
```

`os.Root` (パストラバーサル防止)、`testing.B.Loop()` (ベンチ簡略化)、Swiss Tables map (2-3% CPU削減)。

---

## 2. エラーハンドリング

```go
// センチネルエラー
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
)

// %w でラップ (チェーン保持)
func GetUser(id string) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, fmt.Errorf("GetUser(%s): %w", id, err)
    }
    return user, nil
}

// 検査
if errors.Is(err, ErrNotFound) { /* 404 */ }
var validErr *ValidationError
if errors.As(err, &validErr) { /* バリデーション固有処理 */ }
```

| 原則 | 説明 |
|------|------|
| メッセージは「何が期待され何が起きたか」 | `"connecting to %s:%d: %w"` |
| panic は初期化失敗のみ | 通常は error を返す |
| errgroup で並行エラー集約 | `g, ctx := errgroup.WithContext(ctx)` |

---

## 3. 並行処理パターン

| パターン | 用途 |
|---------|------|
| Worker Pool | 固定数ワーカーでタスク並列処理 |
| Fan-Out/Fan-In | 分散処理→結果集約 |
| Pipeline | ステージ間をチャネルで接続 |
| Semaphore | `sem := make(chan struct{}, N)` で並行度制限 |

### 構造化並行性 (errgroup + セマフォ)

```go
func processItems(ctx context.Context, items []Item) error {
    g, ctx := errgroup.WithContext(ctx)
    sem := make(chan struct{}, 10)
    for _, item := range items {
        item := item
        g.Go(func() error {
            sem <- struct{}{}
            defer func() { <-sem }()
            return processItem(ctx, item)
        })
    }
    return g.Wait()
}
```

**チャネル方向性**: `chan<-` (送信専用), `<-chan` (受信専用) を明示。

---

## 4. プロジェクト構造

### 機能ベース構成 (推奨)

```
myproject/
├── cmd/api/main.go          # エントリポイント (最小限)
├── internal/                 # プライベートパッケージ
│   ├── user/                 # 機能ベース (handler/service/repo)
│   └── product/
├── pkg/                      # 外部公開ライブラリ (不要なら省略)
├── api/                      # OpenAPI/Protobuf 定義
└── go.mod
```

### ヘキサゴナル構成

```
internal/
├── domain/       # エンティティ + ポート (インターフェース)
├── application/  # ユースケース
└── adapter/      # http/ postgres/ redis/
```

| 原則 | 説明 |
|------|------|
| `main.go` は最小限 | 組み立て・設定・起動のみ |
| `internal/` 積極活用 | 外部インポート防止 |
| `utils` `helpers` 禁止 | 具体的なパッケージ名を使う |
| フラットな階層 | 過度なネスト回避 |

---

## 5. 依存性注入

### コンストラクタインジェクション (推奨)

```go
type UserService struct {
    repo   UserRepository  // インターフェース
    logger *slog.Logger
}

func NewUserService(repo UserRepository, logger *slog.Logger) *UserService {
    return &UserService{repo: repo, logger: logger}
}
```

### Functional Options

```go
type Option func(*Server)

func WithTimeout(d time.Duration) Option {
    return func(s *Server) { s.timeout = d }
}

func NewServer(addr string, opts ...Option) *Server {
    s := &Server{addr: addr, timeout: 30 * time.Second}
    for _, opt := range opts { opt(s) }
    return s
}
```

| 規模 | 推奨 |
|------|------|
| 小〜中 | 手動コンストラクタ + Functional Options |
| 大規模 | Wire (コンパイル時) or Fx (ランタイム) |

---

## 6. テスト

### テーブル駆動テスト

```go
func TestCalc(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
        wantErr  bool
    }{
        {"add", 2, 3, 5, false},
        {"div_zero", 10, 0, 0, true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            result, err := Calc(tt.a, tt.b)
            if tt.wantErr { assert(t, err != nil); return }
            assert(t, result == tt.expected)
        })
    }
}
```

| コマンド | 用途 |
|---------|------|
| `go test -race ./...` | レースコンディション検出 **(必須)** |
| `go test -coverprofile=c.out` | カバレッジ |
| `go test -bench=. -benchmem` | ベンチマーク |

**モック**: インターフェースベースの手動モック推奨。`t.Helper()` でヘルパー関数を定義。

---

## 7. 構造化ロギング (slog)

```go
// JSON出力 (本番) / Text出力 (開発) を切り替え
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
}))

logger.Info("request completed",
    slog.String("method", r.Method),
    slog.Duration("latency", duration),
    slog.Int("status", code),
)
```

**秘密情報マスク**: `LogValuer` インターフェース or `ReplaceAttr` で REDACTED。

---

## 8. アンチパターン

| # | パターン | 問題 | 修正 |
|---|---------|------|------|
| 1 | Single Model | API/DB/バリデーションが1構造体に混在 | Request/DBModel/Response に分離 |
| 2 | 隠れた Goroutine | 関数内で暗黙的に `go` を起動 | 呼び出し側で非同期制御 |
| 3 | 可変グローバル状態 | パッケージレベル変数 | コンストラクタ注入 |
| 4 | Promiscuous Interface | 汎用的すぎるメソッド | ドメイン固有の小さいインターフェース |
| 5 | 引数の暴走 | 位置引数5個以上 | 構造体でグループ化 |
| 6 | 汎用パッケージ名 | `utils`, `helpers` | 具体的な名前 (`timeformat`) |
| 7 | 不要なポインタ | スライス/マップにポインタ | 参照型はそのまま渡す |
| 8 | 非変数の var | 変更しない値に `var` | `const` を使う |

**Source:** [Go 1.24 Release](https://go.dev/blog/go1.24) · [Go Anti-patterns (hackmysql)](https://hackmysql.com/golang/go-antipatterns/) · [ThreeDots Clean Architecture](https://threedots.tech/post/introducing-clean-architecture/) · [JetBrains 10x Commandments](https://blog.jetbrains.com/go/2025/10/16/the-10x-commandments-of-highly-effective-go/)
