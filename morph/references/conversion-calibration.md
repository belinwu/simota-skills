# Conversion Calibration System (TRANSMUTE)

Tool effectiveness tracking, quality trend analysis, template performance measurement, and conversion pattern improvement.
Morph gets better at format conversion by learning from outcomes.

---

## Overview

The TRANSMUTE phase runs post-task (or periodically) to close the feedback loop between conversion activities and actual output quality. Without TRANSMUTE, tool selection stays static and template choices remain uncalibrated. With it, Morph's conversions become progressively higher quality and more efficient.

```
RECORD ──→ EVALUATE ──→ CALIBRATE ──→ PROPAGATE
  │            │            │            │
  │ Log       │ Measure    │ Update    │ Share with
  │ conversions│ quality &  │ tool &    │ Lore
  │ & scores  │ trends     │ template  │
  │           │            │ weights   │
```

---

## RECORD — Log Conversion Activities

After each conversion task, record:

```yaml
Conversion: [conversion-id]
Type: [Markdown→PDF | Markdown→Word | Markdown→HTML | Word→PDF | HTML→PDF | Batch | Other]
Source_Format: [Markdown | Word | HTML | Excel | draw.io | Mermaid]
Target_Format: [PDF | Word | HTML | PNG | SVG]
Tool_Used: [pandoc+xelatex | pandoc+wkhtmltopdf | LibreOffice | Chrome/Puppeteer | mermaid-cli | draw.io-cli]
Template_Used: [corporate-ja | technical-ja | report-ja | minimal | corporate.css | technical.css | print.css | none]
Quality_Score:
  structure: [0-100]
  visual: [0-100]
  content: [0-100]
  metadata: [0-100]
  overall: [0-100]
  grade: [A/B/C/D/F]
Features_Lost: [list of unconvertible features]
Japanese_Specific: [kinsoku/fonts/tategaki applied: yes/no]
Accessibility_Applied: [PDF/UA/WCAG: yes/no]
Processing_Time: [seconds]
Downstream_Handoff: [Guardian/Nexus/Lore/None]
```

### What to Track

| Data Point | Why | Used For |
|-----------|-----|----------|
| Tool × format quality | Core calibration input | Tool selection heuristic improvement |
| Template effectiveness | Which templates produce highest quality per context | Template recommendation improvement |
| Feature loss rate | Which features are most commonly lost | Pre-conversion warning improvement |
| Processing time | Speed vs quality trade-offs | Pipeline optimization |
| Japanese-specific issues | Font/kinsoku problems | Japanese conversion tuning |
| Accessibility compliance | PDF/UA/WCAG pass rates | Accessible conversion improvement |

---

## EVALUATE — Measure Conversion Quality

### Quality Trend Tracking

```
Average Quality Score = Sum of Overall Scores / Total Conversions

> 90  = Excellent conversion quality (Grade A average)
80-90 = Good quality (maintain approach)
70-80 = Moderate quality (review tool selection, templates)
< 70  = Low quality (investigate root causes)
```

### Tool Performance Tracking

```
Tool Effectiveness = Conversions Scoring Grade A or B / Total Conversions with Tool

> 0.85  = Highly effective tool for this format pair
0.70-0.85 = Good, some issues in specific contexts
< 0.70  = Underperforming (review alternatives)
```

### Evaluation Triggers

| Trigger | Check |
|---------|-------|
| Grade C or below | Tool selection, template match, source quality |
| Feature loss reported | Conversion matrix accuracy, pre-warning completeness |
| Stakeholder feedback | Output format, styling, readability |
| New tool version available | Re-evaluate tool effectiveness |
| Quarterly review | Overall conversion health |

### Per-Period Evaluation Summary

```markdown
### Conversion Evaluation

| Metric | Value | Trend |
|--------|-------|-------|
| Conversions completed | 20 | — |
| Average quality score | 87/100 | ↑ |
| Grade A rate | 65% (13/20) | ↑ |
| Grade B rate | 25% (5/20) | — |
| Grade C or below | 10% (2/20) | ↓ |
| Average processing time | 4.2s | — |
| Feature loss rate | 8% | ↓ |
| Accessibility pass rate | 90% | ↑ |

**Strongest tool**: pandoc+xelatex for Markdown→PDF (95% Grade A)
**Weakest area**: Word→Markdown (complex tables frequently lost)
**Note**: corporate-ja template improved stakeholder satisfaction by 20%.
```

---

## CALIBRATE — Update Conversion Heuristics

### Tool Effectiveness Scoring

Track which tools work best for which format pairs:

