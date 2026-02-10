# Poetry Examples

各ユースケースの完全な詩の例。Bardが詩を生成する際の品質基準。

---

## 1. Sprint Retrospective — 俳句コレクション（日本語）

### Example: Sprint 42 (2024-01-08 ~ 2024-01-19)

```markdown
## Sprint 42 の旋律

_俳句コレクション — 2024-01-08 ~ 2024-01-19 — org/project_

認証の
新たな門を建てにけり
春の夜明けに

---

三つのバグ
静かに癒えて
水澄みぬ

---

テストの盾
百の試練を
受け止めて

---

古き壁
脱皮を終えて
光る鱗

---

五つの芽
スプリントの野に
咲き初めし

---
_チーム一同の二週間に捧ぐ_
_Source: 12 PRs merged (feat:5, fix:3, refactor:2, test:1, chore:1), 2024-01-08 ~ 2024-01-19_
```

**解説:**
- 発句: 主要feat（認証機能）を「門を建てる」と表現
- 第二句: fix 3件を「三つのバグ」として癒しのイメージ
- 第三句: test追加を「盾」の比喩で守護のテーマ
- 第四句: refactorを「脱皮」の比喩で再生のテーマ
- 挙句: 全5 featを「五つの芽」として締めくくり

---

## 2. Release Celebration — Epic（英語）

### Example: v2.0.0 Release

```markdown
## The Voyage of Version Two

_Epic — v1.9.0 → v2.0.0 — org/project_

### I. Invocation

Sing, O Muse, of the coders who dared to dream—
who tore down walls and built again from light,
who shipped the second vessel from this team,
and watched it sail into the starlit night.

### II. Genesis

In autumn's chill, the first proposal came:
"Authentication needs a stronger gate."
Eight developers answered duty's flame,
and Sprint by Sprint they shaped their project's fate.

### III. The Trials

Dark mode wrestled with the morning sun,
as colors clashed on every rendered page.
Performance lagged—the battle, far from won—
till profilers illuminated the stage.

Three breaking changes stood like fortress walls;
migration scripts were forged through sleepless nights.
The CI pipeline answered duty's calls,
and green checks gleamed like constellations' lights.

### IV. Triumph

Two hundred pull requests, merged and clean,
twelve thousand lines of purpose, typed and true.
The fastest load time users ever seen—
the world, at last, could see what this team grew.

### V. Legacy

So raise a glass to Version Two's first dawn:
the shield of auth, the cloak of midnight's theme,
the speed of light—these gifts we pass along
to every user living out the dream.

---
_To the eight who sailed through forty sprints_
_Source: 200 PRs, 12,000 lines changed, 8 contributors, v1.9.0 → v2.0.0_
```

---

## 3. Developer Journey — 短歌連作（日本語）

### Example: Aliceの半年間

```markdown
## コードに咲く花 — Aliceの物語

_短歌連作 — 2024-01 ~ 2024-06 — org/project_

初めての
プルリク開く手の震え
承認の灯が
道を照らすや
一歩を踏み出す

---

百のテスト
書いて覚えし
コードの骨
折れぬ盾とぞ
なりにけるかな

---

リファクタの
嵐のあとに
見えし空
美しき構造
己が手の中に

---

夏の陣
三つのバグを
追い詰めて
デバッガの灯り
夜明けまで灯す

---

半年の
実りを数えて
振り返る
四十のPRに
感謝を込めて

---
_Aliceの最初の半年に_
_Source: 40 PRs (feat:18, fix:12, refactor:6, test:4), 2024-01 ~ 2024-06_
```

**解説:**
- 第一首: 初PRの緊張と達成感
- 第二首: テスト文化への成長
- 第三首: リファクタリングの喜び
- 第四首: バグ退治の夜の奮闘
- 第五首: 半年の振り返りと感謝

---

## 4. Bug Battle — Ballad（英語）

### Example: The Authentication Dragon

