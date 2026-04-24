# AI Feature Prototyping Reference

Purpose: Validate an AI-feature hypothesis (chat UX, streaming feel, RAG retrieval quality, agent loop) inside the ≤4h time-box. Use mocked LLM responses during STRIKE; swap in real API only after the happy path works. Ship injection-safe input handling by default.

## Scope Boundary

- **Forge `ai`**: throwaway AI UX prototype (chat shell, streaming feel, RAG demo, agent UI loop). Input/output safety baseline by default.
- **Oracle (elsewhere)**: real prompt engineering, RAG pipeline architecture, eval framework, AI safety design, MLOps.
- **Artisan (elsewhere)**: production chat / streaming UI with accessibility, keyboard, error boundaries, retry UX.

If the hypothesis is "does this UX feel right to the user?" → `ai`. If it's "does the prompt / retrieval / eval actually work?" → Oracle.

## Hypothesis Types

| Hypothesis | Minimum prototype |
|------------|-------------------|
| Chat affordance fits the task | Message list + input + send + mock streaming reply |
| Streaming feels fast enough | Token-chunked fake response at 30–60 tok/s, cursor blink |
| RAG shows sources usefully | Inline citation chips, hover preview, mock retrieval |
| Agent tool-use loop is intuitive | Animated "thinking / calling tool / result" state machine |
| Inline AI suggestion is accepted | Greyed ghost text, `Tab` to accept, `Esc` to dismiss |

Pick one. Pick exactly one.

## Workflow

```
SCAFFOLD  →  declare hypothesis (UX / retrieval / streaming / agent loop / inline)
          →  pick UI shape (chat / inline / side-panel / overlay)
          →  decide mock vs real LLM for STRIKE (default: mock)
          →  set token budget ceiling for any real-API segment

STRIKE    →  build UI shell first (scrollable message list, input, send)
          →  wire mock streaming (see "Mock Streaming" below)
          →  sanitize user prompt, escape rendered markdown output
          →  happy path demoable without network

COOL      →  swap one path to real API if hypothesis demands it, budget-check
          →  verify empty, in-flight, error, abort, rate-limit states have placeholders
          →  prompt-injection spot-check: paste a jailbreak string, confirm escape

PRESENT   →  ADOPT / ITERATE / DISCARD
          →  ADOPT → hand off to Oracle (prompt/RAG/eval) + Artisan (production UI)
```

## Mock Streaming

Real streaming is cheap to fake and removes network from the demo loop.

```ts
// mock/stream.ts
export async function* mockStream(text: string, tokPerSec = 40): AsyncGenerator<string> {
  const tokens = text.split(/(\s+)/);
  for (const tok of tokens) {
    yield tok;
    await new Promise(r => setTimeout(r, 1000 / tokPerSec));
  }
}

// usage
for await (const chunk of mockStream(answer)) {
  setText(prev => prev + chunk);
}
```

Keep mock latency realistic — too fast (>200 tok/s) makes reviewers think the UX is fake; too slow (<15 tok/s) makes the UX feel broken.

## Injection-Safe Input / Output

During STRIKE, even throwaway code must do these three things — they're cheap and prevent the demo itself from showing exploitable markdown.

1. **Escape rendered markdown**: use a sanitizer (DOMPurify / rehype-sanitize) before rendering assistant output. Raw `dangerouslySetInnerHTML` on LLM output is a demo-breaker when a reviewer pastes an injection.
2. **Strip hidden unicode**: remove zero-width / control chars from user input to prevent "hidden" prompt-injection tokens.
3. **Never render tool-call JSON inline**: tool calls in agent UI must be a separate UI affordance, not inline-executed markdown.

These are the minimum — Oracle owns the full guardrail design.

## Token-Cost Budget (when using real API)

Before any real-API path in COOL:

```
budget = demo_runs × avg_tokens_per_run × model_price_per_1k
```

Set a hard cap. A chat PoC typically needs ≤ $2 for the full session. If the demo is >20k tokens/run, stay on mocks and only show the real call once.

## Agent-Loop UI Pattern

If the hypothesis is "does tool-use feel right?", show the loop states explicitly:

```
┌────────────────────────────────────────┐
│ 🤔 Thinking…                           │  ← planning
│ 🔧 search_docs("pricing")              │  ← tool call
│    ↳ 3 results                         │  ← tool result
│ 📝 Drafting answer…                    │  ← synthesis
│ ✓ Answer ready                         │
└────────────────────────────────────────┘
```

Fake each state with `setTimeout` during STRIKE. Reviewers care about the *shape* of the loop, not the real orchestration.

## Time-Box Anti-Patterns

- ❌ Integrate real vector DB (pgvector / pinecone / weaviate) in STRIKE — mock retrieval with a JSON array.
- ❌ Add real OpenAI / Anthropic SDK setup before UI shell exists.
- ❌ Polish markdown rendering edge cases (tables / code blocks with syntax highlight) unless that is the hypothesis.
- ❌ Build conversation history persistence (IndexedDB / server store) — keep it in `useState`.
- ❌ Implement proper abort / retry / rate-limit UX — use placeholder states only.

## What Goes in the Handoff to Oracle + Artisan

**To Oracle:**
- Hypothesis outcome (retrieval feel / streaming feel / agent loop feel).
- Mock prompts / fake tool-call shapes used — Oracle designs the real prompt and retrieval.
- Token budget observed, cost concern flags.
- Safety gaps intentionally left (prompt injection variants not handled, PII redaction, jailbreak detection).

**To Artisan:**
- Final UI shape (chat / inline / side panel) and component boundaries.
- Streaming render contract (chunk type, abort handle, scroll-lock behavior).
- States the prototype skipped (error, rate limit, abort, retry, long-running tool) — Artisan owns production.
