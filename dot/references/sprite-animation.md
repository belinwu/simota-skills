# Sprite Animation Reference

スプライトシートのレイアウト規則、アニメーションフレーム設計、メタデータ仕様、アニメーション原則。

---

## Spritesheet Layout Rules

### Standard Layout

```
Row 0: idle      [frame0] [frame1] [frame2] [frame3]
Row 1: walk      [frame0] [frame1] [frame2] [frame3] [frame4] [frame5]
Row 2: run       [frame0] [frame1] [frame2] [frame3] [frame4] [frame5]
Row 3: attack    [frame0] [frame1] [frame2] [frame3]
Row 4: hurt      [frame0] [frame1]
Row 5: death     [frame0] [frame1] [frame2] [frame3] [frame4]
```

### Layout Conventions

| Rule | Description |
|------|-------------|
| **Row-major** | Each animation occupies one horizontal row |
| **Uniform cell size** | All frames share the same width x height |
| **Power-of-two sheet** | Total sheet dimensions should be 2^n (256, 512, 1024) |
| **No padding (default)** | 0px gap between frames; engine handles UV |
| **Direction order** | Down -> Left -> Right -> Up (RPG Maker convention) |
| **Consistent origin** | Character "feet" at bottom-center of every frame |

### Power-of-Two Dimension Guide

| Sprite Size | Cols x Rows | Sheet Size | Total Frames |
|-------------|-------------|------------|-------------|
| 16x16 | 16 x 16 | 256 x 256 | 256 |
| 16x16 | 32 x 32 | 512 x 512 | 1024 |
| 32x32 | 8 x 8 | 256 x 256 | 64 |
| 32x32 | 16 x 16 | 512 x 512 | 256 |
| 64x64 | 8 x 8 | 512 x 512 | 64 |
| 64x64 | 16 x 16 | 1024 x 1024 | 256 |

**Rule:** Sheet width & height should each be a power of two. GPU texture sampling is most efficient at 256, 512, 1024, 2048.

### Padding & Spacing

| Option | Value | When |
|--------|-------|------|
| No padding | 0px | Default; most engines handle UV correctly |
| 1px padding | 1px transparent border | Prevents bleeding at fractional zoom |
| 2px extrusion | Duplicate edge pixels outward | WebGL mipmap/filter artifacts |

**Tip:** If you see "color bleeding" at sprite edges, add 1px transparent padding around each frame and adjust UV coordinates.

### Direction Variants

For 4-directional characters:

```
Row 0: down-idle   [f0][f1][f2][f3]
Row 1: down-walk   [f0][f1][f2][f3][f4][f5]
Row 2: left-idle   [f0][f1][f2][f3]
Row 3: left-walk   [f0][f1][f2][f3][f4][f5]
Row 4: right-idle  [f0][f1][f2][f3]
Row 5: right-walk  [f0][f1][f2][f3][f4][f5]
Row 6: up-idle     [f0][f1][f2][f3]
Row 7: up-walk     [f0][f1][f2][f3][f4][f5]
```

**Optimization:** If left/right are mirrored, store only one direction and flip at runtime (`sprite.flipX = true`).

---

## Standard Frame Counts

### Basic Actions

| Animation | Frames | Loop | Notes |
|-----------|--------|------|-------|
| **idle** | 2-4 | Yes | Subtle breathing/blinking |
| **walk** | 4-6 | Yes | Contact-pass-contact-pass |
| **run** | 6-8 | Yes | Extended stride, lean forward |
| **attack (melee)** | 3-5 | No | Anticipation-swing-follow-through |
| **attack (ranged)** | 4-6 | No | Draw-aim-release-recover |
| **hurt** | 2 | No | Flinch + flash white |
| **death** | 4-6 | No | Collapse sequence, hold last frame |
| **jump** | 3-5 | No | Crouch-rise-apex(-fall-land) |
| **fall** | 2 | Yes | Descend-land |
| **cast/spell** | 4-6 | No | Wind-up-channel-release-effect |
| **interact** | 2-3 | No | Reach-grab-retract |
| **dodge/roll** | 4-6 | No | Crouch-tuck-roll-recover |
| **block/guard** | 2-3 | No | Raise shield-hold-lower |
| **climb** | 4-6 | Yes | Hand-over-hand cycle |
| **swim** | 4-6 | Yes | Stroke cycle |

