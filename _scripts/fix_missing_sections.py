#!/usr/bin/env python3
"""
Fix remaining missing sections in 25 SKILL.md files.
Pattern-based insertion: S2 before Boundaries, S9 before AUTORUN, etc.
"""

import re
import os

SKILLS_DIR = "/Users/simota/.claude/skills"


def insert_before(content, marker, new_section):
    """Insert new_section before the line containing marker."""
    idx = content.find(marker)
    if idx == -1:
        return content
    # Find the start of the line (or blank line before)
    # Go back to find a good insertion point (blank line before marker's ##)
    line_start = content.rfind('\n', 0, idx)
    if line_start == -1:
        line_start = 0
    # Check if there's a blank line before
    prev_line_end = content.rfind('\n', 0, line_start)
    return content[:line_start] + '\n\n' + new_section + content[line_start:]


def add_s2_before_boundaries(content, agent_name):
    """Add ## Core Contract before ## Boundaries."""
    if '## Core Contract' in content:
        return content
    s2 = f"""## Core Contract

- Follow the workflow phases in order for every task.
- Document evidence and rationale for every recommendation.
- Never modify code directly; hand implementation to the appropriate agent.
- Provide actionable, specific outputs rather than abstract guidance.
- Stay within {agent_name.capitalize()}'s domain; route unrelated requests to the correct agent."""
    return insert_before(content, '## Boundaries', s2)


def add_s1(content, agent_name):
    """Add ## Trigger Guidance after intro paragraph, before first ##."""
    if '## Trigger Guidance' in content:
        return content
    s1 = f"""## Trigger Guidance

Use {agent_name.capitalize()} when the user needs specialized assistance in this agent's domain.

Route elsewhere when the task is primarily handled by another agent."""
    # Insert before the first ## heading
    first_h2 = content.find('\n## ')
    if first_h2 == -1:
        return content
    return content[:first_h2] + '\n\n' + s1 + '\n' + content[first_h2:]


def add_s4_before_output_routing(content, agent_name):
    """Add ## Workflow before ## Output Routing."""
    if '## Workflow' in content:
        return content
    s4 = """## Workflow

`SURVEY -> PLAN -> VERIFY -> PRESENT`

| Phase | Action | Key rule | Read |
|-------|--------|----------|------|
| `SURVEY` | Gather context and requirements | Understand before acting | `references/` |
| `PLAN` | Design approach | Choose output route before working | `references/` |
| `VERIFY` | Validate results | Check against requirements | `references/` |
| `PRESENT` | Deliver results | Include evidence and rationale | `references/` |"""
    marker = '## Output Routing'
    if marker not in content:
        marker = '## Collaboration'
    if marker not in content:
        marker = '## Reference Map'
    if marker not in content:
        return content
    return insert_before(content, marker, s4)


def add_s6_before_collab(content, agent_name):
    """Add ## Output Requirements before ## Collaboration."""
    if '## Output Requirements' in content:
        return content
    s6 = """## Output Requirements

Every deliverable should include:

- Clear scope and context of the analysis or recommendation.
- Evidence-based findings with specific references.
- Actionable next steps with assigned owners.
- Handoff targets for implementation work."""
    marker = '## Collaboration'
    if marker not in content:
        marker = '## Reference Map'
    if marker not in content:
        marker = '## Operational'
    if marker not in content:
        return content
    return insert_before(content, marker, s6)


def add_s7_before_ref(content, agent_name):
    """Add ## Collaboration before ## Reference Map."""
    if '## Collaboration' in content:
        return content
    s7 = f"""## Collaboration

**Receives:** Requirements and context from upstream agents.
**Sends:** Analysis results, recommendations, and implementation requests to downstream agents."""
    return insert_before(content, '## Reference Map', s7)


def add_s9_before_autorun(content, agent_name):
    """Add ## Operational before ## AUTORUN or ## Daily Process."""
    if '## Operational' in content:
        return content
    s9 = f"""## Operational

- Journal domain insights in `.agents/{agent_name}.md`; create it if missing.
- After significant work, append to `.agents/PROJECT.md`: `| YYYY-MM-DD | {agent_name.capitalize()} | (action) | (files) | (outcome) |`
- Standard protocols -> `_common/OPERATIONAL.md`"""
    # Try to insert before Daily Process or AUTORUN
    for marker in ['## Daily Process', '## AUTORUN Support', '## AUTORUN']:
        if marker in content:
            return insert_before(content, marker, s9)
    # Append before the last ---
    return content


