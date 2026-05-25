# Loudness Standards & Platform Targets

Authoritative reference for ITU-R BS.1770-4, EBU R128, AES17, and distribution-platform targets. Cite the standard alongside every loudness number.

## Standards

### ITU-R BS.1770-4
- Defines the K-weighted loudness measurement algorithm used by every modern streaming platform.
- Gating: -70 LUFS absolute gate + -10 LU relative gate against ungated mean.
- Measurement windows (each defined separately by the standard):
  - **Momentary**: 400 ms sliding window, no gating.
  - **Short-term**: 3 s (3000 ms) sliding window, no gating.
  - **Integrated**: 400 ms blocks with **75% overlap**, then absolute + relative gating applied to the block set, then K-weighted mean of surviving blocks.
- True-peak measurement is defined separately in Annex 2 — requires ≥4× oversampling with a specific 48-tap FIR.

### EBU R128
- Builds on BS.1770; adds Loudness Range (LRA) and True Peak (dBTP).
- Broadcast target: **-23 LUFS ±0.5** Integrated, LRA ≤20 LU, True Peak ≤ -1.0 dBTP.
- Tech 3341 (meters), Tech 3342 (LRA), Tech 3343 (production), Tech 3344 (distribution).

### AES17
- Standard for digital audio engineering measurements; defines THD+N, dynamic range, crosstalk methodology. Use when reporting analog-domain-style measurements.

### ATSC A/85
- US broadcast loudness compliance (CALM Act). Dialog-anchored at **-24 LKFS ±2**. True-peak ceiling of **-2 dBTP** is common practice (per the Recommended Practice) but A/85 itself does not mandate a hard TP value; producers may negotiate per delivery contract.

## Distribution Platform Targets

| Platform | Integrated LUFS | True Peak (dBTP) | LRA | Normalization | Notes |
|----------|----------------|------------------|-----|---------------|-------|
| Spotify (Loud preset) | -11 | -1.0 | — | On (user-selected) | App-side "Loud" volume preset |
| Spotify (Normal preset) | -14 | -1.0 | — | On (default) | Default user setting; this is the canonical Spotify target |
| Spotify (Quiet preset) | -19 | -2.0 | — | On (user-selected) | Battery-saver / late-night |
| Apple Music | -16 | -1.0 | — | Sound Check (on by default) | Stricter gain reduction |
| YouTube | -14 | -1.0 | — | Per-track | No upward normalization beyond -1 dBTP |
| YouTube Music | -14 | -1.0 | — | Per-track | Same as YouTube |
| Tidal | -14 | -1.0 | — | On | Aligns with Spotify |
| Amazon Music | -14 | -2.0 | — | On | Tighter True Peak ceiling |
| Deezer | -15 | -1.0 | — | On | Slightly quieter target |
| SoundCloud | (no published target) | -1.0 | — | Not officially documented | Deliver as mastered. Industry consensus suggests -14 LUFS for streaming consistency; loud uploads (~-8 LUFS) are accepted but not boosted |
| Pandora | -14 | -1.0 | — | On | — |
| TikTok | ~-14 | -1.0 | — | On (app-side, since 2024+) | Earlier guidance "loud master (-10..-8)" is stale; TikTok now normalizes similarly to other social platforms. Re-verify on release |
| Instagram / Reels | -14 | -1.0 | — | On | Aligned with streaming defaults |
| Broadcast EBU R128 | -23 ±0.5 | -1.0 | ≤20 | Hard compliance | TV / radio in EU |
| Broadcast ATSC A/85 | -24 ±2 | -2.0 | — | Hard compliance | US TV |
| Broadcast ARIB TR-B32 | -24 ±1 | -1.0 | — | Hard compliance | JP TV — cite version: ARIB TR-B32 v3.0 (2016) or later |
| Cinema (Dolby) | 85 dB SPL @ -20 dBFS reference | — | — | — | Theatrical monitoring standard. Dolby AC-3 `dialnorm` metadata typically -27 (informs consumer-side downmix; not a measured master target) |
| Podcast (Apple Podcasts) | -16 | -1.0 | — | Recommended | Mono podcasts -19 LUFS |
| Podcast (Spotify) | -14 to -16 | -1.0 | — | Recommended | Match streaming |

