# LLM Evaluation & Observability Best Practices

> LLM 評価の方法論・アンチパターン、本番オブザーバビリティ、LLM-as-Judge の落とし穴と対策

## 1. 評価の 2 層安全ネットモデル

```
Layer 1: 自動メトリクス（第一防衛線）
  ├── テキスト類似度: BLEU, ROUGE-L, BERTScore
  ├── 正確性: Exact Match, F1 Score
  ├── 品質スコア: GPTScore, LLM-as-Judge
  └── RAG 固有: Faithfulness, Relevancy, Context Precision

Layer 2: 人間レビュー（第二防衛線）
  ├── Likert スケール評価（1-5）
  ├── ドメイン専門家の判断
  ├── エッジケース・ニュアンス検出
  └── バイアス・公平性監査

核心: 自動メトリクスは明白な問題をフラグし、
      人間レビューはニュアンスを処理する
      → 両方の組み合わせが各単独を上回る
```

---

## 2. LLM-as-Judge のアンチパターン

| # | アンチパターン | 問題 | 対策 |
|---|-------------|------|------|
| **EV-01** | **自己評価** | LLM が自身の出力を評価 → 誤りの強化 | 別モデルを Judge として使用、または人間評価と併用 |
| **EV-02** | **Position Bias** | A/B 比較で先に提示された回答を好む傾向 | 順序ランダム化 · 複数回実行で平均化 |
| **EV-03** | **Verbosity Bias** | 長い回答を高品質と判定する傾向 | 簡潔さも評価基準に含める · 文字数正規化 |
| **EV-04** | **Rubric 不在** | 各スコアの定義が曖昧 → Judge 間で不一致 | アンカー例付きの明確な Rubric 定義 |
| **EV-05** | **単一 Judge** | 1 つの Judge モデルのバイアスがそのまま反映 | Multi-Judge (3+) で多数決または平均 |
| **EV-06** | **Ground Truth 不在** | 参照回答なしで絶対評価 → 基準のドリフト | Reference Grounding: 必ず Ground Truth を提供 |
| **EV-07** | **テストセット再生成** | 実行ごとにテストデータを再生成 → ノイズ混入 | 安定したテストセットを固定、変更のみを測定 |
| **EV-08** | **一括評価** | Retrieval + Generation を一体評価 → 問題箇所特定不能 | コンポーネント別評価（Retrieval / Generation / Task） |

---

## 3. 評価を CI/CD に統合

```
評価を最終 QA ではなく継続的統合として扱う:

  開発フェーズ:
    1. プロンプト変更 → eval スイート自動実行
    2. Regression 検出（5% 以上の低下でブロック）
    3. 新テストケース追加（失敗トレースをデータセット化）

  デプロイフェーズ:
    4. Shadow Mode で 24h 検証
    5. Canary (5%) → 25% → 50% → 100%
    6. 各段階で品質メトリクスチェック

  本番フェーズ:
    7. サンプリング評価（5% のリクエスト）
    8. ドリフト検出アラート
    9. 定期的な人間評価（週次/月次）
    10. フィードバックを次の eval データセットに還元

アンチパターン: 評価をリリース前の最終チェックとしてのみ実行
  → ドリフト、モデル更新、データ変化に対応不能
```

---

## 4. オブザーバビリティの 7 つの柱

| # | 柱 | 説明 | 必須メトリクス |
|---|---|------|-------------|
| **1** | **セマンティック計装** | セッション・トレース・スパン・生成に一意 ID | trace_id, span_id, session_id |
| **2** | **完全なリクエスト-レスポンスキャプチャ** | 入力・出力・中間状態の完全ログ | query, response, tool_calls, retrieved_docs |
| **3** | **継続的メトリクス監視** | トークン使用量・コスト・レイテンシ・品質スコア | tokens, cost, latency_p95, eval_score |
| **4** | **統合評価** | 自動スコアリング + 人間レビューの組み合わせ | auto_score, human_score, agreement_rate |
| **5** | **リアルタイムアラート** | レイテンシ・コスト・品質のしきい値アラート | alert_threshold, incident_count |
| **6** | **データエクスポート** | 外部分析ツールへのトレースデータ転送 | export_format, destination |
| **7** | **エンタープライズセキュリティ** | RBAC・SSO・VPC・データレジデンシー | access_control, compliance_status |

