# Prompt Engineering Patterns

プロンプト設計パターン、バージョニング、テスト、最適化のリファレンス。

---

## Prompt Design Patterns

### System Prompt Architecture

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Role-based** | Assign persona with expertise | Domain-specific tasks |
| **Chain-of-Thought** | Step-by-step reasoning | Complex reasoning, math |
| **Few-shot** | Include examples in prompt | Format consistency |
| **Self-consistency** | Multiple reasoning paths → majority vote | High-stakes decisions |
| **ReAct** | Reasoning + Action interleaving | Tool-using agents |
| **Tree-of-Thought** | Branching exploration paths | Creative/planning tasks |

### Prompt Structure Template

```markdown
## Role
You are [role] with expertise in [domain].

## Context
[Background information relevant to the task]

## Instructions
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Output Format
[Exact format specification with example]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Examples
### Input: [example input]
### Output: [example output]
```

### Output Control Techniques

| Technique | Implementation | When to Use |
|-----------|---------------|-------------|
| **JSON mode** | `response_format: { type: "json_object" }` | Structured data extraction |
| **Function calling** | Tool/function definitions | API integration |
| **XML tags** | `<output>...</output>` | Delimiter-based parsing |
| **Markdown** | Headers, lists, code blocks | Human-readable structured output |

---

## Prompt Versioning

### Version Control Strategy

```
prompts/
├── v1.0.0/
│   ├── system.md
│   ├── examples.json
│   └── config.yaml
├── v1.1.0/
│   ├── system.md
│   ├── examples.json
│   └── config.yaml
└── registry.json        # Active version mapping
```

### Registry Format

```json
{
  "prompts": {
    "classify-intent": {
      "active": "v1.1.0",
      "rollback": "v1.0.0",
      "model": "claude-sonnet-4-5-20250929",
      "temperature": 0.0,
      "max_tokens": 500
    },
    "generate-summary": {
      "active": "v2.0.0",
      "rollback": "v1.3.0",
      "model": "claude-haiku-4-5-20251001",
      "temperature": 0.3,
      "max_tokens": 1000
    }
  }
}
```

### Version Naming

| Change Type | Version Bump | Example |
|------------|-------------|---------|
| Instructions rewrite | Major (X.0.0) | System prompt restructured |
| Few-shot examples updated | Minor (0.X.0) | Added 3 new examples |
| Wording tweaks | Patch (0.0.X) | Clarified constraint |

---

## Prompt Testing

### Test Framework Structure

```python
# prompt_test.py
class PromptTestSuite:
    def __init__(self, prompt_version: str, model: str):
        self.prompt = load_prompt(prompt_version)
        self.model = model

    def test_accuracy(self, test_cases: list[TestCase]) -> float:
        """Run test cases and measure accuracy."""
        correct = 0
        for case in test_cases:
            response = call_llm(self.prompt, case.input, self.model)
            if self.evaluate(response, case.expected):
                correct += 1
        return correct / len(test_cases)

    def test_consistency(self, input: str, n: int = 10) -> float:
        """Run same input N times, measure consistency."""
        responses = [call_llm(self.prompt, input, self.model) for _ in range(n)]
        unique = len(set(responses))
        return 1 - (unique - 1) / n

    def test_edge_cases(self, edge_cases: list[EdgeCase]) -> list[Result]:
        """Test boundary conditions and adversarial inputs."""
        return [
            Result(
                case=case,
                response=call_llm(self.prompt, case.input, self.model),
                passed=self.evaluate_edge(case)
            )
            for case in edge_cases
        ]
```

### Test Case Categories

| Category | Examples | Priority |
|----------|----------|----------|
| **Happy path** | Normal expected inputs | Must pass |
| **Edge cases** | Empty input, very long input, special characters | Must pass |
| **Adversarial** | Prompt injection attempts, role-breaking | Must pass |
| **Format** | Output matches expected structure | Must pass |
| **Consistency** | Same input produces similar output | Should pass |
| **Regression** | Previously fixed issues don't recur | Must pass |

### Regression Test Template

```json
{
  "test_id": "classify-001",
  "prompt_version": "v1.1.0",
  "input": "I want to cancel my subscription",
  "expected_output": { "intent": "cancellation", "confidence": 0.9 },
  "assertion": "output.intent == 'cancellation'",
  "added_reason": "Bug fix: was classifying as 'billing' in v1.0.0"
}
```

---

## Prompt Optimization

### Token Reduction Techniques

| Technique | Savings | Trade-off |
|-----------|---------|-----------|
| **Remove redundancy** | 10-30% | None if done carefully |
| **Abbreviate instructions** | 15-25% | May reduce clarity |
| **Reduce examples** | 20-50% | May reduce accuracy |
| **Use structured references** | 10-20% | Requires format knowledge |
| **Prompt compression** | 30-60% | Quality degradation risk |

### A/B Testing Framework

```python
class PromptABTest:
    def __init__(self, prompt_a: str, prompt_b: str, model: str):
        self.variants = {"A": prompt_a, "B": prompt_b}
        self.model = model
        self.results = {"A": [], "B": []}

    def run(self, test_cases: list, metrics: list[str]) -> dict:
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

### Optimization Checklist

- [ ] Remove unnecessary context that doesn't improve output
- [ ] Test with fewer examples (start with 0, add until quality meets threshold)
- [ ] Try smaller model with optimized prompt before using larger model
- [ ] Measure cost per query and quality score together
- [ ] Compare temperature settings (0.0 for deterministic, 0.3-0.7 for creative)
- [ ] Test system prompt vs user prompt placement
- [ ] Validate with regression test suite after any change
