# Nexus Proactive Mode Reference

`/Nexus` のみで呼び出された場合（引数なし）に自動発動するモード。

---

## トリガー条件

| 条件 | 発動 |
|------|------|
| `/Nexus` のみ（引数なし） | ✅ PROACTIVE_MODE |
| `/Nexus [タスク]` | ❌ 通常ルーティング |
| `## NEXUS_AUTORUN` | ❌ 通常AUTORUN |
| `## NEXUS_HANDOFF` | ❌ 継続処理 |

---

## 分析フェーズ

### Phase 0-A: プロジェクト状態スキャン

**1. Git Status チェック**
```bash
git status --porcelain
```
- 未コミット変更の有無
- ステージング状態
- 未追跡ファイル

**2. Activity Log 確認**
```
.agents/PROJECT.md → Activity Log セクション
```
- 最終アクティビティ日時
- 最終エージェント
- 最終作業内容

**3. コミット傾向分析**
```bash
git log --oneline -10
```
- 直近の作業パターン
- 頻出ファイル/ディレクトリ
- コミットの種類（feat/fix/refactor等）

---

### Phase 0-B: 健全性評価

4つの指標でプロジェクト健全性を評価:

| 指標 | 評価方法 | 状態 |
|------|----------|------|
| `test_health` | テスト実行結果、カバレッジ | 🟢/🟡/🔴 |
| `security_health` | 脆弱性スキャン、依存関係 | 🟢/🟡/🔴 |
| `code_health` | lint警告、型エラー | 🟢/🟡/🔴 |
| `doc_health` | README更新、JSDoc率 | 🟢/🟡/🔴 |

**評価基準:**
- 🟢 良好: 問題なし
- 🟡 注意: 軽微な問題あり
- 🔴 要対応: 即時対応が必要

---

### Phase 0-C: 推奨アクション生成

**優先度決定ロジック:**

| 優先度 | 条件 |
|--------|------|
| 🔴 高 | セキュリティ問題、テスト失敗、ビルドエラー |
| 🟡 中 | lint警告、カバレッジ低下、ドキュメント不足 |
| 🟢 低 | リファクタリング機会、最適化提案 |

**カテゴリ別提案テンプレート:**

```yaml
# テスト関連
- condition: "テストが失敗している"
  priority: 🔴
  suggestion: "失敗テストの修正"
  agent: Radar
  reason: "CI/CDが通らない状態を解消"

- condition: "カバレッジが80%未満"
  priority: 🟡
  suggestion: "テストカバレッジ向上"
  agent: Radar
  reason: "リグレッション防止のため"

# セキュリティ関連
- condition: "npm audit に脆弱性"
  priority: 🔴
  suggestion: "脆弱性のある依存関係の更新"
  agent: Sentinel
  reason: "セキュリティリスクの排除"

# コード品質
- condition: "lint警告が10件以上"
  priority: 🟡
  suggestion: "lint警告の解消"
  agent: Zen
  reason: "コード品質の維持"

- condition: "未使用コードが検出された"
  priority: 🟢
  suggestion: "デッドコードの削除"
  agent: Sweep
  reason: "メンテナンス性向上"

# ドキュメント
- condition: "READMEが30日以上更新なし"
  priority: 🟢
  suggestion: "READMEの更新"
  agent: Quill
  reason: "ドキュメントの鮮度維持"

# 継続作業
- condition: "未コミット変更がある"
  priority: 🟡
  suggestion: "前回の作業を継続"
  agent: "(前回のエージェント)"
  reason: "中断された作業の完了"
```

---

## 出力フォーマット

```markdown
## Nexus プロアクティブ分析

### プロジェクト状態

| 項目 | 状態 |
|------|------|
| 最終アクティビティ | [YYYY-MM-DD] - [Agent] - [内容] |
| 未コミット変更 | [なし / X files modified] |
| 健全性 | test: 🟢 / security: 🟢 / code: 🟡 / doc: 🟢 |

### 推奨アクション

| # | 優先度 | 提案 | エージェント | 理由 |
|---|--------|------|--------------|------|
| 1 | 🔴 高 | [提案内容] | [Agent] | [理由] |
| 2 | 🟡 中 | [提案内容] | [Agent] | [理由] |
| 3 | 🟢 低 | [提案内容] | [Agent] | [理由] |

### 次のステップ

推奨アクションを実行する場合は番号を選択してください。
新しいタスクを指示する場合は `/Nexus [タスク]` と入力してください。
```

---

## ユーザーインタラクション

プロアクティブ分析後のオプション:

```yaml
ON_PROACTIVE_START:
  timing: BEFORE_START
  when: "/Nexus が引数なしで呼び出された場合"
  options:
    - label: "推奨アクション #1 を実行（推奨）"
      description: "[最優先の提案内容]"
    - label: "推奨アクション #2 を実行"
      description: "[次の提案内容]"
    - label: "前回の作業を継続"
      description: "Activity Log の最終作業を再開"
    - label: "新しいタスクを指示"
      description: "/Nexus [タスク] で新規タスクを開始"
```

---

## AUTORUN との関係

プロアクティブモードは AUTORUN の**前段階**として位置づけ:

```
/Nexus (引数なし)
    ↓
Phase 0: PROACTIVE_ANALYSIS
    ↓
ユーザー選択
    ↓
├─ 推奨アクション選択 → AUTORUN_FULL 開始
├─ 前回作業継続 → AUTORUN_FULL 開始
└─ 新規タスク指示 → 通常ルーティング
```

既存の AUTORUN モードとの後方互換性は完全に維持される。

---

## 軽量実行のガイドライン

プロアクティブ分析が重くならないよう、以下を遵守:

1. **段階的実行**: 必要な情報のみを順次取得
2. **キャッシュ活用**: 同一セッション内は再分析しない
3. **タイムアウト**: 各チェックは5秒以内に完了
4. **スキップ条件**: `.agents/PROJECT.md` がなければ簡易分析のみ
