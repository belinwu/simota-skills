# Realm Directory Data

Agent ecosystem 紹介ディレクトリサイトのデータ層。JSON Schema (Draft 2020-12) 準拠の
スキーマ定義 + taxonomy (マスターデータ) + agent fixture で構成。SSG / 検索 /
プレビューのいずれも、このディレクトリを単一ソースとして読み取る。

---

## ディレクトリ構造

```
assets/data/
├── schema/              # JSON Schema Draft 2020-12 定義(検証用)
│   ├── agent.schema.json
│   ├── class.schema.json
│   ├── category.schema.json
│   ├── rank.schema.json
│   └── affinity.schema.json
├── taxonomy/            # マスターデータ(変動少 / 真実のソース)
│   ├── classes.json     # 21 class
│   ├── categories.json  # 21 category
│   ├── ranks.json       # 8 rank tiers
│   └── affinities.json  # project affinity 6 種
├── agents/              # 個別 agent fixture(編集はここ)
│   ├── vision.json
│   ├── flow.json
│   └── ... (30 体)
├── agents.index.json    # 全 agent をフラット配列に統合(SSG / 検索の主)
└── README.md            # このファイル
```

---

## 設計原則

### 1. 単一ソースは個別ファイル、配信は index

- **編集**は `agents/{name}.json` で行う(1 agent = 1 file)。
- **SSG / 検索**は `agents.index.json` を読む。index は個別ファイルの統合キャッシュ。
- 一貫性は更新フロー(後述)で担保する。

### 2. 参照は ID(slug)、表示は taxonomy

- agent fixture が持つ `class` / `category` / `affinity[].project` / `rank.tier` は
  すべて slug の **FK**。表示用 label / archetype / badge color などは taxonomy が真実のソース。
- これにより 30 → 135 体スケール時も agent fixture を触るだけで済み、リネームは
  taxonomy 一箇所で完了する。

### 3. 双方向 relation の整合

- `taxonomy/classes.json` の `classes[].members[]` と
  `taxonomy/categories.json` の `categories[].classes[]` は双方向。
- 個別 agent は class.members[] に slug が含まれる必要がある(更新フロー §B 参照)。

### 4. cold-start 安全

- `rank: null` と `badges: []` は schema 上常にフィールドが存在(クライアント側の
  optional チェック不要)。XP データが揃うまで `null` のまま。

### 5. portrait 画像は遅延差し替え

- `portrait.src` は `../portraits/{slug}.png` を指す相対パス(agents/ ディレクトリ起点)。
- 画像未生成のあいだは `portrait.status: "pending"`。Sketch が画像を生成したら
  `portraits/{slug}.png` を配置し、`status: "generated"` に変更するだけ。
- 画像のコミットと fixture 更新を同 PR にしておくと、レビューがしやすい。

---

## スキーマ概要

| Schema | $id | 主な責務 |
|---|---|---|
| `agent.schema.json` | `https://realm.local/schema/agent.schema.json` | 個別 agent エントリ。FK で taxonomy を参照 |
| `class.schema.json` | `https://realm.local/schema/class.schema.json` | 21 class マスター。members[] / synergies[] |
| `category.schema.json` | `https://realm.local/schema/category.schema.json` | 21 category マスター。classes[] |
| `rank.schema.json` | `https://realm.local/schema/rank.schema.json` | 8 tier rank。XP 閾値 + Badge Color (Light/Dark) |
| `affinity.schema.json` | `https://realm.local/schema/affinity.schema.json` | project affinity 6 種。icon symbol descriptor |

参照規則:

- agent.class → class.id
- agent.category → category.id
- agent.affinity[].project → affinity.id
- agent.rank.tier → rank.id (enum: F/E/D/C/B/A/S/SS)
- class.members[] ↔ agent.class(双方向)
- class.category ↔ category.classes[](双方向)

循環参照は無し。schema は taxonomy だけが指す(agent は schema を直接 import しない)。

---

## 更新フロー