```yaml
# Default tool effectiveness by conversion pair
markdown_to_pdf:
  pandoc_xelatex: 0.95
  pandoc_wkhtmltopdf: 0.80
  pandoc_lualatex: 0.90
markdown_to_word:
  pandoc: 0.85
markdown_to_html:
  pandoc: 0.95
word_to_pdf:
  libreoffice: 0.90
  pandoc: 0.65
html_to_pdf:
  chrome_puppeteer: 0.90
  wkhtmltopdf: 0.80
  pandoc: 0.60

# Calibrated (from TRANSMUTE data)
# Example: wkhtmltopdf more effective than expected for simple docs
html_to_pdf:
  wkhtmltopdf: 0.80 → 0.88  # Simple HTML docs converted well without Chrome overhead
```

### Calibration Rules

1. **3+ conversions required** before adjusting tool effectiveness scores
2. **Max adjustment per cycle**: ±0.15 (prevent overcorrection)
3. **Decay**: Adjustments decay 10% per quarter toward defaults
4. **Override**: User explicit tool preferences always win

### Template Performance Calibration

Track which templates produce best results by context:

| Template | Best For | Quality Score | Stakeholder Satisfaction |
|----------|----------|--------------|------------------------|
| corporate-ja.tex | Business proposals, formal reports | High | Very High |
| technical-ja.tex | API docs, technical specs | High | High |
| report-ja.tex | Project reports, status updates | High | High |
| minimal.tex | Quick conversions, simple docs | Medium | Medium |
| corporate.css | Web-exported business docs | Medium-High | High |
| technical.css | Code documentation, developer guides | High | High |
| print.css | Physical printing, booklets | High | Medium-High |

### Quality Score Calibration by Format Pair

Track typical quality scores and common issues:

| Format Pair | Default Expected Grade | Calibrated Range | Common Issues |
|------------|----------------------|-----------------|---------------|
| Markdown → PDF | A | A-B | Font embedding, image paths |
| Markdown → Word | B+ | B-A | Style mapping, code blocks |
| Markdown → HTML | A | A | Minimal issues |
| Word → PDF | A | A-B | Layout preservation |
| Word → Markdown | C+ | C-B | Table complexity, formatting loss |
| HTML → PDF | B+ | B-A | CSS support varies by tool |
| Excel → PDF | B | B-A | Sheet layout, column widths |

---

## PROPAGATE — Share Validated Patterns

### Journal Entry Format

Record TRANSMUTE insights in `.agents/morph.md`:

```markdown
## YYYY-MM-DD - TRANSMUTE: [Conversion Type]

**Conversions assessed**: N
**Average quality**: Grade X (Y/100)
**Key insight**: [description]
**Calibration adjustment**: [tool/template: old → new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Morph
date: YYYY-MM-DD
summary: [conversion insight]
affects: [Morph, Scribe, Lore]
priority: MEDIUM
reusable: true
-->
```

### Pattern Library

Build a library of effective conversion approaches by context:

| Context | Best Tool | Best Template | Key Settings | Quality |
|---------|----------|--------------|-------------|---------|
| Japanese business doc | pandoc+lualatex | corporate-ja | Hiragino fonts, A4, 25mm margins | Very High |
| Technical specification | pandoc+xelatex | technical-ja | Code highlighting, TOC, numbered sections | High |
| Quick PDF export | pandoc+wkhtmltopdf | none | Fast processing, basic styling | Medium |
| Accessible PDF | pandoc+lualatex | tagged PDF options | PDF/UA, lang metadata, 12pt min | High |
| Batch conversion | pandoc + Makefile | varies | Parallel processing, consistent config | High |
| Stakeholder report | pandoc+lualatex | corporate-ja | TOC, header/footer, watermark | Very High |

### Quick Calibration (Small Tasks)

For tasks with < 3 conversions:

```markdown
## Quick TRANSMUTE

**Conversions**: 1 completed
**Quality**: Grade A (92/100)
**Note**: corporate-ja template with lualatex produced excellent stakeholder PDF
**Action**: No weight change (insufficient data)
```

Rule: Do not adjust weights from a single small task. Accumulate data across tasks.

---

## Integration with Ecosystem

TRANSMUTE data feeds into conversion decisions:

| TRANSMUTE Signal | Ecosystem Impact |
|----------------|--------------------|
| Quality improving steadily | Conversion approach is working — continue |
| Quality degrading | Re-examine tool versions, template compatibility |
| Tool consistently underperforming | Switch to alternative, update conversion matrix |
| Template producing high satisfaction | Standardize for similar contexts |
| High feature loss rate | Improve pre-conversion warnings, suggest format alternatives |
| Validated conversion pattern | Share with Lore, update Scribe output recommendations |

---

## Feedback to Ecosystem

When TRANSMUTE discovers patterns valuable beyond a single task:

1. **Record in journal** with `reusable: true` tag
2. **Emit EVOLUTION_SIGNAL** for Lore to collect
3. **Feed to Scribe** if conversion patterns affect specification format choices
4. **Inform Harvest** if report format preferences improve readability
5. **Update tool selection defaults** if new tool versions prove more effective
