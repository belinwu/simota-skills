# C4 Modeling Patterns

Purpose: Collection of C4 modeling patterns for common system architectures.
Read when: You need to confirm how to structure a C4 model for a specific architecture style.

## Contents

- Web Application (Monolith)
- Microservices
- Serverless
- Event-Driven
- Mobile + Backend
- AI/LLM-Backed Application (2026-era pattern)
- Edge + Origin Split (CDN-resident compute)
- Modeling with Archetypes (DSL v4.0+)
- Discovery Heuristics

---

## Pattern 1: Web Application (Monolith)

### L1 Context

```
[User] --> [Web Application System]
[Web Application System] --> [Email Service] (external)
[Web Application System] --> [Payment Gateway] (external)
```

### L2 Container

```dsl
system = softwareSystem "Web Application" {
    spa = container "SPA" "User interface" "React" "WebBrowser"
    server = container "Application Server" "Business logic + API" "Node.js Express"
    db = container "Database" "Persistent storage" "PostgreSQL" "Database"
    cache = container "Session Store" "Session and cache" "Redis" "Database"
}
```

### Characteristics
- The monolith server is represented as a single Container
- SPA and Server are separate Containers (different runtime boundaries)
- DB and Cache are independent Containers

---

## Pattern 2: Microservices

### L1 Context

```
[User] --> [E-Commerce Platform]
[E-Commerce Platform] --> [Payment Provider] (external)
[E-Commerce Platform] --> [Shipping API] (external)
```

### L2 Container

```dsl
platform = softwareSystem "E-Commerce Platform" {
    gateway = container "API Gateway" "Routing and auth" "Kong/Nginx"
    userSvc = container "User Service" "User management" "Go"
    orderSvc = container "Order Service" "Order processing" "Java Spring Boot"
    productSvc = container "Product Service" "Product catalog" "Node.js"
    userDb = container "User DB" "User data" "PostgreSQL" "Database"
    orderDb = container "Order DB" "Order data" "PostgreSQL" "Database"
    productDb = container "Product DB" "Product data" "MongoDB" "Database"
    queue = container "Event Bus" "Async communication" "Kafka"
}
```

### Characteristics
- Each microservice is an individual Container
- Each service has its own DB (Database per Service)
- Event Bus mediates async communication between Containers
- API Gateway serves as the entry point

### Common mistakes
- Making shared libraries into Containers → Include in the Container's technology description
- Vague relationship labels when mixing direct calls and event-driven patterns

---

## Pattern 3: Serverless

### L2 Container

```dsl
system = softwareSystem "Serverless App" {
    spa = container "Web App" "UI" "Next.js" "WebBrowser"
    authFn = container "Auth Function" "Authentication" "AWS Lambda + Node.js"
    apiFn = container "API Function" "Business logic" "AWS Lambda + Python"
    processFn = container "Processing Function" "Async processing" "AWS Lambda + Python"
    db = container "DynamoDB" "Data storage" "AWS DynamoDB" "Database"
    storage = container "S3 Bucket" "File storage" "AWS S3" "Database"
    queue = container "SQS Queue" "Task queue" "AWS SQS"
}
```

### Characteristics
- Each Lambda function is an independent Container (independent runtime boundary)
- However, function groups serving the same purpose can be consolidated into one Container
- Managed services (DynamoDB, S3, SQS) are individual Containers

---

## Pattern 4: Event-Driven

### L2 Container

```dsl
system = softwareSystem "Event-Driven System" {
    producer = container "Event Producer" "Generates events" "Node.js"
    broker = container "Message Broker" "Event routing" "Apache Kafka"
    consumer1 = container "Analytics Consumer" "Processes analytics" "Python"
    consumer2 = container "Notification Consumer" "Sends notifications" "Go"
    consumer3 = container "Audit Consumer" "Records audit trail" "Java"
    analyticsDb = container "Analytics Store" "Analytics data" "ClickHouse" "Database"
    auditDb = container "Audit Log" "Audit records" "PostgreSQL" "Database"
}
```

### Relationship notation notes
```dsl
// Make async relationships explicit
producer -> broker "Publishes OrderCreated events to" "Kafka Protocol"
broker -> consumer1 "Delivers events to" "Kafka Consumer Group"
```

---

## Pattern 5: Mobile + Backend

### L2 Container

```dsl
system = softwareSystem "Mobile Platform" {
    iosApp = container "iOS App" "Native mobile app" "Swift/SwiftUI" "MobileDevicePortrait"
    androidApp = container "Android App" "Native mobile app" "Kotlin/Jetpack Compose" "MobileDevicePortrait"
    bff = container "Mobile BFF" "Backend for frontend" "Node.js Express"
    api = container "Core API" "Business logic" "Go"
    db = container "Database" "Data storage" "PostgreSQL" "Database"
    push = container "Push Service" "Push notifications" "Firebase Cloud Messaging"
}
```

### Characteristics
- iOS/Android are separate Containers (different runtimes)
- With BFF (Backend for Frontend) pattern, the BFF is an independent Container
- Push notification service is either an External System or internal Container (depends on ownership)

---

## Pattern 6: AI/LLM-Backed Application (2026-era pattern)

### L2 Container

