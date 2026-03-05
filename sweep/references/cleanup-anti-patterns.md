# Cleanup Anti-Patterns

> コードクリーンアップ時に陥りやすいアンチパターンと回避策

## 1. 削除プロセスのアンチパターン

### ANTI-001: Big Bang Cleanup

```
定義: 大量のファイル/コードを一度に削除
症状: 「全部まとめてクリーンアップしよう」で 100+ ファイルを一括削除
影響: リグレッション特定不能、ロールバック困難、レビュー不能

Sweep の対策:
  - Confidence Score ≥ 90 のバッチ削除でも段階的に
  - 1 PR あたりの削除スコープを制限
  - カテゴリ別に分割（依存関係 / ファイル / エクスポート）
```

### ANTI-002: Blind Trust in Tools

```
定義: ツールの出力を検証せずそのまま削除
症状: 「knip が未使用って言ってるから削除」
影響: 動的参照、フレームワーク規約ファイルの誤削除

Sweep の対策:
  - Tool Agreement は Confidence Score の 20% に過ぎない
  - 2+ ツールの合意を推奨
  - false-positives.md のガードを必ず適用
  - 特にフレームワーク規約ファイル（pages/, app/ 等）は要注意
```

### ANTI-003: No Backup Deletion

```
定義: バックアップブランチなしに削除を実行
症状: 「git revert すればいいでしょ」
影響: ロックファイルの不整合、複雑な revert

Sweep の対策:
  - 必ず backup ブランチを作成
  - package.json + lockfile のスナップショット
  - 「Always: Create backup branch before deletions」は絶対境界
```

### ANTI-004: Cleanup Without Tests

```
定義: テスト実行せずに削除を完了
症状: 「未使用コードだからテスト不要でしょ」
影響: 間接的な依存の破壊、ビルド失敗

Sweep の対策:
  - VERIFY ステップ必須: テスト全パス + ビルド OK
  - 削除前後で同一テストスイートを実行
  - CI パイプラインでの自動検証
```

---

## 2. 判断ミスのアンチパターン

### ANTI-005: Age-Based Deletion

```
定義: ファイルの古さだけを基準に削除判断
症状: 「1 年以上触ってないから要らない」
影響: 安定したユーティリティ、ライブラリコードの誤削除

Sweep の対策:
  - File Age は Confidence Score の 20% に過ぎない
  - 「Never: Delete based solely on age」は絶対境界
  - Reference Count (30%) を最重要指標とする
  - 安定コード = 触らなくていいコード（デッドではない）
```

### ANTI-006: Comment-Out Instead of Delete

```
定義: コードを削除せずコメントアウトで「無効化」
症状: 「後で使うかもしれないからコメントアウトしておく」
影響: デッドコード増殖、混乱の原因、認知負荷増大

Sweep の対策:
  - コメントアウトコードの検出を cleanup-targets に含む
  - git history に依存し、コメントアウトは削除を推奨
  - Issue tracker で「後で使う可能性」を管理
```

### ANTI-007: Ignoring Dynamic References

```
定義: 静的解析結果のみで削除判断
症状: 「import に出てこないから使ってない」
影響: 動的 import、eval、リフレクションによる参照の見落とし

Sweep の対策:
  - false-positives.md の Dynamic import() ガード
  - 文字列リテラルスキャン（grep ベース）
  - 特に以下を重点チェック:
    □ require() with variable
    □ import() with variable
    □ eval / new Function
    □ Object[key] アクセス
    □ フレームワークのプラグイン/ルート自動ロード
```

### ANTI-008: Deleting Config Orphans Blindly

```
定義: 設定ファイルを「ツールが使われていない」だけで削除
症状: 「.eslintrc は ESLint 使ってないから削除」
影響: CI/CD パイプライン、pre-commit hook、外部ツール連携の破壊

Sweep の対策:
  - Config Remnants は cleanup-targets の独立カテゴリ
  - 設定ファイル → 対応ツール → 使用箇所のフル検証
  - CI 設定、pre-commit hook、IDE 設定も確認
  - 「Ask first: Config files」は必須
```

---

## 3. 組織レベルのアンチパターン

### ANTI-009: Cleanup as One-Off Project

```
定義: クリーンアップを一度きりの大プロジェクトとして実施
症状: 「来月のクリーンアップスプリントで全部やる」
影響: 効果が持続しない、デッドコードの再蓄積

Sweep の対策:
  - Maintenance Mode で継続的なスキャン
  - Per-PR / Sprint-end / Quarterly の 3 層スキャン
  - ベースライントラッキングでトレンド監視
  - Boy Scout Rule: 触ったコードの周辺をきれいに
```

### ANTI-010: No Ownership for Cleanup

```
定義: クリーンアップの責任者・オーナーが不明確
症状: 「誰かがやるだろう」で放置
影響: デッドコードが蓄積し続ける

Sweep の対策:
  - CODEOWNERS に基づく削除提案のルーティング
  - Guardian → Sweep の PR クリーンアップ連携
  - Sprint retrospective でクリーンアップメトリクスを共有
```

---

## 4. チェックリスト: 安全な削除前の確認

```
□ Confidence Score は 50 以上か？
□ 2 つ以上のツール/手法で未使用を確認したか？
□ 動的参照の可能性をチェックしたか？
□ フレームワーク規約ファイルではないか？
□ CI/CD パイプラインで使用されていないか？
□ 設定ファイルから参照されていないか？
□ 最近（30 日以内）変更されていないか？
□ バックアップブランチを作成したか？
□ 削除後のテスト計画はあるか？
□ 影響を受けるドキュメントの更新計画はあるか？
```

---

## 5. Zombie Code の特別扱い

```
最も危険なデッドコード = Zombie Code:
  定義: 実行パスは存在するが本番では決して通らないコード
  例: Feature flag で無効化されたブランチ
  危険性: 設定変更で「復活」する（Knight Capital 型）

検出:
  - Coverage レポートで 0% の実行パスを特定
  - Feature flag の TTL 管理と連携
  - 動的解析（プロファイリング）で本番トラフィックを確認

Sweep の対応:
  - 通常のデッドコードより高い severity で報告
  - Feature flag の期限切れを検出トリガーに追加
  - confidence scoring に「Zombie Risk」を考慮
```

**Source:** [Axify: Dead Code Guide 2025](https://axify.io/blog/dead-code) · [vFunction: Dead Code Strategies](https://vfunction.com/blog/dead-code/) · [understandlegacycode.com: Delete Unused Code](https://understandlegacycode.com/blog/delete-unused-code/) · [Meta Engineering: SCARF](https://engineering.fb.com/2023/10/24/data-infrastructure/automating-dead-code-cleanup/) · [claudecn.com: Safe Dead Code Cleanup](https://claudecn.com/en/docs/claude-code/workflows/refactor-clean/)
