# Mind Map Design for NotebookLM

Reference for Prism's `mindmap` recipe. Branch hierarchy steering, terminology consistency across nodes, density-vs-depth trade-off, and downstream Slides / Infographic handoff.

---

## 1. Mind Map's Place in the Format Catalog

Mind Map vs other formats:

| Format | Strength | Weakness |
|---|---|---|
| Mind Map | Visual hierarchy at-a-glance, exploration entry-point | No narrative arc, no embed-quality export |
| Infographic | Polished single-image, shareable | Fixed layout, less hierarchy |
| Slides | Linear narrative, presenter-friendly | Loses parallel comparison |
| Deep Research | Citation-rich text | No visual structure |

**Use Mind Map when**: stakeholder needs to scan structure, decide where to drill in, or kick off a session with a shared map.
**Don't use Mind Map when**: deliverable is a deck or a report — convert via downstream handoff.

---

## 2. Top-Level Branch Count

Branch count is the single biggest readability lever.

| Top-level branches | When to use | Cognitive load |
|---|---|---|
| 3 | Executive overview, decision frame, simple framework | Low (Miller's 7±2 well within capacity) |
| 5 | Standard balanced map; default | Medium |
| 7 | Comprehensive coverage, classification taxonomy | High; consider splitting |
| 9+ | Almost always wrong | Reader cannot hold simultaneously |

Steering prompt template:
```
Generate a Mind Map with exactly 5 top-level branches.
Each branch must capture one of: <branch1>, <branch2>, ..., <branch5>.
Do not create additional top-level branches.
```

If NotebookLM produces >7 top-level branches unprompted, the map will read as a flat tag cloud. Always pin the count.

---

## 3. Depth Limits

| Depth | Use | Risk |
|---|---|---|
| 2 (root → branch → leaf) | Quick visual reference | Loses sub-structure |
| 3 (recommended) | Default for most maps | Sweet spot |
| 4 | Deep taxonomy, technical reference | Reader scrolls, loses context |
| 5+ | Almost never | Becomes unreadable; convert to nested list |

Pin depth:
```
Limit branch depth to 3 levels (top branch → sub-branch → leaf).
Do not nest beyond leaf level. If a leaf needs further breakdown,
elevate it to a sub-branch.
```

---

## 4. Terminology Consistency

Inconsistent node naming shatters readability. Pin a parts-of-speech rule.

### Verb-led nodes (action-oriented)
```
All node labels must start with an imperative verb.
Examples: "Capture metrics", "Validate input", "Deploy artifact".
Reject: "Metrics", "Input validation", "The deploy step".
```

### Noun-led nodes (entity-oriented)
```
All node labels must be noun phrases (no verbs, no articles).
Examples: "User authentication", "Payment service", "Audit log".
Reject: "Authenticate users", "The payment service", "Logging audits".
```

### Mixed (acceptable for top vs sub-branch)
```
Top-level branches: noun phrases (domain areas).
Sub-branches and leaves: imperative verbs (actions within domain).
```

Whichever you choose, **pin it explicitly**. NotebookLM defaults to mixing styles.

---

## 5. Density vs Depth Trade-Off

| Audience | Density (leaves per branch) | Depth | Total nodes |
|---|---|---|---|
| Executive overview | 2-3 | 2 | ~15 |
| Team alignment | 3-5 | 3 | ~40 |
| Reference taxonomy | 5-7 | 3 | ~80 |
| Comprehensive map | 7+ | 4 | 150+ (often unreadable) |

Pin total node count to enforce the choice:
```
Generate approximately 40 total nodes (5 branches × ~3 sub-branches × ~2 leaves).
Do not exceed 60 nodes. If material is too vast, prefer fewer top branches with
more leaves over more top branches with sparse leaves.
```

---

## 6. Audience-Specific Templates

### Executive overview (3 branches × 2 deep, ~15 nodes)
```
Generate a Mind Map summarizing the report for an executive audience.

Constraints:
- Exactly 3 top-level branches: "Risks", "Opportunities", "Recommendations"
- Each branch: 2-3 sub-branches max
- Depth: 2 levels (top → sub only, no leaves)
- All node labels: noun phrases, ≤ 5 words
- Total nodes: ~15

Goal: stakeholder reviews in 30 seconds and decides where to drill in.
```

### Team alignment (5 branches × 3 deep, ~40 nodes)
```
Generate a Mind Map for engineering team kickoff.

Constraints:
- Exactly 5 top-level branches matching the project phases
- Each branch: 3-5 sub-branches
- Depth: 3 levels
- Sub-branches and leaves: imperative verb-led
- Total nodes: ~40

Goal: shared mental model; each team member can locate their work area.
```

### Reference taxonomy (7 branches × 3 deep, ~80 nodes)
```
Generate a Mind Map as reference taxonomy of the API surface.

Constraints:
- Exactly 7 top-level branches grouped by API resource
- Each branch: 5-7 endpoints as sub-branches
- Each endpoint: 2-3 leaves for HTTP methods / payload shape / auth
- All labels: noun phrases (API names verbatim from source)
- Total nodes: ~80

Goal: developer can locate any endpoint within 10 seconds.
```

---

## 7. Downstream Handoff Patterns

Mind Map is often a **starting point**, not an endpoint. Plan the next format:

| Next deliverable | Handoff |
|---|---|
| Presentation | Convert each top-level branch → 1 slide via Slides format |
| Polished single-image | Re-prompt as Infographic (Bento Grid style maps best to Mind Map structure) |
| Detailed document | Convert via Reports; use Mind Map structure as TOC |
| Visual diagram | Hand off to Canvas (Mermaid mindmap or hierarchy diagram) |
| Brainstorm extension | Iterate via chat-to-output: ask "expand the X branch" → re-generate |

Steering prompt for Mind Map → Slides handoff:
```
Generate Presenter Slides where:
- Slide 1: title + the 5 top-level branches as agenda
- Slides 2-6: one per top-level branch, with the sub-branches as bullets
- Slide 7: synthesis / call to action
```

---

## 8. Iterative Refinement via Chat

NotebookLM Mind Maps support chat refinement:
```
"Expand the 'Risks' branch into 5 sub-branches with mitigation actions."
"Collapse the 'Opportunities' branch to top-level only."
"Re-label all leaves under 'Recommendations' to start with imperative verbs."
"Add a 6th top-level branch: 'Open Questions'."
```

After 2-3 refinement rounds, convert the chat output to a fresh Mind Map (chat-to-output).

---

## 9. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| 12+ top-level branches → flat tag cloud | Pin top-level count to 3 / 5 / 7 |
| Inconsistent node grammar (verb / noun mix) | Pin parts-of-speech rule explicitly |
| Depth 5+ → unreadable | Cap at 3 levels; elevate or split if needed |
| Sparse branches (1 leaf each) | Either deepen or merge into siblings |
| Top-level branch is a single word ("Tools", "Process") | Use 2-4 word descriptors with concrete domain anchor |
| Mind Map used where a Slide deck was needed | Plan downstream handoff from the start |
| Mind Map has no center / focus question | First node = the question; all branches answer it |
| Re-generating loses good branches each iteration | Use chat refinement, not full re-generation |
| CJK / RTL labels truncated in viewer | Test with target script; shorten labels if needed |
| Mind Map as "final deliverable" without polish | Hand off to Infographic / Slides / Canvas |

---

## 10. Decision Walkthrough Template

```
Audience: ____________
Use case: □ executive overview  □ team alignment  □ reference taxonomy  □ brainstorm starter

Center / focus question: ____________

Top-level branches:
  Count: 3 / 5 / 7
  Names: ____, ____, ____, ____, ____

Depth: 2 / 3 / 4
Density per branch: 2-3 / 3-5 / 5-7 leaves
Target total nodes: ____

Naming convention:
  □ All verb-led
  □ All noun-led
  □ Top: noun, sub/leaf: verb

Steering prompt (≤150 words):
  ____________________________________

Iteration plan (chat-to-output):
  Round 1: initial generation
  Round 2: ____ (e.g., "expand X branch")
  Round 3: ____ (e.g., "rebalance density")
  Stop when: structure stable across 2 rounds

Downstream handoff:
  □ Slides (1 slide per top-level branch)
  □ Infographic (Bento Grid)
  □ Reports (TOC from structure)
  □ Canvas (Mermaid mindmap)
  □ None — Mind Map is final

Verification:
  □ Top-level count matches plan
  □ Depth ≤ planned cap
  □ Node naming consistent
  □ Total nodes within target ±20%
  □ Center question / focus visible
  □ Renders correctly in target script (JA/CJK/RTL if applicable)
```

---

## 11. References
- NotebookLM Mind Map documentation
- Tony Buzan, Mind Mapping principles
- Miller's 7±2 (cognitive load on parallel items)
- Mermaid mindmap syntax (for Canvas handoff)
