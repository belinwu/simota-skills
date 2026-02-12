# Morph Conversion Workflow

Detailed 5-step conversion process: Analyze → Configure → Convert → Verify → Deliver.

---

## 1. ANALYZE — Understand the Source

**Input Analysis:**
- Identify source format and structure
- Detect features that may not convert (tables, images, code blocks)
- Check for external dependencies (images, fonts, stylesheets)
- Estimate conversion complexity

**Feature Inventory Template:**
```markdown
## Source Analysis: [filename]

**Format:** Markdown / Word / HTML / Other
**Size:** X pages / Y KB
**Structure:**
- Headings: [levels used]
- Tables: [count, complexity]
- Images: [count, formats]
- Code blocks: [count, languages]
- Cross-references: [internal links]

**Potential Issues:**
- [Feature that may not convert]
- [Missing dependencies]
```

---

## 2. CONFIGURE — Select Tools and Options

**Tool Selection:**
- Choose best tool for source → target conversion
- Configure output options (page size, margins, fonts)
- Select template if applicable
- Set up metadata (title, author, date)

**Configuration Template:**
```yaml
conversion:
  source: input.md
  target: output.pdf
  tool: pandoc
  options:
    pdf-engine: xelatex
    toc: true
    toc-depth: 3
    template: corporate
    metadata:
      title: "Document Title"
      author: "Author Name"
      date: "2025-01-15"
```

---

## 3. CONVERT — Execute Transformation

**Conversion Steps:**
1. Validate source file
2. Prepare dependencies (images, fonts)
3. Execute conversion command
4. Check for errors/warnings
5. Generate output

**Error Handling Template:**
```markdown
## Conversion Log

**Status:** SUCCESS / PARTIAL / FAILED

**Warnings:**
- [Warning about feature loss]
- [Font substitution]

**Errors:**
- [Critical error if any]

**Output:** [path/to/output.pdf]
```

---

## 4. VERIFY — Quality Check

**Quality Checklist:**
- [ ] All headings preserved
- [ ] Tables render correctly
- [ ] Images display properly
- [ ] Code blocks formatted
- [ ] Links functional (internal/external)
- [ ] Page breaks appropriate
- [ ] Fonts render correctly
- [ ] Metadata present

---

## 5. DELIVER — Provide Output

**Delivery Template:**
```markdown
## Conversion Complete

**Source:** [source file path]
**Output:** [output file path]
**Format:** PDF / Word / HTML

**Quality Score:** X/10

**Notes:**
- [Any important observations]
- [Recommendations for future]

**Command Used:**
\`\`\`bash
[actual command]
\`\`\`
```
