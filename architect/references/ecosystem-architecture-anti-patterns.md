# Ecosystem Architecture Anti-Patterns

> エージェントエコシステムのアーキテクチャ落とし穴、モジュラー設計の失敗、ガバナンスドリフト、プラットフォーム設計の罠

## 1. エコシステムアーキテクチャ 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **EA-01** | **Big Ball of Mud** | 構造なきエコシステム成長 | エージェント間の境界が不明瞭、依存関係が暗黙的 | カテゴリ分類 + 明示的な COLLABORATION_PATTERNS |
| **EA-02** | **The Blob（God Agent）** | 1 エージェントが過剰な責務を吸収 | capabilities が 10+ 項目、他エージェントとの重複多数 | 専門化原則の徹底、責務の分離 |
| **EA-03** | **Gas Factory（過剰設計）** | 単純な問題に複雑なエコシステムを構築 | 使用率の低いエージェント多数、学習コスト高 | 80% ルール、実需からの逆算設計 |
| **EA-04** | **Modularity Violation** | 独立であるべきエージェントが常に一緒に変更される | 変更波及が予測不能、修正が連鎖 | 境界の再定義、依存グラフの可視化 |
| **EA-05** | **Phantom Agent** | 定義はあるが使用されないエージェント | 使用率 < 10%、ドキュメント陳腐化 | 定期的な使用率監査、非活性エージェントの廃止 |
| **EA-06** | **Circular Dependency** | エージェント間の循環的な依存関係 | A→B→C→A のフロー、無限ループリスク | 依存方向の単方向化、中間者パターン |
| **EA-07** | **Erosion（浸食）** | 設計意図からの漸進的な逸脱 | 命名規則違反、パターン不一致、ドキュメント劣化 | 定期的な健全性監査、ガバナンスルールの自動検証 |

---

## 2. モジュラー設計の原則とアンチパターン

```
モジュラーエコシステムの 5 原則:

  1. 高凝集（High Cohesion）:
     ✅ 各エージェントの責務が密接に関連
     ❌ 関連しない機能が 1 エージェントに混在
     → 1 エージェント = 1 ドメイン = 1 専門性

  2. 疎結合（Loose Coupling）:
     ✅ エージェント間の依存が最小限
     ❌ エージェント A の変更が B, C, D に波及
     → ハンドオフテンプレートで接続面を標準化

  3. 情報隠蔽（Information Hiding）:
     ✅ CAPABILITIES_SUMMARY で外部 API を定義
     ❌ 内部実装詳細が他エージェントに漏洩
     → references/ を内部知識、SKILL.md を外部インターフェース

  4. 代替可能性（Substitutability）:
     ✅ 同じハンドオフで異なるエージェントが機能
     ❌ 特定エージェントに密結合
     → 標準化されたハンドオフフォーマット

  5. 漸進的採用（Incremental Adoption）:
     ✅ 新エージェントの段階的統合
     ❌ ビッグバン導入
     → カテゴリ単位の段階的拡張

モジュラー設計アンチパターン:

  ❌ Feature Envy:
    エージェント A が B のデータ/機能を頻繁に使用
    → A と B の境界を再定義するか統合を検討

  ❌ Shotgun Surgery:
    1 つの変更が多数のエージェントに影響
    → 責務の再分配、共通部分を _common/ に抽出

  ❌ Speculative Generality:
    将来必要になるかもしれないエージェントを先行作成
    → 実需 3+ プロダクトからの逆算
```

---

## 3. エコシステムガバナンスのドリフトパターン

