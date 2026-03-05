# Documentation Architecture Anti-Patterns

> ドキュメント組織化の失敗パターン、Docs-as-Code の罠、ドキュメント腐敗と漂流の防止

## 1. ドキュメントアーキテクチャ 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **DA-01** | **Doc Drift（ドキュメント漂流）** | コード変更にドキュメント更新が追従しない | 非推奨APIの参照、削除済みフィールドの記載、古いコードサンプル | Docs-as-Code（コードと同リポジトリ管理）、PR でのドキュメント更新強制 |
| **DA-02** | **Single-Owner Fossil（単一所有者の化石化）** | 1人のエンジニアが全ドキュメントを所有 | その人の退職でドキュメントが化石化、誰も更新しない | 共有オーナーシップ（コード変更者がドキュメントも更新）、CODEOWNERS 設定 |
| **DA-03** | **Audience Blindness（対象者不在）** | 全読者に向けた汎用ドキュメント | バックエンド/フロントエンド/運用チーム全員に不十分、誰にも刺さらない | 対象者別レイヤー分離（architecture/, operations/, guides/） |
| **DA-04** | **Intent Amnesia（意図の喪失）** | 「なぜ」の記載がなく「何を」だけ記述 | ADR 不在、過去の議論の繰り返し、以前修正した問題の再導入 | ADR 必須化、クリティカルな不変条件の明示的記載 |
| **DA-05** | **Wiki Graveyard（Wiki 墓場）** | Confluence/Wiki に分散したドキュメントがコードと乖離 | バージョン管理なし、検索性低下、最終更新が数年前 | リポジトリ内 docs/ への一元化、Markdown + Git による管理 |
| **DA-06** | **Text-Only Complex Systems（テキストのみの複雑系）** | 分散システムのフローをテキストだけで説明 | リトライ動作・冪等性ルール・サービス間依存をエンジニアがそれぞれ異なる理解 | シーケンス図・アーキテクチャ図・データフロー図の必須化 |
| **DA-07** | **Post-Implementation Docs（実装後ドキュメント）** | ドキュメントが実装の「おまけ」扱い | PR にドキュメント変更なし、レビュー時に意図が不明、仕様書の事後作成 | PR ワークフローにドキュメント更新チェック組み込み、CI での検証 |

---

## 2. ドキュメント腐敗の検出と防止

```
腐敗の 4 段階:

  Stage 1: Fresh（新鮮）
    → コードと完全に同期
    → 最終更新がコード変更と同日

  Stage 2: Stale（古い）
    → 小さな不整合が発生
    → コードは変わったがドキュメントは未更新
    → 期間: 1-3 ヶ月放置

  Stage 3: Misleading（誤解を招く）
    → ドキュメントが実装と矛盾
    → 開発者がドキュメントを「信用しない」
    → 期間: 3-6 ヶ月放置

  Stage 4: Fossil（化石）
    → 誰も読まず、誰も更新しない
    → 存在が混乱の原因に
    → 削除 or アーカイブが必要

検出方法:
  □ docs/ 内ファイルの最終更新日を追跡
  □ 関連ソースファイルの変更日と比較
  □ リンク切れの自動検出
  □ コードサンプルの自動検証（可能な場合）

防止策:
  □ Per-PR: コード変更時にドキュメント更新をチェック
  □ Per-release: 正確性レビュー
  □ Quarterly: 古い図・非推奨フラグ・レガシーサービス参照の削除
```

---

## 3. Docs-as-Code ベストプラクティス

