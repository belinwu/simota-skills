# Agent Teams API Quick Reference

Claude Code Agent Teams API のクイックリファレンス。
Rally が使用するツールとデータ構造の一覧。

---

## ツール一覧

### TeamCreate

チームを作成する。チーム名でタスクリストも自動作成される。

```yaml
TeamCreate:
  team_name: string      # チーム名（必須）
  description: string    # チームの説明（任意）
  agent_type: string     # チームリードのタイプ（任意）
```

**生成されるファイル:**
- `~/.claude/teams/{team-name}/config.json` - チーム設定
- `~/.claude/tasks/{team-name}/` - タスクリストディレクトリ

---

### Task（チームメイトスポーン）

チームメイトをスポーンする。`team_name` と `name` を指定。

```yaml
Task:
  subagent_type: string  # エージェントタイプ（必須）
  team_name: string      # 所属チーム名（チームメイトとして参加）
  name: string           # チームメイト名（チーム内で一意）
  description: string    # 3-5語の説明（必須）
  prompt: string         # タスク説明とコンテキスト（必須）
  mode: string           # 権限モード（任意）
  model: string          # モデル指定（任意）
  run_in_background: boolean  # バックグラウンド実行（任意）
  max_turns: integer     # 最大ターン数（任意）
```

**subagent_type 選択肢:**
| タイプ | ツール |
|--------|--------|
| `general-purpose` | 全ツール |
| `Explore` | 読み取り系のみ |
| `Plan` | 読み取り系のみ |
| `Bash` | Bash のみ |

**mode 選択肢:**
| モード | 説明 |
|--------|------|
| `bypassPermissions` | 全ツール自動許可（低リスクタスク向け） |
| `plan` | plan_mode_required（高リスクタスク向け、Rally が承認） |
| `default` | ユーザーに許可を求める |
| `acceptEdits` | ファイル編集を自動許可 |
| `dontAsk` | 確認なしで実行 |
| `delegate` | 委任モード |

**model 選択肢:**
| モデル | ID |
|--------|-----|
| `sonnet` | デフォルト |
| `opus` | 高性能 |
| `haiku` | 軽量 |

---

### TaskCreate

タスクを作成する。

```yaml
TaskCreate:
  subject: string        # タスクタイトル（必須、命令形）
  description: string    # タスク詳細（必須）
  activeForm: string     # 実行中の表示テキスト（推奨、進行形）
```

---

### TaskUpdate

タスクを更新する。

```yaml
TaskUpdate:
  taskId: string         # タスクID（必須）
  status: string         # pending | in_progress | completed | deleted
  subject: string        # タイトル変更（任意）
  description: string    # 説明変更（任意）
  activeForm: string     # 表示テキスト変更（任意）
  owner: string          # 所有者変更（チームメイト名）
  addBlockedBy: [string] # ブロッカーに追加するタスクID
  addBlocks: [string]    # このタスクがブロックするタスクID
  metadata: object       # メタデータ（任意）
```

---

### TaskList

全タスクの一覧を取得する。

```yaml
TaskList: {}  # パラメータなし
```

**戻り値:**
- `id`: タスクID
- `subject`: タイトル
- `status`: pending | in_progress | completed
- `owner`: 所有者（チームメイト名）
- `blockedBy`: ブロッカーのタスクIDリスト

---

### TaskGet

特定タスクの詳細を取得する。

```yaml
TaskGet:
  taskId: string  # タスクID（必須）
```

---

### SendMessage

チームメイトにメッセージを送信する。

**ダイレクトメッセージ:**
```yaml
SendMessage:
  type: "message"
  recipient: string      # チームメイト名（必須）
  content: string        # メッセージ本文（必須）
  summary: string        # 5-10語の要約（必須）
```

**ブロードキャスト:**
```yaml
SendMessage:
  type: "broadcast"
  content: string        # メッセージ本文（必須）
  summary: string        # 5-10語の要約（必須）
```

**シャットダウン要求:**
```yaml
SendMessage:
  type: "shutdown_request"
  recipient: string      # チームメイト名（必須）
  content: string        # シャットダウン理由（任意）
```

**シャットダウン応答:**
```yaml
SendMessage:
  type: "shutdown_response"
  request_id: string     # リクエストID（必須）
  approve: boolean       # 承認/拒否（必須）
  content: string        # 拒否理由（拒否時）
```

**プラン承認応答:**
```yaml
SendMessage:
  type: "plan_approval_response"
  request_id: string     # リクエストID（必須）
  recipient: string      # チームメイト名（必須）
  approve: boolean       # 承認/拒否（必須）
  content: string        # フィードバック（拒否時）
```

---

### TeamDelete

チームとタスクリストを削除する。

```yaml
TeamDelete: {}  # パラメータなし（現在のチームコンテキストを使用）
```

**注意:** アクティブなメンバーがいる場合は失敗する。事前に全員を shutdown すること。

---

## データ構造

### config.json

`~/.claude/teams/{team-name}/config.json` の構造:

```json
{
  "team_name": "feature-auth",
  "description": "認証機能の並列実装チーム",
  "members": [
    {
      "name": "backend-impl",
      "agentId": "abc-123",
      "agentType": "general-purpose"
    },
    {
      "name": "frontend-impl",
      "agentId": "def-456",
      "agentType": "general-purpose"
    }
  ]
}
```

**注意:** メンバーの参照には常に `name` を使用する。`agentId` は内部用。

### タスクリスト

`~/.claude/tasks/{team-name}/` ディレクトリにタスクファイルが格納される。
TaskList/TaskGet/TaskCreate/TaskUpdate ツールで操作する。

---

## 制約事項・注意点

### チームサイズ

- **推奨:** 2-4人
- **上限:** 10人（Never do に記載）
- **5人以上:** ユーザー確認が必要（Ask first）

### コスト

- 各チームメイトは独立した Claude インスタンス → トークンコスト発生
- `broadcast` は全メンバーに個別送信 → N倍のコスト
- `haiku` モデルで軽量タスクのコスト削減を推奨

### メッセージ配信

- チームメイトからのメッセージは**自動配信**される（手動チェック不要）
- チームメイトは各ターン終了時に idle になる（正常動作）
- idle 状態のチームメイトにメッセージ送信可能（自動復帰）

### hub-spoke パターン

- Rally がハブ、チームメイトがスポーク
- チームメイト同士の直接通信は許可しない
- 全コミュニケーションは Rally を経由する

### ファイル操作

- `Explore` / `Plan` タイプのチームメイトはファイル編集不可
- 実装タスクには必ず `general-purpose` を使用する
- ファイル所有権はチームメイトの prompt で明示的に伝える（API レベルの制約はない）

### TeamDelete の前提条件

- 全メンバーがシャットダウン済みであること
- アクティブなメンバーがいると TeamDelete は失敗する

### Display Modes

チームメイトの表示モードは環境に依存:
- **in-process**: メインプロセス内で表示
- **split-pane**: IDE 統合時に分割表示

現時点では明示的な設定は不要（システムが自動決定）。
