# Web Sources & Third-Party Metadata APIs

Catalog of third-party APIs for acoustic fingerprinting, metadata enrichment, and lyrics lookup. Every entry includes auth, rate limit, what gets transmitted (fingerprint hash vs raw audio), and data-retention notes. Cite the source API and retrieval timestamp on every external-data claim.

## Privacy Policy (mandatory)

Sonar enforces a **consent gate** on every network call:
- **`--network=ask`** (default): prompt before the first call per session; cache subsequent calls.
- **`--network=allow`**: session-level consent for fingerprint-only APIs; raw-audio APIs still require per-call consent.
- **`--network=deny`**: local-only; skip all lookups; report `lookup: skipped (no-consent)`.

**Never** silently upload audio bytes to a third-party API. **Always** generate the Chromaprint fingerprint locally via `fpcalc` before any network call — the hash, not the audio, leaves the machine for AcoustID-class lookups.

## API Catalog

### A. Acoustic Fingerprinting & Track Identification

| API | Endpoint | Free tier | Auth | What's uploaded | Retention | 2026 status |
|-----|----------|-----------|------|-----------------|-----------|-------------|
| **AcoustID v2** | `https://api.acoustid.org/v2/lookup` | Free for non-commercial; commercial via acoustid.biz | `client` API key (app), `user` key only for submissions | **Chromaprint hash only** (no raw audio) | Anonymized fingerprints only; no audio retained | Active. Default recommended path. |
| **MusicBrainz WS/2** | `https://musicbrainz.org/ws/2/{entity}/{mbid}?fmt=json` | Unlimited within rate limit (1 req/sec/IP) | None for read; OAuth/Digest for write | No audio | N/A | Active. Descriptive `User-Agent: AppName/x.y ( contact )` MANDATORY. Anonymous UA throttled to 50 r/s aggregate. |
| **AudD** | `https://api.audd.io/` | First 300 requests free (per third-party reports; not on official docs) | `api_token` form/query param | **Raw audio (URL / multipart / base64)** | Raw audio kept ~72h, fingerprints indefinitely (third-party-sourced; AudD's privacy page text unverified via direct fetch) | Active. Paid: $2-5 per 1000 file requests. **Per-call consent required.** |
| **ACRCloud** | `https://identify-{region}.acrcloud.com/v1/identify` | Trial only | `access_key` + HMAC-SHA1 signature | Fingerprint or raw audio (mode-dependent) | Commercial TOS — verify before use | Active. **Per-call consent required for raw-audio mode.** |
| **Apple ShazamKit** | Native SDK (iOS/macOS/visionOS/Android) | Free with Apple Developer account | App entitlement | Audio signatures (lossy, non-invertible per Apple) | "Audio not shared with Apple; signatures cannot be inverted" | Active. **No HTTP API — on-device only**, unusable from CLI Python. |
| **Shazam unofficial HTTP wrappers** | Various (RapidAPI, shazam-api.com) | Varies | Third-party | Audio upload | Not sanctioned by Apple; ToS-violating; subject to break | **Avoid for production.** |

### B. Metadata & Release Info

| API | Endpoint | Free tier | Auth | Notes |
|-----|----------|-----------|------|-------|
| **MusicBrainz WS/2** | (see above) | 1 req/sec/IP | UA required | Canonical free metadata source. Lookup by MBID / ISRC / metadata search |
| **Discogs** | `https://api.discogs.com/` | 60 r/min authed, 25 r/min anonymous | Personal access token, OAuth 1.0a, or consumer key/secret | Release, label, marketplace data. Headers `X-Discogs-Ratelimit{,-Used,-Remaining}`. Unique `User-Agent` required |
| **ListenBrainz** | `https://api.listenbrainz.org/1/...` | Free, no per-key cap published | User token for writes; reads token-optional | MetaBrainz-operated FOSS alternative. Similar-artists labs at `https://labs.api.listenbrainz.org/similar-artists` |
| **MusicBrainz Pictures (CAA)** | `https://coverartarchive.org/release/{mbid}` | Free | None | Cover art from Cover Art Archive |
| **AcousticBrainz** | Historical dataset | Free (bulk download) | None | **Submission discontinued 2022**; dataset still downloadable for offline use |

### C. Recommendation / Similar Tracks (External)

| API | Endpoint | Free tier | Notes |
|-----|----------|-----------|-------|
| **Last.fm `track.getSimilar`** | `http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&...` | Free; rate limit unpublished; error 29 on overage | Returns `match` score 0-1. Good for popular tracks; sparse for indie/new releases |
| **Last.fm `artist.getSimilar`** | `...&method=artist.getsimilar&...` | Same | Similar artists list |
| **ListenBrainz CF recommendations** | `/1/cf/recommendation/user/{name}/recording` | Free | Collaborative-filter recommendations |
| **ListenBrainz similar-artists labs** | `https://labs.api.listenbrainz.org/similar-artists` | Free | MBID-based |
| **Spotify `/v1/recommendations` / `/v1/audio-features` / `/v1/audio-analysis` / `/v1/artists/{id}/related-artists`** | (Web API) | **DEPRECATED 2024-11-27 for new apps** | Only apps with prior extended-mode approval still work. No re-enable through 2026-02 changelog. **Do not target for new sonar deployments.** [Source: Spotify dev blog 2024-11-27, TechCrunch] |

### D. Lyrics

| API | Endpoint | Free tier | Notes |
|-----|----------|-----------|-------|
| **Genius** | `https://api.genius.com/search`, `/songs/{id}` | Free with registered client | OAuth 2.0 bearer. **Returns metadata + URL only** — full lyrics require scraping the page (legally contested; safest = quote attribution + URL link, not mass redistribution) |
| **MusixMatch** | Commercial API | Paid | Licensed lyrics access. Use when commercial-grade lyrics are required |

**Legal note**: Lyrics scraping outside a licensed API is legally contested (cf. *hiQ v. LinkedIn* on public-data scraping). Sonar's policy: cite attribution + URL via Genius's licensed metadata API; refuse mass redistribution of scraped lyrics text.

### E. Touring / Performance

| API | Endpoint | Free tier | Notes |
|-----|----------|-----------|-------|
| **Songkick** | `https://api.songkick.com/api/3.0/` | Free with API key | Concert / tour data |
| **Setlist.fm** | `https://api.setlist.fm/rest/1.0/` | Free with API key | Live setlists |

## Code Skeletons

### Skeleton 1: Local Fingerprint + AcoustID Lookup (privacy-safe default)

```python
# pip install pyacoustid musicbrainzngs requests
# System: fpcalc binary (apt install acoustid-fingerprinter / brew install chromaprint)
import os, requests
import acoustid
import musicbrainzngs as mb

ACOUSTID_KEY = os.environ.get("ACOUSTID_API_KEY")  # required
if not ACOUSTID_KEY:
    raise RuntimeError("ACOUSTID_API_KEY missing — eagerly Read env vars at INGEST")

mb.set_useragent("sonar", "0.1", "you@example.com")  # MANDATORY for MusicBrainz

def identify_track(audio_path: str) -> dict:
    # Step 1: fingerprint locally — no audio leaves the machine
    duration, fp = acoustid.fingerprint_file(audio_path)

    # Step 2: send fingerprint hash + duration only (privacy-safe)
    r = requests.get("https://api.acoustid.org/v2/lookup", params={
        "client": ACOUSTID_KEY,
        "meta": "recordings releasegroups",
        "duration": int(duration),
        "fingerprint": fp,
    })
    results = r.json().get("results", [])
    if not results:
        return {"match": "no match", "candidates": []}

    # Honesty: return ALL candidates if multiple, ranked by score
    candidates = []
    for res in results[:5]:
        for rec in res.get("recordings", []):
            candidates.append({
                "mbid": rec["id"],
                "title": rec.get("title", "(unknown)"),
                "artist": rec.get("artists", [{}])[0].get("name", "(unknown)"),
                "score": res.get("score", 0.0),
            })

    # Step 3: resolve via MusicBrainz (1 req/sec — musicbrainzngs auto-throttles)
    for c in candidates[:3]:
        try:
            rec = mb.get_recording_by_id(c["mbid"], includes=["artists", "releases", "tags"])
            c["releases"] = [r["title"] for r in rec["recording"].get("release-list", [])[:3]]
            c["tags"] = [t["name"] for t in rec["recording"].get("tag-list", [])[:5]]
        except mb.MusicBrainzError:
            pass

    return {
        "match": "ambiguous" if len(candidates) > 1 else "match",
        "candidates": candidates,
        "method": "AcoustID + MusicBrainz",
        "source_apis": ["acoustid.org/v2/lookup", "musicbrainz.org/ws/2"],
        "retrieved_at": "<ISO timestamp>",
    }
```

### Skeleton 2: Last.fm Similar Tracks

```python
# pip install requests
import os, requests

LASTFM_KEY = os.environ.get("LASTFM_API_KEY")
if not LASTFM_KEY:
    raise RuntimeError("LASTFM_API_KEY missing")

def similar_tracks(artist: str, track: str, limit: int = 20) -> list[dict]:
    r = requests.get("http://ws.audioscrobbler.com/2.0/", params={
        "method": "track.getsimilar",
        "artist": artist,
        "track": track,
        "api_key": LASTFM_KEY,
        "format": "json",
        "limit": limit,
    })
    out = []
    for t in r.json().get("similartracks", {}).get("track", []):
        out.append({
            "title": t["name"],
            "artist": t["artist"]["name"],
            "match": float(t.get("match", 0)),  # 0-1 similarity
            "mbid": t.get("mbid"),
            "method": "lastfm.track.getSimilar",
        })
    return out
```

### Skeleton 3: Consent Gate Decorator

```python
import functools

_session_consent = {"fingerprint_only": None, "raw_audio_per_call": True}

def requires_network_consent(category: str = "fingerprint_only"):
    """category: 'fingerprint_only' (session-level OK) or 'raw_audio' (per-call required)."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if category == "fingerprint_only":
                if _session_consent[category] is None:
                    print(f"[consent] {fn.__name__} will send a fingerprint hash to a third-party API.")
                    ans = input("Allow for this session? [y/N] ").strip().lower()
                    _session_consent[category] = ans == "y"
                if not _session_consent[category]:
                    return {"error": "lookup skipped (no consent)", "consent": "denied"}
            elif category == "raw_audio":
                print(f"[consent] {fn.__name__} will upload RAW AUDIO bytes.")
                print("  The API may retain or train on uploaded content.")
                ans = input("Allow this specific call? [y/N] ").strip().lower()
                if ans != "y":
                    return {"error": "upload skipped (no consent)", "consent": "denied"}
            return fn(*args, **kwargs)
        return wrapper
    return decorator
```

### Skeleton 4: Cache-First Lookup Pattern

```python
# pip install requests-cache
import requests_cache

# Persistent SQLite cache — re-hitting paid APIs for the same content is wasteful
session = requests_cache.CachedSession(
    cache_name="sonar_api_cache",
    backend="sqlite",
    expire_after=86400 * 30,  # 30 days
)

# All subsequent session.get(...) calls are cache-first
r = session.get("https://api.acoustid.org/v2/lookup", params={...})
print("From cache?" , r.from_cache)
```

### Skeleton 5: Genius Metadata Lookup (no full-lyrics scraping)

```python
# pip install lyricsgenius
import os
import lyricsgenius

GENIUS_TOKEN = os.environ.get("GENIUS_ACCESS_TOKEN")
genius = lyricsgenius.Genius(GENIUS_TOKEN, skip_non_songs=True)

def fetch_lyrics_metadata(artist: str, title: str) -> dict:
    song = genius.search_song(title, artist)
    if not song:
        return {"error": "not found"}
    return {
        "title": song.title,
        "artist": song.artist,
        "url": song.url,
        "release_date": str(song.release_date) if song.release_date else None,
        "media": song.media,  # links to YouTube, Spotify (not lyrics text)
        "method": "Genius API (metadata only)",
        "note": "Quote attribution + URL link is policy. Full-lyrics scraping is legally contested.",
    }
```

## Error Handling

| Error | Cause | Sonar response |
|-------|-------|----------------|
| AcoustID `400 Invalid fingerprint` | fpcalc version mismatch | Re-generate with current `pyacoustid`; warn user |
| AcoustID `429 Rate limit` | Too many requests | Exponential backoff; cache-first prevents recurrence |
| AcoustID no match | Unknown / unreleased track | Report `match: no match`; suggest local CLAP-embedding kNN (see `similarity-inference.md`) |
| AcoustID ambiguous (>1 candidate) | Multiple recordings hash-collide | Return ALL candidates ranked. Never silently pick top hit |
| MusicBrainz `503 Service Unavailable` | Rate limit (1 r/s exceeded) | Throttle; retry after 1s |
| MusicBrainz `404 Not Found` | MBID unknown | Skip enrichment; return fingerprint match alone |
| Last.fm `error 29` | Rate limit exceeded | Exponential backoff |
| Spotify `403 Forbidden` (new app) | Endpoint deprecated for non-grandfathered apps | Skip; use local CLAP-embedding kNN instead |
| Genius lyrics page returns HTML shell | Bot detection | Use metadata only; do not scrape |

## Library Pins

```python
# Web/metadata stack
pyacoustid>=1.3.0      # Chromaprint fingerprinting wrapper
musicbrainzngs>=0.7.1  # MusicBrainz client
python3-discogs-client>=2.7
pylast>=5.3            # Last.fm client
liblistenbrainz>=0.6   # ListenBrainz client
lyricsgenius>=3.0      # Genius metadata client
requests-cache>=1.2    # SQLite cache layer
spotipy>=2.24          # Spotify (legacy apps only; new apps blocked)
requests>=2.31

# System binaries
fpcalc                 # Chromaprint — apt install acoustid-fingerprinter / brew install chromaprint
```

## Required Environment Variables (front-load at INGEST)

| Variable | Required for | Get key at |
|----------|--------------|-----------|
| `ACOUSTID_API_KEY` | AcoustID lookup | https://acoustid.org/api-key |
| `LASTFM_API_KEY` | Last.fm similar tracks/artists | https://www.last.fm/api/account/create |
| `DISCOGS_USER_TOKEN` | Discogs metadata | https://www.discogs.com/settings/developers |
| `GENIUS_ACCESS_TOKEN` | Genius metadata | https://genius.com/api-clients |
| `SPOTIFY_CLIENT_ID` + `SPOTIFY_CLIENT_SECRET` | Legacy Spotify apps only | https://developer.spotify.com/dashboard |

**Eager-Read at INGEST**: For the `explore` recipe, check every required env var at INGEST and abort with a clear missing-key error before emitting any pipeline code. Cheap vs cost of failing partway through a network pipeline.

## Sonar Decision Matrix

| Goal | Recommended path | Avoid |
|------|------------------|-------|
| Identify an unknown track (privacy-safe) | `fpcalc` → AcoustID → MusicBrainz | Shazam unofficial HTTP (ToS-violating) |
| Identify with higher recall (esp. recent releases) | AcoustID first; AudD as paid fallback with per-call consent | Spotify (deprecated for new apps) |
| Similar tracks (popular catalog) | Last.fm `track.getSimilar` | Spotify recommendations (deprecated) |
| Similar tracks (privacy / indie / unreleased) | Local CLAP-embedding kNN (see `similarity-inference.md`) | Any API requiring full-audio upload |
| Artist bio / release / label info | MusicBrainz → Discogs | — |
| Lyrics metadata + URL | Genius API | Lyrics-page scraping (legally contested) |
| Concert / tour data | Songkick or Setlist.fm | — |

## Unresolved / Unverified

- AudD `audd.io/privacy/` exact retention text — WebFetch returned navigation-only shell; 72h retention sourced from third-party wikis. Re-verify before relying on the figure for any compliance claim.
- Last.fm per-API-key requests-per-minute cap — not published in official endpoint docs; only error code 29 documented.
- ListenBrainz rate limits — none specified in the recommendations API docs page.
- Spotify Extended Audio Features (Musicae third-party proxy) — re-exposes deprecated endpoints; legal/longevity status unverified for production use.