## Normalization Gain Prediction

Given a measured Integrated LUFS `Lm` and platform target `Lt`:

- **Predicted gain shift**: `ΔG = Lt − Lm` (LU = dB at K-weighted gain).
- **True-peak after shift**: `TPshifted = TPmeasured + ΔG`.
- **Clipping risk**: if `TPshifted > Lt_TPceiling`, the platform either rejects the upward shift (most platforms cap at ceiling) or applies a limiter (rare).

Example: master at `-9 LUFS / -0.3 dBTP` on Spotify (target `-14 LUFS / -1.0 dBTP`):
- `ΔG = -14 − (-9) = -5 LU` → Spotify reduces gain by 5 dB.
- `TPshifted = -0.3 + (-5) = -5.3 dBTP` → well under ceiling. Audible result: noticeably quieter than master peak loudness suggested.

Conversely, master at `-20 LUFS / -3.0 dBTP` on Spotify:
- `ΔG = -14 − (-20) = +6 LU` → Spotify wants to boost.
- `TPshifted = -3.0 + 6 = +3.0 dBTP` → **exceeds -1 dBTP ceiling**. Spotify caps the boost at `+2 LU` (ceiling-limited), final delivery `-18 LUFS / -1.0 dBTP`. The user hears a quiet track. Remediation: re-master closer to platform target.

## Loudness Range (LRA)

- **LRA < 5 LU**: heavily compressed; suspect over-mastering. Acceptable for some EDM/pop, problematic for jazz/classical.
- **LRA 5-12 LU**: typical modern pop/rock master.
- **LRA 12-20 LU**: dynamic; cinematic, jazz, classical, audiophile.
- **LRA > 20 LU**: very dynamic; broadcast rejects (EBU R128 LRA ≤20).

## Peak Loudness Ratio (PLR) and PSR

- **PLR** = True Peak − Integrated LUFS. Headroom indicator. PLR ≥ 9 dB → mastering-grade dynamics. PLR < 6 dB → compressed.
- **PSR** (Pop Music Loudness Indicator) = Short-term True Peak − Short-term LUFS over a 3 s window. Tracks moment-by-moment dynamics.

## Measurement Parameter Defaults

| Parameter | Default | Notes |
|-----------|---------|-------|
| Block size (Momentary) | 400 ms | BS.1770-4 |
| Block size (Short-term) | 3000 ms | BS.1770-4 |
| Overlap | 75% | BS.1770-4 |
| Absolute gate | -70 LUFS | BS.1770-4 |
| Relative gate | -10 LU below ungated mean | BS.1770-4 |
| K-weighting filter | RLB-weighted high-shelf + high-pass | BS.1770-4 |
| True-peak oversampling | 4x minimum | ITU-R BS.1770-4 Annex 2 |

## Tool Cross-Check

When two tools disagree by >0.5 LU on Integrated LUFS, suspect:
1. Different gating implementations (some libs skip the relative gate).
2. Different K-weighting filter coefficients (rare; usually rounding).
3. Different downmix matrix for multi-channel.
4. One tool measuring per-channel mean instead of true loudness sum.

Always cross-check with `ffmpeg -af ebur128` as the BS.1770-4 reference implementation, and `pyloudnorm` for Python pipelines.

## Common Mistakes

- **Reporting RMS as "loudness"**: RMS is not K-weighted, not gated, not LUFS. Don't conflate.
- **Reporting peak as True Peak**: sample peak ≠ inter-sample peak. True Peak requires oversampling.
- **Measuring before final master**: BUS compression and limiting change LUFS by 2-4 LU. Measure the master, not the mix.
- **Ignoring True Peak for streaming**: most streaming-induced distortion comes from inter-sample-peak overshoot during transcoding, not Integrated LUFS being too loud.
- **Trusting embedded ReplayGain tags**: re-measure; tags are often stale or from different algorithms.
