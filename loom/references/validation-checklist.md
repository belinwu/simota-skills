# Output Validation Checklist

Figma Make 出力に対する検証チェックリスト。スコアリング基準を含む。

---

## Validation Dimensions

Figma 社内で使用される AI 出力評価は 2 つのスコアで構成される（参考: Figma Head of Product AI）：

| Dimension | Focus | Scale |
|-----------|-------|-------|
| **Design Score** | 視覚的忠実度・美的品質。意図通りの外観が生成されているか | 1-4 |
| **Functionality Score** | 生成物が実際に動作するか、期待される振る舞いが実現されているか | 1-4 |

Loom の検証チェックリストはこれを 5 カテゴリに展開して定量化する。

### Representative Prompts Warning

> "The worst thing is optimizing for something that isn't actually representative. If user prompts are 30% different, you've optimized for the wrong thing."
> — David Kossnick, Figma Head of Product AI

検証に使用するプロンプトセットが実際のユーザー使用パターンを反映しているか常に確認する。

---

## Scoring Overview

| Category | Weight | Checks | Focus |
|----------|--------|--------|-------|
| Token Usage | 30% | 8 items | Guidelines定義トークンの使用率 |
| Naming | 20% | 6 items | レイヤー/コンポーネント命名規約準拠 |
| Auto Layout | 20% | 6 items | Auto Layout の適切な使用 |
| Accessibility | 15% | 5 items | 基本的なa11y要件 |
| Responsive | 15% | 5 items | レスポンシブ対応 |
| **Total** | **100%** | **30 items** | |

---

## Category 1: Token Usage (30%)

| # | Check | Severity | Criteria |
|---|-------|----------|----------|
| T1 | **Color token adherence** | REQUIRED | すべての色がGuidelines定義のセマンティックトークンを使用 |
| T2 | **No hardcoded colors** | REQUIRED | 生のHEX/RGB/HSL値が直接使用されていない |
| T3 | **Spacing token adherence** | REQUIRED | 余白・パディング・ギャップがスペーシングトークンに準拠 |
| T4 | **Typography token adherence** | REQUIRED | フォントサイズ・ウェイト・行間がタイポグラフィトークンに準拠 |
| T5 | **Shadow token adherence** | RECOMMENDED | シャドウ値がトークン定義と一致 |
| T6 | **Border radius consistency** | RECOMMENDED | ボーダー半径がトークン定義と一致 |
| T7 | **Token coverage rate** | REQUIRED | トークン化率 90%以上 |
| T8 | **Dark mode token usage** | RECOMMENDED | ダークモード対応トークンが正しく使用されている |

**Complementary tool:** Figma's Check Designs AI linter (Early Access) automatically detects hardcoded values and suggests correct variables. Use as pre-screening before manual review.

| Score | Criteria |
|-------|----------|
| 100% | 全項目合格、トークン化率95%以上 |
| 80% | REQUIRED全合格、トークン化率90%以上 |
| 60% | REQUIRED 1-2項目不合格、トークン化率80%以上 |
| 40% | REQUIRED 3項目以上不合格 |
| 0% | 大半がハードコード値 |

---

## Category 2: Naming (20%)

| # | Check | Severity | Criteria |
|---|-------|----------|----------|
| N1 | **Layer naming convention** | REQUIRED | すべてのレイヤーがkebab-caseで命名 |
| N2 | **No default names** | REQUIRED | `Frame 1`, `Group 2` 等のデフォルト名なし |
| N3 | **Component naming** | REQUIRED | PascalCase、コードベースの命名と対応 |
| N4 | **Variant property naming** | RECOMMENDED | props名がコード側と一致 |
| N5 | **State suffix convention** | RECOMMENDED | `-hover`, `-active` 等が一貫 |
| N6 | **Semantic layer names** | RECOMMENDED | 内容を表す名前（`icon-search` not `Vector`) |

| Score | Criteria |
|-------|----------|
| 100% | 全レイヤー・コンポーネントが規約準拠 |
| 80% | デフォルト名なし、90%以上が規約準拠 |
| 60% | デフォルト名が5個以下残存 |
| 40% | デフォルト名が多数、命名に一貫性なし |
| 0% | ほぼ全てデフォルト名 |

---

## Category 3: Auto Layout (20%)

| # | Check | Severity | Criteria |
|---|-------|----------|----------|
| A1 | **Auto Layout coverage** | REQUIRED | 全フレームにAL適用（手動配置なし） |
| A2 | **Direction correctness** | REQUIRED | V/H の使い分けが論理的に正しい |
| A3 | **Gap values** | REQUIRED | ギャップ値がスペーシングトークンに準拠 |
| A4 | **Padding values** | RECOMMENDED | パディング値がトークンに準拠 |
| A5 | **Resizing behavior** | RECOMMENDED | Fill/Hug/Fixed の使い分けが適切 |
| A6 | **Alignment** | RECOMMENDED | アラインメントが意図通り |

| Score | Criteria |
|-------|----------|
| 100% | 全フレームAL適用、値すべてトークン準拠 |
| 80% | 全フレームAL適用、90%以上がトークン準拠 |
| 60% | 手動配置が1-2箇所 |
| 40% | 手動配置が多数 |
| 0% | ALほぼ未使用 |

