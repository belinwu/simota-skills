# Roblox Platform Game Design

## Purpose

Roblox is a UGC-first platform with its own economy (Robux / DevEx), discovery algorithm, content-maturity regime, and AI-assisted creation surface (Studio Assistant + built-in MCP server). Designs that treat Roblox as "just another mobile game" miss the structural differences: mobile-dominant sessions, multi-game session loops, server-authoritative anti-exploit constraints, age-verification-gated communication, and a discovery funnel where icon CTR is a first-class design variable. Use this reference whenever the target platform is Roblox, the request involves Robux pricing / DevEx payout, or the workflow can be grounded against an open `.rbxl` via the Roblox Studio MCP server.

## Scope Boundary

- IN scope: Roblox-native genre conventions, Robux ↔ USD math, DevEx eligibility, Content Maturity Labels, age-verification implications for design, Studio MCP-grounded design recommendations (read-only tool set), Cube 3D / Code Assist / Assistant integration boundaries, discovery-algorithm-aware design (icon CTR, recommended-for-you signals), platform-specific compliance (Brazil ECA Digital + EU DSA), mobile-first performance budgets, Roblox Kids / Select / Plus account tiers.
- OUT of scope: Luau implementation code (delegate to `builder`), Studio plugin engineering (delegate to `builder`), `.rbxl` automation scripts (delegate to `builder`), MCP server deployment / hardening (delegate to `gear` or `latch`), avatar / mesh authoring pipelines (delegate to `clay` or asset specialists), Roblox ToS legal interpretation beyond the table below (consult counsel), engineering benchmarks for Luau performance (out of design scope).

## Source Tier Posture

