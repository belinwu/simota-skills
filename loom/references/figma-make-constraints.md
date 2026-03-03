# Figma Make Constraints

Figma Make の既知制約、挙動上の quirks、および回避パターン集。プロンプト設計と Guidelines.md 生成時に参照。

---

## Auto Layout Constraints

| Constraint | Detail | Workaround |
|-----------|--------|------------|
| **ネスト深度** | 4階層以上のネストされた Auto Layout は正しく推論されない場合がある | 3階層以下に制約。深い構造は分割生成→後で統合 |
| **Mixed direction** | 同一フレーム内の水平・垂直混在指定が不安定 | 方向ごとにフレームを分離し、明示的に `direction: HORIZONTAL` / `VERTICAL` を指定 |
| **Space between** | `Space between` モードの間隔計算が期待通りにならない場合がある | 固定 `gap` 値を明示的に指定し、`Space between` は避ける |
| **Absolute position** | AL 内の absolute 配置が無視されることがある | absolute 要素は別レイヤーとして分離するか、position 情報をプロンプトに明記 |
| **Padding asymmetry** | 上下左右の個別 padding 指定が一律になる場合がある | `padding: 16 24 16 24` のように具体的な4方向値をプロンプトに記述 |

### Recommendation Template

```
Auto Layout: Vertical, gap: 16px, padding: 24px 32px
  ├── Header row: Horizontal, gap: 8px, align: center
  ├── Content area: Vertical, gap: 12px
  └── Footer: Horizontal, gap: 16px, justify: space-between
```

---

## Token & Variable Reference

| Constraint | Detail | Workaround |
|-----------|--------|------------|
| **Variable name resolution** | Guidelines に書いた Variable 名が正確にマッピングされないことがある | 正確な Variable パスを記述（例: `color/primary/500` ではなく `Primitives/color/primary/500`） |
| **Alias chain** | Variable alias（参照チェーン）が途切れることがある | Guidelines にプリミティブ値とエイリアス両方を記載し、フォールバックを確保 |
| **Mode switching** | Light/Dark モードの Variable 切り替えが不完全 | Guidelines にモード別の値テーブルを含め、デフォルトモードを明示 |
| **Numeric tokens** | spacing / sizing の数値トークンが無視されハードコード値になる場合 | トークン名に加えて `(= 16px)` のように実値も括弧内に記載 |

### Variable Reference Template

```markdown
## Color Tokens
| Token | Light Mode | Dark Mode | Usage |
|-------|-----------|-----------|-------|
| `color/primary/500` | #3B82F6 | #60A5FA | Primary actions, links |
| `color/neutral/100` | #F3F4F6 | #1F2937 | Surface backgrounds |

Always use the Variable name, NOT the hex value directly.
```

---

## Component Generation

| Constraint | Detail | Workaround |
|-----------|--------|------------|
| **Variant limit** | 5+ variants のコンポーネントは品質が低下しやすい | 3-4 variants ずつに分割生成し、後でコンポーネントセットとして統合 |
| **Boolean property** | Boolean prop が正しく設定されないことがある | `hasIcon: true/false` のように明示的にBooleanプロパティ名と値を列挙 |
| **Instance swap** | Instance swap slot が設定されない | slot 候補のコンポーネント名を明示的にリストアップ |
| **Default variant** | デフォルト variant の選択が意図と異なる場合 | `Default variant: size=medium, style=primary` と明記 |
| **Nested components** | 子コンポーネントの props がフラット化される | 子コンポーネントを先に独立生成し、親コンポーネントで参照 |

### Component Definition Template

```
## Button Component
Variants:
  - size: [small, medium, large] (default: medium)
  - style: [primary, secondary, ghost] (default: primary)
  - state: [default, hover, disabled] (default: default)
Properties:
  - label: text (required)
  - hasIcon: boolean (default: false)
  - iconPosition: [left, right] (default: left, visible when hasIcon=true)
```

---

## Layout & Responsive