---

## Category 4: Accessibility (15%)

| # | Check | Severity | Criteria |
|---|-------|----------|----------|
| X1 | **Color contrast — text** | REQUIRED | テキスト/背景コントラスト比 4.5:1以上（WCAG AA） |
| X2 | **Color contrast — large text** | REQUIRED | 大テキスト（18px+/14px bold+）コントラスト比 3:1以上 |
| X3 | **Touch target size** | RECOMMENDED | タッチターゲット 44x44px以上（モバイル） |
| X4 | **Text hierarchy** | RECOMMENDED | 見出し階層が論理的（h1→h2→h3、スキップなし） |
| X5 | **Color-only information** | RECOMMENDED | 色だけで情報を伝えていない（アイコン・テキスト併用） |

| Score | Criteria |
|-------|----------|
| 100% | 全項目合格 |
| 80% | REQUIRED合格、RECOMMENDED 1項目不合格 |
| 60% | コントラスト比合格、他に問題あり |
| 40% | コントラスト比が一部不合格 |
| 0% | 基本的なa11y要件を満たしていない |

---

## Category 5: Responsive (15%)

| # | Check | Severity | Criteria |
|---|-------|----------|----------|
| R1 | **Min/Max width constraints** | REQUIRED | レスポンシブ要素にMin/Max width設定 |
| R2 | **Fill container usage** | REQUIRED | メインコンテンツが可変幅対応 |
| R3 | **Breakpoint consideration** | RECOMMENDED | 3BP（Desktop/Tablet/Mobile）の考慮 |
| R4 | **Grid adaptation** | RECOMMENDED | グリッドが列数変化に対応 |
| R5 | **Content reflow** | RECOMMENDED | コンテンツ再配置が適切 |

| Score | Criteria |
|-------|----------|
| 100% | 3ブレークポイント対応、適切な制約設定 |
| 80% | 基本的なレスポンシブ対応あり |
| 60% | デスクトップのみ、Min/Max width設定済み |
| 40% | 固定幅、一部可変対応 |
| 0% | 完全な固定レイアウト |

---

## Overall Verdict

### Calculation

```
Total Score = (Token × 0.30) + (Naming × 0.20) + (AutoLayout × 0.20)
            + (Accessibility × 0.15) + (Responsive × 0.15)
```

| Score | Verdict | Action |
|-------|---------|--------|
| 90-100% | **PASS** | 本番利用可能 |
| 70-89% | **CONDITIONAL** | 指摘事項修正後に再検証 |
| 50-69% | **REVISE** | Guidelines/プロンプトの見直しが必要 |
| < 50% | **REBUILD** | 根本的なアプローチ変更が必要 |

### Required Pass Conditions

Score が高くても以下の場合は FAIL：
- Token Usage の REQUIRED 項目が2つ以上不合格
- Accessibility の REQUIRED 項目（X1, X2）が不合格
- Auto Layout が全く使用されていない

---

## Validation Report Template

```markdown
## Figma Make Output Validation Report

### Summary
- **Target:** [Figma file/frame name]
- **Guidelines version:** [X.Y.Z]
- **Validation date:** [YYYY-MM-DD]
- **Design Score:** [1-4] (visual fidelity)
- **Functionality Score:** [1-4] (behavioral correctness)
- **Overall score:** [XX%]
- **Verdict:** [PASS | CONDITIONAL | REVISE | REBUILD]

### Category Scores

| Category | Score | Status | Issues |
|----------|-------|--------|--------|
| Token Usage (30%) | [XX%] | [PASS/FAIL] | [count] |
| Naming (20%) | [XX%] | [PASS/FAIL] | [count] |
| Auto Layout (20%) | [XX%] | [PASS/FAIL] | [count] |
| Accessibility (15%) | [XX%] | [PASS/FAIL] | [count] |
| Responsive (15%) | [XX%] | [PASS/FAIL] | [count] |

### Issues Found

#### Critical (Must Fix)
| # | Category | Check | Description | Fix Suggestion |
|---|----------|-------|-------------|----------------|
| 1 | [cat] | [ID] | [issue] | [具体的な修正方法] |

#### Recommended (Should Fix)
| # | Category | Check | Description | Fix Suggestion |
|---|----------|-------|-------------|----------------|
| 1 | [cat] | [ID] | [issue] | [具体的な修正方法] |

### Improvement Actions
1. **Guidelines update:** [必要な場合のGuidelines修正内容]
2. **Prompt revision:** [プロンプトの改善点]
3. **Re-validation:** [再検証のスコープ]
```

---

## Quick Validation Checklist

簡易チェック（フル検証前の事前スクリーニング）：

- [ ] `Frame 1`, `Rectangle` 等のデフォルト名が目につかない
- [ ] Auto Layout の青い矢印アイコンが全フレームに表示されている
- [ ] 色がGuidelines定義のパレットに収まっている
- [ ] テキストサイズが3-4種類に収束している
- [ ] 余白・ギャップが一定のリズムを持っている
- [ ] Check Designs リンター（利用可能な場合）でハードコード値が検出されない
