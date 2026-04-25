# Tilesheet Design Reference

Purpose: Author tile-based sheets for 2D maps and platformers. Cover tile size selection, autotile masks (16 / 47 / Wang / Blob), terrain transitions, atlas packing, and integration with Tiled, LDtk, Phaser tilemap, Godot TileMap, Unity 2D Tilemap.

## Scope Boundary

- **dot `tilesheet`**: Tile-based world tile design (this document).
- **dot `animation` (elsewhere)**: Character / sprite animation cycles.
- **dot `palette` (elsewhere)**: Palette constraint applied to tiles.
- **Quest (elsewhere)**: Game design level concepts.
- **Builder (elsewhere)**: Engine integration code (TileMap loaders).
- **Realm (elsewhere)**: Phaser-specific level rendering.

## Tile Size Selection

| Size | Era / use |
|------|-----------|
| 8×8 | NES, Game Boy, gameboy color, Pico-8 (with 2× upscale) |
| 16×16 | SNES, Mega Drive, classic JRPG, modern indie standard |
| 24×24 | Some indies (Hollow Knight UI, Stardew portraits) |
| 32×32 | Modern detailed pixel art, action platformers |
| 48×48 / 64×64 | Higher-resolution pixel-art (Owlboy-class) |

**Rule of thumb**: smallest tile that comfortably represents your detail. Doubling tile size quadruples art workload.

## Autotile Systems

Player-placed terrain edges should *automatically* pick the correct tile based on neighbors. The complexity of the system depends on edge richness needed.

### Wang 2-edge (Blob 4-bit, 16-tile)

Each edge of a tile is one of two states. Used for simple grass/dirt boundaries.

- 16 tiles total (2^4 corner combinations)
- Sufficient for hard grass-on-dirt edges with no diagonals

### 47-tile (RPG Maker / Tiled "Terrain")

Standard for top-down terrain with corners + edges + diagonals. Used by RPG Maker, Tiled, and most 2D engines.

- 47 unique tiles to cover all neighbor combinations including inner corners
- Stored in a 8-tile-wide × 6-tile-tall bitmask layout
- Each cell uses 4-bit corner + 4-bit edge mask (subset of 256 → 47 unique)

```
Bitmask layout (Tiled / RPG Maker MV style):
[NW][N][NE]      adjacent edges/corners → mask bit
[W ][C][E ]
[SW][S][SE]
```

### 16-tile Blob (corners only)

Each *corner* references a tile. 4 corners × 4 states = 16 tile candidates per corner.

- Used by Godot 4 Terrain Sets
- Cleaner result for organic shapes

### Wang 2-corner (255-tile)

Per-corner full Wang. Powerful but expensive to author.

### Selection

| Need | Choose |
|------|--------|
| Simple platformer ground | Wang 2-edge or 47-tile |
| RPG-style map (grass / sand / water) | 47-tile per terrain |
| Hand-painted organic edges | 16-tile blob (Godot) |
| Hex tiles | Hex 47-tile variant |

## Terrain Transitions

For multi-terrain interactions (grass↔sand, sand↔water), each terrain pair needs its own 47-tile set. Or use stacked terrain layers (sand-on-grass overlay) to compose without exponential growth.

```
LAYER STRATEGY (recommended):
Layer 0: base ground (grass)
Layer 1: sand-on-grass overlay (47 tiles)
Layer 2: water-on-sand overlay (47 tiles)

versus

ALL-PAIRS STRATEGY (avoid):
N terrains → N×(N-1)/2 transition sets
```

## Atlas Packing

Engines need a single image (texture atlas) with tiles laid out predictably.

| Layout | Use |
|--------|-----|
| Grid (uniform tile size) | Tiled .tsx, Phaser tilemap default |
| Bitmask layout (47-tile, fixed positions) | RPG Maker MV / MZ |
| Free-pack (TexturePacker) | Variable-size sprites only, NOT for tilemap |

**For tilemaps, always use uniform grid.** Engines compute tile index from grid position.

```
Grid example (16×16 tiles, 8 columns wide):
GID 1  2  3  4  5  6  7  8
GID 9  10 11 12 13 14 15 16
...
```

GID 0 is reserved for "no tile" in Tiled/TMX format.

## Engine Integration

### Tiled (.tsx + .tmx)