---

## 5. オブザーバビリティのアンチパターン

| # | アンチパターン | 問題 | 対策 |
|---|-------------|------|------|
| **OB-01** | **サイロ化されたデータ** | ログ・評価・アラートが別ツールで分断 | トレース・評価・アラートを単一フィードバックループに統合 |
| **OB-02** | **リクエスト単位の孤立** | 各リクエストを独立扱い、会話パターンを見落とす | セッション単位のトレーシング、会話レベルの分析 |
| **OB-03** | **エンジニア専用評価** | 評価実行が開発者のみ → スケール制約 | PM・QA・ドメイン専門家が参加可能な評価 UI |
| **OB-04** | **ブラックボックス推論** | モデル内部ロジックが不透明 | CoT の外部化 · ツールコール詳細ログ · 決定根拠の記録 |
| **OB-05** | **マルチステップ追跡欠如** | RAG パイプラインやエージェントの各段階が未計装 | Retrieval / Reranking / Generation / Tool Call 各段階のスパン |

---

## 6. 本番監視ダッシュボード設計

### 必須メトリクス

| カテゴリ | メトリクス | アラートしきい値 |
|---------|---------|--------------|
| **パフォーマンス** | p50 / p95 / p99 レイテンシ | p95 > ベースライン 2 倍 |
| **品質** | LLM-as-Judge スコア（サンプリング） | ベースラインの 90% 未満 |
| **コスト** | リクエストあたりトークン / 日次支出 | 予算の 120% 超 |
| **エラー** | 失敗リクエスト率 | > 1% |
| **安全性** | ガードレール発火率 | > 5% |
| **ドリフト** | 入力分布変化 | 有意な変化検出 |
| **ユーザーフィードバック** | 👍/👎 率、NPS | 満足率 < 80% |

### トレーシングアーキテクチャ

```
Session（マルチターン会話）
  └── Trace（エンドツーエンドリクエスト処理）
       ├── Span: クエリ処理
       ├── Span: Retrieval（RAG コンテキスト取得）
       ├── Span: Reranking
       ├── Span: Generation（LLM 呼び出し）
       ├── Span: Tool Call（外部 API 実行）
       └── Span: ガードレール検証

各スパンに付与:
  - 開始/終了タイムスタンプ
  - トークン使用量
  - モデルバージョン
  - 入力/出力
  - カスタムメタデータ（experiment_id, user_segment）
```

---

## 7. 規制対応（2025-2026）

```
EU AI Act / 米国州法への対応:
  1. トレーサビリティ: 評価スコアを正確なプロンプト/モデル/データセットバージョンに紐付け
  2. 公平性監査: 定期的なバイアステスト（四半期ごと）
  3. 監査証跡: 全ツールコールと判断根拠の不変ログ
  4. データ保護: PII マスキング・テナント分離・データレジデンシー
  5. 説明責任: 高リスク判断での人間承認ゲート
```

---

## 8. Oracle との連携

```
Oracle での活用:
  1. EVALUATE モードで EV-01〜08 の検出チェックリスト適用
  2. DESIGN モードで OB-01〜05 回避のオブザーバビリティ設計
  3. ASSESS モードで本番監視ダッシュボードの Gap 分析
  4. SPECIFY モードでトレーシング・評価要件を Builder 仕様に含める

品質ゲート:
  - LLM-as-Judge が自己評価 → 別モデル使用を要求（EV-01 防止）
  - テストセットが固定されていない → 安定セット作成を要求（EV-07 防止）
  - オブザーバビリティがログのみ → トレーシング + 評価統合を要求（OB-01 防止）
  - 評価が開発者専用 → 非エンジニア参加可能な仕組みを推奨（OB-03 防止）
```

**Source:** [Maxim AI: LLM Observability Best Practices for 2025](https://www.getmaxim.ai/articles/llm-observability-best-practices-for-2025/) · [FutureAGI: LLM Evaluation Frameworks 2026](https://futureagi.substack.com/p/llm-evaluation-frameworks-metrics) · [Confident AI: Top 7 LLM Observability Tools](https://www.confident-ai.com/knowledge-base/top-7-llm-observability-tools) · [Monte Carlo Data: LLM-As-Judge Best Practices](https://www.montecarlodata.com/blog-llm-as-judge/)
