# Interaction Trigger Templates

Use `AskUserQuestion` tool to confirm with user at these decision points.
See `_common/INTERACTION.md` for standard formats.

## ON_SCENARIO_DESIGN

```yaml
questions:
  - question: "デモのシナリオを確認します。このストーリーフローで進めてよいですか？"
    header: "Scenario"
    options:
      - label: "このシナリオで進める (Recommended)"
        description: "提案されたストーリーフローで撮影を開始します"
      - label: "シナリオを調整"
        description: "操作手順や待機タイミングを変更します"
      - label: "別の機能を先にデモ"
        description: "デモ対象の機能を変更します"
    multiSelect: false
```

## ON_RECORDING_CONFIG

```yaml
questions:
  - question: "Select recording resolution."
    header: "Resolution"
    options:
      - label: "Desktop 1280x720 (Recommended)"
        description: "Standard desktop, web embedding (~5MB/30s)"
      - label: "Desktop 1920x1080 (Full HD)"
        description: "Full HD, presentations & detailed views (~10MB/30s)"
      - label: "Desktop 2560x1440 (2K/QHD)"
        description: "High resolution, large screens & Retina (~18MB/30s)"
      - label: "Desktop 3840x2160 (4K)"
        description: "Maximum quality, production use (~35MB/30s)"
    multiSelect: false
  - question: "Select device type."
    header: "Device"
    options:
      - label: "Desktop Chrome (Recommended)"
        description: "Standard desktop browser"
      - label: "Mobile iPhone 14 Pro"
        description: "390x844, mobile app demos"
      - label: "Mobile iPhone SE"
        description: "375x667, compact mobile demos"
      - label: "Tablet iPad"
        description: "768x1024, tablet app demos"
    multiSelect: false
```

## ON_SENSITIVE_CONTENT

```yaml
questions:
  - question: "デモに含まれるデータに機密情報が含まれる可能性があります。どう対応しますか？"
    header: "Sensitive"
    options:
      - label: "ダミーデータに置換 (Recommended)"
        description: "すべてのデータをリアルだが架空のものに置換"
      - label: "マスキングを追加"
        description: "特定フィールドにぼかしやマスクを適用"
      - label: "そのまま続行"
        description: "データは問題ないことを確認済み"
    multiSelect: false
```
