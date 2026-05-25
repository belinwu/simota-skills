# Creative Variation: Direction-Shift Proposals

Framework for proposing **alternative directions** for an analyzed track. Sonar MEASURES and PROPOSES; it does NOT GENERATE audio (that's `tone`) or rewrite lyrics (that's `lyric`). Every proposal cites a measured feature as anchor.

## Core Rules

- Every proposal carries `change`, `rationale`, `measured_anchor`, and (if applicable) `next_agent`.
- **No vague suggestions** ("make it more emotional"). Name the parameter (BPM, key, RT60, PLR, instrument, section structure).
- **No fabricated genre tropes**. If you make a claim like "lo-fi hip-hop wants 80-95 BPM", that's a defensible convention (cite source or qualify as common practice).
- **No legal grey zone without flagging**. If user asks "make it sound like [specific artist]", surface the derivative-work concern before producing the proposal.
- **Anchor every proposal**: "Recommendation X because measurement Y shows Z." Unanchored proposals are rejected.
- **Think step-by-step before recommending structural reorders** — listener expectation is high-cost to break. Tempo / instrument / effector shifts are lower-cost.

## Variation Axes

Five orthogonal axes. Recipe `variation` accepts `--axes` flag (one or more of `genre|tempo-key|arrangement|instrument|effector|all`, default `all`).

### Axis 1: Genre Re-cast

Propose how the track would change if produced under a different genre's conventions.

**Method**:
1. Identify current genre cluster from measured features (BPM, time signature, instrument mix, PLR, spectral profile, structural pattern).
2. Compare to target genre's typical conventions (tempo range, instrument palette, mix-bus traits).
3. List the deltas.

**Proposal template**:
```
- Current: 128 BPM / 4/4 / heavy sidechain (PLR 7.2 dB) / synth-lead-dominant / 32-bar verse-chorus / "house" cluster
- Target: lo-fi hip-hop
- Proposed changes:
  - Tempo: 128 → 82-92 BPM (lo-fi convention: half-time perception of original groove)
  - Swing: straight → ~58-62% (subtle MPC-style swing)
  - Sidechain: remove (lo-fi prefers minimal pumping for "warm" feel)
  - PLR target: 7.2 → 11-13 dB (lo-fi prefers more dynamic master)
  - Instrument swaps: synth lead → Rhodes/Wurlitzer sample; saw bass → upright bass sample
  - Mix-bus: add subtle tape saturation, vinyl-style high-frequency rolloff above 12 kHz
  - Structure: reduce 32-bar verse to 16-bar loop with sparse variation
- Anchors: measured BPM (128), PLR (7.2), instrument detection (synth lead 0.84 confidence), section count (4 sections via msaf)
- Next agent: Tone (generate stems matching target convention), Lyric (re-write for slower tempo)
```

**Tooling support**:
- Genre-cluster centroid distance via Essentia Discogs-EffNet (non-commercial only) or LAION-CLAP zero-shot against genre label set
- Reference corpus of genre-typical PLR/BPM/instrument distributions (build locally from your library)

### Axis 2: Tempo / Key / Time-Signature Variants

Propose alternative tempos and keys with explicit rationale.

**Method**:
1. Compute musical relatives (parallel major/minor, relative major/minor, dominant key, subdominant).
2. Compute tempo conventions (halftime ×0.5, doubletime ×2.0, ±10%, 3:2 polymeter).
3. Filter to perceptually meaningful options (avoid suggesting 256 BPM unless source is already fast).

**Proposal template**:
```
- Current: 128 BPM / A minor / 4/4
- Tempo candidates:
  - 64 BPM (halftime feel): emotional / introspective re-cast. Use case: ballad version of same melody
  - 140 BPM (+10%): more energetic, slight uplift. Use case: gym/sport version
  - 96 BPM (3:4 ratio): triplet-feel rework. Use case: shuffle/swing variation
- Key candidates:
  - A major (parallel): brighter mood, same root. Easy vocal re-record
  - C major (relative): inverted emotional pole; chord progressions translate directly
  - E minor (dominant): tension-shift; chorus may want resolution back to A
  - D minor (subdominant): more grounded, ballad-friendly
- Time signature candidates:
  - 6/8 (compound feel): completely re-grooves; full re-arrangement required
  - 3/4 (waltz): unusual for source genre; experimental
- Anchors: measured BPM (128 ± 0.5), measured key (A minor, confidence 0.84 via Krumhansl), measured time signature (4/4 via madmom)
- Next agent: Tone (render previews at each candidate)
```

### Axis 3: Arrangement / Structural Reorder

Propose section reorders, insertions, removals, or restructurings. **Highest-cost variation** — listener expectation is broken most by structure changes.

**Method**:
1. Use msaf to segment into sections (A B A B C A — typical pop structure).
2. Identify the structural template (verse-chorus, AABA, through-composed).
3. Propose alternatives: insert breakdown at 2:30, swap bridge with extended outro, etc.

