# 仕様キャリブレーションシステム (UNIFY)

テンプレート効果追跡、クロスチーム整合度スコアリング、セクション活用度分析、仕様品質の継続改善。
Accordは仕様の成果から学び、より効果的な統合仕様を作成できるようになる。

---

## 概要

UNIFYフェーズは各仕様タスク完了後（または定期的に）実行し、仕様作成と実際のチーム間整合度の間のフィードバックループを閉じる。UNIFYなしではテンプレート選択が静的なままで、対象者別の記述パターンも未調整のまま。UNIFYにより、Accordの仕様は3チーム全員の整合に対して漸進的に効果的になる。

**実行主体:** Accord自身がDELIVERフェーズ直後に実行
**記録先:** `.agents/accord.md`（Journalセクション）
**評価タイミング:** 3仕様蓄積ごと、または四半期ごとのいずれか早い方

```
RECORD ──→ EVALUATE ──→ CALIBRATE ──→ PROPAGATE
  │            │            │            │
  │ Log       │ Measure    │ Update    │ Share with
  │ specs &   │ alignment  │ template  │ Lore
  │ outcomes  │ & usage    │ weights   │
```

---

## RECORD — 仕様活動ログ

各仕様タスク完了後、Accordが`.agents/accord.md`に以下を記録:

```yaml
Spec: [spec-id]
Scope: [Full | Standard | Lite]
Feature_Complexity: [High | Medium | Low]
Teams_Involved: [Biz+Dev+Design | Biz+Dev | Dev+Design | Biz+Design | Single]
Requirements_Count: [total REQ IDs]
BDD_Scenarios_Count: [total AC IDs]
Sections_Used:
  L0: [yes/no]
  L1: [yes/no]
  L2_Biz: [yes/no]
  L2_Dev: [yes/no]
  L2_Design: [yes/no]
  L3: [yes/no]
Traceability_Completeness: [0-100%]
Cross_Team_Alignment:
  biz_understanding: [High/Medium/Low]
  dev_understanding: [High/Medium/Low]
  design_understanding: [High/Medium/Low]
Revisions_Required: [count]
Downstream_Handoff: [Sherpa/Builder/Radar/Voyager/Canvas/None]
```

### 追跡項目

| データポイント | 理由 | 用途 |
|-------------|------|------|
| スコープ×複雑度の適合 | 適切なスコープが選択されたか？ | スコープ選択ヒューリスティクスの改善 |
| セクション活用度 | どのL2セクションが最も/最も使われないか？ | テンプレートの合理化 |
| クロスチーム整合度 | 全チームが仕様を理解したか？ | 記述パターンの改善 |
| 修正頻度 | 承認までの修正ラウンド数 | 初期品質の改善 |
| BDDカバレッジ | 受入基準は十分か？ | BDDガイダンスの調整 |
| 下流採用度 | Builder/Radarが仕様を直接使用したか？ | 出力フォーマットの改善 |

---

## EVALUATE — 仕様インパクト測定

### クロスチーム整合度スコア

```
Alignment = (Biz_Understanding + Dev_Understanding + Design_Understanding) / 3

High (all 3 High)  = Excellent specification (template is working)
Medium (mixed)     = Moderate alignment (review writing patterns, section coverage)
Low (any 1 Low)    = Weak specification (investigate root cause per team)
```

### スコープ精度追跡

```
Scope Accuracy = Specs Where Selected Scope Was Sufficient / Total Specs

> 0.85  = Good scope selection heuristic
0.70-0.85 = Some over/under-scoping
< 0.70  = Review complexity indicators
```

### 評価トリガー

| トリガー | チェック内容 |
|---------|------------|
| 仕様納品後にチームが明確化を要求 | 記述の明瞭性、対象者適合度 |
| 仕様が3回以上の修正を要求 | スコープ選択、セクション完全性 |
| Builder/Radarが仕様を直接使用できない | 出力フォーマット、詳細レベル |
| 仕様と実装にギャップが発生 | 要件の完全性、BDDカバレッジ |
| 四半期レビュー | 仕様全体の有効性 |

### 期間評価サマリー

```markdown
### 仕様評価

| Metric | Value | Trend |
|--------|-------|-------|
| Specs created | 10 | — |
| Scope accuracy | 80% | ↑ |
| Average alignment score | High | — |
| Average revisions | 1.5 | ↓ |
| BDD coverage (Must REQs) | 95% | ↑ |
| Downstream adoption | 90% | — |
| Traceability completeness | 88% | ↑ |

**Strongest pattern**: Standard scope for 2-team features (100% alignment)
**Weakest area**: L2-Design section (often under-specified)
**Note**: BDD scenarios reduced implementation gaps by 35%.
```

---

## CALIBRATE — 仕様ヒューリスティクスの更新

### スコープ選択キャリブレーション

複雑度ごとの最適スコープを追跡:

```yaml
# Default scope by complexity
scope_selection:
  high_complexity: Full    # 0.90
  medium_complexity: Standard  # 0.85
  low_complexity: Lite     # 0.90

# Calibrated (from UNIFY data)
# Example: Medium complexity with 3 teams benefits from Full
scope_selection:
  medium_complexity_3_teams: Standard → Full  # 3-team projects need more detail
```

### セクション効果スコア

各セクションがチーム間整合にどれだけ寄与するかを追跡する:

```yaml
section_effectiveness:
  L0_vision: 0.95        # ほぼ常に有用 — 全チームの共通理解の起点（根拠: 仕様テンプレート設計のベストプラクティス）
  L1_requirements: 0.95  # コア — 全スコープで必須（根拠: 要件なしに仕様は成立しない）
  L2_biz: 0.80          # ステークホルダー合意に有用（根拠: 保守的初期値、Bizチーム不参加のケースを考慮）
  L2_dev: 0.90          # 実装に不可欠（根拠: Builder/Radarの下流採用に直結）
  L2_design: 0.75       # 活用度に改善余地あり（根拠: Vision/Paletteとの境界で記述が不足しがち、保守的初期値）
  L3_bdd: 0.90          # 共通理解へのインパクト大（根拠: Given-When-Then形式の普遍的な合意形成力）
  L3_traceability: 0.70 # Standard/Liteで省略されがち（根拠: 保守的初期値、省略時の品質影響を観察中）
```

**初期値設定方針:** 実運用データがないため保守的な値を設定。0.95 = ほぼ必須のコアセクション、0.90 = 高インパクト、0.80 = 中インパクト、0.75/0.70 = 改善余地あり（上方修正を期待）。3仕様蓄積後に実データで再調整。

### キャリブレーションルール

1. **3仕様以上の蓄積が必要** — ヒューリスティクス調整の前提条件
2. **サイクルあたりの最大調整幅**: ±0.15（過修正の防止）
3. **減衰**: 調整値は四半期ごとにデフォルトに向けて10%減衰
4. **上書き**: ユーザーの明示的な設定が常に優先

### 記述パターンキャリブレーション

クロスチーム理解に最も効果的なパターンを追跡:

| パターン | 整合度への影響 | 最適な場面 |
|---------|-------------|----------|
| 問題先行型L0（痛み→解決策） | 非常に高い | 全スコープ |
| L1でのMoSCoW優先度付け | 高い | Standard, Full |
| L2-Designでの視覚的ユーザーフロー | 高い | UI機能 |
| L2-Devでのインラインコード例 | 高い | API機能 |
| BDDで具体的な値を使用（抽象的でなく） | 非常に高い | 全スコープ |
| クロスチーム用語集 | 中～高 | Fullスコープ |

---

## PROPAGATE — 検証済みパターンの共有

### Journal記録フォーマット

UNIFYインサイトを`.agents/accord.md`に記録:

```markdown
## YYYY-MM-DD - UNIFY: [Scope × Teams]

**Specs assessed**: N
**Average alignment**: [High/Medium/Low]
**Key insight**: [description]
**Calibration adjustment**: [scope/pattern: old → new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Accord
date: YYYY-MM-DD
summary: [specification insight]
affects: [Accord, Scribe, Bridge, Lore]
priority: MEDIUM
reusable: true
-->
```

### パターンライブラリ

コンテキスト別の効果的な仕様アプローチを蓄積:

| コンテキスト | 最適スコープ | 主要セクション | 有効性 |
|------------|-----------|-------------|-------|
| 新規プロダクト機能（3チーム） | Full | 全L2 + 完全BDD | 非常に高い |
| API拡張（Dev + Biz） | Standard | L2-Dev + L2-Biz + BDD | 高い |
| UI改善（Design + Dev） | Standard | L2-Design + L2-Dev + BDD | 高い |
| ビジネスインパクトのあるバグ修正 | Lite | L0 compact + 主要BDD | 高い |
| インフラ変更（Devのみ） | Lite | L2-Dev inline + 主要BDD | 中～高 |
| クロスチームプロセス変更 | Full | L2-Biz中心 + L3 BDD | 高い |

### クイックキャリブレーション（小規模タスク）

仕様が3件未満の場合:

```markdown
## Quick UNIFY

**仕様数**: 1件完了
**スコープ**: Standard
**メモ**: L2-DesignセクションにFigmaリンクをインラインで含めると整合度が改善
**アクション**: ウェイト変更なし（データ不足）
```

ルール: 単一の小規模タスクからウェイトを調整しない。タスク横断でデータを蓄積すること。

---

## エコシステムとの統合

UNIFYデータは仕様に関する意思決定にフィードバックされる:

| UNIFYシグナル | エコシステムへの影響 |
|-------------|-------------------|
| 整合度が着実に改善 | テンプレートアプローチが機能している — 継続 |
| 整合度が低下傾向 | 記述パターン・スコープ選択を再検討 |
| セクションが継続的に未使用 | デフォルトテンプレートからの除外を検討 |
| 修正回数が多い | 初期品質改善、事前レビューチェックリスト追加 |
| 下流採用率が低い | 出力フォーマット調整、ハンドオフ品質改善 |
| 仕様パターンが検証済み | Loreに共有、Scribeテンプレート更新 |

---

## エコシステムへのフィードバック

UNIFYが単一タスクを超えて価値のあるパターンを発見した場合:

1. **Journalに記録** — `reusable: true` タグ付き
2. **EVOLUTION_SIGNALを発行** — Loreが収集
3. **Scribeにフィード** — 仕様パターンが個別文書品質を改善する場合
4. **Bridgeに通知** — クロスチーム言語パターンが翻訳品質を改善する場合
5. **テンプレートデフォルトを更新** — 新しい構造パターンがより効果的と証明された場合