### Frame Count by Game Style

| Style | idle | walk | attack | Total (est.) |
|-------|------|------|--------|-------------|
| **Minimalist** (PICO-8) | 2 | 4 | 3 | ~20 frames |
| **Standard** (NES-era) | 4 | 6 | 4 | ~40 frames |
| **Rich** (SNES-era) | 6 | 8 | 6 | ~80 frames |
| **Detailed** (GBA+) | 8 | 10 | 8 | ~120+ frames |

---

## FPS (Frames Per Second) Guidelines

### By Animation Type

| Animation Type | FPS | ms/frame | Feel |
|---------------|-----|----------|------|
| Idle | 4-6 | 166-250 | Calm, breathing rhythm |
| Walk | 8-10 | 100-125 | Natural pace |
| Run | 10-12 | 83-100 | Energetic |
| Attack (melee) | 12-15 | 66-83 | Snappy, impactful |
| Attack (ranged) | 10-12 | 83-100 | Controlled |
| Cast/Spell | 8-10 | 100-125 | Deliberate |
| Jump/Fall | 10-12 | 83-100 | Responsive |
| Death | 8-10 | 100-125 | Dramatic |
| UI animation | 6-8 | 125-166 | Smooth but not distracting |
| Explosion/VFX | 12-15 | 66-83 | Dynamic, brief |
| Water/fire | 4-6 | 166-250 | Ambient, subtle |
| Blinking/eyes | 2-4 | 250-500 | Sporadic |

### By Game Genre

| Genre | Base FPS | Notes |
|-------|---------|-------|
| RPG (turn-based) | 6-8 | Slower, emphasize readability |
| Platformer | 10-12 | Faster, responsive feel |
| Action RPG | 10-15 | Snappy combat, smooth movement |
| Strategy/Tactics | 4-6 | Economy of animation |
| Puzzle | 4-8 | Clarity over speed |

### Variable Frame Duration

Not all frames in an animation need the same duration. Key poses (contact, apex) can be held longer.

```javascript
// Phaser 3 — variable frame duration
scene.anims.create({
  key: 'attack',
  frames: [
    { key: 'hero', frame: 0, duration: 100 },  // anticipation (hold)
    { key: 'hero', frame: 1, duration: 50 },   // swing (fast)
    { key: 'hero', frame: 2, duration: 50 },   // impact (fast)
    { key: 'hero', frame: 3, duration: 150 },  // follow-through (hold)
  ],
  repeat: 0,
});
```

### Common Game Engine Defaults

| Engine | Default FPS | Frame Duration |
|--------|------------|----------------|
| Phaser 3 | 10 | 100ms |
| Godot | 5 (AnimatedSprite) | 200ms |
| Unity | 12 (Animator) | 83ms |
| RPG Maker | 4 per pattern | 250ms |
| Aseprite | 100ms per frame | 10 FPS |

---

## Walk Cycle Deep Dive

### 6-Frame Walk Cycle (Standard)

```
Frame 0: Contact    — front foot touches ground, body at mid-height
Frame 1: Down       — body lowest point, weight on front foot
Frame 2: Passing    — legs cross, body rises, back leg swings forward
Frame 3: Contact    — other foot touches ground (mirrored frame 0)
Frame 4: Down       — body lowest point (mirrored frame 1)
Frame 5: Passing    — legs cross, body rises (mirrored frame 2)
```

**Key physics:**
- Body bobs **up** during passing, **down** during contact
- Bob amount: 1px for 16x16, 1-2px for 32x32
- Arms swing opposite to legs
- Head stays relatively stable (anchor point)

### 4-Frame Walk Cycle (Simplified)

```
Frame 0: Stand      — neutral pose (both feet grounded)
Frame 1: Step-L     — left foot forward, slight lean
Frame 2: Stand      — neutral pose (same as frame 0)
Frame 3: Step-R     — right foot forward (mirror of frame 1)
```

**Tip:** For 8x8 or very small sprites, 2 frames (stand + step) is sufficient.

### Walk Cycle Pixel Counts by Size

