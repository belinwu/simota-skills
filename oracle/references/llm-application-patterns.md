# LLM Application Patterns (2025-2026)

> Agent architecture, MCP integration, tool use design, structured output, caching, streaming

## 1. Agent Architecture Patterns

| # | Pattern | Structure | Best For | Risk |
|---|---------|-----------|----------|------|
| **AP-01** | **ReAct** | Think → Act → Observe loop | General reasoning + tool use | Infinite loops, reasoning drift |
| **AP-02** | **Plan-and-Execute** | Plan phase → Execute phase | Long tasks, multi-step | Plan rigidity, replan cost |
| **AP-03** | **Specialized Multi-Agent** | Role-per-agent + orchestration | Composite domains | Handoff failure, state inconsistency |
| **AP-04** | **Router** | Input classification → specialist routing | Diverse input types | Misclassification |
| **AP-05** | **Supervisor** | Central agent manages child agents | Team-style tasks | Bottleneck risk |

### Default Recommendation

```
Plan-and-Execute as default:
  - Reduces iterative back-and-forth vs pure ReAct
  - Better performance on long tasks (LangChain analysis)
  - Explicit plans enable audit and debugging
  - Use ReAct loops only for dynamic sub-tasks

Decision flow:
  Fixed sequence, predictable branching → Deterministic workflow (Airflow / Temporal)
  Dynamic branching, tool selection needed → Agent (LLM-based decision loop)
  Predictable stages + some dynamic decisions → Hybrid (fixed workflow + agent branches)
```

---

## 2. Agent Reliability Principles

| # | Principle | Implementation |
|---|-----------|---------------|
| **1** | Structured output enforcement | JSON schema on all outputs; auto-repair on schema violation |
| **2** | Validation at every step | Pass/fail check per sub-task, not just at the end |
| **3** | Immutable audit trail | Trace all tool calls and decision rationale |
| **4** | Least-privilege access | NIST AC-6; role-based tool access; read-only default |
| **5** | Cost & latency caps | Circuit breaker, rate limiting, per-execution budget |

### Agent Failure Modes

| Failure Mode | Detection | Mitigation |
|-------------|-----------|-----------|
| **Format Drift** | Schema validation | Structured Outputs enforcement |
| **Plan Divergence** | Step count monitoring | ReAct paradigm (reasoning + observation) |
| **Ambiguity Loops** | Loop count detection | Explicit schema for tool selection |
| **Silent Errors** | Output quality sampling | Validation-embedded planning |
| **Tool Abuse** | Tool call audit log | Usage policy + permission restrictions |
| **Cost Explosion** | Cost monitoring, step cap | Per-execution cost ceiling + circuit breaker |
| **State Corruption** | State snapshot comparison | Explicit state management + transactions |

---

## 3. Model Context Protocol (MCP)

### Architecture

```
Host Application ←→ MCP Client ←→ MCP Server
                                      ↓
                              [Tools | Resources | Prompts]
```

**Core primitives:**
- **Tools**: Actions the AI can invoke (like function calls)
- **Resources**: Structured data sources for context (read-only)
- **Prompts**: Predefined templates for specific tasks

### MCP Best Practices

| Practice | Detail |
|----------|--------|
| Single Responsibility | One server = one clear purpose |
| Security (OAuth 2.1) | Mandatory for HTTP transport; never echo secrets |
| Transport | stdio for local; Streamable HTTP for networked/scalable |
| Idempotent tools | Accept client-generated request IDs; deterministic results |
| Pagination | Use cursors/tokens for list operations; keep responses small |
| Consent & confirmation | Require confirmation for state changes or spending; support dry-run mode |
| Output schemas | Declare tool output shapes for efficient context window usage |
| LLM + human readable | Structured JSON for model; content blocks for users |

### MCP Security Considerations

- Never pass raw user input to MCP tool parameters without sanitization
- Validate all tool results before passing to LLM context
- Implement rate limiting per MCP server connection
- Log all tool invocations for audit
- Use fine-grained permissions per tool (read vs write vs delete)

---

## 4. Tool Use Design

