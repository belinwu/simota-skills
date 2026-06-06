#!/usr/bin/env python3
"""Sync Recipes from each skill's SKILL.md into the realm-directory JSON data.

For every directory under `/Users/simota/.claude/skills/<agent>/SKILL.md`,
parse the `## Recipes` section's markdown table and write the resulting
list into `templates/realm-directory/assets/data/agents/<agent>.json` as:

    "recipes": [
      {
        "subcommand": "pr",
        "label": "PR Preparation",
        "default": true,
        "when": "PR preparation (title/body/review angles/risk assessment)"
      },
      ...
    ]

Then regenerate `agents.index.json` from the per-agent files (preserving
existing order; new agents are appended alphabetically).

Run manually whenever a SKILL.md Recipes table is added or changed.
"""
import json
import re
import sys
from pathlib import Path

SKILLS = Path("/Users/simota/.claude/skills")
DATA = SKILLS / "realm/templates/realm-directory/assets/data"
AGENTS_DIR = DATA / "agents"
INDEX = DATA / "agents.index.json"

RECIPE_HEAD_RE = re.compile(r"^\|\s*Recipe\s*\|\s*Subcommand\s*\|", re.IGNORECASE)
SEPARATOR_RE = re.compile(r"^\|[\s\-:|]+\|$")
ROW_RE = re.compile(r"^\|(.+)\|$")


def parse_recipes(md_path: Path) -> list[dict]:
    """Parse a SKILL.md and return the list of Recipe dicts."""
    text = md_path.read_text(encoding="utf-8")
    in_section = False
    in_table = False
    rows: list[dict] = []
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            if in_section:
                break
            in_section = line == "## Recipes"
            continue
        if not in_section:
            continue
        if RECIPE_HEAD_RE.match(line):
            in_table = True
            continue
        if in_table and SEPARATOR_RE.match(line):
            continue
        if not in_table:
            continue
        m = ROW_RE.match(line)
        if not m:
            if line == "":
                continue
            in_table = False
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if len(cells) < 4:
            continue
        label, sub_raw, default_raw, when = cells[0], cells[1], cells[2], cells[3]
        sub_match = re.search(r"`([^`]+)`", sub_raw)
        subcommand = sub_match.group(1) if sub_match else sub_raw
        if not subcommand:
            continue
        is_default = (
            "✓" in default_raw
            or "yes" in default_raw.lower()
            or "default" in default_raw.lower()
        )
        rows.append({
            "subcommand": subcommand,
            "label": label,
            "default": is_default,
            "when": when,
        })
    return rows


def sync_all() -> tuple[int, int, int]:
    """Update every per-agent JSON. Returns (updated, missing_json, no_recipes)."""
    updated = 0
    missing_json = 0
    no_recipes = 0
    skill_dirs = sorted(d for d in SKILLS.iterdir() if d.is_dir() and (d / "SKILL.md").exists())
    for sd in skill_dirs:
        name = sd.name
        json_path = AGENTS_DIR / f"{name}.json"
        if not json_path.exists():
            missing_json += 1
            continue
        recipes = parse_recipes(sd / "SKILL.md")
        if not recipes:
            no_recipes += 1
        data = json.loads(json_path.read_text(encoding="utf-8"))
        data["recipes"] = recipes
        json_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        updated += 1
    return updated, missing_json, no_recipes


def rebuild_index() -> int:
    """Rebuild agents.index.json from the per-agent JSONs.

    Preserves existing order; appends new entries alphabetically.
    """
    existing = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else {"agents": []}
    existing_order = [a["name"] for a in existing.get("agents", [])]
    agents = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in AGENTS_DIR.glob("*.json")}
    ordered: list[dict] = []
    for name in existing_order:
        if name in agents:
            ordered.append(agents[name])
            del agents[name]
    for name in sorted(agents.keys()):
        ordered.append(agents[name])
    INDEX.write_text(
        json.dumps({"agents": ordered}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return len(ordered)


def main() -> int:
    updated, missing_json, no_recipes = sync_all()
    total = rebuild_index()
    print(f"Per-agent JSON updated: {updated}")
    print(f"Per-agent JSON missing: {missing_json}")
    print(f"Agents with no Recipes table: {no_recipes}")
    print(f"agents.index.json rebuilt with {total} agents")
    return 0


if __name__ == "__main__":
    sys.exit(main())
