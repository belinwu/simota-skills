# AI Safety & Guardrails (2025-2026)

> OWASP Top 10 for LLM 2025, guardrail architecture, hallucination detection, PII handling, agent safety

## 1. OWASP Top 10 for LLM Applications (2025)

| # | Threat | Risk | Key Mitigations |
|---|--------|------|-----------------|
| **LLM01** | **Prompt Injection** | Attacker overrides instructions via direct/indirect injection | Instruction/data separation · input sanitization · pattern blocking |
| **LLM02** | **Sensitive Information Disclosure** | PII leaks via training data, RAG, or jailbreaks | Data sanitization · input/output validation · PII masking |
| **LLM03** | **Supply Chain** | Backdoors in pre-trained models, LoRA adapters, datasets | Verified sources · integrity checks · signed SBOM |
| **LLM04** | **Data Poisoning** | Manipulated training/fine-tuning data | Data provenance tracking · trusted source validation |
| **LLM05** | **Improper Output Handling** | Unvalidated LLM output to downstream systems (XSS, RCE) | Context-aware encoding · output sanitization · sandboxed execution |
| **LLM06** | **Excessive Agency** | Agentic systems granted too much autonomy/permissions | Minimal tool scope · human approval gates · action audit |
| **LLM07** | **System Prompt Leakage** | Sensitive info in system prompts exposed to attackers | Keep secrets external · output guardrails · prompt isolation |
| **LLM08** | **Vector & Embedding Weaknesses** | RAG vector DB access, embedding inversion, data poisoning | Access controls · fine-grained partitioning · source validation |
| **LLM09** | **Misinformation** | Hallucinations, bias, user over-reliance | RAG with verified sources · cross-verification · human fact-checking |
| **LLM10** | **Unbounded Consumption** | Resource exhaustion from oversized inputs or request floods | Rate limiting · timeouts · dynamic resource monitoring |

---

## 2. Guardrail Architecture — Defense in Depth

```
User Input → [Input Guardrails] → [LLM] → [Output Guardrails] → User Output
                   ↓                              ↓
             - PII detection               - Hallucination check
             - Prompt injection             - Toxicity filter
             - Topic boundary               - PII redaction
             - Input length limit           - Format validation
             - Rate limiting                - Confidence threshold
```

### Input Guardrails

| Guardrail | Purpose | Implementation |
|-----------|---------|----------------|
| **Prompt injection detection** | Prevent instruction override | Classifier + heuristics + instruction/data separation |
| **PII detection** | Protect user data | Regex + NER model; redact BEFORE sending to LLM |
| **Topic boundary** | Keep on-topic | Intent classifier |
| **Input length limit** | Prevent token abuse | Token counter with hard ceiling |
| **Rate limiting** | Prevent abuse | Token bucket per user/session |

### Output Guardrails

| Guardrail | Purpose | Implementation |
|-----------|---------|----------------|
| **Factuality check** | Verify claims against sources | Source attribution + citation enforcement |
| **PII redaction** | Remove leaked PII from output | Regex + NER post-processing |
| **Output sanitization** | Prevent XSS/injection in downstream use | Context-aware encoding before rendering |
| **Format validation** | Ensure output structure | JSON schema validation (Structured Outputs) |
| **Confidence threshold** | Flag uncertain answers | Self-evaluation prompt or calibrated scoring |

---

## 3. Hallucination Detection

| Strategy | Mechanism | Reliability |
|----------|-----------|-------------|
| **Source attribution** | Require [Source: doc_id] citations | High |
| **Self-consistency** | Multiple generations, compare for agreement | Medium-High |
| **Retrieval verification** | Check claims against knowledge base | High |
| **Entailment check** | NLI model on (source, claim) pairs | High |
| **Confidence scoring** | LLM self-rates confidence | Medium |

### Grounding Prompt Template

