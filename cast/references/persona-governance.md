# Persona Governance & Organizational Readiness

> ペルソナライフサイクルガバナンス、廃止基準、組織導入戦略、Living Document 設計

## 1. ペルソナライフサイクルガバナンス

### 5 フェーズモデル（Pruitt & Adlin 拡張）

```
Phase 1 — Family Planning（計画）:
  - ペルソナの目的・スコープを定義
  - ステークホルダーの特定と巻き込み
  - 必要なデータソースの特定
  - 成功基準の定義

Phase 2 — Conception & Gestation（構想・醸成）:
  - データ収集（インタビュー、サーベイ、行動ログ）
  - セグメント分析
  - Proto-Persona ドラフト作成
  - ステークホルダーレビュー

Phase 3 — Birth & Maturation（誕生・成熟）:
  - データ検証（三角測量、ML クラスタリング）
  - ペルソナの正式化（confidence > 0.60）
  - レジストリ登録（draft → active）
  - 組織全体への配信

Phase 4 — Adulthood（成人期）:
  - 意思決定での積極的活用
  - 定期的なデータ更新（月次/四半期）
  - ドリフト検出と進化
  - 影響測定（ペルソナが意思決定にどう影響したか）

Phase 5 — Retirement（引退）:
  - 廃止トリガーの検出
  - ステークホルダー通知
  - アーカイブ（active → archived）
  - 後継ペルソナへの移行
```

### ガバナンス RACI マトリクス

| 活動 | UX リサーチ | プロダクト | エンジニア | ビジネス |
|------|-----------|----------|----------|---------|
| ペルソナ作成 | **R** (Responsible) | **C** (Consulted) | **I** (Informed) | **C** |
| データ検証 | **R** | **A** (Accountable) | **C** | **I** |
| 更新判断 | **R** | **A** | **I** | **C** |
| 廃止判断 | **C** | **A** | **I** | **C** |
| 活用推進 | **C** | **R** | **R** | **R** |

---

## 2. 更新トリガーとスケジュール

### 更新トリガー

| トリガー | 緊急度 | 例 |
|---------|--------|---|
| **重大な市場変化** | P0 (即時) | パンデミック、規制変更、競合の破壊的イノベーション |
| **ユーザーベースの急変** | P1 (1週間以内) | 急激なデモグラフィック変化、新規大口顧客 |
| **行動データの乖離** | P2 (1ヶ月以内) | ドリフト検出、新しい利用パターンの出現 |
| **定期レビュー** | P3 (四半期) | 定例のペルソナレビューサイクル |
| **新製品/機能リリース** | P2 | ユーザー行動に影響する大きな変更 |
| **フィードバック蓄積** | P3 | NPS/CSAT 傾向の変化、サポートチケットパターン変化 |

### 推奨スケジュール

```
月次:
  - ペルソナレジストリの鮮度チェック
  - 行動データとの乖離スキャン
  - confidence スコアの減衰適用

四半期:
  - フルペルソナレビュー（全ステークホルダー参加）
  - 新規セグメントの有無チェック
  - Anti-Persona の見直し
  - 活用実績の測定

年次:
  - 大規模データ再検証（ML クラスタリング再実行）
  - ペルソナセット全体の再評価
  - 廃止候補の特定
  - ガバナンスプロセス自体のレビュー
```

---

## 3. ペルソナ廃止（Retirement）基準

### 廃止トリガー

| # | トリガー | 判定基準 | アクション |
|---|---------|---------|----------|
| 1 | **セグメント消滅** | 該当ユーザーが 5% 未満に減少 | 即時アーカイブ |
| 2 | **セグメント統合** | 2 つのペルソナの行動差が有意でなくなった | ペルソナ統合 |
| 3 | **長期未使用** | 6 ヶ月間、意思決定で参照されていない | 廃止検討 |
| 4 | **confidence 崩壊** | confidence が 0.30 未満に低下 | 再検証 or 廃止 |
| 5 | **データソース喪失** | 主要データソースが利用不可になった | 代替データ or 廃止 |
| 6 | **ビジネス方針転換** | 対象市場/セグメントからの撤退 | アーカイブ |

### 廃止プロセス

```
Step 1: 廃止候補の特定
  - 上記トリガーのいずれかに該当
  - ステークホルダーへの事前通知

Step 2: 影響分析
  - このペルソナに依存するワークフローの特定
  - 下流エージェント（Echo/Spark/Retain）への影響評価
  - 代替ペルソナの有無確認

Step 3: ステークホルダー承認
  - プロダクトオーナーの承認（RACI で Accountable）
  - 異議申し立て期間（2 週間）

Step 4: 段階的移行
  - 後継ペルソナへのマッピング定義
  - 下流エージェントへの通知
  - レジストリステータス変更（active → archived）

Step 5: アーカイブ
  - ペルソナファイルを archive/ ディレクトリに移動
  - レジストリに archived_date と reason を記録
  - 進化ログに廃止記録を追加
```