```
ドリフトパターン（設計意図からの漸進的逸脱）:

  Drift-01: 命名規則ドリフト
    原因: 新エージェント作成時に既存規則を確認しない
    兆候: 類似名のエージェントが並存（例: analyze / analysis / analyzer）
    対策: naming-conventions.md の参照を必須化

  Drift-02: 構造ドリフト
    原因: SKILL.md テンプレートの自由解釈
    兆候: エージェントごとにセクション構成が異なる
    対策: skill-template.md の厳格な適用 + validation-checklist.md

  Drift-03: 協調パターンドリフト
    原因: ハンドオフの非標準化
    兆候: INPUT/OUTPUT の記述形式がバラバラ
    対策: 標準ハンドオフテンプレートの徹底

  Drift-04: カテゴリドリフト
    原因: 新エージェントのカテゴリ分類が曖昧
    兆候: 同じカテゴリ内に異質なエージェント
    対策: agent-categories.md のカテゴリ定義との整合性チェック

  Drift-05: 品質ドリフト
    原因: Health Score の定期計測を怠る
    兆候: 一部エージェントの references/ が陳腐化
    対策: review-loop.md の PDCA サイクル実行
```

---

## 4. プラットフォーム設計の教訓

```
Platform as Product の原則:

  1. 内部開発者体験（DX）優先:
     → エージェント設計者（= ユーザー）の体験を最適化
     → テンプレート、チェックリスト、自動検証ツールの提供

  2. 漸進的複雑性:
     Level 0: _common/ のみ参照（最小限の知識で開始）
     Level 1: SKILL.md テンプレートで標準エージェント作成
     Level 2: references/ で専門知識を深化
     Level 3: Nexus 統合 + 自己進化サブシステム

  3. ドキュメンテーションは API:
     → SKILL.md = エージェントの API 仕様
     → CAPABILITIES_SUMMARY = ルーティング用メタデータ
     → references/ = 内部実装ドキュメント
     → ドキュメントの品質 = システムの品質

  4. 「使いたくなる」設計:
     → 強制ではなく価値提供
     → 成功事例の共有
     → 低い参入障壁 + 高い天井

スケーリング時の注意:

  ❌ 56 エージェント → 100 エージェントの直線的拡張
    → カテゴリあたりのエージェント数が過剰になる
    → 発見可能性（discoverability）が低下

  ✅ カテゴリの細分化 + ルーティングの階層化
    → Nexus → カテゴリハブ → 専門エージェント
    → 段階的な絞り込みで適切なエージェントに到達
```

---

## 5. エコシステム健全性メトリクス

| メトリクス | 目標値 | 計測方法 |
|-----------|--------|---------|
| エージェント使用率 | 全エージェントの 80%+ が月 1 回以上使用 | journal/PROJECT.md の記録 |
| 重複率 | エージェント間重複 30% 未満 | overlap-detection.md スコアリング |
| Health Score 平均 | Grade B (80+) 以上 | review-loop.md 公式 |
| ドキュメント鮮度 | 1 スプリント以内の更新 | 最終更新日チェック |
| カテゴリバランス | カテゴリあたり 2-8 エージェント | agent-categories.md |
| 孤立エージェント数 | 0 | INPUT/OUTPUT パートナーの存在確認 |

---

## 6. Architect との連携

```
Architect での活用:
  1. ENVISION フェーズで EA-01〜07 のスクリーニング
  2. 新エージェント設計時にモジュラー原則の適用確認
  3. エコシステム拡張時にガバナンスドリフトの検出
  4. VALIDATE フェーズで健全性メトリクスの確認

品質ゲート:
  - 責務 10+ capabilities → 分割を提案（EA-02 防止）
  - 使用率 < 10% → 廃止または統合を検討（EA-05 防止）
  - カテゴリあたり 8+ エージェント → カテゴリ細分化（スケーリング対策）
  - ハンドオフ形式が非標準 → テンプレート適用（Drift-03 防止）
  - 循環依存検出 → 依存方向の再設計（EA-06 防止）
  - Health Score < C (70) → 改善計画策定（EA-07 防止）
```

**Source:** [InfoQ: Architecture Trends 2025](https://www.infoq.com/articles/architecture-trends-2025/) · [O'Reilly: Software Architecture Patterns, Antipatterns, and Pitfalls](https://www.oreilly.com/library/view/software-architecture-patterns/0642572221119/) · [Brainhub: Software Architecture Patterns](https://brainhub.eu/library/software-architecture-patterns)
