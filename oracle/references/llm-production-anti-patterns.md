# LLM Production Anti-Patterns (2025-2026)

> Production failure modes, architecture anti-patterns, security threats, reasoning limits, MCP anti-patterns

## 1. 8 Production Challenge Categories

| # | Category | Problem | Impact | Mitigation |
|---|---------|---------|--------|-----------|
| **LP-01** | **Hallucination** | Confident generation of plausible falsehoods | Critical | RAG grounding · citation enforcement · low temperature (0.0-0.2) |
| **LP-02** | **Prompt Injection** | Malicious instructions override safety rules | Critical | Input sanitization · instruction/data separation · least privilege · audit logs |
| **LP-03** | **Context Window Limits** | Early info "Lost in the Middle" in long conversations | High | Chunk splitting (400-800 tokens) · top 5-8 retrieval · summary compression |
| **LP-04** | **Non-determinism** | Same input → different output; impossible to debug | High | Fixed temperature · pinned model version · full parameter logging |
| **LP-05** | **Cost & Latency** | $6,000+/month bills; 5-10s response times | High | Model tiering · caching · prompt compression · streaming |
| **LP-06** | **Bias & Fairness** | Gender, race, age biases in outputs | Medium | Diverse demographic testing · >20% deviation flagging · quarterly audits |
| **LP-07** | **Privacy & Data Leakage** | PII exposure from training data or context | Critical | PII detection/masking · tenant isolation · auto-deletion · local models |
| **LP-08** | **Reasoning Limits** | Arithmetic, multi-step logic, temporal reasoning failures | High | Tool calls (calculator, date, policy lookup) · validation layer · specialist models |

---

## 2. Architecture & Design Anti-Patterns

| # | Anti-Pattern | Problem | Fix |
|---|-------------|---------|-----|
| **LA-01** | **Over-complexity** | Multi-agent framework for single-agent problem | Start simplest; escalate only when needed |
| **LA-02** | **Multi-task per request** | Extract + judge + generate in one prompt → hallucination | Single Logical Change: one request = one task |
| **LA-03** | **Framework over-reliance** | Generic platform for all problems | Domain-specific custom tools when needed |
| **LA-04** | **Model infallibility assumption** | Trust LLM output without verification | Treat LLM as "unreliable compute"; validate all outputs |
| **LA-05** | **No output handling** | Pass raw LLM output to downstream systems → XSS/RCE | Output sanitization · schema validation · least privilege |
| **LA-06** | **Floating model names** | `gpt-4` auto-updates → behavior change | Pin exact version (e.g., `claude-sonnet-4-6`) |
| **LA-07** | **Over-privileged agents** | Tool-calling model with broad permissions | Least privilege · read-only default · action audit |
| **LA-08** | **Supply chain blindness** | Ignore model format, server, hub, connector vulnerabilities | Dependency audit · unsafe deserialization detection |

---

## 3. MCP-Specific Anti-Patterns

| # | Anti-Pattern | Problem | Fix |
|---|-------------|---------|-----|
| **MA-01** | **God server** | One MCP server handles all tools | Single responsibility: one server = one domain |
| **MA-02** | **No input validation** | Raw user input passed to tool parameters | Validate and sanitize all parameters before execution |
| **MA-03** | **Unconfirmed state changes** | Tools modify state without user awareness | Require confirmation for writes/deletes/spending; support dry-run |
| **MA-04** | **Secret leakage** | API keys or tokens echoed in tool results | Never return secrets in tool outputs or elicitation messages |
| **MA-05** | **Missing output schemas** | Tool outputs are unstructured → wasted context window | Declare output schemas for efficient token usage |
| **MA-06** | **No rate limiting** | Unrestricted tool invocations → cost explosion | Per-server rate limits and cost ceilings |

---

## 4. Agent-Specific Anti-Patterns

| # | Anti-Pattern | Problem | Fix |
|---|-------------|---------|-----|
| **AA-01** | **God agent** | One agent handles all responsibilities | Single responsibility per agent |
| **AA-02** | **Implicit communication** | Natural language only between agents | Structured data interfaces (JSON schemas) |
| **AA-03** | **Failure propagation** | Sub-agent failure crashes entire system | Fault isolation; graceful degradation |
| **AA-04** | **Distributed decisions** | No central management; each agent decides independently | Orchestration layer for coordination |
| **AA-05** | **Infinite loops** | ReAct agent without step cap; recursive tool calls | Max steps + circuit breaker + cost ceiling |
| **AA-06** | **Heavy custom agents** | 25k+ token agent definitions → bottleneck | Keep agents <3k tokens for fluid orchestration |

---

## 5. Reasoning Limit Compensations

```
Areas where LLMs fail and compensations:

  Arithmetic: $47,382 − $31,547 − $8,200 = ?
    LLM answer: $7,600 (correct: $7,635)
    → Tool call: calculator, spreadsheet functions

  Multi-step logic: Missing steps, dropped conditions
    → Chain-of-Thought + structured output + step count verification

  Constraint satisfaction: Policy check omissions
    → Constraint checker + validation layer

  Temporal reasoning: Relative dates, timezone errors
    → Dedicated tool call + current time context injection

Core principle:
  "Don't try to make the LLM perfect — build a system
   that works reliably DESPITE the LLM's flaws."
```

---

## 6. Security Threat Matrix (OWASP LLM 2025 Alignment)

| Threat | Attack Vector | Defense |
|--------|--------------|---------|
| **Prompt Injection** | "Ignore previous instructions..." in documents | Instruction/data separation · input sanitization · pattern blocking |
| **Unsafe Output Handling** | LLM-generated HTML/JS rendered unsanitized | Output escaping · CSP headers · sandboxed execution |
| **Sensitive Info Disclosure** | PII in context leaks to response | PII masking · output filtering · data isolation |
| **Excessive Agency** | Tool calls perform unintended actions | Least privilege · human approval gates · action audit |
| **Data Poisoning** | Malicious documents injected into RAG index | Source authentication · data quality checks · anomaly detection |
| **System Prompt Leakage** | Attacker extracts system prompt contents | Externalize secrets · output guardrails · prompt isolation |
| **Vector Weaknesses** | RAG vector DB unauthorized access / poisoning | Access controls · fine-grained partitioning · source validation |

---

## 7. Oracle Integration

```
Oracle workflow integration:
  1. ASSESS: Run LP-01–08 detection checklist on existing system
  2. DESIGN: Avoid LA-01–08 and MA-01–06 in architecture
  3. SPECIFY: Include security requirements (OWASP alignment) in specs
  4. EVALUATE: Test reasoning limit compensations for effectiveness

Quality gates:
  - No output validation → block at DESIGN (LA-04, LA-05)
  - Model version not pinned → require exact version (LA-06)
  - No permission design → require least privilege (LA-07)
  - Arithmetic/logic tasks without tool calls → add compensation (LP-08)
  - MCP server with broad scope → require single responsibility (MA-01)
  - Agent without step cap → require circuit breaker (AA-05)
```

**Source:** [ShiftAsia: 8 LLM Production Challenges](https://shiftasia.com/community/8-llm-production-challenges-problems-solutions/) · [Martin Fowler: GenAI Patterns](https://martinfowler.com/articles/gen-ai-patterns/) · [OWASP Top 10 for LLM 2025](https://genai.owasp.org/llm-top-10/) · [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) · [Anthropic: Building Agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