---

## 4. 組織導入（Organizational Readiness）

### Persona Preparedness 評価

```
組織のペルソナ活用準備度を 5 軸で評価:

1. リーダーシップ支持 (Leadership Support):
   - 経営層がペルソナの価値を理解しているか
   - 予算とリソースが割り当てられているか

2. プロセス統合 (Process Integration):
   - 意思決定プロセスにペルソナが組み込まれているか
   - PRD/設計レビューでペルソナ参照が標準か

3. データ基盤 (Data Infrastructure):
   - ペルソナ更新に必要なデータが収集されているか
   - 行動ログ、フィードバック、サーベイの仕組みがあるか

4. スキル (Team Skills):
   - チームがペルソナの作成・更新・活用スキルを持つか
   - リサーチ手法の知識があるか

5. 文化 (Culture):
   - ユーザー中心の意思決定文化があるか
   - ペルソナに基づく議論が自然に行われるか
```

### 段階的導入ロードマップ

| Phase | 目標 | 活動 | 期間 |
|-------|------|------|------|
| **Seed** | 認知 | ペルソナワークショップ、成功事例共有 | 1-2 ヶ月 |
| **Grow** | 試行 | パイロットプロジェクトでペルソナ活用 | 2-3 ヶ月 |
| **Scale** | 標準化 | 全プロジェクトでペルソナ必須化 | 3-6 ヶ月 |
| **Optimize** | 最適化 | データ駆動更新、自動化、影響測定 | 6-12 ヶ月 |

---

## 5. Living Document 設計原則

### NN/G の 5 原則

| 原則 | 説明 | 実装 |
|------|------|------|
| **編集容易性** | 編集困難な形式は更新されない | Markdown/Wiki/Slides で管理 |
| **アクセス容易性** | チームが日常的にアクセスできる場所に配置 | リポジトリ or Wiki（チームの作業場所） |
| **更新の低コスト化** | 大規模リデザイン不要な軽微更新 | 属性単位の差分更新 |
| **変更履歴の可視化** | 何がいつ変わったかが分かる | バージョニング + 変更ログ |
| **安定性と柔軟性の両立** | 頻繁すぎる変更は混乱を招く | Core Identity 固定 + 周辺属性は柔軟 |

### フォーマット戦略

```
推奨: 「最も美しく、かつ簡単に編集できる形式」

避けるべき形式:
  × 高品質 PDF → 編集不可 = 更新不可
  × 複雑な Figma ファイル → デザイナー以外編集不可
  × 静的画像 → 部分更新不可

推奨形式:
  ○ Markdown（.md）→ エンジニアフレンドリー、Git 管理可能
  ○ Google Slides / Notion → 非技術者もアクセス可能
  ○ Wiki → 組織全体でアクセス + 編集可能
  ○ 構造化 YAML + 人間可読ビュー → Cast の採用方式
```

---

## 6. Cast との連携

```
Cast のガバナンスサポート:
  1. registry.yaml のライフサイクル状態管理（draft→active→evolved→archived）
  2. confidence 減衰アルゴリズムで自動的に鮮度を追跡
  3. AUDIT モードで廃止トリガーの自動チェック
  4. EVOLVE モードで Living Document の差分更新を実現
  5. DISTRIBUTE モードで更新を全下流エージェントに自動配信

ガバナンス強化提案:
  - registry に last_decision_reference（最後に意思決定で参照された日）を追加
  - 6 ヶ月未使用のペルソナに自動警告
  - 廃止承認ワークフローのテンプレート提供
  - 年次ペルソナレビュー用チェックリストの標準化
```

**Source:** [ScienceDirect: Persona Lifecycle](https://www.sciencedirect.com/topics/computer-science/persona-lifecycle) · [ResearchGate: Five Phases of Persona Lifecycle](https://www.researchgate.net/publication/301118893_The_five_phases_of_the_persona_lifecycle) · [NN/G: Personas Are Living Documents](https://www.nngroup.com/articles/personas-are-living-documents/) · [NN/G: Revising Personas](https://www.nngroup.com/articles/revising-personas/) · [PMC: Persona Preparedness Survey](https://pmc.ncbi.nlm.nih.gov/articles/PMC9469059/) · [Financial Brand: Persona Development Guide](https://thefinancialbrand.com/news/bank-marketing/a-guide-to-persona-development-from-demographic-profiles-to-usable-decision-tools-195763)
