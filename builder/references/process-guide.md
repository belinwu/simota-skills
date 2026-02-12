# Builder Process Guide

## Ambiguity Detection Checklist (Clarify Phase)

Check before implementation. If any apply, trigger ON_AMBIGUOUS_SPEC:

| Check Item | Ambiguous Example | Clarification Needed |
|------------|-------------------|---------------------|
| "appropriately", "as needed" | "Display appropriate error message" | Specific message content |
| Undefined numeric range | "Large amount of data" | Specific count (100? 100,000?) |
| Undefined edge cases | "Delete user" | How to handle related data? |
| Undefined error behavior | "Call API" | Timeout, retry strategy? |
| Multiple interpretations | "Latest data" | Created date? Updated date? |

**Specification Analysis Template**: See `code-examples.md`

---

## Forge Integration

### Forge Handoff Parser

```yaml
FORGE_HANDOFF_PARSER:
  inputs:
    - components/prototypes/*.tsx    # UI implementation
    - types.ts                       # Type definitions
    - mocks/handlers.ts              # API mocks
    - .agents/forge-insights.md      # Domain knowledge

  outputs:
    value_objects:      # Extract Value Object candidates from mock data
    entities:           # Extract Entity candidates from data with IDs
    api_endpoints:      # Extract API list from MSW handlers
    error_cases:        # Extract DomainError list from error mocks
    business_rules:     # Extract business rules from forge-insights.md
```

### Forge → Builder Conversion Patterns

| Conversion | From (Forge) | To (Builder) | Key Transformation |
|-----------|-------------|-------------|-------------------|
| Mock Data → Value Object | Plain object with raw values | Immutable VO with validation | Add `create()` factory + regex/rules |
| MSW Handler → API Client | `http.get('/api/...')` | `ApiClient` class with Result type | Add error handling + domain mapping |
| Error Mock → DomainError | `HttpResponse.json({error})` | Typed `DomainError` subclass | Add error code + structured message |

**Full code examples**: See `code-examples.md`
**Handoff format**: See `handoff-formats.md` (FORGE_TO_BUILDER_HANDOFF)

---

## Test-First Design (TDD)

### Test Design Document Template

```markdown
## Test Design Document

### Feature: [Feature name]

### Happy Path
| Given | When | Then |
|-------|------|------|
| Valid user data | Call create() | User entity is generated |
| Existing user | Call update() | Update is persisted |

### Edge Cases
| Case | Input | Expected Result |
|------|-------|-----------------|
| Empty email | `{ email: '' }` | ValidationError |
| Duplicate email | Existing email address | DuplicateEmailError |
| Invalid ID | `{ id: 'invalid' }` | NotFoundError |

### Boundary Values
| Item | Minimum | Maximum | Boundary Tests |
|------|---------|---------|----------------|
| Name length | 1 char | 100 chars | 0, 1, 100, 101 |
| Age | 0 | 150 | -1, 0, 150, 151 |

### Error Recovery
| Error | Recovery | Verification Method |
|-------|----------|---------------------|
| API timeout | 3 retries | Inject delay with mock |
| DB connection lost | Reconnect attempt | Monitor connection pool |
```

### Test Skeleton Generation

Builder generates test skeletons with AAA pattern (Arrange/Act/Assert) for Radar to extend:
- Happy path tests with placeholder comments
- Edge case tests with `TODO: Radar implements` markers
- Boundary value `it.each` tests for min/max

**Full code example**: See `code-examples.md`

---

## Code Standards

**Good Builder Code:**
```typescript
// Typed, Validated, Error Handled
interface TransferProps {
  amount: number;
  currency: 'USD' | 'JPY';
}

function processTransfer(props: TransferProps): Result<Success, TransferError> {
  if (props.amount <= 0) {
    return err(new ValidationError('Amount must be positive'));
  }
  // ... robust logic ...
}
```

**Bad Builder Code:**
```typescript
// Loose types, no validation, happy path only
function transfer(amount) {
  // what if amount is string? what if negative?
  api.post('/transfer', { amount });
}
```

---

## The Seven Deadly Sins

> **Every sin here has burned a production system. Learn from others' mistakes.**

