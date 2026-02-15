# Interaction Trigger Templates

YAML templates for `AskUserQuestion` at Latch decision points.

---

## ON_HOOK_SCOPE

When the user's request could be addressed by multiple hook events.

```yaml
trigger: ON_HOOK_SCOPE
timing: BEFORE_START
questions:
  - question: "フックで対応するスコープを確認します。どの範囲にフックを適用しますか？"
    header: "Hook Scope"
    options:
      - label: "特定ツールのみ（推奨）"
        description: "Write/Edit/Bash など、対象ツールを限定してフックを適用"
      - label: "特定イベントのみ"
        description: "PreToolUse/Stop/SessionStart など、対象イベントを限定"
      - label: "ワークフロー全体"
        description: "複数イベントにまたがる包括的なフックセットを構成"
```

---

## ON_BLOCKING_HOOK

When the proposed hook uses exit code 2 (blocks Claude operations).

```yaml
trigger: ON_BLOCKING_HOOK
timing: ON_RISK
questions:
  - question: "提案するフックは Claude の操作をブロックする可能性があります。ブロッキング動作を許可しますか？"
    header: "Blocking"
    options:
      - label: "ブロッキングフックを許可（推奨）"
        description: "条件に合致した場合、Claude の操作を中断して確認を求める"
      - label: "警告のみ（ブロックしない）"
        description: "systemMessage で警告を出すが、操作は続行する"
      - label: "ログのみ"
        description: "記録するだけで、操作にも警告にも影響しない"
```

---

## ON_EXISTING_HOOKS

When existing hooks conflict with or overlap proposed hooks.

```yaml
trigger: ON_EXISTING_HOOKS
timing: ON_DECISION
questions:
  - question: "既存のフックと提案するフックが重複または競合しています。どう対処しますか？"
    header: "Conflict"
    options:
      - label: "既存フックを置換（推奨）"
        description: "既存のフックを新しいフックで上書きする"
      - label: "既存フックに追加"
        description: "両方のフックを並列で実行する（パフォーマンスに影響の可能性あり）"
      - label: "既存フックを維持"
        description: "提案を取り下げ、現在の設定を変更しない"
```

---

## ON_SETTINGS_MODIFY

When modifying the user's settings.json.

```yaml
trigger: ON_SETTINGS_MODIFY
timing: ON_RISK
questions:
  - question: "settings.json のフック設定を変更します。変更方法を選択してください。"
    header: "Settings"
    options:
      - label: "バックアップして変更（推奨）"
        description: "settings.json.bak を作成してから変更を適用"
      - label: "直接変更"
        description: "バックアップなしで即座に変更（設定が少ない場合に推奨）"
      - label: "差分のみ表示"
        description: "変更内容を表示するだけで、実際の変更は行わない"
```

---

## ON_BROAD_MATCHER

When the proposed matcher is `*` or a regex matching many tools.

```yaml
trigger: ON_BROAD_MATCHER
timing: ON_RISK
questions:
  - question: "提案するマッチャー ('*' または広範囲の正規表現) は多くのツール呼び出しに影響します。続行しますか？"
    header: "Matcher"
    options:
      - label: "広範囲マッチャーを許可（推奨）"
        description: "Stop/SessionStart 等のイベントでは '*' が一般的で安全"
      - label: "対象を限定"
        description: "特定ツールのみにマッチするよう修正して適用"
      - label: "スキップ"
        description: "このフックの追加をスキップする"
```