```dsl
system = softwareSystem "AI Assistant Platform" {
    spa       = container "Web App" "Chat UI" "Next.js" "WebBrowser"
    bff       = container "BFF" "Stream orchestration, auth, rate limiting" "Node.js"
    agentSvc  = container "Agent Orchestrator" "Tool calls, planning, retries" "Python / FastAPI"
    ragSvc    = container "Retrieval Service" "Hybrid (vector + keyword) retrieval" "Python"
    vectorDb  = container "Vector Index" "Embedding index" "pgvector / Pinecone" "Database"
    docDb     = container "Document Store" "Source corpus + chunk metadata" "PostgreSQL" "Database"
    evalSvc   = container "Eval Harness" "Offline & online eval, rubrics" "Python"
    obs       = container "Trace Store" "LLM traces, spans, metrics" "OTel + Tempo + Grafana"
    llm       = softwareSystem "LLM Provider" "Hosted foundation model API" "Existing System"
    sandbox   = softwareSystem "Code Sandbox" "Isolated code execution for tools" "Existing System"
}
```

### Characteristics

- The hosted LLM is an **External Software System**, not an internal Container — it has its own deployment lifecycle and is independently owned.
- Retrieval (RAG), agent orchestration, and evaluation each get their own Container because their runtimes, scaling profiles, and failure modes differ.
- A dedicated **Trace Store** Container is non-negotiable for production AI systems; LLM observability cannot be folded into generic APM.
- The **Eval Harness** must be modeled even if it only runs offline — it is the system's quality contract and ADRs reference it.

### Common mistakes

- Treating the LLM provider as an internal Container (it isn't).
- Modeling each LangChain / DSPy / agent SDK chain as a Container (they are Components inside `agentSvc`).
- Omitting the **Sandbox / Tool Execution** boundary when the agent runs untrusted code or shell commands.

---

## Pattern 7: Edge + Origin Split (CDN-resident compute)

### L2 Container

```dsl
system = softwareSystem "Globally Cached Storefront" {
    edge     = container "Edge Runtime" "Routing, A/B, personalisation, auth at the edge" "Cloudflare Workers"
    origin   = container "Origin App" "Authoritative business logic and templates" "Next.js on Node.js"
    api      = container "Core API" "Business logic" "Go"
    kv       = container "Edge KV" "Hot config + session" "Cloudflare KV" "Database"
    db       = container "Database" "Authoritative data" "PostgreSQL" "Database"
}
```

### Characteristics

- The edge runtime is its own Container because it has a distinct runtime (V8 isolate, cold-start envelope, geo distribution).
- Edge KV is a Database Container, not a Component of the edge runtime — its consistency model is fundamentally different from the relational origin DB and must be visible to reviewers.
- Relationships from edge to origin and from edge to KV should carry their latency budgets in the description (e.g., "Reads cached personalisation in `< 5 ms`").

### Common mistakes

- Hiding the edge runtime inside the CDN external system. It belongs to the team that owns the workers.
- Drawing edge → origin as "Uses" — name the actual cache-miss fallback flow.

---

## Modeling with Archetypes (DSL v4.0+)

For models with `5+` containers that share a common technology stack or for relationships that fall into a few protocol families, prefer archetypes over repeating literal labels. The same model from Pattern 1 written with archetypes:

```dsl
model {
    archetypes {
        spaApp     = container { technology "React"; tag "WebBrowser" }
        appServer  = container { technology "Node.js Express" }
        datastore  = container { tag "Database" }
        https      = -> { technology "JSON/HTTPS"; tag "Synchronous" }
    }

    system = softwareSystem "Web Application" {
        spa    = spaApp    "SPA"            "User interface"
        server = appServer "Application Server" "Business logic + API"
        db     = datastore "Database"       "Persistent storage" "PostgreSQL"
        cache  = datastore "Session Store"  "Session and cache"  "Redis"

        spa    --https-> server "Calls REST endpoints"
    }
}
```

Archetypes pay back the most when a model is reviewed repeatedly by multiple teams (the vocabulary becomes the contract) and when styles are tag-driven (one Tag style covers every archetype instance).

---

## Discovery Heuristics

Heuristics for extracting C4 elements from a codebase.

### Container Candidates

| Signal | Suggested Container |
|--------|---------------------|
| `Dockerfile` or `docker-compose.yml` service | Each service is a Container candidate |
| Independent `package.json` | Web app or API Container |
| `go.mod` / `*.csproj` / `pom.xml` (independent) | Service Container |
| DB connection config (`DATABASE_URL`, etc.) | Database Container |
| Message queue connection (`REDIS_URL`, `KAFKA_BROKERS`) | Queue/Cache Container |
| Port config in `.env` | Listening port of an independent Container |
| CI/CD deploy targets | Each target is a Container candidate |
| Kubernetes manifest / ECS task definition | Each workload is a Container |

### External System Candidates

| Signal | Suggested External System |
|--------|---------------------------|
| External API URLs (`stripe.com`, `api.sendgrid.com`) | External SaaS System |
| OAuth config (`GOOGLE_CLIENT_ID`) | Auth provider System |
| CDN config | CDN System |
| External webhook config | External integration System |

### Person Candidates

| Signal | Suggested Person |
|--------|------------------|
| Auth roles (admin, user, viewer) | Each role is a Person candidate |
| API key types (public, internal) | User category |
| User-facing UI vs. admin panel | Separate Persons |

### Component Candidates (L3)

| Signal | Suggested Component |
|--------|---------------------|
| Controller / Handler / Router | API endpoint group |
| Service / UseCase / Interactor | Business logic |
| Repository / DAO / Store | Data access |
| Client / Adapter / Gateway | External integration |
| Middleware / Guard / Filter | Cross-cutting concern |
| Job / Worker / Consumer | Async processing |
