# Roadmap

> Phases after Phase 1 are **plans, not commitments**. Their order and scope
> may change after the engine feasibility study. No dates are promised.

| Phase | Name | Goal | Exit criteria | Status |
| --- | --- | --- | --- | --- |
| 0 | Foundation & branding | Docs, rules, brand system, README, continuity | Task 001 PR approved by owner | **In progress** |
| 1 | Engine feasibility | Choose a foundation (Chromium, Brave/brave-core, Firefox/Gecko, other) that can be built and maintained on free infrastructure | Written study plus at least one experimental CI build attempt, owner decision recorded | **Desk study + runner probe done** (CONDITIONAL GO); build experiment pending |
| 2 | Free CI build pipeline | Reproducible unbranded builds on GitHub-hosted runners for the first target | Downloadable test artifact for macOS Apple Silicon | Planned |
| 3 | Core browsing prototype | Branded browser: tabs, navigation, bookmarks, history, themes, updates design | Owner can browse daily-test sites on macOS arm64 | Planned |
| 4 | Privacy engine | Default network and cosmetic blocking, per-site controls | Passes a documented blocking test set | Planned |
| 5 | Extension ecosystem | Chrome extensions, then Firefox add-on research and compatibility layer | Published compatibility matrix of tested extensions | Planned |
| 6 | Media Grabber | Detection, queue, HLS/DASH (non-DRM), merge | Documented test matrix | Planned |
| 7 | Public beta | Windows x64 and Linux x64 builds, signed updates, security review | Owner approval for a public pre-release | Planned |

Platform order: macOS Apple Silicon → Windows x64 → Linux x64 → remaining targets.

## Key risks

- **Build cost.** Full Chromium builds can exceed free runner time, disk and
  RAM limits. Phase 1 must measure this; mitigations include prebuilt
  components, caching, sccache, split builds or a lighter foundation.
- **macOS distribution** without a paid Apple Developer membership means
  unsigned or ad-hoc signed test builds, so Gatekeeper prompts are expected.
- **Dual extension support** is technically hard on any single engine.
- **Brand rights** unresolved (see [BRAND_PROVENANCE.md](BRAND_PROVENANCE.md)).
