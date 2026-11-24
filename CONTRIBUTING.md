# Contributing to Brizo

Thank you for your interest. Brizo is in **Phase 0 (Architecture & Foundation)**.
There is no browser code yet, so the most valuable contributions right now are:

- Feedback on the [vision](docs/PROJECT_VISION.md), [requirements](docs/FEATURE_REQUIREMENTS.md) and [roadmap](docs/ROADMAP.md).
- Evidence for the [engine feasibility study](docs/TECHNICAL_RESEARCH_PLAN.md):
  build requirements, CI limits, licensing.
- Documentation fixes.

## Before you start

1. Open an issue to discuss anything non-trivial.
2. Read [`CLAUDE.md`](CLAUDE.md). Its honesty, security and branding rules apply to human contributors too.
3. Check open pull requests and branches. `main` is not always the newest work.

## Pull requests

- Branch from the latest relevant branch. Never push to `main` directly.
- Keep changes focused and commits descriptive.
- Do not describe planned features as implemented, and do not add benchmarks
  or compatibility claims without reproducible evidence.
- Do not add proprietary assets (logos, icons, fonts) from other browsers or vendors.
- Do not add the Brizo logo to tracked files while its provenance is unresolved
  ([BRAND_PROVENANCE.md](docs/BRAND_PROVENANCE.md)).
- Generated assets in `assets/readme/` must come from `scripts/brand/`; run
  `npm run build:readme && npm run validate` in `scripts/brand/`.
- Pull requests are merged only with owner approval.

## Licence of contributions

The project licence has **not been chosen yet** (see [DECISIONS.md](docs/DECISIONS.md), D-005).
Until it is, please limit contributions to discussion and documentation, and
expect to be asked to confirm that your contribution may be released under the
licence eventually chosen.

## Security issues

Please do **not** open public issues for vulnerabilities. See [SECURITY.md](SECURITY.md).
