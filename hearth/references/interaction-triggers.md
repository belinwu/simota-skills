# Hearth Interaction Trigger Templates

YAML question templates for `AskUserQuestion` tool.

---

## ON_TOOL_SELECTION

```yaml
questions:
  - question: "どのツールの設定を行いますか？"
    header: "Tool"
    options:
      - label: "zsh（推奨）"
        description: "シェル環境の設定（.zshrc、プラグイン、エイリアス、completion）"
      - label: "neovim"
        description: "エディタ設定（init.lua、LSP、プラグイン管理）"
      - label: "ghostty"
        description: "ターミナルエミュレータの設定（テーマ、フォント、キーバインド）"
      - label: "tmux"
        description: "ターミナルマルチプレクサの設定（キーバインド、ステータスバー）"
    multiSelect: true
```

## ON_PROFILE_CHOICE

```yaml
questions:
  - question: "どのプロファイルレベルで設定しますか？"
    header: "Profile"
    options:
      - label: "Minimal"
        description: "必要最低限の設定のみ。起動速度重視。プラグインなし"
      - label: "Standard（推奨）"
        description: "バランスの取れた設定。厳選されたプラグインと便利なエイリアス"
      - label: "Power"
        description: "フル機能。豊富なプラグイン、カスタムウィジェット、高度な設定"
    multiSelect: false
```

## ON_EXISTING_CONFIG

```yaml
questions:
  - question: "既存の設定ファイルが検出されました。どう処理しますか？"
    header: "Config"
    options:
      - label: "マージ（推奨）"
        description: "既存設定を保持しつつ、新しい設定を追加。バックアップも作成"
      - label: "上書き"
        description: "バックアップ作成後、新しい設定で完全に置き換え"
      - label: "スキップ"
        description: "このファイルは変更せず、次のツールへ進む"
    multiSelect: false
```

## ON_PLUGIN_MANAGER

```yaml
questions:
  - question: "どのプラグインマネージャーを使用しますか？"
    header: "Plugins"
    options:
      - label: "sheldon（推奨）"
        description: "Rust製。高速、TOML設定、遅延読み込み対応"
      - label: "zinit"
        description: "高機能。Turbo mode、豊富なice修飾子"
      - label: "なし"
        description: "プラグインマネージャーを使わず、手動管理または直接source"
    multiSelect: false
```

## ON_OS_SPECIFIC

```yaml
questions:
  - question: "OS固有の設定変更を適用しますか？"
    header: "OS Config"
    options:
      - label: "適用（推奨）"
        description: "検出されたOSに最適な設定を自動適用"
      - label: "スキップ"
        description: "OS固有の設定は行わず、クロスプラットフォーム設定のみ"
      - label: "確認しながら"
        description: "各OS固有設定について個別に確認しながら適用"
    multiSelect: false
```
