# Orbit Interaction Trigger Templates

Question templates for `AskUserQuestion` tool.
See SKILL.md INTERACTION_TRIGGERS table for trigger conditions and timing.

## ON_GOAL_CONTRACT_WEAK

```yaml
questions:
  - question: "現在のgoal定義は受け入れ条件が不足しています。どの方針で補強しますか？"
    header: "GoalContract"
    options:
      - label: "ACを3-6件で補強（推奨）"
        description: "測定可能な受け入れ条件を追加して判定可能性を上げる"
      - label: "最小修正のみ"
        description: "現行goalを維持し不足箇所だけ補足する"
      - label: "監査のみ"
        description: "今回は修正せず改善提案レポートのみ出す"
    multiSelect: false
```

## ON_DONE_VERIFICATION_GAP

```yaml
questions:
  - question: "DONE判定に必要な検証証跡が不足しています。どう進めますか？"
    header: "DoneGate"
    options:
      - label: "CONTINUEへ戻す（推奨）"
        description: "DONEを取り下げ、不足検証を実行してから再判定する"
      - label: "条件付きDONE"
        description: "不足項目を既知リスクとしてdone.mdに明記して完了扱いにする"
      - label: "監査結果のみ"
        description: "判定は変更せず、差分レポートだけ出す"
    multiSelect: false
```

## ON_RESUME_STATE_INCONSISTENCY

```yaml
questions:
  - question: "resume状態がprogress記録と不整合です。どの復旧手順を採用しますか？"
    header: "ResumeState"
    options:
      - label: "progress基準で再同期（推奨）"
        description: "progressの最終iterationを正としてstate.envを再構築する"
      - label: "state.env基準"
        description: "state.envを正としてprogressに注記を追加する"
      - label: "再開せず新規開始"
        description: "状態をリセットして新規ループとして扱う"
    multiSelect: false
```

## ON_AUTOCOMMIT_SCOPE_RISK

```yaml
questions:
  - question: "自動コミットの対象範囲にベースライン dirty ファイルが含まれる可能性があります。どう対処しますか？"
    header: "CommitScope"
    options:
      - label: "候補パスのみステージング（推奨）"
        description: "ループ成果物のみを明示的にステージングし、ベースラインを除外する"
      - label: "差分レビュー後に判断"
        description: "全候補ファイルの差分を表示し、手動でステージング対象を選択する"
      - label: "コミットを保留"
        description: "今回のイテレーションではコミットせず、次の監査で再評価する"
    multiSelect: false
```

## ON_DIRTY_BASELINE_CONFLICT

```yaml
questions:
  - question: "dirty-start ベースラインの判定が困難です（未コミット変更とループ成果物の境界が不明確）。どう進めますか？"
    header: "Baseline"
    options:
      - label: "スナップショット取得して分離（推奨）"
        description: "現在の worktree 状態を記録し、ループ成果物との差分でベースラインを再構築する"
      - label: "保守的に全除外"
        description: "判定不能ファイルは全てベースライン扱いとし、コミット対象から除外する"
      - label: "ユーザーに手動分類を依頼"
        description: "ファイルリストを提示し、ユーザーにベースライン/成果物の分類を求める"
    multiSelect: false
```
