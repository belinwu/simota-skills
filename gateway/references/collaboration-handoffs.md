# Collaboration & Handoff Templates

## Gateway → Builder Handoff

```markdown
## Gateway → Builder Handoff

### API Design Summary
**Endpoint:** [METHOD /path]
**Purpose:** [What this endpoint does]

### OpenAPI Specification
[Include complete OpenAPI spec or path to file]

### Implementation Requirements
- [ ] Request validation per schema
- [ ] Response format per schema
- [ ] Error handling per error catalog
- [ ] Authentication: [method]
- [ ] Authorization: [rules]
- [ ] Rate limiting: [limits]

### Key Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [Decision 1] | [Choice] | [Why] |

### Implementation Decision Criteria

以下の判断はBuilderに委ねる（Gatewayは決定しない）:
| 判断項目 | Gatewayの責任 | Builderの責任 |
|----------|---------------|-------------|
| バリデーション方式 | 何を検証するか定義 | Zod/Yup/class-validatorの選択 |
| エラーハンドリング | エラーコード・メッセージ定義 | try-catch/Result型の選択 |
| 認証チェック | 認証が必要かどうか | ミドルウェア実装方法 |
| DB操作 | 必要なデータ構造 | ORM/クエリ実装 |
| キャッシュ | キャッシュ可否の指定 | Redis/In-memory選択 |

### Edge Cases
1. [Edge case 1] → [Expected behavior]
2. [Edge case 2] → [Expected behavior]

### Test Scenarios for Radar
- [ ] Happy path: [scenario]
- [ ] Validation error: [scenario]
- [ ] Auth failure: [scenario]
- [ ] Not found: [scenario]
```

## Gateway → Quill Handoff

```markdown
## Gateway → Quill Handoff

### Documentation Request
**API Endpoint:** [METHOD /path]
**OpenAPI Spec:** [path to spec file]

### Documentation Needs
- [ ] README section for this endpoint
- [ ] Usage examples (curl, SDK)
- [ ] Error handling guide
- [ ] Migration guide (if versioning)

### Target Audience
- [ ] External developers
- [ ] Internal team
- [ ] Both

### Existing Documentation
[Links to current docs to update]
```

## Spark → Gateway Handoff

```markdown
## Spark → Gateway Handoff

### Feature Proposal
[Summary from Spark]

### API Design Request
- Resource identification
- Endpoint structure
- Request/response design
- Error handling
- Versioning consideration
```

## Canvas Integration

API flow diagram / resource relationship diagram requests:

```
/Canvas create API flow diagram showing:
- Client request
- Authentication/Authorization
- Business logic
- Database operations
- Response flow
- Error paths
```

```
/Canvas create ER-style diagram for API resources:
- User → Orders (1:N)
- Order → OrderItems (1:N)
- OrderItem → Product (N:1)
```

---

## GATEWAY_TO_BUILDER_HANDOFF (Compact)

```markdown
## BUILDER_HANDOFF (from Gateway)

### API Specification
- **Endpoint:** [METHOD /path]
- **Version:** [v1/v2]
- **OpenAPI spec:** [file path]

### Implementation Requirements
- [ ] Route handler with request validation
- [ ] Response serialization matching schema
- [ ] Error handling per error spec
- [ ] Rate limiting configuration
- [ ] Authentication middleware

Suggested command: `/Builder implement API endpoint [path]`
```

## GATEWAY_TO_QUILL_HANDOFF (Compact)

```markdown
## QUILL_HANDOFF (from Gateway)

### API Documentation
- **Endpoints designed:** [list]
- **OpenAPI spec:** [file path]
- **Documentation needed:**
  - [ ] API reference page
  - [ ] Usage examples
  - [ ] Authentication guide

Suggested command: `/Quill document API endpoints`
```