| Sprite Size | Body Bob | Arm Swing | Leg Stride |
|-------------|---------|-----------|------------|
| 8x8 | 0px | 0-1px | 1px |
| 16x16 | 1px | 1px | 1-2px |
| 32x32 | 1-2px | 1-2px | 2-3px |
| 64x64 | 2-3px | 2-3px | 3-5px |

---

## Attack Animation Breakdown

### Melee Attack (3-Act Structure)

```
ACT 1: Anticipation (1-2 frames)
  - Pull back / wind up
  - Body leans away from swing direction
  - Creates visual "spring tension"

ACT 2: Action (1-2 frames)
  - Fast forward motion
  - Weapon traces arc
  - Optional: smear frame for speed
  - Impact frame: slight pause (hold 2x duration)

ACT 3: Follow-through (1-2 frames)
  - Weapon continues past target
  - Body recovers to neutral
  - Optional: recoil from impact
```

**Common pattern (5 frames):**

```
[Anticipation] [Anticipation+] [Swing] [Impact] [Recovery]
   150ms          100ms         50ms    100ms     150ms
```

### Ranged Attack

```
Frame 0: Draw      — pull bow / raise staff (150ms)
Frame 1: Aim       — full extension, target alignment (100ms)
Frame 2: Release   — projectile fires, recoil begins (50ms)
Frame 3: Projectile — projectile in flight (separate sprite) (100ms)
Frame 4: Recover   — return to idle stance (150ms)
```

### Cast/Spell Attack

```
Frame 0: Channel   — raise hands, energy gathers (200ms)
Frame 1: Charge    — visual buildup (particles/glow) (150ms)
Frame 2: Release   — cast pose, energy expelled (50ms)
Frame 3: Effect    — spell visible (separate VFX sprite) (100ms)
Frame 4: Cooldown  — arms lower, slight fatigue pose (150ms)
```

---

## Jump Animation

### 3-Frame Jump (Minimal)

```
Frame 0: Crouch    — compress before launch
Frame 1: Apex      — full extension at top
Frame 2: Land      — compress on landing
```

### 5-Frame Jump (Standard)

```
Frame 0: Crouch    — anticipation, body compresses 1-2px
Frame 1: Launch    — body extends, feet leave ground
Frame 2: Apex      — highest point, full extension
Frame 3: Fall      — legs tuck, prepare for landing
Frame 4: Land      — compress on impact, slight bounce
```

### 9-Frame Jump (Detailed)

```
Frame 0: Idle      — standing neutral
Frame 1: Crouch    — squat, anticipation
Frame 2: Launch    — push off, legs extend
Frame 3: Rise      — ascending, arms up
Frame 4: Apex      — peak height, float pose
Frame 5: Turn      — body shifts to descend
Frame 6: Fall      — descending, legs tuck
Frame 7: Impact    — feet hit, body compresses
Frame 8: Recover   — return to idle
```

---

## Death & Hit Animations

### Hit/Hurt (2 frames)

```
Frame 0: Flinch    — body jerks away from hit direction
Frame 1: Flash     — white overlay or color inversion (1-2 frame hold)
```

**Hit feedback techniques:**
- **White flash:** Replace all colors with white for 1-2 frames
- **Color shift:** Shift toward red for 1-2 frames
- **Knockback:** Sprite moves 2-4px away from hit source
- **Freeze frame:** Pause ALL animation for 2-3 frames on hit (game feel)

### Death (5-Frame Standard)

```
Frame 0: Hit       — final blow reaction
Frame 1: Stagger   — lose balance, lean
Frame 2: Collapse  — body falls, limbs go limp
Frame 3: Ground    — hit the ground, possible bounce
Frame 4: Rest      — final pose (hold indefinitely or fade)
```

**Variations:**
- **Disintegrate:** 4-6 frames, body breaks into particles
- **Fade out:** Hold last frame, reduce alpha over time
- **Dramatic:** 6-8 frames with slow-motion hold at moment of impact

---

## Animation Principles for Pixel Art

### Core Principles

