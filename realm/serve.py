#!/usr/bin/env python3
"""
Realm HQ Map — Live Server
Watches realm-state.md and serves a real-time updating floor plan map.

Usage:
    python3 realm/serve.py              # Start on port 8765
    python3 realm/serve.py --port 9000  # Custom port
"""
import http.server
import json
import hashlib
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PORT = 8765
BASE_DIR = Path(__file__).parent
REPO_DIR = BASE_DIR.parent
TEMPLATE_PATH = BASE_DIR / 'templates' / 'realm-map.html'
AGENTS_DIR = REPO_DIR / '.agents'
STATE_PATH = AGENTS_DIR / 'realm-state.md'

# ============================================
# Static department structure
# ============================================
DEPT_STRUCTURE = {
    "command": {
        "name": "Command Center", "icon": "\u2694", "type": "Executive Suite",
        "ability": {"name": "Grand Strategy", "description": "Can initiate multi-department operations"},
        "all_members": ["Nexus", "Sherpa", "Titan"],
    },
    "frontline": {
        "name": "Frontline", "icon": "\U0001f528", "type": "Development Floor",
        "ability": {"name": "Mass Production", "description": "Parallel build capacity"},
        "all_members": ["Builder", "Forge", "Artisan", "Schema", "Arena", "Architect"],
    },
    "intel": {
        "name": "Intel Corps", "icon": "\U0001f50d", "type": "Research Lab",
        "ability": {"name": "Deep Analysis", "description": "Uncovers hidden connections"},
        "all_members": ["Scout", "Spark", "Compete", "Voice", "Researcher", "Triage", "Rewind"],
    },
    "defense": {
        "name": "Defense", "icon": "\U0001f6e1", "type": "Security Center",
        "ability": {"name": "Shield Wall", "description": "Multi-layer defense"},
        "all_members": ["Sentinel", "Probe", "Radar", "Voyager"],
    },
    "academy": {
        "name": "Academy", "icon": "\U0001f4da", "type": "Training Center",
        "ability": {"name": "Peer Review", "description": "Improves all output quality"},
        "all_members": ["Judge", "Zen", "Sweep", "Warden"],
    },
    "council": {
        "name": "Council", "icon": "\U0001f3db", "type": "Strategy Office",
        "ability": {"name": "Blueprint", "description": "Provides architectural guidance"},
        "all_members": ["Atlas", "Gateway", "Scaffold", "Ripple", "Helm", "Levy"],
    },
    "enchant": {
        "name": "Enchant Hall", "icon": "\u2728", "type": "Design Studio",
        "ability": {"name": "Charm", "description": "Improves user delight"},
        "all_members": ["Vision", "Palette", "Muse", "Flow", "Echo", "Showcase", "Frame"],
    },
    "workshop": {
        "name": "Workshop", "icon": "\u2699", "type": "Infrastructure Lab",
        "ability": {"name": "Automate", "description": "Reduces manual toil"},
        "all_members": ["Gear", "Anvil", "Launch", "Pipe", "Orbit"],
    },
    "observatory": {
        "name": "Observatory", "icon": "\U0001f4ca", "type": "Analytics Lab",
        "ability": {"name": "Foresight", "description": "Data-driven prediction"},
        "all_members": ["Pulse", "Experiment"],
    },
    "herald": {
        "name": "Herald's Tower", "icon": "\U0001f4ef", "type": "Communications",
        "ability": {"name": "Chronicle", "description": "Comprehensive record keeping"},
        "all_members": ["Guardian", "Harvest", "Quill", "Scribe", "Canvas"],
    },
    "pantheon": {
        "name": "Pantheon", "icon": "\U0001f31f", "type": "CTO Office",
        "ability": {"name": "Shape Reality", "description": "Modifies ecosystem itself"},
        "all_members": ["Darwin", "Sigil", "Realm"],
    },
    "outlands": {
        "name": "Outlands", "icon": "\U0001f30d", "type": "Innovation Hub",
        "ability": {"name": "Frontier", "description": "Handles edge cases and new territories"},
        "all_members": ["Horizon", "Polyglot", "Relay", "Growth", "Retain", "Navigator",
                        "Director", "Stream", "Morph", "Specter", "Bard"],
    },
}

