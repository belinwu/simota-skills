# Handoff Formats Reference

Bard の全 Inbound / Outbound ハンドオフ定義。

---

## Overview

```
┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐
│  Harvest  │  │  Launch   │  │  Rewind   │  │ Guardian  │
└─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
      │              │              │              │
      │ SPRINT_DATA  │ RELEASE      │ ARCHAEOLOGY  │ QUALITY
      │              │              │              │
      └──────────────┴──────┬───────┴──────────────┘
                            ▼
                   ┌─────────────────┐
                   │      Bard       │
                   └────────┬────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
         ▼                  ▼                  ▼
   ┌───────────┐     ┌───────────┐     ┌───────────┐
   │   Quill   │     │  Canvas   │     │   Morph   │
   └───────────┘     └───────────┘     └───────────┘
```

---

## Inbound Handoffs

### HARVEST_TO_BARD

Harvestが収集したPR統計データからの投稿生成依頼。

```yaml
HARVEST_TO_BARD:
  type: "sprint_data" | "release_data" | "individual_data"
  timestamp: "2024-01-19T18:00:00Z"
  repository: "org/project"

  period:
    start: "2024-01-08"
    end: "2024-01-19"

  statistics:
    total_prs: 12
    merged: 10
    open: 2
    additions: 3500
    deletions: 1200
    categories:
      feat: 5
      fix: 3
      refactor: 2
    top_contributors:
      - name: "Alice"
        prs: 4
      - name: "Bob"
        prs: 3

  highlights:
    - "New authentication system (PR #150)"
    - "Performance improvement: 2x faster API (PR #148)"

  request:
    persona: "auto" | "codex" | "gemini" | "claude"  # Persona selection (auto = weighted)
    format: "auto" | "one_liner" | "short_monologue" | "slack_rant" | "retro_roast" | "philosophical_musing" | "mixed_monologue"
    purpose: "sprint_retro" | "team_celebration" | "report_decoration"
    # Legacy fallback: 'form' and 'language' fields are accepted but mapped to persona/format
```

---

### LAUNCH_TO_BARD

リリースイベントの詩的祝福依頼。

```yaml
LAUNCH_TO_BARD:
  type: "release_event"
  timestamp: "2024-03-15T10:00:00Z"
  repository: "org/project"

  release:
    version: "v2.0.0"
    previous_version: "v1.9.0"
    type: "major" | "minor" | "patch"
    date: "2024-03-15"

  content:
    highlights:
      - "New authentication system"
      - "Performance improvements (2x faster)"
      - "Dark mode support"
    breaking_changes: 1
    total_prs: 45
    contributors_count: 8
    lines_changed: 12000

  request:
    persona: "auto" | "codex" | "gemini" | "claude"
    format: "auto" | "slack_rant" | "mixed_monologue" | "short_monologue"
    tone: "celebratory" | "reflective" | "terrified"
    # Legacy fallback: 'form' and 'language' fields are accepted but mapped to persona/format
```

---

### REWIND_TO_BARD

コード考古学の結果を物語化する依頼。

```yaml
REWIND_TO_BARD:
  type: "archaeology_narrative"
  timestamp: "2024-02-01T14:00:00Z"
  repository: "org/project"

  findings:
    subject: "Authentication module evolution"
    timeline:
      - date: "2022-10-01"
        event: "Initial auth implementation"
        commit: "abc1234"
        author: "Charlie"
      - date: "2023-03-15"
        event: "OAuth2 integration"
        commit: "def5678"
        author: "Alice"
      - date: "2024-01-10"
        event: "Major security refactor"
        commit: "ghi9012"
        author: "Bob"
    key_decisions:
      - "JWT over session-based auth (2022-10)"
      - "OAuth2 for third-party login (2023-03)"
    contributors: ["Charlie", "Alice", "Bob", "Dave"]

  request:
    persona: "auto" | "codex" | "gemini" | "claude"
    format: "auto" | "mixed_monologue" | "philosophical_musing" | "slack_rant"
    purpose: "onboarding" | "project_history" | "celebration"
    # Legacy fallback: 'form' and 'language' fields are accepted but mapped to persona/format
```

---

### GUARDIAN_TO_BARD

変更分析データから開発者を称える詩の依頼。

```yaml
GUARDIAN_TO_BARD:
  type: "quality_praise"
  timestamp: "2024-01-19T17:00:00Z"
  repository: "org/project"

  analysis:
    pr_number: 150
    title: "feat(auth): add OAuth2 support"
    author: "Alice"
    quality_score: 95
    highlights:
      - "Atomic commits (5 well-structured commits)"
      - "Comprehensive test coverage"
      - "Clear PR description"
    stats:
      additions: 450
      deletions: 120
      files_changed: 12

  request:
    persona: "auto" | "codex" | "gemini" | "claude"
    format: "auto" | "retro_roast" | "philosophical_musing" | "short_monologue"
    purpose: "praise" | "roast" | "celebration"
    # Legacy fallback: 'form' and 'language' fields are accepted but mapped to persona/format
```

---

## Outbound Handoffs

### BARD_TO_QUILL

投稿をドキュメントに組み込む依頼。

```yaml
BARD_TO_QUILL:
  type: "post_for_docs"
  timestamp: "2024-01-19T19:00:00Z"
  repository: "org/project"

  post:
    title: "Sprint 42 所感"
    persona: "codex"
    format: "short_monologue"
    content: |
      feat 5件。テスト追加 0件。
      ...まあいいけど。
    source_period: "2024-01-08 ~ 2024-01-19"
    source_stats: "12 PRs merged (feat:5, fix:3, refactor:2)"
  # Legacy fallback: 'poem' field is accepted and mapped to 'post'

  integration:
    target_file: "README.md"
    target_section: "Team Culture" | "Sprint History" | "Release Notes"
    format: "blockquote" | "collapsible" | "inline"
    position: "append" | "prepend" | "replace"
```

---

### BARD_TO_CANVAS

投稿を視覚化する依頼。

```yaml
BARD_TO_CANVAS:
  type: "visual_post"
  timestamp: "2024-01-19T19:00:00Z"
  repository: "org/project"

  post:
    title: "Sprint 42: The Reckoning"
    persona: "gemini"
    format: "retro_roast"
    content: |
      [Full post content]
  # Legacy fallback: 'poem' field is accepted and mapped to 'post'

  visualization_request:
    type: "timeline_with_quotes" | "ascii_art_frame" | "mermaid_journey"
    data_points:
      - date: "2024-01-08"
        event: "Sprint start"
        quote_excerpt: "12 PRs merged. Let's TALK about it."
      - date: "2024-01-19"
        event: "Sprint end"
        quote_excerpt: "Ship it and pray 🚢🙏"
    style: "dramatic" | "minimal" | "dev-culture"
```

---

### BARD_TO_MORPH

投稿のフォーマット変換依頼。

```yaml
BARD_TO_MORPH:
  type: "post_format_conversion"
  timestamp: "2024-01-19T19:00:00Z"

  source:
    format: "markdown"
    content: |
      ## Sprint 42 所感
      [Full post in Markdown]

  target:
    format: "pdf" | "html" | "docx"
    styling:
      font: "monospace" | "serif" | "sans-serif"
      alignment: "left"
      margins: "normal"
    metadata:
      title: "Sprint 42 所感"
      author: "Bard (Codex)"
      persona: "codex"
      date: "2024-01-19"
```
