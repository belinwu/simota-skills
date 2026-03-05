# Codebase Organization Anti-Patterns

> フォルダ構造設計の失敗パターン、レイヤーベース vs フィーチャーベースの罠、スケーラビリティ問題

## 1. コードベース構造 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **CO-01** | **Type-First Trap（型別構造の罠）** | components/hooks/utils/styles で全ファイルを分類 | 1機能の理解に5-7ディレクトリ横断、変更が多フォルダに波及 | Feature-based organization への移行、Feature-Sliced Design 検討 |
| **CO-02** | **Copy-Paste Discovery（コピペ発見）** | 構造の見通しが悪く既存コードが見つからずコピペ | 同一ロジックが複数箇所に散在、リファクタ時に漏れ発生 | 機能別グルーピング、barrel export による公開 API 明確化 |
| **CO-03** | **Convention Mismatch（規約不一致）** | 言語固有の慣習を無視した構造設計 | Go で src/ 配置、Python で __init__.py 未配置、Java でパッケージ規約違反 | 言語検出 → 言語固有テンプレート適用（Go: cmd/internal/, Python: pyproject.toml 等） |
| **CO-04** | **Premature Abstraction（早すぎる抽象化）** | 初期段階で過度に階層化した構造を設計 | 3ファイルのプロジェクトに5層のディレクトリ、空フォルダ多数 | 現在のサイズに適した構造、成長に応じて段階的にリファクタ |
| **CO-05** | **Naming Collision（命名衝突）** | lib/shared/utils/helpers/common が混在 | 同じ目的のディレクトリが複数存在、新規ファイルの配置先が曖昧 | 1つの目的に1つの名前、チーム合意の命名規約 |
| **CO-06** | **Cyclic Module Dependency（循環モジュール依存）** | モジュール間の双方向依存が発生 | 独立テスト・独立デプロイ不能、変更影響の予測不能 | 依存方向の一方向化、共有インターフェースの抽出、イベントバスによる分離 |
| **CO-07** | **Test-Source Divorce（テスト-ソース離婚）** | テストとソースの対応関係が崩壊 | テストファイルの配置が不統一、カバレッジ測定困難、CI設定の複雑化 | co-location（Go/Rust 式）or centralized（JS/Python 式）を1つ選び統一 |

---

## 2. 構造パターン比較

```
Type-Based（レイヤーベース）:

  src/
    components/     ← UIコンポーネント全部
    hooks/          ← カスタムフック全部
    services/       ← API呼び出し全部
    utils/          ← ユーティリティ全部
    styles/         ← スタイル全部

  問題:
    → 低凝集: 関連する機能が 5-7 ディレクトリに散在
    → 高結合: 無関係なモジュールが相互インポート
    → 変更増幅: 1機能の変更が多数のフォルダに波及
    → チーム並行開発が困難（同じフォルダを複数チームが変更）

Feature-Based（機能ベース）:

  src/
    features/
      auth/
        components/
        hooks/
        services/
        index.ts      ← 公開 API（barrel export）
      user/
        components/
        hooks/
        services/
        index.ts
    shared/
      ui/
      utils/

  利点:
    → 高凝集: 関連ファイルが1ディレクトリに集約
    → 低結合: 公開 API 経由のみでアクセス
    → チーム独立: 各チームが自分の feature を独立開発
    → 安全なリファクタ: 内部変更が外部に影響しない

Feature-Sliced Design（FSD）:

  src/
    app/              ← 初期化、ルーティング
    pages/            ← ルーティング可能な画面
    widgets/          ← 複合セクション
    features/         ← ユーザーインタラクション
    entities/         ← ビジネスモデル
    shared/           ← 再利用コード

  依存ルール: app → pages → widgets → features → entities → shared
  → 上位レイヤーは下位に依存可能、逆は禁止
  → 各スライスは index.ts で公開 API を制御

  適用条件:
    ✓ 複数ビジネスドメイン、長期プロダクト、チーム拡大
    ✗ 小規模プロトタイプ、マーケティングサイト、個人開発
```

---

## 3. 構造選択の判断基準