All numeric claims in this reference are dated. Re-verify quarterly against the [Roblox IR newsroom](https://about.roblox.com/newsroom/) and [DevForum announcements](https://devforum.roblox.com/c/announcements/49). The Roblox platform's monetization rules, age-verification scope, and AI-tool surface change faster than most platforms — treat any fact >6 months old as "verify before designing on it."

---

## 1. Platform & Audience (as of 2026 Q1)

| Metric | Value | As of | Source tier |
|--------|-------|-------|-------------|
| DAU (avg) | 132M (+35% YoY) | 2026 Q1 | T1 (Roblox shareholder letter) |
| Hours engaged | 31B / quarter (+43% YoY) | 2026 Q1 | T1 |
| Peak DAU | 152M | 2025 Q3 | T1 |
| Revenue / Bookings | $1.4B / $1.7B | 2026 Q1 | T1 SEC 8-K |
| Daily session length | ~2.7-2.8h per DAU | 2025 Q2-Q3 | T2 |
| Mobile share of sessions | ~80% | 2026 | T3 (T1 earnings summary) |
| Mobile share of revenue | >52% | 2026 | T3 |
| Console share | ~3% (Roblox does not break out PS5 / Xbox / Switch separately) | 2026 | T1 lump |
| Age 17+ share (all reported users) | ~44% | 2026 | T2/T3 — methodology varies |
| Age-verified DAUs: 13-17 / 18+ | ~38% / ~27% (of the ~45% who completed age check) | early 2026 | T1 newsroom |

**Session loop reality.** A Roblox session is rarely one game. The default loop is *lobby → game A → social/Home → game B*. ~50% of players open Roblox 2+ times/day; ~25% 3+ times/day. **Designing for "a single 30-minute session" loses the bottom 75% of the funnel.** Bottom-quartile session is ~2 minutes; top 5% is 37+ minutes.

**Platform reach beyond mobile/desktop.**
- PS5 native app launched 2026-04-14 — ~30% faster load, DualSense haptics; previously cloud-streamed since 2023-10.
- Meta Quest 2 / 3 / Pro supported since 2023-10-30; **minimum age 10+** on VR.
- Switch: cross-platform via standard Roblox client.

---

## 2. Robux Economy & DevEx

### Robux ↔ USD reference table (as of 2026)

| Direction | Rate per Robux | Per 1,000 Robux | Notes |
|-----------|----------------|-----------------|-------|
| **Purchase** (player buying) | ~$0.0125 | ~$12.50 | Varies by SKU; web vs mobile platform fee can shift effective rate |
| **DevEx payout** — earned **after 2025-09-05** | $0.0038 | $3.80 | +8.5% increase announced at RDC 2025 |
| **DevEx payout** — earned **before 2025-09-05** | $0.0035 | $3.50 | Legacy rate |

- DevEx **minimum payout**: 30,000 earned Robux (≈$114 at new rate)
- DevEx eligibility: Roblox Premium subscription (now Roblox Plus for new signups, see below), age 13+, account in good standing, U.S./Canada/EU/UK/select other regions
- Roblox Plus replaces Premium for **new signups** as of 2026-04-30 ($4.99/mo); existing Premium subscribers grandfathered. DevEx eligibility flows from whichever subscription is active.

### Revenue share

| Surface | Creator share | Platform cut |
|---------|---------------|--------------|
| Game Passes | 70% | 30% |
| Developer Products (consumables) | 70% | 30% |
| Avatar Marketplace items | 30%-70% tiered by price-vs-floor multiplier (max 70% at ≥6× floor) | inverse |
| Subscriptions within Experiences | 70% (less platform fees on iOS/Android in-app billing) | 30% + IAP fees |
| Limited UGC resales | 10% perpetual royalty to original creator | rest split per platform |

- Engagement-Based Payouts **deprecated 2025-07-24** → replaced by **Creator Rewards Program** (multi-metric: engagement + monetization + retention, not just Premium time-spent).
- Creator payouts crossed **$1B annual** for the first time in 2025.

### Monetization surfaces inside experiences

1. **Game Passes** — permanent unlocks (one-time purchase).
2. **Developer Products** — consumables, repeatable purchase.
3. **Private Servers** — recurring rental, creator-priced.
4. **Subscriptions within Experiences** — Robux or local currency, GA since 2024 and expanded at RDC 2025. Use for sustained value (battle-pass-style, monthly cosmetics drops, premium currency drips).
5. **Limited UGC collectibles** — 30-day holding period before resale; creator earns 10% royalty on every secondary trade. Top-tier limiteds trade at 5-20× original price.

### Designer-relevant economy rules

- **Sink Coverage** still applies (95-105% from `economy-design.md`), but on Roblox the Robux economy is closed inside each experience — the platform is the only true sink for Robux outside the experience. Inside the experience, design soft and hard sinks for the **in-game currency**, not for Robux directly.
- **Mobile IAP friction is real**: ~80% of sessions are mobile and Apple/Google take their own cut on top of Roblox's 30%. Effective creator share on mobile IAP can fall below 50%. Account for this in LTV models.
- **Subscription churn is the new lever**: post-2024 in-experience subscriptions reward retention design more than one-time Game Passes.

---

## 3. Roblox-Native Design Patterns

### Genre conventions

| Genre | Core verb | Retention spine | Reference titles |
|-------|-----------|-----------------|------------------|
| **Simulator** | Repeated single action (fish/mine/train) | Stat progression + rebirth resets | many; pattern dominant 2022-2026 |
| **Tycoon** | Build → automate → throughput | Automation is the single biggest retention driver post-day-3 (2024-2026) | Retail Tycoon, Theme Park Tycoon |
| **Obby** | Skill-based parkour, short retry | Short-loop dopamine; highest concurrent-player genre | Tower of Hell |
| **Hangout / RP** | Social presence + customization | Identity + social validation | MeepCity (first to 1B), Brookhaven, Adopt Me! |
| **Story games** | Branching narrative | Single-session arcs, replay for variants | Piggy, The Mimic |
| **Horror** | Tension + jumpscare loop | Co-op session social proof | Doors, The Mimic |
| **Tower Defense** | Wave-based strategic placement | Meta-progression unlocks | TDS, All-Star Tower Defense |

**Viral DNA pattern in 1B+ visit titles**: trivially-learnable verb in <30 sec → persistent-progress hook within 60 sec → other players visible/relevant → short-loop reward cadence aligned to multi-session daily habit. **Grow a Garden** (built in 3 days by a 16-year-old) hit **22.3M concurrent users on 2025-08-23** and generated $12M in May 2025 alone — proof that the platform still rewards mechanically-tight idle-progression loops over polish.

### Discovery algorithm (T1)

The Home page uses a two-stage "Recommended For You" ranker. Signals that move impressions:
1. **Game-side changes** — updates, new content (creator-controlled).
2. **Signal changes** — retention, monetization, friend-plays (engagement-derived).
3. **Roblox-side algorithm changes** — periodic re-tuning (uncontrollable).
4. **Total Home traffic** — seasonality (uncontrollable).

**Charts (Popular / Top Rated)** are aggregate-engagement driven, not personalized.

**Icon CTR is a first-class design variable**:
- Acquisition page shows **Home Recommendations Conversion Rate** so creators can A/B icons against impression→play conversion.
- **Thumbnail personalization** launched Nov 2024 — Roblox picks per-user which icon variant to show. Design 3-5 icon variants per experience, not one.
- **Icon & thumbnail text auto-translation** experiment launched Aug 2024 to lift international CTR. Localized icons matter for non-English markets.

### Onboarding norms

- **30 seconds** to convince a new player to stay.
- Most leavers leave within the first **2 minutes**.
- Patterns that work on Roblox specifically:
  - Instant action in <10 sec (no mandatory cutscene).
  - First reward in <60 sec.
  - Contextual tutorials triggered by zone entry, not modal walls.
  - Early social proof — show other players in-frame.
- **Update cadence**: weekly events / seasonal passes are *table stakes* for retention-focused titles. A static experience that doesn't ship updates loses its discovery slot.

---

## 4. Technical Constraints Affecting Design

(High-level only — designers, not engineers.)

- **Luau** is Roblox's typed, sandboxed Lua dialect. Treat per-frame `Heartbeat` work and instance creation as expensive. Replication-heavy designs that fire many small RemoteEvents are mobile-hostile.
- **Workspace instance budget**: aim for **<5,000 instances** during active play; 15,000-20,000 is "almost always struggling on mobile." Designs that imply thousands of dynamic props need a culling/streaming plan in the spec.
- **Server authority is mandatory** for any value the player can exploit (currency, position-based rewards, score). The design rule: *validate on server, render on client* for anything monetized. Anti-exploit needs dictate that "client predicts, server confirms" must be in the spec, not bolted on later.
- **Mobile-first is non-negotiable**: 80% of sessions are mobile. UI must work at touch density (44pt minimum tap target). Particle counts, dynamic lighting modes (ShadowMap vs Compatibility vs Voxel), and shadow detail must be designed for low-end Android baseline.
- **Cube 3D Mesh Generation API** (beta, 2025-03) — designers can prototype 3D assets from text prompts inside Studio *and* at runtime via Lua API. Open-sourced March 2025 on HuggingFace/GitHub (arXiv:2503.15475). Tokenizes 3D objects autoregressively rather than via image reconstruction.

---

## 5. Compliance & Safety (2026)

### Content Maturity Labels (replaced old Experience Guidelines on 2024-11-18)

| Label | Allowed content (summary) | Age gate |
|-------|---------------------------|----------|
| **Minimal** | Occasional mild violence, light unrealistic blood, occasional mild fear | All ages |
| **Mild** | Repeated mild violence, heavy unrealistic blood, mild crude humor | 9+ |
| **Moderate** | Moderate violence, light realistic blood, **unplayable** gambling, moderate fear | 13+ |
| **Restricted** | Strong violence, heavy realistic blood, romantic themes, alcohol, strong language | **18+ only, requires facial or ID age verification** |

- **2025-09-30**: unrated experiences became **unplayable** — every public experience must complete the Maturity & Compliance Questionnaire.
- **2025-2026**: age limit for Restricted experiences raised from 17→18; social-hangout experiences depicting private spaces tightened.

### Age verification (2025-2026)

- **Facial Age Estimation bands**: Under 9 / 9-12 / 13-15 / 16-17 / 18-20 / 21+
- Communication features (chat, voice, links, Studio Team Create) now require age check globally. US rollout Dec 2025; global through Jan 2026.
- **2026-04**: introduced **Roblox Kids** (ages 5-8, Minimal/Mild only, all comms off by default) and **Roblox Select** (9-15, up to Moderate) account types, rolling out early June 2026.

### Paid random items policy (loot box / gacha)

- Defined broadly: any Robux-purchasable item granting random outcomes, **including** indirect chains (Robux → in-game currency → random pull).
- Must be disclosed in the Maturity & Compliance Questionnaire. Designs that include them push toward Moderate/Restricted.
- **Brazil-specific (ECA Digital, Lei 15.211/2025)**: under-18s cannot access paid-random mechanics; creators must use built-in tools to gate by age verification. Enforcement via ANPD up to R$ 50M / 10% of Brazilian revenue (see `references/monetization-design.md`).
- Cross-reference: **EU DFA** (Q4 2026 Work Programme, application ~2029), **PEGI 2026-06** (paid random items → minimum PEGI 16), **South Korea GIPA Article 38-2** (immediate surcharge), **Belgium prohibition**. All apply to Roblox creators publishing in those regions.

### Other regulatory

- **EU DSA**: Roblox publishes annual transparency reports; legal rep is DP-Dock Netherlands BV. Creators are downstream of Roblox's compliance posture but still responsible for individual experience content.
- **COPPA**: Roblox claims compliance; biometric collection for under-13 facial scans is an active concern under the updated 2024 COPPA Rule.
- **Generative AI policy**: Roblox enforces "AI-Based Tools Supplemental Terms and Disclaimer" for any creator using Assistant or other generative tools. Disclosure expectations apply to AI-generated UGC submissions — flag in every spec that uses AI-generated assets.

---

## 6. Roblox Studio MCP Server (Designer's Lens)

The Roblox Studio MCP server lets a quest-style agent **ground design recommendations in the actual `.rbxl` place state** instead of guessing. This section covers ONLY the read-only, designer-relevant tools. Builder-facing tools (`execute_luau`, `multi_edit`, input simulation, asset generation) are out of scope here — delegate those to `builder`.

### Status & history

| Date | Milestone |
|------|-----------|
| 2025-05-13 | Open-source standalone Rust MCP server released (Claude Desktop + Cursor) |
| 2026-02-21 | Open-source server gains `get_console_output`, `start_stop_play`, `run_script_in_play_mode`, `get_studio_mode` |
| 2026-03-05 | **"Studio Built-in MCP Server and Playtest Automation"** — server moves natively into Studio, gains full tool surface |
| 2026-04-03 | Standalone repo archived (read-only); built-in server is the only supported path going forward |

- **Maintainer**: Roblox Corporation (first-party). Anthropic provides the MCP standard only.
- **Stability**: Built-in server is GA (shipping in Studio Assistant). Multi-Studio routing (`list_roblox_studios` / `set_active_studio`) is flagged experimental.
- **License**: Standalone repo MIT; built-in server proprietary (ships with Studio).
- **Supported MCP clients** (as of 2026-05): Claude Desktop, Claude Code, Cursor, VS Code, Antigravity (agy), Codex CLI, Gemini CLI.

### Designer-relevant tools (read-only, safe for no-code agents)

| Tool | Purpose | Designer use |
|------|---------|--------------|
| `search_game_tree` | Query Instance hierarchy | Real counts of NPCs, weapons, zones — ground design briefs in actual scene |
| `inspect_instance` | Detailed properties of an Instance | Verify configured values match design spec |
| `script_read` | Read a script's source (optional line range) | Reconnaissance before writing design briefs that touch existing systems |
| `script_search` | Fuzzy search for scripts by name | Locate the right module before recommending changes |
| `script_grep` | Pattern search across all scripts | Audit usage of a constant / pattern across the codebase |
| `console_output` | Read Studio console/runtime logs | Verify balance behavior during playtest observation |
| `screen_capture` | Screenshot viewport | Design reviews, layout audits, mood checks |
| `start_stop_play` | Start/stop Play, Run-Server modes | Observe a playtest without authoring automation |
| `insert_from_creator_store` | Insert Creator Store / Marketplace asset | Pull reference assets for spec comparison |
| `explore_subagent` | Spawns parallel investigation subagent that returns a summary | Delegate "summarize how X is organized" passes |
| `list_roblox_studios` | Enumerate connected Studio instances | Multi-place workflows |
| `set_active_studio` | Select active Studio for subsequent calls | Multi-place workflows |

### Builder-only tools (do NOT call from quest)

`execute_luau`, `multi_edit`, `playtest_subagent`, `character_navigation`, `keyboard_input`, `mouse_input`, `generate_mesh`, `generate_material`, `generate_procedural_model`. These mutate the place or execute code — delegate to `builder` with an explicit handoff brief.

### Setup (for designer awareness)

The MCP server runs as a local binary launched by the MCP client over stdio. Studio must be running with **Assistant → Manage MCP Servers → "Enable Studio as MCP server"** toggled on. Green indicator confirms a client has connected.

**macOS Claude Code / Desktop config snippet:**

```json
{
  "mcpServers": {
    "Roblox_Studio": {
      "command": "/Applications/RobloxStudio.app/Contents/MacOS/StudioMCP"
    }
  }
}
```

**Windows:**

```json
{
  "mcpServers": {
    "Roblox_Studio": {
      "command": "cmd.exe",
      "args": ["/c", "%LOCALAPPDATA%\\Roblox\\mcp.bat"]
    }
  }
}
```

- **Transport**: stdio.
- **Authentication**: None. Local-only trust model — whoever can launch the binary can drive Studio. No Roblox API key, OAuth, or cookie required.
- **Multi-Studio**: single client can attach to multiple open Studios; auto-routes by default.

### Designer-side risk posture

- **Trust boundary is the MCP client**. Roblox docs explicitly warn that connected clients can "read and modify content in your open Roblox places" — there is no per-tool consent prompt inside Studio. **Treat any MCP-connected place as if the client could exfiltrate scripts and assets.**
- **Privacy**: server is local-only with no Roblox-side telemetry, but transcripts sent to a third-party LLM client (Claude, GPT, Gemini) leave the machine and follow that vendor's policy. **Place contents and script source can be exfiltrated by a malicious client.**
- **No ACL**: any local process that can launch the binary can drive Studio while the toggle is on. Disable the MCP toggle when not in active use, especially on shared workstations.
- **Multi-Studio routing is experimental**: tool routing across several open Studios can be ambiguous; use `set_active_studio` as a manual escape hatch.
- **Standalone repo is archived (2026-04-03)** — bug fixes / new tools land only in the built-in server.
- **No published quotas** — full-tree dumps on very large places and `script_grep` across thousands of scripts can be slow.
- **Roblox ToS**: no MCP-specific exception. Standard Studio / Creator ToS applies; automated mass-publishing via MCP-driven Luau falls under existing automation restrictions.

### Related tools (don't confuse with MCP)

- **Roblox Assistant** (built-in): Studio's first-party AI; since 2026-02-21 supports bring-your-own keys for Claude / OpenAI / Gemini. **Uses the same MCP toolset internally** — "every MCP tool available in Assistant is automatically available through the built-in MCP Server."
- **Roblox Code Assist**: in-editor code completion / chat. Predates MCP. Not an MCP server.
- **Community MCP servers** (T3, unofficial): `boshyxd/robloxstudio-mcp`, `drgost1/robloxstudio-mcp` (51 tools), `hope1026/weppy-roblox-mcp`, `rbx-mcp-hub`. **Treat as third-party supply-chain risk** — not endorsed by Roblox. Cross-reference `chain` skill before recommending.

---

## 7. Player Psychology on Roblox

- **Bartle skew**: anecdotally Socializer + Explorer dominant on Roblox (driven by hangout/RP/obby genre mix), **but no peer-reviewed or Roblox-published distribution is available**. Flag as anecdotal in spec.
- **Session psychology**: multi-game session loop means the player is *one click from leaving*. Every loading screen, every modal, every friction point is competing with one-tap exit to Home.
- **Social proof primacy**: visible other-player presence in the experience is a stronger retention signal on Roblox than on most platforms. "Empty-server problem" kills new experiences faster than poor mechanics.
- **Identity over achievement**: avatar customization, owned UGC items, displayed social status (friend count, group membership) are first-order motivators alongside achievement progression.

---

## 8. Quest Design Checklist for Roblox Projects

Use this checklist alongside the standard quest workflow (`DISCOVER → FRAME → DESIGN → VALIDATE → DELIVER`):

**DISCOVER additions:**
- [ ] Target Roblox **maturity label** identified (Minimal / Mild / Moderate / Restricted) — drives every downstream content decision.
- [ ] Mobile-first vs cross-platform decision documented (80% mobile sessions is the default assumption).
- [ ] Discovery target genre / chart identified — informs icon design and the 30-sec onboarding hook.
- [ ] Roblox Studio MCP availability checked — if `.rbxl` is accessible via MCP, use `search_game_tree` / `inspect_instance` to ground the spec.

**FRAME additions:**
- [ ] Icon CTR strategy (3-5 variants planned, not one).
- [ ] Update-cadence commitment (weekly events / seasonal pass).
- [ ] Mobile UI density verified at 44pt minimum touch target.

**DESIGN additions:**
- [ ] Robux pricing math uses 2026 rates ($0.0125/Robux purchase, $0.0038/Robux DevEx payout).
- [ ] If randomized rewards: paid-random-items policy compliance + regional age-gate plan (Brazil ECA Digital, PEGI 16, EU DFA awareness).
- [ ] Server-authoritative validation explicitly designed for any monetized or exploitable value.
- [ ] Workspace instance budget (<5,000 active) is in the spec.
- [ ] If AI-generated assets: Roblox AI-Based Tools Supplemental Terms disclosure plan.

**VALIDATE additions:**
- [ ] Anti-pattern check vs `references/anti-patterns.md` (standard).
- [ ] Maturity Questionnaire dry-run — what label does the design actually score?
- [ ] If MCP-grounded: `console_output` and `screen_capture` evidence attached to the spec.

**DELIVER additions:**
- [ ] Asset briefs for Tone (audio) / Dot (2D icons + UI) / Clay (3D models or Cube 3D prompts) routed appropriately.
- [ ] Builder handoff includes MCP tool boundary — designer-side tools were used to ground; `execute_luau` / `multi_edit` are the builder's surface.
- [ ] DevEx payout projection included in monetization deliverable when applicable.

---

## 9. Anti-Patterns Specific to Roblox

| Anti-pattern | Why it fails | Fix |
|--------------|--------------|-----|
| **Designing for desktop input first** | 80% of sessions are mobile touch; desktop hover/right-click UX falls apart | Design touch-first; verify with mobile-emulator playtest |
| **One static icon** | Thumbnail personalization picks per-user; one icon means no A/B signal | Ship 3-5 icon variants from day one |
| **Modal-wall tutorial** | Roblox players exit within 2 min; modal walls compound exit risk | Contextual zone-triggered tutorials, instant action <10 sec |
| **No update cadence** | Static experiences lose discovery slot regardless of initial quality | Plan weekly events / seasonal passes before launch |
| **Robux-priced cosmetics only** | Lower ARPU than systems with consumable + subscription mix | Layer Game Passes + Developer Products + Subscriptions |
| **Server-trust on currency** | Exploiters destroy economy within days | Server-authoritative validation in the spec, not bolted on |
| **Restricted-tier design without age-gate plan** | Experience becomes unplayable for unverified users (majority) | Either design at Moderate ceiling or accept Restricted's verified-only audience |
| **Paid random items targeting under-13** | Brazil ECA / PEGI / DFA exposure + Roblox internal policy | Either remove randomness or hard-gate by age verification |
| **AI-generated assets without disclosure** | Violates Roblox AI-Based Tools Supplemental Terms | Disclose in submission + Maturity Questionnaire |
| **MCP-driven mass publishing** | Falls under Roblox automation restrictions in standard ToS | Use MCP for design grounding + builder workflows, not for production publishing automation |
| **Treating Roblox as "just mobile"** | Misses session-loop economics, discovery algorithm, age-verification regime | Use this reference; do not import generic mobile F2P playbooks wholesale |

---

## 10. Handoff Targets

- **Builder** — when the design implies Luau implementation, Studio plugin work, or `.rbxl` automation (including MCP `execute_luau` / `multi_edit` usage).
- **Tone** — audio briefs for SFX, BGM, ambient. Roblox supports streaming audio with creator-uploaded assets subject to moderation.
- **Dot** — 2D icon variants (3-5 per experience), UI sprites, marketplace thumbnails. Critical for Home Recommendations CTR.
- **Clay** — 3D model briefs. Optionally route as Cube 3D prompts for in-Studio generation.
- **Schema** — data model for in-experience persistence (DataStore design, player profile shape).
- **Radar** — test specs for game mechanics; pair with `voyager` if E2E flows across Studio + Play mode are needed.
- **Accord** — integrated spec packages when the design spans multiple disciplines.
- **Chain** — supply-chain audit before recommending any unofficial / community MCP server.
- **Gear** / **Latch** — MCP server deployment, hook configuration, or CI integration.
- **Cloak** — privacy review when the experience collects under-13 data or uses Facial Age Estimation results.
- **Comply** — broader regulatory check beyond loot-box compliance.

---

## 11. Reference URLs (re-verify quarterly)

- Roblox Newsroom: https://about.roblox.com/newsroom/
- Roblox Creator Docs: https://create.roblox.com/docs
- Studio MCP docs: https://create.roblox.com/docs/studio/mcp
- DevForum Announcements: https://devforum.roblox.com/c/announcements/49
- Content Maturity Labels: https://en.help.roblox.com/hc/en-us/articles/8862768451604
- DevEx: https://en.help.roblox.com/hc/en-us/articles/13061189551124
- Paid Random Items Policy: https://devforum.roblox.com/t/paid-random-items-policy/4030080
- Discovery / Recommended For You: https://devforum.roblox.com/t/boost-your-discovery-with-the-improved-recommended-for-you-algorithm-and-analytics-for-creators/3587441
- Cube 3D announcement: https://about.roblox.com/newsroom/2025/03/introducing-roblox-cube
- Brazil ECA Digital: https://en.help.roblox.com/hc/nl/articles/48706630819476-Brazil-Digital-ECA-Updates
- EU DSA: https://en.help.roblox.com/hc/en-us/articles/13061336948244-EU-Digital-Services-Act
