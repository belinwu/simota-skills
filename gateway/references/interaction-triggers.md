# Interaction Triggers

`AskUserQuestion` tool で確認する判断ポイントの YAML テンプレート集。
`_common/INTERACTION.md` の標準フォーマットに従う。

## ON_BREAKING_CHANGE

```yaml
questions:
  - question: "This change will affect existing clients. How would you like to proceed?"
    header: "Breaking Change"
    options:
      - label: "Create new version (v2) (Recommended)"
        description: "Introduce v2 design while maintaining existing v1"
      - label: "Maintain backward compatibility"
        description: "Consider alternative design avoiding breaking changes"
      - label: "Allow immediate change"
        description: "Proceed with changes accepting client impact"
    multiSelect: false
```

## ON_VERSION_STRATEGY

```yaml
questions:
  - question: "Please select an API versioning strategy."
    header: "Versioning"
    options:
      - label: "URL path (Recommended)"
        description: "/api/v1/... format. Clear and cacheable"
      - label: "Header"
        description: "Accept: application/vnd.api.v1+json format"
      - label: "Query parameter"
        description: "?version=1 format. No URL changes"
    multiSelect: false
```

## ON_AUTH_DESIGN

```yaml
questions:
  - question: "Please select an authentication method."
    header: "Auth Design"
    options:
      - label: "Bearer Token (JWT) (Recommended)"
        description: "Standard JWT authentication. Stateless"
      - label: "API Key"
        description: "For service-to-service communication. Simple"
      - label: "OAuth 2.0"
        description: "For third-party integration. Full-featured"
      - label: "Follow existing method"
        description: "Match the method currently used in project"
    multiSelect: false
```

## ON_NAMING_CONFLICT

```yaml
questions:
  - question: "Naming convention differs from existing pattern. Which should we follow?"
    header: "Naming Convention"
    options:
      - label: "Match existing pattern (Recommended)"
        description: "Maintain consistency within project"
      - label: "Adopt new convention"
        description: "Introduce better convention and migrate existing"
      - label: "Hybrid"
        description: "Apply new convention only to new endpoints"
    multiSelect: false
```

## ON_PAGINATION_CHOICE

```yaml
questions:
  - question: "Please select a pagination method."
    header: "Pagination"
    options:
      - label: "Cursor-based (Recommended)"
        description: "For large datasets. High consistency"
      - label: "Offset-based"
        description: "Simple. Allows random access"
      - label: "Follow existing method"
        description: "Match the method currently used in project"
    multiSelect: false
```

## ON_SPEC_FORMAT

```yaml
questions:
  - question: "Please select the API specification format."
    header: "Spec Format"
    options:
      - label: "OpenAPI 3.1 (YAML) (Recommended)"
        description: "Latest spec. Full JSON Schema compatibility"
      - label: "OpenAPI 3.0 (YAML)"
        description: "Widely supported stable version"
      - label: "OpenAPI (JSON)"
        description: "For programmatic processing"
    multiSelect: false
```
