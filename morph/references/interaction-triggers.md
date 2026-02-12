# Morph Interaction Trigger Templates

YAML question templates for `AskUserQuestion` tool.

---

## ON_FORMAT_CHOICE

```yaml
questions:
  - question: "Which output format do you need?"
    header: "Output Format"
    options:
      - label: "PDF (Recommended)"
        description: "Universal, print-ready, preserves layout"
      - label: "Word (.docx)"
        description: "Editable, track changes support"
      - label: "HTML"
        description: "Web-ready, responsive"
      - label: "Markdown"
        description: "Plain text, version control friendly"
    multiSelect: false
```

## ON_TEMPLATE_SELECT

```yaml
questions:
  - question: "Which template should be applied?"
    header: "Template"
    options:
      - label: "Default (Recommended)"
        description: "Clean, minimal styling"
      - label: "Corporate"
        description: "Company branding, headers/footers"
      - label: "Technical"
        description: "Code-focused, syntax highlighting"
      - label: "Print-optimized"
        description: "High quality for physical printing"
    multiSelect: false
```

## ON_FEATURE_LOSS

```yaml
questions:
  - question: "Some features cannot be converted. How to proceed?"
    header: "Feature Loss"
    options:
      - label: "Proceed with best effort (Recommended)"
        description: "Convert what's possible, document losses"
      - label: "Choose different format"
        description: "Select a format that supports all features"
      - label: "Create hybrid output"
        description: "Split into multiple files by feature support"
      - label: "Cancel conversion"
        description: "Do not proceed until source is modified"
    multiSelect: false
```

## ON_TOOL_SELECT

```yaml
questions:
  - question: "Multiple tools can handle this conversion. Which to use?"
    header: "Tool Selection"
    options:
      - label: "Pandoc (Recommended)"
        description: "Most versatile, best for complex documents"
      - label: "LibreOffice"
        description: "Best for Office formats, complex tables"
      - label: "wkhtmltopdf"
        description: "Best for HTML to PDF with web styling"
      - label: "Chrome/Puppeteer"
        description: "Best for modern CSS, JavaScript rendering"
    multiSelect: false
```

## ON_BATCH_CONFIRM

```yaml
questions:
  - question: "Batch processing will convert multiple files. Confirm?"
    header: "Batch"
    options:
      - label: "Process all files (Recommended)"
        description: "Convert all matching files with same settings"
      - label: "Select specific files"
        description: "Choose which files to convert"
      - label: "Process in test mode first"
        description: "Convert one file first to verify settings"
      - label: "Cancel"
        description: "Do not proceed with batch conversion"
    multiSelect: false
```

## ON_STYLE_CHOICE

```yaml
questions:
  - question: "Multiple styling options available. Which to apply?"
    header: "Style"
    options:
      - label: "Default styling (Recommended)"
        description: "Clean, standard formatting"
      - label: "Custom CSS/template"
        description: "Apply project-specific styling"
      - label: "Minimal"
        description: "No extra styling, content only"
    multiSelect: false
```

## ON_OUTPUT_LOCATION

```yaml
questions:
  - question: "Where should the converted file be saved?"
    header: "Output"
    options:
      - label: "Same directory as source (Recommended)"
        description: "Place output next to the source file"
      - label: "Dedicated output directory"
        description: "Place in ./output/ or similar"
      - label: "Custom path"
        description: "Specify a custom output location"
    multiSelect: false
```
