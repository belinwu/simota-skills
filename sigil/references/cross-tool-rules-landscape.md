# Cross-Tool Rules Landscape

> CLAUDE.md vs .cursorrules vs .windsurfrules vs AGENTS.md vs Copilot instructions — 比較、相互運用、rulesync 戦略

## 1. ルールファイル比較マトリクス

| 特性 | CLAUDE.md | .cursorrules | .windsurfrules | AGENTS.md | .github/copilot-instructions.md |
|------|-----------|-------------|----------------|-----------|-------------------------------|
| ツール | Claude Code | Cursor | Windsurf | Cline/Roo | GitHub Copilot |
| 場所 | ルート / サブディレクトリ | ルート | ルート | ルート / サブディレクトリ | .github/ |
| 階層対応 | ✅（ディレクトリ別） | ❌ | ❌ | ✅（ディレクトリ別） | ❌ |
| @import | ✅ | ❌ | ❌ | ❌ | ❌ |
| フック連携 | ✅（hooks） | ❌ | ❌ | ❌ | ❌ |
| スキルシステム | ✅（skills/） | ❌ | ❌ | ❌ | ❌ |
| 動的コンテキスト | ✅（`!`cmd``） | ❌ | ❌ | ❌ | ❌ |
| フォーマット | Markdown | Markdown/Text | Markdown/Text | Markdown | Markdown |
| 成熟度 | 高 | 高 | 中 | 中 | 中 |

---

## 2. 各ツールの特徴

### CLAUDE.md（Claude Code）

**独自の強み:**
- 階層的ルール適用（ディレクトリスコープ）
- `@import` による分割管理
- `!`command`` 動的コンテキスト注入
- hooks による自動化
- skills/ による拡張

**制限:**
- Claude Code 専用（他ツールは無視）

### .cursorrules（Cursor）

**特徴:**
- `.cursorrules`（レガシー）→ `.cursor/rules/` ディレクトリ（新）に移行中
- パスベースのルール適用をサポート（新形式）
- コミュニティルールの共有文化が発達（cursor.directory）

```
.cursor/
├── rules/
│   ├── global.md          # 全ファイルに適用
│   ├── typescript.md      # *.ts に適用
│   └── testing.md         # *test*.ts に適用
```

### .windsurfrules（Windsurf）

**特徴:**
- `.windsurfrules` にプロジェクトルールを記述
- Cascade（AI アシスタント）が参照
- シンプルなフラット構造

### AGENTS.md（Cline/Roo Code）

**特徴:**
- 階層対応（ディレクトリ別 AGENTS.md）
- エージェントモードごとのルール分離
- ファイル・ディレクトリパターンでスコープ指定可能

### .github/copilot-instructions.md（GitHub Copilot）

**特徴:**
- GitHub リポジトリ設定と統合
- VS Code / JetBrains / GitHub.com で共通
- パスベースのスコープは未サポート

---

## 3. 共通記述パターン

### ツール横断で有効なルール記述

すべてのツールで効果的なルール記述パターン:

| パターン | 説明 | 例 |
|---------|------|-----|
| **禁止リスト** | 使ってはいけないもの | `console.log を本番コードに残さない` |
| **パターン指定** | 使うべきパターン | `エラーハンドリングは Result 型を使う` |
| **ファイル構成** | ディレクトリルール | `コンポーネントは components/ に配置` |
| **テスト方針** | テスト記述ルール | `各 API エンドポイントに統合テストを書く` |
| **コメント方針** | ドキュメント規約 | `公開関数には JSDoc を書く` |

### ツール固有のルールが必要な場面

| 場面 | 対応 |
|------|------|
| ツール固有の API 操作 | 各ツールのルールファイルに個別記述 |
| MCP サーバー設定 | Claude Code 固有（settings.json） |
| エディタ操作の制御 | 各エディタのルールファイル |

---

## 4. 相互運用戦略

### Strategy A: 共通ルールファイル + ツール固有ファイル

```
project/
├── .ai-rules/                    # 共通ルール（ツール非依存）
│   ├── coding-standards.md
│   ├── testing-policy.md
│   └── architecture.md
├── CLAUDE.md                     # @import .ai-rules/* + Claude 固有
├── .cursorrules                  # 共通ルール参照 + Cursor 固有
├── .windsurfrules                # 共通ルール参照 + Windsurf 固有
└── .github/copilot-instructions.md  # 共通ルール転記 + Copilot 固有
```

**利点**: 共通部分の重複を最小化
**課題**: @import を持たないツールは手動転記が必要

### Strategy B: rulesync ツール

自動同期ツールを使用してルールを一元管理:

```bash
# rulesync 的なアプローチ
# 1. 共通ルールファイルを編集
# 2. ビルドスクリプトで各ツール形式に変換
npm run sync-rules
```

**同期対象マッピング:**

| ソース | → | ターゲット |
|-------|---|-----------|
| `.ai-rules/*.md` | → | `CLAUDE.md`（@import） |
| `.ai-rules/*.md` | → | `.cursorrules`（結合） |
| `.ai-rules/*.md` | → | `.windsurfrules`（結合） |
| `.ai-rules/*.md` | → | `.github/copilot-instructions.md`（結合） |

### Strategy C: CLAUDE.md をマスターにする

CLAUDE.md の @import 機能を活かし、マスターとして他ツール向けに変換:

```bash
# CLAUDE.md → 他ツールへの変換スクリプト
# 1. CLAUDE.md と import ファイルを結合
# 2. Claude 固有の構文（!`cmd`）を除去
# 3. 各ツール形式に出力
```

---

## 5. パスベーススコーピングの比較

| ツール | スコープ方法 |
|--------|------------|
| CLAUDE.md | ディレクトリに CLAUDE.md を配置 |
| .cursor/rules/ | ファイルパターンでマッチング |
| AGENTS.md | ディレクトリに AGENTS.md を配置 |
| .windsurfrules | スコープなし（グローバルのみ） |
| Copilot | スコープなし（グローバルのみ） |

### モノレポでの考慮

```
monorepo/
├── CLAUDE.md                # ルート共通ルール
├── packages/
│   ├── frontend/
│   │   └── CLAUDE.md        # React 固有ルール
│   └── backend/
│       └── CLAUDE.md        # API 固有ルール
```

---

## 6. Sigil への示唆

### スキル生成時の考慮

1. **ルールファイル検出**: SCAN フェーズで全ルールファイルを検出
   - CLAUDE.md, .cursorrules, .windsurfrules, AGENTS.md, copilot-instructions.md
2. **共通ルール抽出**: 複数ツールで共通のルールを特定
3. **Claude 固有最適化**: Claude Code の強み（@import, !`cmd`, hooks, skills）を活用したスキル生成
4. **互換性考慮**: 生成するスキルが他ツールのルールと矛盾しないことを確認

### ルールファイル自動生成

Sigil が CLAUDE.md 自体の生成・更新を支援する可能性:
- プロジェクト分析結果 → CLAUDE.md の推奨ルール提案
- 既存の .cursorrules → CLAUDE.md への変換支援
- CLAUDE.md 成熟度レベルの評価と改善提案

**Source:** [Cursor Rules Documentation](https://docs.cursor.com/context/rules-for-ai) · [Windsurf Rules](https://docs.codeium.com/windsurf/memories#rules) · [AGENTS.md (Cline/Roo)](https://docs.cline.bot/improving-your-prompting/agents-md) · [GitHub Copilot Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot) · [rulesync (npm)](https://www.npmjs.com/package/rulesync)
