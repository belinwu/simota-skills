# Memory Leak Diagnosis

> メモリリークの診断ツール、ワークフロー、ヒープ分析、予防戦略

## 1. 診断ワークフロー

```
Step 1: 症状の確認
  → プロセスメモリの時系列推移を監視
  → GC 後もメモリが減少しない = リーク疑い

Step 2: ヒープスナップショット取得
  → 通常状態（ベースライン）でスナップショット 1
  → 疑わしい操作を繰り返す
  → スナップショット 2 を取得

Step 3: 差分分析
  → Comparison ビューで Delta 列を確認
  → Shallow Size / Retained Size でソート
  → 増加したオブジェクトの Retainers を追跡

Step 4: 根本原因の特定
  → Retainers パネルで参照チェーンを遡る
  → GC Root からの参照パスを確認
  → リーク元のコードを特定

Step 5: 修正 & 検証
  → Builder に修正を委譲
  → 修正後に同じワークフローでスナップショット比較
  → メモリ増加が解消されたことを確認
```

---

## 2. ツール別ガイド

### Node.js 内蔵ツール

| ツール | 用途 | コマンド/使い方 |
|-------|------|---------------|
| **v8.writeHeapSnapshot()** | ヒープスナップショット取得 (v11.13+) | `require('v8').writeHeapSnapshot()` |
| **--inspect** | Chrome DevTools 接続 | `node --inspect app.js` |
| **--max-old-space-size** | メモリ上限設定 | `node --max-old-space-size=512 app.js` |
| **process.memoryUsage()** | メモリ使用量取得 | `rss`, `heapTotal`, `heapUsed`, `external` |

### npm パッケージ

| パッケージ | 用途 | 特徴 |
|-----------|------|------|
| **heapdump** | ヒープスナップショット | SIGUSR2 でトリガー、Chrome DevTools で分析 |
| **memwatch-next** | リーク検出 | `leak` イベントで自動検出、`stats` イベントで GC 統計 |
| **clinic.js** | 総合診断 | Doctor（全般）/ Bubbleprof（async）/ Flame（CPU） |
| **prom-client** | メトリクス公開 | Prometheus 統合、`nodejs_external_memory_bytes` |
| **why-is-node-running** | プロセス終了阻害検出 | アクティブハンドル/タイマーの一覧 |

### Chrome DevTools Memory パネル

```
Heap Snapshot:
  1. Memory パネル → "Take heap snapshot"
  2. Summary ビュー: Constructor 別のメモリ使用
  3. Comparison ビュー: 2 つのスナップショットの差分
  4. Containment ビュー: オブジェクト参照ツリー
  5. Statistics ビュー: メモリ使用の内訳

Allocation Timeline:
  1. "Record allocation timeline" で操作中のアロケーションを記録
  2. 青バー = 操作終了時もまだ生存しているオブジェクト
  3. リーク候補として詳細を確認

Allocation Sampling:
  1. 軽量なサンプリングプロファイラ
  2. 本番環境に近い状態でも使用可能
  3. 関数別のメモリアロケーション統計
```

---

## 3. リーク源の分類と対策

### ブラウザ/React 固有

| リーク源 | 検出方法 | 対策 |
|---------|---------|------|
| **Event Listener 蓄積** | Chrome DevTools → getEventListeners() | useEffect cleanup で removeEventListener |
| **Detached DOM** | Heap snapshot → "Detached" フィルタ | 参照を null にする、WeakRef を使用 |
| **Closure 捕捉** | Retainers パネルで大オブジェクトの参照追跡 | 必要な値のみを変数にコピー |
| **Timer 未クリア** | why-is-node-running で確認 | clearInterval/clearTimeout in cleanup |
| **State update on unmounted** | React warnings in console | AbortController / cancelled flag |

### Node.js/サーバー固有

| リーク源 | 検出方法 | 対策 |
|---------|---------|------|
| **Global 変数蓄積** | Heap snapshot で global の Retained Size | WeakMap/WeakSet、TTL 付きキャッシュ |
| **Stream 未消費** | process.memoryUsage() 監視 | pipe() 接続、destroy() 呼出し |
| **Module キャッシュ** | require.cache のサイズ監視 | 動的 require の回避 |
| **Buffer 蓄積** | external メモリの増加 | Buffer プール、ストリーミング処理 |
| **非 strict mode の暗黙 global** | ESLint strict mode ルール | "use strict" / ES Modules |

---

## 4. WeakRef / FinalizationRegistry

```
ES2021 で追加された GC フレンドリーな参照:

WeakRef:
  - オブジェクトへの弱い参照（GC を妨げない）
  - キャッシュに最適: GC が必要時に自動回収
  - deref() で参照取得（GC 済みなら undefined）

FinalizationRegistry:
  - オブジェクトが GC された時のコールバック
  - リソースクリーンアップの最終手段
  - 注意: タイミングは保証されない

使い分け:
  ✅ キャッシュ（LRU + WeakRef）
  ✅ Observer パターンの弱い参照
  ❌ 重要なリソースクリーンアップ（タイミング不定）
  ❌ ファイルハンドル/DB 接続の解放（明示的に close すべき）
```

---

## 5. 本番環境でのメモリ監視

### メトリクス

| メトリクス | 警告閾値 | アクション |
|-----------|---------|----------|
| **heapUsed** | 連続 30 分上昇 | ヒープスナップショット取得 |
| **rss** | プロセスメモリ上限の 80% | スケールアウト検討 |
| **external** | ベースラインの 2 倍 | Buffer/native アドオン調査 |
| **GC pause** | > 100ms | GC チューニング |

### PM2 自動再起動

```
PM2 の max_memory_restart:
  - リーク未修正時の一時的な緩和策
  - 根本原因の修正までのつなぎ
  - 例: pm2 start app.js --max-memory-restart 512M
```

**Source:** [Better Stack: Node.js Memory Leaks](https://betterstack.com/community/guides/scaling-nodejs/high-performance-nodejs/nodejs-memory-leaks/) · [Medium: JS Memory Leaks in 2025](https://medium.com/@deval93/javascript-memory-leaks-in-2025-how-to-detect-prevent-and-fix-them-ade013bd8b46) · [Sematext: Node.js Memory Leak Detection](https://sematext.com/blog/nodejs-memory-leaks/) · [Node.js: Memory Diagnostics](https://nodejs.org/en/learn/diagnostics/memory) · [Toptal: Debugging Memory Leaks](https://www.toptal.com/nodejs/debugging-memory-leaks-node-js-applications)
