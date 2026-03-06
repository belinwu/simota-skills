# Prompt Engineering Patterns (2025-2026)

> Design patterns, versioning, testing, optimization, and Claude 4.x–specific techniques

## 1. Core Design Patterns

| Pattern | Description | Best For |
|---------|-------------|----------|
| **Role-based** | Assign persona with expertise in system prompt | Domain-specific tasks |
| **Chain-of-Thought** | Step-by-step reasoning (or use extended thinking) | Complex reasoning, math |
| **Few-shot** | 3–5 structured examples in `<examples>` tags | Format consistency, tone |
| **Self-consistency** | Multiple reasoning paths → majority vote | High-stakes decisions |
| **ReAct** | Reasoning + Action interleaving | Tool-using agents |
| **Plan-and-Execute** | Plan steps → execute each with validation | Multi-step workflows |

### Prompt Structure Template

```markdown
## Role
You are [role] with expertise in [domain].

## Context
[Background information relevant to the task]

## Instructions
1. [Step 1]
2. [Step 2]

## Output Format
[Exact format specification with example]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Examples
<examples>
  <example>
    <input>[example input]</input>
    <output>[example output]</output>
  </example>
</examples>
```

---

## 2. Claude 4.x–Specific Techniques

### Adaptive Thinking (Opus 4.6 / Sonnet 4.6)

```python
# Adaptive thinking — Claude decides when and how much to think
client.messages.create(
    model="claude-opus-4-6",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},  # max | high | medium | low
    messages=[{"role": "user", "content": "..."}],
)
```

| Effort | Use Case | Thinking Behavior |
|--------|----------|-------------------|
| `max` | Research, deep analysis | Maximum reasoning depth |
| `high` | Agentic coding, multi-step | Deep reasoning on complex queries |
| `medium` | General tasks | Balanced quality/speed |
| `low` | High-volume, latency-sensitive | Minimal or no thinking |

**Key rules:**
- Prefer `"think thoroughly"` over hand-written step-by-step plans — Claude's reasoning often exceeds what you'd prescribe
- Use `<thinking>` tags in few-shot examples to show reasoning patterns
- Ask Claude to self-check: "Before finishing, verify your answer against [criteria]"
- If Claude overthinks, add: "Choose an approach and commit. Avoid revisiting decisions unless new information contradicts your reasoning."

### Structured Outputs

```python
# Guaranteed JSON schema compliance (beta)
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": text}],
    # Option 1: Tool-based structured output
    tools=[{
        "name": "extract_info",
        "description": "Extract structured information",
        "input_schema": schema
    }],
    tool_choice={"type": "tool", "name": "extract_info"}
)

# Option 2: output_format for JSON mode
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    output_format={"type": "json", "schema": schema},
    messages=[...]
)
```

### XML Tags — Claude's Native Structuring

```xml
<instructions>Task description</instructions>
<context>Background information</context>
<documents>
  <document index="1">
    <source>file.md</source>
    <document_content>{{CONTENT}}</document_content>
  </document>
</documents>
<output_format>Expected structure</output_format>
```

**Best practices:**
- Use consistent, descriptive tag names
- Nest tags for hierarchical content
- Place long documents at the TOP of the prompt (up to 30% quality improvement)
- Use `<example>` tags to separate examples from instructions

### Prefill Deprecation (Claude 4.6+)

Prefilled responses on the last assistant turn are no longer supported. Migrations:

| Old Pattern | New Approach |
|-------------|-------------|
| Force JSON format | Structured Outputs API or tool_choice |
| Skip preamble | System prompt: "Respond directly without preamble" |
| Avoid refusals | Clear prompting (Claude 4.6 handles refusals better) |
| Continuations | "Your previous response ended with `[text]`. Continue from there." |

---

## 3. Prompt Versioning

```
prompts/
├── v1.0.0/
│   ├── system.md
│   ├── examples.json
│   └── config.yaml
├── v2.0.0/
│   └── ...
└── registry.json        # Active version mapping
```

| Change Type | Version Bump | Example |
|------------|-------------|---------|
| Instructions rewrite | Major (X.0.0) | System prompt restructured |
| Few-shot examples updated | Minor (0.X.0) | Added 3 new examples |
| Wording tweaks | Patch (0.0.X) | Clarified constraint |

---

## 4. Prompt Testing

### Test Case Categories

| Category | Priority | Description |
|----------|----------|-------------|
| **Happy path** | Must pass | Normal expected inputs |
| **Edge cases** | Must pass | Empty, very long, special characters |
| **Adversarial** | Must pass | Prompt injection, role-breaking |
| **Format** | Must pass | Output matches expected structure |
| **Consistency** | Should pass | Same input → similar output |
| **Regression** | Must pass | Previously fixed issues don't recur |

### A/B Testing

```python
class PromptABTest:
    def run(self, test_cases, metrics: list[str]) -> dict:
        for case in test_cases:
            for variant_name, prompt in self.variants.items():
                response = call_llm(prompt, case.input, self.model)
                scores = {m: evaluate_metric(m, response, case) for m in metrics}
                self.results[variant_name].append(scores)
        return {
            "winner": self.determine_winner(),
            "metrics": self.aggregate_metrics(),
            "significance": self.statistical_test()
        }
```

---

## 5. Optimization Checklist

- [ ] Remove unnecessary context that doesn't improve output
- [ ] Test with fewer examples (start with 0, add until quality meets threshold)
- [ ] Try smaller model with optimized prompt before using larger model
- [ ] Measure cost per query and quality score together
- [ ] Use appropriate effort level (low for simple, high for complex)
- [ ] Enable prompt caching for repeated system prompts
- [ ] Validate with regression test suite after any change
- [ ] Remove over-prompting from pre-4.6 era ("CRITICAL: You MUST..." → "Use this tool when...")

---

## 6. Agentic Prompt Patterns

### Parallel Tool Calling

```xml
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies
between the tool calls, make all independent calls in parallel.
Do NOT call dependent tools in parallel — call them sequentially.
Never use placeholders or guess missing parameters.
</use_parallel_tool_calls>
```

### Autonomy vs Safety Balance

```
Consider the reversibility and potential impact of your actions.
Freely take local, reversible actions (editing files, running tests).
For actions that are hard to reverse or affect shared systems,
ask the user before proceeding.
```

### Subagent Orchestration

- Light custom agents (<3k tokens) enable fluid orchestration
- Heavy agents (25k+ tokens) create bottlenecks
- Explicit guidance prevents excessive delegation:
  "Use subagents when tasks can run in parallel or require isolated context.
   For simple tasks or single-file edits, work directly."

**Source:** [Anthropic: Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) · [Anthropic: Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) · [Anthropic: Adaptive Thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) · [Anthropic: Building Agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
