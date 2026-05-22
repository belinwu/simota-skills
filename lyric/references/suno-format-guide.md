# Suno AI Format Guide

Suno AIの技術仕様・メタタグ・制約の完全リファレンス。

## Model Generation Snapshot (2026-05)

| Model | Released | Key change | Use when |
|-------|----------|-----------|----------|
| **V6** | 2026 H1 (latest) | Faster prompting, stronger style control, cleaner lyrics-to-song flow, more polished instrumentals | Default for new projects in 2026-05+ |
| **V5.5** | 2026-03-26 | Adds **Voices** (vocal-persona cloning) — train an AI vocal persona on your own voice samples; the **Voices** button replaces the legacy **Personas** button in the Create menu (Style Personas still accessible from inside Voices) | Voice-driven consistency across releases, "AI artist" branding |
| **V5** | Late 2025 | Production-quality audio baseline | Legacy projects; budget-constrained generation |
| **V4.5** | 2025 | `~8 min` audio output, `44.1 kHz` | Long-form (full songs, ambient) |
| **V4 / Legacy** | Pre-2025 | `~200` char style prompt, `~4 min` audio | Avoid for new work |

Pick V6 first; fall back to V5.5 only when the Voices feature is the critical capability. Legacy V4 should not be the choice for new projects in 2026.

## Technical Constraints

| Field | Limit | Notes |
|-------|-------|-------|
| Style Prompt (Legacy/V4) | ~200 chars | Excess is silently truncated |
| Style Prompt (V4.5+) | ~1,000 chars | Tag-based or conversational prose |
| Lyrics | ~3,000 chars | 40-60 lines, 200-300 words equivalent |
| Song Title | 80 chars | Minimal impact on music output |
| Recommended lines | 30-40 | For standard 3-4 min songs |
| Lines per section | 2-6 | Longer sections cause vocal drift |
| Audio output (Legacy/V4) | 1-4 min | Per generation |
| Audio output (V4.5+) | Up to 8 min | 44.1 kHz output |

- 3,000文字超過: セクションが駆け足、または短い出力になる
- 15行未満: 曲が短縮される傾向
- v4.5/v5/v5.5/v6: APIレベルで最大5,000文字対応

## Metatag Syntax Rules

1. 角括弧 `[ ]` で囲む（コロン `Verse:` は歌詞として歌われる）
2. 独立した行に配置（歌詞の途中に埋め込まない）
3. タグは1-3語で短く保つ
4. セクション間に空白行を入れる
5. 最初の20-30語のタグが最も強い影響力を持つ

## Pipe Stacking

複数の指示を1つの括弧内で組み合わせる:
```
[Chorus | chill | synth lead | soft vocal]
[Verse | spoken word | low energy]
[Bridge | female vocal | melancholic]
```
- 2-4要素に抑える（5つ以上は非推奨）

## Structure Tags

### Primary Structure
| Tag | Purpose | Notes |
|-----|---------|-------|
| `[Short Instrumental Intro]` | Intro | `[Intro]`より安定して動作 |
| `[Verse]` / `[Verse 1]` | Verse | 各2-6行 |
| `[Pre-Chorus]` | Pre-Chorus | 期待感の醸成、短め |
| `[Chorus]` | Chorus/Hook | 繰り返し可能なフック |
| `[Post-Chorus]` | Post-Chorus | コーラス後の余韻 |
| `[Hook]` | Hook | 短く印象的なフレーズ |
| `[Bridge]` | Bridge | 対比とスペース |
| `[Outro]` | Outro | 曲の締めくくり |

### Dynamic Tags
| Tag | Purpose |
|-----|---------|
| `[Build-Up]` / `[Buildup]` | テンション上昇 |
| `[Drop]` | EDMドロップ |
| `[Break]` / `[Percussion Break]` | ブレイク |
| `[Instrumental]` / `[Instrumental Break]` | インスト部分 |
| `[Interlude]` / `[Melodic Interlude]` | インタールード |
| `[Solo]` / `[Guitar Solo]` | ソロパート |

