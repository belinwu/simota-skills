# Continuous Discovery & Mixed Methods

> Continuous Discovery Habits のリサーチ適用、混合手法設計、三角測量フレームワーク、Always-On リサーチ

## 1. Continuous Discovery とリサーチ

### 定義

アジャイルチームにおいて、プロダクト開発ライフサイクル全体を通じて小規模・高頻度のリサーチ活動を継続的に行うアプローチ。Teresa Torres が提唱。

### コア原則

```
従来: リサーチは「プロジェクト」（開始 → 完了 → 次まで待機）
  ↓
Continuous: リサーチは「習慣」（毎週のリズムで常時実行）
```

| 原則 | 説明 |
|------|------|
| **週次の顧客接点** | 毎週少なくとも1回ユーザーと対話 |
| **デュアルトラック** | Discovery（学習）と Delivery（構築）を同時並行 |
| **仮説駆動** | すべてのリサーチが検証すべき仮説から始まる |
| **小さく速く** | 大規模プロジェクトより小さな実験を繰り返す |
| **チーム全体で** | Product Trio（PM + Designer + Engineer）が参加 |

### 2026年のトレンド統計

| トレンド | リサーチャーの選択率 |
|---------|-------------------|
| AI 活用分析・合成 | **88%** |
| Synthetic Users | **48%** |
| リサーチ民主化 | **36%** |
| リサーチリポジトリ・インサイト管理 | **29%** |
| リサーチの戦略的ポジショニング | **27%** |
| **Continuous Discovery アプローチ** | **26%** |
| ResearchOps・リサーチスケーリング | **25%** |
| アクセシビリティファーストなリサーチ | **22%** |
| マルチモーダルリサーチ手法 | **20%** |
| 縦断的・Always-On リサーチ | **14%** |

---

## 2. Continuous Discovery リサーチケイデンス

### 週次リズムテンプレート

```
月曜: リサーチプランニング + 仮説レビュー
火曜: ユーザーインタビュー / ユーザビリティテスト（1-2セッション）
水曜: 分析・合成 + チーム共有
木曜: インサイト統合 + ロードマップへの反映検討
金曜: 振り返り + 来週のリクルーティング確認
```

### 習慣ループの設計

```
トリガー（定期スケジュール）
  → ルーチン（週次インタビュー + 合成）
    → 報酬（チームの意思決定改善を実感）
      → 強化（トリガーの定着）
```

**鍵**: 散発的な Discovery は定着しない。チームのイテレーションサイクルに自然に組み込むシステムが必要。

### プロジェクトベース vs Continuous

| 観点 | プロジェクトベース | Continuous |
|------|-----------------|-----------|
| **頻度** | 四半期/半期に1回 | 毎週 |
| **スコープ** | 大規模・包括的 | 小規模・焦点的 |
| **チーム関与** | リサーチャー主導 | Product Trio 参加 |
| **インサイトの鮮度** | 数週間〜数ヶ月前のデータ | 今週のデータ |
| **意思決定への影響** | 遅延あり（レポート待ち） | 即座に反映 |
| **コスト** | 高（集中リソース） | 低（分散型） |
| **適用場面** | 戦略的判断、新市場参入 | 日常的なプロダクト改善 |

### Researcher フェーズとの統合

| Continuous 活動 | Researcher フェーズ | 頻度 |
|----------------|-------------------|------|
| 週次インタビュー | DEFINE → DESIGN → ANALYZE | 毎週 |
| クイックテスト | DESIGN → ANALYZE | 必要時 |
| インサイト合成 | SYNTHESIZE | 毎週 |
| パターンレビュー | DISTILL | 月次 |
| 戦略的リサーチ（大規模） | 全フェーズ | 四半期 |

---

## 3. Mixed Methods（混合手法）

### 定義

定性的（QUAL）と定量的（QUANT）のリサーチを意図的・協調的に組み合わせ、より豊かで行動可能なインサイトを生み出すアプローチ。

### 3つの基本デザイン

| デザイン | 順序 | 用途 | 例 |
|---------|------|------|-----|
| **Explanatory Sequential** | QUANT → QUAL | 定量結果の「なぜ」を掘り下げ | サーベイで不満検出 → インタビューで原因究明 |
| **Exploratory Sequential** | QUAL → QUANT | 定性発見を定量検証 | インタビューでニーズ発見 → サーベイで普遍性検証 |
| **Convergent Parallel** | QUAL + QUANT 同時 | 多角的な同時検証 | ユーザビリティテスト + アナリティクスデータ同時分析 |

### Mixed Methods 選択フローチャート

```
Q: 何を知りたいか?
  → 「なぜそうなるか?」を知りたい
    → 定量データが既にある?
      → Yes → Explanatory Sequential（QUANT → QUAL）
      → No → まず QUAL で探索
  → 「どの程度広がっているか?」を知りたい
    → 定性インサイトが既にある?
      → Yes → Exploratory Sequential（QUAL → QUANT）
      → No → まず QUAL でパターン発見
  → 「全体像を把握したい」
    → リソースが十分?
      → Yes → Convergent Parallel（同時実行）
      → No → Sequential のどちらかを選択
```

### 実践テンプレート

