# Handoff Formats

Templates for agent-to-agent handoffs involving Latch.

---

## Outbound: Latch → Gear

When a hook requires Git hook or CI/CD integration beyond Claude Code hooks.

```markdown
## NEXUS_HANDOFF

### Step: Latch → Gear
**Agent:** Latch
**Summary:** Claude Code フックの設定完了。Git hooks との連携が必要。

### Findings
- **Configured hooks:** [設定したフック一覧]
- **Integration need:** [Gear に依頼する内容]
  - 例: pre-commit で同等の検証を CI でも実行
  - 例: Husky/Lefthook で lint-staged と連携

### Artifacts
- `~/.claude/settings.json` (hooks セクション更新済み)
- `~/.claude/hooks/[script-name].sh` (フックスクリプト)

### Risks
- Claude Code hooks と Git hooks の重複実行
- CI パイプラインとの検証ロジック不整合

### Pending
- Git hooks 側での同等検証の実装
- CI/CD パイプラインへの統合

### Next
**Agent:** Gear
**Action:** Git hooks / CI パイプラインに同等の検証を追加
```

---

## Outbound: Latch → Hearth

When hook setup requires shell environment or dotfile changes.

```markdown
## NEXUS_HANDOFF

### Step: Latch → Hearth
**Agent:** Latch
**Summary:** Claude Code フックの設定完了。シェル環境の調整が必要。

### Findings
- **Configured hooks:** [設定したフック一覧]
- **Environment need:** [Hearth に依頼する内容]
  - 例: フックスクリプトが使用するツールの PATH 設定
  - 例: シェルエイリアスの追加（claude --debug 等）

### Artifacts
- `~/.claude/settings.json` (hooks セクション更新済み)
- `~/.claude/hooks/` (フックスクリプトディレクトリ)

### Next
**Agent:** Hearth
**Action:** シェル環境の設定調整
```

---

## Outbound: Latch → Canvas

When hook configuration needs visual documentation.

```markdown
## NEXUS_HANDOFF

### Step: Latch → Canvas
**Agent:** Latch
**Summary:** Claude Code フック設定のフロー図作成を依頼。

### Findings
- **Hook configuration:** [設定内容の概要]
- **Visualization need:** イベントフロー、matcher ロジック、判定フローの図解

### Artifacts
- `~/.claude/settings.json` (hooks セクション)
- フック構成の概要テキスト

### Next
**Agent:** Canvas
**Action:** Mermaid フローチャートまたはシーケンス図の作成
```

---

## Outbound: Latch → Sentinel

When hook analysis reveals security gaps beyond hooks' scope.

```markdown
## NEXUS_HANDOFF

### Step: Latch → Sentinel
**Agent:** Latch
**Summary:** フック設定中にセキュリティギャップを発見。

### Findings
- **Security gaps:** [発見したギャップ]
  - 例: フックでは防げない SAST レベルの脆弱性
  - 例: 入力検証が必要だがフックのスコープ外
- **Hook coverage:** [フックでカバーできている範囲]

### Risks
- フックだけではカバーできないセキュリティ要件
- 静的解析が必要な脆弱性パターン

### Next
**Agent:** Sentinel
**Action:** セキュリティ監査の実施、フックではカバーできない領域の対応
```

---

## Inbound: Sentinel → Latch

When Sentinel identifies security requirements addressable by hooks.

```markdown
## NEXUS_HANDOFF

### Step: Sentinel → Latch
**Agent:** Sentinel
**Summary:** セキュリティ監査結果。フックで対応可能な項目あり。

### Findings
- **Hook-addressable issues:**
  - [例: 機密ファイルへの書き込み制限]
  - [例: 危険なコマンドの実行ブロック]
  - [例: シークレット漏洩の検出]
- **Severity:** [リスクレベル]

### Recommended Hooks
- PreToolUse (Write|Edit): ファイルパス検証
- PreToolUse (Bash): コマンド安全性検証
- Stop: セキュリティチェック完了の確認

### Next
**Agent:** Latch
**Action:** 推奨フックの設定・実装
```

---

## Inbound: Sigil → Latch

When Sigil discovers project patterns suitable for Claude Code hooks.

```markdown
## NEXUS_HANDOFF

### Step: Sigil → Latch
**Agent:** Sigil
**Summary:** プロジェクト分析結果。Claude Code フック推奨事項あり。

### Findings
- **Project type:** [検出されたプロジェクトタイプ]
- **Recommended hooks:**
  - [例: SessionStart でプロジェクトコンテキスト自動ロード]
  - [例: PostToolUse で自動フォーマット]
  - [例: Stop でプロジェクト固有の品質チェック]
- **Tech stack:** [使用技術スタック]

### Artifacts
- プロジェクト分析レポート
- 検出されたパターン/規約情報

### Next
**Agent:** Latch
**Action:** プロジェクトに最適なフックセットの設定
```

---

## Inbound: Gear → Latch

When Gear encounters Claude Code hook needs during DevOps work.

```markdown
## NEXUS_HANDOFF

### Step: Gear → Latch
**Agent:** Gear
**Summary:** DevOps 設定中に Claude Code フックの必要性を検出。

### Findings
- **Context:** [Gear が作業していた内容]
- **Hook need:** [必要なフックの概要]
  - 例: CI と同等のリント設定を Claude Code セッション内でも実行
  - 例: ビルド検証をセッション終了前に強制
- **Current CI config:** [関連する CI 設定情報]

### Next
**Agent:** Latch
**Action:** Claude Code フックの設定で CI 品質ゲートをローカルにも適用
```
