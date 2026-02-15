# Nexus Integration

AUTORUN I/O templates and NEXUS_HANDOFF format for Latch.

---

## AUTORUN Agent Context

When Nexus invokes Latch in AUTORUN mode:

```
_AGENT_CONTEXT:
  Role: Latch
  Task: [具体的なタスク]
  Input:
    request: [ユーザーの要求]
    current_hooks: [現在のフック設定概要]
    project_type: [プロジェクトタイプ]
  Constraints:
    - settings.json のみ変更（hooks セクション）
    - 変更前にバックアップ作成
    - セッション再起動リマインド必須
  Expected_output:
    - 設定変更内容
    - 作成したスクリプト
    - 検証結果
```

---

## AUTORUN Step Complete

After Latch completes its task:

```
_STEP_COMPLETE:
  Agent: Latch
  Status: SUCCESS|PARTIAL|BLOCKED|FAILED
  Output:
    hooks_configured: [設定したフック一覧]
    scripts_created: [作成したスクリプト一覧]
    settings_modified: true|false
    backup_created: true|false
    verification: [検証結果の概要]
  Risks:
    - [リスク項目があれば記載]
  Reminders:
    - セッション再起動が必要
  Next: [次のエージェント]|DONE
```

---

## NEXUS_HANDOFF Format

When returning results to Nexus hub:

```markdown
## NEXUS_HANDOFF

### Step: Latch
**Summary:** [1行の要約]

### Changes
- **settings.json:** [変更内容]
- **Scripts:** [作成/変更したスクリプト]
- **Backup:** [バックアップ情報]

### Verification
- `/hooks` で確認: [確認結果]
- `claude --debug` テスト: [テスト結果]
- スクリプト単体テスト: [テスト結果]

### Risks & Follow-ups
- [リスクや後続タスク]
- セッション再起動が必要

### Next
**Agent:** [次のエージェント]
**Action:** [次のアクション]
```

---

## Nexus Routing Integration

Latch is routed by Nexus for the following task types:

| Task Type | Chain | When |
|-----------|-------|------|
| HOOKS | Latch | Claude Code フックの設定・デバッグ |
| HOOKS/security | Sentinel → Latch | セキュリティ要件をフックで実装 |
| HOOKS/quality | Latch → Radar | 品質ゲートフック＋テスト検証 |
| INFRA/hooks | Latch → Gear | フック＋CI/CD 連携 |
