# Handoff Format Templates

## Input Patterns

### From Builder
```
/Schema design tables for [feature]
Context: Need data model for [domain].
Entities: [entity list]
Requirements: [access patterns, constraints]
```

### From Fixture
```
/Schema verify test data compatibility
Context: Fixture needs schema details for [tables].
Requirements: Relationships, constraints, seed data rules.
```

---

## SCHEMA_TO_BUILDER_HANDOFF

```markdown
## BUILDER_HANDOFF (from Schema)

### Schema Designed
- **Tables:** [List of tables created/modified]
- **Framework:** [Prisma/TypeORM/Drizzle]
- **Migration:** [Migration file path]

### Implementation Needed
- [ ] Repository/DAO layer for [table]
- [ ] CRUD operations with proper typing
- [ ] Relationship eager/lazy loading configuration

### Schema Details
[Prisma/TypeORM/Drizzle schema snippet]

Suggested command: `/Builder implement repository for [table]`
```

## SCHEMA_TO_TUNER_HANDOFF

```markdown
## TUNER_HANDOFF (from Schema)

### Initial Index Design
- **Table:** [Table name]
- **Indexes Created:** [List of indexes]
- **Expected Query Patterns:** [List of common queries]

### Optimization Needed
- [ ] Validate index effectiveness with EXPLAIN ANALYZE
- [ ] Check for missing indexes on frequent queries
- [ ] Evaluate partial index opportunities

Suggested command: `/Tuner optimize queries for [table]`
```

## SCHEMA_TO_CANVAS_HANDOFF

```markdown
## CANVAS_HANDOFF (from Schema)

### Visualization Request
- **Type:** ER Diagram
- **Tables:** [List of tables]
- **Relationships:** [List of relationships]
- **Format:** Mermaid erDiagram

Suggested command: `/Canvas create ER diagram`
```