### Ending Tags
| Tag | Purpose |
|-----|---------|
| `[Final Chorus]` | 最大盛り上がりのコーラス |
| `[Big Finish]` | 大サビ的な終結 |
| `[Refrain]` | リフレイン（`[Outro]`より創造的） |
| `[Fade Out]` / `[Fade to End]` | フェードアウト |
| `[End]` | 即座に終了 |

## Punctuation as Musical Direction

| Punctuation | Effect |
|-------------|--------|
| `,` (comma) | マイクロポーズ（微小な間） |
| `--` (dash) | 息継ぎ、スタッガード・デリバリー |
| `...` (ellipsis) | フレージングのゆらぎ |
| `!` (exclamation) | アグレッシブなアタック（次行に伝播注意） |
| Line break | 音楽的なブレスの位置 |
| ALL CAPS | ボーカルの強調・トーン変化 |

## Ad-libs and Vocal Effects

### Ad-libs (parentheses)
```
Now I know (yeah) now I know (uh-huh)
We're gonna make it (oh yeah!)
```

### Sustained notes (hyphens/repetition)
```
lo-ove
sooo-long
knooowwww
```

## Critical Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| `[Intro]` tag alone | Use `[Short Instrumental Intro]` |
| `[My Custom Tag]` | Only use recognized standard tags |
| `repeat chorus` or similar | Write full chorus text every time |
| Style text as plain lyrics | Always use `[brackets]` for tags |
| `*sound effects*` in lyrics | No asterisks, SFX descriptions, or sound cues |
| `!` overuse | Use sparingly; aggression bleeds to next line |
| Too many pipe elements | Keep to 2-4 per bracket |

## Style Prompt Priority Order (200 chars)

1. Genre/sub-genre (e.g., indie pop, lo-fi hip hop)
2. Vocal direction (e.g., female mid-range, breathy)
3. Primary mood (e.g., melancholic, uplifting)
4. 1-2 instruments (e.g., acoustic guitar, piano)
5. BPM/tempo (e.g., 90 BPM, mid-tempo)
6. Production quality (e.g., lo-fi, polished)

Rules:
- Drop articles, use comma separation
- 4-8 style tags is the sweet spot
- Adding era changes sound drastically ("80s synth-pop" vs "2020s synth-pop")
- Avoid contradictory tags (aggressive + calm)

## Suno v5 / v5.5 / v6 Specific

- **Top anchor**: Put vocal role + BPM + structure summary at prompt start
- **Syllable count**: Specify "Verse lines: 8-10 syllables"
- **Rhyme scheme**: Vary schemes (ABAB, ABCB, mixed) — avoid defaulting to AABB, which signals AI-generated lyrics
- **Lyric fidelity**: Add "Do not change any words inside brackets. Sing exactly as written."
- **Pronunciation fix**: Adjust at text level (e.g., "bahss" for "bass")
- **Callback tag** (Studio Extend/Replace): `[Callback: <reference>]` instructs Suno to maintain feel or reference a prior section during Extend chains (e.g., `[Callback: Chorus melody]` in Outro to recall the main hook)
- **V5.5 Voices** (replaces Personas): trains an AI **vocal persona** on uploaded voice samples, capturing pitch / tone / timbre. The output is "recognisably similar" to the source, not an exact clone — design copy and credits accordingly. When generating, the style prompt should *complement* the trained vocal character, not fight it.
- **Persona reuse**: from any generated track, click "Create Persona" on a vocal you like to save it as a reusable voice across an album / project.
- **V6 improvements**: faster prompting (style locked in earlier in the request), stronger style adherence (less drift between section tags), cleaner lyrics-to-song mapping (fewer dropped syllables in dense verses), more polished instrumentals (less muddy low-mids). Carry forward the prompt-engineering rules above — V6 does not change the metatag vocabulary, it just executes it better.
- **Custom Models** (Pro/Premier only): require min 6 uploaded songs. Use when the project needs a *distinct house sound* across releases, not just a single track.