```markdown
## Mixed Methods Research Plan

### リサーチクエスチョン
[中心的な問い]

### デザイン選択
- [ ] Explanatory Sequential（QUANT → QUAL）
- [ ] Exploratory Sequential（QUAL → QUANT）
- [ ] Convergent Parallel（同時）

### Phase 1: [QUAL / QUANT]
- **手法**: [インタビュー / サーベイ / テスト]
- **参加者**: [N名]
- **期間**: [X週]
- **アウトプット**: [テーマ / 統計 / パターン]

### Phase 2: [QUAL / QUANT]
- **手法**: [インタビュー / サーベイ / テスト]
- **参加者**: [N名]
- **期間**: [X週]
- **アウトプット**: [テーマ / 統計 / パターン]

### 統合分析
- 収斂点: [QUAL と QUANT が一致するポイント]
- 相違点: [不一致のポイント → 追加調査の候補]
- 統合インサイト: [両方から得られた総合的な理解]
```

---

## 4. 三角測量（Triangulation）

### 定義

複数のデータソースまたはアプローチを使用してリサーチの信頼性を高める手法。

### 4種類の三角測量

| 種類 | 説明 | 例 |
|------|------|-----|
| **データ三角測量** | 異なるソースからのデータを比較 | インタビュー + アナリティクス + サポートチケット |
| **手法三角測量** | 異なるリサーチ手法の結果を比較 | ユーザビリティテスト + ダイアリースタディ |
| **研究者三角測量** | 複数の研究者が独立に分析 | 2名が独立にコーディング → 比較 |
| **理論三角測量** | 異なる理論的レンズで解釈 | 認知心理学 + 社会学の視点 |

### Spotify の同時三角測量モデル

ユーザーリサーチとデータサイエンスの手法を同時に混合:

```
ユーザーリサーチ（定性）     データサイエンス（定量）
  インタビュー        ←→     行動ログ分析
  ダイアリースタディ    ←→     コホート分析
  ユーザビリティテスト   ←→     A/B テスト結果
          ↓                      ↓
        統合分析（同時三角測量）
          ↓
      包括的インサイト
```

### 三角測量の解釈パターン

| 結果 | 意味 | アクション |
|------|------|----------|
| **収斂（Convergence）** | 複数手法が同じ結論を指す | 高信頼度のインサイトとして扱う |
| **補完（Complementarity）** | 手法が異なる側面を照らす | 統合して全体像を構築 |
| **矛盾（Discrepancy）** | 手法間で結論が異なる | **最も興味深い発見**の可能性 → 深掘り |

**矛盾の例:**
```
サーベイ: ユーザーはオンボーディングに「満足」と回答
ユーザビリティテスト: オンボーディング画面で繰り返し混乱
  → 「言っていること」と「していること」の乖離
  → 真のインサイト: 社会的望ましさバイアス + 無意識の摩擦
```

---

## 5. Always-On リサーチ

### 定義

特定のプロジェクトに紐づかない、常時稼働のフィードバック収集メカニズム。

### Always-On チャネル設計

| チャネル | データ種別 | 頻度 | ツール例 |
|---------|----------|------|---------|
| **アプリ内サーベイ** | 満足度、NPS、タスク後フィードバック | 継続 | Hotjar, Qualtrics |
| **フィードバックウィジェット** | 自由記述フィードバック | 継続 | UserVoice, Canny |
| **セッション録画** | 行動データ | 継続 | FullStory, LogRocket |
| **サポートチケット分析** | ペインポイント、バグ | 日次 | Zendesk + AI 分析 |
| **レビュー監視** | 感情、競合比較 | 週次 | AppFollow, G2 |
| **パネル常備** | クイックリサーチ用参加者 | 常時利用可能 | Rally, UserInterviews |

### Continuous + Always-On + プロジェクト の統合

```
Always-On（常時収集）
  → シグナル検出（パターン・異常）
    → Continuous Discovery（週次検証）
      → 重要テーマの場合 → プロジェクトベースリサーチ（深堀り）
      → 軽微な場合 → インサイトカード化 → リポジトリ登録
```

### Researcher との統合

| リサーチ種別 | 頻度 | 深さ | Researcher フェーズ |
|------------|------|------|-------------------|
| Always-On | 常時 | 浅い（シグナル） | — (自動) |
| Continuous | 週次 | 中程度（検証） | DEFINE → ANALYZE |
| プロジェクト | 四半期 | 深い（戦略的） | 全フェーズ |

**Source:** [Teresa Torres: Continuous Discovery](https://www.producttalk.org/2021/07/user-research-and-continuous-discovery/) · [Product School: Continuous Discovery](https://productschool.com/blog/product-fundamentals/continuous-discovery) · [IxDF: What Is Continuous Discovery](https://www.interaction-design.org/literature/topics/continuous-discovery) · [NN/g: Mixed Methods Research](https://www.nngroup.com/articles/mixed-methods-research/) · [NN/g: Triangulation](https://www.nngroup.com/articles/triangulation-better-research-results-using-multiple-ux-methods/) · [Spotify Design: Simultaneous Triangulation](https://spotify.design/article/simultaneous-triangulation-mixing-user-research-and-data-science-methods) · [Looppanel: Mixed Methods Research](https://www.looppanel.com/blog/mixed-methods-research) · [Lyssna: UX Research Trends 2026](https://www.lyssna.com/blog/ux-research-trends/)
