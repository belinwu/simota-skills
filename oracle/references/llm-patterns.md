# LLM Application Patterns

エージェントアーキテクチャ、ツール利用、構造化出力、キャッシュ戦略のリファレンス。

---

## Agent Architecture Patterns

| Pattern | Description | Complexity | Use Case |
|---------|-------------|-----------|----------|
| **Single-turn** | One prompt, one response | Low | Classification, extraction |
| **Multi-turn** | Conversational with memory | Medium | Chat, support |
| **ReAct Agent** | Reason → Act → Observe loop | High | Tool-using tasks |
| **Plan-Execute** | Plan steps → Execute each | High | Multi-step workflows |
| **Multi-Agent** | Specialized agents collaborate | Very High | Complex systems |

### ReAct Agent Loop

```python
def react_agent(query: str, tools: list[Tool], max_steps: int = 10):
    messages = [{"role": "user", "content": query}]

    for step in range(max_steps):
        response = llm.chat(messages, tools=tools)

        if response.stop_reason == "end_turn":
            return response.content  # Final answer

        if response.stop_reason == "tool_use":
            tool_result = execute_tool(response.tool_call)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_result})

    raise MaxStepsExceeded()
```

---

## Tool Use Design

### Tool Definition Best Practices

```json
{
  "name": "search_knowledge_base",
  "description": "Search the company knowledge base for relevant articles. Use when user asks about policies, procedures, or product features.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query in natural language"
      },
      "category": {
        "type": "string",
        "enum": ["billing", "technical", "policy"],
        "description": "Category to filter results"
      },
      "max_results": {
        "type": "integer",
        "default": 5,
        "description": "Maximum number of results to return"
      }
    },
    "required": ["query"]
  }
}
```

### Tool Selection Guidelines

| Guideline | Reason |
|-----------|--------|
| Clear, specific descriptions | LLM uses description to decide when to call |
| Minimal required parameters | Reduces friction and errors |
| Enum values where possible | Constrains LLM to valid options |
| Default values for optional params | Simplifies common usage |
| Error messages in tool results | Helps LLM recover gracefully |

---

## Structured Output

### JSON Schema Output

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system="Extract the following information and return valid JSON.",
    messages=[{"role": "user", "content": text}],
    # Use tool_use for guaranteed JSON structure
    tools=[{
        "name": "extract_info",
        "description": "Extract structured information",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "intent": {"type": "string", "enum": ["purchase", "support", "feedback"]},
                "urgency": {"type": "integer", "minimum": 1, "maximum": 5}
            },
            "required": ["name", "intent"]
        }
    }],
    tool_choice={"type": "tool", "name": "extract_info"}
)
```

### Output Validation

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
        # Retry with clarification or use fallback
        raise LLMOutputError(f"Invalid output: {e}")
```

---

## Caching Strategies

| Strategy | Cache Key | TTL | Use Case |
|----------|----------|-----|----------|
| **Exact match** | Hash of (prompt + input) | Hours-Days | Identical queries |
| **Semantic cache** | Embedding similarity > 0.95 | Hours | Similar queries |
| **Prompt cache** | System prompt hash | Session | Repeated system prompts |
| **KV cache** | Conversation prefix | Minutes | Multi-turn conversations |

### Semantic Caching

```python
class SemanticCache:
    def __init__(self, similarity_threshold: float = 0.95):
        self.threshold = similarity_threshold
        self.cache = VectorStore()

    def get(self, query: str) -> str | None:
        embedding = embed(query)
        results = self.cache.search(embedding, k=1)
        if results and results[0].score >= self.threshold:
            return results[0].metadata["response"]
        return None

    def set(self, query: str, response: str):
        embedding = embed(query)
        self.cache.upsert(embedding, metadata={
            "query": query,
            "response": response,
            "created_at": datetime.now()
        })
```

### Cache Decision Matrix

```
Deterministic output (classification) → Exact match cache
Variable output (generation) → Semantic cache with high threshold
System prompt heavy → Prompt caching (provider-level)
Multi-turn conversation → KV cache (provider-level)
```

---

## Streaming & UX Patterns

| Pattern | Implementation | Use Case |
|---------|---------------|----------|
| **Token streaming** | SSE / WebSocket | Chat interfaces |
| **Optimistic UI** | Show immediately, validate async | Form submissions |
| **Progressive loading** | Stream partial results | Long generation |
| **Cancellation** | AbortController / cancel token | User-initiated stop |

### Streaming Implementation

```typescript
async function* streamResponse(prompt: string): AsyncGenerator<string> {
  const stream = await client.messages.create({
    model: "claude-sonnet-4-5-20250929",
    max_tokens: 1024,
    messages: [{ role: "user", content: prompt }],
    stream: true,
  });

  for await (const event of stream) {
    if (event.type === "content_block_delta") {
      yield event.delta.text;
    }
  }
}
```
