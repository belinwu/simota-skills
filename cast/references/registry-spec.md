# Cast Registry Specification

Full specification for `.agents/personas/registry.yaml` — the single source of truth for persona inventory.

---

## Overview

The registry tracks all Cast-managed personas across services, providing a centralized index for discovery, status tracking, and lifecycle management.

```
.agents/personas/
├── registry.yaml              # THIS FILE — persona index
├── ec-platform/
│   ├── first-time-buyer.md
│   ├── power-shopper.md
│   └── mobile-browser.md
├── admin-dashboard/
│   └── it-admin.md
└── _archive/
    └── ec-platform/
        └── old-persona.md
```

---

## Schema

```yaml
# registry.yaml
# Cast Persona Registry — Single source of truth for all managed personas
# Do not edit manually unless Cast is unavailable

schema_version: "1.0"
updated: "YYYY-MM-DD"              # Last registry modification date

services:
  {service-name}:                   # Kebab-case service identifier
    description: "Service description"
    personas:
      - file: "{service-name}/{persona-name}.md"
        name: "Display Name"
        status: active              # draft | active | evolved | archived
        version: "1.0"
        confidence: 0.65
        category: user              # user | developer | designer | business | operations
        type: custom                # custom | base | internal
        echo_base_mapping: Newbie
        tags: [b2c, e-commerce]
        created: "YYYY-MM-DD"
        last_updated: "YYYY-MM-DD"
        evolution_count: 0
        priority: P0                # P0 | P1 | P2 | P3+

    coverage:
      segments_identified: 3        # Known user segments
      segments_covered: 3           # Segments with personas
      gaps: []                      # Identified but uncovered segments
      last_audit: "YYYY-MM-DD"      # Last audit date

    metadata:
      primary_platform: mobile      # mobile | desktop | both
      service_type: b2c             # b2b | b2c | both
      created: "YYYY-MM-DD"        # When this service was first registered
```

---

## Field Definitions

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | string | Yes | Registry schema version (currently "1.0") |
| `updated` | date | Yes | Last modification date of registry |
| `services` | map | Yes | Map of service names to service entries |

### Service Entry Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | string | Optional | Human-readable service description |
| `personas` | array | Yes | List of persona entries |
| `coverage` | object | Optional | Segment coverage tracking |
| `metadata` | object | Optional | Service-level metadata |

### Persona Entry Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | string | Yes | Relative path from `.agents/personas/` |
| `name` | string | Yes | Display name of persona |
| `status` | enum | Yes | `draft` / `active` / `evolved` / `archived` |
| `version` | string | Yes | Current semantic version |
| `confidence` | float | Yes | Current confidence score (0.0–1.0) |
| `category` | enum | Yes | `user` / `developer` / `designer` / `business` / `operations` |
| `type` | enum | Yes | `custom` / `base` / `internal` |
| `echo_base_mapping` | string | Recommended | Echo base persona name |
| `tags` | string[] | Optional | Classification tags |
| `created` | date | Yes | Initial creation date |
| `last_updated` | date | Yes | Last evolution/modification date |
| `evolution_count` | integer | Yes | Number of evolutions applied |
| `priority` | enum | Optional | `P0` / `P1` / `P2` / `P3+` |

### Coverage Fields

| Field | Type | Description |
|-------|------|-------------|
| `segments_identified` | integer | Total known user segments |
| `segments_covered` | integer | Segments with active personas |
| `gaps` | string[] | Named segments without personas |
| `last_audit` | date | Date of last AUDIT mode run |

---

## Lifecycle States

```
                    ┌──────────┐
         create───→│  draft    │
                    └────┬─────┘
                         │ validate
                         ↓
                    ┌──────────┐     evolve     ┌──────────┐
                    │  active   │──────────────→│  evolved  │
                    └────┬─────┘               └────┬─────┘
                         │                          │ settle
                         │                          ↓
                         │                    ┌──────────┐
                         │                    │  active   │
                         │                    └──────────┘
                         │
                         │ archive
                         ↓
                    ┌──────────┐
                    │ archived  │
                    └──────────┘
```

| State | Description | Allowed Operations |
|-------|-------------|-------------------|
| `draft` | Created but not validated | Edit, Validate → active, Delete |
| `active` | Validated and in use | Evolve, Distribute, Audit, Archive |
| `evolved` | Transient state during evolution | Settle → active |
| `archived` | Preserved but not active | Restore → active, Delete |

