# Technical Research Plan: Phase 1 (Engine Feasibility)

**Not started.** Requires owner approval before work begins.

## Question

Which browser foundation can Brizo realistically build, update and ship using
**only free infrastructure** (GitHub-hosted runners, free storage limits) and
**no mandatory local toolchain**, while meeting the goals in
[FEATURE_REQUIREMENTS.md](FEATURE_REQUIREMENTS.md)?

## Candidates

| Candidate | Why consider it | Main concerns to measure |
| --- | --- | --- |
| Chromium (direct) | Chrome extension compatibility, mature security | Source ~100+ GB with history; full build several hours on large machines; free runner limits |
| Brave (`brave-core` on Chromium) | Built-in adblock engine (`adblock-rust`), privacy patches | Same Chromium build cost plus Brave tooling; MPL-2.0 obligations; branding removal |
| Ungoogled-Chromium–style patch set | Privacy-hardening patch set, packaging scripts for many platforms | Same build cost; patch maintenance |
| Firefox / Gecko | Firefox add-ons native, MPL-2.0 | Build cost (smaller than Chromium but large), Chrome-extension compatibility gap |
| Prebuilt-engine approaches (e.g. CEF / prebuilt Chromium binaries, system WebView) | Avoids compiling the engine | Extension support, update control, security patch latency |

## Method

1. Desk research: official build requirements (disk, RAM, time) per platform.
2. Measure GitHub-hosted runner limits that apply to this repository
   (job timeout, disk, RAM, concurrency, artifact/cache quotas). Use current
   GitHub documentation; do not assume.
3. Small, time-boxed CI experiments **only after owner approval**:
   e.g. fetch-and-configure of a candidate, or a component build with caching.
   Never clone huge trees inside this repository.
4. Evaluate extension-ecosystem feasibility per candidate (MV2/MV3, WebExtension APIs).
5. Evaluate licensing obligations (BSD-3 / MPL-2.0 / GPL components) and
   what they imply for the Brizo licence.
6. Evaluate update and signing paths that need no paid services (and list
   which ones would need owner-approved spending).

## Deliverable

`docs/ENGINE_FEASIBILITY.md` with measured evidence, a ranked recommendation,
explicit unknowns, and a proposed Phase 2 plan. The owner makes the final decision.
