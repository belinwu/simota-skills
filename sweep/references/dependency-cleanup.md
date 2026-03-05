# Dependency Cleanup Best Practices

> 未使用依存関係の検出・安全な削除・ツール別ワークフロー・セキュリティ考慮

## 1. 依存関係クリーンアップの重要性

```
影響:
  - パッケージサイズの削減
  - 脆弱性の攻撃対象面（Attack Surface）縮小
  - バージョンアップデートの負荷軽減
  - ビルド時間の短縮
  - ライセンスリスクの低減
```

---

## 2. ツール別ワークフロー

### JavaScript/TypeScript: knip（推奨）

```bash
# 基本スキャン
npx knip --reporter compact

# 依存関係のみ
npx knip --include dependencies

# モノレポ
npx knip --workspace

# CI 統合（非ゼロ終了コード）
npx knip --reporter codeowners --no-exit-code
```

```
knip の優位性:
  - depcheck + ts-prune + unimported を統合
  - 100+ フレームワーク/ツールプラグイン
  - エントリポイントから依存グラフを構築
  - dependencies + devDependencies 両方を検出
  - 重複 export、未使用クラスメンバーも検出
  - モノレポ対応（ワークスペース）
```

### knip 設定例（knip.json）

```json
{
  "$schema": "https://unpkg.com/knip@latest/schema.json",
  "entry": ["src/index.ts"],
  "project": ["src/**/*.ts"],
  "ignore": ["**/*.test.ts", "**/*.stories.ts"],
  "ignoreDependencies": [
    "husky",
    "@types/*"
  ]
}
```

### JavaScript/TypeScript: depcheck（フォールバック）

```bash
# 基本スキャン
npx depcheck

# JSON 出力
npx depcheck --json

# 特定ディレクトリ除外
npx depcheck --ignores="@types/*,husky"
```

```
depcheck の制限:
  ❌ 動的 import を検出できない場合がある
  ❌ 設定ファイル内での使用を見逃す
  ❌ ビルドツール（webpack plugin 等）を誤検出
  ❌ peer dependencies を「未使用」と報告する問題あり
  ❌ React 関連パッケージの誤検出

対策:
  .depcheckrc で ignoreDependencies を設定
  手動検証を必ず実施
```

### Python: pip-audit + pipreqs

```bash
# 未使用パッケージ検出
pip install pipreqs
pipreqs . --force  # 実際の import から requirements.txt を再生成
diff requirements.txt requirements_new.txt

# セキュリティ監査
pip-audit

# vulture で未使用コード（import 含む）
vulture src/ --min-confidence 80
```

### Go: go mod tidy

```bash
# 未使用依存の自動クリーンアップ
go mod tidy

# 未使用の直接依存を確認
go mod why -m <module>
```

### Rust: cargo udeps

```bash
# 未使用依存検出
cargo +nightly udeps
```

---

## 3. False Positive ガイド（依存関係固有）

| パターン | FP リスク | 理由 | 対策 |
|---------|----------|------|------|
| **ビルドプラグイン** | 高 | コードで直接 import しない | `ignoreDependencies` に追加 |
| **型定義パッケージ** | 高 | `@types/*` は暗黙的に使用 | 型パッケージは除外 |
| **PostCSS/Babel プラグイン** | 高 | 設定ファイルからのみ参照 | 設定ファイルスキャンを有効化 |
| **Peer Dependencies** | 中-高 | ホストパッケージが require | 手動確認 |
| **CLI ツール** | 中 | scripts からのみ呼び出し | package.json scripts を確認 |
| **Polyfill** | 中 | 暗黙的にロード | ブラウザ互換性を確認 |
| **Dev サーバー** | 低-中 | 開発時のみ使用 | devDependencies を確認 |

---

## 4. 安全な削除ワークフロー

```
Step 1: 検出
  → knip --include dependencies を実行
  → 結果リストを取得

Step 2: 分類
  → Confidence Score で分類（cleanup-protocol.md 参照）
  → 依存関係固有の追加チェック:
    □ package.json scripts での使用確認
    □ 設定ファイル（webpack.config, babel.config 等）での参照確認
    □ CI/CD パイプラインでの使用確認
    □ ドキュメントでの言及確認

Step 3: バックアップ
  → ブランチ作成
  → package.json + lockfile のスナップショット

Step 4: 段階的削除
  → 高 Confidence (≥90) から開始
  → 1 パッケージずつ削除 → npm install → テスト
  → バッチ削除は同カテゴリ内のみ

Step 5: 検証
  → npm install / yarn install 成功
  → ビルド成功
  → テスト全パス
  → dev サーバー起動確認

Step 6: ロックファイル確認
  → package-lock.json / yarn.lock の差分確認
  → 間接依存の意図しない削除がないか
```

---

## 5. セキュリティ考慮事項

```
未使用依存がセキュリティリスクになる理由:

1. CVE の攻撃対象面拡大
   - 使っていないパッケージの脆弱性が悪用される可能性
   - npm audit で報告される不要なアラート

2. サプライチェーン攻撃
   - 未使用パッケージのメンテナが乗っ取られた場合
   - 依存数が多いほどリスク増大

3. ライセンスリスク
   - GPL 等のコピレフトライセンスパッケージが混入
   - 使っていなくても法的リスクの可能性

推奨:
  □ npm audit / pip-audit を定期実行
  □ 未使用依存の削除を脆弱性修正と同等に扱う
  □ SBOM（Software Bill of Materials）を定期更新
```

---

## 6. CI 統合パターン

```yaml
# GitHub Actions での knip 統合例
name: Dependency Check
on: [pull_request]
jobs:
  knip:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx knip --include dependencies --no-exit-code
        # --no-exit-code: 警告のみ（ブロックしない）
        # 本番環境では --reporter codeowners を追加
```

**Source:** [Knip: Declutter JS/TS Projects](https://knip.dev/) · [Tim Santeford: Clean Up with Knip](https://www.timsanteford.com/posts/how-to-clean-up-your-codebase-with-knip/) · [depcheck: npm module analysis](https://github.com/depcheck/depcheck) · [Medium: Cleaning Up Unused Dependencies](https://luisrangelc.medium.com/cleaning-up-unused-dependencies-af9654e270ad)