# Class → Emoji icon mapping (21 classes)
CLASS_ICONS = {
    "Commander": "⚔️", "Ranger": "🏹", "Artisan": "🔨", "Guardian": "🛡️",
    "Paladin": "⚡", "Sage": "📖", "Alchemist": "⚗️", "Scribe": "✒️",
    "Architect": "📐", "Pioneer": "🚀", "Enchanter": "✨", "Engineer": "⚙️",
    "Merchant": "💰", "Oracle": "🔮", "Herald": "📯", "Demiurge": "🌀",
    "Strategist": "♟️", "Diplomat": "🤝", "Navigator": "🧭", "Transmuter": "💎",
    "Watcher": "👁️",
}

# Agent name → class (for unlisted F-rank agents)
AGENT_CLASS = {
    "Nexus": "Commander", "Sherpa": "Commander", "Titan": "Commander",
    "Builder": "Artisan", "Forge": "Artisan", "Artisan": "Artisan",
    "Schema": "Artisan", "Arena": "Artisan", "Architect": "Demiurge",
    "Scout": "Ranger", "Spark": "Ranger", "Compete": "Ranger",
    "Voice": "Ranger", "Researcher": "Ranger", "Triage": "Ranger", "Rewind": "Ranger",
    "Sentinel": "Paladin", "Probe": "Paladin", "Radar": "Guardian", "Voyager": "Guardian",
    "Judge": "Sage", "Zen": "Sage", "Sweep": "Sage", "Warden": "Sage",
    "Atlas": "Architect", "Gateway": "Architect", "Scaffold": "Engineer",
    "Ripple": "Architect", "Helm": "Strategist", "Levy": "Strategist",
    "Vision": "Enchanter", "Palette": "Enchanter", "Muse": "Enchanter",
    "Flow": "Enchanter", "Echo": "Enchanter", "Showcase": "Enchanter", "Frame": "Enchanter",
    "Gear": "Engineer", "Anvil": "Engineer", "Launch": "Engineer",
    "Pipe": "Engineer", "Orbit": "Engineer",
    "Pulse": "Oracle", "Experiment": "Oracle",
    "Guardian": "Herald", "Harvest": "Herald",
    "Quill": "Scribe", "Scribe": "Scribe", "Canvas": "Scribe",
    "Darwin": "Demiurge", "Sigil": "Demiurge", "Realm": "Demiurge",
    "Horizon": "Pioneer", "Polyglot": "Pioneer",
    "Relay": "Diplomat", "Bard": "Diplomat", "Director": "Navigator",
    "Growth": "Merchant", "Retain": "Merchant", "Navigator": "Navigator",
    "Stream": "Transmuter", "Morph": "Transmuter", "Specter": "Watcher",
}

# Department name → key mapping
DEPT_NAME_TO_KEY = {
    "Command": "command", "Command Center": "command",
    "Frontline": "frontline",
    "Intel": "intel", "Intelligence Corps": "intel",
    "Defense": "defense",
    "Academy": "academy",
    "Council": "council",
    "Enchant Hall": "enchant", "Enchantment Hall": "enchant",
    "Workshop": "workshop",
    "Observatory": "observatory",
    "Herald's Tower": "herald", "Herald": "herald",
    "Pantheon": "pantheon",
    "Outlands": "outlands",
}

ROADS = [
    {"from": "command", "to": "frontline", "type": "allied"},
    {"from": "command", "to": "intel", "type": "allied"},
    {"from": "intel", "to": "defense", "type": "allied"},
    {"from": "academy", "to": "frontline", "type": "cooperative"},
    {"from": "council", "to": "command", "type": "advisory"},
    {"from": "enchant", "to": "frontline", "type": "cooperative"},
    {"from": "workshop", "to": "frontline", "type": "support"},
    {"from": "pantheon", "to": "command", "type": "oversight"},
    {"from": "workshop", "to": "defense", "type": "support"},
    {"from": "observatory", "to": "intel", "type": "cooperative"},
    {"from": "herald", "to": "command", "type": "cooperative"},
    {"from": "outlands", "to": "intel", "type": "cooperative"},
]

EVENT_ICONS = {
    "Character Introduction": "\U0001f31f",
    "Kingdom Restructuring": "\u2694",
    "Mass Upgrade": "\U0001f527",
    "Era Shift": "\U0001f680",
}

