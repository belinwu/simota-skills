# Interaction Trigger Templates

## ON_DOC_SCOPE

```yaml
questions:
  - question: "Please select documentation scope. How much should be covered?"
    header: "Scope"
    options:
      - label: "Target files only (Recommended)"
        description: "Document only specified files/functions"
      - label: "Entire related module"
        description: "Include related files with dependencies"
      - label: "Entire package"
        description: "Document all public APIs in the package"
    multiSelect: false
```

## ON_TYPE_STRICTNESS

```yaml
questions:
  - question: "How strict should `any` type replacements be?"
    header: "Type Strictness"
    options:
      - label: "Strict type definitions (Recommended)"
        description: "Define explicit types for all properties"
      - label: "Flexible type definitions"
        description: "Type only required properties, use Partial for optionals"
      - label: "Gradual typing"
        description: "Replace with unknown first, add detailed types later"
    multiSelect: false
```

## ON_README_UPDATE

```yaml
questions:
  - question: "Confirming README update scope. How much should be updated?"
    header: "README Update"
    options:
      - label: "Relevant section only (Recommended)"
        description: "Update only sections directly related to changes"
      - label: "Update related sections"
        description: "Review install instructions, env vars, etc."
      - label: "Full review"
        description: "Verify consistency of entire README and update"
    multiSelect: false
```

## ON_TYPE_PATTERN_CHOICE

```yaml
questions:
  - question: "複数の型定義パターンが適用可能です。どのアプローチを使用しますか？"
    header: "型パターン"
    options:
      - label: "Genericsを使用（推奨）"
        description: "再利用性の高いジェネリック型で定義"
      - label: "具体的な型を定義"
        description: "この用途専用の具体的なインターフェースを作成"
      - label: "Utility Typesを活用"
        description: "既存型からPick/Omit等で派生"
    multiSelect: false
```

## ON_ATLAS_ADR_REQUEST

```yaml
questions:
  - question: "アーキテクチャ決定のドキュメント化が必要です。Atlasに依頼しますか？"
    header: "ADR作成"
    options:
      - label: "Atlasに依頼（推奨）"
        description: "AtlasエージェントにADR作成を依頼"
      - label: "簡易コメントで対応"
        description: "コード内コメントで決定理由を説明"
      - label: "READMEに追記"
        description: "READMEのアーキテクチャセクションに追記"
    multiSelect: false
```
