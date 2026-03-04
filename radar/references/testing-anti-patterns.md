# Testing Anti-Patterns & Quality Metrics

> テストのアンチパターン検出、品質メトリクス、テストコード健全性評価

## 1. 13 大テスト・アンチパターン（Codepipes分類）

### Unit Test アンチパターン

| # | パターン | 症状 | 対策 |
|---|---------|------|------|
| 1 | **The Liar** | 常にパスするが何も検証しない | 意味あるアサーション必須（AAA徹底） |
| 2 | **Excessive Setup** | テスト準備が本体より長い | テストデータファクトリ・Builder パターン |
| 3 | **The Giant** | 1テストで複数の振る舞いを検証 | 1テスト1アサーション原則 |
| 4 | **The Mockery** | モックだらけで実際の振る舞いと乖離 | 統合テストとのバランス、Testcontainers |
| 5 | **The Inspector** | 内部実装の詳細をテスト | 振る舞い（入出力）のみ検証 |
| 6 | **Generous Leftovers** | テスト間で状態が共有・残存 | 各テストで独立セットアップ・クリーンアップ |
| 7 | **The Local Hero** | 特定環境でのみパス | CI環境での検証必須、環境依存排除 |
| 8 | **The Nitpicker** | 些細な実装変更でテストが壊れる | スナップショットの過度な使用を避ける |
| 9 | **The Secret Catcher** | エラーケースを明示せず例外で暗黙キャッチ | 期待する例外を明示的にアサート |
| 10 | **The Dodger** | 複雑なロジックを避けて簡単な部分だけテスト | リスクベースでカバレッジ対象を選定 |

### Integration / System Test アンチパターン

| # | パターン | 症状 | 対策 |
|---|---------|------|------|
| 11 | **The Slow Poke** | テストスイートが遅すぎてフィードバック遅延 | 並列実行、テスト選択戦略、軽量フィクスチャ |
| 12 | **Chain Gang** | テスト間の順序依存 | 各テスト完全独立、共有状態の排除 |
| 13 | **The Flickering Test** | 非決定的にパス/フェイル | → `flaky-test-guide.md` 参照 |

---

## 2. テストピラミッド・アンチパターン

### Ice Cream Cone（アイスクリームコーン）

```
    手動テスト ← 最も多い
   ┌──────────┐
   │   E2E    │
   ├──────────┤
   │Integration│
   ├──────────┤
   │  Unit    │ ← 最も少ない
   └──────────┘
問題: 遅い・不安定・メンテナンス高コスト
```

### Hourglass（砂時計）

```
   ┌──────────┐
   │  Unit    │ ← 多い
   ├──────────┤
   │Integration│ ← 極端に少ない
   ├──────────┤
   │   E2E    │ ← 多い
   └──────────┘
問題: 統合部分のギャップ、E2E肥大化
```

### 正しいピラミッド比率

| レイヤー | 割合 | 実行速度 | フィードバック |
|---------|------|---------|-------------|
| Unit | 70% | < 10ms | 即座 |
| Integration | 20% | < 1s | 数秒 |
| E2E | 10% | < 30s | 数分 |

---

## 3. テスト品質メトリクス

### カバレッジを超えるメトリクス

| メトリクス | 測定対象 | 目標 | ツール |
|-----------|---------|------|--------|
| **Line Coverage** | 実行された行 | 80%+ | istanbul, v8, coverage.py |
| **Branch Coverage** | 分岐の網羅 | 70%+ | 同上 |
| **Mutation Score** | テストの検出力 | 60%+（重要コード 80%+） | Stryker, mutmut, cargo-mutants |
| **Test-to-Code Ratio** | テストコード比率 | 1:1 〜 3:1 | LOC 計測 |
| **Assertion Density** | テストあたりアサーション数 | 1-3 | 静的分析 |
| **Test Execution Time** | スイート実行時間 | < 5min（Unit）| CI計測 |
| **Flaky Rate** | 非決定テスト率 | < 1% | CI統計 |
| **MTTR (Mean Time To Repair)** | テスト失敗→修復時間 | < 1h | CI計測 |

### Mutation Testing の価値

```
カバレッジ 100% ≠ テスト品質が高い
  例: `return a + b` を `return a - b` に変異
    → テストが失敗しない = テストが不十分（Survived Mutant）

Mutation Score = Killed Mutants / Total Mutants × 100%
```

**実績データ:**
- Google: 変異テストを全社的に導入、コードレビューに統合
- Sentry: 重要な金融ロジックに限定適用
- HCSC: ヘルスケア規制コードの品質保証

### IDE 統合による DX 改善

| ツール | 言語 | 特徴 |
|--------|------|------|
| Stryker Dashboard | JS/TS, C#, Scala | CI統合、差分mutation |
| IntelliJ Pitest | Java | IDE内でmutant表示 |
| cargo-mutants | Rust | 自動mutant生成 |
| mutmut | Python | pytest統合 |

---

## 4. テストコードの匂い（Test Smells）

### 検出チェックリスト

**構造の匂い:**
- [ ] テストメソッド名が `test1`, `test2` など意味不明
- [ ] `beforeEach` が 20行以上（Excessive Setup）
- [ ] テストファイルが 500行以上（分割が必要）
- [ ] 1テストに 5個以上のアサーション（The Giant）

**ロジックの匂い:**
- [ ] `if/else` がテストコード内にある（条件付きテスト）
- [ ] テスト内でループを使用（テスト生成の方が適切）
- [ ] プロダクションコードをテスト内にコピー（DRY違反）
- [ ] Magic Number がテストに散在

**依存の匂い:**
- [ ] モックが 3階層以上ネスト（The Mockery）
- [ ] `Date.now()` や乱数に依存（非決定的）
- [ ] ファイルシステムやネットワークに直接依存
- [ ] テスト実行順序に依存（Chain Gang）

---

## 5. アンチパターン防止テンプレート

### テストレビューチェックリスト

```markdown
## Test Review Checklist

### 構造
- [ ] テスト名が振る舞いを説明している（should_verb_when_condition）
- [ ] AAA（Arrange-Act-Assert）パターンに従っている
- [ ] 1テスト1アサーション（論理的に）
- [ ] セットアップが簡潔（< 10行）

### 品質
- [ ] エッジケースをカバー（境界値、null、空、エラー）
- [ ] 内部実装ではなく振る舞いをテスト
- [ ] テスト失敗時のメッセージが分かりやすい
- [ ] 非決定的要素が排除されている

### メンテナンス
- [ ] テストデータファクトリを使用
- [ ] マジックナンバーに名前が付いている
- [ ] 重複テストコードが抽出されている
- [ ] テストが他のテストに依存しない
```

**Source:** [Codepipes: Software Testing Anti-Patterns](https://blog.codepipes.com/testing/software-testing-antipatterns.html) · [Fowler: Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) · [Google Testing Blog: Mutation Testing](https://testing.googleblog.com/) · [Stryker Mutator: Documentation](https://stryker-mutator.io/)
