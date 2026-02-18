# Evaluation Criteria Reference — Void

5つの存在検証問の詳細、対象分類、YAGNIガイド。

---

## 5 Existence Questions — 詳細ガイド

### Q1: Who uses it?

**目的:** 実際のユーザーと仮想のユーザーを区別する。

```yaml
question: "Who uses it?"
investigation:
  - "このコード/機能を直接呼び出しているのは誰か？（コード内の参照）"
  - "このAPIを実際に消費している外部クライアントはあるか？"
  - "最後にこの機能を使ったユーザーはいつ、何人か？"
  - "この機能が無くなったら誰が困るか？名前を挙げられるか？"

scoring:
  high_confidence_keep: "日次アクティブユーザーが存在し、使用ログで確認可能"
  medium_confidence: "間接的に使用されているが、直接の利用者は不明"
  high_confidence_remove: "使用者を特定できない。「いつか誰かが使うかも」レベル"

red_flags:
  - "「将来的に必要になるかもしれない」"
  - "「他のチームが使っているはず」（確認なし）"
  - "「念のため残しておこう」"
```

### Q2: What breaks if removed?

**目的:** 実際の依存関係と想定上の依存関係を区別する。

```yaml
question: "What breaks if removed?"
investigation:
  - "コンパイル/ビルドが失敗するか？"
  - "テストが失敗するか？（テスト自体が不要な可能性も検討）"
  - "ランタイムエラーが発生するか？"
  - "ユーザーフローが断絶するか？"
  - "データの整合性が壊れるか？"

blast_radius_levels:
  NONE: "何も壊れない — 即座にREMOVE候補"
  LOCAL: "同一モジュール内のみ影響 — REMOVE/SIMPLIFY候補"
  CROSS_MODULE: "他モジュールに波及 — 慎重なSIMPLIFY/DEFER"
  PUBLIC_API: "外部クライアントに影響 — Magi escalation必須"
  DATA: "データ整合性に影響 — 最高注意、DEFER推奨"
```

### Q3: When was it last meaningfully changed?

**目的:** アクティブなメンテナンスと放置を区別する。

```yaml
question: "When was it last meaningfully changed?"
investigation:
  - "最後の実質的な変更（バグ修正/機能追加）はいつか？"
  - "依存関係の自動更新やフォーマット変更は除外する"
  - "関連するissue/PRは最近あったか？"

staleness_thresholds:
  fresh: "3ヶ月以内に実質的変更あり"
  aging: "3-12ヶ月変更なし — 注意"
  stale: "12-24ヶ月変更なし — SIMPLIFY/REMOVE候補"
  fossilized: "24ヶ月以上変更なし — 強いREMOVE候補"

exceptions:
  - "安定しているから変更不要な場合（例: 数学ライブラリ）"
  - "規制/コンプライアンス要件で変更できない場合"
  - "災害復旧コード（普段は使わないが、必要な時に必須）"
```

### Q4: Why was it built?

**目的:** 構築時の意図と現在の現実を比較する。

```yaml
question: "Why was it built?"
investigation:
  - "元のissue/PRの説明は何か？"
  - "当時の要件は今も有効か？"
  - "解決しようとした問題は今も存在するか？"
  - "別の方法で同じ問題が既に解決されていないか？"

obsolescence_signals:
  - "元の要件が撤回された"
  - "別のアプローチで同じ問題が解決済み"
  - "ビジネスモデルの変更で不要になった"
  - "技術スタックの変更で不要になった"
  - "実験的機能として作られ、実験は終了した"
```

### Q5: What does keeping it cost?

**目的:** 隠れた維持コストを可視化する。

```yaml
question: "What does keeping it cost?"
investigation:
  - "メンテナンスにどれくらいの時間が費やされているか？"
  - "テストの実行時間にどれくらい影響しているか？"
  - "新メンバーがこの部分を理解するのにどれくらいかかるか？"
  - "依存関係の更新頻度はどの程度か？"
  - "このコードに起因するバグの頻度は？"

hidden_costs:
  - "認知負荷: コードベースを理解する際の混乱"
  - "ビルド時間: コンパイル・テスト実行への影響"
  - "依存関係: 間接的な依存のメンテナンス"
  - "ドキュメント: 説明・更新が必要な文書"
  - "オンボーディング: 新メンバーへの説明コスト"
```

---

## Target Categories — 対象分類

| Category | Definition | Examples | Typical Pattern |
|----------|-----------|----------|----------------|
| **Feature** | ユーザーが直接操作する機能 | ダッシュボード、エクスポート機能、通知設定 | Feature Sunset |
| **Abstraction** | コード内の設計パターン・抽象化 | ベースクラス、ジェネリックハンドラ、プラグインシステム | Abstraction Collapse |
| **Scope** | 機能の範囲・バリエーション | 対応フォーマット数、設定オプション数 | Scope Cut |
| **Dependency** | 外部ライブラリ・サービス | npm packages、外部API、マイクロサービス | Dependency Elimination |
| **Configuration** | 設定可能なパラメータ | 環境変数、Feature Flag、管理画面の設定項目 | Configuration Reduction |

---

## YAGNI Decision Guide

```
対象を評価する際のYAGNI判定フロー:

1. 現在使われているか？
   ├─ YES → Q2-Q5へ進む
   └─ NO  → 即座にREMOVE候補（例外確認: 災害復旧/コンプライアンス）

2. 今後6ヶ月以内に必要になる具体的な計画があるか？
   ├─ YES（具体的なチケット/ロードマップ） → KEEP-WITH-WARNING
   └─ NO or 「いつか必要かも」 → REMOVE候補

3. 同じ機能を後から追加するコストは高いか？
   ├─ HIGH（データベーススキーマ変更等） → DEFER + 定期レビュー
   └─ LOW（通常の実装） → REMOVE（必要になったら再実装）
```

---

## Evaluation Summary Template

```yaml
target_evaluation:
  target_name: "<対象名>"
  category: "FEATURE | ABSTRACTION | SCOPE | DEPENDENCY | CONFIGURATION"
  questions:
    q1_who_uses: { answer: "string", confidence: "HIGH | MEDIUM | LOW" }
    q2_what_breaks: { answer: "string", blast_radius: "NONE | LOCAL | CROSS_MODULE | PUBLIC_API | DATA" }
    q3_last_changed: { answer: "YYYY-MM-DD", staleness: "FRESH | AGING | STALE | FOSSILIZED" }
    q4_why_built: { answer: "string", still_valid: true }
    q5_keeping_cost: { answer: "string", cost_level: "NEGLIGIBLE | LOW | MEDIUM | HIGH | CRITICAL" }
  yagni_verdict: "CURRENTLY_USED | PLANNED_USE | SPECULATIVE | DEAD"
  next_phase: "→ WEIGH (Cost-of-Keeping Score算出)"
```
