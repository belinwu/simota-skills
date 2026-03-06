#!/usr/bin/env python3
"""
Second pass: fix remaining issues from first refactoring pass.
1. Remove INTERACTION_TRIGGERS with parenthesized headers
2. Remove remaining Agent Boundaries tables
3. Add missing _common/OPERATIONAL.md references
4. Remove standalone Interaction Triggers sections
5. Remove standalone Collaboration Partners sections
"""
import os
import re
import glob

SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKIP = {"_common", "_templates", "_scripts"}


def fix_skill(filepath):
    skill_name = filepath.split("/")[-2]
    with open(filepath, "r") as f:
        content = f.read()

    original = content

    # 1. Remove INTERACTION_TRIGGERS with parens in header
    content = re.sub(
        r'## INTERACTION_TRIGGERS\s*\([^)]*\)\n\n.*?(?=\n## |\n---\n)',
        '',
        content,
        flags=re.DOTALL
    )

    # 2. Remove "## Interaction Triggers" sections (with various formats)
    content = re.sub(
        r'## Interaction Triggers\n.*?(?=\n## |\n---\n)',
        '',
        content,
        flags=re.DOTALL
    )

    # 3. Remove remaining Agent Boundaries sections
    content = re.sub(
        r'## Agent Boundaries\n.*?(?=\n## |\n---\n)',
        '',
        content,
        flags=re.DOTALL
    )

    # 4. Compress "## Collaboration Partners" tables to Receives/Sends
    collab_match = re.search(
        r'## Collaboration Partners\n\n(.*?)(?=\n## |\n---\n)',
        content,
        flags=re.DOTALL
    )
    if collab_match:
        text = collab_match.group(1)
        # Extract from table rows
        receives = []
        sends = []
        for match in re.finditer(r'\|\s*(→S|S→)\s*\|\s*\*\*(\w+)\*\*\s*\|\s*(.*?)\s*\|', text):
            direction, agent, what = match.groups()
            if direction == '→S':
                receives.append(f"{agent} ({what.strip()})")
            else:
                sends.append(f"{agent} ({what.strip()})")

        if receives or sends:
            recv_str = " · ".join(receives) if receives else "Nexus (task context)"
            send_str = " · ".join(sends) if sends else "Nexus (results)"
            replacement = f"## Collaboration\n\n**Receives:** {recv_str}\n**Sends:** {send_str}\n"
            content = re.sub(
                r'## Collaboration Partners\n\n.*?(?=\n## |\n---\n)',
                replacement,
                content,
                flags=re.DOTALL
            )

    # 5. Add _common/OPERATIONAL.md if missing
    if '_common/OPERATIONAL.md' not in content:
        # Try to find and compress the Operational section
        op_match = re.search(
            r'(## Operational\n\n)(.*?)(\n## |\n---\n|\Z)',
            content,
            flags=re.DOTALL
        )
        if op_match:
            op_text = op_match.group(2)
            # Extract journal topic
            record_match = re.search(r'[Rr]ecord\s+(.*?)\s+only', op_text)
            if record_match:
                topic = record_match.group(1).strip()
                journal_line = f"**Journal** (`.agents/{skill_name}.md`): {topic} only — patterns and insights worth preserving."
            else:
                journal_match = re.search(r'\*\*Journal\*\*.*?:\s*(.*?)(?:\n|$)', op_text)
                if journal_match:
                    topic = journal_match.group(1).strip()
                    if len(topic) > 120:
                        topic = topic[:120].rsplit(' ', 1)[0] + "..."
                    journal_line = f"**Journal** (`.agents/{skill_name}.md`): {topic}"
                else:
                    journal_line = f"**Journal** (`.agents/{skill_name}.md`): Domain insights only — patterns and learnings worth preserving."

            replacement = f"## Operational\n\n{journal_line}\nStandard protocols → `_common/OPERATIONAL.md`\n"
            content = re.sub(
                r'## Operational\n\n.*?(?=\n## |\n---\n|\Z)',
                replacement,
                content,
                flags=re.DOTALL
            )
        else:
            # No Operational section at all - add before References or at end
            if '## References' in content:
                content = content.replace(
                    '## References',
                    f"## Operational\n\n**Journal** (`.agents/{skill_name}.md`): Domain insights only — patterns and learnings worth preserving.\nStandard protocols → `_common/OPERATIONAL.md`\n\n## References"
                )

    # 6. Add _common/BOUNDARIES.md if missing
    if '_common/BOUNDARIES.md' not in content:
        boundaries_match = re.search(r'(## Boundaries\n\n)', content)
        if boundaries_match:
            content = content.replace(
                boundaries_match.group(1),
                f"## Boundaries\n\nAgent role boundaries → `_common/BOUNDARIES.md`\n\n"
            )

    # Clean up multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.rstrip() + '\n'

    if content != original:
        with open(filepath, "w") as f:
            f.write(content)
        orig_lines = len(original.splitlines())
        new_lines = len(content.splitlines())
        return True, orig_lines, new_lines
    return False, 0, 0


def main():
    skills = sorted(glob.glob(os.path.join(SKILLS_DIR, "*/SKILL.md")))
    changed = 0

    for filepath in skills:
        skill_name = filepath.split("/")[-2]
        if skill_name in SKIP:
            continue

        was_changed, orig, new = fix_skill(filepath)
        if was_changed:
            changed += 1
            print(f"  FIXED {skill_name}: {orig} → {new}")

    print(f"\nTotal fixed: {changed} skills")


if __name__ == "__main__":
    main()
