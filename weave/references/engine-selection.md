# Workflow Engine Selection Guide

**Purpose:** Selection guide for workflow engines.
**Read when:** Picking the right workflow engine for a project.

---

## Engine Comparison Matrix

| Engine | Type | Language | Hosting | Durability | Complexity | Cost Model |
|--------|------|----------|---------|------------|------------|------------|
| Temporal | General | Go/Java/TS/Python | Self/Cloud | High | Medium-High | Self: infra, Cloud: per-action |
| AWS Step Functions | Serverless | ASL (JSON) | AWS | High | Medium | Per transition |
| Inngest | Event-driven | TS/Go/Python | Cloud/Self | High | Low-Medium | Per run |
| XState | Client-side | TS/JS | N/A (in-process) | None (stateless) | Low-Medium | Free |
| Cadence | General | Go/Java | Self-hosted | High | High | Infra only |
| Apache Airflow | Data pipeline | Python | Self/Cloud | Medium | Medium | Infra only |
| Prefect | Data pipeline | Python | Self/Cloud | Medium | Low-Medium | Per task |

---

## Selection Decision Tree

```
What kind of workflow is it?
├── Frontend state management
│   └── XState
├── Data pipeline / ETL
│   ├── Python-heavy → Airflow or Prefect
│   └── Stream integration → Kafka Streams (see Stream agent)
├── Serverless / event-driven
│   ├── AWS-only → Step Functions
│   └── Multi-cloud → Inngest
└── General business workflow
    ├── Already on AWS → Step Functions
    ├── Multi-cloud / high availability
    │   ├── Want managed service → Temporal Cloud
    │   └── Self-hosting OK → Temporal OSS or Cadence
    └── Simple event chain → Inngest
```

---

## Temporal

### Strengths
- Language-native workflow definitions (code is the workflow)
- Strong durability guarantees (replay-safe execution)
- Signal/Query/Update for external interaction with workflow state
- Child Workflow and Continue-as-new support long-running workflows

### Best For
- Long-running business processes (days to months)
- Complex compensation and retry logic
- Microservice-to-microservice orchestration

### Template

```yaml
TEMPORAL_WORKFLOW:
  name: "[WorkflowName]"
  task_queue: "[queue-name]"
  workflow_execution_timeout: "30d"
  activities:
    - name: "[ActivityName]"
      start_to_close_timeout: "30s"
      retry_policy:
        initial_interval: "1s"
        backoff_coefficient: 2.0
        maximum_attempts: 5
        non_retryable_error_types: ["BusinessError"]
  signals:
    - name: "[SignalName]"
      description: "[External trigger]"
  queries:
    - name: "[QueryName]"
      description: "[State inspection]"
```

---

## AWS Step Functions

### Strengths
- Native integration with AWS services (Lambda, SQS, DynamoDB, etc.)
- Declarative workflow definitions via ASL
- Two execution modes: Express and Standard
- Built-in error handling and retries

### Best For
- AWS-centric architectures
- Serverless workflows
- Orchestrating Lambda functions

### Template

```json
{
  "Comment": "[WorkflowDescription]",
  "StartAt": "[FirstState]",
  "States": {
    "[StateName]": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...",
      "Retry": [{
        "ErrorEquals": ["States.TaskFailed"],
        "IntervalSeconds": 2,
        "MaxAttempts": 3,
        "BackoffRate": 2.0
      }],
      "Catch": [{
        "ErrorEquals": ["States.ALL"],
        "Next": "[ErrorHandler]"
      }],
      "Next": "[NextState]"
    }
  }
}
```

---

## Inngest

### Strengths
- Event-driven with a simple API
- Serverless-first (integrates with Vercel, Cloudflare, and others)
- Built-in step functions, sleep, and wait-for-event
- Great local development experience (Dev Server)

### Best For
- Next.js / Vercel-based projects
- Event-driven workflows
- Background jobs

### Template (TypeScript)

```typescript
// Inngest function definition
const workflow = inngest.createFunction(
  { id: "[function-id]", retries: 3 },
  { event: "[trigger/event]" },
  async ({ event, step }) => {
    const result1 = await step.run("[step-1]", async () => {
      // Step 1 logic
    });

    await step.sleep("wait-period", "1h");

    const result2 = await step.run("[step-2]", async () => {
      // Step 2 logic using result1
    });

    return { result1, result2 };
  }
);
```

---

## XState (v5)

### Strengths
- TypeScript type safety
- Works in both browser and Node.js
- Visual editor via Stately Studio
- Scalable design built on the actor model

### Best For
- Frontend state management
- Form wizards and UI flows
- Client-side workflows

### Template

```typescript
import { createMachine } from 'xstate';

const machine = createMachine({
  id: '[machineName]',
  initial: '[initialState]',
  context: {
    // typed context
  },
  states: {
    // state definitions
  },
});
```

---

## Non-Functional Requirements Checklist

Non-functional requirements to verify during selection:

| Requirement | Question |
|-------------|----------|
| Durability | Can a workflow resume if the process crashes mid-execution? |
| Scalability | What is the concurrency ceiling? Does it scale out? |
| Observability | Are execution-state visibility, logs, and metrics sufficient? |
| Cost | Cost projection based on execution count and transition count |
| Latency | Latency requirements between steps |
| Vendor lock-in | Degree of dependency on a specific cloud vendor |
| Team skill | Fit with the team's existing skill set |
| Community | Community activity and documentation quality |