```markdown
Answer based ONLY on the provided context.
If the answer is not in the context, say "I don't have enough information."

Rules:
- Every factual claim must be supported by the context
- Use [Source: doc_id] citations after each claim
- State uncertainty explicitly when applicable
- Never extrapolate beyond what the context states
```

### Faithfulness Targets

| Metric | Target |
|--------|--------|
| Faithfulness | >0.95 (claims supported by sources) |
| Answer relevancy | >0.85 (answer addresses question) |
| Context precision | >0.80 (retrieved docs are relevant) |
| Context recall | >0.80 (relevant docs are retrieved) |

---

## 4. Agent Safety (2025 — Year of LLM Agents)

### Excessive Agency Prevention

| Principle | Implementation |
|-----------|---------------|
| **Least privilege** | Read-only default; allowlist only needed permissions |
| **Human approval gates** | Require confirmation for state changes, spending, external actions |
| **Action audit** | Log all tool calls with timestamps, parameters, results |
| **Scope limitation** | One agent = one bounded responsibility |
| **Cost/time caps** | Per-execution budget ceiling + circuit breaker |

### MCP Security

- OAuth 2.1 mandatory for HTTP-based transport
- Never echo secrets in tool results or elicitation messages
- Validate all tool parameters before execution
- Require confirmation for state-changing or cost-incurring operations
- Implement dry-run mode for destructive actions

---

## 5. PII Handling

| Category | Examples | Detection | Action |
|----------|----------|-----------|--------|
| **Direct identifiers** | SSN, passport | Regex | Redact BEFORE LLM |
| **Contact info** | Email, phone | Regex | Redact or mask |
| **Financial** | Credit card, bank account | Regex + Luhn | Redact BEFORE LLM |
| **Health** | Medical records | NER model | Redact BEFORE LLM |
| **Names** | Full names | NER model | Context-dependent |

### Redaction Strategy

```python
def redact_pii(text: str) -> tuple[str, dict]:
    """Redact PII and return mapping for re-identification if needed."""
    mapping = {}
    # Email, Phone, SSN patterns → replace with [EMAIL_0], [PHONE_0], etc.
    # Store mapping for post-processing re-insertion if required
    return redacted_text, mapping
```

---

## 6. Bias Evaluation

| Dimension | Test Method | Flag Threshold |
|-----------|------------|----------------|
| **Gender** | Swap pronouns, compare outputs | >20% variance |
| **Race/Ethnicity** | Swap names, compare treatment | >20% variance |
| **Age** | Test with different age contexts | >20% variance |
| **Socioeconomic** | Test with different economic contexts | >20% variance |

Schedule: Quarterly bias audits for production systems.

---

## 7. Regulatory Compliance (2025-2026)

```
EU AI Act / US State Laws:
  1. Traceability: Link eval scores to exact prompt/model/dataset versions
  2. Fairness audits: Quarterly bias testing
  3. Audit trail: Immutable logs of all tool calls and decision rationale
  4. Data protection: PII masking · tenant isolation · data residency
  5. Accountability: Human approval gates for high-risk decisions
  6. Transparency: Disclose AI involvement to end users where required
```

---

## 8. Oracle Integration

```
Oracle workflow integration:
  1. ASSESS: Evaluate against OWASP LLM01–10 checklist
  2. DESIGN: Apply defense-in-depth guardrail architecture
  3. SPECIFY: Include security requirements in Builder handoff specs
  4. EVALUATE: Run adversarial testing (prompt injection, PII leak, bias)

Quality gates:
  - No output validation → block at DESIGN (LLM05)
  - No prompt injection defense → require input guardrails (LLM01)
  - Agent with broad permissions → require least-privilege design (LLM06)
  - System prompt contains secrets → externalize (LLM07)
  - No PII handling → require redaction strategy (LLM02)
```

**Source:** [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/) · [Confident AI: OWASP Top 10 2025 Analysis](https://www.confident-ai.com/blog/owasp-top-10-2025-for-llm-applications-risks-and-mitigation-techniques) · [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) · [Anthropic: Agent Safety](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
