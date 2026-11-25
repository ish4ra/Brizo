# Decision Log

Format: ID · date · status (**Accepted** / **Proposed** / **Pending**) · decision · rationale.
Never delete entries. Supersede them with a new entry instead.

## D-001 · 2026-11-24 · Accepted: Project identity
Name **Brizo**, product name **Brizo Browser**. Working tagline
*Fast. Private. Lightweight. Open.* is **Proposed** (owner approval pending).
Trademark clearance not done (see D-004).

## D-002 · 2026-11-24 · Accepted: Brand palette
Primary: `#6FBCEB` rear sail, `#1684D1` front sail, `#174EA4` hull.
Supporting: `#F4F8FC`, `#0B1220`, `#D8E5F3`, `#FFFFFF`, `#0F172A`. Fixed by owner.
Extra neutrals and semantic colours in BRAND_GUIDELINES.md are **Proposed**.

## D-003 · 2026-11-24 · Accepted: Logo direction
Minimalist three-shape sailboat, Balanced variation, flat colours. The vector
candidate (master v1) is **provisional** pending D-004.

## D-004 · 2026-11-24 · Pending: Logo provenance & trademark
Reference image origin and "Brizo" trademark status unknown. Until resolved,
logo assets stay private (git-ignored `branding-private/` plus a private
review page) and public visuals are source-independent.

## D-005 · 2026-11-24 · Pending: Project licence
Free and open source, but **no licence is chosen yet**. It will be selected after the
engine decision so that it is compatible with upstream obligations
(Chromium BSD-3-Clause and mixed licences; Brave/Firefox MPL-2.0; GPL components
such as FFmpeg builds or aria2 if used). Until then no `LICENSE` file exists.

## D-006 · 2026-11-24 · Accepted: Asset tooling
Node ≥ 20 scripts in `scripts/brand/` with pinned dependencies:
`@resvg/resvg-js` 2.6.2 (MPL-2.0, rendering), `opentype.js` 1.3.4 (MIT,
text outlining), `@fontsource/inter` 5.2.8 (OFL-1.1 font). ICO/ICNS/BMP
encoders are written in-house to avoid native tools. Rationale: reproducible
on any free CI runner, no system packages.

## D-007 · 2026-11-24 · Accepted: README animation approach
CSS-animated SVGs with outlined text, light/dark variants via `<picture>`,
`prefers-reduced-motion` support, static PNG fallbacks. GitHub does not execute
JavaScript in READMEs or in SVGs loaded via `<img>`.

## D-008 · 2026-11-24 · Accepted: Workflow & cost
Claude Code Cloud → branch → PR → GitHub Actions (free runners) → test builds →
owner testing → release. No paid services without explicit owner approval.
No merges or releases without owner approval.

## D-009 · 2026-11-24 · Pending: Browser foundation
Not selected. See TECHNICAL_RESEARCH_PLAN.md (Phase 1).

**Update 2026-11-25 (Proposed, awaiting owner):** Task 002 research recommends a
**CONDITIONAL GO** on a Gecko (Firefox Release) downstream patch set, conditional on
measured free-runner builds (conditions C1–C4). Fallbacks: a Chromium patch set
(needs donated/paid compute), and a CEF prototype shell. See
`docs/research/ARCHITECTURE_DECISION_PROPOSAL.md`. D-005 licence recommendation:
MPL-2.0 (not applied).

## D-010 · 2026-11-25 · Accepted: Sailing-logo hero stays private until rights are cleared
The animated hero with the exact sailboat mark (boat left, type block moved
right, surge/bob/rock motion, parallax waves, wake) is built by
`scripts/brand/build-private-hero.mjs` from the private master into the
git-ignored `branding-private/hero-v2/`. The public README keeps the
source-independent Task 001 hero. When the owner confirms usage rights, the
switch is one reviewed change (pass the boat renderer to `hero()`), and the
leak check in `validate.mjs` is updated deliberately, never bypassed.
No "distinct" substitute boat was published, so no second boat identity exists.

## D-011 · 2026-11-25 · Accepted: Reduced motion via `<picture>` sources
Measured in Chromium: `@media (prefers-reduced-motion)` inside an SVG loaded by
`<img>` did not stop its CSS animation (inline SVG did). Every animated README
`<picture>` therefore lists reduced-motion `<source>`s that serve the static
PNG fallbacks. `validate.mjs` enforces this. The artwork is unchanged.

## D-012 · 2026-11-25 · Accepted: README appearance control = settings link, not a switch
READMEs cannot run JavaScript or change the viewer's GitHub theme. The hero has
a compact sun/moon note with an accurately labelled link to
`https://github.com/settings/appearance`. A real Sun/Moon toggle is specified
for the future website (`docs/website/`), but is not deployed.
