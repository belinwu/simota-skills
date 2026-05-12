# Unicode Tag / Bidi / Zero-Width Scan

Purpose: load this when running `chain scan` or when the intake checklist's Unicode step needs detailed procedure. Defines the codepoint policy, allowlist exceptions, and scanner commands.

## Why this matters

Hidden-instruction channels in Markdown / SKILL.md / bundled scripts are the canonical way to defeat human review. The Unicode Tag block (`U+E0000`–`U+E007F`) was originally intended for language tagging and has no legitimate use in modern documents — yet major LLMs interpret it as instructions. Bidi overrides and zero-width chars can rearrange visible-vs-actual code (`bidi-bomb` attacks, e.g. CVE-2021-42574 "Trojan Source"). Reject all three on sight inside skill / plugin / MCP artifacts.

[Source: embracethered.com — Scary Agent Skills; Trojan Source CVE-2021-42574]

## Codepoint Policy

| Range | Name | Default policy | Allowlist exception |
|-------|------|----------------|---------------------|
| `U+E0000`–`U+E007F` | Unicode Tags block | **REJECT** in all files | None. Tag block has no legitimate use here. |
| `U+202A`–`U+202E` | LRE / RLE / PDF / LRO / RLO (Bidi overrides) | **REJECT** | i18n strings explicitly marked `<!-- i18n: bidi -->` |
| `U+2066`–`U+2069` | LRI / RLI / FSI / PDI (Bidi isolates) | **REJECT** | i18n strings explicitly marked `<!-- i18n: bidi -->` |
| `U+200B` | ZWSP (Zero-Width Space) | **REJECT** in instruction positions | URLs, regex character classes, allowlisted `<!-- zwsp: ok -->` |
| `U+200C` | ZWNJ | **REJECT** in instruction positions | i18n (Persian, Arabic, Indic scripts) — allowlist with `<!-- i18n: zwnj -->` |
| `U+200D` | ZWJ | **REJECT** in instruction positions | emoji sequences, i18n |
| `U+FEFF` | BOM / ZWNBSP | **REJECT** mid-file | file start only |
| `U+0085`, `U+2028`, `U+2029` | NEL / LS / PS | **FLAG** | normal line separators are `\n` / `\r\n` |

"Instruction positions" means any line that is not inside a fenced code block (` ``` ... ``` `) and not inside an explicit i18n allowlist marker.

## Scanner Commands

### Unicode Tag (P0 reject)

The Unicode Tag block in UTF-8 is encoded as `F3 A0 80 80` through `F3 A0 81 BF`.

```bash
# Detect any byte sequence in the Tag range
LC_ALL=C grep -rPl '\xf3\xa0[\x80\x81][\x80-\xbf]' <skill-dir>
```

Any hit → return file path and offset → `REJECT + QUARANTINE` with severity `P0`.

### Bidi overrides (P0 reject outside allowlist)

```bash
# LRE/RLE/PDF/LRO/RLO: U+202A–U+202E → E2 80 AA–AE
# LRI/RLI/FSI/PDI:     U+2066–U+2069 → E2 81 A6–A9
LC_ALL=C grep -rPnE $'\xe2\x80[\xaa-\xae]|\xe2\x81[\xa6-\xa9]' <skill-dir>
```

For each hit, check the surrounding 50 chars for an `<!-- i18n: bidi -->` marker on the same line or immediately preceding line. No marker → `P0 REJECT`.

### Zero-width chars in instruction positions

```bash
# ZWSP/ZWNJ/ZWJ → E2 80 8B/8C/8D; BOM → EF BB BF
LC_ALL=C grep -rPnE $'\xe2\x80[\x8b-\x8d]|\xef\xbb\xbf' <skill-dir> \
  | grep -v '```' \
  | grep -vE '<!-- (zwsp|i18n): '
```

Hits outside allowlist → `P1 REJECT`. BOM mid-file → `P1 FLAG`.

### Combined one-shot

```bash
#!/bin/bash
# chain/scripts/unicode-scan.sh — usage: unicode-scan.sh <skill-dir>
set -euo pipefail
target="$1"
status=0

echo "== Unicode Tag block (U+E0000-U+E007F) =="
if LC_ALL=C grep -rPln '\xf3\xa0[\x80\x81][\x80-\xbf]' "$target"; then
  echo "P0: Unicode Tag detected — REJECT"
  status=2
fi

echo "== Bidi overrides (U+202A-U+202E, U+2066-U+2069) =="
hits=$(LC_ALL=C grep -rPln $'\xe2\x80[\xaa-\xae]|\xe2\x81[\xa6-\xa9]' "$target" || true)
for line in $hits; do
  if ! grep -B1 -F "$line" "$target" | grep -q '<!-- i18n: bidi -->'; then
    echo "P0: Bidi override (no allowlist marker) — $line"
    status=2
  fi
done

echo "== Zero-width chars =="
LC_ALL=C grep -rPln $'\xe2\x80[\x8b-\x8d]' "$target" | grep -v '```' | \
  grep -vE '<!-- (zwsp|i18n): ' && status=1 || true

exit $status
```

Exit codes: `0` pass, `1` flag (P1/P2), `2` reject (P0).

## Hex Dump Verification

When a scanner hit is reported, confirm with a hex dump of the affected line:

```bash
sed -n '<line>p' <file> | xxd | head -4
```

Look for `f3 a0 80 80`–`f3 a0 81 bf` (Tag), `e2 80 aa`–`e2 80 ae` (LRE/RLE/PDF/LRO/RLO), `e2 81 a6`–`e2 81 a9` (LRI/RLI/FSI/PDI), `e2 80 8b`–`e2 80 8d` (ZWSP/ZWNJ/ZWJ).

## Allowlist Marker Syntax

Allowed only in contexts where the codepoint is necessary:

```markdown
<!-- i18n: bidi -->
‮This Arabic line uses RLE intentionally.‬

<!-- i18n: zwnj -->
می‌خواهم (Persian word with ZWNJ)

<!-- zwsp: ok -->
example‍.com (deliberate ZWSP for display reasons)
```

Markers must be on the line immediately above the codepoint or on the same line. A trailing space or wrapped marker is invalid.

## What If the Skill Legitimately Needs Tag-Block Codepoints

No. There is no legitimate use of the Unicode Tag block in SKILL.md / plugin manifest / MCP tool descriptions. If a maintainer claims a legitimate need, treat it as a red flag and escalate to `triage`.

## Manifest Annotation

When a skill passes the Unicode scan, record the scan result in `.chain-manifest.json`:

```json
{
  "unicode_scan": {
    "version": "1",
    "tag_block": "clean",
    "bidi_overrides": "clean",
    "zero_width": "clean",
    "scanned_at": "2026-05-12T00:00:00Z",
    "scanner": "chain/scripts/unicode-scan.sh"
  }
}
```

On drift detection (`chain audit`), rerun the scanner and update the manifest only if all checks remain clean and the maintainer's explanation passes review.
