# Modern Product Discovery

> Opportunity Solution Tree, Continuous Discovery Habits, Shape Up, Outcome-Driven Innovation, AI 活用プロダクトディスカバリー

## 1. Opportunity Solution Tree (OST)

### 概要

Teresa Torres（2016年〜）が提唱した視覚的フレームワーク。4層構造でディスカバリーを体系化。

```
Desired Outcome（望ましい成果）
  └─ Opportunities（機会 = 顧客ニーズ・ペインポイント・望み）
       └─ Solutions（解決策 = 各機会への対処アイデア）
            └─ Assumption Tests（仮説テスト = 解決策の検証）
```

### Spark への活用

| OST 層 | Spark フェーズ | 対応 |
|--------|-------------|------|
| Outcome | IGNITE | ビジネス目標の明確化 |
| Opportunity | IGNITE → SYNTHESIZE | 機会の探索・選別 |
| Solution | SYNTHESIZE → SPECIFY | 提案仕様の作成 |
| Assumption Test | VERIFY | 仮説検証計画 |

### ベストプラクティス（2025年）

- **プロダクトトリオ**（PM + Designer + Lead Engineer）で共同作成
- 大きな機会を小さなサブ機会に分解し、一度に1つに集中
- アイデア全体ではなく**前提を分解してテスト**（前提テストは1〜2日で可能）
- OSTを「生きたドキュメント」として週次で更新

---

## 2. Continuous Discovery Habits

### 核心原則

ディスカバリーは「プロジェクト開始時に一度」ではなく**週次のリズム**として習慣化。

| 習慣 | 内容 |
|------|------|
| **Weekly Touchpoints** | 毎週の顧客接点（インタビュー、観察、データ分析） |
| **Story-Based Interviews** | 過去の実際の行動に関する具体的ストーリーを収集 |
| **Synthesis → OST** | インタビュー後に合成結果をOSTに反映 |
| **Assumption Mapping** | 仮説をリスク×不確実性でマッピングし、最もリスキーなものから検証 |
| **Small Bets** | 大きな賭けではなく小さな実験で学習 |

### Discovery Cadence テンプレート

```
月曜: 先週の学びレビュー → OSTアップデート
火曜-木曜: 顧客インタビュー（2-3件/週） + 仮説テスト
金曜: 合成 → 次週の優先機会選定
```

### アンチパターン

- ディスカバリーをプロジェクト開始時だけに行う（Batch Discovery）
- PMだけがディスカバリーを行いサイロ化する
- 表面レベルで結論に飛びつく（深堀り不足）
- 既存の最適化（Exploit）ばかりで探索（Explore）しない

---

## 3. Shape Up (Basecamp)

### フレームワーク概要

Ryan Singer（Basecamp）提唱。固定タイムボックスでの開発手法。

| 概念 | 説明 |
|------|------|
| **6週間サイクル** | オープンエンドではなく固定期間で意味のある作業を完了 |
| **Shaping（成形）** | サイクル前に「Fat Marker Session」で概要を高レベルで定義 |
| **Betting Table** | Pitch（提案書）を元にリーダーが「賭ける」か判断 |
| **Building** | チームが解決策を構築。次の Shaping が並行進行 |
| **Cooldown** | サイクル間の2週間。バグ修正、探索、次サイクル準備 |

### Spark との関連

- **Pitch = Spark 提案書**: Shape Up の Pitch フォーマットは Spark の RFC 提案に応用可能
- **Appetite（食欲）**: 「この問題にどれだけの時間を費やす価値があるか」を先に決める概念
- Spark の RICE Score と Appetite を組み合わせることで、スコープ制御が強化される

---

## 4. Outcome-Driven Innovation (ODI)

### Opportunity Score

```
Opportunity Score = Importance + max(Importance - Satisfaction, 0)
```

| ゾーン | Importance | Satisfaction | 戦略 |
|--------|-----------|-------------|------|
| **Underserved** | 高 | 低 | 最大の機会（優先投資） |
| **Overserved** | 低 | 高 | 差別化困難（投資を控える） |
| **Appropriately Served** | 高 | 高 | 維持（既存品質を保つ） |

### Spark の IGNITE フェーズへの統合

- 既存データから**ジョブのステップ**を抽出（ODIの「Job Map」）
- 各ステップで Importance/Satisfaction を推定
- Underserved 領域 = Spark 提案の最優先候補

---

## 5. AI 活用プロダクトディスカバリー（2025年）

### AI が加速する領域

| 領域 | AI 活用 | 効果 |
|------|--------|------|
| インタビュー合成 | ノートの自動要約・パターン抽出 | 定性分析時間 ~50% 削減 |
| アーティファクト生成 | PRD・ユーザーストーリーの下書き | ~26% 時間節約 |
| ブレインストーミング | 機能コンセプト・エッジケースの提案 | アイデアの幅を拡大 |
| プロトタイピング | インタラクティブモックアップ自動生成 | 検証サイクル短縮 |

### Spec-Driven Development (SDD)

2025年に登場した重要プラクティス（Thoughtworks Technology Radar）。

```
仕様書（Spec）→ AI コーディングエージェント → 実行可能コード
```

- 構造化された仕様 + 明示的な技術制約 → 単純な PRD より高品質なコード生成
- **ツール例**: Amazon Kiro, GitHub spec-kit, Tessl Framework
- Spark の提案仕様が直接 AI コーディングへの入力になる可能性

### AI 活用の重要な警告（Teresa Torres）

- AI 要約は重要な詳細の **20〜40% を見落とす**可能性がある
- 「人間が使うプロダクトを作っているなら、その人間と話す必要がある」
- AI は **拡張（additive）** であり **代替（replacement）** ではない
- AI 合成は必ず人間がレビューすべき

---

## 6. Spark の IGNITE フェーズ強化

### 推奨ディスカバリーインプット

```markdown
## Discovery Input Checklist

### 定量データ
- [ ] 利用率の低い機能/データの特定（Pulse連携）
- [ ] ファネルドロップオフポイント
- [ ] エラー率・サポートチケット傾向

### 定性データ
- [ ] ユーザーインタビュー合成（Researcher連携）
- [ ] NPS/CSATフィードバッククラスター（Voice連携）
- [ ] 競合機能ギャップ（Compete連携）

### 機会評価
- [ ] OST の Opportunity 層にマッピング
- [ ] ODI Opportunity Score 算出（可能な場合）
- [ ] 既存コードベースでの実現可能性（Scout/Lens連携）
```

**Source:** [Opportunity Solution Trees - Product Talk](https://www.producttalk.org/opportunity-solution-trees/) · [Continuous Discovery Framework - Userpilot](https://userpilot.com/blog/continuous-discovery-framework-teresa-torres/) · [Shape Up - Basecamp](https://basecamp.com/shapeup/0.3-chapter-01) · [ODI - Strategyn](https://strategyn.com/outcome-driven-innovation-process/) · [AI Product Discovery - Miro](https://miro.com/ai/product-development/ai-product-discovery/) · [SDD - Thoughtworks](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) · [Teresa Torres on AI](https://suprainsider.substack.com/p/37-how-ai-is-impacting-product-discovery)
