# Cast Interaction Triggers

YAML question templates for all Cast decision points. Uses `AskUserQuestion` tool format per `_common/INTERACTION.md`.

---

## BEFORE_START Triggers

### ON_SOURCE_SELECTION

When multiple input sources are available for persona generation.

```yaml
questions:
  - question: "ペルソナ生成にどのソースを使用しますか？"
    header: "Source"
    options:
      - label: "自動検出（推奨）"
        description: "README、docs、srcを自動分析"
      - label: "ドキュメントのみ"
        description: "ドキュメントファイルのみを分析"
      - label: "コードのみ"
        description: "ソースコードのみを分析"
      - label: "ファイルを指定"
        description: "分析対象ファイルを手動指定"
    multiSelect: false
```

### ON_PERSONA_COUNT

When unclear how many personas to generate.

```yaml
questions:
  - question: "何人のペルソナを生成しますか？"
    header: "Count"
    options:
      - label: "3人（推奨）"
        description: "Primary、Secondary、Edge Caseの3人"
      - label: "5人"
        description: "より詳細なセグメント分割"
      - label: "自動判定"
        description: "検出されたユーザータイプ数に基づいて決定"
    multiSelect: false
```

### ON_DETAIL_LEVEL

When persona detail level is not specified.

```yaml
questions:
  - question: "ペルソナの詳細レベルを選択してください"
    header: "Detail"
    options:
      - label: "自動（推奨）"
        description: "抽出データ量に基づいて自動選択"
      - label: "Minimal"
        description: "必須属性のみ。高速生成"
      - label: "Standard"
        description: "主要な拡張属性を含む"
      - label: "Full"
        description: "全拡張属性を含む（B2B向け）"
    multiSelect: false
```

### ON_PERSONA_TYPE

When both user and internal personas are possible.

```yaml
questions:
  - question: "どのタイプのペルソナを生成しますか？"
    header: "Type"
    options:
      - label: "ユーザーペルソナ（推奨）"
        description: "サービス利用者向けペルソナ"
      - label: "Internalペルソナ"
        description: "開発組織向けペルソナ"
      - label: "両方"
        description: "両タイプを生成"
    multiSelect: false
```

### ON_NO_VOICE_PROFILE

When SPEAK mode is invoked but the target persona has no `voice_profile` defined.

```yaml
questions:
  - question: "ペルソナ「{persona_name}」にvoice_profileが未定義です。どうしますか？"
    header: "Voice"
    options:
      - label: "自動推定で続行（推奨）"
        description: "既存属性からvoice_profileをAuto-Deriveして音声生成"
      - label: "voice_profileを設定してからSPEAK"
        description: "EVOLVEモードでvoice_profileを設定後に再実行"
      - label: "デフォルト設定で続行"
        description: "言語デフォルトのボイス・スタイルで音声生成"
    multiSelect: false
```

### ON_ENGINE_UNAVAILABLE

When the specified or preferred TTS engine is not available.

```yaml
questions:
  - question: "TTSエンジン「{engine_name}」が利用できません。どうしますか？"
    header: "Engine"
    options:
      - label: "代替エンジンを使用（推奨）"
        description: "{fallback_engine}にフォールバック"
      - label: "テキストのみ出力"
        description: "音声なしでセリフテキストのみ表示"
      - label: "キャンセル"
        description: "SPEAKモードを中止"
    multiSelect: false
```

### ON_DIALOGUE_COMPLEXITY

When a dialogue involves 3 or more personas.

```yaml
questions:
  - question: "{count}人のペルソナによる対話です。ターン数を選択してください"
    header: "Turns"
    options:
      - label: "4ターン（推奨）"
        description: "コンパクトで要点がわかる対話"
      - label: "6ターン"
        description: "より深い議論を展開"
      - label: "8ターン"
        description: "各ペルソナの立場を十分に表現"
    multiSelect: false
```

### ON_SERVICE_IDENTIFICATION

When service name cannot be auto-detected.

```yaml
questions:
  - question: "対象サービスの名前を選択してください"
    header: "Service"
    options:
      - label: "リポジトリ名を使用（推奨）"
        description: "現在のリポジトリ名をサービス名として使用"
      - label: "package.jsonから取得"
        description: "package.jsonのname fieldを使用"
      - label: "手動指定"
        description: "サービス名を直接入力"
    multiSelect: false
```

---

## ON_DECISION Triggers

### ON_MERGE_CONFLICT

When fusing data from multiple sources with conflicting information.

```yaml
questions:
  - question: "データソース間で矛盾が検出されました。どのように解決しますか？"
    header: "Conflict"
    options:
      - label: "新しいデータを優先（推奨）"
        description: "より最近のデータソースの値を採用"
      - label: "信頼度が高い方を優先"
        description: "Confidence scoreが高いソースの値を採用"
      - label: "両方を保持"
        description: "矛盾を記録し、両方の値を注釈付きで保持"
      - label: "手動で選択"
        description: "各矛盾について個別に判断"
    multiSelect: false
```

### ON_LOW_CONFIDENCE

When a persona's confidence drops below 0.4.