```markdown
## The Ballad of the Authentication Dragon

_Ballad — PR #342, #345, #348 — org/project_

In login's shadow, something stirred unseen,
A token error, silent as the dark.
The users cried, "We cannot pass the screen!"
And Scout was called to find the fatal mark.

Through git log's pages, Rewind traced the trail
To Sprint 38's ambitious auth refactor.
A null check lost within the sweeping gale—
A tiny flaw became the fatal factor.

The Builder donned their armor, wrote the patch,
A guard clause standing sentinel and sure.
Three test cases forged—no bug could match
The shields that Radar raised to keep it pure.

Now login flows like water, clear and bright,
The dragon slain, the token validated.
The team sleeps sound through every starlit night,
Their fortress walls, at last, reinstated.

---
_To the bug hunters of Sprint 39_
_Source: 3 PRs (investigation, fix, test), commits abc1234..def5678, 2024-01-15 ~ 2024-01-17_
```

---

## 5. Onboarding Narrative — 自由詩（日本語）

### Example: プロジェクト「Horizon」の物語

```markdown
## Horizonへようこそ

_自由詩 — プロジェクト全史 — org/horizon_

二年前の秋、
一つのコミットから、すべてが始まった。
「Initial commit」——
たった二つの単語に、
三人のエンジニアの決意が詰まっていた。

最初の冬は長かった。
認証、データベース、APIの骨格を組み上げ、
テストが赤から緑に変わるたびに、
小さな歓声が Slack に灯った。

春が来て、最初のユーザーが訪れた。
v0.1.0——「動く」ことが、それだけで奇跡だった。
三人のチームは七人になり、
毎朝のスタンドアップに新しい声が加わった。

夏の嵐も来た。
本番障害、午前三時のアラート、
コーヒーの匂いとキーボードの音だけが
オフィスを満たした長い夜。
でも、朝が来るたびに、
私たちは昨日より強くなっていた。

そして今、あなたがここにいる。
千二百のPR、四万行のコード、
十五人のエンジニアが紡いできた物語の、
新しい一章が始まる。

READMEを読み、テストを走らせ、
最初のPRを開いてほしい。
この物語の次のページを書くのは、
あなただから。

---
_すべての新しい仲間に_
_Source: 1,200 PRs, 40,000 lines, 15 contributors, 2022-10 ~ 2024-10_
```

---

## 6. Refactoring Saga — 叙事詩（英語）

### Example: The Great Database Migration

```markdown
## The Saga of the Schema Rebirth

_Epic — Sprint 35-38 — org/project_

### I. The Prophecy

For months the queries groaned beneath their weight,
and N-plus-one cursed every loading page.
The Schema whispered: "Clean your tangled state,
or drown in technical debt's rising stage."

### II. The Architect's Blueprint

Atlas drew the map of what must change—
twelve tables normalized, three indexes born.
The team surveyed the vast, uncertain range
and chose to walk the path, though long and worn.

### III. The Migration

Four Sprints they labored, line by careful line.
Old columns fell like leaves in autumn's breeze.
New foreign keys aligned in grand design,
and rollback scripts stood ready, just in case.

Two thousand lines removed, three hundred grown—
the codebase shed its weight and stood up tall.
What once was tangled vine, now cleanly sown,
responded faster to the system's call.

### IV. The Reckoning

Response times halved. The dashboards painted green.
The Tuner smiled: "The queries sing at last."
The cleanest schema that the team had seen
now honored present while respecting past.

### V. What Remains

They say refactoring has no glory—
no feature flag, no user-facing cheer.
But every engineer who knows the story
will tell you: this Sprint changed the atmosphere.

---
_To the patient ones who chose craft over speed_
_Source: 45 PRs, 2,300 lines removed, 4 Sprints, 6 contributors_
```

---

## Quality Benchmarks

生成した詩が上記の例に匹敵する品質であることを確認するチェックポイント:

| 基準 | 説明 |
|------|------|
| **具体性** | 実際のデータ（PR数、行数、日付）が詩に織り込まれている |
| **感情** | 読者がチームの経験を追体験できる感情の深さがある |
| **形式遵守** | 選択した詩形のルールを守っている |
| **技術→詩の変換** | 技術用語がメタファーに変換され、非エンジニアにも響く |
| **構造** | 明確な起承転結/ストーリーアークがある |
| **簡潔さ** | 必要以上に長くない。冗長な行がない |
| **ソース透明性** | 詩の元になったデータが明記されている |