```xml
<tileset firstgid="1" name="terrain" tilewidth="16" tileheight="16">
  <image source="terrain.png" width="128" height="96"/>
  <wangsets>
    <wangset name="grass" type="mixed" tile="-1">
      <wangcolor name="Grass" color="#00ff00" tile="0" probability="1"/>
      <wangtile tileid="0" wangid="1,1,1,1,1,1,1,1"/>
      <!-- 47 entries -->
    </wangset>
  </wangsets>
</tileset>
```

### LDtk (.ldtk)

LDtk uses *Auto-Layer Rules* — pattern-based rather than wang. Author rules in the editor; LDtk applies them at runtime / export.

```json
{
  "rules": [
    { "tileIds": [1], "size": 1, "pattern": [1] },
    { "tileIds": [2,3,4], "size": 3, "pattern": [0,1,0,1,1,1,0,1,0] }
  ]
}
```

### Phaser 3 Tilemap

```javascript
this.load.image('tiles', 'assets/terrain.png');
this.load.tilemapTiledJSON('map', 'assets/level.json');

const map = this.make.tilemap({ key: 'map' });
const tileset = map.addTilesetImage('terrain', 'tiles');
const ground = map.createLayer('ground', tileset, 0, 0);
ground.setCollisionByProperty({ collides: true });
```

### Godot 4 TileMap (Terrain Sets)

```gdscript
# Resource: TileSet → Terrains tab
# Use blob 16-tile mode by default for clean organic edges
# Per-tile: mark corners as "Terrain N" or "Empty"
```

### Unity 2D Tilemap

Use `RuleTile` (asset) or `AnimatedRuleTile`. 47-tile pattern via `Sprite[]` array indexed by neighbor mask.

## Animated Tiles

Water, lava, torches — frames cycle on a timer.

```json
{
  "frames": [
    { "tileid": 12, "duration": 200 },
    { "tileid": 13, "duration": 200 },
    { "tileid": 14, "duration": 200 },
    { "tileid": 13, "duration": 200 }
  ]
}
```

Tiled supports per-tile animation natively. Phaser/Godot/Unity all consume it.

## Collision + Properties

Per-tile metadata:

| Property | Purpose |
|----------|---------|
| `collides: true` | Solid for physics |
| `oneway: true` | Pass-through from below (platforms) |
| `slope: 45` | Angled collision |
| `friction: 0.1` | Ice |
| `damage: 10` | Spike |
| `transition: water` | Trigger swim mode |

Define in Tiled tileset; engines read at load.

## Workflow

```
PLAN         →  tile size (8/16/32)
             →  terrain types (grass / sand / stone / water / ...)
             →  autotile system (Wang / 47-tile / blob)

PALETTE      →  inherit from dot `palette`
             →  per-tile color count discipline

KEY TILES    →  draw the central tile per terrain (full surround)
             →  ensure tileable seams

EDGE TILES   →  derive corners + edges + transitions
             →  follow chosen autotile bitmask layout

TEST         →  build a 16x16 cell test scene with all combinations
             →  visual continuity at each combination

ANIMATED     →  identify cycling tiles (water / lava / torch / leaves)
             →  4-frame default; consistent timing

PROPERTIES   →  collision per tile
             →  one-way platforms / slopes / damage
             →  custom properties for game logic

PACK         →  uniform grid atlas
             →  GID 0 reserved (no-tile)
             →  consistent column count

EXPORT       →  Tiled .tsx + .tmx
             →  LDtk .ldtk (with rules)
             →  Phaser tilemap JSON
             →  Godot TileSet resource

VALIDATE     →  paint a sample map; verify autotile correctness
             →  performance: ≤1 atlas per layer
             →  collision shape vs visual

HANDOFF      →  Builder: engine integration code
             →  Realm / Phaser: level rendering
             →  Quest: level design with tilesheet
             →  dot `palette`: palette compatibility
```

## Output Template