| Principle | Application | Pixel-Level Detail |
|-----------|------------|-------------------|
| **Squash & stretch** | 1px vertical compression on landing, 1px stretch on jump | Only modify silhouette, not internal detail |
| **Anticipation** | 1-2 frame wind-up before action | Move body 1-2px opposite to action direction |
| **Follow-through** | 1 frame overshoot after action peak | Weapon/limb continues 1-2px past target |
| **Slow in / slow out** | Variable frame duration instead of even timing | Hold key poses longer (150-200ms), pass-throughs shorter (50ms) |
| **Secondary motion** | Hair, cape, tail lag behind primary motion by 1-2 frames | Offset by 1 frame + 1px position shift |
| **Exaggeration** | Enlarge key poses beyond anatomical accuracy | Sword swing wider than realistic, jump higher |

### Smear Frames

Elongate sprite in motion direction for 1 frame to convey speed. Used for fast attacks, dashes, and impacts.

```
Normal:    ████      Smear:  ██████████
           ████              ████
           ████              ████
```

**Rules:**
- Only use for 1 frame (never hold a smear)
- Direction follows motion arc
- Width increase: 50-100% of sprite width
- Reduce vertical detail in the smear (blur effect)
- Used primarily in attack and dash animations

### Sub-Pixel Animation

Create apparent motion smaller than 1 pixel by alternating colors between adjacent pixels.

```
Frame A:  ██░░    Frame B:  ░██░    (apparent 0.5px shift)
```

**Implementation:**

```python
# Sub-pixel shift: alternate between two positions
frame_a = [[1, 1, 0, 0],
           [1, 1, 0, 0]]
frame_b = [[0, 1, 1, 0],
           [0, 1, 1, 0]]
# Displaying these at 8-12 FPS creates smooth sub-pixel motion
```

**When to use:** Idle breathing, slow ambient animation, water surface, floating objects.

### Secondary Motion Checklist

| Element | Lag Frames | Pixel Offset | Notes |
|---------|-----------|-------------|-------|
| Hair | 1-2 | 1-2px | Swings opposite to movement |
| Cape/Cloak | 2-3 | 2-3px | Larger mass = more lag |
| Tail | 1-2 | 1px | S-curve wave pattern |
| Earrings/Jewelry | 1 | 1px | Quick settle, small mass |
| Weapon (sheathed) | 1 | 1px | Slight sway, rigid body |
| Belt/Sash | 1-2 | 1px | Follows body, slight wave |

---

## Color Techniques in Animation

### Hit Flash Implementation

```javascript
// Method 1: White overlay (Canvas)
function flashWhite(ctx, sprite, duration) {
  ctx.globalCompositeOperation = 'source-atop';
  ctx.fillStyle = '#FFFFFF';
  ctx.fillRect(0, 0, sprite.width, sprite.height);
  ctx.globalCompositeOperation = 'source-over';
}

// Method 2: Palette swap (index-based)
const NORMAL_PALETTE = ['#1a1c2c', '#5d275d', '#b13e53', '#ef7d57'];
const HIT_PALETTE = ['#ffffff', '#ffffff', '#ffffff', '#ffffff'];
// Swap palette for 2-3 frames, then revert
```

### Afterimage / Motion Trail

```
Frame N:    ████  (100% opacity)
Frame N-1:  ████  (50% opacity, 2px behind)
Frame N-2:  ████  (25% opacity, 4px behind)
```

---

## Metadata Formats

### Standard Spritesheet Metadata (Dot Format)

```json
{
  "name": "character-hero",
  "image": "hero-spritesheet.png",
  "frameWidth": 16,
  "frameHeight": 16,
  "scale": 1,
  "palette": ["#1a1c2c", "#5d275d", "#b13e53", "#ef7d57"],
  "animations": [
    {
      "name": "idle",
      "row": 0,
      "frames": [0, 1, 2, 3],
      "fps": 4,
      "loop": true
    },
    {
      "name": "walk",
      "row": 1,
      "frames": [0, 1, 2, 3, 4, 5],
      "fps": 8,
      "loop": true
    },
    {
      "name": "attack",
      "row": 2,
      "frames": [0, 1, 2, 3],
      "fps": 12,
      "loop": false,
      "frameDurations": [150, 100, 50, 150]
    }
  ]
}
```

### Phaser 3 Texture Atlas (JSON Hash)

