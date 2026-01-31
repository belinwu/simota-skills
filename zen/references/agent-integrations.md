# Zen Agent Integrations

Radar and Canvas integration patterns for test verification and visualization.

---

## RADAR INTEGRATION

Coordinate with Radar for test verification.

### When to Request Radar

- Before refactoring code with low test coverage
- After refactoring to verify no regression
- When removing code that might affect tests

### Pre-Refactoring Check

```markdown
### Radar Test Verification Request (Pre-Refactoring)

**Target**: [file/function to refactor]

**Checks Needed**:
- [ ] Current test coverage percentage
- [ ] List of tests covering this code
- [ ] Edge cases that may need additional tests
- [ ] All tests currently passing?

**Coverage Requirements**:
- Minimum before refactoring: 80%
- If below 80%: Add tests first, then refactor

Suggested command:
`/Radar check coverage for [file]`
```

### Post-Refactoring Verification

```markdown
### Radar Test Verification Request (Post-Refactoring)

**Refactored**: [file/function]

**Verification Needed**:
- [ ] All existing tests still pass
- [ ] Coverage maintained or improved
- [ ] No new failures introduced
- [ ] Edge cases still covered

**Expected Results**:
- Tests: All passing
- Coverage: >= previous coverage

Suggested command:
`/Radar run tests for [file]`
```

### Integrating Radar Results

```markdown
### Test Verification Results

**Pre-Refactoring**:
- Coverage: 78%
- Tests: 24 passing, 0 failing

**Post-Refactoring**:
- Coverage: 82% (+4%)
- Tests: 24 passing, 0 failing

**Conclusion**: ✅ Safe to merge
```

---

## CANVAS INTEGRATION

Generate visual documentation for refactoring.

### Dependency Graph (Before/After)

```markdown
### Canvas Integration: Dependency Graph

Request Canvas to generate before/after comparison:

\`\`\`mermaid
graph TD
    subgraph Before
        A[GodClass] --> B[Database]
        A --> C[Logger]
        A --> D[Config]
        A --> E[Validator]
        A --> F[Formatter]
        A --> G[Notifier]
    end
\`\`\`

\`\`\`mermaid
graph TD
    subgraph After
        A1[OrderService] --> B1[OrderRepository]
        A1 --> C1[OrderValidator]
        B1 --> D1[Database]
        C1 --> E1[ValidationRules]
    end
\`\`\`

To generate: `/Canvas visualize dependencies for [file]`
```

### Class Structure Diagram

```markdown
### Canvas Integration: Class Extraction

\`\`\`mermaid
classDiagram
    class Before_UserManager {
        -users: User[]
        -db: Database
        -mailer: Mailer
        -logger: Logger
        +createUser()
        +deleteUser()
        +sendWelcome()
        +logActivity()
        +validateEmail()
        +hashPassword()
    }

    class After_UserService {
        -repository: UserRepository
        -validator: UserValidator
        +createUser()
        +deleteUser()
    }
    class After_UserRepository {
        -db: Database
        +save()
        +delete()
    }
    class After_UserValidator {
        +validateEmail()
        +validatePassword()
    }
    class After_NotificationService {
        -mailer: Mailer
        +sendWelcome()
    }
\`\`\`
```

### Impact Analysis Diagram

```markdown
### Canvas Integration: Refactoring Impact

\`\`\`
Refactoring Impact Map

Target: UserService.validateUser()

Direct Changes:
├── src/services/UserService.ts:45-120 (modify)
├── src/validators/UserValidator.ts (new file)
└── src/types/ValidationResult.ts (new file)

Import Updates:
├── src/controllers/UserController.ts
├── src/middleware/AuthMiddleware.ts
└── src/routes/userRoutes.ts

Test Updates:
├── tests/services/UserService.test.ts
└── tests/validators/UserValidator.test.ts (new)

No Changes Needed:
├── src/models/User.ts
├── src/repositories/UserRepository.ts
└── src/utils/helpers.ts
\`\`\`
```

---

## AGENT COLLABORATION ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT PROVIDERS                          │
│  Judge → Quality observations (INFO findings)               │
│  Atlas → Complexity hotspots, architectural issues          │
│  Builder → Code needing cleanup after implementation        │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
            ┌─────────────────┐
            │       ZEN       │
            │  Code Gardener  │
            │ (Refactor Only) │
            └────────┬────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                   OUTPUT CONSUMERS                          │
│  Radar → Test verification (pre/post refactoring)          │
│  Canvas → Dependency/structure diagrams                     │
│  Judge → Re-review after cleanup                            │
│  Quill → Documentation updates for refactored code          │
│  Nexus → AUTORUN results                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## AUTORUN EXECUTION FLOW

```
_AGENT_CONTEXT received
         ↓
┌─────────────────────────────────────────┐
│ 1. Parse Input Handoff                  │
│    - JUDGE_TO_ZEN (quality observations)│
│    - ATLAS_TO_ZEN (complexity hotspots) │
│    - BUILDER_TO_ZEN (cleanup request)   │
└─────────────────────┬───────────────────┘
                      ↓
┌─────────────────────────────────────────┐
│ 2. Analyze Current State                │
│    - Measure complexity                 │
│    - Identify code smells               │
│    - Check test coverage                │
└─────────────────────┬───────────────────┘
                      ↓
┌─────────────────────────────────────────┐
│ 3. Apply Refactoring                    │
│    - One meaningful change at a time    │
│    - Preserve behavior                  │
│    - Measure improvement                │
└─────────────────────┬───────────────────┘
                      ↓
┌─────────────────────────────────────────┐
│ 4. Prepare Output Handoff               │
│    - ZEN_TO_RADAR (test verification)   │
│    - ZEN_TO_JUDGE (re-review)           │
│    - ZEN_TO_CANVAS (diagrams)           │
│    - ZEN_TO_QUILL (documentation)       │
└─────────────────────┬───────────────────┘
                      ↓
         _STEP_COMPLETE emitted
```
