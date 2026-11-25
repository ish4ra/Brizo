# Browser Foundation Comparison

Verified 2026-11-25. Evidence labels and source IDs: [SOURCES.md](SOURCES.md).
Ratings are relative judgements for **a small FOSS team on free
infrastructure**, not a measure of each project's quality.

## 1. Architecture types

| Type | Examples | What Brizo would maintain |
| --- | --- | --- |
| **Downstream patch set** on an engine tarball | ungoogled-chromium, Helium, Zen, LibreWolf | A patch series + build scripts, rebased on every upstream release |
| **Full fork** with own history | Brave (brave-core over Chromium), Waterfox | A large divergent tree; very high rebase cost |
| **Embedding a prebuilt engine** | CEF apps, Qt WebEngine apps, Electron apps | Own browser shell (tabs, UI, storage) around an engine library |
| **System WebView / WebKit** | Orion (WebKit), WebKitGTK/WPE apps | Own shell + own extension runtime |

## 2. Candidates

| Candidate | Engine | Licence | Chrome ext. | Firefox add-ons | Native blocking prior art | Free-build outlook | Small-team maintenance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Chromium** (direct) | Blink | BSD-3 + third-party | Native; MV2 removed from Chrome Web Store 2026-08-31 (UBO1) | No | Subresource filter (Chromium) [A] | Poor: ≥100 GB, no Linux→mac cross (CR1, CR3) | Hard (4-week milestones) |
| **Ungoogled Chromium** | Blink | BSD-3 (patches) | Native; carries MV2 re-enable patch (UC1) | No | — | Poor; sponsored runners cut "days to hours" (UC2) | Medium: patch set is ~112 entries (UC1) [V] |
| **Helium** | Blink (ungoogled base) | GPL-3.0 own code (HE1) | Native + MV2 patch; bundled uBO fork (HE1) | No | uBO built in | Poor (sponsored runners, HE2) | Medium–hard (~397 patch entries) [V] |
| **Brave / brave-core** | Blink | MPL-2.0 (BR1) | Native; Brave-specific MV2 handling [A] | No | **adblock-rust** native (BR2) | Very poor (same Chromium cost plus Brave tooling) | Very hard to fork; strong source of components |
| **Firefox / Gecko** | Gecko | MPL-2.0 | No CRX; many popular extensions publish Firefox builds (see EXTENSION_COMPATIBILITY) | **Native, MV2 + MV3 incl. blocking webRequest** (MDN1) | uBO runs at full strength [V: UBO1 "works best on Firefox"] | **Best**: 0.77 GiB source, Linux cross-compile to mac/win (ZEN1) | Medium: 4-week releases, or ESR |
| **LibreWolf** | Gecko | MPL-2.0 | — | Native; ships uBO [A] | uBO bundled [A] | Builds on its own CI [U] | Patch-set model, close to Brizo's needs |
| **Floorp** | Gecko | MPL-2.0 (FL1) | — | Native | — | Not checked [U] | Heavier UI fork |
| **Zen** | Gecko (Firefox 161.0) | MPL-2.0 (ZEN1) | — | Native | — | **Proven pattern**: Linux runners compile all 3 OSes (sponsored 8–16 vCPU) (ZEN1) | Patch set + "surfer" tooling |
| **Waterfox** | Gecko | MPL-2.0 [A] | — | Native | — | `mach` builds (WF1); CI not checked [U] | Full-tree fork |
| **WebKit** (WebKitGTK/WPE, Apple WKWebView) | WebKit | LGPL/BSD | Must build own WebExtension runtime | Same | Apple content-blocker format (adblock-rust can export, BR2) | Linux OK; **Windows port weak** [A] | Very hard (whole extension layer) |
| **Orion** (reference only) | WebKit | Proprietary macOS app; Linux/Windows code reportedly open-sourced Oct 2026 (S2) [U] | Experimental, via its own WebExtensions port (S1) | Same | Built-in blocker [S] | n/a | Shows dual-ecosystem support needs a large custom runtime |
| **Qt WebEngine** | Blink (lagging) | LGPL-3 / GPL / commercial | New `QWebEngineExtensionManager` (QT1); scope limited [A] | No | — | **Good** (prebuilt Qt) | Security lag behind Chromium [A] |
| **CEF** | Blink | BSD (CEF1) | Partial, depending on runtime style [A] | No | — | **Good** (prebuilt CEF binaries) [A] | Must build a whole browser UI; patch cadence tied to CEF |
| **Electron** | Blink | MIT | "Subset" of Chrome APIs; not arbitrary extensions (EL1) | No | — | Good | Not designed as a general browser; heavy per-app runtime |

## 3. Scoring against Brizo's goals (1 = poor, 5 = strong)

| Goal | Chromium patch set | Gecko patch set | CEF/Qt shell |
| --- | --- | --- | --- |
| Website compatibility | 5 | 4 | 4 (lagging versions) |
| Chrome extensions | 5 (CWS now MV3-only) | 2 (native Firefox builds of the same extensions; no CRX) | 2 |
| Firefox add-ons | 1 | 5 | 1 |
| Full uBlock Origin / MV2 power | 3 (patch must survive upstream removal) | 5 | 1 |
| Native content blocking | 5 (adblock-rust precedent in Brave) | 4 (bundle uBO, or integrate adblock-rust) | 3 |
| Media Grabber integration | 4 | 4 | 3 |
| RAM/CPU optimisation hooks | 4 | 4 | 3 |
| Native UI customisation | 3 (C++/WebUI) | 4 (chrome JS/CSS) | 5 |
| Cross-platform | 5 | 5 | 4 |
| Security maintenance for a small team | 2 (heavy rebuilds) | 4 | 2 (vendor lag) |
| **Free cloud build** | **1** | **4 (pending measurement)** | 5 |
| Licensing simplicity | 4 | 5 | 3 |

## 4. Conclusions

1. **Free builds decide the choice.** Chromium is the strongest engine on paper,
   but its build demands (≥100 GB, no Linux→macOS cross) and the experience
   of ungoogled-chromium and Helium ("days" without sponsored runners) rule out a
   timely, free, cloud-only pipeline today.
2. **Gecko is the only full-browser foundation with a credible free pipeline**:
   a small source tree (0.77 GiB), cross-compilation of all three desktop
   targets from Linux (used in production by Zen), MPL-2.0 throughout, native
   Firefox add-ons including MV2 and blocking webRequest, and full-strength uBO.
3. **Embedding (CEF/Qt)** makes builds trivial but cannot meet the extension
   goals and inherits vendor security lag. It is useful only as a UI prototype
   harness.
4. **Orion** confirms that running both ecosystems on one engine needs a large
   custom WebExtensions runtime. Brizo should not promise that.

See [ARCHITECTURE_DECISION_PROPOSAL.md](ARCHITECTURE_DECISION_PROPOSAL.md).
