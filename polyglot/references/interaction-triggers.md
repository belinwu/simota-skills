# Interaction Trigger Templates

YAML question templates for `AskUserQuestion` at key i18n decision points.

---

## BEFORE_LANGUAGE_SELECT

```yaml
questions:
  - question: "Which languages should be supported?"
    header: "Languages"
    options:
      - label: "Japanese and English only (Recommended)"
        description: "Start with minimal language set"
      - label: "Add major Asian languages"
        description: "Include Chinese, Korean"
      - label: "Global support"
        description: "Include European and RTL languages"
    multiSelect: false
```

## ON_TRANSLATION_APPROACH

```yaml
questions:
  - question: "Which translation approach should be used?"
    header: "Translation"
    options:
      - label: "Extract keys only (Recommended)"
        description: "Prepare translation keys, humans translate later"
      - label: "Machine translation draft"
        description: "Use machine translation as placeholder"
      - label: "Keep English"
        description: "Prepare for translation but maintain English text"
    multiSelect: false
```

## ON_LOCALE_FORMAT

```yaml
questions:
  - question: "Which date/currency format style should be used?"
    header: "Locale"
    options:
      - label: "Follow browser settings (Recommended)"
        description: "Auto-detect user's locale"
      - label: "Match UI language"
        description: "Use format of selected language"
      - label: "ISO standard format"
        description: "Use region-independent standard format"
    multiSelect: false
```

## ON_GLOSSARY_CHANGE

```yaml
questions:
  - question: "Glossary changes are needed. How should we proceed?"
    header: "Glossary"
    options:
      - label: "Maintain existing terms (Recommended)"
        description: "Use current terms for consistency"
      - label: "Record new terms as proposal"
        description: "Document change proposal for later review"
      - label: "Update terminology"
        description: "Change to new terms project-wide"
    multiSelect: false
```

## ON_RTL_SUPPORT

```yaml
questions:
  - question: "RTL (right-to-left) language support is needed. How should we proceed?"
    header: "RTL Support"
    options:
      - label: "Use CSS logical properties (Recommended)"
        description: "Use start/end for automatic flipping"
      - label: "RTL-specific stylesheet"
        description: "Manage RTL styles in separate CSS file"
      - label: "Handle later"
        description: "Support only LTR languages for now"
    multiSelect: false
```
