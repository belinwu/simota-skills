# Concurrency & Async Anti-Patterns

> 並行性・非同期処理のアンチパターン、Race Condition 防止、Deadlock 予防

## 1. Promise アンチパターン

### AP-001: Explicit Construction（不要な Promise ラップ）

```
定義: 既に Promise を返す関数を new Promise() で再ラップ
症状: 冗長なコード、エラーの飲み込み
影響: async executor 内のエラーが catch されない

Bad:
  new Promise(async (resolve, reject) => {
    const data = await fetchData();
    resolve(data);
  });

Good:
  async function getData() {
    return await fetchData();
  }

検出: Pattern DL-001 (await inside Promise executor) と連動
```

### AP-002: forEach with Async（非同期 forEach）

```
定義: Array.forEach() 内で async/await を使用
症状: ループが非同期完了を待たない、実行順序が不定
影響: 予期しない並行実行、データ不整合

Bad:
  items.forEach(async (item) => {
    await processItem(item);  // forEach は待たない
  });

Good (Sequential):
  for (const item of items) {
    await processItem(item);
  }

Good (Parallel):
  await Promise.all(items.map(item => processItem(item)));
```

### AP-003: Promise.all() の脆弱なエラー処理

```
定義: Promise.all() で 1 つの reject が全体を失敗させる
症状: 部分的成功の結果が失われる
影響: 再試行不能、ユーザー体験の悪化

Bad:
  const results = await Promise.all([fetchA(), fetchB(), fetchC()]);
  // 1 つでも失敗すると全結果が失われる

Good:
  const results = await Promise.allSettled([fetchA(), fetchB(), fetchC()]);
  const successes = results.filter(r => r.status === 'fulfilled');
  const failures = results.filter(r => r.status === 'rejected');
```

### AP-004: return vs await in try-catch

```
定義: try-catch 内で await なしで Promise を return
症状: reject された Promise が catch されない
影響: エラーハンドリングのバイパス

Bad:
  async function getData() {
    try {
      return fetchData();  // reject は catch されない
    } catch (e) {
      handleError(e);  // 到達しない
    }
  }

Good:
  async function getData() {
    try {
      return await fetchData();  // reject は catch される
    } catch (e) {
      handleError(e);
    }
  }
```

### AP-005: await in Loop（ループ内 await）

```
定義: ループ内で逐次 await して並列化の機会を逃す
症状: N 件の処理が直列実行され、N 倍の時間がかかる
影響: パフォーマンス低下

Bad:
  for (const id of ids) {
    const user = await fetchUser(id);  // 直列
    results.push(user);
  }

Good:
  const results = await Promise.all(
    ids.map(id => fetchUser(id))  // 並列
  );

注意: 意図的な直列実行（レートリミット、依存関係）は除外
```

---

## 2. Race Condition 防止戦略

### 戦略マトリクス

| 戦略 | 適用場面 | 実装 |
|------|---------|------|
| **AbortController** | React/fetch のキャンセル | `signal` で古いリクエストを中断 |
| **Request ID トラッキング** | 最新リクエストのみ適用 | ID 比較で stale データを無視 |
| **Debouncing** | ユーザー入力トリガー | 最後の入力から一定時間後に実行 |
| **Atomic Update** | DB 更新 | `$inc`, `updateOne` with condition |
| **Optimistic Locking** | 競合更新 | version フィールドで CAS |
| **Distributed Lock** | マルチサーバー | Redis/async-mutex でロック |
| **Cancellation Token** | 長時間処理 | トークンで処理中断を通知 |

### React 固有の Race Condition 対策

```
1. useEffect cleanup:
   - let cancelled = false; ... return () => { cancelled = true; }
   - AbortController + signal

2. React Query / SWR:
   - 内部で stale-while-revalidate を管理
   - 自動キャンセル/再フェッチ

3. useTransition (React 18+):
   - 非同期状態更新の競合を防止
   - isPending で UI フィードバック
```

---

## 3. Deadlock 予防

### Coffman の 4 条件

```
Deadlock は以下 4 条件が同時に成立した時に発生:
  1. Mutual Exclusion（相互排他）: リソースを 1 つのプロセスのみが使用
  2. Hold and Wait（保持と待機）: リソース保持中に別リソースを要求
  3. No Preemption（横取り不可）: リソースを強制解放できない
  4. Circular Wait（循環待機）: A→B→C→A の循環依存

予防 = いずれか 1 条件を破る
```

### JavaScript/Node.js での Deadlock パターン

| パターン | 例 | 対策 |
|---------|---|------|
| **Nested async locks** | lockA → await → lockB（別スレッドで逆順） | ロック順序を統一 |
| **Promise chain cycle** | A.then → B.then → A（循環依存） | 依存グラフを可視化 |
| **Connection pool exhaustion** | 全接続使用中に新接続要求 | プールサイズ + タイムアウト設定 |
| **Worker thread deadlock** | メインスレッドが Worker 完了を sync 待ち | 非同期メッセージパッシング |

### Deadlock 予防チェックリスト

```
□ 複数ロックの獲得順序がコードベース全体で統一されているか？
□ ロックにタイムアウトが設定されているか？
□ async-mutex 等のライブラリで安全なロック管理をしているか？
□ Connection pool の maxConnections と acquireTimeout が適切か？
□ Worker thread とメインスレッド間で同期待ちがないか？
```

---

## 4. 並行性安全パターン

### Immutability

```
共有状態を不変にすることで Race Condition を根本的に排除:
  - Object.freeze() / structuredClone()
  - Immer ライブラリ（produce() で安全な更新）
  - Redux/Zustand の状態管理パターン
```

### Actor Model

```
メッセージパッシングで共有状態を排除:
  - Worker Threads + postMessage()
  - BullMQ / Bee-Queue（ジョブキュー）
  - 各 Actor が独自の状態を管理
```

### Semaphore/Mutex

```
並行数を制限:
  - async-mutex: Mutex / Semaphore
  - p-limit: 並列数制限
  - p-queue: 優先度付きキュー
```

**Source:** [DEV: Tackling Async Bugs in JS](https://dev.to/alex_aslam/tackling-asynchronous-bugs-in-javascript-race-conditions-and-unresolved-promises-7jo) · [DEV: Preventing Race Conditions with Distributed Locks](https://dev.to/koistya/preventing-race-conditions-in-nodejs-with-distributed-locks-48fp) · [Medium: Understanding Deadlocks](https://medium.com/@parvjn616/understanding-deadlocks-in-concurrent-programming-799d78ebe7a8) · [Bluebird: Promise Anti-Patterns](http://bluebirdjs.com/docs/anti-patterns.html) · [Medium: 6 Common Pitfalls in Async JS](https://medium.com/codex/6-common-pitfalls-and-anti-patterns-in-asynchronous-javascript-7d8d250a1a64)
