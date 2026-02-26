# Business-Tech Translation (absorbed from Bridge)

Methodology for translating between business requirements and technical implementation. Previously a standalone agent (Bridge), now integrated as an Accord capability.

---

## When to Apply

Use this methodology when creating Accord specification packages that involve:
- Business stakeholders with non-technical language
- Technical teams needing business context
- Scope creep risks between requirement phases
- Expectation gaps between teams

---

## Framework: CLARIFY → ALIGN → GUARD → DOCUMENT

| Phase | Purpose | Key Actions |
|-------|---------|-------------|
| **CLARIFY** | 要件の翻訳・明確化 | Business language → technical spec, hidden assumptions surfacing |
| **ALIGN** | 認識の整合 | Gap analysis between stakeholder expectations, trade-off explanation |
| **GUARD** | スコープ管理 | Scope creep detection, change impact assessment |
| **DOCUMENT** | 意思決定記録 | Decision log, trade-off rationale, assumption tracking |

---

## Intent Translation Patterns

| Business Says | Technical Meaning | Accord Action |
|--------------|------------------|---------------|
| "Make it fast" | Performance requirement | Define measurable SLA in L1 |
| "Simple to use" | UX requirement | Define usability criteria in L2-Design |
| "Secure" | Security requirement | Define threat model scope in L2-Dev |
| "Scalable" | Architecture requirement | Define load targets in L2-Dev |
| "Like [competitor]" | Feature parity | Map specific features in L1 |
| "ASAP" | Priority signal | Scope cut proposal, not deadline |
| "Can you just..." | Scope expansion | Flag as potential scope creep |
| "It should be obvious" | Implicit requirement | Make explicit in L1 requirements |

---

## Scope Creep Detection

| Signal | Risk Level | Response |
|--------|-----------|----------|
| "While we're at it..." | HIGH | Flag, defer to next iteration |
| "Can we also add..." | MEDIUM | Assess impact, propose trade-off |
| "It would be nice if..." | LOW | Note as future enhancement |
| Expanding acceptance criteria | HIGH | Compare against original L1 scope |
| New stakeholder enters late | MEDIUM | Re-align expectations, update L0 |

---

## Business-Tech Glossary (Common Terms)

| Business Term | Technical Translation |
|--------------|---------------------|
| ダウンタイム | Service unavailability (SLA target) |
| レスポンス | API response time (p50/p95/p99) |
| セキュリティ | AuthN/AuthZ, encryption, audit logging |
| スケーラビリティ | Horizontal/vertical scaling, load capacity |
| 使いやすさ | WCAG compliance, cognitive load, task completion rate |
| パフォーマンス | Core Web Vitals, TTFB, query latency |
| コスト | Infrastructure + development + maintenance TCO |
| 品質 | Test coverage, defect rate, MTTR |

---

## Anti-Patterns in Cross-Team Communication

| Anti-Pattern | Problem | Prevention |
|-------------|---------|-----------|
| Jargon dumping | Technical terms alienate business | Use glossary translations |
| Silent assumptions | Each team assumes different things | Explicit assumption list in L1 |
| Scope ambiguity | "Phase 1" means different things | Define explicit deliverables |
| Missing "why" | Teams don't understand rationale | Include business context in L2 |
| One-way communication | Specs thrown over the wall | Cross-reference in L2 views |
