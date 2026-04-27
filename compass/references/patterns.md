# Task-to-Skill Mapping Patterns

**Purpose:** Common scenarios and the recommended agent(s) for each.
**Read when:** You need to match a user's task to the best skill agent(s).

---

## Quick Decision Tree

```
ユーザーの要求
  │
  ├─ コードを書いてほしい
  │   ├─ 新機能実装 → Builder
  │   ├─ プロトタイプ → Forge
  │   ├─ フロントエンド → Artisan
  │   ├─ CLI/TUI → Anvil
  │   └─ モバイル → Native
  │
  ├─ コードを直してほしい
  │   ├─ バグ調査 → Scout
  │   ├─ リファクタリング → Zen
  │   ├─ パフォーマンス(アプリ全体) → Bolt
  │   ├─ パフォーマンス(DB/クエリ) → Tuner
  │   └─ セキュリティ修正 → Sentinel
  │
  ├─ テストしてほしい
  │   ├─ ユニットテスト → Radar
  │   ├─ E2Eテスト → Voyager
  │   └─ 負荷/耐障害テスト → Siege
  │
  ├─ 設計してほしい
  │   ├─ アーキテクチャ → Atlas
  │   ├─ DB設計 → Schema
  │   ├─ API設計 → Gateway
  │   └─ UI/UX設計 → Vision
  │
  ├─ ドキュメントを書いてほしい
  │   ├─ 技術仕様書 → Scribe
  │   ├─ コードドキュメント → Quill
  │   ├─ UXライティング → Prose
  │   └─ 学習教材 → Tome
  │
  ├─ レビューしてほしい
  │   ├─ コードレビュー → Judge
  │   ├─ セキュリティ監査 → Sentinel
  │   └─ 規格準拠チェック → Canon
  │
  ├─ 調査・分析してほしい
  │   ├─ コード理解 → Lens
  │   ├─ Git履歴調査 → Trail
  │   ├─ レガシーコード解析 → Fossil
  │   ├─ 影響範囲分析 → Ripple
  │   └─ 競合調査 → Compete
  │
  ├─ DevOps/インフラ
  │   ├─ CI/CD → Pipe
  │   ├─ IaC → Scaffold
  │   ├─ 依存関係管理 → Gear
  │   └─ 監視設計 → Beacon
  │
  ├─ 計画・戦略
  │   ├─ タスク分解 → Sherpa
  │   ├─ 複数エージェント連携 → Nexus
  │   ├─ 優先順位付け → Rank
  │   └─ リリース計画 → Launch
  │
  └─ その他
      ├─ ブラウザ操作 → Navigator
      ├─ i18n対応 → Polyglot
      ├─ ピクセルアート → Dot
      ├─ SVGアイコン → Ink
      ├─ 効果音/BGM → Tone
      └─ アイデア出し → Riff
```

---

## Scenario-Based Patterns

### "バグを直したい"

| 状況 | 推薦 | 理由 |
|------|------|------|
| 原因不明のバグ | Scout → Builder | Scout で原因特定、Builder で修正 |
| リグレッション | Trail → Scout → Builder | Trail で原因コミット特定 |
| パフォーマンス劣化 | Bolt | パフォーマンス専門 |
| セキュリティ脆弱性 | Sentinel → Builder | Sentinel で検出、Builder で修正 |

### "新機能を追加したい"

| 状況 | 推薦 | 理由 |
|------|------|------|
| 仕様が明確 | Builder | 直接実装 |
| 仕様が曖昧 | Scribe → Builder | Scribe で仕様策定後に実装 |
| プロトタイプが欲しい | Forge | 高速プロトタイピング |
| 大規模機能 | Sherpa → Nexus | 分解してからオーケストレーション |

### "コードの品質を上げたい"

| 状況 | 推薦 | 理由 |
|------|------|------|
| リファクタリング | Zen | 可読性・構造改善 |
| テスト不足 | Radar | テスト追加 |
| ドキュメント不足 | Quill | JSDoc/コメント追加 |
| 不要コード削除 | Sweep | デッドコード検出・削除 |

### "セキュリティを強化したい"

| 状況 | 推薦 | 理由 |
|------|------|------|
| 静的解析 | Sentinel | コードベースのセキュリティ監査 |
| 動的テスト | Probe | DAST実行 |
| レッドチーム | Breach | 攻撃シナリオ設計 |
| 暗号設計 | Crypt | 暗号アーキテクチャ |

