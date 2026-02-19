# Evaluation Criteria Reference — Void

5つの存在検証問の詳細（ドメイン別調査項目）、対象分類（8カテゴリ）、YAGNIガイド。

---

## 5 Existence Questions — 詳細ガイド

### Q1: Who uses it?

**目的:** 実際のユーザーと仮想のユーザーを区別する。

```yaml
question: "Who uses it?"
investigation_by_domain:
  Code:
    - "この関数を呼び出しているのは誰か？Import graph 確認"
    - "このAPIを実際に消費している外部クライアントはあるか？"
  Feature:
    - "DAU は？使用ログ確認"
    - "最後にこの機能を使ったユーザーはいつ、何人か？"
  Process:
    - "このフローを通る人/案件は月何件？"
    - "このステップを実際に確認している人は？"
  Document:
    - "最後に閲覧/更新したのは誰？いつ？"
    - "このドキュメントを参照して判断した事例は？"
  Design:
    - "このUIパスを通るユーザーは何%？"
    - "この画面の滞在時間・離脱率は？"

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
investigation_by_domain:
  Code:
    - "コンパイル/ビルドが失敗するか？"
    - "テストが失敗するか？（テスト自体が不要な可能性も検討）"
    - "ランタイムエラーが発生するか？"
  Feature:
    - "ユーザーフローが断絶するか？"
    - "データの整合性が壊れるか？"
    - "代替手段で同じ目的を達成できるか？"
  Process:
    - "コンプライアンス違反になるか？"
    - "品質低下が起きるか？"
    - "法的・規制上の問題が生じるか？"
  Document:
    - "オンボーディングが困難になるか？"
    - "判断根拠が喪失するか？"
    - "監査対応に影響するか？"
  Design:
    - "ユーザージャーニーが断絶するか？"
    - "コンバージョンファネルに影響するか？"

blast_radius_levels:
  NONE: "何も壊れない — 即座にREMOVE候補"
  LOCAL: "同一モジュール/チーム内のみ影響 — REMOVE/SIMPLIFY候補"
  CROSS_MODULE: "他モジュール/チームに波及 — 慎重なSIMPLIFY/DEFER"
  PUBLIC_API: "外部クライアント/ステークホルダーに影響 — Magi escalation必須"
  DATA: "データ整合性に影響 — 最高注意、DEFER推奨"
```

### Q3: When was it last meaningfully changed?

**目的:** アクティブなメンテナンスと放置を区別する。

```yaml
question: "When was it last meaningfully changed?"
investigation:
  - "最後の実質的な変更（バグ修正/機能追加/内容更新）はいつか？"
  - "自動更新やフォーマット変更は除外する"
  - "関連するissue/PR/チケットは最近あったか？"

staleness_thresholds:
  fresh: "3ヶ月以内に実質的変更あり"
  aging: "3-12ヶ月変更なし — 注意"
  stale: "12-24ヶ月変更なし — SIMPLIFY/REMOVE候補"
  fossilized: "24ヶ月以上変更なし — 強いREMOVE候補"

exceptions:
  - "安定しているから変更不要な場合（例: 数学ライブラリ、確定した規約）"
  - "規制/コンプライアンス要件で変更できない場合"
  - "災害復旧/緊急時コード（普段は使わないが、必要な時に必須）"
```

### Q4: Why was it built?

**目的:** 構築時の意図と現在の現実を比較する。

```yaml
question: "Why was it built?"
investigation:
  - "元のissue/PR/企画書の説明は何か？"
  - "当時の要件は今も有効か？"
  - "解決しようとした問題は今も存在するか？"
  - "別の方法で同じ問題が既に解決されていないか？"

obsolescence_signals:
  - "元の要件が撤回された"
  - "別のアプローチで同じ問題が解決済み"
  - "ビジネスモデルの変更で不要になった"
  - "技術スタック/組織構造の変更で不要になった"
  - "実験的に作られ、実験は終了した"
  - "担当者が退職し、背景を知る人がいない"
```

### Q5: What does keeping it cost?

**目的:** 隠れた維持コストを可視化する。

