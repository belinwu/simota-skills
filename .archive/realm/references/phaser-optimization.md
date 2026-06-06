# Phaser 3 Optimization & Best Practices

Purpose: Preserve Realm's Phaser-specific performance rules, rank-based sprite sizing, and version guidance for the game template.

Contents:
- Performance principles
- Object pooling
- Tilemap option
- Animation and sprite sizing
- Version policy
- Upgrade priorities

## Performance Principles

| # | Technique | Realm use |
|---|---|---|
| 1 | FPS counter | Show FPS in live mode when debugging |
| 2 | Object pooling | Reuse agent sprites and particles |
| 3 | Reference caching | Cache department and agent lookups |
| 4 | Loop optimization | Update only the visible area |
| 5 | Asset compression | Prefer atlases over many small textures |
| 6 | Lazy loading | Defer off-screen department details |
| 7 | Canvas/WebGL fallback | Improve compatibility and lower-end performance |

## Object Pooling

- Use Phaser `Group` objects as sprite pools.
- Target pool size: around 100 entities to support `60+` active agents plus effects.
- Despawn instead of destroying transient sprites wherever possible.

## Tilemap / Procedural Layout Option

This is an optional upgrade path, not the baseline layout:
- Start from a central lobby (`Command Center`).
- Place strongly collaborating departments adjacent to each other.
- Connect departments with corridor paths.
- Support fog, darkening, or other health-based room styling only if it does not hide essential status.

## Animation State Machine

| State | Frames | Rate |
|---|---|---|
| `idle` | `[0, 1]` | 2 |
| `walk` | `[2, 3, 4, 5]` | 8 |
| `work` | `[6, 7]` | 4 |
| `celebrate` | `[8, 9, 10, 11]` | 12 |
| `battle` | `[12, 13, 14]` | 10 |

### Rank-Based Sprite Size

| Rank | Size | Effect |
|---|---|---|
| F-E | `12×12` | No aura |
| D-C | `16×16` | Walking shadow |
| B-A | `20×20` | Subtle glow |
| S | `24×24` | Gold aura |
| SS | `28×28` | Rainbow particles |

## Version Policy

| Version | Release | Notes |
|---|---|---|
| 3.80 | 2024-02 | Particle improvements |
| 3.85 | 2024-09 | `ParticleEmitter` GameObject support |
| 3.87 | 2025-02 | Particle and stability fixes |
| 3.90.0 | 2025-05 | "Tsugumi" — **final Phaser 3 release**; no further v3 development planned ([phaser.io/download/stable](https://phaser.io/download/stable)) |
| 4.0.0 | 2026-04-10 | "Caladan" — first stable Phaser 4 release; TypeScript-native, RenderNode architecture, SpriteGPULayer (up to 100x faster than v3 standard rendering in single draw call) ([GitHub release](https://github.com/phaserjs/phaser/releases/tag/v4.0.0)) |
| 4.1.0 | 2026-04-30 | "Salusa" — smarter rendering, ESM fixes, reworked Layer ([phaser.io/download/release/v4.1.0](https://phaser.io/download/release/v4.1.0)) |

Action: use Phaser `3.90.0` for existing Realm templates. **Use Phaser 4 (v4.1.0) for all new builds** — it is now stable. Migration from v3: standard sprite/tilemap/text scenes migrate in hours; custom WebGL pipelines must be rewritten as RenderNodes. Breaking changes: `setTintFill()` removed; `roundPixels` defaults to false; texture Y-axis orientation changed (GL-native). See [migration guide](https://phaser.io/news/2026/04/migrating-from-phaser-3-to-phaser-4-what-you-need-to-know) and [renderer deep-dive](https://phaser.io/news/2026/04/phaser-4-renderer-faster-cleaner-and-built-for-modern-games).

## Upgrade Priorities

| Priority | Upgrade | Cost | Benefit |
|---|---|---|---|
| P0 | Object pooling | Small | Major performance improvement |
| P0 | Existing templates: stay on Phaser `3.90.0` | Zero | Stability (final v3) |
| P0 | New builds: use Phaser 4 (`v4.1.0`) | Small | RenderNode perf, TypeScript, SpriteGPULayer |
| P1 | Animation state machine | Medium | Better clarity and charm |
| P1 | Canvas/WebGL fallback | Small | Better compatibility |
| P2 | Migrate custom v3 WebGL pipelines to v4 RenderNodes | Large | Required for v4 compatibility |
| P2 | Tilemap migration | Large | More flexible layout |
| P2 | Procedural sprite generation | Medium | Better rank/class differentiation |