```
核心原則:
  「ドキュメントはプロダクトのコンポーネントであり、
   コードと同じ厳格さ・テスト・ユーザー中心設計が必要」

実践方法:

  1. バージョン管理:
     → docs/ をリポジトリ内に配置（Wiki は補助のみ）
     → Git で変更追跡・レビュー・ロールバック可能
     → Markdown + 静的サイトジェネレーター（Docusaurus, MkDocs 等）

  2. 自動化:
     → CI でリンク切れ検出
     → コードサンプルの自動テスト（可能な場合）
     → ドキュメント変更なしの PR にワーニング

  3. 情報アーキテクチャ:
     → ユーザージャーニーに沿った構成
     → 段階的開示（Getting Started → Advanced → API Reference）
     → モジュラーコンポーネント（再利用可能なスニペット）

  4. 検索性:
     → 内部検索機能の最適化
     → 予測可能なセクション構成
     → インシデント中にアクセスされることを前提に設計

  5. フィードバックループ:
     → アクセス解析で頻繁に参照されるページを特定
     → ユーザーからの直接フィードバック収集
     → 繰り返される質問のドキュメント化
```

---

## 4. ドキュメント構造の対象者別設計

```
レイヤー分離モデル:

  docs/
    architecture/        ← エンジニア向け
      adr/               ← Architecture Decision Records
      diagrams/          ← シーケンス図、アーキテクチャ図
      invariants/        ← クリティカルな不変条件
    operations/          ← 運用チーム向け
      runbooks/          ← 障害対応手順
      alerts/            ← アラート対応ガイド
      deployment/        ← デプロイ手順
    guides/              ← 全エンジニア向け
      getting-started/   ← オンボーディング
      contributing/      ← コントリビューションガイド
      troubleshooting/   ← トラブルシューティング
    api/                 ← API 利用者向け
      openapi/           ← OpenAPI 仕様
      examples/          ← コードサンプル

  不変条件の明示的記載例:
    "This must always hold:
     - The tax-calculation service must never call the discount-engine directly
     - All payment events must be idempotent
     - User deletion must cascade to all dependent services within 24h"

  → 明示的な不変条件がリファクタ時の誤削除を防止
```

---

## 5. クロスリポジトリのドキュメント一貫性

```
マルチリポジトリ環境の課題:

  問題:
    → チームごとに異なる用語でドメインオブジェクトを記述
    → ドキュメントスタイルの不統一が構造的負債に
    → 新メンバーがパターンを再学習する必要

  対策:

    1. スタイルガイド共有:
       → 命名規約、API コントラクトパターン、エラー記述フォーマット
       → 図の配置ルール、不変条件の記法
       → テンプレートリポジトリ or 共有パッケージで配布

    2. 用語集（Glossary）:
       → ドメイン固有用語の定義を一元管理
       → 各リポジトリからリンク参照

    3. レビュー基準:
       → ドキュメント変更に対するレビューチェックリスト
       → 用語の一貫性チェック
       → 図の存在確認（分散システムの場合）

    4. 定期監査:
       → 四半期ごとのクロスリポジトリ一貫性チェック
       → 古いドキュメントの検出・アーカイブ
       → 新サービス追加時のドキュメントテンプレート適用
```

---

## 6. Grove との連携

```
Grove での活用:
  1. SCAN フェーズで DA-01〜07 のスクリーニング
  2. docs/ 構造の AP-005（Doc Desert）/ AP-006（Orphaned Docs）と複合評価
  3. SCORE フェーズで Doc Completeness 軸（25%）に DA チェックを統合
  4. Scribe への GROVE_TO_SCRIBE_HANDOFF でドキュメント改善提案

品質ゲート:
  - コード変更にドキュメント更新なし → PR ワーニング（DA-01 防止）
  - ドキュメントオーナー 1 人 → 共有オーナーシップ移行（DA-02 防止）
  - ADR ディレクトリ不在 → 作成提案（DA-04 防止）
  - Wiki 依存 → リポジトリ内 docs/ 移行提案（DA-05 防止）
  - 分散システムに図なし → ダイアグラム作成提案（DA-06 防止）
  - 実装 PR にドキュメントなし → チェックリスト適用（DA-07 防止）
```

**Source:** [DeepDocs: Technical Documentation Best Practices](https://deepdocs.dev/technical-documentation-best-practices/) · [Qodo: Code Documentation Best Practices](https://www.qodo.ai/blog/code-documentation-best-practices-2026/) · [42 Coffee Cups: Technical Documentation Best Practices 2025](https://www.42coffeecups.com/blog/technical-documentation-best-practices)