**Proposal template**:
```
- Current sections (msaf): [0:00-0:16 Intro] [0:16-0:48 Verse1] [0:48-1:20 Chorus1] [1:20-1:52 Verse2] [1:52-2:24 Chorus2] [2:24-2:56 Bridge] [2:56-3:28 Chorus3] [3:28-3:44 Outro]
- Proposed restructuring candidates:
  A. Insert breakdown at 2:24 (replace Bridge): 8 bars of stripped arrangement (drums + lead only). Restores energy contrast before final chorus. Use case: EDM-style buildup
  B. Move Bridge to 0:48 (between Intro and Verse1): re-cast as "cold open" with hook upfront. Use case: TikTok-optimized 15s hook
  C. Remove Verse2 entirely (1:20-1:52): tightens runtime to 3:12, faster radio cut. Use case: single edit
  D. Loop Chorus3 → Outro into 16-bar extended outro for DJ-friendly mix-out
- Anchors: msaf segment boundaries (7 sections detected), measured BPM (128, allows DJ mixing), measured key (A minor, allows seamless looping)
- Risk: structural reorder is high-cost; A/B test with audience before committing
- Next agent: Tone (re-render with new structure), Lyric (revise verse-chorus relationship if Verse2 removed)
```

**Think step-by-step before proposing structural changes**: every reorder breaks listener expectation. Tempo/instrument/effector changes are lower-cost. Default to small structural tweaks (insert breakdown, extend outro) over wholesale reorders.

### Axis 4: Instrument Substitution

Propose swapping detected instruments for alternative families.

**Method**:
1. Use detected instruments (from `similarity-inference.md` Section B) as anchors.
2. Propose swaps based on:
   - Genre re-cast targets (Axis 1 mapping)
   - Emotional palette shift (synth → acoustic = warmer, acoustic → synth = colder)
   - Sparsity adjustment (add/remove a layer)

**Proposal template**:
```
- Detected instruments (CLAP zero-shot):
  - synthesizer (lead): 0.87 confidence
  - drum kit (electronic): 0.91 confidence
  - bass guitar (synth bass): 0.79 confidence
  - vocals: 0.95 confidence
- Substitution candidates:
  A. Synth lead → Electric guitar (clean, single-coil): rock re-cast; use Stratocaster-style tone. Rationale: lead role retained, organic timbre shift
  B. Drum kit (electronic) → Acoustic drum kit: live-band re-cast. Removes sidechain dependency. Rationale: changes feel from "club" to "venue"
  C. Synth bass → Upright bass (recorded): jazz/acoustic re-cast. Rationale: walking bass line opens harmonic movement
  D. Add: String quartet pad behind chorus: cinematic uplift. Rationale: sparse arrangement detected (3 layers); adding 4th provides depth
  E. Remove: Drum kit during Bridge: dramatic moment. Rationale: empty space increases impact of next chorus
- Anchors: instrument detection confidences (all ≥0.79), measured PLR (7.2 dB — suggests dense mix that could benefit from sparsity)
- Next agent: Tone (generate substitute stems), Director (if making demo video of variants)
```

### Axis 5: Effector Chain Alternatives

Propose alternative effector treatments based on inferred current effects.

**Method**:
1. Use inferred effectors (from `similarity-inference.md` Section C) as anchors.
2. Propose alternatives:
   - Dry vs reverb-heavy
   - Parallel vs serial compression
   - Tape saturation vs digital limiting
   - Wide vs narrow stereo

**Proposal template**:
```
- Inferred current effects:
  - Compression family: heavy limiting (PLR 7.2 dB, confidence 0.85)
  - Reverb: present, moderate (cannot infer RT60 blindly; family hint: plate-style, confidence 0.4)
  - Stereo width: wide (0.62, confidence 0.9)
- Effector chain candidates:
  A. Reduce limiting → moderate compression (target PLR 10-12 dB): restores dynamics, suits vinyl/audiophile masters. Rationale: PLR 7.2 is over-compressed for non-streaming delivery
  B. Add parallel-compressed drum bus: punchier transients without raising peak. Rationale: heavy limiting flattens; parallel restores
  C. Reverb: try short room (RT60 ~0.4s) for intimate feel, OR long hall (RT60 ~3.2s) for cinematic. Current "moderate plate" is generic
  D. Stereo width: narrow to 0.3 (mid-focused for mono-compatible) OR widen to 0.85 (immersive for headphones). Current 0.62 is middle-ground
  E. Add tape saturation on mix bus: harmonic richness, softer transient curve. Rationale: contrast with current "digital-clean" feel
  F. Add subtle chorus on lead synth: modulation widens single-line presence. Rationale: synth-lead detected at 0.87 confidence
- Anchors: PLR (7.2), stereo width (0.62), instrument detection (synth lead 0.87)
- Next agent: Tone (re-render mix with target effect chain)
```

## Composition Pattern: Multi-Axis Variation Briefs

