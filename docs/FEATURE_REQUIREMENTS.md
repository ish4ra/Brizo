# Feature Requirements

Status legend: **Planned** = agreed goal, not started · **Research** = feasibility unknown.
Every item below is currently **not implemented**.

Priority: **P0** first usable build · **P1** early beta · **P2** later.

## A. Dual extension ecosystem (Research)

| ID | Requirement | Priority | Notes |
| --- | --- | --- | --- |
| EXT-1 | Install and run Chrome (Chromium) extensions | P1 | Native if a Chromium-family base is chosen |
| EXT-2 | Install and run Firefox WebExtension add-ons | P2 | Requires a compatibility layer on a Chromium base (or vice versa) |
| EXT-3 | Unified extension manager UI | P1 | One list, one permission model |
| EXT-4 | Chrome Web Store integration | P1 | Only where store terms permit |
| EXT-5 | Mozilla Add-ons (AMO) integration | P2 | Only where AMO terms permit |
| EXT-6 | Local CRX / XPI install | P2 | Signature and permission checks required |
| EXT-7 | Manifest V2 / V3 compatibility research | P1 | Document what is and is not possible |
| EXT-8 | Secure, transparent permission prompts | P1 | No silent permission escalation |

Acceptance: compatibility is measured against a published test list of real
extensions. No "works with all extensions" claim.

## B. Built-in privacy engine (Planned)

| ID | Requirement | Priority |
| --- | --- | --- |
| PRV-1 | Network ad & tracker blocking, on by default | P0 |
| PRV-2 | EasyList / EasyPrivacy filter syntax compatibility | P0 |
| PRV-3 | Cosmetic (element-hiding) filtering | P1 |
| PRV-4 | Custom filter lists and custom rules | P1 |
| PRV-5 | Per-site protection toggle and status UI | P0 |
| PRV-6 | Element picker | P2 |
| PRV-7 | Popup blocking | P0 |
| PRV-8 | Advanced-user controls (dynamic filtering-style) | P2 |
| PRV-9 | Filter list updates over HTTPS with integrity checks | P0 |

Candidate building blocks (to evaluate, not yet chosen): Brave `adblock-rust`
(MPL-2.0), uBlock Origin's engine (GPL-3.0), Chromium subresource filter.

## C. Integrated Media Grabber (Planned)

| ID | Requirement | Priority |
| --- | --- | --- |
| MED-1 | Detect video / audio / image resources on a page | P1 |
| MED-2 | Direct file download | P1 |
| MED-3 | HLS & DASH download for authorised, non-DRM media | P1 |
| MED-4 | Quality selection; audio-only extraction | P1 |
| MED-5 | Bulk image download | P2 |
| MED-6 | Queue with pause / resume / retry | P1 |
| MED-7 | Parallel segmented downloads where servers allow | P2 |
| MED-8 | Audio + video merge; optional local conversion | P2 |

Hard rule: **no DRM circumvention, no bypassing access controls.**
Components to evaluate: yt-dlp (Unlicense), FFmpeg (LGPL/GPL by build), aria2 (GPL-2.0).

## D. Lightweight performance (Planned)

| ID | Requirement | Priority |
| --- | --- | --- |
| PERF-1 | Automatic tab sleeping with exclusions | P0 |
| PERF-2 | Smart tab discarding under memory pressure | P1 |
| PERF-3 | Lazy session restore | P0 |
| PERF-4 | Reduced / on-demand background services | P1 |
| PERF-5 | Battery-aware behaviour | P2 |
| PERF-6 | Efficient extension execution (suspend idle background pages) | P2 |
| PERF-7 | Reproducible benchmark suite before any public performance claim | P1 |

Constraint: sandboxing, site isolation, certificate validation and other
security protections are **never** reduced to save resources.

## E. Desktop experience (Planned)

| ID | Requirement | Priority |
| --- | --- | --- |
| UX-1 | Horizontal tabs | P0 |
| UX-2 | Vertical tabs | P1 |
| UX-3 | Tab groups | P1 |
| UX-4 | Workspaces | P2 |
| UX-5 | Session management | P1 |
| UX-6 | Bookmarks & history | P0 |
| UX-7 | Profiles | P1 |
| UX-8 | Password manager | P1 |
| UX-9 | Light & dark themes, customisation | P0 |
| UX-10 | Picture-in-picture | P1 |
| UX-11 | Split-screen browsing | P2 |
| UX-12 | Advanced download manager | P1 |
| UX-13 | Optional userscript manager | P2 |
| UX-14 | Secure, signed automatic updates | P0 |

New features must be justified against the lightweight philosophy.
