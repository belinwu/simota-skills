#!/usr/bin/env python3
"""
Fix quality issues found in normalization verification:
- F1: Capitalize name: field in frontmatter
- S3: Convert **Always**/**Ask first**/**Never** to ### subheaders
- S4: Add Read column to Workflow tables missing it
"""

import re
import os
import glob

SKILLS_DIR = "/Users/simota/.claude/skills"
SKIP = {"_common", "_scripts", "_templates"}


def fix_f1_name(content):
    """Capitalize the name: field in frontmatter."""
    def capitalize_name(m):
        name = m.group(1)
        return f"name: {name[0].upper()}{name[1:]}"

    return re.sub(r'^name: ([a-z])', lambda m: f"name: {m.group(1).upper()}", content, count=1, flags=re.MULTILINE)


def fix_s3_boundaries(content):
    """Convert **Always**/**Ask first**/**Never** to ### subheaders."""
    # Handle **Always** or **Always:**
    content = re.sub(r'^\*\*Always:?\*\*\s*$', '### Always', content, flags=re.MULTILINE)
    content = re.sub(r'^\*\*Ask first:?\*\*\s*$', '### Ask First', content, flags=re.MULTILINE)
    content = re.sub(r'^\*\*Ask First:?\*\*\s*$', '### Ask First', content, flags=re.MULTILINE)
    content = re.sub(r'^\*\*Never:?\*\*\s*$', '### Never', content, flags=re.MULTILINE)

    return content


def fix_s4_workflow(content):
    """Add Read column to Workflow tables missing it."""
    # Find workflow section
    workflow_match = re.search(r'(## Workflow.*?)(?=\n## |\Z)', content, re.DOTALL)
    if not workflow_match:
        return content

    section = workflow_match.group(1)

    # Check if already has Read column
    if '| Read' in section or '|Read' in section:
        return content

    # Find table in section - look for | Phase | or | Step | patterns
    # Add Read column to header and separator, and empty Read to data rows
    lines = section.split('\n')
    new_lines = []
    in_table = False
    header_found = False

    for line in lines:
        if '|' in line and not in_table and not header_found:
            # Check if this looks like a table header
            if re.match(r'\s*\|.*\|.*\|', line):
                in_table = True
                header_found = True
                # Add Read column to header
                line = line.rstrip()
                if line.endswith('|'):
                    line = line[:-1] + ' Read |'
                else:
                    line = line + ' | Read |'
                new_lines.append(line)
                continue

        if in_table and re.match(r'\s*\|[\s-]+\|', line):
            # Separator row
            line = line.rstrip()
            if line.endswith('|'):
                line = line[:-1] + '------|'
            else:
                line = line + '------|'
            new_lines.append(line)
            continue

        if in_table and line.startswith('|'):
            # Data row
            line = line.rstrip()
            if line.endswith('|'):
                line = line[:-1] + ' `references/` |'
            else:
                line = line + ' `references/` |'
            new_lines.append(line)
            continue

        if in_table and not line.startswith('|') and line.strip() != '':
            in_table = False

        new_lines.append(line)

    new_section = '\n'.join(new_lines)
    content = content[:workflow_match.start()] + new_section + content[workflow_match.end():]
    return content


def process_file(filepath):
    """Process a single SKILL.md file."""
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    changes = []

    # F1: Capitalize name
    new_content = fix_f1_name(content)
    if new_content != content:
        content = new_content
        changes.append('F1')

    # S3: Fix boundaries format
    new_content = fix_s3_boundaries(content)
    if new_content != content:
        content = new_content
        changes.append('S3')

    # S4: Add Read column
    new_content = fix_s4_workflow(content)
    if new_content != content:
        content = new_content
        changes.append('S4')

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return changes
    return []


def main():
    total = 0
    for d in sorted(os.listdir(SKILLS_DIR)):
        if d in SKIP or d.startswith('_') or d.startswith('.'):
            continue
        filepath = os.path.join(SKILLS_DIR, d, "SKILL.md")
        if not os.path.exists(filepath):
            continue

        changes = process_file(filepath)
        if changes:
            print(f"FIX  {d}: {', '.join(changes)}")
            total += 1
        # Don't print SKIP for clean files

    print(f"\nTotal files fixed: {total}")


if __name__ == "__main__":
    main()