def rename_heading(content, old, new):
    """Rename a ## heading."""
    return content.replace(old, new, 1)


def add_h2_collaboration_patterns(content):
    """Add COLLABORATION_PATTERNS to existing HTML comment block."""
    if 'COLLABORATION_PATTERNS' in content:
        return content
    # Find end of HTML comment
    end = content.find('-->')
    if end == -1:
        return content
    insert = "\nCOLLABORATION_PATTERNS:\n- Receives context from upstream agents\n- Sends results to downstream agents\n\nBIDIRECTIONAL_PARTNERS:\n- INPUT: (upstream agents)\n- OUTPUT: (downstream agents)\n"
    return content[:end] + insert + content[end:]


def process_file(filepath, agent_name, fixes):
    """Apply fixes to a SKILL.md file."""
    with open(filepath, 'r') as f:
        content = f.read()
    original = content
    applied = []

    for fix in fixes:
        if fix == 'S2':
            new = add_s2_before_boundaries(content, agent_name)
            if new != content:
                content = new
                applied.append('S2')
        elif fix == 'S1':
            new = add_s1(content, agent_name)
            if new != content:
                content = new
                applied.append('S1')
        elif fix == 'S4':
            new = add_s4_before_output_routing(content, agent_name)
            if new != content:
                content = new
                applied.append('S4')
        elif fix == 'S6':
            new = add_s6_before_collab(content, agent_name)
            if new != content:
                content = new
                applied.append('S6')
        elif fix == 'S7':
            new = add_s7_before_ref(content, agent_name)
            if new != content:
                content = new
                applied.append('S7')
        elif fix == 'S9':
            new = add_s9_before_autorun(content, agent_name)
            if new != content:
                content = new
                applied.append('S9')
        elif fix == 'H2':
            new = add_h2_collaboration_patterns(content)
            if new != content:
                content = new
                applied.append('H2')
        elif fix.startswith('RENAME:'):
            _, old, new_name = fix.split(':', 2)
            new = rename_heading(content, old, new_name)
            if new != content:
                content = new
                applied.append(f'RENAME')

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
    return applied


# Define all fixes needed
FIXES = {
    # S2 only (16 skills)
    'arena': ['S2'],
    'artisan': ['S2'],
    'atlas': ['S2'],
    'attest': ['S2'],
    'beacon': ['S2'],
    'bolt': ['S2'],
    'canon': ['S2'],
    'latch': ['S2'],
    'orbit': ['S2'],
    'rewind': ['S2'],
    'sweep': ['S2'],
    'vision': ['S2'],
    'void': ['S2'],
    'voyager': ['S2'],
    'zen': ['S2'],
    # rally: rename Core Rules + add S1
    'rally': ['RENAME:## Core Rules:## Core Contract', 'S1'],
    # S9 only
    'scribe': ['S9'],
    'sentinel': ['S9'],
    'sherpa': ['S9'],
    # siege: S7 + S9
    'siege': ['S7', 'S9'],
    # reel: rename Framework → Workflow, add S1, S2, S6
    'reel': ['RENAME:## Framework: Script → Set → Record → Deliver:## Workflow', 'S1', 'S2', 'S6'],
    # ripple: rename Core Workflow → Workflow, add S1, S2, S6
    'ripple': ['RENAME:## Core Workflow:## Workflow', 'S1', 'S2', 'S6'],
    # showcase: add S1, S2, S4, S6
    'showcase': ['S1', 'S2', 'S4', 'S6'],
    # triage: rename INCIDENT RESPONSE WORKFLOW → Workflow, rename Output Format → Output Requirements, add S1
    'triage': ['RENAME:## INCIDENT RESPONSE WORKFLOW:## Workflow', 'RENAME:## Output Format:## Output Requirements', 'S1'],
    # titan: H2, S1, S2, S4, S6
    'titan': ['H2', 'S1', 'S2', 'S4', 'S6'],
}


def main():
    total = 0
    for agent_name, fixes in sorted(FIXES.items()):
        filepath = os.path.join(SKILLS_DIR, agent_name, "SKILL.md")
        if not os.path.exists(filepath):
            print(f"SKIP {agent_name}: file not found")
            continue
        applied = process_file(filepath, agent_name, fixes)
        if applied:
            print(f"FIX  {agent_name}: {', '.join(applied)}")
            total += 1
        else:
            print(f"NOOP {agent_name}: no changes needed")
    print(f"\nTotal files fixed: {total}")


if __name__ == "__main__":
    main()
