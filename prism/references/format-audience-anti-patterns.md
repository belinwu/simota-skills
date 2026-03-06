# Format & Audience Matching Anti-Patterns

> 出力フォーマット選定・オーディエンス適合・コンテンツ戦略の失敗パターン

## 1. フォーマット選定 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **FA-01** | **Format Fixation（フォーマット固定）** | 常にAudio Overviewのみ使用し他フォーマットを無視 | 視覚的データがAudioで表現しきれない、配布資料が不足 | 目的→フォーマット選定マトリクスに従い最適形式を選択 |
| **FA-02** | **Audience-Format Mismatch（オーディエンス-フォーマット不一致）** | 経営層にDeep Dive 30分、学生にBrief 3分 | コンテンツ離脱率が高い、「長すぎ」「物足りない」のフィードバック | オーディエンス×目的のフィット表を参照して選定 |
| **FA-03** | **Purpose Blindness（目的盲目）** | フォーマットの「見栄え」で選び、目的との適合を無視 | Videoを作ったが実際にはSlide配布が必要だった | まず「この出力は何に使うか」を明確にしてから形式を選定 |
| **FA-04** | **One-Size-Fits-All Tone（万能トーン）** | 全オーディエンスに同じトーンを使用 | B2B向けにカジュアルすぎ、学生向けにフォーマルすぎ | オーディエンスタイプ別のトーンキャリブレーション表を使用 |
| **FA-05** | **Duration Disconnect（時間の不適合）** | オーディエンスの注意力に合わない長さ | 経営層向け25分（離脱）、研究者向け5分（情報不足） | オーディエンス別の最適尺表を参照 |
| **FA-06** | **Multi-Format Incoherence（マルチフォーマット不整合）** | 同一トピックのAudio/Video/Slideで内容が矛盾 | 各フォーマットで異なるキーメッセージ | コアメッセージを先に定義、全フォーマットで一貫させる |
| **FA-07** | **Accessibility Ignorance（アクセシビリティ無視）** | 出力の利用環境・制約を考慮しない | 通勤中にSlide共有、会議中にAudio再生 | 利用シーン（移動中/デスク/会議）を確認し適切な形式を選定 |

---

## 2. オーディエンス分析の罠

```
オーディエンス理解の失敗:

  ❌ Assumed Knowledge（知識の仮定）:
    → オーディエンスの事前知識を過大/過小評価
    → 専門家に基本概念の説明で時間浪費、初心者に用語の洪水
    → 対策: 知識レベルを明示（「5年の経験を持つエンジニア」）

  ❌ Monolithic Audience（一枚岩のオーディエンス）:
    → 全視聴者を均一な集団として扱う
    → 一部の層には合うが他の層には不適合
    → 対策: 主要オーディエンスを1つ定義、サブオーディエンスは注記

  ❌ Demographic-Only Persona（属性のみのペルソナ）:
    → 「30代男性エンジニア」のように属性だけ定義
    → 動機・課題・意思決定文脈が不明
    → 対策: ゴール・課題・文脈・意思決定段階まで定義

  ❌ Self-as-Audience（自分=オーディエンス）:
    → 自分が理解できるレベルで満足
    → 実際のターゲットの知識レベルとずれている
    → 対策: ペルソナを明示的に設定し、自分の視点から切り離す

  ❌ No Decision Context（意思決定文脈の欠如）:
    → オーディエンスが「何を決めるために」聴くかを考慮しない
    → 情報提供で終わり、行動に繋がらない
    → 対策: 「このコンテンツを聴いた後、何を判断するか」を定義
```

---

## 3. フォーマット×オーディエンス適合表

### Audio Overview 適合ガイド

| オーディエンス | 推奨スタイル | 最適時間 | 避けるべき |
|-------------|-----------|---------|-----------|
| C-suite | Brief: Executive Summary | 5-8分 | Deep Dive（時間なし） |
| プロダクトマネージャー | Brief/Deep Dive | 8-15分 | Lecture Mode（学術的すぎ） |
| シニアエンジニア | Deep Dive: Technical | 15-20分 | Brief（情報不足） |
| ジュニア開発者 | Lecture: Tutorial | 20-25分 | Critique（経験不足で理解困難） |
| 研究者 | Critique: Research | 12-18分 | Brief（深度不足） |
| 一般向け | Deep Dive: General | 15-18分 | Technical Deep Dive（専門的すぎ） |
| 学生 | Lecture: Tutorial | 20-25分 | Executive Brief（文脈不足） |
| セールスチーム | Brief: Social Share | 3-8分 | Academic Lecture（関心外） |

### Video Overview 適合ガイド

