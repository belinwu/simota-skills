# Onboarding & Usage Examples

**Purpose:** Concrete examples of Compass interactions for onboarding users.
**Read when:** You need onboarding scenarios, example dialogues, or usage guidance.

---

## Onboarding Guide

### Level 1: First Contact (初めての方)

エコシステムの全体像を伝える。詳細よりも「こういうことができる」を重視。

**推薦トーク:**

```
このエコシステムには100以上の専門スキルがあり、大きく5つの領域に分かれます:

1. 作る系: Builder(実装), Forge(プロトタイプ), Artisan(フロントエンド)
2. 直す系: Scout(調査), Zen(リファクタ), Bolt(高速化)
3. 守る系: Sentinel(セキュリティ), Radar(テスト), Judge(レビュー)
4. 設計する系: Atlas(アーキテクチャ), Schema(DB), Gateway(API)
5. 運用する系: Pipe(CI/CD), Scaffold(インフラ), Beacon(監視)

まず何をしたいか教えてください。最適なスキルを提案します。
```

### Level 2: Category Deep Dive (カテゴリ深掘り)

特定のカテゴリに興味を持ったユーザーに詳細を説明。

**例: 「テスト系のスキルを教えて」**

```
テスト系のスキルは3つあります:

1. Radar - ユニットテスト・エッジケース追加・flaky テスト修正
   使い方: `/radar このモジュールのテストカバレッジを上げて`

2. Voyager - E2Eテスト（Playwright/Cypress）
   使い方: `/voyager ログインフローのE2Eテストを作って`

3. Siege - 負荷テスト・カオスエンジニアリング・契約テスト
   使い方: `/siege このAPIの負荷テスト計画を作って`

使い分けの目安:
- 関数・モジュール単位 → Radar
- ユーザーフロー全体 → Voyager
- 非機能要件の検証 → Siege
```

### Level 3: Scenario Matching (シナリオマッチング)

具体的なタスクに対して最適なスキルを推薦。

**例: 「本番環境で500エラーが出てる」**

```
## 推薦: 本番500エラーの調査と修正

### 1. Scout (最推薦)
- **何をするか**: バグの根本原因を特定し、再現手順と影響範囲を報告
- **なぜこれか**: 500エラーの原因は多岐にわたるため、まず調査が必要
- **使い方**: `/scout 本番で/api/usersに500エラーが出ている。エラーログは〇〇`
- **注意**: Scout はコードを書かない。修正は Builder に引き継ぐ

### 2. Triage (代替案)
- **何をするか**: インシデント初動対応・影響範囲特定・復旧手順策定
- **こちらを選ぶ場面**: 多数のユーザーに影響があり、緊急度が高い場合

### 次のステップ
Scout の調査結果を元に `/builder` で修正、`/radar` で再発防止テストを追加
```

---

## FAQ Patterns

### Q: 「Nexus と Compass の違いは？」

```
- Compass: どのスキルを使うべきか案内する（ナビゲーター）
- Nexus: 実際にスキルを組み合わせてタスクを実行する（オーケストレータ）

例えるなら:
- Compass = 旅行ガイドブック（どこに行くべきか教える）
- Nexus = ツアーガイド（実際に連れて行ってくれる）

簡単なタスクなら Compass の推薦を見て直接スキルを呼べます。
複雑なタスクなら Compass → Nexus の流れで自動実行できます。
```

### Q: 「似たスキルが多くて選べない」

```
よくある混同ペアと使い分けは patterns.md の "Don't Use" Quick Reference を参照。

迷ったら「コードを変えるか変えないか」で判断:
- 変える系: Builder, Zen, Artisan, Bolt
- 変えない系: Scout, Judge, Atlas, Sentinel
```

### Q: 「新しいプロジェクトを始めたい」

```
新規プロジェクトの推薦チェーン:

1. Scribe - 要件定義・技術仕様書の作成
2. Atlas - アーキテクチャ設計
3. Schema - DB設計（必要な場合）
4. Gateway - API設計（必要な場合）
5. Grove - リポジトリ構造設計
6. Scaffold - 開発環境・インフラ構築
7. Forge - プロトタイプ作成
8. Builder - 本格実装

全部やる必要はありません。規模に応じて：
- 小規模: Forge → Builder
- 中規模: Scribe → Builder → Radar
- 大規模: Scribe → Atlas → Builder → Radar → Judge
```

---

## Interaction Examples

### Example 1: Direct Skill Question

**User**: 「DBのクエリが遅い」
**Compass**:

```
## 推薦: DBクエリパフォーマンス改善

### 1. Tuner (最推薦)
- EXPLAIN ANALYZE 分析、実行計画最適化、インデックス提案
- `/tuner この遅いクエリを最適化して: SELECT ...`

### 2. Bolt (代替案)
- アプリケーション層のキャッシュ戦略やN+1解消も含む場合
- `/bolt このAPIエンドポイントのレスポンスを高速化して`

DB側だけなら Tuner、アプリ全体なら Bolt。
```

### Example 2: Vague Request

**User**: 「コードの質を上げたい」
**Compass**:

```
「コードの質」にはいくつかの側面があります。どれに近いですか？

1. 可読性・構造の改善 → Zen (リファクタリング)
2. テスト追加 → Radar (テストカバレッジ)
3. セキュリティ強化 → Sentinel (脆弱性検出)
4. ドキュメント追加 → Quill (JSDoc/コメント)
5. 不要コード削除 → Sweep (デッドコード除去)
6. 全部まとめて → Nexus で上記を組み合わせ

特に気になる部分があれば教えてください。
```

### Example 3: Gap Detection

**User**: 「Slackボットを作りたい」
**Compass**:

```
## 推薦: Slackボット開発

### 1. Relay (最推薦)
- メッセージング統合・ボット開発・Webhook設計の専門スキル
- `/relay Slackボットのアーキテクチャを設計して`

### 2. Builder (実装フェーズ)
- Relay の設計を元に実装する場合
- `/builder Relay の設計に基づいてSlackボットを実装して`

### 次のステップ
Relay で設計 → Builder で実装 → Radar でテスト
```
