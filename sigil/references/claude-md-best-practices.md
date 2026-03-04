# CLAUDE.md Best Practices

> 成熟度レベル、含めるべき内容と除外すべき内容、RFC 2119 言語、アンチパターン、@import 構文

## 1. CLAUDE.md 成熟度モデル（L0-L6）

| レベル | 名称 | 特徴 | 典型的な内容 |
|--------|------|------|-------------|
| L0 | Absent | CLAUDE.md なし | — |
| L1 | Minimal | 基本規約のみ | コーディングスタイル、言語設定 |
| L2 | Structured | セクション分け | テスト方針、コミット規約、ツール設定 |
| L3 | Comprehensive | 網羅的なガイド | アーキテクチャ方針、セキュリティルール、CI/CD |
| L4 | Composable | @import で分割管理 | ドメイン別ファイル、チーム別設定 |
| L5 | Adaptive | 条件分岐付き | ブランチ別、環境別のルール |
| L6 | Self-Evolving | 自動更新機構 | フック連携、CI 統合でルール自動更新 |

### 推奨進化パス

```
L0 → L1: まず言語・スタイルルールだけ書く
L1 → L2: セクション分けと具体的な指示を追加
L2 → L3: アーキテクチャ・セキュリティ方針を追加
L3 → L4: 肥大化したら @import で分割
L4 → L5: 環境依存ルールの条件分岐
L5 → L6: フック・CI でルール自動保守
```

---

## 2. 含めるべき内容

### 高効果（必須級）

| カテゴリ | 具体例 | 理由 |
|---------|-------|------|
| **コーディング規約** | インデント、命名規則、import 順序 | 一貫性の基盤 |
| **テスト方針** | テストフレームワーク、カバレッジ基準 | 品質の基盤 |
| **コミット規約** | Conventional Commits、署名ルール | 履歴の品質 |
| **アーキテクチャ方針** | レイヤー構成、モジュール境界 | 設計の一貫性 |
| **禁止事項** | 使用禁止の API、避けるべきパターン | ミスの予防 |
| **エラー処理方針** | エラーハンドリングパターン | 堅牢性 |

### 中効果（推奨）

| カテゴリ | 具体例 |
|---------|-------|
| **依存関係方針** | 許可されたライブラリ、バージョン固定ルール |
| **セキュリティルール** | シークレット管理、入力検証 |
| **パフォーマンス基準** | N+1 禁止、キャッシュ方針 |
| **ドキュメント方針** | JSDoc/TSDoc 必須箇所 |

### 低効果（オプション）

| カテゴリ | 注意 |
|---------|------|
| プロジェクト説明 | 長すぎるとノイズ |
| 変更履歴 | 別ファイルが適切 |
| チーム構成 | CLAUDE.md の目的外 |

---

## 3. 除外すべき内容（アンチパターン）

### 過剰指定（Overspecification）

```markdown
❌ BAD: 全関数に JSDoc を書くこと。パラメータの説明は必ず含めること。
         戻り値の型は @returns で記述すること。例外は @throws で記述すること。

✅ GOOD: 公開 API には JSDoc を書く。パラメータと戻り値を含める。
```

**問題**: 過剰な指示は遵守率を下げ、重要なルールが埋もれる。

### スタイルルールの直接記述

```markdown
❌ BAD: インデントは2スペース。セミコロンなし。シングルクォート使用。
         trailing comma は常に付ける。行の最大長は100文字。

✅ GOOD: コードスタイルは .prettierrc / .eslintrc に従う。
```

**理由**: ツール設定ファイルが正（Single Source of Truth）。CLAUDE.md に重複記述すると乖離リスク。

### 曖昧な指示

```markdown
❌ BAD: きれいなコードを書いてください。
❌ BAD: パフォーマンスに注意してください。

✅ GOOD: React コンポーネントでは useMemo/useCallback を使用する基準:
         - 計算コストが O(n²) 以上の場合
         - 子コンポーネントが React.memo でラップされている場合
```

### 矛盾するルール

複数の CLAUDE.md ファイル間で矛盾が生じやすいポイント:
- ルートと子ディレクトリで異なるスタイル指定
- テスト方針の矛盾（「全てテスト」vs「重要な部分のみ」）

---

## 4. RFC 2119 言語パターン

[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) のキーワードで指示の強度を明確化:

| キーワード | 強度 | 用途 |
|-----------|------|------|
| **MUST** / **MUST NOT** | 絶対的要件 | セキュリティ、データ整合性 |
| **SHOULD** / **SHOULD NOT** | 強い推奨 | ベストプラクティス |
| **MAY** | オプション | 好み、状況依存 |

```markdown
## セキュリティ
- API キーは MUST NOT ハードコードする
- 入力値は MUST サニタイズする

## テスト
- ビジネスロジックには SHOULD ユニットテストを書く
- UI コンポーネントは MAY スナップショットテストを使用する
```

**Sigil での活用**: 生成するスキルの指示レベルに RFC 2119 言語を適用し、強制度を明確化。

---

## 5. @import 構文（Composable CLAUDE.md）

### 基本構文

```markdown
# CLAUDE.md

@import ./docs/coding-standards.md
@import ./docs/testing-policy.md
@import ./docs/security-rules.md
```

### 配置パターン

```
project/
├── CLAUDE.md                    # ルート（@import でアセンブル）
├── docs/
│   ├── coding-standards.md      # コーディング規約
│   ├── testing-policy.md        # テスト方針
│   └── security-rules.md       # セキュリティルール
├── packages/
│   └── api/
│       └── CLAUDE.md            # パッケージ固有ルール
└── .claude/
    └── settings.json
```

### 分割の基準

| 分割すべき時 | 分割しない方が良い時 |
|------------|-------------------|
| 500行超 | 100行未満 |
| 複数チームが異なるセクションを管理 | 単一チーム |
| ドメイン別に異なるルール | 統一ルール |
| 頻繁に変更されるセクションがある | 変更頻度が均一 |

---

## 6. 階層的 CLAUDE.md

### 階層と適用順序

```
~/.claude/CLAUDE.md              # グローバル（個人設定）
project/CLAUDE.md                # プロジェクトルート
project/packages/api/CLAUDE.md   # パッケージ/ディレクトリ固有
```

**適用ルール**: 下位が上位を上書き（より具体的なルールが優先）。

### Sigil への示唆

スキル生成時に CLAUDE.md 階層を考慮:
- ルートの CLAUDE.md と矛盾しないスキルを生成
- パッケージ固有の CLAUDE.md がある場合、そのスコープに合わせたスキルを生成
- CLAUDE.md に記載されたルールをスキル内で重複しない

---

## 7. 効果的な CLAUDE.md の構造テンプレート

```markdown
# Project Rules

## Language & Style
(ツール設定ファイルへの参照、追加ルールのみ)

## Architecture
(レイヤー構成、モジュール境界、依存方向)

## Testing
(フレームワーク、カバレッジ基準、テストパターン)

## Security
(MUST/MUST NOT で記述)

## Git & PR
(コミット規約、ブランチ戦略)

## Do NOT
(禁止事項リスト)
```

**Source:** [Claude Code CLAUDE.md Documentation](https://docs.anthropic.com/en/docs/claude-code/claude-md) · [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) · [Addy Osmani - Claude Code Tips](https://addyosmani.com/blog/claude-code-workflow/) · [CLAUDE.md Maturity Model (Community)](https://www.reddit.com/r/ClaudeAI/comments/claude_md_tips/)