---

## Operations

### Create Service

```yaml
# Adding a new service to registry
services:
  new-service:
    description: "New service description"
    personas: []
    coverage:
      segments_identified: 0
      segments_covered: 0
      gaps: []
    metadata:
      primary_platform: both
      service_type: b2c
      created: "2026-02-16"
```

### Register Persona

Add persona entry to service's personas array:

```yaml
- file: "new-service/primary-user.md"
  name: "Primary User"
  status: draft
  version: "1.0"
  confidence: 0.65
  category: user
  type: custom
  echo_base_mapping: Newbie
  tags: [b2c]
  created: "2026-02-16"
  last_updated: "2026-02-16"
  evolution_count: 0
  priority: P0
```

### Update on Evolution

When a persona evolves, update:
- `version` — bump minor
- `confidence` — recalculated
- `last_updated` — current date
- `evolution_count` — increment
- `status` — set to `active` (after transient `evolved`)

### Archive Persona

When archiving:
1. Move file to `_archive/{service-name}/`
2. Set `status: archived` in registry
3. Update `file` path to `_archive/` location
4. Update `coverage.segments_covered` count
5. Add archived segment to `coverage.gaps` if not replaced

### Remove Service

When a service is removed:
1. Archive all personas
2. Remove service entry from registry
3. Optionally delete service directory

---

## Registry Operations Summary

| Operation | Registry Change | File System Change |
|-----------|----------------|-------------------|
| **CONJURE** | Add persona entries | Create persona .md files |
| **FUSE** | Update persona fields (confidence, version) | Update persona .md content |
| **EVOLVE** | Update persona fields (version, confidence, evolution_count) | Update persona .md content + evolution log |
| **AUDIT** | Update coverage, flag issues | No file changes |
| **DISTRIBUTE** | No changes | Generate handoff files (temporary) |
| **SPEAK** | No changes (Auto-Derive is transient) | Generate audio files + transcript |
| **Archive** | Update status, move file path | Move file to `_archive/` |

---

## Validation Rules

The registry must satisfy these invariants:

| Rule | Description |
|------|-------------|
| **File exists** | Every `file` path must point to an existing persona file |
| **Unique files** | No duplicate `file` paths within a service |
| **Unique names** | No duplicate `name` within a service |
| **Status valid** | Status must be one of: draft, active, evolved, archived |
| **Confidence range** | Confidence must be 0.0–1.0 |
| **Version format** | Version must match `"X.Y"` pattern |
| **Date format** | All dates must be ISO 8601 (YYYY-MM-DD) |
| **Coverage consistent** | `segments_covered` ≤ `segments_identified` |
| **Active has mapping** | Active personas should have `echo_base_mapping` |

---

## Example Registry

```yaml
schema_version: "1.0"
updated: "2026-02-16"

services:
  ec-platform:
    description: "E-commerce platform for consumer shopping"
    personas:
      - file: "ec-platform/first-time-buyer.md"
        name: "First-Time Buyer"
        status: active
        version: "1.2"
        confidence: 0.82
        category: user
        type: custom
        echo_base_mapping: Newbie
        tags: [b2c, e-commerce, mobile-first]
        created: "2026-02-01"
        last_updated: "2026-02-15"
        evolution_count: 2
        priority: P0

      - file: "ec-platform/power-shopper.md"
        name: "Power Shopper"
        status: active
        version: "1.0"
        confidence: 0.60
        category: user
        type: custom
        echo_base_mapping: Power User
        tags: [b2c, e-commerce, desktop]
        created: "2026-02-01"
        last_updated: "2026-02-01"
        evolution_count: 0
        priority: P1

      - file: "ec-platform/accessibility-shopper.md"
        name: "Accessibility Shopper"
        status: active
        version: "1.0"
        confidence: 0.55
        category: user
        type: custom
        echo_base_mapping: Accessibility User
        tags: [b2c, e-commerce, a11y]
        created: "2026-02-01"
        last_updated: "2026-02-01"
        evolution_count: 0
        priority: P2

    coverage:
      segments_identified: 4
      segments_covered: 3
      gaps: ["enterprise-buyer"]
      last_audit: "2026-02-16"

    metadata:
      primary_platform: mobile
      service_type: b2c
      created: "2026-02-01"
```
