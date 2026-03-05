# Static Analysis & Detection Tools

> 静的解析ツール、ESLint ルール、ランタイム検出、テスト戦略

## 1. ESLint ルール（非同期コード）

### 必須ルール（Specter 推奨）

| ルール | プラグイン | 検出対象 | 重要度 |
|-------|----------|---------|--------|
| **no-floating-promises** | @typescript-eslint | await/catch なしの Promise | CRITICAL |
| **no-misused-promises** | @typescript-eslint | if 文等への Promise 渡し | HIGH |
| **await-thenable** | @typescript-eslint | 非 Promise 値の await | HIGH |
| **no-async-promise-executor** | ESLint Core | async な Promise executor | HIGH |
| **require-atomic-updates** | ESLint Core | await 後の Race Condition | CRITICAL |
| **no-await-in-loop** | ESLint Core | ループ内の逐次 await | MEDIUM |
| **promise-function-async** | @typescript-eslint | async なし Promise 返却関数 | MEDIUM |

### 推奨ルール

| ルール | プラグイン | 検出対象 | 重要度 |
|-------|----------|---------|--------|
| **no-promise-executor-return** | ESLint Core | executor 内の return | LOW |
| **max-nested-callbacks** | ESLint Core | コールバック地獄 | MEDIUM |
| **prefer-promise-reject-errors** | ESLint Core | Error 以外での reject | LOW |
| **node/no-sync** | eslint-plugin-n | 同期 API の使用 | MEDIUM |
| **node/handle-callback-err** | eslint-plugin-n | エラー引数の無視 | HIGH |

### React 固有ルール

| ルール | プラグイン | 検出対象 |
|-------|----------|---------|
| **react-hooks/exhaustive-deps** | eslint-plugin-react-hooks | useEffect 依存配列の不足 |
| **no-direct-mutation-state** | eslint-plugin-react | State の直接変更 |

### ESLint 設定例

```json
{
  "rules": {
    "@typescript-eslint/no-floating-promises": "error",
    "@typescript-eslint/no-misused-promises": "error",
    "@typescript-eslint/await-thenable": "error",
    "no-async-promise-executor": "error",
    "require-atomic-updates": "error",
    "no-await-in-loop": "warn",
    "max-nested-callbacks": ["warn", 3]
  }
}
```

---

## 2. 静的解析ツール

### JavaScript/TypeScript

| ツール | 検出能力 | 特徴 |
|-------|---------|------|
| **TypeScript Compiler** | 型レベルの非同期エラー | async/await の型安全性 |
| **ESLint + typescript-eslint** | Promise パターン違反 | 上記ルール参照 |
| **SonarQube/SonarCloud** | リソースリーク、複雑度 | CI 統合、品質ゲート |
| **CodeQL** | セキュリティ + 並行性 | GitHub 統合、カスタムクエリ |
| **Semgrep** | カスタムパターン検出 | YAML ルール定義、高速 |

### Python

| ツール | 検出能力 |
|-------|---------|
| **Bandit** | セキュリティ + リソース管理 |
| **PyLint** | リソースリーク、コード品質 |
| **mypy** | 型チェックで async エラー検出 |

### Go

| ツール | 検出能力 |
|-------|---------|
| **go vet** | 並行性バグ、goroutine リーク |
| **golangci-lint** | 複合リンター（staticcheck 含む） |
| **race detector** | `go test -race` でランタイム検出 |

---

## 3. ランタイム検出ツール

### メモリプロファイラ

| ツール | 言語 | 用途 |
|-------|------|------|
| **Chrome DevTools Memory** | JS (Browser) | ヒープスナップショット、アロケーション追跡 |
| **clinic.js** | Node.js | Doctor / Bubbleprof / Flame |
| **memory_profiler** | Python | 行レベルのメモリ使用量 |
| **pprof** | Go | CPU/メモリプロファイリング |

### 並行性デバッガ

| ツール | 用途 |
|-------|------|
| **async-race-detector** | JS Race Condition 検出 |
| **Jaeger/Zipkin** | 分散トレーシングで非同期フロー可視化 |
| **Go race detector** | goroutine Race Condition 検出 |
| **ThreadSanitizer** | C/C++/Go のスレッド安全性 |

### リソースモニタリング

| ツール | 監視対象 |
|-------|---------|
| **lsof** | オープンファイルディスクリプタ |
| **ss / netstat** | ネットワークソケット状態 |
| **PM2 + metrics** | Node.js プロセスメモリ |
| **Prometheus + Grafana** | カスタムメトリクス可視化 |

---

## 4. テスト戦略

### 並行性テスト

| テストタイプ | 目的 | ツール |
|------------|------|--------|
| **Stress Test** | 高負荷での Race Condition | Artillery, k6 |
| **Soak Test** | 長時間実行でのリーク | 長時間実行 + メモリ監視 |
| **Concurrency Test** | 同時アクセスでの競合 | Promise.all で並行リクエスト |
| **Chaos Test** | ランダムな障害注入 | Chaos Monkey, Toxiproxy |

### メモリリークテスト

```
テスト手順:
  1. ベースラインメモリを記録
  2. 疑わしい操作を N 回繰り返す
  3. GC を強制実行（--expose-gc + global.gc()）
  4. メモリ使用量を記録
  5. 増加率が閾値を超えたらリーク確定

自動化例:
  - Jest + process.memoryUsage()
  - ヒープスナップショットの自動比較
  - CI パイプラインでの定期実行
```

### Race Condition テスト

```
テスト手順:
  1. 共有リソースを特定
  2. 複数の同時操作を生成
  3. 結果の一貫性を検証
  4. 100+ 回反復で間欠的問題を検出

例:
  const results = await Promise.all(
    Array(100).fill().map(() => incrementCounter())
  );
  expect(finalCount).toBe(100);  // Race なら < 100
```

---

## 5. Specter との連携

### 静的解析ツールの出力を Specter に入力

```
活用パターン:
  1. ESLint 違反レポート → Specter のスキャン候補
  2. SonarQube の issue → Specter の深掘り分析
  3. CodeQL アラート → Specter のリスクスコアリング

Specter の付加価値:
  - ツールの FP（False Positive）フィルタリング
  - ビジネスコンテキストに基づくリスク評価
  - Bad→Good の修正例提示
  - Radar へのテストケースハンドオフ
```

### CI 統合パイプライン

```yaml
# GitHub Actions 統合例
- name: ESLint Async Check
  run: npx eslint --rule '{"@typescript-eslint/no-floating-promises":"error"}' src/
- name: Memory Leak Test
  run: node --expose-gc tests/memory-leak.test.js
- name: Concurrency Test
  run: npx jest tests/concurrency/ --runInBand
```

**Source:** [Maxim Orlov: 14 Linting Rules for Async JS](https://maximorlov.com/linting-rules-for-asynchronous-code-in-javascript/) · [typescript-eslint: no-floating-promises](https://typescript-eslint.io/rules/no-floating-promises/) · [typescript-eslint: no-misused-promises](https://typescript-eslint.io/rules/no-misused-promises/) · [Propel: Resource Leak Detection](https://www.propelcode.ai/blog/resource-leak-detection-code-review-comprehensive-guide)
