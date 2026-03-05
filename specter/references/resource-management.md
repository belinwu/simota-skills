# Resource Management Patterns

> リソースリーク防止、接続プール管理、コードレビューチェックリスト、言語別パターン

## 1. リソースリークの 5 カテゴリ

| カテゴリ | OS 上限 | 枯渇時の影響 | 検出難易度 |
|---------|--------|------------|----------|
| **Memory** | プロセスメモリ上限 | OOM Kill、クラッシュ | 中（ヒープ分析で可視化） |
| **File Handle** | 1,024〜65,536/プロセス | EMFILE エラー、ファイル操作不可 | 高（`lsof` で確認可能） |
| **DB Connection** | プールサイズ依存 | タイムアウト、カスケード障害 | 中（プール統計で監視） |
| **Network Socket** | ~65,535/ホスト | 接続不可、タイムアウト | 高（netstat/ss で確認） |
| **Thread/Worker** | プールサイズ依存 | 新タスク処理不可 | 中（プール統計で監視） |

---

## 2. 言語別リソース管理パターン

### JavaScript/TypeScript

```typescript
// Symbol.dispose (TC39 Stage 3 — Explicit Resource Management)
// TypeScript 5.2+ で使用可能
class DatabaseConnection {
  [Symbol.dispose]() {
    this.close();
  }
}

// using 宣言（提案中）
{
  using conn = new DatabaseConnection();
  // スコープ終了時に自動 dispose
}

// 現在の推奨パターン: try-finally
async function query() {
  const conn = await pool.getConnection();
  try {
    return await conn.query('SELECT ...');
  } finally {
    conn.release();  // 必ず実行
  }
}
```

### Python

```python
# Context Manager（推奨）
with open('file.txt') as f:
    data = f.read()
# 自動 close

# async Context Manager
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.json()
```

### Go

```go
// defer（推奨）
func query() error {
    conn, err := pool.Get()
    if err != nil { return err }
    defer conn.Close()  // 必ず実行
    // ...
}
```

---

## 3. 接続プール管理

### 設定パラメータ

| パラメータ | 推奨値 | 説明 |
|-----------|--------|------|
| **maxConnections** | 10-50（用途依存） | 最大接続数 |
| **minConnections** | 2-5 | 最小接続数（ウォームアップ） |
| **acquireTimeout** | 5000-30000ms | 接続取得タイムアウト |
| **idleTimeout** | 30000-600000ms | アイドル接続の解放時間 |
| **leakDetectionThreshold** | 2000-5000ms | リーク検出閾値 |
| **maxLifetime** | 1800000ms (30min) | 接続の最大寿命 |

### リーク検出メカニズム

```
HikariCP 型のリーク検出:
  1. 接続取得時にタイムスタンプを記録
  2. leakDetectionThreshold 超過で警告ログ
  3. スタックトレースを出力（どこで取得されたか）

Node.js (knex/pg-pool):
  pool.on('acquire', () => { /* 取得追跡 */ });
  pool.on('release', () => { /* 解放追跡 */ });

  リーク検出:
    - acquire から release までの時間を監視
    - 閾値超過で警告
    - pool.numUsed() を定期監視
```

### 接続プール枯渇のカスケード

```
枯渇シナリオ:
  1. リクエスト A が接続を取得、解放しない（コードバグ）
  2. 接続プールが徐々に枯渇
  3. 新しいリクエストが acquireTimeout で失敗
  4. ヘルスチェックも接続取得に失敗
  5. ロードバランサーがサーバーを unhealthy 判定
  6. トラフィックが残りのサーバーに集中
  7. 残りサーバーも同じバグで枯渇 → 全体障害

実例: DB 接続プール枯渇でグローバルユーザーの 75% に影響
```

---

## 4. コードレビューチェックリスト

### リソース取得・解放

```
□ すべてのリソース取得に対応する解放があるか？
□ 解放は finally / defer / using / with で保証されているか？
□ 早期 return がリソース解放をバイパスしていないか？
□ 例外パスでリソース解放が行われるか？
□ ループ内でリソースを取得し、ループ外で解放しているか？
```

### 接続・ストリーム

```
□ DB 接続にタイムアウトが設定されているか？
□ HTTP クライアントにタイムアウトが設定されているか？
□ WebSocket に reconnect/cleanup ロジックがあるか？
□ Stream が pipe() で接続され、エラーハンドリングがあるか？
□ 一時ファイルが使用後に削除されるか？
```

### イベント・タイマー

```
□ addEventListener に対応する removeEventListener があるか？
□ setInterval に対応する clearInterval があるか？
□ Observable/EventEmitter の subscribe に unsubscribe があるか？
□ React useEffect に cleanup return があるか？
□ AbortController でフェッチがキャンセル可能か？
```

### プール・キャッシュ

```
□ 接続プールの maxConnections が適切か？
□ キャッシュにサイズ上限/TTL があるか？
□ Global コレクションにエビクションポリシーがあるか？
□ WeakMap/WeakRef が適用できる箇所はないか？
```

---

## 5. リソースリークのアンチパターン

| アンチパターン | 症状 | 対策 |
|--------------|------|------|
| **Happy Path Only** | 正常系でのみ解放、例外パスで漏れ | try-finally を必須化 |
| **Early Return Bypass** | return で finally をスキップ | finally は return 後も実行（JS/Java） |
| **Nested Resource** | 外側のリソースのみ解放 | 各リソースを個別に try-finally |
| **Pooled but Unleased** | プールから取得して解放しない | リーク検出閾値の設定 |
| **Fire-and-Forget Close** | close() の Promise を await しない | await で完了を確認 |
| **Conditional Cleanup** | 特定条件でのみクリーンアップ | 無条件クリーンアップ |

---

## 6. 実世界のインシデント

| インシデント | 原因 | 影響 |
|------------|------|------|
| **CVE-2024-21626** | runc のファイルディスクリプタリーク | コンテナエスケープ攻撃 |
| **グローバル DB 障害** | 接続プール枯渇のカスケード | 75% のユーザーに影響 |
| **Google Shakespeare** | 高負荷時のリソースリーク | サービスカスケード障害 |
| **CheckMK ハンドルリーク** | Windows ハンドルの累積 | 複数サーバーで障害 |

**Source:** [Propel: Resource Leak Detection Guide](https://www.propelcode.ai/blog/resource-leak-detection-code-review-comprehensive-guide) · [DZone: DB Connection Leak Detection](https://dzone.com/articles/detecting-and-resolving-database-connection-leaks) · [DoHost: Connection Pool Exhaustion](https://dohost.us/index.php/2025/08/01/troubleshooting-connection-pool-exhaustion/) · [Etleap: Preventing DB Connection Leaks](https://etleap.com/blog/preventing-database-connection-leaks)
