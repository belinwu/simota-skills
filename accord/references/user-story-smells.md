# User Story Smells & Prioritization Pitfalls

> ユーザーストーリー 9 大スメル、MoSCoW 優先度付け 5 大ミス、Product Backlog アンチパターン

## 1. ユーザーストーリー 9 大スメル

| # | スメル | 症状 | 対策 |
|---|-------|------|------|
| **USS-01** | **全てがストーリー** | ユーザーストーリー以外の形式を許容しない | PBI は任意の形式が可 · 技術タスクはストーリーにしなくても良い |
| **USS-02** | **複数ページストーリー** | 1つのストーリーが数ページの文書 → 要件ドキュメントと混同 | ストーリーは会話のプレースホルダー · 補足は別成果物に |
| **USS-03** | **AC 欠如** | 受入基準なしで作業開始 → 完了条件が不明 | Sprint Planning までに AC を段階的に追加・精緻化 |
| **USS-04** | **AC と DoD の混同** | 全ストーリー共通の品質チェックを AC に記述 | AC = 機能固有 · DoD = チーム共通品質基準 |
| **USS-05** | **巨大ストーリー** | 1 Sprint で完了できない規模 → 不完全なインクリメント | 見積り困難/Sprint 超過/Sprint 全消費 → 分割 |
| **USS-06** | **技術レイヤー分割** | GUI/ビジネスロジック/永続化で分割 → 単体で価値なし | End-to-End の機能を提供する縦割り分割 |
| **USS-07** | **Ready 定義なし** | 十分にリファインされていないストーリーで Sprint 開始 | 価値・サイズ・AC・補足文書の Ready 基準を定義 |
| **USS-08** | **リファインメント省略** | 詳細なストーリーを最初に書いて二度と見直さない | Sprint 中に継続的にリファインメント実施 |
| **USS-09** | **会話の忘却** | ストーリーを静的文書として扱う → 対話なし | 会話が「最も重要な部分」 · 実装が近づくほど対話を増やす |

---

## 2. MoSCoW 優先度付け 5 大ミス

| # | ミス | 問題 | 対策 |
|---|-----|------|------|
| **MP-01** | **全部 Must** | 全ステークホルダーが自分の要件を Critical と主張 → Must 肥大化 | Must は全体工数の 60% 以下に制限（DSDM ルール） |
| **MP-02** | **ステークホルダー不整合** | ビジネスと技術で優先度の認識が異なる | 3チーム合同での優先度ワークショップ · 基準の明示化 |
| **MP-03** | **一度きりの優先度付け** | 最初に決めたら見直さない → 環境変化に追従不能 | Sprint/イテレーションごとに優先度を再評価 |
| **MP-04** | **緊急と重要の混同** | 緊急な要件を Must と判断 → 戦略的に重要な要件が後回し | 緊急度と重要度を分離して評価 · Eisenhower マトリクス |
| **MP-05** | **成功基準未定義** | 「成功」の定義なしに優先度付け → 主観的・感情的判断 | L0 の KPI から逆算した優先度付け · データ駆動判断 |

### Must カテゴリの適正チェック

```
Must 過剰の警告サイン:
  - Must が全要件の 60% を超えている
  - 「全部やらないとリリースできない」という声
  - Could/Won't が空または1-2件のみ

対策:
  1. 「これがなかったら本当にリリースできないか？」テスト
  2. Must → Should 降格候補を3チームで協議
  3. タイムボックス制約を明示（「4週間で Must のみ」）
  4. Won't の定義を「やらない」ではなく「今回はやらない」と再フレーミング
```

---

## 3. Product Backlog アンチパターン

| パターン | 問題 | Accord での対策 |
|---------|------|---------------|
| **肥大化バックログ** | 100+ アイテム → 優先度付け不能 | REQUIREMENTS_OVERFLOW トリガーで分割提案 |
| **陳腐化アイテム** | 古い/無関係な PBI が残留 | 定期レビュー · Deprecated ステータスの活用 |
| **事前全見積り** | 全ストーリーにタイムライン付き → 変更コスト大 | 直近 Sprint のみ詳細見積り · 段階的詳細化 |
| **エピック不在** | ストーリー群がどのビジネス目標に紐付くか不明 | L0 ビジョン → L1 US → L2 詳細の階層で紐付け |
| **技術負債の隠蔽** | 技術負債がバックログに可視化されない | L2-Dev の技術的制約セクションで明示 |

---

## 4. Accord との連携

```
Accord での活用:
  1. L1 のユーザーストーリー記述時に USS-01〜09 チェックを適用
  2. L1 の MoSCoW 優先度付けで MP-01〜05 を事前警告
  3. Must が 60% 超の場合に INTERACTION_TRIGGER を発火
  4. UNIFY フェーズでストーリー品質と優先度精度を追跡
  5. L1 品質チェックリストに USS/MP チェック項目を統合

品質ゲート:
  - AC なしのストーリーは Ready ではない（USS-03 防止）
  - Must > 60% で警告（MP-01 防止）
  - 技術レイヤー分割を検出したら縦割り分割を提案（USS-06 防止）
  - L0 KPI から逆算できない優先度に疑問フラグ（MP-05 防止）
```

**Source:** [Kaizenko: 9 User Story Smells and Anti-Patterns](https://www.kaizenko.com/9-user-story-smells-and-anti-patterns/) · [Age of Product: 27 Product Backlog Anti-Patterns](https://age-of-product.com/28-product-backlog-anti-patterns/) · [Medium: 5 Common MoSCoW Prioritization Mistakes](https://medium.com/@edstellarofficial/5-common-moscow-prioritization-mistakes-that-derail-projects-and-how-to-avoid-them-92ed0419400f) · [Agile Business Consortium: MoSCoW DSDM](https://www.agilebusiness.org/dsdm-project-framework/moscow-prioritisation.html) · [World of Agile: User Story Antipatterns](https://worldofagile.com/blog/typical-antipatterns-seen-in-a-user-story/)
