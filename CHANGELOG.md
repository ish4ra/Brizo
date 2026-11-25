# Changelog

All notable changes are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Brizo has no
releases yet, so there are no version numbers.

## [Unreleased]

### Added — Task 002 (part B): engine feasibility research
- `docs/research/`: engine comparison, free-build feasibility, extension
  compatibility and test plan, content blocking, Media Grabber, performance
  benchmark plan, security architecture, licence audit, architecture decision
  proposal (CONDITIONAL GO), and a dated source register.
- Bounded zero-cost runner probe workflow and measured results (`research/probe/`).

### Added — Task 002 (part A): hero refinement & appearance
- Sailing-logo hero mode in `build-readme-assets.mjs` and a private build script
  (`build-private-hero.mjs`); output stays in git-ignored `branding-private/`.
- Compact sun/moon appearance note under the README hero, linking to GitHub
  appearance settings (labelled as a link, not a switch).
- Reference website Sun/Moon theme toggle and behaviour test (`docs/website/`).

### Fixed
- README animations now honour reduced motion through `<picture>` sources that
  serve static PNGs (SVG-internal media queries were ignored inside `<img>`).

### Added — Task 001: project foundation
- Project documentation: vision, feature requirements, roadmap, decision log,
  technical research plan, development state tracker.
- `CLAUDE.md` with permanent development, honesty, branding and checkpoint rules.
- Brand guidelines with the fixed palette, theme tokens and measured contrast ratios.
- Brand provenance record documenting unresolved logo and trademark status.
- Reproducible asset tooling in `scripts/brand/` (SVG → PNG/ICO/ICNS/BMP).
- Animated, source-independent README artwork with light/dark variants and static fallbacks.
- Redesigned README presenting the project honestly as early development.
- Locally generated brand-style badges (no third-party badge service).
- Lightweight validation workflow for docs and assets.
