# AI Safety Reference

ガードレール設計、ハルシネーション検出、バイアス評価、コンテンツフィルタリングのリファレンス。

---

## Guardrail Architecture

### Defense in Depth

```
User Input → [Input Guardrails] → [LLM] → [Output Guardrails] → User Output
                 ↓                              ↓
           - PII detection               - Hallucination check
           - Prompt injection             - Toxicity filter
           - Topic boundary               - PII redaction
           - Rate limiting                - Format validation
```

### Input Guardrails

| Guardrail | Purpose | Implementation |
|-----------|---------|----------------|
| **Prompt injection detection** | Prevent instruction override | Classifier + heuristics |
| **PII detection** | Protect user data | Regex + NER model |
| **Topic boundary** | Keep conversation on-topic | Intent classifier |
| **Input length limit** | Prevent token abuse | Token counter |
| **Rate limiting** | Prevent abuse | Token bucket per user |

### Output Guardrails

| Guardrail | Purpose | Implementation |
|-----------|---------|----------------|
| **Factuality check** | Verify claims against sources | Source attribution |
| **PII redaction** | Remove leaked PII | Regex + NER |
| **Toxicity filter** | Block harmful content | Classifier |
| **Format validation** | Ensure output structure | Schema validation |
| **Confidence threshold** | Flag uncertain answers | Self-evaluation prompt |

---

## Hallucination Detection

### Detection Strategies

| Strategy | Mechanism | Reliability |
|----------|-----------|-------------|
| **Source attribution** | Require citations for claims | High |
| **Self-consistency** | Multiple generations, compare | Medium-High |
| **Retrieval verification** | Check claims against knowledge base | High |
| **Confidence scoring** | LLM self-rates confidence | Medium |
| **Entailment check** | NLI model on (source, claim) pairs | High |

### Grounding Template

```markdown
## Instructions
Answer the question based ONLY on the provided context.
If the answer is not in the context, say "I don't have enough information to answer that."

## Context
{retrieved_documents}

## Rules
- Every factual claim must be supported by the context
- Use [Source: doc_id] citations after each claim
- If you're uncertain, state your uncertainty explicitly
- Never extrapolate beyond what the context states

## Question
{user_question}
```

### Hallucination Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Faithfulness** | >0.95 | % claims supported by sources |
| **Answer relevancy** | >0.85 | % answer addresses question |
| **Context precision** | >0.80 | % retrieved docs are relevant |
| **Context recall** | >0.80 | % relevant docs are retrieved |

---

## Bias Evaluation

### Evaluation Dimensions

| Dimension | Test Method | Example |
|-----------|------------|---------|
| **Gender** | Swap pronouns, check output consistency | "He/She is a CEO..." |
| **Race/Ethnicity** | Swap names, check treatment consistency | Various cultural names |
| **Age** | Test with different age contexts | "25-year-old" vs "65-year-old" |
| **Socioeconomic** | Test with different economic contexts | Loan approval scenarios |

### Bias Test Framework

```python
class BiasTest:
    def __init__(self, prompt_template: str, model: str):
        self.template = prompt_template
        self.model = model

    def test_gender_bias(self, input_text: str) -> BiasResult:
        variants = {
            "male": input_text.replace("{pronoun}", "he"),
            "female": input_text.replace("{pronoun}", "she"),
            "neutral": input_text.replace("{pronoun}", "they"),
        }

        results = {k: call_llm(self.template, v) for k, v in variants.items()}
        return BiasResult(
            variance=calculate_variance(results),
            flagged=any_significant_difference(results)
        )
```

---

## Content Filtering

### Moderation Categories

| Category | Risk Level | Action |
|----------|-----------|--------|
| **Hate speech** | Critical | Block + Log |
| **Violence** | Critical | Block + Log |
| **Self-harm** | Critical | Block + Escalate |
| **Sexual content** | High | Block + Log |
| **Misinformation** | Medium | Flag + Disclaimer |
| **Off-topic** | Low | Redirect |

### Safety Response Templates

```python
SAFETY_RESPONSES = {
    "off_topic": "I'm designed to help with {domain}. Could you rephrase your question?",
    "uncertain": "I'm not confident in my answer. Please verify with {source}.",
    "no_info": "I don't have enough information to answer accurately.",
    "pii_detected": "I noticed personal information in your message. For security, I've redacted it.",
    "blocked": "I can't help with that request. Is there something else I can assist with?"
}
```

---

## PII Handling

### PII Categories

| Category | Examples | Detection | Action |
|----------|----------|-----------|--------|
| **Direct identifiers** | SSN, passport | Regex | Redact before LLM |
| **Contact info** | Email, phone | Regex | Redact or mask |
| **Financial** | Credit card, bank account | Regex + Luhn | Redact before LLM |
| **Health** | Medical records, conditions | NER model | Redact before LLM |
| **Names** | Full names | NER model | Context-dependent |

### Redaction Strategy

```python
def redact_pii(text: str) -> tuple[str, dict]:
    """Redact PII and return mapping for re-identification."""
    mapping = {}

    # Email
    for match in re.finditer(r'\b[\w.+-]+@[\w-]+\.[\w.-]+\b', text):
        placeholder = f"[EMAIL_{len(mapping)}]"
        mapping[placeholder] = match.group()
        text = text.replace(match.group(), placeholder)

    # Phone
    for match in re.finditer(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text):
        placeholder = f"[PHONE_{len(mapping)}]"
        mapping[placeholder] = match.group()
        text = text.replace(match.group(), placeholder)

    return text, mapping
```