For multi-axis variations (e.g., "give me 3 different directions"), compose 2-3 axes per proposal:

```
## Variation Candidate 1: "Lo-fi Re-cast"
- Genre (Axis 1): house → lo-fi hip-hop
- Tempo/Key (Axis 2): 128 → 88 BPM, A minor → C minor
- Instruments (Axis 4): synth lead → Rhodes, synth bass → upright
- Effectors (Axis 5): heavy limiting → moderate; add tape saturation
- (Axis 3 omitted — structure retained)
- Anchors: ... | Next agent: Tone

## Variation Candidate 2: "Cinematic Re-cast"
- Tempo/Key (Axis 2): 128 → 96 BPM, A minor (retained)
- Instruments (Axis 4): + string quartet, drums removed in bridge
- Effectors (Axis 5): + long hall reverb (RT60 3.2s), parallel compression
- (Axes 1, 3 omitted)
- Anchors: ... | Next agent: Tone, Director (demo video)

## Variation Candidate 3: "TikTok-Optimized Hook-First Cut"
- Arrangement (Axis 3): move Bridge to 0:00 as cold open; tighten to 0:30 hook + 1:30 song body
- Tempo/Key (Axis 2): retained (128 / A minor)
- Effectors (Axis 5): retained
- Anchors: ... | Next agent: Tone, Lyric (revise hook)
```

## Legal & Honesty Boundaries

| Risk | Mitigation |
|------|-----------|
| User asks "sound like [specific copyrighted artist/track]" | Flag legal grey: derivative work. Confirm intent is personal study OR commercial original-but-inspired-by, not direct cover. Refuse if intent is unauthorized cover |
| Recommending changes that violate user's stated brief | Escalate — don't silently override |
| Vague proposals ("make it more emotional") | Reject — name the parameter |
| Fabricated genre tropes (no source, no convention) | Refuse — cite at least one defensible reference convention |
| Plugin/hardware brand recommendations ("use Waves SSL") | Out of scope — sonar can suggest effect family; pick-a-plugin is for the producer |
| Variations that would clearly break user's measured intent (e.g. removing key vocal feature) | Surface as risk; ask before including |

## Output Schema

The `variation` recipe produces a Markdown proposal document, structured as:

```markdown
# Variation Proposals — <track-name>

## Measured Baseline
- BPM: <n>, Key: <k>, Time Signature: <ts>, LUFS: <l>, PLR: <p>, Stereo width: <w>
- Detected instruments: [...]
- Inferred effectors: [...]
- Structure (msaf): [...]

## Variation Axes Requested
[all|genre|tempo-key|arrangement|instrument|effector]

## Candidate 1: <name>
- Changes: ...
- Rationale: ...
- Measured anchors: ...
- Next agent: <Tone|Lyric|Director|...>
- Risk: <none|moderate|high — listener expectation>

## Candidate 2: <name>
...

## Candidate 3: <name>
...

## Handoff Briefs
- Tone: <generation brief for selected candidate>
- Lyric: <rewrite brief for selected candidate>
- Director: <demo video brief for A/B>
```

## Decision Matrix

| User intent | Default axes | Rationale |
|-------------|-------------|-----------|
| "Give me alternatives" (no axis specified) | `all` (5 axes, 3 candidates each) | Comprehensive exploration |
| "What if it were [genre]" | `genre` + `tempo-key` + `instrument` | Genre re-cast typically requires tempo/instrument shifts too |
| "Tighter version for radio" | `arrangement` | Structural cut, not genre/effect change |
| "Same song, different mood" | `key` + `effector` | Mood shifts driven by key + effect chain |
| "Live-band version" | `instrument` + `effector` | Acoustic re-cast with appropriate effect chain |
| "TikTok cut" | `arrangement` (hook-first) | 15-30s edit prioritizing hook position |
| "DJ-friendly mix" | `arrangement` (intro/outro extension) + `tempo-key` (BPM-matched key) | Mixing convention |

## Library Pins

```python
# Re-uses existing sonar stack — no new pins for variation generation
# Variations are PROPOSALS (Markdown), not audio renders
# Audio realization handoff goes to Tone; lyric re-write to Lyric
msaf>=0.1.80           # structural segmentation (also in acoustic-analysis.md)
librosa>=0.10.1,<0.13  # spectral / feature analysis (also in tool-stack.md)
```

## Handoff Briefs

After producing a variation proposal, sonar can hand off to:

- **Tone**: "Generate <stem> at <BPM> in <key> with <effector chain>" — full audio realization
- **Lyric**: "Re-write lyrics for <new genre/tempo/mood>" — vocal-line revision
- **Director**: "Produce demo video of A/B variants" — UX comparison
- **Spark**: "Variation proposal as feature-spec seed" — product / track-concept ideation
- **Compete**: "Similar-artist surface for market positioning" — competitive context

The variation proposal MUST include explicit handoff briefs in its final section so the receiving agent can act without re-deriving context.
