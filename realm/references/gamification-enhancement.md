# Gamification Enhancement Strategies

> Octalysis フレームワーク、リーダーボード設計、エンゲージメント維持メカニクスの改善知見

## 1. Octalysis 8 Core Drives × Realm 適用

Octalysis（Yu-kai Chou開発）: 3,300+学術引用、Google/LEGO/Tesla採用。

| # | Core Drive | 分類 | Realm現状 | 改善提案 |
|---|-----------|------|----------|----------|
| 1 | Epic Meaning & Calling | White Hat | △ Chronicle | エコシステム「物語」強化 |
| 2 | Development & Accomplishment | White Hat | ◎ XP/Rank | マイルストーン演出追加 |
| 3 | Empowerment of Creativity | White Hat | △ 限定的 | カスタムアバター、部門デコレーション |
| 4 | Ownership & Possession | Left Brain | ○ Badge | コレクション完了度表示 |
| 5 | Social Influence & Relatedness | Right Brain | ○ Leaderboard | メンター関係、部門ランキング |
| 6 | Scarcity & Impatience | Black Hat | × 未実装 | 期間限定クエスト、シーズンイベント |
| 7 | Unpredictability & Curiosity | Black Hat | △ 限定的 | ランダムイベント、隠しバッジ |
| 8 | Loss & Avoidance | Black Hat | △ XP減衰 | ストリーク継続プレッシャー |

**改善ポイント:** CD2偏重 → CD1, 3, 6, 7の強化でバランス実現。White Hat（上位CD）は長期エンゲージメント、Black Hat（下位CD）は短期アクション誘発。

**Source:** [Octalysis Framework](https://yukaichou.com/gamification-examples/octalysis-gamification-framework/) · [Understanding Octalysis](https://www.nudgenow.com/blogs/gamification-behavioral-design-octalysis-framework)

---

## 2. リーダーボード設計改善

> "Traditional leaderboards motivate only the top 5-10% but often demoralize others."

| 種類 | 対象 | 効果 |
|------|------|------|
| Global Top 10 | 全エージェント | 上位層を刺激 |
| **Department Ranking** | 部門内 | 小グループ競争（効果大） |
| **Weekly Rising Stars** | 週間XP増加量 | 新規・中位層を刺激 |
| **Streak Champions** | 連続SUCCESS数 | 継続性を報酬 |
| **Synergy Awards** | コラボ回数 | 協力行動を促進 |
| **Personal Best** | 自己記録比較 | 全員がモチベ対象 |

**"Urgent Optimism":** `❌ 56人中43位` → `✅ 次のランクまで350 XP！今週のペースなら4日で到達`

**Source:** [Effective Leaderboards](https://yukaichou.com/advanced-gamification/how-to-design-effective-leaderboards-boosting-motivation-and-engagement/) · [When To Use Leaderboards](https://medium.com/design-bootcamp/gamification-strategy-when-to-use-leaderboards-7bef0cf842e1)

---

## 3. ナラティブ・ダッシュボード

| 要素 | 現状 | 改善後 |
|------|------|--------|
| データ表示 | 統計テーブル | ストーリー形式のプログレスジャーニー |
| マイルストーン | ランクアップのみ | エコシステム全体のタイムライン |
| 予測 | なし | "このペースなら X は来週 Rank A に到達" |
| 回顧 | エラ検出のみ | 月次レトロスペクティブ自動生成 |

**Source:** [From Numbers to Narratives](https://www.conversifytech.com/blog/from-numbers-to-narratives-how-to-tell-a-story-with-gamified-dashboards/)

---

## 4. エンゲージメント維持メカニクス

### シーズンシステム

```
Season 1-4 (各3ヶ月): 限定バッジ + 1.5倍XPクエスト + シーズンランキング(リセット)
```

### ストリーク改善

```
現状: 3+ SUCCESS で ×1.2

改善:  3日 ×1.2 · 7日 ×1.5 + "On Fire" · 14日 ×1.8 + "Unstoppable" · 30日 ×2.0 + "Legend Streak"
保護:  月3回フリーズ可 · PARTIAL でもストリーク維持
```

### デイリー/ウィークリーチャレンジ

| 周期 | チャレンジ例 | XP |
|------|-------------|-----|
| Daily | 1タスク完了 / 2エージェントチェーン参加 | 10-20 |
| Weekly | 5タスク完了 / 3カテゴリ貢献 | 100-150 |
| Monthly | 全部門に1+エージェント参加 | 500 |

---

## 5. チーム・部門エンゲージメント

> セレブレーション演出の実装詳細は `celebration-effects.md` を参照。

### 部門対抗イベント（月次）

- 最多XP部門 → "Department of the Month"
- 最多コラボチェーン部門 → "Unity Award"
- 最多新人育成部門 → "Mentor Department"

### 部門ヘルス可視化改善

| スコア | メタファー |
|--------|-----------|
| S (90+) | Flourishing Garden |
| A (80+) | Healthy Garden |
| B (70+) | Growing Garden |
| C (60+) | Autumn Garden |
| D (50+) | Dry Garden |
| F (<50) | Frozen Garden |

**Source:** [Team Engagement with Gamified Dashboards](https://www.plecto.com/blog/gamification/team-engagement-and-gamification-dashboards/)

---

## 改善優先度サマリー

| 優先度 | 改善項目 | 工数 | Core Drive |
|--------|----------|------|-----------|
| P0 | 多層リーダーボード | 小 | CD5 |
| P0 | セレブレーション演出 | 小 | CD2 (→ celebration-effects.md) |
| P1 | シーズンシステム | 中 | CD6 |
| P1 | ストリーク改善 | 小 | CD8 |
| P1 | Department Challenge | 小 | CD5 |
| P2 | ナラティブダッシュボード | 中 | CD1 |
| P2 | デイリー/ウィークリーチャレンジ | 中 | CD2 |
| P3 | カスタムアバター | 大 | CD3 |