| オーディエンス | 推奨スタイル | 最適時間 | 避けるべき |
|-------------|-----------|---------|-----------|
| 技術者 | Explainer: Whiteboard | 3-5分 | Cinematic（装飾的） |
| 経営者 | Explainer: Corporate | 2-3分 | Academic（学術的） |
| SNSフォロワー | Brief: Casual | 30-90秒 | Whiteboard（地味） |
| 学生 | Explainer: Classroom | 5-10分 | Corporate（ビジネス寄り） |

### Slide Deck 適合ガイド

| 用途 | 推奨形式 | スライド数 | 文字密度 |
|------|---------|-----------|---------|
| カンファレンス登壇 | Presenter: TED-style | 10-15 | 最小（6語/スライド） |
| 社内報告 | Presenter: Internal | 10-20 | 中程度 |
| 配布資料 | Detailed: Handout | 15-30 | 高（自立的に読める） |
| 研修教材 | Detailed: Educational | 20-30 | 中〜高 |

---

## 4. コンテンツ戦略の罠

```
戦略レベルの失敗:

  ❌ Format Before Strategy（戦略前のフォーマット決定）:
    → 「Podcastを作りたい」から始まり目的を後付け
    → 形式と目的が合わない、効果測定ができない
    → 対策: 目的（教育/説得/共有/記録）→オーディエンス→フォーマットの順

  ❌ No Repurposing Plan（再利用計画なし）:
    → 1ソースから1フォーマットのみ生成
    → 同じ労力でマルチチャネル展開可能だったのに機会損失
    → 対策: 1ノートブックからAudio+Slide+Infographicを計画的に生成

  ❌ Engagement Metric Absence（エンゲージメント指標なし）:
    → 「作って終わり」で効果を測定しない
    → 改善のフィードバックループが欠如
    → 対策: 視聴完了率・共有数・アクション実行率等のKPIを設定

  ❌ Channel-Blind Distribution（チャネル無視の配布）:
    → 30分のDeep Diveをソーシャルメディアに投稿
    → プラットフォームの特性と合わないコンテンツ
    → 対策: チャネル→最適フォーマット・長さのマッピング

  ❌ Seasonal Tone Mismatch（時期とトーンの不一致）:
    → 緊急報告にカジュアルトーン、日常共有にフォーマルトーン
    → 状況にそぐわないコンテンツ
    → 対策: 緊急度・状況に応じたトーンキャリブレーション
```

---

## 5. マルチフォーマット展開のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **MF-01** | **Sequential Duplicate（逐次複製）** | Audio→Videoに単純コピーし各フォーマットの特性を無視 | Videoが「音声の焼き直し」、ビジュアル活用なし | 各フォーマットの強みを活かした個別最適化 |
| **MF-02** | **Key Message Drift（キーメッセージの漂流）** | フォーマットごとに微妙に異なるメッセージ | オーディエンスが複数接点で矛盾を感じる | コアメッセージを先に3点定義し全フォーマットで維持 |
| **MF-03** | **Flat Adaptation（平坦な適応）** | 全フォーマットに同じ深度・幅で情報を詰める | Briefが長すぎ、Deep Diveが浅すぎ | フォーマット別の情報量ガイド: Brief=3点、Deep Dive=5-8点 |
| **MF-04** | **Missing Funnel Design（ファネル設計の欠如）** | Teaser→Brief→Deep Diveの導線がない | 各コンテンツが孤立、次のアクションに繋がらない | コンテンツファネル: Teaser(興味)→Brief(理解)→Deep Dive(深化) |

---

## 6. Prism との連携

```
Prism での活用:
  1. SOURCE フェーズで FA-01〜07 のフォーマット適合性チェック
  2. STEER フェーズでオーディエンス分析の品質確認
  3. GUIDE フェーズでフォーマット×オーディエンス適合表の適用
  4. SPECTRUM フェーズでフォーマット-オーディエンスフィットの追跡

品質ゲート:
  - Audio Overviewのみ使用 → 目的に合うフォーマット提案（FA-01 防止）
  - 経営層に30分Deep Dive → Brief推奨（FA-02 防止）
  - トーン未指定 → オーディエンス別トーン提案（FA-04 防止）
  - フォーマット先行の依頼 → 目的→オーディエンス→フォーマット順の誘導（Format Before Strategy 防止）
  - マルチフォーマットでメッセージ不一致 → コアメッセージ事前定義（MF-02 防止）
  - 導線なしの複数コンテンツ → ファネル設計提案（MF-04 防止）
```

**Source:** [Storyteq: AI Content Audience Preferences](https://storyteq.com/blog/how-does-ai-content-generation-adapt-to-audience-preferences/) · [Wellows: 10 AI Content Mistakes](https://wellows.com/blog/ai-mistakes-marketers-should-avoid/) · [Optimizely: Quality Content with AI](https://www.optimizely.com/insights/blog/quality-content-with-ai/) · [Google Blog: NotebookLM Video/Audio Overviews](https://blog.google/innovation-and-ai/models-and-research/google-labs/notebooklm-video-overviews-studio-upgrades/)