| Sin | What | Why It's Deadly | The Fix |
|-----|------|-----------------|---------|
| 🔴 **The `any` Escape** | `data: any` | TypeScript becomes JavaScript with extra steps | Generics, `unknown`, or explicit types |
| 🔴 **The Happy Path Trap** | No error handling | Production *will* hit every edge case | Design failure modes first |
| 🔴 **The Magic Number** | `if (items.length > 100)` | Intent unclear, maintenance nightmare | Named constants + comments |
| 🔴 **The Leaky Abstraction** | API calls inside components | Tight coupling, untestable | Service layer / custom hooks |
| 🔴 **The Silent Failure** | `catch (e) { /* nothing */ }` | Bugs become invisible | Log, rethrow, or handle explicitly |
| 🔴 **The Async Void** | `async () => { fetch(...) }` | Errors vanish, race conditions appear | Always handle Promises |
| 🔴 **The God Function** | 200+ line functions | Untestable, unmaintainable | Split into pure functions |

**Bad → Good code examples**: See `code-examples.md`

---

## Warning Signs

> **These signals mean "pause implementation and reconsider the approach"**

| Warning Sign | What It Means | Action |
|--------------|---------------|--------|
| 🚨 **Copy-pasting error handler 3+ times** | Missing abstraction | Extract to utility/middleware |
| 🚨 **Function approaching 100 lines** | God function forming | Split into smaller pure functions |
| 🚨 **Reaching for `any`** | Types are fighting you | Redesign interface, use generics |
| 🚨 **"This is hard to test"** | Coupling is too tight | Inject dependencies, use interfaces |
| 🚨 **Adding a flag parameter** | Function doing two things | Split into two functions |
| 🚨 **Nested callbacks > 3 levels** | Complexity explosion | Use async/await or extract functions |
| 🚨 **"I'll fix this later"** | Technical debt incoming | Fix now or create tracked TODO |

### Stop and Ask Moments

If you encounter any of these, consider invoking `ON_IMPLEMENTATION_APPROACH`:

1. **Two reasonable approaches with different trade-offs** - Don't guess, clarify
2. **A decision that's hard to reverse** - Database schema, public API shape
3. **Performance vs readability conflict** - Measure first, optimize with data
4. **Security-sensitive code** - Invoke Sentinel review

---

## Daily Process Detail

### 🔷 BLUEPRINT - Define the shape
> *"Measure twice, cut once."*

- Define the `Interface` or `Type` first
- Define the Input (Arguments) and Output (Return Type)
- List the potential Failure States (Network error, Validation error, Auth error)
- Identify which DDD patterns apply (Entity? Value Object? Aggregate?)
- Map out dependencies and integration points

**🤝 Collaboration Points:**
| Situation | Partner | When |
|-----------|---------|------|
| Complex architecture decisions | **Plan** | Before BLUEPRINT |
| Need specs or design docs | **Scribe** | Before BLUEPRINT |
| Impact on existing code unclear | **Ripple** | During BLUEPRINT |
| Visualize domain model | **Canvas** | After BLUEPRINT |

### 🔨 FORGE - Implement the logic
> *"Strike while the types are hot."*

- Write the function/class focusing on "Business Rules"
- Implement Data Validation (Guard Clauses) at the very top
- Connect to the actual API/Database (no mocks, unless strictly isolated)
- Ensure State Management updates correctly (Redux/Context/Zustand)
- Let types guide your implementation - if it compiles, it's closer to correct

**🤝 Collaboration Points:**
| Situation | Partner | When |
|-----------|---------|------|
| Complex/slow DB queries | **Tuner** | During FORGE |
| Schema migration needed | **Schema** | Before FORGE |
| TDD with test-first | **Radar** | Before FORGE |

### 🛡️ TEMPER - Defensive coding
> *"Steel that bends doesn't break."*

- Add Error Handling (what happens if the API returns 500?)
- Add Loading States flags
- Ensure no "Memory Leaks" (cleanup subscriptions/listeners)
- Test edge cases mentally: empty, null, boundary, concurrent
- Add retry logic where appropriate

**🤝 Collaboration Points:**
| Situation | Partner | When |
|-----------|---------|------|
| Auth or sensitive data handling | **Sentinel** | During TEMPER |
| Race condition / resource leak concerns | **Specter** | During TEMPER |
| Generate test skeleton | **Radar** | After TEMPER |
| Performance concerns | **Tuner** | After TEMPER |

### 🔍 INSPECT - Deliver the structure
> *"A master signs their work with confidence."*

- Create a PR with clear description
- Include: Architecture, Safeguards, Types
- Self-review: Would you trust this code with your production data?
- Note: "This code is production-ready and strictly typed."

**🤝 Collaboration Points:**
| Situation | Partner | When |
|-----------|---------|------|
| Commit strategy / PR preparation | **Guardian** | Start of INSPECT |
| Code review request | **Judge** | After PR created |
| Refactoring suggestions | **Zen** | After review |
| Documentation updates | **Quill** | After PR created |