### "デプロイ・運用を改善したい"

| 状況 | 推薦 | 理由 |
|------|------|------|
| CI/CD構築 | Pipe | GitHub Actions専門 |
| インフラ構築 | Scaffold | IaC設計 |
| 監視・アラート | Beacon | SLO/SLI設計 |
| インシデント対応 | Triage → Mend | 調査→自動修復 |

### "UI/UXを改善したい"

| 状況 | 推薦 | 理由 |
|------|------|------|
| デザイン方向性 | Vision | クリエイティブディレクション |
| ユーザビリティ改善 | Palette | インタラクション品質 |
| アニメーション | Flow | CSS/JSアニメーション |
| ユーザーテスト | Echo | ペルソナ認知ウォークスルー |
| モックアップ→コード | Pixel | 画像からHTML/CSS生成 |

---

## Multi-Agent Chain Patterns

### Feature Development Chain
```
Scribe(仕様) → Builder(実装) → Radar(テスト) → Judge(レビュー)
```

### Bug Fix Chain
```
Scout(調査) → Builder(修正) → Radar(テスト追加)
```

### Security Audit Chain
```
Sentinel(静的解析) → Probe(動的テスト) → Breach(レッドチーム)
```

### Architecture Improvement Chain
```
Atlas(分析) → Ripple(影響評価) → Builder(実装) → Judge(レビュー)
```

### UX Improvement Chain
```
Echo(認知ウォークスルー) → Vision(方向性) → Palette(改善) → Flow(アニメーション)
```

### Performance Optimization Chain
```
Tuner(DB最適化) → Bolt(アプリ最適化) → Beacon(監視設定)
```

### Legacy Modernization Chain
```
Fossil(解析) → Horizon(移行計画) → Shift(移行実行)
```

---

## "Don't Use" Quick Reference

よくある間違いを防ぐための逆引きガイド。

| やりたいこと | 間違いやすいスキル | 正しいスキル | 理由 |
|-------------|------------------|-------------|------|
| コード実装 | Scout | Builder | Scout は調査のみ |
| E2Eテスト | Radar | Voyager | Radar はユニットテスト |
| DB最適化 | Schema | Tuner | Schema は設計、Tuner は最適化 |
| PRレビュー | Zen | Judge | Zen はリファクタリング |
| API仕様書 | Quill | Gateway | Quill はコードドキュメント |
| ブラウザ操作 | Voyager | Navigator | Voyager はE2Eテスト |
| リリース管理 | Guardian | Launch | Guardian はPR管理 |
| コード理解 | Scout | Lens | Scout はバグ調査、Lens はコード理解全般 |
| 全体アーキテクチャ | Schema | Atlas | Schema はDB特化、Atlas は全体設計 |
| 技術仕様書 | Quill | Scribe | Quill はコード内ドキュメント |
| 本格実装 | Forge | Builder | Forge はプロトタイプ |

迷ったら「コードを変えるか変えないか」で判断:
- 変える系: Builder, Zen, Artisan, Bolt
- 変えない系: Scout, Judge, Atlas, Sentinel

---

## Output Formats

### Recommendation Format

```markdown
## 推薦: [タスクの要約]

### 1. [Agent Name] (最推薦)
- **何をするか**: [1行説明]
- **なぜこれか**: [ユーザーの状況との適合理由]
- **使い方**: `/[agent-name] [具体的な指示例]`
- **注意**: [使うべきでない場面があれば]

### 2. [Agent Name] (代替案)
- **何をするか**: [1行説明]
- **こちらを選ぶ場面**: [1の代わりにこちらが適する条件]

### 次のステップ
[具体的なアクション提案]
```

### Comparison Format

```markdown
## 比較: [Agent A] vs [Agent B]

| 観点 | Agent A | Agent B |
|------|---------|---------|
| 主な役割 | ... | ... |
| コード生成 | する/しない | する/しない |
| 入力 | ... | ... |
| 出力 | ... | ... |
| 使うべき時 | ... | ... |

### 使い分けの目安
- [条件1] → Agent A
- [条件2] → Agent B
- [条件3] → 両方（Agent A → Agent B のチェーン）
```
