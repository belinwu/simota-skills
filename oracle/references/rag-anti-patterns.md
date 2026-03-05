# RAG Anti-Patterns & Failure Modes

> RAG パイプラインの既知失敗パターン、統計データ、検出・予防戦略

## 1. RAG 失敗統計（2025-2026）

| 指標 | 値 | 出典 |
|------|---|------|
| RAG の本番サイレント失敗率 | **70%** | Redwerk 2025 |
| Agentic RAG の本番失敗率（2024） | **90%** | 業界レポート |
| 失敗の根本原因：チャンキング | **80%** | RAG 研究 |
| Naive 固定チャンキングの Faithfulness | **0.47-0.51** | 比較研究 |
| 最適化 Semantic チャンキングの Faithfulness | **0.79-0.82** | 比較研究 |
| Retrieval チューニングのみでの精度改善 | **50%+** | 最新研究 |
| データ品質が失敗主因のケース | **42%** | 実装レポート |
| 各レイヤー 95% 精度 → システム全体 | **81%** | カスケード失敗分析 |

---

## 2. RAG 10 大アンチパターン

| # | アンチパターン | 症状 | Oracle での影響 | 対策 |
|---|-------------|------|---------------|------|
| **RP-01** | **Retrieval 後付け** | LLM PoC に Retrieval を後から追加 | 検索品質が低く、ハルシネーション改善されず | Retrieval を first-class システムとして設計・独自 SLO 設定 |
| **RP-02** | **Naive 固定チャンキング** | 512 トークン固定分割、セクション・見出し無視 | Faithfulness 0.47-0.51 の低品質 | Semantic チャンキング、見出し保持、クエリ粒度に合わせた分割 |
| **RP-03** | **単一モノリシックインデックス** | 全コンテンツを 1 つの Vector DB に投入 | 検索精度低下、関連性の薄い結果 | ドメイン別インデックス分離（FAQ / ポリシー / 技術文書 / ログ） |
| **RP-04** | **プロンプト偏重・クエリ軽視** | プロンプトテンプレートに注力、クエリパイプライン未設計 | ユーザーの曖昧なクエリで検索失敗 | クエリリライト・意図分類・明確化ターンの導入 |
| **RP-05** | **評価フレームワーク不在** | Retrieval 固有メトリクス（Recall@K、Precision@K）未計測 | 品質劣化に気づかない | Retrieval / Generation / Task レベルの 3 層評価 |
| **RP-06** | **知識ベースの混沌** | 矛盾するドキュメント、古い情報が混在 | 「自信満々な混沌の増幅器」になる | ドキュメント品質管理、バージョン管理、矛盾検出 |
| **RP-07** | **ライブデータ直結** | RAG をライブ API に直接接続 | システムが脆弱化、API 障害でサービス停止 | 3 層知識ベース（静的コア / 定期更新 / オンデマンド）に分離 |
| **RP-08** | **ガードレール欠如** | ガバナンスがパイプラインに未統合 | ポリシー違反、データ漏洩、コンプライアンス問題 | 入力フィルタリング、ソースホワイトリスト、出力バリデーション |
| **RP-09** | **コンテキストウィンドウ過負荷** | 文書全体をコンテキストに投入 | 「Lost in the Middle」問題、精度低下 | Top 5-8 チャンクのみ取得、Reranker でコンテキスト圧縮 |
| **RP-10** | **Reranking 未適用** | Vector 検索の結果をそのまま使用 | 関連性の低い結果が混入、コンテキスト品質低下 | Cross-Encoder Reranker 導入（最も ROI が高い改善の 1 つ） |

---

## 3. カスケード失敗モデル

```
RAG パイプラインの各レイヤーが 95% 正確でも:
  Retrieval (0.95) × Reranking (0.95) × Generation (0.95) × Guardrails (0.95)
  = 0.81 (19% 失敗率)

失敗の連鎖:
  誤文書取得 → 不適切なリランキング → ハルシネーション生成 → ガードレールすり抜け
  → 4-5 段階の連鎖失敗

対策: 各レイヤーで独立した品質ゲートと失敗検出
  - Retrieval: Recall@K ≥ 0.8
  - Reranking: Precision@5 ≥ 0.7
  - Generation: Faithfulness ≥ 0.8
  - Guardrails: ポリシー違反率 < 1%
```

---

## 4. Hybrid Search 戦略

```
Vector 検索のみ vs Hybrid Search:
  Vector のみ: セマンティック類似度は高いが、キーワード一致を見逃す
  BM25 のみ: キーワード一致は強いが、意味的類似を見逃す
  Hybrid (BM25 + Dense Vector): 二桁の関連性向上

推奨構成:
  1. BM25 で候補を広く取得
  2. Dense Vector で意味的類似を取得
  3. Reciprocal Rank Fusion で結合
  4. Cross-Encoder Reranker で精緻化
  5. Top-K 結果をコンテキストに注入
```

---

## 5. RAG 評価の 3 層モデル

| 層 | 対象 | メトリクス | 目標値 |
|---|------|---------|-------|
| **Retrieval** | 検索品質 | Recall@K, Precision@K, MRR, NDCG | Recall@5 ≥ 0.8, Precision@5 ≥ 0.7 |
| **Generation** | 生成品質 | Faithfulness, Relevancy, Answer Correctness | Faithfulness ≥ 0.8 |
| **Task** | ビジネス価値 | Deflection Rate, Handle Time, CSAT | タスク固有に定義 |

```
評価アンチパターン:
  - テストセットを実行ごとに再生成 → ノイズ混入、結果比較不能
  - Retrieval と Generation を一括評価 → 問題箇所特定不能
  - 漠然とした「精度」のみ計測 → 改善アクション不明

ベストプラクティス:
  - 安定したテストセットを固定し、変更のみを測定
  - 3 層を独立して評価し、ボトルネックを特定
  - Task レベルメトリクスでビジネス価値を直接計測
```

---

## 6. Oracle との連携

```
Oracle での活用:
  1. ASSESS モードで RP-01〜10 のチェックリスト適用
  2. DESIGN モードで Hybrid Search 戦略を標準構成として推奨
  3. EVALUATE モードで 3 層評価モデルを適用
  4. SPECIFY モードで Builder への Retrieval SLO 仕様を含める

品質ゲート:
  - Retrieval SLO 未定義 → DESIGN 段階でブロック（RP-01 防止）
  - チャンキング戦略が固定サイズのみ → Semantic チャンキング検討を要求（RP-02 防止）
  - 評価メトリクスが「精度」のみ → 3 層評価を要求（RP-05 防止）
  - Reranker 未検討 → ROI 分析を推奨（RP-10 防止）
```

**Source:** [Redwerk: RAG Best Practices](https://redwerk.com/blog/rag-best-practices/) · [Martin Fowler: Emerging Patterns in Building GenAI Products](https://martinfowler.com/articles/gen-ai-patterns/) · [Evidently AI: RAG Evaluation Guide](https://www.evidentlyai.com/llm-guide/rag-evaluation) · [Orkes: Best Practices for Production-Scale RAG Systems](https://orkes.io/blog/rag-best-practices/)
