# Multilingual Strategy for NotebookLM

Reference for Prism's `multilingual` recipe. Cross-lingual source handling, output language pinning, terminology glossary as a source, and code-switching prompt patterns.

---

## 1. Three Decision Points

For every multilingual task, decide:

1. **Source language strategy** — translate before ingest, or let NotebookLM read native?
2. **Output language strategy** — pin via steering prompt, or let inference choose?
3. **Terminology consistency strategy** — glossary as source, or in-prompt list?

Decisions interact. Pin output to Japanese with English-only sources → NotebookLM auto-translates everything (lossy on jargon). Add a JA terminology glossary as a 6th source → quality jumps measurably.

---

## 2. Source Language Strategies

### Strategy 1: native (recommended default)
Upload sources in their original language; NotebookLM reads multilingually.

| When | Avoid when |
|---|---|
| Sources < 10 | Sources > 15 (multilingual context dilutes focus) |
| Each source is internally monolingual | Sources are bilingual (mixed within one document) |
| Rich source content (depth matters) | Need exact terminology preservation |

### Strategy 2: translate-before-ingest
Pre-translate sources to a single target language, then upload.

| When | Avoid when |
|---|---|
| Need exact JA / ZH terminology in output | Source has critical nuance lost in translation |
| Audience consumes only one language | Working budget allows native + glossary instead |
| Sources are short, translation is cheap | Translating destroys figures, code blocks |

Translation tools: DeepL, Google Translate, GPT-4o, Claude. Verify domain terminology against an authoritative glossary.

### Strategy 3: hybrid
Native sources + 1-2 translated companion sources for hardest passages.

Best for: 10-15 sources where 2-3 are critical and benefit from a controlled translation alongside the original.

---

## 3. Output Language Pinning

NotebookLM defaults to inferring output language from prompt + source mix. **Pin explicitly** for predictable results.

### Pin via steering prompt (preferred)
Place at the top of the steering prompt:
```
Generate the entire output in Japanese (日本語).
Do not switch to English except for proper nouns,
code identifiers, and the technical terms in the glossary source.
```

### Common pin templates
```
[JA pin]
すべての出力を日本語で生成してください。
固有名詞・コード識別子・グロッサリーソースの用語以外は英語を使わないでください。

[EN pin]
Output everything in English. Quote Japanese phrases inline only when
the source uses them as defined terms.

[Mixed: EN body, JA technical terms]
Output in English. Keep Japanese kanji terms (e.g., 確定申告, 青色申告)
as they appear in the source — do not translate them. Add a parenthetical
gloss on first mention only.
```

### Audio Overview language
Audio Overview language follows the steering prompt. Test with a short prompt first — voice mismatch (e.g., asking for Japanese with an English voice model) is jarring.

Cinematic Video is **English-only** (Ultra tier). Document this constraint upfront.

---

## 4. Terminology Glossary as a Source

The single highest-impact multilingual technique: **upload a glossary as a dedicated source**.

### Glossary format (Markdown / TXT, < 5 pages)
```markdown
# Project Glossary — JA / EN

## Tax domain
- 確定申告 (kakutei shinkoku) → "Income tax filing" — annual self-reported tax return
- 青色申告 (aoiro shinkoku) → "Blue return" — bookkeeping-based filing with deductions
- 白色申告 (shiroiro shinkoku) → "White return" — simplified filing without bookkeeping
- 給与所得 (kyūyo shotoku) → "Salary income" — wages from employment
- 事業所得 (jigyō shotoku) → "Business income" — sole-proprietorship revenue

## Use these EN translations consistently throughout outputs.
## When the JA term has no idiomatic EN equivalent, keep JA + parenthetical gloss.
```

Reference it in the steering prompt:
```
Use the terminology defined in the "Project Glossary — JA / EN" source
for all bilingual mappings. Do not invent alternative translations.
```

NotebookLM's grounding architecture will cite this source for terminology choices, dramatically improving consistency.

---

## 5. Code-Switching Patterns

### Pattern A: parenthetical gloss on first mention
```
Output in English. On first mention of a Japanese term, format as:
"<English translation> (<日本語>)". On subsequent mentions, use English only
unless quoting the source verbatim.
```

### Pattern B: inline JA preservation
```
Output in Japanese. Keep English technical terms (API names, CLI flags,
library names) in original Latin script — do not transliterate to katakana
unless the source does.
```

### Pattern C: dual-column for critical sections
```
For the "Comparison" section, render as a 2-column table:
| English term | 日本語 |
|---|---|
For all other sections, output in Japanese only.
```

### Pattern D: locale-aware numbers
```
Format numbers and dates per the JA locale:
- Numbers: 1,000,000 (English-style separators) — Japanese readers accept both
- Dates: 2026年4月25日 (full kanji) for formal text
- Currency: 1,500円 or ¥1,500 — match source convention
- Era: prefer 西暦 (CE) over 令和; if 令和 in source, gloss as "令和8年 (2026)"
```

---

## 6. Common Multilingual Pitfalls

| Pitfall | Avoidance |
|---|---|
| Mixed-language sources without glossary → terminology drift | Add glossary source; pin output language |
| Auto-translation of source produces awkward jargon | Translate-before-ingest with human-reviewed translation |
| Pin output to JA but sources only in EN → lossy | Add hybrid translated source for critical sections |
| Character encoding mojibake on upload | Verify UTF-8; re-export source if needed |
| Audio Overview voice mismatch with text language | Test short prompt first; check tier voice availability |
| Cinematic Video requested in JA → English only constraint | Document constraint; route to Video Brief instead |
| RTL languages (Arabic, Hebrew) in mixed source | NotebookLM handles direction inference; verify output |
| CJK character count vs token count miscalculated | CJK uses ~2-3 tokens per character; halve word-count budgets |
| Proper noun romanization inconsistent | Pin via glossary: "東京 → Tokyo (not Toukyou)" |
| Quoting verbatim across languages → loses citation grounding | Use "the source states" + native quote; avoid free translation in citations |

---

## 7. Decision Walkthrough Template

```
Sources languages detected:
  - Source 1: ____ (lang: ____, internally monolingual: ✓ / ✗)
  - Source 2: ____ (lang: ____, internally monolingual: ✓ / ✗)
  - Source 3: ____
  ...

Audience primary language: ____
Audience secondary languages: ____

Output language pin: ____ (rationale: ____)

Source strategy:
  □ Native (default)
  □ Translate-before-ingest  → tools: ____
  □ Hybrid (native + N translated)

Glossary source needed: ✓ / ✗
  If ✓, location: ____, format: MD / TXT / CSV

Code-switching pattern:
  □ A — parenthetical gloss on first mention
  □ B — inline preservation
  □ C — dual-column for critical sections
  □ D — locale-aware numbers
  □ Custom: ____________

Format-specific constraints:
  Audio Overview language: ____
  Video — Cinematic available?: EN-only (✓ / not applicable)
  Slides — locale font fallback verified: ✓ / ✗

Verification:
  □ Output language matches pin
  □ Terminology consistent with glossary
  □ No mojibake in source
  □ Citation grounding preserved
  □ Number / date format matches locale
  □ Audio voice matches text language
```

---

## 8. References
- NotebookLM language support documentation
- Google Cloud Translation glossary best practices
- W3C Internationalization — Bidirectional text
- DeepL / GPT-4o translation comparison for technical terminology