```json
{
  "frames": {
    "hero_idle_0": {
      "frame": { "x": 0, "y": 0, "w": 16, "h": 16 },
      "sourceSize": { "w": 16, "h": 16 },
      "spriteSourceSize": { "x": 0, "y": 0, "w": 16, "h": 16 }
    },
    "hero_idle_1": {
      "frame": { "x": 16, "y": 0, "w": 16, "h": 16 },
      "sourceSize": { "w": 16, "h": 16 },
      "spriteSourceSize": { "x": 0, "y": 0, "w": 16, "h": 16 }
    }
  },
  "meta": {
    "image": "hero-atlas.png",
    "format": "RGBA8888",
    "size": { "w": 256, "h": 256 },
    "scale": 1
  }
}
```

### Aseprite JSON Array Export

```json
{
  "frames": [
    {
      "filename": "hero_idle 0.aseprite",
      "frame": { "x": 0, "y": 0, "w": 16, "h": 16 },
      "rotated": false,
      "trimmed": false,
      "spriteSourceSize": { "x": 0, "y": 0, "w": 16, "h": 16 },
      "sourceSize": { "w": 16, "h": 16 },
      "duration": 100
    }
  ],
  "meta": {
    "app": "http://www.aseprite.org/",
    "version": "1.3",
    "image": "hero.png",
    "format": "RGBA8888",
    "size": { "w": 256, "h": 256 },
    "scale": "1",
    "frameTags": [
      { "name": "idle", "from": 0, "to": 3, "direction": "forward" },
      { "name": "walk", "from": 4, "to": 9, "direction": "forward" },
      { "name": "attack", "from": 10, "to": 13, "direction": "forward" }
    ],
    "layers": [
      { "name": "outline", "opacity": 255, "blendMode": "normal" },
      { "name": "fill", "opacity": 255, "blendMode": "normal" }
    ]
  }
}
```

### Aseprite CLI Export Commands

```bash
# Export spritesheet + JSON metadata
aseprite -b hero.aseprite --sheet hero-sheet.png --data hero-sheet.json \
  --format json-array --sheet-type horizontal --sheet-pack

# Export specific animation tag
aseprite -b hero.aseprite --sheet idle.png --data idle.json \
  --format json-array --frame-tag "idle"

# Export individual frames
aseprite -b hero.aseprite --save-as hero_{tag}_{frame}.png

# Scale up (nearest neighbor)
aseprite -b hero.aseprite --scale 4 --sheet hero-4x.png
```

### TexturePacker Format

```json
{
  "frames": {
    "hero_idle_0.png": {
      "frame": { "x": 0, "y": 0, "w": 16, "h": 16 },
      "rotated": false,
      "trimmed": false,
      "spriteSourceSize": { "x": 0, "y": 0, "w": 16, "h": 16 },
      "sourceSize": { "w": 16, "h": 16 },
      "pivot": { "x": 0.5, "y": 1.0 }
    }
  },
  "meta": {
    "app": "https://www.codeandweb.com/texturepacker",
    "version": "1.1",
    "image": "hero-atlas.png",
    "format": "RGBA8888",
    "size": { "w": 256, "h": 256 },
    "scale": 1,
    "smartupdate": "$TexturePacker:SmartUpdate:hash$"
  }
}
```

### PixiJS Spritesheet Format

```json
{
  "frames": {
    "hero_idle_0": {
      "frame": { "x": 0, "y": 0, "w": 16, "h": 16 },
      "sourceSize": { "w": 16, "h": 16 },
      "spriteSourceSize": { "x": 0, "y": 0, "w": 16, "h": 16 }
    }
  },
  "animations": {
    "idle": ["hero_idle_0", "hero_idle_1", "hero_idle_2", "hero_idle_3"],
    "walk": ["hero_walk_0", "hero_walk_1", "hero_walk_2", "hero_walk_3"]
  },
  "meta": {
    "image": "hero.png",
    "scale": 1
  }
}
```

---

## Engine Integration

### Phaser 3 — Spritesheet Animation

```javascript
// Load spritesheet with metadata
this.load.spritesheet('hero', 'hero-spritesheet.png', {
  frameWidth: 16,
  frameHeight: 16,
});

// Create animations from metadata
metadata.animations.forEach(anim => {
  this.anims.create({
    key: anim.name,
    frames: this.anims.generateFrameNumbers('hero', {
      start: anim.row * framesPerRow + anim.frames[0],
      end: anim.row * framesPerRow + anim.frames[anim.frames.length - 1],
    }),
    frameRate: anim.fps,
    repeat: anim.loop ? -1 : 0,
  });
});
```

