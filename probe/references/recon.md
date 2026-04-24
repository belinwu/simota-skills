# External Attack-Surface Recon Reference

Purpose: Map an organization's externally reachable attack surface using passive and lightly-active OSINT techniques — subdomain enumeration, certificate transparency, DNS, technology fingerprinting, exposed-secret search, leaked-credential lookup. Reconnaissance only — no exploitation, no auth attempts, no active vulnerability scanning.

## Scope Boundary

- **Probe `recon`**: passive / low-touch recon. Output is an inventory (assets, tech, exposures, leaked secrets) — not a penetration test. No exploitation, no credential spraying, no active scanning of discovered assets without a separate scope change.
- **Breach**: full red-team engagement including initial access, lateral movement, and objective achievement. `recon` is the first phase Breach would run, broken out as an explicit standalone deliverable.
- **Sentinel**: static source audit of known repositories. `recon` searches the *public internet* (including GitHub, Pastebin, search dorks) for leaked material from any repo, including ones the org didn't know were public.
- **Other Probe recipes** (`zap`/`burp`/`nuclei`/`api`/`mobile`/`pentest`): active DAST. `recon` feeds them a target list; it never attacks.

If the question is "what's out there?" → `recon`. "Can we break in?" → Breach. "Is this specific repo leaking?" → Sentinel.

**AUTHORIZATION**: Passive recon against material the target organization has chosen to publish (DNS, CT logs, public repos, Shodan snapshots) is generally lawful without written authorization, BUT:

- Some techniques cross into active territory: DNS zone transfer attempts, reverse-IP portscans, unauthenticated fetches of discovered admin panels, brute-force subdomain resolution at high rate, login-page access. These require written scope.
- Any active probing of discovered assets (port scan, vulnerability scan, auth attempt) requires separate written authorization naming those assets.
- Leaked-credential verification MUST NOT include actually logging in — confirm via hash match or HIBP-style APIs only.
- Default posture: passive OSINT only until scope expands in writing.

## Technique Inventory

| Layer | Technique | Tools | Passive/Active |
|-------|-----------|-------|----------------|
| Subdomain | Passive enumeration | `subfinder`, `amass enum -passive`, `assetfinder` | Passive |
| Subdomain | Certificate transparency | `crt.sh`, `censys`, `shuffledns` on CT data | Passive |
| Subdomain | Brute force | `puredns`, `shuffledns` with resolvers | Active (DNS) — scope required |
| DNS | Zone walking / NSEC | `dnsrecon`, `dig` | Passive (read-only) |
| DNS | Zone transfer (AXFR) | `dig axfr` | Active — explicit scope required |
| IP / port | Shodan / Fofa / Censys / ZoomEye | API queries | Passive (third-party snapshot) |
| IP / port | Direct port scan | `nmap`, `masscan`, `naabu` | Active — scope required |
| Tech fingerprint | Passive HTTP headers via Wappalyzer / httpx | `httpx -tech-detect` | Low-active (one GET) |
| Secrets | Public repo search | `trufflehog`, `gitleaks` in `--source=github`, GitHub code search, grep.app | Passive |
| Secrets | Pastebin / Gist / archive.org | `pastebin` monitors, `waybackurls` | Passive |
| Credentials | HIBP, DeHashed, Leak-Lookup | API queries | Passive — DO NOT log in to confirm |
| Cloud | Bucket enumeration | `cloud_enum`, `s3scanner` | Low-active — scope-recommended for bucket reads |

## Workflow

```
PLAN      →  confirm scope: root domains, known IP ranges, subsidiaries in-scope
          →  declare passive-only vs scope-expanded (active DNS, port scan, cloud)
          →  declare destinations off-limits (M&A targets, shared infra, third-party SaaS)
          →  note legal jurisdiction; some countries treat portscans as unauthorized access

SCAN      →  subdomain: subfinder + amass passive + assetfinder + crt.sh; dedupe
          →  resolve: `dnsx` passive pass (no brute)
          →  CT monitor: snapshot active certs to catch staging/dev leaks
          →  shodan/fofa/censys by org name, SSL cert CN/SAN, favicon hash
          →  tech fingerprint: `httpx -tech-detect -title -status-code` (single GET per host)
          →  secret search: trufflehog on GitHub org + public-mention dorks
          →  leaked creds: HIBP breach count per employee email domain (no confirmation logins)
          →  wayback / archived URLs: `waybackurls`, `gau` for historical endpoints

VALIDATE  →  dedupe + ownership confirmation (WHOIS, ASN) — avoid reporting assets not owned
          →  flag shadow IT vs sanctioned assets
          →  flag high-signal exposures: dev/staging panels, exposed `.git`, open S3, debug endpoints
          →  mark each exposure: Confirmed (observed directly) vs Suggested (indirect signal)

REPORT    →  inventory: subdomains, IPs, tech stack, exposed services, leaked secrets
          →  risk-ranked: what would a real attacker target first
          →  recommend next: `pentest` / `zap` / `api` / `mobile` for prioritized active follow-up
```

## Passive-First Toolchain

```bash
# Subdomain aggregation (all passive)
subfinder -d example.com -all -silent              > subs.txt
amass enum -passive -d example.com                 >> subs.txt
assetfinder --subs-only example.com                >> subs.txt
curl -s "https://crt.sh/?q=%25.example.com&output=json" | jq -r '.[].name_value' >> subs.txt
sort -u subs.txt > subs.uniq.txt

# Resolve passively (no brute)
dnsx -silent -l subs.uniq.txt -a -resp > resolved.txt

# Tech fingerprint with single GET per host
httpx -l resolved.txt -tech-detect -title -status-code -silent > fingerprint.txt

# Leaked secrets in org's public GitHub footprint
trufflehog github --org=example --only-verified
```

## Leaked-Credential Handling

- Query HIBP / DeHashed / similar for domains and executive emails.
- Report: count, earliest breach, most recent, password-exposure class (plaintext / hashed / hash-cracked).
- **Never** attempt to log into the target's systems with discovered credentials — even to "confirm". That crosses from recon into unauthorized access.
- Recommend org-side rotation and MFA rollout; defer authenticated validation to a scoped `pentest` engagement.

## Anti-Patterns

- Brute-force subdomain resolution at 10k req/s against authoritative nameservers — DoS-adjacent, burns goodwill, triggers alerts.
- Crawling discovered admin panels "just to see" — that's unauthorized access once a login form appears.
- Including assets that WHOIS / ASN shows belong to a third party (CDN edge, shared SaaS) as "target exposures" — noise and potential legal exposure.
- Publishing recon output externally — this is a target-attack blueprint; treat as confidential.
- Using discovered credentials to verify validity — see above; never do this.
- Treating Shodan snapshots as current truth — re-verify timestamps; service may have moved.

## Handoff

- **→ `pentest` / `zap` / `nuclei` / `api` / `mobile`**: prioritized target list with tech fingerprint; requires scope expansion to active.
- **→ Sentinel**: discovered public repos with secret hits → static audit.
- **→ Breach**: full inventory feeds red-team planning; `recon` is the input, Breach owns the adversary scenario.
- **→ Canvas**: attack-surface map visualization.
- **→ Triage**: actively-exposed critical asset (exposed `.env`, public admin panel with default creds evidenced indirectly) → immediate escalation.
- **→ Cloak**: leaked PII / credential trove with privacy-law implications (GDPR notification clock).
