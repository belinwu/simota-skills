#!/usr/bin/env python3
"""
Batch refactor SKILL.md files for the 余白 (margin) improvement plan.
Applies mechanical transformations to compress skills.
"""
import os
import re
import glob

SKILLS_DIR = "/Users/simota/.claude/skills"
SKIP = {"_common", "_templates", "_scripts", "nexus", "titan", "darwin"}


def refactor_skill(filepath):
    """Apply all transformation rules to a single SKILL.md."""
    with open(filepath, "r") as f:
        content = f.read()

    original_lines = len(content.splitlines())
    skill_name = filepath.split("/")[-2]

    # 1. DELETE Agent Boundaries table section
    # Pattern: ## Agent Boundaries ... until next ## section
    content = re.sub(
        r'## Agent Boundaries\n\n.*?(?=\n## )',
        '',
        content,
        flags=re.DOTALL
    )

    # Also handle "## Agent Boundaries" that may end with "**When to use**" etc
    # Clean up double newlines left by deletion
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 2. Add _common/BOUNDARIES.md reference at start of Boundaries section
    # Only add if not already present
    if '_common/BOUNDARIES.md' not in content:
        content = re.sub(
            r'(## Boundaries\n\n)',
            r'\1Agent role boundaries → `_common/BOUNDARIES.md`\n\n',
            content
        )

    # 3. DELETE INTERACTION_TRIGGERS section
    content = re.sub(
        r'## INTERACTION_TRIGGERS\n\n.*?(?=\n## |\n---\n)',
        '',
        content,
        flags=re.DOTALL
    )
    # Also handle "## Interaction Triggers" variant
    content = re.sub(
        r'## Interaction Triggers\n\n.*?(?=\n## |\n---\n)',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 4. COMPRESS Agent Collaboration section
    # Extract receives/sends info then replace
    collab_match = re.search(
        r'## Agent Collaboration\n\n(.*?)(?=\n## |\n---\n)',
        content,
        flags=re.DOTALL
    )
    if collab_match:
        collab_text = collab_match.group(1)
        receives, sends = extract_collaboration(collab_text)
        replacement = f"## Collaboration\n\n**Receives:** {receives}\n**Sends:** {sends}\n"
        content = re.sub(
            r'## Agent Collaboration\n\n.*?(?=\n## |\n---\n)',
            replacement,
            content,
            flags=re.DOTALL
        )

    # Also handle existing "## Collaboration & Tactics" variant
    collab_match2 = re.search(
        r'## Collaboration & Tactics\n\n(.*?)(?=\n## |\n---\n)',
        content,
        flags=re.DOTALL
    )
    if collab_match2:
        collab_text = collab_match2.group(1)
        receives, sends = extract_collaboration(collab_text)
        replacement = f"## Collaboration\n\n**Receives:** {receives}\n**Sends:** {sends}\n"
        content = re.sub(
            r'## Collaboration & Tactics\n\n.*?(?=\n## |\n---\n)',
            replacement,
            content,
            flags=re.DOTALL
        )

    # 5. COMPRESS Operational section
    # Find the Operational section and extract journal topic
    operational_match = re.search(
        r'## Operational\n\n(.*?)(?=\n## References|\n## References\n|\n---\n|\Z)',
        content,
        flags=re.DOTALL
    )
    if operational_match:
        op_text = operational_match.group(1)
        journal_topic = extract_journal_topic(op_text, skill_name)
        replacement = f"## Operational\n\n**Journal** (`.agents/{skill_name}.md`): {journal_topic}\nStandard protocols → `_common/OPERATIONAL.md`\n"
        content = re.sub(
            r'## Operational\n\n.*?(?=\n## References|\n---\n|\Z)',
            replacement,
            content,
            flags=re.DOTALL
        )

    # Also compress standalone Journal section if it exists before Operational
    content = re.sub(
        r'## Journal\n\n.*?(?=\n## )',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 6. Ensure consistent closing format
    # Make sure there's --- before the closing > line
    content = re.sub(r'\n\n(> (?:Remember|You\'re).*?)$', r'\n\n---\n\n\1', content, flags=re.MULTILINE)
    # But don't double the ---
    content = re.sub(r'---\n\n---', '---', content)

    # Final cleanup
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.rstrip() + '\n'

    new_lines = len(content.splitlines())

    with open(filepath, "w") as f:
        f.write(content)

    return original_lines, new_lines


def extract_collaboration(text):
    """Extract receives/sends from collaboration section text."""
    # Try to find INPUT/Inbound patterns
    receives_parts = []
    sends_parts = []

    # Look for "Input:" or "Inbound" patterns
    input_match = re.search(r'(?:Input|Inbound|Receives)[:\s]*\n?\|.*?\n((?:\|.*?\n)*)', text, re.IGNORECASE)
    output_match = re.search(r'(?:Output|Outbound|Sends)[:\s]*\n?\|.*?\n((?:\|.*?\n)*)', text, re.IGNORECASE)

    if input_match:
        for row in re.findall(r'\|\s*(\w+)\s*\|\s*(.*?)\s*\|', input_match.group(1)):
            if row[0] not in ('---', 'From', 'Agent'):
                receives_parts.append(f"{row[0]} ({row[1].strip().rstrip('|').strip()})")

    if output_match:
        for row in re.findall(r'\|\s*(\w+)\s*\|\s*(.*?)\s*\|', output_match.group(1)):
            if row[0] not in ('---', 'To', 'Agent'):
                sends_parts.append(f"{row[0]} ({row[1].strip().rstrip('|').strip()})")

    # Fallback: look for pattern table rows
    if not receives_parts and not sends_parts:
        # Try to parse generic table
        rows = re.findall(r'\|\s*\*\*([A-Z])\*\*\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|', text)
        if rows:
            for r in rows:
                flow = r[2].strip()
                agents = re.findall(r'(\w+)(?:→|/)', flow)
                if agents:
                    for a in agents[:1]:
                        receives_parts.append(a)

        # Try looking at **Input**: / **Output**: patterns in comment block
        input_inline = re.search(r'\*\*Input\*\*:\s*(.*?)(?:\n|$)', text)
        output_inline = re.search(r'\*\*Output\*\*:\s*(.*?)(?:\n|$)', text)
        if input_inline:
            receives_parts = [input_inline.group(1).strip()]
        if output_inline:
            sends_parts = [output_inline.group(1).strip()]

    # Fallback: look for "Patterns" text and extract agent names
    if not receives_parts:
        pattern_agents = re.findall(r'(\w+)(?:\s*→\s*|\s*←\s*)', text)
        if pattern_agents:
            receives_parts = [f"{a} (context)" for a in set(pattern_agents[:3])]

    receives = " · ".join(receives_parts) if receives_parts else "Nexus (task context)"
    sends = " · ".join(sends_parts) if sends_parts else "Nexus (results)"

    return receives, sends


def extract_journal_topic(text, skill_name):
    """Extract the journal-specific topic from operational section."""
    # Look for "Record ... only" or similar patterns
    record_match = re.search(r'[Rr]ecord\s+(.*?)\s+only', text)
    if record_match:
        topic = record_match.group(1).strip()
        return f"{topic} only — patterns and insights worth preserving."

    # Look for journal-specific description
    journal_match = re.search(r'[Jj]ournal.*?:\s*(.*?)(?:\n|Format:)', text, re.DOTALL)
    if journal_match:
        topic = journal_match.group(1).strip()
        if len(topic) > 100:
            topic = topic[:100].rsplit(' ', 1)[0] + "..."
        return topic

    # Default based on skill name
    topic_map = {
        "scout": "Investigation patterns only — root cause insights, effective search strategies.",
        "builder": "Implementation patterns only — effective approaches, reusable solutions.",
        "radar": "Testing insights only — effective test patterns, flaky test solutions.",
        "sentinel": "Security findings only — vulnerability patterns, effective mitigations.",
        "bolt": "Performance insights only — optimization patterns, measurement techniques.",
    }
    return topic_map.get(skill_name, f"Domain insights only — patterns and learnings worth preserving.")


def main():
    skills = sorted(glob.glob(os.path.join(SKILLS_DIR, "*/SKILL.md")))
    results = []

    for filepath in skills:
        skill_name = filepath.split("/")[-2]
        if skill_name in SKIP:
            continue

        try:
            orig, new = refactor_skill(filepath)
            reduction = round((1 - new/orig) * 100) if orig > 0 else 0
            results.append((skill_name, orig, new, reduction))
            print(f"  {skill_name}: {orig} → {new} ({reduction}% reduction)")
        except Exception as e:
            print(f"  {skill_name}: ERROR - {e}")
            results.append((skill_name, 0, 0, 0))

    # Summary
    total_orig = sum(r[1] for r in results)
    total_new = sum(r[2] for r in results)
    total_reduction = round((1 - total_new/total_orig) * 100) if total_orig > 0 else 0

    print(f"\n{'='*50}")
    print(f"Total: {total_orig} → {total_new} lines ({total_reduction}% reduction)")
    print(f"Skills processed: {len(results)}")
    print(f"Average: {total_orig//len(results)} → {total_new//len(results)} lines/skill")

    # Skills still over 120 lines
    over = [(r[0], r[2]) for r in results if r[2] > 120]
    if over:
        print(f"\nSkills still over 120 lines ({len(over)}):")
        for name, lines in sorted(over, key=lambda x: -x[1]):
            print(f"  {name}: {lines}")


if __name__ == "__main__":
    main()