```
プロジェクト規模別推奨:

  規模          | ファイル数  | 推奨構造
  ------------|----------|-------------------
  小規模        | ~20      | フラット構造（サブディレクトリ最小限）
  中規模        | 20-100   | Feature-Based（機能別グルーピング）
  大規模        | 100-500  | Feature-Sliced Design or DDD
  超大規模      | 500+     | モノレポ + パッケージ分割

  判断フロー:
    Q1: チーム人数は？
      1-3人 → シンプルな Feature-Based
      4-10人 → Feature-Based + 公開 API 制御
      10人+ → FSD or DDD + モジュール境界強制

    Q2: ドメイン複雑性は？
      単純（CRUD中心） → レイヤーベースでも可
      中程度 → Feature-Based
      複雑（複数ドメイン） → DDD + Bounded Context

    Q3: フレームワーク規約は？
      強い規約あり（Next.js App Router, Rails） → フレームワーク規約に従う
      弱い or なし → Feature-Based を基本選択
```

---

## 4. スケーラビリティの落とし穴

```
成長に伴う構造劣化パターン:

  Stage 1（初期）:
    → フラット構造で問題なし
    → 全員がすべてのファイルを把握

  Stage 2（成長期）:
    → ファイル数 50+ で発見性が低下
    → 「どこに置けばいいかわからない」問題の発生
    → CO-01（Type-First Trap）に陥りやすい

  Stage 3（成熟期）:
    → 100+ ファイルで構造のリファクタが必要
    → しかしリファクタのコストが高く先送り
    → CO-02（Copy-Paste Discovery）が蔓延

  Stage 4（危機）:
    → God Directory（AP-001）や Flat Hell（AP-008）が定着
    → 新メンバーのオンボーディング時間が倍増
    → 構造変更の合意形成が困難

  予防策:
    → Stage 2 で Feature-Based への移行を計画
    → 20 ファイル超で最初のグルーピングを開始
    → 50 ファイル超で公開 API（barrel export/index.ts）を導入
    → 100 ファイル超でモジュール境界の強制を検討
```

---

## 5. 命名規約の統一

```
ディレクトリ命名ガイド:

  統一すべき名前:
    ソースコード    → src/ (Go 以外) or cmd/internal/ (Go)
    テスト         → tests/ (centralized) or *.test.* (co-located)
    ドキュメント    → docs/
    設定           → config/
    スクリプト      → scripts/
    共有コード      → shared/ (1つだけ選ぶ、lib/utils/helpers/common は NG)

  ファイル命名:
    → 言語規約に従う（CamelCase/snake_case/kebab-case）
    → 目的を名前に含める（auth.service.ts, auth.controller.ts）
    → テストファイルはソースと対応させる（auth.service.test.ts）

  アンチパターン:
    ❌ lib/ + shared/ + utils/ + helpers/ + common/ の併存
    ❌ 言語規約と異なるケース使用
    ❌ 略語の多用（util, svc, mgr, hdlr）
    ❌ 連番やバージョン付きディレクトリ（v2/, new-src/）
```

---

## 6. Grove との連携

```
Grove での活用:
  1. DETECT フェーズで言語検出 → 構造パターン推奨
  2. SCAN フェーズで CO-01〜07 のスクリーニング
  3. AUDIT フェーズで AP-001〜016 との複合評価
  4. PLAN フェーズで規模別の構造移行提案

品質ゲート:
  - Type-Based 検出 → Feature-Based 移行提案（CO-01 防止）
  - 同一ロジック重複 → 共有モジュール抽出提案（CO-02 防止）
  - 言語規約違反 → 自動修正提案（CO-03 防止）
  - 空ディレクトリ多数 → 構造簡素化提案（CO-04 防止）
  - 同目的ディレクトリ重複 → 統合提案（CO-05 防止）
  - 循環依存検出 → 依存方向整理提案（CO-06 防止）
```

**Source:** [Feature-Sliced Design: Frontend Folder Structure](https://feature-sliced.design/blog/frontend-folder-structure) · [Iterators: Project Codebase Organization](https://www.iteratorshq.com/blog/a-comprehensive-guide-on-project-folder-organization/) · [GitHub Well-Architected: Anti-Patterns](https://wellarchitected.github.com/library/scenarios/anti-patterns/)