### Phaser 3.60+ Aseprite Native Support

```javascript
// Load Aseprite file directly
this.load.aseprite('hero', 'hero.png', 'hero.json');

// Create all animations from Aseprite tags automatically
this.anims.createFromAseprite('hero');

// Play animation
const sprite = this.add.sprite(100, 100, 'hero');
sprite.play('idle');

// Animation events
sprite.on('animationcomplete-attack', () => {
  sprite.play('idle');
});
```

### Pillow Spritesheet Generation

```python
from PIL import Image

def create_spritesheet(frames, frame_width, frame_height, cols=None):
    """Pack animation frames into a spritesheet.

    Args:
        frames: list of PIL Image objects
        frame_width: width of each frame
        frame_height: height of each frame
        cols: frames per row (default: all in one row)
    """
    if cols is None:
        cols = len(frames)
    rows_needed = (len(frames) + cols - 1) // cols

    # Ensure power-of-two dimensions
    sheet_w = cols * frame_width
    sheet_h = rows_needed * frame_height

    sheet = Image.new('RGBA', (sheet_w, sheet_h), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        x = (i % cols) * frame_width
        y = (i // cols) * frame_height
        sheet.paste(frame, (x, y))
    return sheet


def create_gif(frames, fps=8, scale=4):
    """Create animated GIF from pixel art frames."""
    scaled = []
    for frame in frames:
        if scale > 1:
            w, h = frame.size
            frame = frame.resize((w * scale, h * scale), Image.NEAREST)
        # GIF doesn't support RGBA, convert
        bg = Image.new('RGBA', frame.size, (0, 0, 0, 0))
        bg.paste(frame, (0, 0), frame)
        scaled.append(bg.convert('RGB'))

    duration = int(1000 / fps)
    scaled[0].save(
        'animation.gif',
        save_all=True,
        append_images=scaled[1:],
        duration=duration,
        loop=0,
        disposal=2,  # clear frame before drawing next
    )
```

---

## Animation State Machine

### Basic State Transitions

```
        ┌────────┐
        │  idle  │<──────────────────────┐
        └───┬────┘                       │
            │ move input                 │ no input
            v                            │
        ┌────────┐                       │
   ┌───>│  walk  │───────────────────────┘
   │    └───┬────┘
   │        │ sprint input
   │        v
   │    ┌────────┐
   │    │  run   │
   │    └───┬────┘
   │        │ jump input    attack input
   │        v               v
   │    ┌────────┐      ┌────────┐
   │    │  jump  │      │ attack │
   │    └───┬────┘      └───┬────┘
   │        │ land          │ anim complete
   │        v               v
   │    ┌────────┐      ┌────────┐
   └────│  land  │      │  idle  │
        └────────┘      └────────┘
                            ^
        ┌────────┐          │
        │  hurt  │──────────┘ (after hit stun)
        └────────┘
        ┌────────┐
        │  death │ (terminal state)
        └────────┘
```

### Priority System

When multiple inputs occur simultaneously:

| Priority | State | Overrides |
|----------|-------|-----------|
| 1 (highest) | death | Everything |
| 2 | hurt | attack, cast, move |
| 3 | attack | move, idle |
| 4 | cast | move, idle |
| 5 | jump/fall | walk, run |
| 6 | run | walk, idle |
| 7 | walk | idle |
| 8 (lowest) | idle | Nothing |

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| **Floating feet** | Character slides across ground | Ensure contact frames have feet planted on bottom edge |
| **Stiff movement** | Walk looks robotic | Add 1px body bob, arm swing, secondary motion |
| **Inconsistent speed** | Walk and run look same speed | Run should have 50-100% wider stride and faster FPS |
| **Pop/snap transitions** | Jarring animation changes | Add 1-2 transition frames between states |
| **Twinning** | Both arms/legs move identically | Offset limb pairs: when left arm forward, right arm back |
| **Even timing** | All frames same duration | Use variable timing: hold key poses, speed through in-betweens |
| **Orphan frames** | Unused frames in sheet waste texture space | Pack efficiently, remove unused frames before export |
