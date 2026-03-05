# Specification Anti-Patterns

> 仕様パッケージ作成における 12 大アンチパターン、クロスチームコミュニケーション失敗パターン

## 1. 仕様パッケージ 12 大アンチパターン

### 作成フェーズ

| # | アンチパターン | 症状 | 対策 |
|---|-------------|------|------|
| **SA-01** | **L0 Skip** | L0（ビジョン）を省略して即 L2 詳細に着手 → 3チームの共通理解なし | 必ず L0 から開始 · 2分で書ける1ページに制限 |
| **SA-02** | **Kitchen Sink Spec** | 全てを1つの仕様に詰込む → 100+ REQ の巨大仕様 | 10+ REQ で分割 · Sherpa でタスク分解 |
| **SA-03** | **Solution-First Spec** | 問題定義なしで解決策から記述 → 本当の課題を見落とす | L0 で「問題（Why）」を先に記述 · 解決策は L2 |
| **SA-04** | **Audience Blindness** | 全セクションを同じ言語・抽象度で記述 → チーム固有のニーズに不適合 | L2 で対象者別に記述 · 用語集の作成 |
| **SA-05** | **Static Spec** | 一度作成したら更新しない → 実装との乖離が拡大 | Living Document 化 · バージョン管理 · 定期レビュー |

### 品質フェーズ

| # | アンチパターン | 症状 | 対策 |
|---|-------------|------|------|
| **SA-06** | **Phantom Traceability** | トレーサビリティマトリクスを作るが実際はリンク切れだらけ | BRIDGE フェーズで整合性検証 · 前方/後方追跡 |
| **SA-07** | **Wishful BDD** | BDD シナリオが抽象的すぎて検証不能（具体値なし） | Given/When/Then に具体値を必須化 |
| **SA-08** | **Over-Specified L2** | L2 に実装詳細を書きすぎ → 開発チームの裁量を奪う | 「何を」は仕様、「どう」は実装チームの判断 |

### 組織・プロセスフェーズ

| # | アンチパターン | 症状 | 対策 |
|---|-------------|------|------|
| **SA-09** | **Throw Over the Wall** | 仕様を一方的に投げて終わり → フィードバックループなし | Cross-reference による双方向リンク · レビュープロセス |
| **SA-10** | **Single Author Spec** | 1人（通常 PM）が全セクションを書く → 偏った視点 | 3チーム共同作成 · 各 L2 は担当チームが記述 |
| **SA-11** | **Beautiful but Useless** | 見栄えの良い文書だが意思決定に使われない | 編集可能な形式 · 実行可能な BDD · 下流エージェント採用率追跡 |
| **SA-12** | **Scope Creep Enabler** | スコープ Out が未定義 → 際限なく要件が追加 | L0 で明示的に Out を定義 · 変更影響評価プロセス |

---

## 2. クロスチームコミュニケーション失敗統計

### データ

```
コミュニケーション失敗の実態:
  - B2B プロジェクトの 67% がステークホルダー整合の欠如で失敗（Gartner 2024）
  - プロジェクト失敗の 60% がコミュニケーション断絶に起因（PwC）
  - 非効率なステークホルダーコミュニケーションで CAC が平均 32% 増加（PwC 2025）
  - Time-to-Market が平均 41% 延長（PwC 2025）
  - 効果的なステークホルダー管理で成功確率が平均 38% 向上（PMI 2024）
  - 非効率なミーティング管理で中規模企業の運営収益の 2.5-3.8% が浪費（Deloitte 2025）
```

### 失敗パターンと対策

| 失敗パターン | 影響 | Accord での対策 |
|------------|------|---------------|
| **暗黙の仮定** | 各チームが異なる前提で作業 | L1 で仮定リストを明示化 |
| **専門用語の押付け** | 技術用語がビジネスチームを疎外 | 用語集 + L2 での対象者別記述 |
| **一方通行の仕様** | 仕様を投げるだけでフィードバックなし | L3 BDD での3チーム合意プロセス |
| **スコープの曖昧さ** | 「フェーズ1」の意味がチームごとに異なる | L0 の明示的 In/Out 定義 |
| **Why の欠如** | チームがビジネス文脈を理解しない | L0 の問題記述 + L2-Biz のビジネスインパクト |
| **遅延合流** | 新ステークホルダーが後から参加して再調整 | STAKEHOLDER_EXPANSION トリガーで早期検出 |

---

## 3. Accord との連携

```
Accord での活用:
  1. ALIGN フェーズで SA-01〜12 のリスクを事前スキャン
  2. ELABORATE フェーズで対象者別記述ガイドラインを適用
  3. BRIDGE フェーズで Phantom Traceability（SA-06）を検出
  4. VERIFY フェーズで BDD 品質チェック（SA-07 対策）
  5. UNIFY フェーズでアンチパターン発生率を追跡

品質ゲート:
  - L0 なしの仕様パッケージは生成しない（SA-01 防止）
  - L0 に Out セクションがない場合は警告（SA-12 防止）
  - BDD シナリオに具体値がない場合はフラグ（SA-07 防止）
```

**Source:** [Gartner: B2B Project Failure Statistics 2024](https://brixongroup.com/en/stakeholder-alignment-meeting-cadence-best-practices-for-successful-b2b-projects-in/) · [PMI: Pulse of the Profession 2024](https://www.pmi.org/learning/library/ensuring-sponsorship-stakeholder-alignment-project-8985) · [PwC: Stakeholder Communication Analysis 2025](https://brixongroup.com/en/stakeholder-alignment-meeting-cadence-best-practices-for-successful-b2b-projects-in/) · [Deloitte: Meeting Management Cost 2025](https://brixongroup.com/en/stakeholder-alignment-meeting-cadence-best-practices-for-successful-b2b-projects-in/)
