# Non-Functional Regression Investigation

Git bisect と専門ツールを組み合わせた非機能リグレッションの調査手法。

## Performance Regression

### Benchmark-Driven Bisect

```bash
# bisect terms で意味的な名前を使用
git bisect start --term-old=fast --term-new=slow

# ベンチマークスクリプトで自動判定
git bisect run ./scripts/perf-bisect.sh
```

### perf-bisect.sh テンプレート

```bash
#!/bin/bash
# Build
npm run build 2>/dev/null || exit 125  # skip if build fails

# Run benchmark
RESULT=$(npm run bench -- --json 2>/dev/null | jq '.results[0].mean')

# Compare against threshold (e.g., 200ms)
THRESHOLD=200
if (( $(echo "$RESULT > $THRESHOLD" | bc -l) )); then
  exit 1  # slow (new/bad)
else
  exit 0  # fast (old/good)
fi
```

### CI/CD Performance Test Integration

- CI パフォーマンステスト結果の履歴グラフから回帰ポイントを特定
- `git log --after="regression-date" --before="regression-date+1d"` で候補コミット絞り込み
- GitHub Actions artifact からベンチマーク結果を取得: `gh run download`

## Memory Regression

### Heap Growth Bisect

```bash
#!/bin/bash
# Memory bisect script
npm run build 2>/dev/null || exit 125

# Run with memory profiling
node --max-old-space-size=512 --expose-gc scripts/memory-test.js

# Check peak RSS
PEAK_RSS=$(cat /tmp/peak-rss.txt)
THRESHOLD=256  # MB

if [ "$PEAK_RSS" -gt "$THRESHOLD" ]; then
  exit 1  # leak (new/bad)
else
  exit 0  # ok (old/good)
fi
```

### Memory Leak Onset Identification

1. Specter が検出したリーク箇所の blame で最終変更者を特定
2. bisect でリーク開始コミットを特定
3. コミット前後の heap snapshot 比較

## Bundle Size Regression

### Bundle Size Bisect

```bash
#!/bin/bash
npm run build 2>/dev/null || exit 125
SIZE=$(stat -f%z dist/bundle.js 2>/dev/null || stat -c%s dist/bundle.js)
THRESHOLD=500000  # 500KB
[ "$SIZE" -gt "$THRESHOLD" ] && exit 1 || exit 0
```

## Startup Time Regression

- Cold start / warm start の区別
- Container 環境: `time docker run --rm app` の wall time 測定
- Node.js: `--prof` + `--prof-process` でボトルネックモジュール特定
- Python: `python -X importtime` でインポート時間プロファイリング

## Specter Escalation Criteria

bisect 結果が以下に該当する場合、`REWIND_TO_SPECTER_HANDOFF` (`_common/INVESTIGATION_ESCALATION.md`):

- 並行性制御の変更（lock, mutex, semaphore, channel）
- リソース管理の変更（connection pool, file handle, socket）
- 非同期処理パターンの変更（Promise chain, async/await, event listener）
- メモリ管理の変更（cache, buffer, stream）
