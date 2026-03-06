# Diagram Templates Reference

Purpose: Read this when you need a fast, syntax-safe starter for a common diagram family.

## Contents

- Selection matrix
- Mermaid starters
- draw.io note

## Selection Matrix

| Diagram | Use For |
|---------|---------|
| Flowchart | Control flow, business process, API routes |
| Sequence | Interactions over time |
| State | Lifecycle or state transitions |
| Class | Types and dependencies |
| ER | Database structure |
| Journey | User or DX experience |
| Mind Map | Concepts or hierarchy |
| Gantt | Schedule and dependencies |
| Git Graph | Branch or merge history |
| Pie Chart | Ratios or composition |

## Flowchart

```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[Alternative]
```

## Sequence

```mermaid
sequenceDiagram
    actor User
    participant API
    participant DB
    User->>API: Request
    API->>DB: Query
    DB-->>API: Result
    API-->>User: Response
```

## State

```mermaid
stateDiagram-v2
    [*] --> idle
    idle --> loading
    loading --> success
    loading --> error
```

## Class

```mermaid
classDiagram
    class User
    class Session
    User "1" --> "*" Session
```

## ER

```mermaid
erDiagram
    USER ||--o{ POST : writes
    USER {
      string id
      string email
    }
    POST {
      string id
      string title
    }
```

## Journey

```mermaid
journey
    title Checkout Flow
    section Cart
      View cart: 4: User
    section Payment
      Submit payment: 2: User
```

## Mind Map

```mermaid
mindmap
  root((System))
    Frontend
    Backend
    Database
```

## Gantt

```mermaid
gantt
    title Release Plan
    dateFormat  YYYY-MM-DD
    section Build
    Implement :a1, 2026-03-01, 5d
    Test      :a2, after a1, 3d
```

## Git Graph

```mermaid
gitGraph
    commit
    branch feature
    checkout feature
    commit
    checkout main
    merge feature
```

## Pie Chart

```mermaid
pie title Test Composition
    "Unit" : 70
    "Integration" : 20
    "E2E" : 10
```

## draw.io Note

Use `references/drawio-specs.md` when XML structure, IDs, edge routing, or layout control matters.
