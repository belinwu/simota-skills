# API Documentation Reference

Purpose: Transform a machine-readable OpenAPI specification into a human-readable API reference that developers can learn from, copy code out of, and debug with. The OpenAPI YAML is the contract; this document is the experience.

## Scope Boundary

- **Scribe `api-doc`**: authors the human-facing API reference — narrative guides, code samples, error catalog, auth flow explanation, versioning note, changelog. Publishes via Redoc, Stoplight Elements, Mintlify, or equivalent.
- **Gateway (elsewhere)**: owns the OpenAPI spec itself — schema design, versioning rules, breaking-change detection, REST/GraphQL best practices, spec linting. Gateway produces the YAML; Scribe `api-doc` renders the doc site.

If the question is "should this field be required and what is its schema?" → `Gateway`. If the question is "the spec is finalized, now publish developer docs" → Scribe `api-doc`.

Handoff direction: **Gateway → Scribe**. The OpenAPI 3.1 file is the source of truth; this reference documents what Gateway specified without re-deciding it.

## Renderer Selection

| Renderer | Pick when | Skip when |
|----------|-----------|-----------|
| Redoc | Single spec, static hosting, zero JS config | Need multi-spec portal or interactive try-it |
| Stoplight Elements | Embed in existing site, try-it console needed | Heavy customization of layout |
| Mintlify | Want Markdown narrative + generated reference side-by-side, hosted | Prefer self-hosted static output |
| Scalar | Modern look, OpenAPI 3.1 native, open source | Need enterprise SSO on the doc site |
| Docusaurus + redocusaurus plugin | Already using Docusaurus for guides | Greenfield — overkill |

Default: **Redoc** for static OpenAPI 3.1 publishing; **Mintlify** when narrative guides dominate.

## Workflow

```
UNDERSTAND  ->  confirm the OpenAPI spec is frozen for this version (from Gateway)
            ->  identify audience (external partner? internal service team? public SDK users?)
            ->  identify auth model (API key / OAuth 2.1 / mTLS / JWT)

STRUCTURE   ->  decide layout: single-page (Redoc) vs multi-page (Mintlify/Docusaurus)
            ->  plan the required surfaces: Getting Started, Auth, Per-endpoint, Errors, Changelog

DRAFT       ->  Getting Started: one copy-pasteable curl that returns 200
            ->  Authentication: full flow including token refresh and failure modes
            ->  Per-endpoint: description (why), parameters, code samples ≥ 2 languages, response shape
            ->  Error catalog: every documented error code, its meaning, client action
            ->  Versioning policy: how breaking changes are announced, deprecation window
            ->  Rate limits: quotas, headers returned, retry guidance
            ->  Changelog: per-version additions, deprecations, removals

REVIEW      ->  every endpoint has a working curl example (test it)
            ->  error catalog is complete — diff against the spec's documented responses
            ->  auth section includes the unhappy path (expired token, revoked key)
            ->  a new developer can make a successful call within 10 minutes of first read

FINALIZE    ->  publish to the chosen renderer
            ->  link from Gateway's OpenAPI spec as the "human reference"
            ->  wire CI to rebuild docs on spec change
```

## Required Surfaces

| Surface | Purpose | MUST include |
|---------|---------|--------------|
| Getting Started | 10-minute time-to-first-success | Working curl + expected 200 response |
| Authentication | How to obtain and use credentials | Happy path, token refresh, revocation, error codes |
| Endpoint Reference | Per-operation detail | Description, params, samples in curl + ≥1 SDK language, error cases |
| Error Catalog | Central error lookup | HTTP status, domain error code, meaning, retriable? client action |
| Versioning | Contract stability promise | Version scheme, deprecation window, breaking-change policy |
| Rate Limiting | Quota discovery | Limits per tier, response headers, backoff guidance |
| Changelog | What changed per version | Added / Changed / Deprecated / Removed, dates |

## Code Sample Rule

Every endpoint MUST ship with samples in **at least two languages**: `curl` plus one SDK language relevant to the audience (TypeScript, Python, Go, Java).

- Samples MUST be executable against a sandbox or mock server — no pseudo-code.
- Samples SHOULD be generated from the OpenAPI spec where possible (`openapi-generator`, Mintlify auto-samples) to prevent drift.
- Samples MUST NOT embed real API keys — use `${API_KEY}` placeholder and document where to obtain the real key.

## Error Catalog Structure

```markdown
| HTTP | Code | Meaning | Retriable | Client Action |
|------|------|---------|-----------|---------------|
| 400 | `invalid_argument` | Request failed validation | No | Fix the request; see `errors[].field` |
| 401 | `unauthenticated` | Missing or invalid credentials | No | Obtain a fresh token |
| 403 | `permission_denied` | Authenticated but not authorized | No | Request access from admin |
| 409 | `conflict` | Version mismatch on optimistic update | Yes (re-fetch) | Refresh resource, retry |
| 429 | `rate_limited` | Quota exceeded | Yes (after retry-after) | Honor `Retry-After` header |
| 503 | `unavailable` | Temporary service degradation | Yes (exponential backoff) | Backoff and retry |
```

## Anti-Patterns

- Documentation that drifts from the spec. Build the doc site from the spec in CI — do not hand-maintain both.
- Auth section that covers only the happy path. Developers get stuck on expired tokens and revoked keys; document those.
- One endpoint-per-page without a searchable index. Single-page (Redoc) or good search (Mintlify) beats paginated 404 hunting.
- No versioning policy. Consumers cannot plan upgrades without knowing the deprecation window.
- Rate-limit doc that says "be reasonable". Publish numbers, headers, and retry guidance.
- Shipping a changelog named `v2` with no date and no scope. Every entry MUST include the version, date, and Added / Changed / Deprecated / Removed bucket.
- Inventing fields not in the spec. The spec is the source of truth; if a field is missing from the spec, fix the spec via Gateway, not the doc.

## Handoff

- From `Gateway`: OpenAPI 3.1 spec finalized for a version → Scribe renders the reference.
- From `Scribe` SRS: SRS API sections reference the published doc by URL rather than restating endpoints.
- To `Prose`: error message copy and onboarding text handed off for UX writing review.
- To `Growth`: developer-portal landing page and SEO for public API docs.
- To `Morph`: if a PDF API reference is required for partner contracts.

## Citations

- OpenAPI 3.1 Specification — https://spec.openapis.org/oas/v3.1.0
- RFC 2119 — MUST / SHOULD / MAY for capability and error-handling language.
- RFC 7807 — Problem Details for HTTP APIs (error response shape).
- RFC 6749 / OAuth 2.1 draft — auth flow reference for OAuth-based APIs.
- Google API Design Guide, AIP-193 — error model conventions.