### Tool Definition Best Practices

```json
{
  "name": "search_knowledge_base",
  "description": "Search the company knowledge base for relevant articles. Use when user asks about policies, procedures, or product features.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": { "type": "string", "description": "Search query in natural language" },
      "category": { "type": "string", "enum": ["billing", "technical", "policy"] },
      "max_results": { "type": "integer", "default": 5 }
    },
    "required": ["query"]
  }
}
```

| Guideline | Reason |
|-----------|--------|
| Clear, specific descriptions | LLM uses description to decide when to call |
| Minimal required parameters | Reduces friction and errors |
| Enum values where possible | Constrains to valid options |
| Default values for optional params | Simplifies common usage |
| Error messages in tool results | Helps LLM recover gracefully |

---

## 5. Structured Output Patterns

### Validation Pipeline

```python
from pydantic import BaseModel, validator

class LLMOutput(BaseModel):
    intent: str
    confidence: float
    entities: list[str]

    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Confidence must be between 0 and 1')
        return v

def parse_llm_response(response: str) -> LLMOutput:
    try:
        data = json.loads(response)
        return LLMOutput(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        raise LLMOutputError(f"Invalid output: {e}")
```

---

## 6. Caching Strategies

| Strategy | Cache Key | TTL | Use Case | Expected Hit Rate |
|----------|----------|-----|----------|------------------|
| **Exact match** | Hash(prompt + input) | Hours-Days | Identical queries | 40-70% (classification) |
| **Semantic cache** | Embedding similarity > 0.95 | Hours | Similar queries | 10-30% (chat) |
| **Prompt cache** | System prompt hash | Session | Repeated system prompts | Up to 90% cost reduction |
| **KV cache** | Conversation prefix | Minutes | Multi-turn | Provider-managed |

### Prompt Caching Impact

```
Prompt caching (provider-level):
  - Latency reduction: up to 80%
  - Input token cost reduction: up to 90%
  - Best for: stable system prompts, tool definitions, shared RAG context
  - Caveat: dynamic content reduces hit rate
```

---

## 7. Multi-Agent Design Principles

```
4 design principles:
  1. Single responsibility: each agent = one clear role
  2. Explicit interfaces: structured data for inter-agent communication
  3. Fault isolation: one agent failure ≠ system-wide failure
  4. Orchestration layer: central coordination (safer than distributed decisions)

Anti-patterns:
  - God agent: one agent handles everything
  - Implicit communication: natural language only between agents
  - Failure propagation: sub-agent failure crashes entire system
  - Distributed decisions: no central management, each agent decides independently

Agent sizing:
  - Light (<3k tokens): fluid orchestration, fast context loading
  - Heavy (25k+ tokens): bottleneck in multi-agent workflows
```

---

## 8. Streaming & UX Patterns

| Pattern | Use Case |
|---------|----------|
| **Token streaming** (SSE/WebSocket) | Chat interfaces |
| **Progressive loading** | Long generation |
| **Optimistic UI** | Form submissions |
| **Cancellation** (AbortController) | User-initiated stop |

---

## 9. Oracle Integration

```
Oracle workflow integration:
  1. DESIGN: Select agent pattern (AP-01–05) based on task complexity
  2. ASSESS: Evaluate reliability principles compliance
  3. SPECIFY: Include MCP tool definitions and agent contracts in Builder specs
  4. EVALUATE: Design failure mode detection tests

Quality gates:
  - No structured output schema → block at DESIGN (Format Drift prevention)
  - No per-step validation → require validation-embedded plan (Silent Errors prevention)
  - No cost cap → require budget estimate + ceiling (Cost Explosion prevention)
  - Multi-agent with implicit communication → require structured interfaces
```

**Source:** [Anthropic: Building Agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) · [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) · [The New Stack: 15 Best Practices for MCP Servers](https://thenewstack.io/15-best-practices-for-building-mcp-servers-in-production/) · [StackAI: Agentic Workflow Architectures 2026](https://www.stackai.com/blog/the-2026-guide-to-agentic-workflow-architectures) · [Google ADK: Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
