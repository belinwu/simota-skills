# Modern RCA Methodology

> Contributing Factors 分析、エビデンス駆動型 RCA、因果グラフ、ポストインシデントレビュー

## 1. 「Root Cause」から「Contributing Factors」へ

### パラダイムシフト

従来の5 Whys やフィッシュボーン図は「障害には単一の特定可能な原因がある」という前提に基づく。複雑なシステムではこの前提は成り立たない。

| 従来の用語 | 現代の用語 |
|-----------|-----------|
| Root Cause | Contributing Factors |
| Human Error | Systemic Conditions |
| Failure | Unexpected Behavior |
| Blame | Learning Opportunity |

**実践**: 15個の contributing factors を発見しても、重要な3-4個に対処すれば良い。

### 5 Whys の限界と拡張

| 限界 | 対策 |
|------|------|
| 単一の因果連鎖に限定 | 複数の because 分岐を許容 |
| エビデンスなしの推測 | 各 Why にエビデンスリンクを紐付け |
| 人為的ミスで止まりがち | 「なぜそれが合理的に見えたか」を問う |
| Breadth を無視 | **Breadth Before Depth** — 深堀りの前に全候補を列挙 |

---

## 2. エビデンス駆動型 RCA

### 6段階プロセス（OpenTelemetry ベース）

| Step | Action | エビデンスソース |
|------|--------|---------------|
| 1. 検出・定量化 | メトリクスで影響の深刻度を測定 | ダッシュボード、アラート |
| 2. リクエストパス追跡 | 分散トレースで障害箇所を特定 | Trace ID、Span |
| 3. シグナル間相関 | トレース・メトリクス・ログを時系列で結合 | 統合 Observability |
| 4. 変更の特定 | インシデント前の変更を発見 | デプロイ履歴、Feature Flag |
| 5. 原因の確認 | 証拠に対して理論を検証 | ログ、再現テスト |
| 6. 文書化・予防 | モニタリングと予防策を策定 | RCA レポート |

### 「共通祖先」分析

エラートレースの **50%以上** に出現するサービスオペレーションを特定し、優先的に調査。

### 変更インテリジェンス

デプロイ、設定変更、フラグ切り替え、マイグレーションをタイムスタンプとオーナーシップ付きでインデックス化。エラー発生 **10分以内** の変更を高信頼度で検出。

---

## 3. 因果グラフ探索

サービス間の信号を因果要因としてマッピングし、トリガーから影響までの因果関係を可視化。

```
[Config Change] ──→ [Service A Timeout] ──→ [Service B Error Rate ↑]
                                          ──→ [Service C Queue Backlog]
                                                   ──→ [User-facing Error]
```

**検証方法**: 再現、トラフィックリプレイ、ロールバックによる仮説検証。

---

## 4. AI 支援型 RCA

### 4つの AI 能力

| 能力 | 説明 |
|------|------|
| トポロジー対応相関 | 依存関係グラフが上流原因と下流影響を強調 |
| 変更インテリジェンス | エラー発生前のデプロイを自動検出 |
| 因果グラフ探索 | サービス間の因果要因マッピング |
| 自動ガードレール | RCA 結果をアドミッションチェック・カナリアポリシーに変換 |

### Scout での活用

- Multi-Engine Mode で複数 AI に独立した仮説を生成させる（既存機能）
- AI の因果推論を **エビデンスで検証** する（「Automation proposes, humans decide」）
- AI のハルシネーションリスク: サイレントな論理エラーが最も危険（Simon Willison 2025）

---

## 5. ポストインシデントレビュー

### 用語の変化

「Postmortem」→「Incident Review」「Learning Review」への移行（暗い医療連想の排除）。

### 8段階プロセス（Pragmatic Engineer）

1. 障害検出
2. オンコールエンジニアによるインシデント宣言
3. 緩和措置の実施
4. インシデント解決
5. **デコンプレッション期間（36-48時間）** — 分析前のクールダウン
6. 分析 / 根本原因調査
7. レビューミーティング
8. アクションアイテムの追跡

### Blameless の質問テクニック

| Blame ベース | システム思考 |
|------------|------------|
| 「なぜ警告を忘れたのか?」 | 「通知が見過ごされたプロセスの隙間は何か?」 |
| 「誰が SLA を逃したのか?」 | 「アラートのタイミングをどう改善できるか?」 |

**変革的な質問:**
- 「このインシデントで何が驚きましたか?」
- 「システムへの理解はどこで誤っていましたか?」
- 「その行動が当時合理的に見えたのはなぜですか?」

### 学習 vs アクションアイテム

| 従来のアプローチ | 現代のアプローチ |
|---------------|---------------|
| アクションアイテム生成が目的 | 学習の抽出が目的 |
| テンプレートに依存 | 柔軟な学習プロセス |
| 「二度と起きない」を期待 | 「aha moments」を重視 |
| ドキュメントのみ | シミュレーション訓練 |

### Scout への示唆

- REPORT フェーズで contributing factors を構造化して記録
- エビデンスリンク（ログ行、トレースセグメント、設定 diff）を必ず含める
- Builder への修正仕様にシステム的な改善提案も含める

**Source:** [Beyond Root Cause - Resilium Labs](https://www.resiliumlabs.com/blog/beyond-root-cause-analysis) · [OpenTelemetry RCA - OneUpTime](https://oneuptime.com/blog/post/2026-02-06-root-cause-analysis-opentelemetry/view) · [Postmortem Best Practices - Pragmatic Engineer](https://blog.pragmaticengineer.com/postmortem-best-practices/) · [Blameless Postmortems - Rootly](https://rootly.com/incident-postmortems/blameless) · [CauSE Workshop 2025](https://causality-software-engineering.github.io/cause-workshop-2025/)