### A. 新 agent を追加する

1. `agents/{name}.json` を作成(`agent.schema.json` で validate)。
2. `taxonomy/classes.json` の対応 class の `members[]` に `name` を追加。
3. `agents.index.json` の末尾に同じレコードを追加(または再生成スクリプト実行)。
4. PR に schema validation の CI 結果を添付。

### B. 既存 agent を編集する

1. `agents/{name}.json` を更新。
2. `agents.index.json` の対応エントリも同期更新(差分が大きいときは index 全体を再生成)。
3. capabilities / collaboration の意味が変わるなら taxonomy 側に影響しないか確認。

### C. taxonomy を編集する(class / category / rank / affinity)

1. `taxonomy/{file}.json` を更新。
2. 影響する agent の FK 値が変わるなら、`agents/*.json` を全件 grep + 一括置換。
3. `agents.index.json` を再生成。
4. portrait の variant に影響する場合は Sketch 側 prompt を再生成。

### D. portrait 画像を差し替える

1. Sketch (Realm の portrait Recipe) で画像生成。
2. `assets/portraits/{slug}.png` に配置(720×720 以上、1:1 / 3:4 / 2:3 は variant に応じる)。
3. `agents/{slug}.json` の `portrait.status` を `"pending"` → `"generated"` に変更。
4. SSG ビルドで生成画像が反映される。

---

## バリデーション

JSON Schema は AJV (Node) / `check-jsonschema` (Python) のどちらでも検証可能。

```bash
# AJV の例
npx ajv validate -s schema/agent.schema.json -d "agents/*.json" --spec=draft2020

# 統合 index 検証
npx ajv validate -s schema/agent.schema.json -d agents.index.json --spec=draft2020 \
  --all-errors --strict=false
```

CI (推奨) では以下を順に走らせる:

1. **Schema validation** — 5 schema 自身の self-check + 全 fixture の検証。
2. **Reference integrity** — `class` / `category` / `affinity[].project` / `rank.tier` が
   taxonomy に存在することを確認。
3. **Bidirectional relation check** — class.members[] と agent.class が一致することを確認。
4. **Index consistency** — `agents.index.json` の各エントリが `agents/{name}.json` と
   キーで一致することを確認(`name` を join key)。

---

## スケールアップ計画(30 → 135)

- agent 数増加で fixture サイズが線形に増えるが、index は単純 concat なのでビルド時間は
  問題にならない。
- class / category は固定(21 種)。新規 archetype が必要なら taxonomy に
  追加してから agent を増やす。
- 検索が重くなったら、index を `agents.index.lite.json`(name / class / category /
  description / tagline のみ)と `agents.index.full.json` に分割し、検索バーは lite を
  使うようにする。
- portrait 画像は WebP + sharp で最適化する。30 体 × 720px ≈ 数 MB なので CDN キャッシュで
  十分。135 体になっても 30 MB 未満。

---

## ファイル間依存関係

```
agents.index.json  ──┐
                     ├──→ schema/agent.schema.json
agents/*.json     ──┘            │
                                 │ (FK)
                                 ▼
              taxonomy/classes.json ──→ schema/class.schema.json
              taxonomy/categories.json ──→ schema/category.schema.json
              taxonomy/ranks.json ──→ schema/rank.schema.json
              taxonomy/affinities.json ──→ schema/affinity.schema.json
```

すべての relation は ID 経由。display 文字列の重複は agent 側にあえて持たせており
(`archetype` / `department`)、SSG が taxonomy 結合をスキップしてもそのまま表示できる。
リネーム時は taxonomy が正で、再ビルド時に agent 側を上書きする想定。

---

## 既知の TODO

- `#TODO(agent): badge-catalog.md` に基づく `taxonomy/badges.json` 追加(現在 badges[] は
  自由記述)。
- `#TODO(agent): synergy 完全展開`(現在 commander のみ。残り 20 class)。
- `#TODO(agent): portrait 画像生成パイプライン`(Sketch との CI 接続)。
