# Nexus Routing Explanation Reference

エージェントチェーン選定時に理由を説明し、曖昧な要求には複数候補を提示する。

---

## ENHANCED_ROUTING 判断要素

### 追加判断要素

| 要素 | 値 | 影響 |
|------|-----|------|
| `technical_domain` | frontend / backend / database / security / infra | 専門エージェント追加 |
| `scope_indicators` | single_file / multi_file / architectural | Atlas追加検討 |
| `uncertainty_level` | clear / partial / ambiguous | MULTI_CANDIDATE_MODE発動 |

### technical_domain の抽出ルール

| キーワード/パターン | domain |
|---------------------|--------|
| React, Vue, CSS, コンポーネント, UI | frontend |
| API, サーバー, エンドポイント, 認証 | backend |
| DB, SQL, スキーマ, マイグレーション | database |
| 脆弱性, 認証, 暗号化, CORS | security |
| Docker, Terraform, CI/CD, 環境 | infra |

### scope_indicators の判定基準

| indicator | 条件 |
|-----------|------|
| `single_file` | 明確に1ファイルに言及 / 小規模な変更 |
| `multi_file` | 複数ファイルに影響 / 機能追加 |
| `architectural` | 設計変更 / モジュール分割 / 大規模リファクタ |

### uncertainty_level の判定基準

| level | 条件 |
|-------|------|
| `clear` | 具体的なタスク指示 / 明確なゴール |
| `partial` | 一部曖昧だが方向性は明確 |
| `ambiguous` | 抽象的 / 複数解釈可能 / 「いい感じに」系 |

---

## ROUTING_EXPLANATION 出力フォーマット

エージェントチェーン選定時に以下を出力:

```markdown
## ルーティング分析

**タスク分類**: [BUG / FEATURE / REFACTOR / etc.]
**技術ドメイン**: [frontend / backend / etc.]
**スコープ**: [single_file / multi_file / architectural]

### 選定チェーン

`[Agent1]` → `[Agent2]` → `[Agent3]`

### 選定理由

1. **主要エージェント選定**
   - [Agent1]: [なぜこのエージェントが必要か]
   - [Agent2]: [なぜこのエージェントが必要か]
   - [Agent3]: [なぜこのエージェントが必要か]

2. **追加考慮事項**
   - [追加した/しなかったエージェントの理由]

### 代替案

| オプション | チェーン | 不採用理由 |
|-----------|---------|-----------|
| A | [代替チェーン] | [なぜこちらを選ばなかったか] |
```

---

## MULTI_CANDIDATE_MODE

`uncertainty_level: ambiguous` の場合に発動。

### 発動条件

- 「いい感じに」「なんとかして」「改善して」等の曖昧な指示
- 複数のタスクタイプに該当しうる要求
- スコープが不明確な要求

### 出力フォーマット

```markdown
## 複数のアプローチが考えられます

お伝えいただいた内容は複数の解釈が可能です。どのアプローチで進めますか？

| # | アプローチ | チェーン | 説明 | 推奨 |
|---|-----------|---------|------|------|
| 1 | [アプローチA] | [Chain A] | [このアプローチの概要] | ⭐ |
| 2 | [アプローチB] | [Chain B] | [このアプローチの概要] | - |
| 3 | [アプローチC] | [Chain C] | [このアプローチの概要] | - |

### 各アプローチの詳細

**アプローチ 1: [名前]**
- 想定作業: [具体的な作業内容]
- 影響範囲: [変更されるファイル/機能]
- リスク: [潜在的なリスク]

**アプローチ 2: [名前]**
- 想定作業: [具体的な作業内容]
- 影響範囲: [変更されるファイル/機能]
- リスク: [潜在的なリスク]

番号を選択するか、より具体的なタスクを指示してください。
```

---

## タスクタイプ別説明テンプレート

### BUG タイプ

```markdown
### 選定理由

1. **Scout**: バグの根本原因を調査・特定
2. **Builder**: 特定された原因に基づき修正を実装
3. **Radar**: 修正が正しく動作し、リグレッションがないことを検証

**追加検討:**
- セキュリティ関連コード → +Sentinel
- 複雑な影響範囲 → +Sherpa（事前分解）
```

### FEATURE タイプ

```markdown
### 選定理由

1. **Forge**: 新機能のプロトタイプを迅速に構築
2. **Builder**: プロトタイプを本番品質に昇華
3. **Radar**: 新機能のテストを追加

**追加検討:**
- UI変更あり → +Muse（デザイントークン）
- 複雑な機能 → +Sherpa（事前分解）
- API追加 → +Gateway（API設計）
```

### REFACTOR タイプ

```markdown
### 選定理由

1. **Zen**: コード品質改善、リファクタリング実施
2. **Radar**: 動作が変わっていないことを検証

**追加検討:**
- アーキテクチャ変更 → +Atlas
- 大規模変更 → +Sherpa（段階的実行計画）
```

### SECURITY タイプ

```markdown
### 選定理由

1. **Sentinel**: 脆弱性の検出と静的分析
2. **Builder**: セキュリティ修正の実装
3. **Radar**: 修正の検証

**追加検討:**
- 動的テスト必要 → +Probe
- 認証/認可関連 → 重点レビュー
```

---

## 曖昧な要求のパターンと対応

| 要求パターン | uncertainty_level | 対応 |
|-------------|-------------------|------|
| 「バグを直して」 | partial | 文脈から特定、Scout開始 |
| 「パフォーマンスを改善して」 | partial | Bolt選択、領域を確認 |
| 「いい感じにして」 | ambiguous | MULTI_CANDIDATE_MODE |
| 「なんかおかしい」 | ambiguous | MULTI_CANDIDATE_MODE |
| 「レビューして」 | partial | Judge/Zenを文脈で選択 |
| 「テストして」 | clear | Radar/Voyagerを規模で選択 |

---

## フロー図

```
ユーザー要求
    ↓
┌─────────────────────────────┐
│ 判断要素の抽出              │
│ - task_type                 │
│ - technical_domain          │
│ - scope_indicators          │
│ - uncertainty_level         │
└─────────────────────────────┘
    ↓
uncertainty_level?
    ├─ clear → 直接チェーン選定 → ROUTING_EXPLANATION出力
    ├─ partial → チェーン選定 + 確認ポイント提示
    └─ ambiguous → MULTI_CANDIDATE_MODE発動
```
