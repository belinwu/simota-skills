/* ============================================================
 * Realm Directory — App JS
 * Vanilla JS, no framework. Modules:
 *   1. Theme toggle (data-theme + localStorage)
 *   2. Data loader (fetch with inline-JSON fallback for file://)
 *   3. Portrait SVG placeholder generator (class symbol + name + pending mark)
 *   4. Component renderers (AgentCard, FilterChip, RankPill, AffinityStrip,
 *      Breadcrumb, CollaborationGraph)
 *   5. Search index (includes-based scoring)
 *   6. Filter state (URL-synced; AND across axes / OR within axis)
 *   7. Page bootstraps (index, category, detail, search) — selected via
 *      <body data-page="...">
 * ============================================================ */

(() => {
  'use strict';

  /* ---------- 1. Theme ---------- */
  const Theme = {
    KEY: 'realm-theme',
    init() {
      const saved = localStorage.getItem(this.KEY);
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const theme = saved || (prefersDark ? 'dark' : 'light');
      this.set(theme);
      const btn = document.querySelector('[data-theme-toggle]');
      if (btn) {
        btn.addEventListener('click', () => {
          const current = document.documentElement.getAttribute('data-theme');
          this.set(current === 'dark' ? 'light' : 'dark');
        });
        this.updateBtn(btn);
      }
    },
    set(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem(this.KEY, theme);
      const btn = document.querySelector('[data-theme-toggle]');
      if (btn) this.updateBtn(btn);
    },
    updateBtn(btn) {
      const t = document.documentElement.getAttribute('data-theme');
      btn.setAttribute('aria-pressed', t === 'dark');
      btn.querySelector('[data-theme-label]').textContent = t === 'dark' ? 'Dark' : 'Light';
    }
  };

  /* ---------- 2. Data loader ---------- */
  const DataStore = {
    cache: null,
    async load() {
      if (this.cache) return this.cache;
      // Inline fallback for file:// runs (browsers block fetch)
      const inline = document.getElementById('agents-index-fallback');
      try {
        const res = await fetch('assets/data/agents.index.json', { cache: 'no-cache' });
        if (!res.ok) throw new Error('http ' + res.status);
        this.cache = await res.json();
      } catch (err) {
        if (inline) {
          try {
            this.cache = JSON.parse(inline.textContent);
          } catch (e) {
            console.error('Inline fallback parse failed', e);
            this.cache = { agents: [] };
          }
        } else {
          console.warn('agents.index.json fetch failed; no inline fallback present', err);
          this.cache = { agents: [] };
        }
      }
      return this.cache;
    },
    async loadAgent(name) {
      try {
        const res = await fetch(`assets/data/agents/${name}.json`, { cache: 'no-cache' });
        if (!res.ok) throw new Error('http ' + res.status);
        return await res.json();
      } catch (err) {
        // Fall back to index entry
        const idx = await this.load();
        return idx.agents.find(a => a.name === name) || null;
      }
    }
  };

  /* ---------- Static taxonomy (mirrored for offline file:// use) ---------- */
  const TAXONOMY = {
    classes: {
      commander:       { label: 'Commander',  symbol: 'crown',    archetype: 'Strategic leader',   passive: 'Rally',         bonus: '+10% CHA on chain coordination' },
      ranger:          { label: 'Ranger',     symbol: 'compass',  archetype: 'Scout and tracker',  passive: 'Track',         bonus: '+10% INT on investigation tasks' },
      artisan:         { label: 'Artisan',    symbol: 'hammer',   archetype: 'Master crafter',     passive: 'Forge',         bonus: '+10% STR on code generation tasks' },
      guardian:        { label: 'Guardian',   symbol: 'shield',   archetype: 'Shield bearer',      passive: 'Shield Wall',   bonus: '+10% CON on test tasks' },
      paladin:         { label: 'Paladin',    symbol: 'sun',      archetype: 'Holy warrior',       passive: 'Purify',        bonus: '+10% INT on security tasks' },
      sage:            { label: 'Sage',       symbol: 'eye',      archetype: 'Wise elder',         passive: 'Discern',       bonus: '+10% WIS on review tasks' },
      alchemist:       { label: 'Alchemist',  symbol: 'flask',    archetype: 'Transmuter',         passive: 'Transmute',     bonus: '+10% DEX on optimization tasks' },
      scribe:          { label: 'Scribe',     symbol: 'quill',    archetype: 'Lorekeeper',         passive: 'Chronicle',     bonus: '+10% WIS on documentation tasks' },
      'architect-class':{ label: 'Architect', symbol: 'ruler',    archetype: 'Master builder',     passive: 'Blueprint',     bonus: '+10% INT on design tasks' },
      enchanter:       { label: 'Enchanter',  symbol: 'star',     archetype: 'Illusionist',        passive: 'Charm',         bonus: '+10% CHA on UX tasks' },
      engineer:        { label: 'Engineer',   symbol: 'gear',     archetype: 'Siege engineer',     passive: 'Automate',      bonus: '+10% CON on infrastructure tasks' },
      merchant:        { label: 'Merchant',   symbol: 'coin',     archetype: 'Trader',             passive: 'Trade',         bonus: '+10% CHA on growth tasks' },
      oracle:          { label: 'Oracle',     symbol: 'orb',      archetype: 'Seer',               passive: 'Foresight',     bonus: '+10% WIS on analytics tasks' },
      herald:          { label: 'Herald',     symbol: 'horn',     archetype: 'Messenger',          passive: 'Proclaim',      bonus: '+10% DEX on version-control tasks' },
      demiurge:        { label: 'Demiurge',   symbol: 'world',    archetype: 'World shaper',       passive: 'Shape Reality', bonus: '+10% WIS on ecosystem tasks' },
      strategist:      { label: 'Strategist', symbol: 'chess',    archetype: 'War council',        passive: 'Stratagem',     bonus: '+10% INT on strategy tasks' },
      diplomat:        { label: 'Diplomat',   symbol: 'bridge',   archetype: 'Ambassador',         passive: 'Bridge',        bonus: '+10% CHA on integration tasks' },
      pioneer:         { label: 'Pioneer',    symbol: 'flag',     archetype: 'Explorer',           passive: 'Trailblaze',    bonus: '+10% DEX on migration tasks' },
      navigator:       { label: 'Navigator',  symbol: 'map',      archetype: 'Cartographer',       passive: 'Chart',         bonus: '+10% DEX on browser tasks' },
      transmuter:      { label: 'Transmuter', symbol: 'prism',    archetype: 'Material converter', passive: 'Refine',        bonus: '+10% STR on data-processing tasks' },
      watcher:         { label: 'Watcher',    symbol: 'moon',     archetype: 'Night sentinel',     passive: 'Vigil',         bonus: '+10% INT on concurrency tasks' }
    },
    categories: {
      orchestration:   { label: 'Orchestration',  trait: 'Party coordination'   },
      investigation:   { label: 'Investigation',  trait: 'Keen observation'     },
      implementation:  { label: 'Implementation', trait: 'Code forging'         },
      testing:         { label: 'Testing',        trait: 'Defect detection'     },
      security:        { label: 'Security',       trait: 'Threat purging'       },
      review:          { label: 'Review',         trait: 'Pattern recognition'  },
      performance:     { label: 'Performance',    trait: 'Speed enhancement'    },
      documentation:   { label: 'Documentation',  trait: 'Knowledge recording'  },
      architecture:    { label: 'Architecture',   trait: 'Structural design'    },
      'ux-design':     { label: 'UX/Design',      trait: 'User enchantment'     },
      devops:          { label: 'DevOps',         trait: 'Automation mastery'   },
      growth:          { label: 'Growth',         trait: 'Value amplification'  },
      analytics:       { label: 'Analytics',      trait: 'Future insight'       },
      'git-pr':        { label: 'Git/PR',         trait: 'Change announcement'  },
      'meta-tooling':  { label: 'Meta/Tooling',   trait: 'Ecosystem evolution'  },
      strategy:        { label: 'Strategy',       trait: 'Long-term planning'   },
      communication:   { label: 'Communication',  trait: 'Bridge building'      },
      modernization:   { label: 'Modernization',  trait: 'New frontier discovery' },
      browser:         { label: 'Browser',        trait: 'Path finding'         },
      data:            { label: 'Data',           trait: 'Format transformation' },
      incident:        { label: 'Incident',       trait: 'Anomaly detection'    }
    },
    affinities: {
      saas:      { label: 'SaaS',       symbol: 'stacked-cards' },
      ecommerce: { label: 'E-commerce', symbol: 'shopping-bag'  },
      mobile:    { label: 'Mobile',     symbol: 'smartphone'    },
      dashboard: { label: 'Dashboard',  symbol: 'gauge'         },
      marketing: { label: 'Marketing',  symbol: 'megaphone'     },
      game:      { label: 'Game',       symbol: 'controller'    }
    },
    ranks: {
      F:  { title: 'Recruit'    },
      E:  { title: 'Novice'     },
      D:  { title: 'Apprentice' },
      C:  { title: 'Journeyman' },
      B:  { title: 'Veteran'    },
      A:  { title: 'Elite'      },
      S:  { title: 'Champion'   },
      SS: { title: 'Legend'     }
    }
  };

  /* ---------- 3. Class symbol SVG paths (geometric, monochrome) ---------- */
  const ClassSymbol = {
    star:    '<path d="M50 18 L58 40 L82 40 L62 54 L70 76 L50 62 L30 76 L38 54 L18 40 L42 40 Z" />',
    hammer:  '<path d="M28 30 H72 V46 H58 V82 H42 V46 H28 Z" />',
    ruler:   '<path d="M22 36 H78 V58 H22 Z M30 36 V46 M40 36 V42 M50 36 V46 M60 36 V42 M70 36 V46" stroke="currentColor" stroke-width="2" fill="none"/>',
    eye:     '<path d="M16 50 Q50 22 84 50 Q50 78 16 50 Z" fill="none" stroke="currentColor" stroke-width="3"/><circle cx="50" cy="50" r="10" />',
    compass: '<circle cx="50" cy="50" r="28" fill="none" stroke="currentColor" stroke-width="3"/><path d="M50 28 L56 52 L50 72 L44 52 Z" />',
    crown:   '<path d="M22 60 L30 36 L42 52 L50 30 L58 52 L70 36 L78 60 Z M22 64 H78 V72 H22 Z" />',
    shield:  '<path d="M50 20 L78 30 V52 Q78 72 50 82 Q22 72 22 52 V30 Z" fill="none" stroke="currentColor" stroke-width="3"/><path d="M50 38 V64 M38 50 H62" stroke="currentColor" stroke-width="3"/>',
    sun:     '<circle cx="50" cy="50" r="14"/><g stroke="currentColor" stroke-width="3"><line x1="50" y1="22" x2="50" y2="32"/><line x1="50" y1="68" x2="50" y2="78"/><line x1="22" y1="50" x2="32" y2="50"/><line x1="68" y1="50" x2="78" y2="50"/><line x1="32" y1="32" x2="38" y2="38"/><line x1="62" y1="62" x2="68" y2="68"/><line x1="32" y1="68" x2="38" y2="62"/><line x1="62" y1="38" x2="68" y2="32"/></g>',
    flask:   '<path d="M40 22 V40 L26 70 Q22 80 32 80 H68 Q78 80 74 70 L60 40 V22 Z" fill="none" stroke="currentColor" stroke-width="3"/><path d="M38 56 H62" stroke="currentColor" stroke-width="3"/>',
    quill:   '<path d="M28 78 L62 30 Q72 24 76 30 Q80 36 70 44 L34 78 Z M30 70 H46" stroke="currentColor" stroke-width="2" fill="none"/>',
    gear:    '<circle cx="50" cy="50" r="14" fill="none" stroke="currentColor" stroke-width="3"/><g stroke="currentColor" stroke-width="6" stroke-linecap="round"><line x1="50" y1="20" x2="50" y2="28"/><line x1="50" y1="72" x2="50" y2="80"/><line x1="20" y1="50" x2="28" y2="50"/><line x1="72" y1="50" x2="80" y2="50"/><line x1="29" y1="29" x2="35" y2="35"/><line x1="65" y1="65" x2="71" y2="71"/><line x1="29" y1="71" x2="35" y2="65"/><line x1="65" y1="35" x2="71" y2="29"/></g>',
    coin:    '<circle cx="50" cy="50" r="26" fill="none" stroke="currentColor" stroke-width="3"/><text x="50" y="58" text-anchor="middle" font-family="serif" font-size="24" font-weight="700" fill="currentColor">¤</text>',
    orb:     '<circle cx="50" cy="46" r="20" fill="none" stroke="currentColor" stroke-width="3"/><path d="M30 64 H70 L62 78 H38 Z" />',
    horn:    '<path d="M22 40 Q40 30 60 40 L78 28 V60 L60 50 Q40 60 22 50 Z" fill="none" stroke="currentColor" stroke-width="3"/>',
    world:   '<circle cx="50" cy="50" r="26" fill="none" stroke="currentColor" stroke-width="3"/><ellipse cx="50" cy="50" rx="26" ry="10" fill="none" stroke="currentColor" stroke-width="2"/><line x1="50" y1="24" x2="50" y2="76" stroke="currentColor" stroke-width="2"/>',
    chess:   '<path d="M34 78 H66 V72 H62 V40 L70 30 H58 V22 H42 V30 H30 L38 40 V72 H34 Z" />',
    bridge:  '<path d="M16 60 Q50 30 84 60" fill="none" stroke="currentColor" stroke-width="3"/><line x1="16" y1="60" x2="16" y2="78" stroke="currentColor" stroke-width="3"/><line x1="84" y1="60" x2="84" y2="78" stroke="currentColor" stroke-width="3"/><line x1="34" y1="48" x2="34" y2="66" stroke="currentColor" stroke-width="2"/><line x1="50" y1="42" x2="50" y2="62" stroke="currentColor" stroke-width="2"/><line x1="66" y1="48" x2="66" y2="66" stroke="currentColor" stroke-width="2"/>',
    flag:    '<line x1="32" y1="20" x2="32" y2="80" stroke="currentColor" stroke-width="3"/><path d="M32 24 L72 32 L60 44 L72 56 L32 50 Z" />',
    map:     '<path d="M22 28 L42 22 L62 30 L78 24 V72 L62 78 L42 70 L22 76 Z M42 22 V70 M62 30 V78" fill="none" stroke="currentColor" stroke-width="2"/>',
    prism:   '<path d="M50 22 L78 72 H22 Z" fill="none" stroke="currentColor" stroke-width="3"/><path d="M50 22 L50 72 M22 72 L78 72" stroke="currentColor" stroke-width="1"/>',
    moon:    '<path d="M62 22 Q42 30 42 50 Q42 70 62 78 Q40 78 32 60 Q28 50 32 40 Q40 22 62 22 Z" />'
  };

  function classSymbol(classId) {
    const tx = TAXONOMY.classes[classId];
    const sym = tx ? tx.symbol : 'star';
    return ClassSymbol[sym] || ClassSymbol.star;
  }

  /* ---------- 3. Affinity icon SVGs ---------- */
  const AffinityIconSvg = {
    'stacked-cards': '<rect x="3" y="3" width="10" height="8" rx="1" fill="none" stroke="currentColor" stroke-width="1.4"/><rect x="5" y="6" width="10" height="8" rx="1" fill="none" stroke="currentColor" stroke-width="1.4"/>',
    'shopping-bag': '<path d="M5 7 H15 L14 16 H6 Z M7 7 V5 a3 3 0 0 1 6 0 V7" fill="none" stroke="currentColor" stroke-width="1.4"/>',
    'smartphone':   '<rect x="6" y="3" width="8" height="14" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.4"/><circle cx="10" cy="14.5" r="0.7" fill="currentColor"/>',
    'gauge':        '<path d="M3 13 a7 7 0 0 1 14 0" fill="none" stroke="currentColor" stroke-width="1.4"/><line x1="10" y1="13" x2="13" y2="8" stroke="currentColor" stroke-width="1.4"/><circle cx="10" cy="13" r="1" fill="currentColor"/>',
    'megaphone':    '<path d="M3 9 V11 L11 14 V6 Z M11 7 a3 3 0 0 1 0 6 M5 11 V15 H7 V12" fill="none" stroke="currentColor" stroke-width="1.4"/>',
    'controller':   '<rect x="2" y="6" width="16" height="8" rx="3" fill="none" stroke="currentColor" stroke-width="1.4"/><circle cx="6" cy="10" r="1" fill="currentColor"/><circle cx="14" cy="9" r="0.8" fill="currentColor"/><circle cx="15.5" cy="11" r="0.8" fill="currentColor"/>'
  };

  function affinityIconSvg(symbol) {
    const inner = AffinityIconSvg[symbol] || '<circle cx="10" cy="10" r="6" fill="none" stroke="currentColor" stroke-width="1.4"/>';
    return `<svg viewBox="0 0 20 20" aria-hidden="true">${inner}</svg>`;
  }

  /* ---------- 4. Renderers ---------- */
  function escapeHtml(str) {
    return String(str || '').replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  function portraitSvg(agent, opts = {}) {
    const cls = TAXONOMY.classes[agent.class];
    const cat = TAXONOMY.categories[agent.category];
    const symPath = classSymbol(agent.class);
    const showCaption = opts.showCaption !== false;
    const isPending = !agent.portrait || agent.portrait.status === 'pending';
    const captionLine1 = (agent.name || '').toLowerCase();
    const captionLine2 = `${cls ? cls.archetype : agent.archetype || ''} · ${cat ? cat.label : agent.category}`;

    // Generated portrait branch — caption block is already baked into the image,
    // so we render <img> directly and rely on baked-in name/archetype/category.
    if (!isPending && agent.portrait && agent.portrait.src) {
      // Data uses `../portraits/{name}.png` relative to `agents/{name}.json`.
      // HTML pages live at the directory root, so rewrite to `assets/portraits/...`.
      const resolvedSrc = String(agent.portrait.src).replace(/^\.\.\/portraits\//, 'assets/portraits/');
      const archetypeLabel = cls ? cls.archetype : (agent.archetype || '');
      const categoryLabel = cat ? cat.label : agent.category;
      const classLabel = cls ? cls.label : agent.class;
      const alt = `${agent.name} — ${archetypeLabel} in the ${categoryLabel} category, ${classLabel} class.`;
      return `<img src="${escapeHtml(resolvedSrc)}" alt="${escapeHtml(alt)}"
                   loading="lazy" decoding="async" class="portrait-image"
                   width="512" height="512"/>`;
    }

    return `
      <svg viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet" role="img"
           aria-label="${escapeHtml(agent.name)} portrait placeholder">
        <rect x="0" y="0" width="100" height="100" rx="8" fill="var(--realm-color-surface-card)"/>
        <rect x="2" y="2" width="96" height="96" rx="6" fill="none"
              stroke="var(--realm-color-border-subtle)" stroke-width="1"/>
        <g transform="translate(0,${showCaption ? -8 : 0})" fill="var(--realm-color-brand-primary-strong)" stroke="none">
          ${symPath}
        </g>
        ${showCaption ? `
        <text x="50" y="78" text-anchor="middle"
              font-family="Nunito, system-ui, sans-serif"
              font-size="9" font-weight="700"
              fill="var(--realm-color-ink-strong)">
          ${escapeHtml(captionLine1)}
        </text>
        <text x="50" y="89" text-anchor="middle"
              font-family="Nunito, system-ui, sans-serif"
              font-size="5" font-weight="500"
              fill="var(--realm-color-ink-soft)">
          ${escapeHtml(captionLine2)}
        </text>
        ` : ''}
        ${isPending ? `
        <g transform="translate(80, 8)">
          <rect x="-2" y="-4" width="22" height="9" rx="3"
                class="portrait-pending-badge"
                fill="var(--realm-color-feedback-info)"/>
          <text x="9" y="2" text-anchor="middle"
                font-family="Nunito, system-ui, sans-serif"
                font-size="5" font-weight="700"
                fill="white" letter-spacing="0.5">PENDING</text>
        </g>` : ''}
      </svg>`;
  }

  function rankPillHtml(rank) {
    if (!rank || !rank.tier) return '';
    const tx = TAXONOMY.ranks[rank.tier];
    const fill = `var(--realm-color-rank-${slugRank(rank.tier)}-fill)`;
    const on   = `var(--realm-color-rank-${slugRank(rank.tier)}-on)`;
    return `<span class="rank-pill" style="--rank-fill:${fill}; --rank-on:${on};"
                 aria-label="rank ${escapeHtml(rank.tier)} ${escapeHtml(tx ? tx.title : '')}">
      ${escapeHtml(rank.tier)} · ${escapeHtml(tx ? tx.title : rank.tier)}
    </span>`;
  }

  function slugRank(tier) {
    return ({ F: 'recruit', E: 'novice', D: 'apprentice', C: 'journeyman',
              B: 'veteran', A: 'elite', S: 'champion', SS: 'legend' })[tier] || 'recruit';
  }

  function affinityStripHtml(affinity) {
    if (!Array.isArray(affinity)) return '';
    const sorted = [...affinity].sort((a, b) => {
      const order = { H: 0, M: 1, L: 2 };
      return (order[a.level] ?? 9) - (order[b.level] ?? 9);
    }).slice(0, 3);
    return `<span class="affinity-strip" aria-label="project affinities">
      ${sorted.map(a => {
        const tx = TAXONOMY.affinities[a.project];
        if (!tx) return '';
        return `<span class="affinity" data-level="${escapeHtml(a.level)}"
                      style="--affinity-color: var(--realm-color-affinity-${escapeHtml(a.project)});"
                      title="${escapeHtml(tx.label)} · ${escapeHtml(a.level)}"
                      aria-label="${escapeHtml(tx.label)} affinity ${escapeHtml(a.level)}">
          ${affinityIconSvg(tx.symbol)}
        </span>`;
      }).join('')}
    </span>`;
  }

  function agentCardHtml(agent) {
    const cls = TAXONOMY.classes[agent.class];
    const cat = TAXONOMY.categories[agent.category];
    const clsLabel = cls ? cls.label : (agent.class || 'Unclassified');
    const catLabel = cat ? cat.label : (agent.category || 'Uncategorized');
    return `
      <a class="agent-card" href="detail.html?name=${encodeURIComponent(agent.name)}"
         data-name="${escapeHtml(agent.name)}"
         aria-label="${escapeHtml(agent.name)}, ${escapeHtml(clsLabel)} class, ${escapeHtml(catLabel)} category">
        <div class="agent-card__portrait">${portraitSvg(agent, { showCaption: true })}</div>
        <div class="agent-card__meta">
          <span class="agent-card__class">${escapeHtml(clsLabel)}</span>
          ${rankPillHtml(agent.rank)}
        </div>
        <div class="agent-card__archetype">${escapeHtml(catLabel)}</div>
        <p class="agent-card__tagline">${escapeHtml(agent.tagline || agent.description || '')}</p>
        <div class="agent-card__footer">
          ${affinityStripHtml(agent.affinity)}
        </div>
      </a>`;
  }

  /* ---------- 5. Search & filter ---------- */
  const FilterState = {
    query: '',
    cat: new Set(),     // categories
    cls: new Set(),     // classes
    aff: new Set(),     // affinity ids (must be H or M)
    sort: 'name',       // name | category | rank
    fromUrl() {
      const p = new URLSearchParams(location.search);
      this.query = p.get('q') || '';
      this.cat = new Set((p.get('cat') || '').split(',').filter(Boolean));
      this.cls = new Set((p.get('cls') || '').split(',').filter(Boolean));
      this.aff = new Set((p.get('aff') || '').split(',').filter(Boolean));
      this.sort = p.get('sort') || 'name';
    },
    toUrl({ replace = true } = {}) {
      const p = new URLSearchParams();
      if (this.query) p.set('q', this.query);
      if (this.cat.size) p.set('cat', [...this.cat].join(','));
      if (this.cls.size) p.set('cls', [...this.cls].join(','));
      if (this.aff.size) p.set('aff', [...this.aff].join(','));
      if (this.sort && this.sort !== 'name') p.set('sort', this.sort);
      const qs = p.toString();
      const url = qs ? `?${qs}` : location.pathname;
      if (replace) history.replaceState(null, '', url);
      else history.pushState(null, '', url);
    },
    toggleSet(name, value) {
      const set = this[name];
      if (set.has(value)) set.delete(value);
      else set.add(value);
    }
  };

  function score(agent, q) {
    if (!q) return 1;
    const Q = q.toLowerCase();
    let s = 0;
    const name = (agent.name || '').toLowerCase();
    const arch = (agent.archetype || '').toLowerCase();
    const cat  = (agent.category  || '').toLowerCase();
    const cls  = (agent.class     || '').toLowerCase();
    const tag  = (agent.tagline   || '').toLowerCase();
    const desc = (agent.description || '').toLowerCase();
    if (name === Q) s += 100;
    if (name.startsWith(Q)) s += 60;
    if (name.includes(Q)) s += 30;
    if (arch.includes(Q)) s += 12;
    if (cat.includes(Q))  s += 8;
    if (cls.includes(Q))  s += 8;
    if (tag.includes(Q))  s += 6;
    if (desc.includes(Q)) s += 4;
    if (Array.isArray(agent.capabilities)) {
      for (const c of agent.capabilities) {
        if ((c.summary || '').toLowerCase().includes(Q)) s += 3;
        if ((c.key || '').toLowerCase().includes(Q)) s += 2;
      }
    }
    return s;
  }

  function applyFilters(agents) {
    return agents.filter(a => {
      if (FilterState.cat.size && !FilterState.cat.has(a.category)) return false;
      if (FilterState.cls.size && !FilterState.cls.has(a.class)) return false;
      if (FilterState.aff.size) {
        const setH = new Set((a.affinity || [])
          .filter(x => x.level === 'H' || x.level === 'M')
          .map(x => x.project));
        // OR within axis: any selected affinity matches
        let any = false;
        for (const id of FilterState.aff) if (setH.has(id)) { any = true; break; }
        if (!any) return false;
      }
      return true;
    });
  }

  function rank(agents) {
    const q = FilterState.query.trim();
    const list = applyFilters(agents);
    if (q) {
      const scored = list
        .map(a => ({ a, s: score(a, q) }))
        .filter(x => x.s > 0)
        .sort((x, y) => y.s - x.s || x.a.name.localeCompare(y.a.name));
      return scored.map(x => x.a);
    }
    const sorter = {
      name: (x, y) => x.name.localeCompare(y.name),
      category: (x, y) => (x.category || '').localeCompare(y.category || '') || x.name.localeCompare(y.name),
      rank: (x, y) => {
        const order = { SS: 0, S: 1, A: 2, B: 3, C: 4, D: 5, E: 6, F: 7 };
        const xt = x.rank?.tier ? order[x.rank.tier] : 99;
        const yt = y.rank?.tier ? order[y.rank.tier] : 99;
        return xt - yt || x.name.localeCompare(y.name);
      }
    }[FilterState.sort] || ((x, y) => x.name.localeCompare(y.name));
    return [...list].sort(sorter);
  }

  /* ---------- Filter rail rendering ---------- */
  function renderFilterRail(container, allAgents) {
    const cats = [...new Set(allAgents.map(a => a.category))].sort();
    const cls  = [...new Set(allAgents.map(a => a.class))].sort();
    const affs = ['saas', 'ecommerce', 'mobile', 'dashboard', 'marketing', 'game'];

    container.innerHTML = `
      <div class="filter-rail__section" data-axis="cat">
        <p class="chip-group__legend">Category</p>
        <div class="chip-group" role="group" aria-label="Filter by category">
          ${cats.map(c => {
            const tx = TAXONOMY.categories[c];
            return `<button class="chip" type="button" role="switch"
                            data-axis="cat" data-value="${escapeHtml(c)}"
                            aria-pressed="${FilterState.cat.has(c)}">
              ${escapeHtml(tx ? tx.label : c)}
            </button>`;
          }).join('')}
        </div>
      </div>
      <div class="filter-rail__section" data-axis="cls">
        <p class="chip-group__legend">Class</p>
        <div class="chip-group" role="group" aria-label="Filter by class">
          ${cls.map(c => {
            const tx = TAXONOMY.classes[c];
            return `<button class="chip" type="button" role="switch"
                            data-axis="cls" data-value="${escapeHtml(c)}"
                            aria-pressed="${FilterState.cls.has(c)}">
              ${escapeHtml(tx ? tx.label : c)}
            </button>`;
          }).join('')}
        </div>
      </div>
      <div class="filter-rail__section" data-axis="aff">
        <p class="chip-group__legend">Affinity</p>
        <div class="chip-group" role="group" aria-label="Filter by project affinity">
          ${affs.map(c => {
            const tx = TAXONOMY.affinities[c];
            return `<button class="chip" type="button" role="switch"
                            data-axis="aff" data-value="${escapeHtml(c)}"
                            aria-pressed="${FilterState.aff.has(c)}">
              ${escapeHtml(tx ? tx.label : c)}
            </button>`;
          }).join('')}
        </div>
      </div>
      <div class="filter-rail__section">
        <p class="chip-group__legend">Sort</p>
        <select class="search__input" data-sort
                aria-label="Sort agents"
                style="border:1px solid var(--realm-color-border-default); padding: 8px; border-radius: var(--realm-radius-md);">
          <option value="name"${FilterState.sort === 'name' ? ' selected' : ''}>Name (A→Z)</option>
          <option value="category"${FilterState.sort === 'category' ? ' selected' : ''}>Category</option>
          <option value="rank"${FilterState.sort === 'rank' ? ' selected' : ''}>Rank</option>
        </select>
      </div>
      <div class="filter-rail__section">
        <button class="btn btn--ghost" type="button" data-filter-clear>Clear filters</button>
      </div>
    `;
  }

  function bindFilterRail(container, onChange) {
    container.addEventListener('click', e => {
      const chip = e.target.closest('.chip[data-axis]');
      if (chip) {
        const axis = chip.dataset.axis;
        const val  = chip.dataset.value;
        const setName = axis === 'cat' ? 'cat' : axis === 'cls' ? 'cls' : 'aff';
        FilterState.toggleSet(setName, val);
        chip.setAttribute('aria-pressed', FilterState[setName].has(val));
        FilterState.toUrl();
        onChange();
        return;
      }
      const clearBtn = e.target.closest('[data-filter-clear]');
      if (clearBtn) {
        FilterState.cat.clear(); FilterState.cls.clear(); FilterState.aff.clear();
        FilterState.query = '';
        const search = document.querySelector('[data-search-input]');
        if (search) search.value = '';
        container.querySelectorAll('.chip[aria-pressed]').forEach(c => c.setAttribute('aria-pressed', 'false'));
        FilterState.toUrl();
        onChange();
      }
    });
    container.addEventListener('change', e => {
      const sel = e.target.closest('[data-sort]');
      if (sel) {
        FilterState.sort = sel.value;
        FilterState.toUrl();
        onChange();
      }
    });
  }

  /* ---------- Search input ---------- */
  function bindSearch(input, onChange) {
    if (!input) return;
    input.value = FilterState.query;
    let t;
    input.addEventListener('input', () => {
      clearTimeout(t);
      t = setTimeout(() => {
        FilterState.query = input.value.trim();
        FilterState.toUrl();
        onChange();
      }, 80);
    });
    document.addEventListener('keydown', e => {
      if (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
        e.preventDefault();
        input.focus();
        input.select();
      }
    });
  }

  /* ---------- Keyboard grid navigation ---------- */
  function bindGridKeynav(grid) {
    if (!grid) return;
    grid.addEventListener('keydown', e => {
      const cards = [...grid.querySelectorAll('.agent-card')];
      if (!cards.length) return;
      const i = cards.indexOf(document.activeElement);
      if (i < 0) return;
      // Approximate columns from grid template
      const styles = getComputedStyle(grid);
      const cols = styles.gridTemplateColumns.split(' ').length || 4;
      let next = i;
      if (e.key === 'ArrowRight') next = Math.min(i + 1, cards.length - 1);
      else if (e.key === 'ArrowLeft') next = Math.max(i - 1, 0);
      else if (e.key === 'ArrowDown') next = Math.min(i + cols, cards.length - 1);
      else if (e.key === 'ArrowUp') next = Math.max(i - cols, 0);
      else if (e.key === 'Home') next = 0;
      else if (e.key === 'End') next = cards.length - 1;
      else return;
      e.preventDefault();
      cards[next].focus();
    });
  }

  /* ---------- Page bootstraps ---------- */
  async function bootIndex() {
    FilterState.fromUrl();
    const data = await DataStore.load();
    const agents = data.agents || [];

    const rail = document.querySelector('[data-filter-rail]');
    const searchInput = document.querySelector('[data-search-input]');
    const resultsRoot = document.querySelector('[data-results]');
    const countEl = document.querySelector('[data-count]');

    renderFilterRail(rail, agents);
    bindSearch(searchInput, render);
    bindFilterRail(rail, render);
    render();
    bindGridKeynav(resultsRoot);

    function render() {
      const list = rank(agents);
      const byCat = list.reduce((acc, a) => {
        (acc[a.category] = acc[a.category] || []).push(a);
        return acc;
      }, {});
      const order = Object.keys(byCat).sort((a, b) => {
        const ord = ['ux-design', 'implementation', 'investigation', 'review',
                     'meta-tooling', 'documentation', 'orchestration'];
        const ia = ord.indexOf(a), ib = ord.indexOf(b);
        return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
      });
      if (!list.length) {
        resultsRoot.innerHTML = `
          <div class="empty-state">
            <div class="empty-state__icon" aria-hidden="true">⌕</div>
            <p>No agents match. Try removing a filter or clearing search.</p>
            <p class="empty-state__hint">Tip: press <code>/</code> to focus the search input.</p>
          </div>`;
      } else {
        resultsRoot.innerHTML = order.map(catId => {
          const items = byCat[catId];
          const tx = TAXONOMY.categories[catId];
          return `
            <section aria-labelledby="sec-${catId}">
              <header class="section-head">
                <h2 class="section-head__title" id="sec-${catId}">${escapeHtml(tx ? tx.label : catId)}</h2>
                <span class="section-head__count">${items.length} agent${items.length === 1 ? '' : 's'}</span>
              </header>
              <div class="grid-cards" role="grid" aria-label="${escapeHtml(tx ? tx.label : catId)} agents">
                ${items.map(agentCardHtml).join('')}
              </div>
            </section>`;
        }).join('');
      }
      if (countEl) countEl.textContent = `${list.length} of ${agents.length}`;
    }
  }

  async function bootCategory() {
    const params = new URLSearchParams(location.search);
    const slug = params.get('slug') || 'ux-design';
    const data = await DataStore.load();
    const agents = (data.agents || []).filter(a => a.category === slug);
    const tx = TAXONOMY.categories[slug];
    const heroEl = document.querySelector('[data-cat-hero]');
    const breadcrumbEl = document.querySelector('[data-breadcrumb]');
    const rosterEl = document.querySelector('[data-roster]');
    const collabEl = document.querySelector('[data-collab]');
    const adjacentEl = document.querySelector('[data-adjacent]');
    const tabRoster = document.querySelector('[data-tab="roster"]');
    const tabCollab = document.querySelector('[data-tab="collab"]');

    if (breadcrumbEl) {
      breadcrumbEl.innerHTML = `
        <a href="index.html">Realm</a>
        <span class="breadcrumb__sep" aria-hidden="true">›</span>
        <span class="breadcrumb__current" aria-current="page">${escapeHtml(tx ? tx.label : slug)}</span>`;
    }
    if (heroEl && tx) {
      heroEl.innerHTML = `
        <p class="category-hero__label">Category</p>
        <h1 class="category-hero__title">${escapeHtml(tx.label)}</h1>
        <p class="category-hero__flavor">${escapeHtml(tx.trait)} — agents in this department share an archetype and a class bonus.</p>
        <div class="category-hero__stats">
          <div class="category-hero__stat">
            <span class="category-hero__stat-num">${agents.length}</span>
            <span class="category-hero__stat-label">agents</span>
          </div>
          <div class="category-hero__stat">
            <span class="category-hero__stat-num">${[...new Set(agents.map(a => a.class))].length}</span>
            <span class="category-hero__stat-label">classes</span>
          </div>
        </div>`;
    }
    if (rosterEl) {
      rosterEl.innerHTML = agents.length
        ? `<div class="grid-cards" role="grid">${agents.map(agentCardHtml).join('')}</div>`
        : `<div class="empty-state">No agents in this category yet.</div>`;
    }
    if (collabEl) {
      collabEl.innerHTML = collaborationGraphSvg(agents);
    }
    if (adjacentEl) {
      const cats = Object.keys(TAXONOMY.categories);
      const idx = cats.indexOf(slug);
      const prev = cats[(idx - 1 + cats.length) % cats.length];
      const next = cats[(idx + 1) % cats.length];
      adjacentEl.innerHTML = `
        <a class="btn btn--ghost" href="?slug=${encodeURIComponent(prev)}">‹ ${escapeHtml(TAXONOMY.categories[prev].label)}</a>
        <a class="btn btn--ghost" href="?slug=${encodeURIComponent(next)}">${escapeHtml(TAXONOMY.categories[next].label)} ›</a>`;
    }
    bindTabs();
    bindGridKeynav(rosterEl);
  }

  function bindTabs() {
    document.querySelectorAll('[data-tabset]').forEach(set => {
      const items = set.querySelectorAll('.tabs__item');
      const panels = document.querySelectorAll('.tab-panel');
      items.forEach(it => {
        it.addEventListener('click', () => {
          items.forEach(i => i.setAttribute('aria-selected', 'false'));
          it.setAttribute('aria-selected', 'true');
          panels.forEach(p => {
            p.hidden = p.dataset.tabPanel !== it.dataset.tab;
          });
        });
      });
    });
  }

  function collaborationGraphSvg(agents) {
    // Pick up to 6 agents for a small radial graph
    const nodes = agents.slice(0, 6);
    const cx = 200, cy = 130, r = 90;
    const center = nodes[0] || { name: 'category' };
    const ring = nodes.slice(1);
    const points = ring.map((n, i) => {
      const angle = (Math.PI * 2 * i) / Math.max(ring.length, 1) - Math.PI / 2;
      return {
        x: cx + Math.cos(angle) * r,
        y: cy + Math.sin(angle) * r,
        node: n
      };
    });
    return `
      <svg class="collab-graph__svg" viewBox="0 0 400 260" role="img"
           aria-label="Collaboration graph">
        ${points.map(p => `<line class="collab-graph__edge"
          x1="${cx}" y1="${cy}" x2="${p.x}" y2="${p.y}" />`).join('')}
        <circle class="collab-graph__node-circle collab-graph__node-circle--center"
                cx="${cx}" cy="${cy}" r="32"/>
        <text class="collab-graph__node-text" x="${cx}" y="${cy + 4}"
              text-anchor="middle" font-weight="700">${escapeHtml(center.name)}</text>
        ${points.map(p => `
          <circle class="collab-graph__node-circle" cx="${p.x}" cy="${p.y}" r="22"/>
          <text class="collab-graph__node-text" x="${p.x}" y="${p.y + 4}"
                text-anchor="middle">${escapeHtml(p.node.name)}</text>
        `).join('')}
      </svg>`;
  }

  async function bootDetail() {
    const params = new URLSearchParams(location.search);
    const name = params.get('name') || 'flow';
    const idx = await DataStore.load();
    const agent = await DataStore.loadAgent(name) || idx.agents.find(a => a.name === name);
    if (!agent) {
      document.querySelector('[data-detail]').innerHTML = `
        <div class="empty-state">
          <p>Agent <strong>${escapeHtml(name)}</strong> not found.</p>
          <p class="empty-state__hint"><a href="index.html">Browse the directory</a></p>
        </div>`;
      return;
    }
    const cls = TAXONOMY.classes[agent.class];
    const cat = TAXONOMY.categories[agent.category];

    const breadcrumbEl = document.querySelector('[data-breadcrumb]');
    if (breadcrumbEl) {
      breadcrumbEl.innerHTML = `
        <a href="index.html">Realm</a>
        <span class="breadcrumb__sep" aria-hidden="true">›</span>
        <a href="category.html?slug=${encodeURIComponent(agent.category)}">${escapeHtml(cat ? cat.label : agent.category)}</a>
        <span class="breadcrumb__sep" aria-hidden="true">›</span>
        <span class="breadcrumb__current" aria-current="page">${escapeHtml(agent.name)}</span>`;
    }

    const heroEl = document.querySelector('[data-detail-hero]');
    heroEl.innerHTML = `
      <div class="detail-hero__portrait">${portraitSvg(agent, { showCaption: false })}</div>
      <div>
        <h1 class="detail-hero__name">${escapeHtml(agent.name)}</h1>
        <p class="detail-hero__archetype">
          ${escapeHtml(cls ? cls.label : agent.class)} · ${escapeHtml(cat ? cat.label : agent.category)}
        </p>
        <p class="detail-hero__tagline">${escapeHtml(agent.tagline || agent.description || '')}</p>
        <div class="cluster">
          ${rankPillHtml(agent.rank)}
          ${affinityStripHtml(agent.affinity)}
        </div>
        <div class="detail-hero__cta">
          <button class="btn btn--primary" data-copy="@${escapeHtml(agent.name)}">
            Copy invocation
          </button>
          <a class="btn btn--ghost" href="map.html#${encodeURIComponent(agent.name)}">See in map</a>
        </div>
      </div>`;

    const overviewEl = document.querySelector('[data-tab-panel="overview"]');
    overviewEl.innerHTML = renderOverviewPanel(agent, cls, cat);

    const capsEl = document.querySelector('[data-tab-panel="capabilities"]');
    capsEl.innerHTML = renderCapabilitiesPanel(agent);

    const collabPanel = document.querySelector('[data-tab-panel="collaboration"]');
    collabPanel.innerHTML = renderCollaborationPanel(agent, idx.agents || []);

    const examplesEl = document.querySelector('[data-tab-panel="examples"]');
    examplesEl.innerHTML = renderExamplesPanel(agent, idx.agents || []);

    // Related strips
    const sameClass = (idx.agents || []).filter(a => a.class === agent.class && a.name !== agent.name).slice(0, 6);
    const sameAff = (idx.agents || []).filter(a => {
      if (a.name === agent.name) return false;
      const aH = new Set((a.affinity || []).filter(x => x.level === 'H').map(x => x.project));
      return (agent.affinity || []).some(x => x.level === 'H' && aH.has(x.project));
    }).slice(0, 6);

    document.querySelector('[data-related-class]').innerHTML = sameClass.length
      ? `<header class="section-head">
           <h2 class="section-head__title">Same class · ${escapeHtml(cls ? cls.label : agent.class)}</h2>
         </header>
         <div class="grid-cards" role="grid">${sameClass.map(agentCardHtml).join('')}</div>`
      : '';

    document.querySelector('[data-related-aff]').innerHTML = sameAff.length
      ? `<header class="section-head">
           <h2 class="section-head__title">Shared project affinity</h2>
         </header>
         <div class="grid-cards" role="grid">${sameAff.map(agentCardHtml).join('')}</div>`
      : '';

    bindTabs();

    document.querySelectorAll('[data-copy]').forEach(b => {
      b.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(b.dataset.copy);
          const orig = b.textContent;
          b.textContent = 'Copied!';
          setTimeout(() => { b.textContent = orig; }, 1500);
        } catch {}
      });
    });
  }

  function detailCollabSvg(agent, allAgents = []) {
    const byName = new Map(allAgents.map(a => [a.name, a]));
    const inputs  = (agent.collaboration?.input  || []).slice(0, 4);
    const outputs = (agent.collaboration?.output || []).slice(0, 4);
    const W = 480, H = 300;
    const cy = H / 2;
    const inX = 60, outX = W - 60, midX = W / 2;
    const inputY  = (i) => 30 + ((H - 60) / Math.max(inputs.length, 1)) * (i + 0.5);
    const outputY = (i) => 30 + ((H - 60) / Math.max(outputs.length, 1)) * (i + 0.5);

    const patternDefs = [];
    const slug = (s) => String(s).replace(/[^a-zA-Z0-9_-]/g, '-');
    const portraitNode = (name, x, y, r, isCenter) => {
      const partner = byName.get(name);
      const hasImg = partner && partner.portrait
        && partner.portrait.status === 'generated' && partner.portrait.src;
      const labelY = y + r + 16;
      const circleClass = isCenter
        ? 'collab-graph__node-circle collab-graph__node-circle--center'
        : 'collab-graph__node-circle';
      const labelWeight = isCenter ? '700' : '500';
      const navHref = `detail.html?name=${encodeURIComponent(name)}`;
      let fillStyle = '';
      if (hasImg) {
        const src = String(partner.portrait.src).replace(/^\.\.\/portraits\//, 'assets/portraits/');
        const patId = `collab-pat-${slug(name)}-${Math.round(x)}-${Math.round(y)}`;
        patternDefs.push(
          `<pattern id="${patId}" patternContentUnits="objectBoundingBox" width="1" height="1">` +
          `<image href="${escapeHtml(src)}" x="0" y="0" width="1" height="1" ` +
          `preserveAspectRatio="xMidYMid slice"/>` +
          `</pattern>`
        );
        fillStyle = ` style="fill: url(#${patId})"`;
      }
      return `
        <a href="${escapeHtml(navHref)}" class="collab-graph__node-link"
           aria-label="View ${escapeHtml(name)} details">
          <circle class="${circleClass}" cx="${x}" cy="${y}" r="${r}"${fillStyle}/>
          <text class="collab-graph__node-text" x="${x}" y="${labelY}"
                text-anchor="middle" font-weight="${labelWeight}">${escapeHtml(name)}</text>
        </a>`;
    };

    const centerNode = portraitNode(agent.name, midX, cy, 38, true);
    const inputNodes = inputs.map((n, i) => portraitNode(n, inX, inputY(i), 22, false)).join('');
    const outputNodes = outputs.map((n, i) => portraitNode(n, outX, outputY(i), 22, false)).join('');

    return `
      <svg class="collab-graph__svg" viewBox="0 0 ${W} ${H}" role="img"
           aria-label="Collaboration: input agents on the left, ${escapeHtml(agent.name)} center, output agents on the right">
        <defs>${patternDefs.join('')}</defs>
        ${inputs.map((n, i) => `<line class="collab-graph__edge" x1="${inX}" y1="${inputY(i)}" x2="${midX}" y2="${cy}"/>`).join('')}
        ${outputs.map((n, i) => `<line class="collab-graph__edge" x1="${midX}" y1="${cy}" x2="${outX}" y2="${outputY(i)}"/>`).join('')}
        ${centerNode}
        ${inputNodes}
        ${outputNodes}
        <text x="${inX}" y="18" text-anchor="middle" font-family="Nunito" font-size="11" font-weight="700"
              fill="var(--realm-color-ink-soft)">INPUT</text>
        <text x="${outX}" y="18" text-anchor="middle" font-family="Nunito" font-size="11" font-weight="700"
              fill="var(--realm-color-ink-soft)">OUTPUT</text>
      </svg>`;
  }

  /* ---------- Detail tab renderers (Overview / Capabilities / Collaboration / Examples) ---------- */

  /** Build the affinity matrix: all 6 project types with level dots (H=3, M=2, L=1, none=0) */
  function affinityMatrixHtml(affinity) {
    const ALL_AFFINITIES = ['saas', 'ecommerce', 'mobile', 'dashboard', 'marketing', 'game'];
    const affinityMap = new Map((affinity || []).map(a => [a.project, a.level]));
    const dotCount = { H: 3, M: 2, L: 1 };
    return `<div class="detail-affinity-matrix" aria-label="Project affinity breakdown">
      ${ALL_AFFINITIES.map(id => {
        const tx = TAXONOMY.affinities[id];
        if (!tx) return '';
        const level = affinityMap.get(id) || null;
        const count = level ? (dotCount[level] || 0) : 0;
        const isNone = !level;
        const dots = [1,2,3].map(i =>
          `<span class="detail-affinity-matrix__dot${i <= count ? ' detail-affinity-matrix__dot--filled' : ''}" aria-hidden="true">●</span>`
        ).join('');
        return `<div class="detail-affinity-matrix__cell${isNone ? ' detail-affinity-matrix__cell--none' : ''}"
                     title="${escapeHtml(tx.label)}: ${escapeHtml(level || 'None')}">
          <span class="detail-affinity-matrix__icon">${affinityIconSvg(tx.symbol)}</span>
          <span class="detail-affinity-matrix__label">${escapeHtml(tx.label)}</span>
          <span class="detail-affinity-matrix__dots" aria-label="${escapeHtml(tx.label)} affinity ${escapeHtml(level || 'None')}">${dots}</span>
          <span class="detail-affinity-matrix__level">${escapeHtml(level || '—')}</span>
        </div>`;
      }).join('')}
    </div>`;
  }

  function renderOverviewPanel(agent, cls, cat) {
    const parts = [];

    // 1. Tagline quote
    if (agent.tagline) {
      parts.push(`<blockquote class="detail-quote">${escapeHtml(agent.tagline)}</blockquote>`);
    }

    // 2. Lede paragraph
    if (agent.description) {
      parts.push(`<p>${escapeHtml(agent.description)}</p>`);
    }

    // 3. Class flavor card
    if (cls) {
      const catTrait = cat ? cat.trait : '';
      const deptLine = agent.department
        ? `<p class="detail-flavor__meta">${escapeHtml(agent.department)}${catTrait ? ` · ${escapeHtml(catTrait)}` : ''}</p>`
        : (catTrait ? `<p class="detail-flavor__meta">${escapeHtml(catTrait)}</p>` : '');
      parts.push(`<div class="detail-flavor">
        <p class="detail-flavor__label">Class Flavor · ${escapeHtml(cls.label)}</p>
        <p class="detail-flavor__archetype">${escapeHtml(cls.archetype)}</p>
        <p class="detail-flavor__passive">Passive: <strong>${escapeHtml(cls.passive)}</strong> — ${escapeHtml(cls.bonus)}</p>
        ${deptLine}
      </div>`);
    }

    // 4. Project affinity full breakdown
    parts.push(`<section aria-labelledby="ov-affinity-head">
      <header class="section-head" style="margin-block: var(--realm-spacing-md) var(--realm-spacing-sm);">
        <h3 class="section-head__title" id="ov-affinity-head">Project Affinity</h3>
      </header>
      ${affinityMatrixHtml(agent.affinity)}
    </section>`);

    // 5. Recipes preview
    const recipes = agent.recipes || [];
    if (recipes.length) {
      const MAX_RECIPES = 6;
      const shown = recipes.slice(0, MAX_RECIPES);
      const extra = recipes.length - shown.length;
      const chips = shown.map(r =>
        `<code class="chip" style="font-family: var(--core-font-family-mono);">/skill ${escapeHtml(agent.name)} ${escapeHtml(r)}</code>`
      ).join('');
      const morePart = extra > 0 ? `<span class="chip chip--muted">+${extra} more</span>` : '';
      parts.push(`<section aria-labelledby="ov-recipes-head">
        <header class="section-head" style="margin-block: var(--realm-spacing-md) var(--realm-spacing-sm);">
          <h3 class="section-head__title" id="ov-recipes-head">Recipes</h3>
        </header>
        <div class="chip-group recipes-chips" role="list">${chips}${morePart}</div>
      </section>`);
    }

    // 6. Quick stats footer
    const capCount = (agent.capabilities || []).length;
    const inputCount = (agent.collaboration?.input || []).length;
    const outputCount = (agent.collaboration?.output || []).length;
    const tierLabel = agent.rank?.tier || '—';
    parts.push(`<p class="detail-stats">
      ${capCount} ${capCount === 1 ? 'capability' : 'capabilities'} ·
      ${inputCount} input partner${inputCount === 1 ? '' : 's'} ·
      ${outputCount} output partner${outputCount === 1 ? '' : 's'} ·
      rank ${escapeHtml(tierLabel)}
    </p>`);

    // 7. Badges
    const badges = agent.badges || [];
    if (badges.length) {
      const badgeChips = badges.map(b =>
        `<span class="chip">${escapeHtml(b)}</span>`
      ).join('');
      parts.push(`<div class="chip-group" role="list" aria-label="Badges" style="margin-top: var(--realm-spacing-sm);">${badgeChips}</div>`);
    }

    return parts.join('\n');
  }

  function renderCapabilitiesPanel(agent) {
    const caps = agent.capabilities || [];
    const header = `<header class="section-head" style="margin-bottom: var(--realm-spacing-md);">
      <h3 class="section-head__title">${caps.length} ${caps.length === 1 ? 'capability' : 'capabilities'}</h3>
    </header>`;
    if (!caps.length) {
      return header + `<div class="empty-note">No capabilities defined yet.</div>`;
    }
    return header + `<ul class="cap-list">
      ${caps.map(c => `
        <li>
          <div class="cap-list__key">${escapeHtml(c.key)}</div>
          <div>${escapeHtml(c.summary)}</div>
        </li>`).join('')}
    </ul>`;
  }

  function renderCollaborationPanel(agent, allAgents) {
    const byName = new Map(allAgents.map(a => [a.name, a]));
    const inputs  = (agent.collaboration?.input  || []);
    const outputs = (agent.collaboration?.output || []);

    if (!inputs.length && !outputs.length) {
      return `<div class="collab-graph">${detailCollabSvg(agent, allAgents)}</div>
        <p class="empty-note">No collaboration partners declared.</p>`;
    }

    const MAX_SHOWN = 6;

    function partnerListHtml(names, labelPrefix) {
      const shown = names.slice(0, MAX_SHOWN);
      const extra = names.length - shown.length;
      const items = shown.map(n => {
        const partner = byName.get(n);
        const pcls = partner ? TAXONOMY.classes[partner.class] : null;
        const role = pcls ? escapeHtml(pcls.archetype) : (partner ? escapeHtml(partner.archetype || partner.category || '') : '');
        const href = `detail.html?name=${encodeURIComponent(n)}`;
        return `<li class="partner-list__item">
          <a class="partner-list__link" href="${escapeHtml(href)}">${escapeHtml(n)}</a>
          ${role ? `<span class="partner-list__role">${role}</span>` : ''}
        </li>`;
      }).join('');
      const moreLine = extra > 0 ? `<li class="partner-list__item partner-list__more">+${extra} more</li>` : '';
      return `<ul class="partner-list">${items}${moreLine}</ul>`;
    }

    return `<div class="collab-graph">${detailCollabSvg(agent, allAgents)}</div>
      <div class="collab-detail-grid">
        <section aria-labelledby="collab-in-head">
          <header class="section-head">
            <h3 class="section-head__title" id="collab-in-head">Receives work from · ${inputs.length}</h3>
          </header>
          ${inputs.length ? partnerListHtml(inputs) : '<p class="empty-note">No input partners.</p>'}
        </section>
        <section aria-labelledby="collab-out-head">
          <header class="section-head">
            <h3 class="section-head__title" id="collab-out-head">Sends work to · ${outputs.length}</h3>
          </header>
          ${outputs.length ? partnerListHtml(outputs) : '<p class="empty-note">No output partners.</p>'}
        </section>
      </div>`;
  }

  function renderExamplesPanel(agent, allAgents) {
    const byName = new Map(allAgents.map(a => [a.name, a]));
    const parts = [];

    // 1. Invocation patterns
    const recipes = agent.recipes || [];
    const recipeChips = recipes.length
      ? recipes.map(r => {
          const invText = `/skill ${agent.name} ${r}`;
          return `<div class="invocation-block invocation-block--sm">
            <code class="invocation-block__code">${escapeHtml(invText)}</code>
            <button class="btn btn--ghost" data-copy="${escapeHtml(invText)}" style="font-size: var(--core-font-size-12); padding: 4px 8px; min-height: 32px;">Copy</button>
          </div>`;
        }).join('')
      : '';

    parts.push(`<section aria-labelledby="ex-invoke-head">
      <header class="section-head" style="margin-bottom: var(--realm-spacing-sm);">
        <h3 class="section-head__title" id="ex-invoke-head">Invocation</h3>
      </header>
      <div class="invocation-block">
        <code class="invocation-block__code">@${escapeHtml(agent.name)}</code>
        <button class="btn btn--primary" data-copy="@${escapeHtml(agent.name)}">Copy</button>
      </div>
      ${recipeChips ? `<div class="recipes-chips" style="margin-top: var(--realm-spacing-sm);">${recipeChips}</div>` : ''}
    </section>`);

    // 2. Sample prompts from capabilities
    const caps = agent.capabilities || [];
    let sampleItems = '';
    if (caps.length) {
      const shown = caps.slice(0, 3);
      const lcFirst = s => s ? s.charAt(0).toLowerCase() + s.slice(1) : s;
      sampleItems = shown.map(c => `
        <li>
          <div class="cap-list__key">Sample prompt</div>
          <div>Use <strong>${escapeHtml(agent.name)}</strong> when you need to ${escapeHtml(lcFirst(c.summary))}.</div>
        </li>`).join('');
    } else {
      const archLabel = agent.archetype || (TAXONOMY.classes[agent.class]?.archetype) || 'specialist';
      sampleItems = `<li>
        <div class="cap-list__key">Sample prompt</div>
        <div>Ask <strong>${escapeHtml(agent.name)}</strong> when you need ${escapeHtml(archLabel)} work.</div>
      </li>`;
    }
    parts.push(`<section aria-labelledby="ex-samples-head" style="margin-top: var(--realm-spacing-lg);">
      <header class="section-head" style="margin-bottom: var(--realm-spacing-sm);">
        <h3 class="section-head__title" id="ex-samples-head">Sample Prompts</h3>
      </header>
      <ul class="cap-list">${sampleItems}</ul>
    </section>`);

    // 3. Pairs well with (collaboration.output top 3)
    const outputs = (agent.collaboration?.output || []).slice(0, 3);
    if (outputs.length) {
      const pairItems = outputs.map(n => {
        const partner = byName.get(n);
        const pcls = partner ? TAXONOMY.classes[partner.class] : null;
        const role = pcls ? escapeHtml(pcls.archetype) : (partner ? escapeHtml(partner.archetype || partner.class || '') : '');
        const href = `detail.html?name=${encodeURIComponent(n)}`;
        return `<li class="partner-list__item">
          <a class="partner-list__link" href="${escapeHtml(href)}">${escapeHtml(n)}</a>
          ${role ? `<span class="partner-list__role">${role}</span>` : ''}
        </li>`;
      }).join('');
      parts.push(`<section aria-labelledby="ex-pairs-head" style="margin-top: var(--realm-spacing-lg);">
        <header class="section-head" style="margin-bottom: var(--realm-spacing-sm);">
          <h3 class="section-head__title" id="ex-pairs-head">Pairs Well With</h3>
        </header>
        <ul class="partner-list">${pairItems}</ul>
      </section>`);
    }

    return parts.join('\n');
  }

  async function bootSearch() {
    FilterState.fromUrl();
    const data = await DataStore.load();
    const agents = data.agents || [];

    const input = document.querySelector('[data-search-input]');
    const tokensEl = document.querySelector('[data-active-filters]');
    const resultsEl = document.querySelector('[data-results]');
    const countEl = document.querySelector('[data-count]');

    bindSearch(input, render);

    document.addEventListener('click', e => {
      const tok = e.target.closest('[data-remove-filter]');
      if (!tok) return;
      const axis = tok.dataset.axis;
      const val  = tok.dataset.value;
      if (axis === 'q') FilterState.query = '';
      else FilterState[axis].delete(val);
      FilterState.toUrl();
      const inp = document.querySelector('[data-search-input]');
      if (axis === 'q' && inp) inp.value = '';
      render();
    });

    render();
    bindGridKeynav(resultsEl);

    function render() {
      const list = rank(agents);
      const tokens = [];
      if (FilterState.query) {
        tokens.push(`<button class="chip chip--remove" type="button"
                       data-remove-filter data-axis="q" data-value="">
                       q: "${escapeHtml(FilterState.query)}"</button>`);
      }
      [['cat', TAXONOMY.categories], ['cls', TAXONOMY.classes], ['aff', TAXONOMY.affinities]]
        .forEach(([axis, tx]) => {
          for (const v of FilterState[axis]) {
            tokens.push(`<button class="chip chip--remove" type="button"
                          data-remove-filter data-axis="${axis}" data-value="${escapeHtml(v)}">
                          ${escapeHtml(tx[v]?.label || v)}</button>`);
          }
        });
      tokensEl.innerHTML = tokens.length
        ? tokens.join(' ')
        : `<span style="color: var(--realm-color-ink-soft); font-size: var(--core-font-size-14);">No active filters.</span>`;
      if (!list.length) {
        const hint = FilterState.aff.has('game')
          ? `Try removing 'Game(H)' or browse <a href="index.html">all categories</a>.`
          : `Try removing a filter or browse <a href="index.html">all categories</a>.`;
        resultsEl.innerHTML = `
          <div class="empty-state">
            <div class="empty-state__icon" aria-hidden="true">⌕</div>
            <p>No agents match your search.</p>
            <p class="empty-state__hint">${hint}</p>
          </div>`;
        if (countEl) countEl.textContent = `0 of ${agents.length}`;
        return;
      }
      resultsEl.innerHTML = `<div class="grid-cards" role="grid" aria-label="Search results">
        ${list.map(agentCardHtml).join('')}
      </div>`;
      if (countEl) countEl.textContent = `${list.length} of ${agents.length}`;
    }
  }

  async function bootMap() {
    const data = await DataStore.load();
    const agents = data.agents || [];

    const graphEl = document.querySelector('[data-map-graph]');
    const countEl = document.querySelector('[data-map-count]');
    const infoEl  = document.querySelector('[data-map-info]');
    const showAllEl = document.querySelector('[data-map-show-all-edges]');
    if (!graphEl) return;

    if (countEl) countEl.textContent = `${agents.length} agents`;

    let activeName = ((location.hash || '').replace('#', '') || '').toLowerCase() || null;
    let showAllEdges = false;

    function render() {
      graphEl.innerHTML = renderMapSvg(agents, activeName, showAllEdges);
      bindNodeEvents();
      if (activeName) scrollNodeIntoView(activeName);
    }

    function bindNodeEvents() {
      graphEl.querySelectorAll('[data-map-node]').forEach(el => {
        const name = el.dataset.mapNode;
        const onActivate = () => {
          activeName = name;
          render();
          showInfo(name);
        };
        el.addEventListener('mouseenter', onActivate);
        el.addEventListener('focus', onActivate);
      });
    }

    function showInfo(name) {
      if (!infoEl) return;
      const a = agents.find(x => x.name === name);
      if (!a) return;
      infoEl.hidden = false;
      const cls = TAXONOMY.classes[a.class];
      const cat = TAXONOMY.categories[a.category];
      const archLabel = cls ? cls.archetype : (a.archetype || a.class);
      const catLabel  = cat ? cat.label : a.category;
      const nameEl = infoEl.querySelector('[data-map-info-name]');
      const metaEl = infoEl.querySelector('[data-map-info-meta]');
      const descEl = infoEl.querySelector('[data-map-info-desc]');
      const linksEl = infoEl.querySelector('[data-map-info-links]');
      if (nameEl) nameEl.textContent = a.name;
      if (metaEl) metaEl.textContent = `${archLabel} · ${catLabel}`;
      if (descEl) descEl.textContent = a.description || '';
      if (linksEl) {
        linksEl.innerHTML = `
          <a class="btn btn--primary" href="detail.html?name=${encodeURIComponent(a.name)}">Open detail</a>
        `;
      }
    }

    function scrollNodeIntoView(name) {
      const node = graphEl.querySelector(`[data-map-node="${name}"]`);
      if (!node) return;
      try { node.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' }); }
      catch { /* old browser fallback */ }
    }

    if (showAllEl) {
      showAllEl.addEventListener('change', () => {
        showAllEdges = showAllEl.checked;
        render();
      });
    }

    window.addEventListener('hashchange', () => {
      const h = ((location.hash || '').replace('#', '') || '').toLowerCase();
      activeName = h || null;
      render();
      if (activeName) showInfo(activeName);
    });

    render();
    if (activeName) showInfo(activeName);
  }

  function renderMapSvg(agents, activeName, showAllEdges) {
    const byClass = agents.reduce((acc, a) => {
      (acc[a.class] = acc[a.class] || []).push(a);
      return acc;
    }, {});
    const classOrder = Object.keys(byClass).sort((a, b) => {
      const da = byClass[b].length - byClass[a].length;
      if (da !== 0) return da;
      return a.localeCompare(b);
    });

    const COL_W = 130;
    const ROW_H = 92;
    const TOP_PAD = 50;
    const SIDE_PAD = 40;
    const NODE_R = 24;

    const positions = new Map();
    classOrder.forEach((cls, ci) => {
      const list = byClass[cls];
      const cx = SIDE_PAD + ci * COL_W + COL_W / 2;
      list.forEach((a, ri) => {
        const cy = TOP_PAD + ri * ROW_H + ROW_H / 2;
        positions.set(a.name, { x: cx, y: cy, agent: a, cls });
      });
    });

    const W = SIDE_PAD * 2 + classOrder.length * COL_W;
    const maxRows = Math.max(0, ...classOrder.map(c => byClass[c].length));
    const H = TOP_PAD + maxRows * ROW_H + 60;

    const slug = (s) => String(s).replace(/[^a-zA-Z0-9_-]/g, '-');
    const patternDefs = [];
    const patIdMap = new Map();
    agents.forEach(a => {
      if (a.portrait && a.portrait.status === 'generated' && a.portrait.src) {
        const src = String(a.portrait.src).replace(/^\.\.\/portraits\//, 'assets/portraits/');
        const id = `map-pat-${slug(a.name)}`;
        patternDefs.push(
          `<pattern id="${id}" patternContentUnits="objectBoundingBox" width="1" height="1">` +
          `<image href="${escapeHtml(src)}" x="0" y="0" width="1" height="1" ` +
          `preserveAspectRatio="xMidYMid slice"/>` +
          `</pattern>`
        );
        patIdMap.set(a.name, id);
      }
    });

    const activeAgent = activeName ? agents.find(a => a.name === activeName) : null;
    const activePartners = new Set();
    if (activeAgent) {
      (activeAgent.collaboration?.input  || []).forEach(n => activePartners.add(n));
      (activeAgent.collaboration?.output || []).forEach(n => activePartners.add(n));
    }

    const edges = [];
    agents.forEach(a => {
      const showThis = showAllEdges || (activeAgent && activeAgent.name === a.name);
      if (!showThis) return;
      (a.collaboration?.input || []).forEach(n => {
        const from = positions.get(n);
        const to = positions.get(a.name);
        if (from && to) edges.push({ x1: from.x, y1: from.y, x2: to.x, y2: to.y, kind: 'in' });
      });
      (a.collaboration?.output || []).forEach(n => {
        const from = positions.get(a.name);
        const to = positions.get(n);
        if (from && to) edges.push({ x1: from.x, y1: from.y, x2: to.x, y2: to.y, kind: 'out' });
      });
    });

    const classLabels = classOrder.map((cls, ci) => {
      const cx = SIDE_PAD + ci * COL_W + COL_W / 2;
      const tx = TAXONOMY.classes[cls];
      const label = tx ? tx.label : (cls && cls !== 'null' ? cls : 'Unclassified');
      const count = byClass[cls].length;
      return `
        <text class="map-graph__class-label" x="${cx}" y="22"
              text-anchor="middle">${escapeHtml(label)}</text>
        <text class="map-graph__class-count" x="${cx}" y="36"
              text-anchor="middle">${count}</text>`;
    }).join('');

    const edgeSvg = edges.map(e =>
      `<line class="map-graph__edge map-graph__edge--${e.kind}"
        x1="${e.x1}" y1="${e.y1}" x2="${e.x2}" y2="${e.y2}"/>`
    ).join('');

    const nodeSvg = agents.map(a => {
      const p = positions.get(a.name);
      if (!p) return '';
      const patId = patIdMap.get(a.name);
      const fill = patId ? ` style="fill: url(#${patId})"` : '';
      const isActive = activeName === a.name;
      const isPartner = activePartners.has(a.name);
      const dim = activeName && !isActive && !isPartner;
      const nodeCls = [
        'map-graph__node',
        isActive ? 'map-graph__node--active' : '',
        isPartner ? 'map-graph__node--partner' : '',
        dim ? 'map-graph__node--dim' : ''
      ].filter(Boolean).join(' ');
      const labelCls = [
        'map-graph__node-text',
        dim ? 'map-graph__node-text--dim' : ''
      ].filter(Boolean).join(' ');
      return `
        <a href="detail.html?name=${encodeURIComponent(a.name)}"
           data-map-node="${escapeHtml(a.name)}"
           tabindex="0"
           class="map-graph__node-link"
           aria-label="${escapeHtml(a.name)}: ${escapeHtml(a.archetype || a.class)}">
          <circle class="${nodeCls}" cx="${p.x}" cy="${p.y}" r="${NODE_R}"${fill}/>
          <text class="${labelCls}" x="${p.x}" y="${p.y + NODE_R + 14}"
                text-anchor="middle">${escapeHtml(a.name)}</text>
        </a>`;
    }).join('');

    return `
      <svg class="map-graph__svg" viewBox="0 0 ${W} ${H}"
           preserveAspectRatio="xMidYMid meet" role="img"
           aria-label="Agent network map: ${agents.length} agents in ${classOrder.length} classes">
        <defs>${patternDefs.join('')}</defs>
        ${classLabels}
        ${edgeSvg}
        ${nodeSvg}
      </svg>`;
  }

  /* ---------- Boot dispatch ---------- */
  document.addEventListener('DOMContentLoaded', () => {
    Theme.init();
    const page = document.body.dataset.page;
    const router = { index: bootIndex, category: bootCategory, detail: bootDetail, search: bootSearch, map: bootMap };
    if (router[page]) router[page]().catch(err => {
      console.error('Page boot failed', err);
      const root = document.querySelector('[data-results], [data-detail], [data-roster]');
      if (root) {
        root.innerHTML = `<div class="empty-state">
          <p>Failed to load data. If you opened this from <code>file://</code>, try
          <code>python3 -m http.server</code> from the directory and visit
          <a href="http://localhost:8000/index.html">http://localhost:8000/index.html</a>.</p>
        </div>`;
      }
    });
  });
})();
