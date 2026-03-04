# CI Anti-Patterns & Cognitive Biases

> 競合分析でよくある失敗パターン、認知バイアス、対策

## 1. 競合分析アンチパターン

### Pattern 1: 競合への過剰フォーカス（Over-Indexing）

**症状**: 競合の動きに反応するだけで、自社独自の戦略を構築しない。

```
❌ 「競合が○○を出した → うちも作ろう」
✅ 「顧客の未充足ニーズは何か → どの解決策が最も価値があるか」
```

**対策**: 競合分析の結論を常に「顧客にとっての価値」に変換。Compete の原則1「Know competitors, obsess over customers」の実践。

### Pattern 2: コピーキャット戦略

**症状**: 競合の機能・価格・ポジショニングをそのまま模倣。差別化が失われる。

| リスク | 結果 |
|-------|------|
| 機能コピー | 追随者のポジション固定化 |
| 価格追随 | マージン侵食の価格競争 |
| メッセージ模倣 | ブランド独自性の喪失 |

**対策**: Blue Ocean の ERRC Grid で「排除・削減・増加・創造」を明確化。

### Pattern 3: 一回限りの分析（One-Off Analysis）

**症状**: CI をプロジェクト開始時だけの活動として扱う。

**現実**: 市場と競合は常に変化。一時点のスナップショットは急速に陳腐化。

**対策**: SHARPEN サイクル（既存）+ 定期的な更新リズム（月次/四半期）。

### Pattern 4: 価格への過剰集中

**症状**: 競合分析を価格比較に矮小化し、不要なディスカウントとマージン侵食を招く。

**データ**: 顧客は品質と価値の両方を評価。価値観に合う製品には高い金額を支払う意思がある。

**対策**: TCO 比較（既存テンプレート）+ バリューベース比較を標準化。

### Pattern 5: 間接競合の無視

**症状**: 直接競合のみに注目し、代替ソリューションを見落とす。

```
例: プロジェクト管理ツール
  直接競合: Asana, Monday.com, ClickUp
  間接競合: Excel/スプレッドシート, メール, Slack チャンネル
  ← ここを無視すると市場シェア浸食に気づけない
```

**対策**: JTBD（Jobs to Be Done）視点で「顧客が解決しようとしている仕事」から競合を定義。

### Pattern 6: サイロ化されたデータ分析

**症状**: 部門ごとにデータを孤立して分析し、市場全体の不正確な結論を導く。

**例**: 一時的な売上スパイクを持続的成長と誤認し、季節的トレンドを見落とす。

**対策**: クロスファンクショナルな CI レビュー（営業 + マーケ + プロダクト）。

### Pattern 7: 無関係な詳細への注力

**症状**: 「必須知識」と「あれば良い知識」を区別せず、時間を浪費。

**対策**: 分析前に「意思決定に影響する問い」を明確化。その問いに答える情報のみ収集。

---

## 2. 認知バイアス

### CI に影響する主要バイアス

| バイアス | CI への影響 | 対策 |
|---------|-----------|------|
| **確認バイアス** | 「競合は弱い/強い」という前提に合致する情報だけを収集 | 反証を意図的に探す。Multi-Engine Mode で複数視点 |
| **アンカリング** | 最初に見た競合データに過度に固執 | 複数ソースを独立に評価してから統合 |
| **利用可能性** | 最近のニュースや目立つ事例に引きずられる | 時系列データで長期トレンドを確認 |
| **生存者バイアス** | 成功した競合戦略だけを参照し、失敗事例を無視 | 撤退・失敗した競合も分析対象に含める |
| **集団思考** | チーム内で異論が出にくく、楽観的/悲観的評価に偏る | Devil's advocate 役を意図的に設定 |
| **正常性バイアス** | 「競合の変化は自社に影響しない」と過小評価 | シナリオ分析で最悪ケースも検討 |

### Compete のバイアス対策

1. **MAP フェーズ**: 複数の独立ソースから収集（ソース信頼度スコアで重み付け）
2. **ANALYZE フェーズ**: 仮説を書き出し、各仮説の検証・反証結果を記録
3. **DIFFERENTIATE フェーズ**: Multi-Engine Mode で複数 AI が独立に差別化戦略を提案
4. **SHARPEN フェーズ**: 予測精度を追跡し、バイアスの影響を定量化

---

## 3. Compete のアンチパターン防止チェックリスト

### 分析開始前

- [ ] 意思決定に影響する問いを明確化したか?
- [ ] 直接競合 + 間接競合を両方リストアップしたか?
- [ ] 既存の前提・仮説を書き出したか?（バイアス防止）

### 分析中

- [ ] 複数の独立ソースからデータを収集したか?
- [ ] 仮説に反する証拠も意図的に探したか?
- [ ] 価格だけでなく価値全体を比較しているか?
- [ ] 競合の模倣ではなく差別化に焦点を当てているか?

### 分析後

- [ ] 結論を「顧客にとっての価値」に変換したか?
- [ ] 予測に自信度を付与したか?（SHARPEN 連携）
- [ ] 次回更新のタイミングを設定したか?
- [ ] クロスファンクショナルなレビューを実施したか?

**Source:** [Confirmation Bias in CI - Uncovered](https://uncovered.so/blog/confirmation-bias-in-competitive-intelligence) · [CI Mistakes - Octopus Intelligence](https://www.octopusintelligence.com/mistakes-in-competitive-intelligence-gathering-and-how-to-sort-them/) · [8 CI Mistakes - Hanover Research](https://www.hanoverresearch.com/reports-and-briefs/corporate/8-mistakes-to-avoid-in-competitive-intelligence/) · [Market Intelligence Pitfalls - Valona](https://valonaintelligence.com/resources/blog/common-pitfalls-in-market-intelligence-research-and-how-to-avoid-them) · [Over-Indexing - rok.biz](https://www.rok.biz/outsmart-the-competition-a-guide-to-competitive-analysis/) · [CI Mistakes - Veridion](https://veridion.com/blog-posts/gathering-competitive-intelligence-mistakes/)
