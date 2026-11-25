# Native Content Blocking Architecture

Verified 2026-11-25. Labels and IDs: [SOURCES.md](SOURCES.md).

**Goal:** strong ad, tracker and popup blocking enabled by default, without the
user installing an extension. No claim of uBlock Origin parity without measurement.

## 1. Engines compared

| | uBlock Origin (full) | uBO Lite | adblock-rust | Brave Shields |
| --- | --- | --- | --- | --- |
| Form | WebExtension (MV2 on Chromium; MV2/MV3 on Firefox) | MV3 extension, declarative only (UBOL1) | Rust library 0.13.6 (BR2) | brave-core feature on top of adblock-rust |
| Licence | GPL-3.0 (UBO1) | GPL-3.0 [A] | **MPL-2.0** (BR2) | MPL-2.0 (BR1) |
| Network filtering | Yes, dynamic | Yes, DNR (static rulesets) | Yes | Yes |
| Cosmetic filtering | Yes | Yes (browser-injected CSS) | Yes (BR2) | Yes |
| Scriptlets / redirects | Yes | Limited by MV3 [A] | Yes, uBO-compatible resources (BR2) | Yes |
| Custom subscriptions | Any list | Built-in rulesets only [A] | Any list, compiled at runtime | Yes |
| Custom rules, element picker, logger | Yes | Partly [A] | Engine only; UI must be built | Yes (Brave UI) |
| Per-site controls | Yes | Yes (filtering modes) | Must be built | Yes |
| Runs without an extension | No | No | **Yes** (in-process) | Yes |
| Strength today | Reference implementation | Weaker against anti-adblock [A] | Production in Brave [V] | Production |

## 2. Recommendation by base

**Gecko base (primary):**
1. **Phase 4a, fastest and strongest:** ship **uBlock Origin as a built-in,
   preinstalled system add-on**, enabled by default with EasyList, EasyPrivacy
   and uBO's lists. It remains a separate GPL-3.0 component (an aggregate), is
   updated from its signed upstream releases, and is not modified. This mirrors
   LibreWolf [A] and Helium (a uBO fork, HE1).
2. **Phase 4b (optional):** evaluate **adblock-rust inside the network stack**
   (MPL-2.0, Rust, which Gecko already builds) for a native "Brizo Shields" layer:
   per-site toggle, early blocking before extensions run, popup and tracker
   rules. Keep uBO for advanced users.
3. Gecko's built-in Enhanced Tracking Protection stays on. Brizo adds to it
   and never weakens it.

**Chromium base (fallback):** integrate adblock-rust natively as Brave does
(BR1/BR2), because full uBO depends on an MV2 patch that upstream can break.

## 3. Feature checklist (for Phase 4 acceptance)

| Feature | Plan |
| --- | --- |
| Network filtering, EasyList/EasyPrivacy | uBO built-in (4a); adblock-rust (4b) |
| Cosmetic filtering, scriptlets, redirects | uBO; adblock-rust supports uBO resources (BR2) |
| Custom subscriptions and rules | uBO dashboard; Brizo settings later |
| Element picker, filter logger | uBO |
| Per-site controls | Brizo toolbar button wrapping uBO and ETP state |
| Automatic list updates | uBO's updater over HTTPS; Brizo pins the uBO version and updates through Brizo releases |
| Popup blocking | Gecko native popup blocker + filters |
| Advanced mode | uBO dynamic filtering |
| Filter list licences | EasyList licence page **not verified** (EL2); confirm before bundling lists inside the binary. Fetching lists at runtime avoids redistribution [A] |

## 4. Measurement before claims

Use a fixed corpus (e.g. 50 news, video and shopping sites) and record blocked
requests, page load time and memory, against stock Firefox with uBO and
Brave. No percentages are published until reproducible (see
[PERFORMANCE_BENCHMARK_PLAN.md](PERFORMANCE_BENCHMARK_PLAN.md)).