```yaml
questions:
  - question: "ペルソナ「{persona_name}」のConfidenceが{confidence}に低下しました。どうしますか？"
    header: "Confidence"
    options:
      - label: "データ補強を推奨（推奨）"
        description: "Trace/Voice/Researcherからの追加データを提案"
      - label: "そのまま維持"
        description: "低Confidenceとして使用を継続"
      - label: "アーカイブ"
        description: "ペルソナをアーカイブに移動"
    multiSelect: false
```

### ON_DISTRIBUTION_TARGET

When multiple agents could receive persona distribution.

```yaml
questions:
  - question: "ペルソナをどのエージェントに配信しますか？"
    header: "Distribute"
    options:
      - label: "Echo（UI検証）"
        description: "ペルソナベースのUI検証に使用"
      - label: "Spark（機能提案）"
        description: "ペルソナのニーズから新機能を提案"
      - label: "Retain（リテンション）"
        description: "ペルソナ別のリテンション戦略設計"
      - label: "全エージェントに配信"
        description: "登録済み全消費エージェントに配信"
    multiSelect: true
```

### ON_EXISTING_PERSONAS

When existing Echo personas are found that Cast could adopt.

```yaml
questions:
  - question: "既存のEchoペルソナが見つかりました。Cast管理下に入れますか？"
    header: "Adopt"
    options:
      - label: "既存を採用し拡張（推奨）"
        description: "Castメタデータを追加し、レジストリに登録"
      - label: "新規生成のみ"
        description: "既存を無視し、新しいペルソナを生成"
      - label: "既存を参照して補完"
        description: "既存をベースに不足情報を補完"
    multiSelect: false
```

---

## ON_RISK Triggers

### ON_IDENTITY_CHANGE

When evolution data suggests a persona's Core Identity (Role) should change.

```yaml
questions:
  - question: "ペルソナ「{persona_name}」の行動パターンがRoleの変更を示唆しています。どうしますか？"
    header: "Identity"
    options:
      - label: "新規ペルソナを作成（推奨）"
        description: "現在のペルソナをアーカイブし、新しいペルソナを作成"
      - label: "進化として適用"
        description: "Role変更をminor evolutionとして適用（非推奨）"
      - label: "変更を無視"
        description: "既存のRoleを維持し、行動データのみ更新"
    multiSelect: false
```

### ON_ARCHIVAL

When a persona is flagged for archival (e.g., confidence too low, replaced).

```yaml
questions:
  - question: "ペルソナ「{persona_name}」のアーカイブが推奨されています（理由: {reason}）。進めますか？"
    header: "Archive"
    options:
      - label: "アーカイブする（推奨）"
        description: "_archive/に移動し、レジストリを更新"
      - label: "データ補強を試みる"
        description: "追加データでConfidence回復を試行"
      - label: "そのまま維持"
        description: "警告付きで現状維持"
    multiSelect: false
```

### ON_BULK_EVOLUTION

When evolving all personas at once could cause many changes.

```yaml
questions:
  - question: "{count}件のペルソナに進化が検出されました。一括適用しますか？"
    header: "Bulk"
    options:
      - label: "全件適用（推奨）"
        description: "全ペルソナに進化を適用"
      - label: "1件ずつ確認"
        description: "各ペルソナの進化内容を確認しながら適用"
      - label: "高Confidence変更のみ"
        description: "Confidenceが向上する変更のみ適用"
    multiSelect: false
```

---

## ON_COMPLETION Triggers

### ON_GENERATION_COMPLETE

After persona generation is complete.

```yaml
questions:
  - question: "生成されたペルソナを保存しますか？"
    header: "Save"
    options:
      - label: "全件保存（推奨）"
        description: ".agents/personas/{service}/に保存"
      - label: "確認してから保存"
        description: "内容を確認後に保存"
      - label: "選択して保存"
        description: "保存するペルソナを選択"
    multiSelect: false
```

### ON_ECHO_HANDOFF

After personas are ready for Echo validation.

```yaml
questions:
  - question: "ペルソナをEchoに渡してUI検証を開始しますか？"
    header: "Handoff"
    options:
      - label: "Echoに渡す（推奨）"
        description: "生成ペルソナでEcho UI検証を開始"
      - label: "後で手動で実行"
        description: "保存のみ。Echoは後で手動起動"
      - label: "まずデータを補強"
        description: "Trace/Voiceからデータを収集してから検証"
    multiSelect: false
```

---

## AUTORUN Mode Behavior

In AUTORUN mode (via `## NEXUS_AUTORUN`), Cast uses these defaults without asking:

| Trigger | Default Action |
|---------|---------------|
| ON_SOURCE_SELECTION | Auto-detect |
| ON_PERSONA_COUNT | 3 (Primary/Secondary/Edge) |
| ON_DETAIL_LEVEL | Auto (based on extracted data) |
| ON_PERSONA_TYPE | User Persona |
| ON_MERGE_CONFLICT | Newer data wins |
| ON_LOW_CONFIDENCE | Recommend enrichment (non-blocking) |
| ON_IDENTITY_CHANGE | Create new persona |
| ON_ARCHIVAL | Archive with notification |
| ON_GENERATION_COMPLETE | Save all |
| ON_NO_VOICE_PROFILE | Auto-derive from existing attributes |
| ON_ENGINE_UNAVAILABLE | Use fallback engine |
| ON_DIALOGUE_COMPLEXITY | 4 turns |
| ON_ECHO_HANDOFF | Include in NEXUS_HANDOFF |
