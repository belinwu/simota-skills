# Template Library

> Ready-to-use templates for LaTeX, CSS, and Word document conversion

This library provides production-quality templates for common document types.

---

## Template Overview

| Template | Format | Purpose | Language Support |
|----------|--------|---------|------------------|
| corporate-ja | LaTeX | Business documents | Japanese |
| technical-ja | LaTeX | Technical documents | Japanese |
| report-ja | LaTeX | Reports | Japanese |
| minimal | LaTeX | Clean, simple | Universal |
| corporate.css | CSS | PDF via HTML | Universal |
| technical.css | CSS | Code-focused | Universal |
| print.css | CSS | Print optimization | Universal |

---

## LaTeX Templates

### Corporate Japanese Template (corporate-ja.tex)

```latex
% corporate-ja.tex - Corporate document template for Japanese
% Usage: pandoc input.md -o output.pdf --template=corporate-ja.tex --pdf-engine=lualatex

\documentclass[a4paper,11pt]{ltjsarticle}

%% ========================================
%% Package imports
%% ========================================
\usepackage{luatexja-fontspec}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{geometry}
\usepackage{setspace}
\usepackage{xcolor}
\usepackage{titlesec}
// ...
```

### Technical Japanese Template (technical-ja.tex)

```latex
% technical-ja.tex - Technical document template for Japanese
% Usage: pandoc input.md -o output.pdf --template=technical-ja.tex --pdf-engine=lualatex

\documentclass[a4paper,10pt]{ltjsarticle}

%% ========================================
%% Package imports
%% ========================================
\usepackage{luatexja-fontspec}
\usepackage{geometry}
\usepackage{setspace}
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{booktabs}
// ...
```

### Report Japanese Template (report-ja.tex)

```latex
% report-ja.tex - Report template for Japanese
% Usage: pandoc input.md -o output.pdf --template=report-ja.tex --pdf-engine=lualatex

\documentclass[a4paper,11pt]{ltjsreport}

%% ========================================
%% Package imports
%% ========================================
\usepackage{luatexja-fontspec}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{geometry}
\usepackage{setspace}
\usepackage{xcolor}
\usepackage{titlesec}
// ...
```

### Minimal Template (minimal.tex)

```latex
% minimal.tex - Clean, minimal template
% Usage: pandoc input.md -o output.pdf --template=minimal.tex --pdf-engine=xelatex

\documentclass[a4paper,11pt]{article}

\usepackage{fontspec}
\usepackage{geometry}
\usepackage{setspace}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{graphicx}

// ...
```

---

## CSS Templates

### Corporate CSS (corporate.css)

```css
/* corporate.css - Corporate PDF styling via HTML conversion */
/* Usage: pandoc input.md -o output.html -s --css=corporate.css */

@charset "UTF-8";

/* ========================================
   Page setup for PDF
   ======================================== */
@page {
  size: A4;
  margin: 25mm;
  @top-left {
    content: "Company Name";
    font-size: 9pt;
    color: #666;
/* ... */
```

### Technical CSS (technical.css)

```css
/* technical.css - Technical document styling with dark code blocks */
/* Usage: pandoc input.md -o output.html -s --css=technical.css */

@charset "UTF-8";

/* ========================================
   Page setup
   ======================================== */
@page {
  size: A4;
  margin: 20mm;
}

/* ========================================
   Root variables
/* ... */
```

### Print CSS (print.css)

```css
/* print.css - Print-optimized stylesheet */
/* Usage: pandoc input.md -o output.html -s --css=print.css */

@charset "UTF-8";

/* ========================================
   Page setup
   ======================================== */
@page {
  size: A4;
  margin: 20mm 25mm;
  @bottom-center {
    content: counter(page) " / " counter(pages);
    font-size: 9pt;
  }
/* ... */
```

---

## Word Reference Documents

### Creating Word Templates

Word templates use reference documents that define styles.

**Creating a reference document:**

1. Create a new Word document
2. Apply styles to sample content:
   - Heading 1, 2, 3
   - Normal text
   - Code
   - Table styles
3. Save as `reference.docx`

**Using with Pandoc:**
```bash
pandoc input.md -o output.docx --reference-doc=reference.docx
```

### Corporate Reference Structure

```
reference-corporate.docx should contain:

# Heading 1
(Font: Gothic, 18pt, Bold, Color: Corporate Blue)

## Heading 2
(Font: Gothic, 14pt, Bold)

### Heading 3
(Font: Gothic, 12pt, Bold)

Normal paragraph text.
(Font: Mincho, 10.5pt, Line spacing 1.7)

`Code inline`
...
```
Code block
```
(Font: Monospace, 9pt, Gray background, Border)

| Table Header |
(Font: Gothic, Bold, Dark background)

| Table Cell |
(Font: Mincho, 10pt)
```

### Technical Reference Structure

```
reference-technical.docx should contain:

# Heading 1
(Font: Sans-serif, 16pt, Bold, Bottom border)

## Heading 2
(Font: Sans-serif, 13pt, Bold)

### Heading 3
(Font: Sans-serif, 11pt, Bold)

Normal paragraph text.
(Font: Sans-serif, 10pt, Line spacing 1.4)

Code sections with monospace font.
...
```

---

## Template Variables

### Common Pandoc Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `$title$` | Document title | Technical Specification |
| `$subtitle$` | Subtitle | v1.0 |
| `$author$` | Author name | John Doe |
| `$date$` | Date | 2025-01-15 |
| `$version$` | Version number | 1.0.0 |
| `$company$` | Company name | ACME Inc. |
| `$logo$` | Logo file path | logo.png |
| `$confidential$` | Confidentiality mark | true |
| `$lang$` | Language code | ja |
| `$toc$` | Include TOC | true |
| `$toc-depth$` | TOC depth | 3 |

### YAML Front Matter Example

```yaml
---
title: "Document Title"
subtitle: "Subtitle Here"
author: "Author Name"
date: 2025-01-15
version: "1.0.0"
company: "Company Name"
logo: "logo.png"
confidential: true
lang: ja
toc: true
toc-depth: 3
abstract: |
  This is the document abstract.
  It can span multiple lines.
# ...
```

### Using Variables in Command Line

```bash
pandoc input.md -o output.pdf \
  --template=corporate-ja.tex \
  --pdf-engine=lualatex \
  -V title="Document Title" \
  -V author="Author Name" \
  -V date="2025-01-15" \
  -V company="Company Name" \
  -V confidential=true \
  -V toc=true
```

---

## Template Selection Guide

| Document Type | Recommended Template |
|---------------|---------------------|
| Business proposal | corporate-ja.tex |
| API documentation | technical-ja.tex |
| Project report | report-ja.tex |
| README/simple docs | minimal.tex |
| Web export | corporate.css |
| Code documentation | technical.css |
| Physical printing | print.css |
