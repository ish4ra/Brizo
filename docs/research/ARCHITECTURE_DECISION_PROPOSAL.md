# Architecture Decision Proposal (ADR draft, needs owner approval)

Date: 2026-11-25 · Status: **Proposed** · Decision owner: project owner
Evidence: [SOURCES.md](SOURCES.md) and the linked research documents.

## Decision requested

**Verdict: CONDITIONAL GO** on a **Gecko (Firefox Release) downstream patch
set** as Brizo's primary browser foundation, conditional on the free-build
measurement below.

## 1. Verified facts that drive the decision

1. Free GitHub runners for public repos: 4 vCPU / 16 GB (Linux, Windows),
   3 CPU / 7 GB (macOS arm64), 6 h per job, 10 GB cache [V GH1–GH3, M probe].
2. Real free disk is large (Linux 116 GiB after cleanup, Windows D: 220 GiB) but undocumented [M].
3. Chromium needs ≥100 GB disk and > 16 GB RAM is "highly recommended", and
   macOS targets need a macOS host [V CR1, CR3]. Chromium downstreams credit
   sponsored runners for going "from days to hours" [V UC2, HE2].
4. Gecko's source archive is 0.77 GiB vs Chromium's 3.95 GiB [M]. Zen compiles
   Linux, Windows **and macOS** releases on Linux runners [V ZEN1].
5. The Chrome Web Store removed all MV2 extensions on 2026-08-31 [V UBO1].
   Firefox keeps MV2 and blocking webRequest, and uBO "works best on Firefox" [V UBO1, MDN1].

## 2. Proposed architecture (primary)

| Layer | Choice |
| --- | --- |
| Engine | Gecko, tracking **Firefox Release**; unbranded; patch set applied to official source tarballs (Zen/LibreWolf model) |
| Build | GitHub-hosted `ubuntu-latest` compiles Linux x64, **macOS arm64 (cross)** and Windows x64 (cross); `macos-latest`/`windows-latest` only for packaging and smoke tests; sccache with the Actions cache; `free-disk-space` |
| UI | Gecko front-end (JS/CSS) customisations: vertical tabs, workspaces, split view, theme |
| Content blocking | Built-in unmodified uBlock Origin (4a), optional adblock-rust native layer (4b) |
| Extensions | Firefox add-ons native (MV2 + MV3). Chrome-only extensions: later research into an MV3 import/shim, never "universal" |
| Media Grabber | Native detector + queue; FFmpeg (LGPL) and optional yt-dlp as sandboxed helpers |
| Updates | MAR updater with Brizo key, GitHub Releases, attestations, SBOM |
| Licence | MPL-2.0 recommended (pending approval) |

## 3. Conditions for GO (Phase 1b, bounded, zero cost)

| # | Condition | Pass criterion |
| --- | --- | --- |
| C1 | Unbranded Firefox 161 opt build on `ubuntu-latest` | Completes in **< 5.5 h** in one job, peak RAM < 15 GiB, disk fits |
| C2 | Rebuild with warm sccache | Clearly faster than C1 (security-update path) |
| C3 | Linux → macOS arm64 cross build | Produces an app that launches on `macos-latest` (ad-hoc signed) |
| C4 | Linux → Windows x64 cross build | Produces an installer or zip that launches on `windows-latest` |

If C1 fails: try `ubuntu-24.04-arm` and chained jobs. If still failing, see fallback.

## 4. Fallbacks

| Rank | Fallback | When | Trade-off |
| --- | --- | --- | --- |
| F1 | **Chromium downstream patch set** on ungoogled-chromium (BSD patches) + adblock-rust | Owner obtains sponsored or donated runners (precedent UC2, HE2, ZEN1) or approves paid compute; or Chrome-extension nativeness is ranked above free builds | Best web and Chrome-extension compatibility; MV2 depends on a patch; heavy, slow builds |
| F2 | **CEF-based shell** with prebuilt CEF binaries | Only to prototype Brizo's UI while C1–C4 are pending | Builds free and fast; limited extensions, vendor security lag. Not a release vehicle |

## 5. Untested assumptions (must be validated)

- Gecko build time and memory on 4 vCPU/16 GB (C1) **[A]**.
- macOS SDK use in a public CI cross-build is permitted by Apple's SDK terms **[U]**. Needs a licence read before C3.
- Free disk on runners stays at current levels **[A]**.
- Store terms (CWS, AMO) for third-party browsers **[U]**.
- Kagi's open-sourced Orion Linux/Windows code (S2): licence and suitability **[U]**. Worth a follow-up look for the CRX/WebExtensions shim idea.

## 6. Unresolved blockers (not engine-related)

- Brizo name trademark search; logo provenance (BRAND_PROVENANCE).
- macOS public distribution needs a paid Apple Developer membership for
  notarisation (owner decision); Windows SmartScreen reputation.

## 7. Recommended next task

**Task 003: Gecko build feasibility experiment (C1–C4)**, i.e. bounded CI
experiments on free runners, no product code, results recorded with run links.
Browser implementation starts only after the owner approves this ADR and C1–C4 pass.
