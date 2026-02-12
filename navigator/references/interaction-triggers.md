# Interaction Trigger Templates

YAML question templates for `AskUserQuestion` tool. See `_common/INTERACTION.md` for standard formats.

---

## ON_TARGET_URL

```yaml
questions:
  - question: "対象URLとタスクの範囲を確認します。このURLで進めてよいですか？"
    header: "Target URL"
    options:
      - label: "このURLで進める (Recommended)"
        description: "指定されたURLでタスクを開始します"
      - label: "URLを変更"
        description: "別のURLを指定します"
      - label: "認証が必要"
        description: "ログイン後のURLを使用します"
    multiSelect: false
```

## ON_AUTH_REQUIRED

```yaml
questions:
  - question: "認証が必要です。どの方法で認証しますか？"
    header: "Auth Method"
    options:
      - label: "環境変数から認証情報を取得 (Recommended)"
        description: "安全に環境変数から認証情報を読み込みます"
      - label: "既存のセッションを使用"
        description: "保存されたセッション/Cookieを使用します"
      - label: "手動でログイン"
        description: "ブラウザを一時停止し、手動でログインします"
      - label: "認証なしで続行"
        description: "認証なしでアクセス可能な部分のみ操作します"
    multiSelect: false
```

## ON_DESTRUCTIVE_ACTION

```yaml
questions:
  - question: "データを変更する操作が含まれています。実行してよいですか？"
    header: "Destructive"
    options:
      - label: "実行する (Recommended)"
        description: "操作を実行し、変更を適用します"
      - label: "ドライランで確認"
        description: "実際には送信せず、内容を確認します"
      - label: "スキップ"
        description: "この操作をスキップして次に進みます"
    multiSelect: false
```

## ON_FORM_SUBMISSION

```yaml
questions:
  - question: "フォームを送信します。入力内容を確認してください。"
    header: "Form Submit"
    options:
      - label: "送信する (Recommended)"
        description: "入力内容でフォームを送信します"
      - label: "内容を修正"
        description: "送信前に入力内容を修正します"
      - label: "キャンセル"
        description: "フォーム送信をキャンセルします"
    multiSelect: false
```

## ON_CAPTCHA_DETECTED

```yaml
questions:
  - question: "CAPTCHAが検出されました。どのように対応しますか？"
    header: "CAPTCHA"
    options:
      - label: "手動で解決 (Recommended)"
        description: "ブラウザを一時停止し、手動でCAPTCHAを解決します"
      - label: "スキップして続行"
        description: "このページをスキップし、次のタスクに進みます"
      - label: "タスクを中止"
        description: "CAPTCHAを回避できないため、タスクを中止します"
    multiSelect: false
```

## ON_RATE_LIMIT

```yaml
questions:
  - question: "レート制限が検出されました。どのように対応しますか？"
    header: "Rate Limit"
    options:
      - label: "待機して再試行 (Recommended)"
        description: "一定時間待機後、再試行します"
      - label: "速度を落として続行"
        description: "リクエスト間隔を広げて続行します"
      - label: "タスクを中止"
        description: "レート制限を回避するため、タスクを中止します"
    multiSelect: false
```

## ON_DATA_VALIDATION

```yaml
questions:
  - question: "収集したデータに問題が検出されました。どのように対応しますか？"
    header: "Data Issue"
    options:
      - label: "そのまま続行 (Recommended)"
        description: "問題を記録し、タスクを続行します"
      - label: "データを再取得"
        description: "問題のあるデータを再度取得します"
      - label: "タスクを中止"
        description: "データ品質の問題により、タスクを中止します"
    multiSelect: false
```

## ON_NAVIGATION_BLOCKED

```yaml
questions:
  - question: "ナビゲーションがブロックされました。どのように対応しますか？"
    header: "Blocked"
    options:
      - label: "別のルートを試す (Recommended)"
        description: "代替のナビゲーションパスを試みます"
      - label: "手動で介入"
        description: "ブラウザを一時停止し、手動で操作します"
      - label: "タスクを中止"
        description: "ブロックを回避できないため、タスクを中止します"
    multiSelect: false
```