# File path prefix → department mapping (for activity attribution)
PATH_TO_DEPT = {
    "nexus/": "command", "sherpa/": "command", "titan/": "command",
    "builder/": "frontline", "forge/": "frontline", "artisan/": "frontline",
    "schema/": "frontline", "arena/": "frontline", "architect/": "frontline",
    "scout/": "intel", "spark/": "intel", "compete/": "intel",
    "voice/": "intel", "researcher/": "intel", "triage/": "intel", "rewind/": "intel",
    "sentinel/": "defense", "probe/": "defense", "radar/": "defense", "voyager/": "defense",
    "judge/": "academy", "zen/": "academy", "sweep/": "academy", "warden/": "academy",
    "atlas/": "council", "gateway/": "council", "scaffold/": "council",
    "ripple/": "council", "helm/": "council", "levy/": "council",
    "vision/": "enchant", "palette/": "enchant", "muse/": "enchant",
    "flow/": "enchant", "echo/": "enchant", "showcase/": "enchant", "frame/": "enchant",
    "gear/": "workshop", "anvil/": "workshop", "launch/": "workshop",
    "pipe/": "workshop", "orbit/": "workshop",
    "pulse/": "observatory", "experiment/": "observatory",
    "guardian/": "herald", "harvest/": "herald", "quill/": "herald",
    "scribe/": "herald", "canvas/": "herald",
    "darwin/": "pantheon", "sigil/": "pantheon", "realm/": "pantheon",
    "horizon/": "outlands", "polyglot/": "outlands", "relay/": "outlands",
    "growth/": "outlands", "retain/": "outlands", "navigator/": "outlands",
    "director/": "outlands", "stream/": "outlands", "morph/": "outlands",
    "specter/": "outlands", "bard/": "outlands",
    "_common/": "pantheon", ".agents/": "pantheon",
}

# Conventional commit scope → agent name
SCOPE_TO_AGENT = {name.lower(): name for name in AGENT_CLASS}

# Journal change tracking
_journal_mtimes = {}