| Constraint | Detail | Workaround |
|-----------|--------|------------|
| **Min/Max width** | Min/Max width 制約の自動設定が不安定 | 具体的な px 値を明記（例: `min-width: 320px, max-width: 1440px`） |
| **Breakpoint behavior** | レスポンシブ breakpoint に基づくレイアウト変更が困難 | デスクトップ版を主として生成し、モバイル版は別プロンプトで生成 |
| **Fill container** | `Fill container` 指定が無視されることがある | `width: Fill container (100% of parent)` と括弧内で明示 |
| **Fixed vs Hug** | Fixed / Hug contents の区別が曖昧になる場合 | 各要素に `sizing: Fixed(200px)` or `sizing: Hug` を明記 |

---

## Naming & Structure

| Constraint | Detail | Workaround |
|-----------|--------|------------|
| **Layer naming** | 生成されたレイヤー名が `Frame 1`, `Rectangle 2` 等の汎用名になる | Guidelines の命名規約セクションに命名ルールを明記し、サンプルを示す |
| **Page structure** | 複数ページ構成が無視され1ページに集約される場合 | 1プロンプトで1ページ分を生成する分割戦略を採用 |
| **Group vs Frame** | Frame であるべき箇所が Group になる | 「Group ではなく Frame を使用すること」を Guidelines に明記 |

### Naming Convention Template

```markdown
## Layer Naming Rules
- Frames: kebab-case (e.g., `header-nav`, `card-container`)
- Text layers: content description (e.g., `title-text`, `price-label`)
- Icons: `icon-{name}` (e.g., `icon-search`, `icon-close`)
- Images: `img-{description}` (e.g., `img-hero`, `img-avatar`)
- NEVER use default names like "Frame 1" or "Rectangle 2"
```

---

## Prompt Complexity Limits

| Screen Count | Reliability | Strategy |
|-------------|-------------|----------|
| **1 screen** | High (90%+) | Single prompt with full detail |
| **2-3 screens** | Good (80%+) | Sequential prompts, shared Guidelines |
| **4-7 screens** | Moderate (65%+) | Component-first → Assembly pattern |
| **8-15 screens** | Variable (50-70%) | System → Pattern → Screen → Polish |
| **15+ screens** | Low (<50%) | Module decomposition, ask first |

### Key Insight

> Figma Make の品質は **プロンプト粒度に反比例して向上する**。1つのプロンプトで多くを求めるほど品質が低下する。「少なく、具体的に」が原則。

---

## Known Quirks

| Quirk | Description | Mitigation |
|-------|-------------|------------|
| **Shadow rendering** | Drop shadow の spread / blur 値が微妙にずれる | 具体的な `x: 0, y: 4, blur: 12, spread: 0, color: rgba(0,0,0,0.1)` で指定 |
| **Border radius** | 大きな border-radius が適用されない場合がある | `border-radius: 12px` と具体値 + 「角を丸くする」の自然言語を併用 |
| **Text truncation** | テキスト truncation（...）設定が正しく適用されない | `text-overflow: ellipsis, max-lines: 2` を明示 |
| **Icon sizing** | アイコンサイズが意図と異なる場合がある | `24x24px, constraints: Scale` と寸法+制約モードを明記 |
| **Color opacity** | opacity が正確に反映されない | rgba 形式で指定（hex + opacity 分離を避ける） |

---

## Constraint-Aware Prompt Checklist

Guidelines.md やプロンプト作成時、以下の制約を考慮しているか確認：

- [ ] Auto Layout のネスト深度が3以下に制限されている
- [ ] Variable 名がフルパスで記述されている
- [ ] 各コンポーネントの variants が4以下に分割されている
- [ ] Min/Max width が具体的な px 値で指定されている
- [ ] レイヤー命名規約がサンプル付きで含まれている
- [ ] 1プロンプトの対象が1-2画面に収まっている
- [ ] Fixed / Hug / Fill の sizing モードが明示されている
- [ ] shadow / border-radius は具体的な数値で指定されている
- [ ] Light/Dark モードの Variable 値テーブルが含まれている
- [ ] Group ではなく Frame を使用する旨が明記されている