```markdown
## Tilesheet: [Project / Theme]

### Spec
- Tile size: [16×16]
- Sheet size: [128×96 / 8 cols × 6 rows]
- Terrain count: [N]
- Autotile system: [47-tile / blob / wang]

### Terrain Inventory
| Terrain | Cells | Pattern | Animated? |
|---------|-------|---------|-----------|
| grass | 0-46 | 47-tile | no |
| water | 47-50 | wang 2-edge | yes (4 frames) |
| stone | 51-97 | 47-tile | no |
| ... | ... | ... | ... |

### Bitmask Layout
[ASCII / image showing tile positions per autotile mask]

### Properties
| Tile | Property | Value |
|------|----------|-------|
| 50 | collides | true |
| 50 | one-way | true |
| 80 | damage | 10 |

### Animated Tiles
| Base | Frames | Timing |
|------|--------|--------|
| water (47) | 47, 48, 49, 48 | 200ms each |
| torch (60) | 60, 61, 62 | 100ms each |

### Engine Outputs
- Tiled: terrain.tsx + sample.tmx
- LDtk: project.ldtk with auto-rules
- Phaser: phaser-tilemap.json
- Godot: TileSet.tres
- Unity: RuleTile.asset

### Palette
- Inherits: [palette name from dot palette]
- Per-tile color budget: [4-6]

### Validation
- Autotile coverage: all 47 cells unique [yes/no]
- Tile seam continuity: [pass / fail]
- Collision-shape vs visual mismatch: [list]
- Animated-tile timing: [consistent/varied]

### Handoffs
- Builder: tile loader integration
- Realm / Phaser: in-game rendering
- Quest: level design constraints
- dot `palette`: ensure tile palette match
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Non-tileable seams between adjacent same-terrain tiles | Test with 4-tile-square sample; fix seam |
| 47-tile authored without bitmask reference | Always use a bitmask cheat sheet |
| Variable tile sizes in same atlas | Uniform grid mandatory for tilemap engines |
| GID 0 used as a real tile | Reserve GID 0 = no-tile |
| All terrains as separate atlases (no batching) | Combine into one atlas per layer |
| Animated tiles with non-uniform frame size | Animated frames must share size |
| One-way platform without `oneway` flag | Set per-tile property; engines read it |
| 47-tile per all transitions (N²) | Layer-overlay strategy reduces art exponentially |
| Non-power-of-2 atlas size on mobile | Pad to POT (e.g., 256×256) for older mobile GPUs |
| Tile palette drift across sheets | Lock palette via dot `palette` first |
| Auto-rules in LDtk without test scene | Always paint a sample; rules can over-trigger |
| Heavy dithering on tiles | Tiles tile; dither creates seam artifacts |
| Forgetting collision shape for slopes | Slopes need polygon collision, not AABB |
| One mega-tilesheet without theme grouping | Group by biome / floor for cache efficiency |
| Per-tile rotation in atlas (over-pack) | Engines support flip flags; don't pre-rotate |
| Ignoring tile metadata serialization | Tiled .tsx is the canonical exchange format |

## Deliverable Contract

When `tilesheet` completes, emit:

- **Tile size + sheet dimensions + terrain count + autotile system**.
- **Terrain inventory** with cell ranges + pattern + animation flags.
- **Bitmask layout** documentation.
- **Per-tile properties** (collision / damage / one-way).
- **Animated tiles** definitions.
- **Engine outputs** (Tiled / LDtk / Phaser / Godot / Unity).
- **Palette inheritance** from dot `palette`.
- **Validation** (autotile coverage, seam, collision).
- **Handoffs**: Builder, Realm, Quest, dot palette.

## References

- Tiled — mapeditor.org (de-facto tilemap editor)
- LDtk — ldtk.io (modern alternative with auto-rules)
- RPG Maker MZ tile spec — kadokawagames.co.jp
- Wang tile reference — gamedev.net/articles/programming/general-and-gameplay-programming/wang-tiles
- *Tiles, Stitches, and Beyond* — Cris Sevilleja
- "How to Use Tile Bitmasking to Auto-Tile" — gamedev.net (Stagecast Creator origin)
- Phaser 3 Tilemap manual — phaser.io/docs/3
- Godot 4 TileMap docs — docs.godotengine.org
- Unity 2D Tilemap manual — docs.unity3d.com
- Tiled TMX format — doc.mapeditor.org
- LDtk file format — github.com/deepnight/ldtk
- "47-tile autotile bitmask" — RPG Maker community references
- Hyper Light Drifter, Stardew Valley, Celeste tilemap postmortems
- Brackeys Godot TileMap tutorials (YouTube)
- Sebastian Lague — procgen tilemap series
- *Game Programming Patterns* — Robert Nystrom (Spatial Partition chapter)
- TexturePacker — codeandweb.com (sprite atlas tool, not for grid tilemaps)