```yaml
question: "What does keeping it cost?"
investigation_by_domain:
  Code:
    - "テスト時間にどれくらい影響しているか？"
    - "ビルド時間への影響は？"
    - "新メンバーがこの部分を理解するのにどれくらいかかるか？"
    - "このコードに起因するバグの頻度は？"
  Process:
    - "人件費×時間：このステップに費やす工数は？"
    - "待ち時間：承認待ちによる意思決定遅延は？"
    - "例外対応：ルールに合わないケースの処理コストは？"
  Document:
    - "更新コスト：内容を最新に保つ労力は？"
    - "誤情報リスク：古い情報による誤判断の可能性は？"
    - "検索ノイズ：情報を探す際の混乱・時間浪費は？"
  Design:
    - "実装コスト：この画面/要素のメンテナンス工数は？"
    - "認知負荷：ユーザーの混乱を生んでいないか？"
  Dependency:
    - "セキュリティ：脆弱性対応の頻度は？"
    - "互換性：バージョンアップ時の破壊的変更リスクは？"

hidden_costs:
  - "認知負荷: 理解・学習・記憶にかかるコスト"
  - "機会費用: この維持に使う時間で他に何ができるか"
  - "伝播コスト: 依存先の変更に追随するコスト"
  - "オンボーディング: 新メンバーへの説明コスト"
  - "信頼性リスク: 古い/不正確な情報による誤判断"
```

---

## Target Categories — 対象分類

| Category | Definition | Examples | Typical Pattern |
|----------|-----------|----------|----------------|
| **Feature** | ユーザーが直接操作する機能 | ダッシュボード、エクスポート機能、通知設定 | Feature Sunset |
| **Abstraction** | コード内の設計パターン・抽象化 | ベースクラス、ジェネリックハンドラ、プラグインシステム | Abstraction Collapse |
| **Scope** | 機能の範囲・バリエーション | 対応フォーマット数、設定オプション数 | Scope Cut |
| **Dependency** | 外部ライブラリ・サービス | npm packages、外部API、SaaSツール | Dependency Elimination |
| **Configuration** | 設定可能なパラメータ | 環境変数、Feature Flag、管理画面の設定項目 | Configuration Reduction |
| **Process** | ワークフロー・手順・承認フロー | コードレビュー手順、承認ステップ、定例会議 | Process Pruning |
| **Document** | 文書・仕様・ガイド | 設計書、Wiki、チェックリスト、ガイドライン | Document Retirement |
| **Design/Specification** | UI要素・画面・要件・受入基準 | 管理画面、ユーザーストーリー、画面遷移 | Scope Cut / Feature Sunset |

---

## YAGNI Decision Guide

```
対象を評価する際のYAGNI判定フロー:

1. 現在使われているか？
   ├─ YES → Q2-Q5へ進む
   └─ NO  → 即座にREMOVE候補（例外確認: 災害復旧/コンプライアンス/規制）

2. 今後6ヶ月以内に必要になる具体的な計画があるか？
   ├─ YES（具体的なチケット/ロードマップ） → KEEP-WITH-WARNING
   └─ NO or 「いつか必要かも」 → REMOVE候補

3. 同じものを後から作り直すコストは高いか？
   ├─ HIGH（データベーススキーマ変更、組織再編等） → DEFER + 定期レビュー
   └─ LOW（通常の実装、手順書作成） → REMOVE（必要になったら再作成）
```

---

## Evaluation Summary Template

```yaml
target_evaluation:
  target_name: "<対象名>"
  domain: "CODE | FEATURE | PROCESS | DOCUMENT | DESIGN | DEPENDENCY | CONFIGURATION | SPECIFICATION"
  category: "FEATURE | ABSTRACTION | SCOPE | DEPENDENCY | CONFIGURATION | PROCESS | DOCUMENT | DESIGN_SPEC"
  questions:
    q1_who_uses: { answer: "string", confidence: "HIGH | MEDIUM | LOW" }
    q2_what_breaks: { answer: "string", blast_radius: "NONE | LOCAL | CROSS_MODULE | PUBLIC_API | DATA" }
    q3_last_changed: { answer: "YYYY-MM-DD", staleness: "FRESH | AGING | STALE | FOSSILIZED" }
    q4_why_built: { answer: "string", still_valid: true }
    q5_keeping_cost: { answer: "string", cost_level: "NEGLIGIBLE | LOW | MEDIUM | HIGH | CRITICAL" }
  yagni_verdict: "CURRENTLY_USED | PLANNED_USE | SPECULATIVE | DEAD"
  next_phase: "→ WEIGH (Cost-of-Keeping Score算出)"
```
