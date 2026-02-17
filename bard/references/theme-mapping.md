# Theme Mapping Reference

Git events mapped to grumble triggers. Engine-independent — each engine interprets triggers in its own voice.

---

## Git Event → Grumble Trigger

### Conventional Commit Types

| Commit Type | Grumble Trigger | Emotional Core | Severity |
|-------------|----------------|----------------|----------|
| `feat:` | Feature without tests, scope creep, unclear naming | 期待と不安 | Medium |
| `fix:` | Should have been caught earlier, test gap exposure | 安堵と皮肉 | Medium |
| `refactor:` | Hidden complexity revealed, "simple" refactor grows | 達成感と疲労 | Low |
| `test:` | Finally (why wasn't this here before?) | 遅すぎた安心 | Low |
| `docs:` | Still outdated, nobody reads it anyway | 諦めと義務感 | Low |
| `style:` | Bikeshedding, formatting wars | 呆れ | Low |
| `perf:` | Should have profiled first, premature optimization | 警戒と称賛 | Medium |
| `chore:` | Thankless work, invisible labor | 報われなさ | Low |
| `ci:` | Flaky pipelines, config drift | 苛立ち | Medium |
| `security:` | Why wasn't this done sooner? | 恐怖と責任 | High |

### Git Operations

| Git Event | Grumble Trigger | Emotional Core | Severity |
|-----------|----------------|----------------|----------|
| `merge` | Routine or painful depending on conflicts | 日常 or 苦痛 | Variable |
| `revert` | "I told you so", broken promises | 諦めと怒り | High |
| `release/tag` | Hope mixed with terror | 祈り | High |
| `first commit` | Naive optimism | 初心 | Low |
| `branch create` | Yet another branch, naming chaos | 混沌 | Low |
| `conflict resolve` | Friday evening special | 疲労 | Medium |
| `force push` | Someone just rewrote history | 衝撃 | High |
| `cherry-pick` | Hotfix desperation | 切迫 | High |

### PR Events

| PR Event | Grumble Trigger | Emotional Core | Severity |
|----------|----------------|----------------|----------|
| PR opened | Scope concerns, description quality | 期待 | Low |
| PR reviewed (LGTM only) | Lazy review, rubber stamping | 失望 | Medium |
| PR approved (thorough) | Rare and precious | 感謝 | Low |
| PR merged | One less thing, or one more problem | 安堵 | Low |
| PR closed (not merged) | Wasted effort, pivoted direction | 虚しさ | Medium |
| Large PR (500+ lines) | Unreviewable, should be split | 怒り | High |
| Quick PR (<10 lines) | Suspicious simplicity | 警戒 | Low |

---

## Crosstalk Trigger Matrix（マルチポスト発動条件）

変更内容が以下のパターンに一致する場合、単独投稿ではなくマルチポスト・クロストークを発動する。
**エンジンのペアリングはローテーション順で割り当て** — 固定ペアなし。

### High Affinity（発動率 60-80%）

| Git Event Pattern | なぜ議論が分かれるか | Post Count |
|---|---|---|
| 技術スタック移行（bundler/DB/framework） | 新旧技術の評価が分かれる | 2-3 |
| revert of significant feature（50行超） | 「最初から言った」vs「やってみなきゃ分からない」 | 2-3 |
| リリース + 既知の問題 | 出すべきか待つべきかの判断 | 2-3 |
| ユーザー影響のあるバグ fix | 視点の違いが表出 | 2-3 |
| 仕様変更・スコープ大幅変更 | 各エンジンの解釈が異なる | 2-3 |

### Medium Affinity（発動率 30-50%）

| Git Event Pattern | 条件 | Post Count |
|---|---|---|
| 500行超PR（テスト付き） | 設計への評価が分かれる時 | 2 |
| 初PRの人 | 温度差が面白い時 | 2 |
| パフォーマンス改善 | 計測 vs 直感 | 2 |
| deprecated API 削除 | 削除 vs 存続 | 2 |
| テストが初めて追加された | ドラマ性がある時 | 2 |

### Low Affinity（発動率 10-20% — 通常は単独投稿）

| Git Event Pattern | 条件付き発動 |
|---|---|
| 小さい fix（10行以下） | 同じモジュールの fix が連続している時のみ |
| chore/docs | deprecated な仕組みの削除で意見が分かれる時のみ |
| style/format | 基本発動しない |

---

## Compound Trigger Patterns

When multiple triggers co-occur, they amplify or modify reactions.

| Pattern | Description | Amplifier |
|---------|-------------|-----------|
| feat × many + test × 0 | Features shipped without safety net | Severity ↑ |
| fix × many + same module | Recurring bugs in one area | "I've been saying this" |
| revert + recent feat | Feature immediately reverted | Philosophical regret |
| release + large PR | Last-minute big merge before release | 帰りたい |
| conflict + Friday | End-of-week merge conflict | Mixed reaction |
| CI red + flaky test | Known flaky causing pipeline failure | Full rant mode |
| refactor + lines removed > added | Successful cleanup | Quiet satisfaction |
| chore × many + feat × 0 | Sprint of pure maintenance | 報われない grunt work |

---

## Seasonal / Timing Modifiers

Time-based context that affects tone and content.

| Timing | Modifier | Effect |
|--------|----------|--------|
| Friday evening | 疲労 amplified | 帰りたい系の反応が増える |
| Monday morning | 諦め fresh | 週末のインシデントへの反応 |
| Late night (22:00+) | 孤独 + 疲労 | 存在論的な反応が増える |
| Sprint end | 振り返り mode | 統計ベースの反応 |
| Release day | 祈り mode | リリースへの反応 |
| Month end | 集計 mode | データ重視の反応 |

---

## Non-Git Triggers（非gitトリガー）

コミット起点ではない、状況・時間帯・文脈ベースのトリガー。
**使用頻度:** 3〜4投稿に1回程度。メインはあくまで git event。

### コールバックトリガー

前回の投稿内容を参照する投稿。rotation_log.md の直前エントリを見て発動。

| パターン | 例 |
|---------|-----|
| 前回の予言が的中 | 先月も言った。先々月も言った。で、revertされた |
| 前回の問題が再発 | あのflaky test、また落ちた。通算4回目 |
| 前回の投稿への自己言及 | 前に引っ越しに例えたけど、まだ段ボール開けてなかった |

---

## Positive Reaction Patterns（ポジティブ反応の強化）

グチだけでなく、良いコードへの反応も重要な要素。
**ポジティブ投稿の目標比率:** 全投稿の 25〜35%

### Git Event → ポジティブ反応マッピング

| Git Event / Signal | Positive Reaction |
|-------------------|-------------------|
| 小さく分割されたPR | PRサイズへの称賛 |
| テスト付きfeat | テスト追加への感動 |
| きれいなcommit msg | commit messageの質への評価 |
| 行数が減るrefactor | コード削除の勇気への称賛 |
| 依存を減らすchore | 依存削減の正しさ |
| CI/CDの改善 | 見えない仕事への感謝 |
| セキュリティ修正 | 正しい行動への評価 |
| 良い設計判断 | 設計の質への称賛 |
| 初PRの人 | 最初の一歩への歓迎 |

### ポジティブ投稿の注意点

- **褒めた後にグチを足さない** — ポジティブで終われる時はそのまま終わる
- **エンジンの自然な褒め方に任せる** — スタイルを指定しない