# ============================================
# Activity collection
# ============================================
def get_recent_commits(since_minutes=5):
    """Parse recent git commits and map to agents/departments."""
    try:
        result = subprocess.run(
            ['git', 'log', f'--since={since_minutes} minutes ago',
             '--oneline', '--no-merges', '--format=%h|%s|%ar'],
            cwd=str(REPO_DIR), capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            return []
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []

    items = []
    active_depts = set()
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        parts = line.split('|', 2)
        if len(parts) < 3:
            continue
        sha, subject, time_ago = parts

        # Extract scope from conventional commit: type(scope): message
        agent = None
        dept = None
        scope_match = re.match(r'\w+\((\w+)\):', subject)
        if scope_match:
            scope = scope_match.group(1).lower()
            agent = SCOPE_TO_AGENT.get(scope)
            if agent:
                # Find department for this agent
                for dk, ds in DEPT_STRUCTURE.items():
                    if agent in ds['all_members']:
                        dept = dk
                        break

        if dept:
            active_depts.add(dept)

        icon = '\U0001f4e6' if 'feat' in subject[:8] else (
            '\U0001f41b' if 'fix' in subject[:8] else '\U0001f527')
        prefix = f"[{agent}] " if agent else ""
        items.append({
            'icon': icon,
            'text': f"{prefix}{subject[:60]}",
            'time': time_ago,
            'type': 'commit',
        })

    return items, active_depts


def get_journal_changes():
    """Detect changes to .agents/*.md journal files."""
    global _journal_mtimes
    items = []
    active_depts = set()

    if not AGENTS_DIR.exists():
        return items, active_depts

    for md_file in AGENTS_DIR.glob('*.md'):
        name = md_file.stem  # e.g., "builder", "nexus"
        try:
            mtime = md_file.stat().st_mtime
        except OSError:
            continue

        old_mtime = _journal_mtimes.get(name, 0)
        if old_mtime > 0 and mtime > old_mtime:
            agent = SCOPE_TO_AGENT.get(name.lower())
            display_name = agent if agent else name.capitalize()
            items.append({
                'icon': '\U0001f4dd',
                'text': f"{display_name} journal updated",
                'time': datetime.fromtimestamp(mtime).strftime('%H:%M:%S'),
                'type': 'journal',
            })
            for dk, ds in DEPT_STRUCTURE.items():
                if display_name in ds['all_members']:
                    active_depts.add(dk)
                    break

        _journal_mtimes[name] = mtime

    return items, active_depts


def get_file_changes():
    """Detect uncommitted file changes via git status."""
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain', '--no-renames'],
            cwd=str(REPO_DIR), capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            return [], set()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return [], set()

    items = []
    active_depts = set()
    seen_depts = set()

    for line in result.stdout.strip().split('\n'):
        if not line or len(line) < 4:
            continue
        status = line[:2].strip()
        filepath = line[3:]

        # Map file to department
        dept = None
        for prefix, dk in PATH_TO_DEPT.items():
            if filepath.startswith(prefix):
                dept = dk
                break

        if dept and dept not in seen_depts:
            seen_depts.add(dept)
            active_depts.add(dept)
            dept_name = DEPT_STRUCTURE.get(dept, {}).get('name', dept)
            status_label = {'M': 'modified', 'A': 'added', '?': 'new',
                            'D': 'deleted'}.get(status, 'changed')
            items.append({
                'icon': '\U0001f4c1',
                'text': f"{dept_name}: files {status_label}",
                'time': 'now',
                'type': 'file_change',
            })

    return items, active_depts


def collect_activity():
    """Aggregate all activity sources."""
    all_items = []
    all_depts = set()

    commit_items, commit_depts = get_recent_commits()
    all_items.extend(commit_items)
    all_depts.update(commit_depts)

    journal_items, journal_depts = get_journal_changes()
    all_items.extend(journal_items)
    all_depts.update(journal_depts)

    file_items, file_depts = get_file_changes()
    all_items.extend(file_items)
    all_depts.update(file_depts)

    return {
        'items': all_items[:30],
        'active_depts': list(all_depts),
        'ts': datetime.now().isoformat(),
    }

# ============================================
# Stat generation (deterministic)
# ============================================
def auto_stats(cls, xp):
    import random as _r
    _r.seed(hash(cls + str(xp)) & 0xFFFFFFFF)
    base = min(85, max(12, 20 + xp // 20))
    boosts = {
        "Commander": "cha", "Ranger": "int", "Artisan": "str",
        "Guardian": "con", "Paladin": "int", "Sage": "wis",
        "Alchemist": "dex", "Scribe": "wis", "Architect": "int",
        "Enchanter": "cha", "Engineer": "con", "Merchant": "cha",
        "Oracle": "wis", "Herald": "dex", "Demiurge": "wis",
        "Strategist": "int", "Diplomat": "cha", "Pioneer": "dex",
        "Navigator": "dex", "Transmuter": "str", "Watcher": "int",
    }
    primary = boosts.get(cls, "str")
    s = {}
    for k in ["str", "dex", "int", "wis", "cha", "con"]:
        v = base + _r.randint(-12, 8)
        if k == primary:
            v += 18
        s[k] = min(99, max(8, v))
    return s


# ============================================
# Markdown table parser
# ============================================
def parse_md_table(content, section_header):
    pattern = rf'^##\s+{re.escape(section_header)}\s*$'
    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        return []

    lines = content[match.end():].split('\n')
    rows = []
    headers = None
    for line in lines:
        line = line.strip()
        if not line.startswith('|'):
            if headers is not None and line and not line.startswith('_'):
                break
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if all(set(c) <= set('-| :') for c in cells):
            continue
        if headers is None:
            headers = cells
        else:
            if len(cells) == len(headers):
                rows.append(dict(zip(headers, cells)))
    return rows


# ============================================
# State parser
# ============================================
def parse_realm_state():
    if not STATE_PATH.exists():
        return None
    content = STATE_PATH.read_text()

    kingdom_table = parse_md_table(content, "Kingdom Overview")
    kingdom_raw = {row.get('Field', ''): row.get('Value', '') for row in kingdom_table}

    agents = parse_md_table(content, "Agent Characters")
    quests = parse_md_table(content, "Recent Quests")
    events = parse_md_table(content, "Current Events")
    badges = parse_md_table(content, "Badges Earned")

    return {
        'kingdom_raw': kingdom_raw,
        'agents': agents,
        'quests': quests,
        'events': events,
        'badges': badges,
    }


def extract_number(s):
    m = re.search(r'(\d+)', s)
    return int(m.group(1)) if m else 0


def extract_grade(s):
    m = re.search(r'\(([A-Z+\-]+)\)', s)
    return m.group(1) if m else '?'


def health_display(score):
    if score >= 80:
        return "thriving", "Thriving", "\U0001f49a"
    elif score >= 60:
        return "stable", "Stable", "\U0001f49b"
    elif score >= 40:
        return "strained", "Strained", "\U0001f7e0"
    else:
        return "critical", "Critical", "\U0001f534"


def calculate_health(members):
    if not members:
        return 30
    ranked = [m for m in members if m['rank'] not in ('F',)]
    activity_ratio = len(ranked) / len(members) if members else 0
    if activity_ratio >= 0.75:
        factor = 1.0
    elif activity_ratio >= 0.5:
        factor = 0.9
    elif activity_ratio >= 0.25:
        factor = 0.7
    else:
        factor = 0.5
    avg_xp = sum(m['xp'] for m in members) / len(members)
    base = min(95, 40 + avg_xp / 15)
    return int(base * factor)


# ============================================
# Build REALM_DATA
# ============================================
def build_realm_data(state=None):
    if state is None:
        state = parse_realm_state()
    if state is None:
        return _default_realm_data()

    kr = state['kingdom_raw']
    kingdom = {
        'name': 'The Realm',
        'efs': extract_number(kr.get('EFS (estimated)', '~50')),
        'efsGrade': extract_grade(kr.get('EFS (estimated)', '(?)')),
        'phase': kr.get('Phase', 'UNKNOWN'),
        'totalAgents': extract_number(kr.get('Total Agents', '0')),
        'activeQuests': extract_number(kr.get('Active Quests', '0')),
        'lastUpdated': datetime.now().strftime('%Y-%m-%d %H:%M'),
    }

    # Group parsed agents by department
    dept_agents = {}
    for a in state['agents']:
        dept_name = a.get('Department', '')
        dept_key = DEPT_NAME_TO_KEY.get(dept_name, None)
        if dept_key is None:
            for k, v in DEPT_NAME_TO_KEY.items():
                if k.lower() in dept_name.lower():
                    dept_key = v
                    break
        if dept_key is None:
            dept_key = 'outlands'

        try:
            xp = int(a.get('XP', '0'))
        except ValueError:
            xp = 0

        dept_agents.setdefault(dept_key, []).append({
            'name': a.get('Agent', ''),
            'class': a.get('Class', 'Artisan'),
            'rank': a.get('Rank', 'F'),
            'xp': xp,
            'isChief': a.get('Chief', 'No') == 'Yes',
        })

    # Fill in missing F-rank agents from structure
    for dept_key, struct in DEPT_STRUCTURE.items():
        known = {m['name'] for m in dept_agents.get(dept_key, [])}
        for name in struct['all_members']:
            if name not in known:
                dept_agents.setdefault(dept_key, []).append({
                    'name': name,
                    'class': AGENT_CLASS.get(name, 'Artisan'),
                    'rank': 'F',
                    'xp': 50,
                    'isChief': False,
                })

    # Build department objects
    departments = {}
    for dept_key, struct in DEPT_STRUCTURE.items():
        agents = dept_agents.get(dept_key, [])
        members = []
        for a in agents:
            members.append({
                **a,
                'classColor': f"var(--class-{a['class'].lower()})",
                'classIcon': CLASS_ICONS.get(a['class'], '👤'),
                'stats': auto_stats(a['class'], a['xp']),
            })

        # Sort: chiefs first, then by XP descending
        members.sort(key=lambda m: (-int(m['isChief']), -m['xp']))

        chief = next((m for m in members if m['isChief']), members[0] if members else None)
        health = calculate_health(members)
        h_status, h_label, h_icon = health_display(health)

        departments[dept_key] = {
            'name': struct['name'],
            'icon': struct['icon'],
            'type': struct['type'],
            'chief': chief['name'] if chief else 'None',
            'chiefRank': chief['rank'] if chief else 'F',
            'health': health,
            'healthStatus': h_status,
            'healthLabel': h_label,
            'healthIcon': h_icon,
            'ability': struct['ability'],
            'members': members,
        }

    # Quests
    quests = []
    rarity_map = {'Common': 'common', 'Uncommon': 'uncommon', 'Rare': 'rare',
                  'Epic': 'epic', 'Legendary': 'legendary'}
    for q in state.get('quests', []):
        status = q.get('Status', 'Complete')
        quests.append({
            'name': q.get('Quest', ''),
            'rarity': rarity_map.get(q.get('Rarity', ''), 'common'),
            'progress': 100 if 'Complete' in status else (0 if 'Failed' in status else 50),
            'party': [p.strip() for p in q.get('Party', '').split(',')],
        })

    # Events
    events = []
    for e in state.get('events', []):
        icon = EVENT_ICONS.get(e.get('Type', ''), '\U0001f4cc')
        events.append({
            'icon': icon,
            'text': e.get('Event', ''),
            'date': e.get('Date', ''),
        })

    # Conversations (generated from active agents)
    conversations = _generate_conversations(departments)

    return {
        'kingdom': kingdom,
        'departments': departments,
        'roads': ROADS,
        'events': events,
        'quests': quests,
        'conversations': conversations,
    }


def _generate_conversations(departments):
    phrases = {
        "command": ["Chain coordination complete", "Routing agents", "Strategy updated"],
        "frontline": ["Build pipeline green", "Feature shipped", "Code merged"],
        "intel": ["Root cause identified", "Pattern found", "Analysis complete"],
        "defense": ["Security scan clear", "All tests passing", "Vulnerabilities: 0"],
        "academy": ["Code clarity improved", "Review approved", "Standards met"],
        "council": ["Architecture aligned", "Blueprint updated", "Schema migrated"],
        "enchant": ["UI patterns updated", "Design tokens synced", "A11y check passed"],
        "workshop": ["Pipeline optimized", "Infra provisioned", "Loop runner deployed"],
        "observatory": ["Metrics dashboard ready", "KPIs on track", "Experiment launched"],
        "herald": ["PR quality A+", "Changelog updated", "Release notes ready"],
        "pantheon": ["EFS scan scheduled", "Ecosystem evolving", "Meta-patterns found"],
        "outlands": ["Stakeholder sync done", "i18n coverage up", "Browser tests pass"],
    }
    convos = []
    for dept_key, dept in departments.items():
        if dept.get('members'):
            chief = next((m for m in dept['members'] if m.get('isChief')), dept['members'][0])
            msgs = phrases.get(dept_key, ["Working..."])
            import random as _r
            _r.seed(hash(chief['name']) & 0xFFFFFFFF)
            convos.append({
                'agent': chief['name'],
                'message': _r.choice(msgs),
                'dept': dept_key,
            })
    return convos


def _default_realm_data():
    return {
        'kingdom': {'name': 'The Realm', 'efs': 50, 'efsGrade': 'C',
                     'phase': 'UNKNOWN', 'totalAgents': 0, 'activeQuests': 0,
                     'lastUpdated': datetime.now().strftime('%Y-%m-%d %H:%M')},
        'departments': {},
        'roads': ROADS,
        'events': [],
        'quests': [],
        'conversations': [],
    }


# ============================================
# HTML generation (template replacement)
# ============================================
def make_agent_avatar_html(m):
    import html as _h
    rank_lc = m['rank'].lower()
    cls_lc = m['class'].lower()
    icon = m.get('classIcon', CLASS_ICONS.get(m['class'], '👤'))
    title = f"{m['name']} [{m['rank']}] {m['class']}"
    tooltip = {'name': m['name'], 'class': m['class'], 'rank': m['rank'],
               'xp': m['xp'], 'classIcon': icon}
    if m.get('isChief'):
        tooltip['isChief'] = True
    j = json.dumps(tooltip, ensure_ascii=False)
    je = j.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
    chief_html = '<span class="chief-crown">👑</span>' if m.get('isChief') else ''
    return (f'<div class="agent-avatar rank-{rank_lc}" '
            f'title="{_h.escape(title)}" '
            f'onmouseenter="showAgentTooltip(event, {je})" '
            f'onmouseleave="hideTooltip()">'
            f'<span class="avatar-icon">{icon}</span>'
            f'<span class="avatar-name">{_h.escape(m["name"])}</span>'
            f'{chief_html}'
            f'</div>')


def make_event_ticker_html(events):
    import html as _h
    items = []
    for ev in events:
        items.append(
            f'<div class="event-ticker__item">'
            f'<span class="event-ticker__item-icon">{ev["icon"]}</span>'
            f'<span class="event-ticker__item-text">{_h.escape(ev["text"])}</span>'
            f'<span class="event-ticker__item-date">{ev["date"]}</span>'
            f'</div>')
    return '\n      '.join(items)


def generate_html(data):
    template = TEMPLATE_PATH.read_text()

    k = data['kingdom']
    efs_level = 'high' if k['efs'] >= 70 else ('mid' if k['efs'] >= 40 else 'low')

    replacements = {
        '{{KINGDOM_ICON}}': '\U0001f3f0',
        '{{EFS_SCORE}}': str(k['efs']),
        '{{EFS_GRADE}}': k['efsGrade'],
        '{{EFS_PERCENT}}': str(k['efs']),
        '{{EFS_LEVEL}}': efs_level,
        '{{PHASE}}': k['phase'],
        '{{AGENT_TOTAL}}': str(k['totalAgents']),
        '{{QUEST_ACTIVE}}': str(k['activeQuests']),
        '{{LAST_UPDATED}}': k['lastUpdated'],
    }

    for dept_key, dept in data['departments'].items():
        D = dept_key.upper()
        replacements[f'{{{{DEPT_{D}_ICON}}}}'] = dept['icon']
        replacements[f'{{{{DEPT_{D}_CHIEF}}}}'] = dept['chief']
        replacements[f'{{{{DEPT_{D}_CHIEF_RANK}}}}'] = dept['chiefRank']
        replacements[f'{{{{DEPT_{D}_CHIEF_RANK_LC}}}}'] = dept['chiefRank'].lower()
        replacements[f'{{{{DEPT_{D}_HEALTH}}}}'] = str(dept['health'])
        replacements[f'{{{{DEPT_{D}_HEALTH_STATUS}}}}'] = dept['healthStatus']
        replacements[f'{{{{DEPT_{D}_HEALTH_LABEL}}}}'] = dept['healthLabel']
        replacements[f'{{{{DEPT_{D}_HEALTH_ICON}}}}'] = dept['healthIcon']
        avatars = '\n            '.join(make_agent_avatar_html(m) for m in dept['members'])
        replacements[f'{{{{DEPT_{D}_AGENTS}}}}'] = avatars

    replacements['{{EVENT_TICKER_ITEMS}}'] = make_event_ticker_html(data.get('events', []))
    replacements['{{REALM_DATA_JSON}}'] = json.dumps(data, ensure_ascii=False, indent=2)

    html = template
    for k, v in replacements.items():
        html = html.replace(k, v)
    return html


# ============================================
# Cache layer
# ============================================
_cache = {'html': None, 'data': None, 'hash': None, 'mtime': 0}


def get_cached():
    try:
        mtime = os.path.getmtime(STATE_PATH) if STATE_PATH.exists() else 0
    except OSError:
        mtime = 0

    if mtime != _cache['mtime'] or _cache['data'] is None:
        data = build_realm_data()
        data_json = json.dumps(data, ensure_ascii=False, sort_keys=True)
        _cache['data'] = data
        _cache['hash'] = hashlib.md5(data_json.encode()).hexdigest()[:12]
        _cache['html'] = generate_html(data)
        _cache['mtime'] = mtime

    return _cache


# ============================================
# HTTP Server
# ============================================
class RealmHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self._serve_html()
        elif self.path == '/api/data':
            self._serve_json()
        elif self.path == '/api/hash':
            self._serve_hash()
        elif self.path == '/api/activity':
            self._serve_activity()
        else:
            self.send_error(404)

    def _serve_html(self):
        cache = get_cached()
        content = cache['html'].encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(content))
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(content)

    def _serve_json(self):
        cache = get_cached()
        content = json.dumps(cache['data'], ensure_ascii=False, indent=2).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(content))
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(content)

    def _serve_hash(self):
        cache = get_cached()
        body = json.dumps({'hash': cache['hash'], 'ts': datetime.now().isoformat()}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def _serve_activity(self):
        data = collect_activity()
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        first = str(args[0]) if args else ''
        if '/api/hash' not in first:
            super().log_message(fmt, *args)


# ============================================
# Main
# ============================================
def main():
    port = PORT
    if '--port' in sys.argv:
        idx = sys.argv.index('--port')
        if idx + 1 < len(sys.argv):
            port = int(sys.argv[idx + 1])

    if not TEMPLATE_PATH.exists():
        print(f"Error: Template not found at {TEMPLATE_PATH}")
        sys.exit(1)

    print(f"\n  \U0001f3f0 Realm HQ Map — Live Server")
    print(f"  {'=' * 40}")
    print(f"  URL:       http://localhost:{port}")
    print(f"  Template:  {TEMPLATE_PATH}")
    print(f"  State:     {STATE_PATH}")
    print(f"  Status:    {'Watching' if STATE_PATH.exists() else 'No state file (will use defaults)'}")
    print(f"  {'=' * 40}")
    print(f"  Press Ctrl+C to stop\n")

    server = http.server.HTTPServer(('', port), RealmHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
        server.server_close()


if __name__ == '__main__':
    main()
