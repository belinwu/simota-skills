# Code Review Effectiveness & Metrics

> レビュー有効性の測定、認知負荷と最適 PR サイズ、KPI 設計、レビュアー疲労の研究

## 1. レビュー有効性のキーメトリクス

### 品質メトリクス

| メトリクス | 説明 | 目標値 |
|-----------|------|--------|
| **Defect Escape Rate** | レビュー通過後に発見されたバグの割合 | < 5% |
| **Review Coverage** | レビューされたコード変更の割合 | > 95% |
| **False Positive Rate** | 誤った指摘の割合 | < 20% |
| **Actionable Finding Rate** | 実際に修正に繋がった指摘の割合 | > 60% |
| **Severity Accuracy** | severity 分類の妥当性 | > 80% |

### 効率メトリクス

| メトリクス | 説明 | 目標値 |
|-----------|------|--------|
| **Review Turnaround Time** | PR 作成からレビュー完了まで | < 24時間 |
| **Time to First Comment** | PR 作成から最初のコメントまで | < 4時間 |
| **Review Iterations** | 承認までのラウンドトリップ回数 | ≤ 2回 |
| **PR Rejection Rate** | リジェクトされた PR の割合 | 10-20% |
| **Lines Reviewed per Hour** | 時間あたりのレビュー行数 | 200-400 LOC |

### プロセスメトリクス

| メトリクス | 説明 | 目標値 |
|-----------|------|--------|
| **PR Size** | 変更行数（追加+削除） | < 400 LOC |
| **Comment Density** | 変更行数あたりのコメント数 | 適切（多すぎず少なすぎず） |
| **Review Participation** | レビューに参加するチームメンバーの割合 | > 80% |
| **Knowledge Distribution** | レビュー担当の分散度 | Gini ≤ 0.4 |

---

## 2. 認知負荷と最適 PR サイズ

### Cisco 研究 + 2025年 LinearB 分析

```
Cisco Study (経年的に確認された知見):
  - 200-400 LOC が最適レビューサイズ
  - 60-90分が1セッションの最適時間
  - 400 LOC/時間を超えるとバグ検出率が急落

LinearB 2025 (610万 PR、3,000チーム分析):
  - エリートチームの平均: 219 LOC/PR
  - この数値は Cisco の最適範囲と一致
```

### 認知負荷の崖（Cognitive Load Cliff）

```
レビュー行数と欠陥検出率の関係:

LOC/hr  | 欠陥検出率 | 状態
--------|-----------|------
< 200   | 高        | 最適ゾーン
200-400 | 中-高     | 推奨範囲
400-450 | 急落開始  | 警告ゾーン
> 450   | 13% のみ  | 87% の欠陥を見逃す

原因: ワーキングメモリが約4チャンク → 認知容量を超過
```

### PR サイズガイドライン

| サイズ | LOC | レビュー深度 | 推奨アクション |
|--------|-----|-----------|------------|
| **Small** | < 100 | 深い | 即座にレビュー |
| **Medium** | 100-400 | 適切 | 標準レビュー |
| **Large** | 400-1000 | 低下開始 | 分割を推奨 |
| **XL** | > 1000 | 形骸化リスク | 分割を強制 |

---

## 3. レビュアー疲労の研究

### 疲労の原因と影響

| 原因 | 影響 | 研究知見 |
|------|------|---------|
| **決定疲労** | 後半の判断品質低下 | 短い/大きい/複雑な変更をスキップ |
| **コンテキストスイッチ** | 集中力の断片化 | レビュー効率 30% 低下 |
| **レビュー不安** | 批判への恐れ/プレッシャー | Springer 2024 研究で実証 |
| **大量 PR 負荷** | バーンアウト | Heroing パターンの原因 |

### 疲労緩和策

```
Judge による緩和:
  1. 自動レビューで基本チェックを肩代わり
     → 人間は高次判断に集中
  2. severity 分類で優先順位を明確化
     → 「全部見る」必要がない
  3. false positive フィルタリング
     → ノイズ削減でレビュー負荷軽減
  4. PR サマリ自動生成
     → コンテキスト理解の加速

組織的緩和:
  1. レビューローテーションの導入
  2. 1セッション 60分以内の制限
  3. 小さな PR の文化を醸成
  4. レビュー負荷の可視化とバランシング
```

---

## 4. DX Core 4 フレームワーク

### 統合的な開発者生産性測定

```
DX Core 4 = DORA + SPACE + DevEx の統合

4つの軸:
  Speed      — デプロイ頻度、リードタイム
  Effectiveness — 開発者体験、フロー状態
  Quality    — 変更失敗率、欠陥密度
  Impact     — ビジネスアウトカム

コードレビューは Quality と Effectiveness の交差点:
  - 品質ゲートとしての機能（Quality）
  - 開発者フローを阻害しない設計（Effectiveness）
```

---

## 5. Judge のメトリクス適用

### 自動計測可能なメトリクス

```
Judge が自動計測できるもの:
  □ PR サイズ（LOC）→ 大きい PR に警告
  □ 指摘数と severity 分布
  □ false positive 推定率（パターンベース）
  □ intent alignment スコア
  □ consistency issue 数
  □ test quality スコア

Judge が計測できないもの（組織レベル）:
  × レビューターンアラウンドタイム
  × defect escape rate
  × レビュー参加率
  × 修正反映率
```

### PR サイズ警告ルール

```
Judge レポートでの PR サイズ警告:

if (totalLOC > 1000):
  ⚠️ "PR が 1000 LOC を超えています。
      レビュー品質が著しく低下する可能性があります。
      分割を強く推奨します。"

elif (totalLOC > 400):
  ℹ️ "PR が 400 LOC を超えています。
      レビュアーの認知負荷に配慮し、
      可能であれば分割を検討してください。"
```

**Source:** [PropelCode: Measuring Code Review Effectiveness](https://www.propelcode.ai/learn/measuring-code-review-effectiveness) · [Rishi Baldawa: Cognitive Load Cliff in Code Review](https://rishi.baldawa.com/posts/pr-throughput/cognitive-load-cliff/) · [Arxiv: Rethinking Code Review Workflows with LLM](https://arxiv.org/html/2505.16339v1) · [Springer: Code Review Anxiety](https://link.springer.com/article/10.1007/s10664-024-10550-9) · [Qodo: Code Quality Metrics 2026](https://www.qodo.ai/blog/code-quality-metrics-2026/)
