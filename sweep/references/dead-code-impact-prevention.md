# Dead Code Impact & Prevention

> デッドコードのビジネスインパクト、コスト、予防戦略、メトリクス

## 1. デッドコードのビジネスインパクト

### 数字で見る影響

| 指標 | データ | 出典 |
|------|--------|------|
| **技術的負債の割合** | ICT 企業の技術資産の 20-40% が技術的負債 | Axify |
| **未使用コード率** | コードベースの 20%、最大 66% が未使用 | Axify |
| **JS 未使用関数** | ページの中央値で 70% の JavaScript 関数が未使用 | Axify |
| **ペイロード削減** | 未使用 JS 除去でペイロード 60% 削減 | Axify |
| **AI コードの冗長性** | AI 生成プロジェクトの 41.17% に冗長メソッドペア | Axify |
| **コメントアウト混入** | 初期開発コミットの最大 20% にコメントアウトコード | Axify |
| **不健全コードの欠陥** | 不健全コードは健全コードの 15 倍の欠陥を持つ | CodeScene |

### 実際のインシデント

```
Knight Capital (2012):
  - 8年間放置された旧コードの feature flag が誤って有効化
  - 約 45 分で $440M の損失
  - 教訓: デッドコードは「無害」ではない

Meta SCARF:
  - 5 年間で 1 億行以上のデッドコード削除
  - 37 万件以上の変更リクエストを自動生成
  - グラフレベル分析で約 50% のカバレッジ改善
```

---

## 2. デッドコードの 6 つのリスク

| リスク | 説明 | 影響度 |
|--------|------|--------|
| **セキュリティ脆弱性** | 古い依存関係・未チェック入力が攻撃対象に | 高 |
| **パフォーマンス低下** | ビルド時間増大、バンドルサイズ肥大化 | 中-高 |
| **認知負荷増大** | 開発者のオンボーディング・デバッグ時間増加 | 中 |
| **メンテナンスコスト** | 不要コードのテスト・レビュー・更新コスト | 中 |
| **インフラコスト** | メモリ使用量・ストレージ・CI 時間の浪費 | 低-中 |
| **意図しない再有効化** | Feature flag や設定変更で眠っていたコードが復活 | 高（Knight Capital 型） |

---

## 3. 予防戦略

### 開発プロセスレベル

```
1. YAGNI 原則の徹底
   - 「いつか使うかも」でコードを残さない
   - 必要になった時に version control から復元

2. コメントアウト禁止ポリシー
   - コメントアウトではなく削除 + git history に依存
   - Issue tracker で「後で使う可能性」を管理

3. Feature Flag のライフサイクル管理
   - Flag 導入時に期限（TTL）を設定
   - 期限切れ Flag の自動検出 + 削除提案

4. Small PR 文化
   - 大きな変更 = デッドコード混入リスク
   - 削除コミットと機能コミットの分離
```

### CI/CD レベル

```
1. 自動検出パイプライン
   - knip / vulture / staticcheck を CI に統合
   - PR 単位で新規デッドコード導入を検出

2. カバレッジゲート
   - 0% カバレッジの関数を定期レポート
   - 新規コードのカバレッジ最低ラインを設定

3. Pre-commit Hook
   - 未使用 import の自動除去
   - コメントアウトコードの検出・警告

4. 定期スキャン
   - Sprint-end: フルスキャン + トレンド追跡
   - Quarterly: ディープスキャン + 依存関係監査
```

### コードレビューレベル

```
1. レビューチェックリストに「デッドコード」を含める
2. 「なぜこのコードが必要か」の説明を求める
3. 6 ヶ月以上未変更のコードへの変更は追加レビュー
4. AI 生成コードの冗長性を重点チェック（41% に冗長メソッド）
```

---

## 4. Sweep のメトリクス

### 計測すべき指標

| メトリクス | 説明 | 目標 |
|-----------|------|------|
| **Dead Code Rate** | コードベース中のデッドコード割合 | < 5% |
| **Cleanup Velocity** | Sprint あたりの削除行数 | 安定的な削減トレンド |
| **Detection Accuracy** | True Positive 率 | > 80% |
| **False Positive Rate** | 誤検出率 | < 20% |
| **Time to Cleanup** | 検出から削除までの時間 | < 2 Sprint |
| **Regression Rate** | 削除後のリグレッション発生率 | < 1% |

### ベースライン追跡

```
Sweep の Maintenance Mode で追跡:
  - SCAN_BASELINE に以下を記録:
    □ 総ファイル数 / 未使用ファイル数
    □ 総 export 数 / 未使用 export 数
    □ 総依存関係数 / 未使用依存関係数
    □ 前回スキャンからの増減（トレンド）
```

**Source:** [Axify: Dead Code Guide 2025](https://axify.io/blog/dead-code) · [Meta Engineering: Automating Dead Code Cleanup](https://engineering.fb.com/2023/10/24/data-infrastructure/automating-dead-code-cleanup/) · [CodeScene: Code Health](https://codescene.com/product/code-health) · [vFunction: Dead Code Strategies](https://vfunction.com/blog/dead-code/)
