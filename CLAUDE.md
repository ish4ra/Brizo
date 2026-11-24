# CLAUDE.md — Rules for AI coding sessions on Brizo

Brizo is an early-stage, free and open-source desktop web browser project.
Current phase: **Early Development — Architecture & Foundation.** There is no
browser implementation yet. Read this file fully before doing anything.

## 1. Start of every session (mandatory)

1. `git fetch --all --prune` and inspect the latest state. **Never assume
   `main` contains the latest work** — development happens on branches.
2. Review open pull requests and recently updated branches.
3. Read `docs/DEVELOPMENT_STATE.md`. It records the active task, completed and
   pending subtasks, blockers, the last verified commit, and exact continuation
   steps. It is the source of truth — not chat history.
4. Read `docs/DECISIONS.md` before changing direction on anything recorded there.

## 2. Working rules

- Preserve existing features and working behaviour. Avoid unnecessary rewrites.
- Never delete important files, assets, design iterations or previous working
  implementations without explicit owner approval.
- Maintain backward compatibility where applicable.
- Use secure coding practices. **Never disable essential security protections**
  (sandboxing, site isolation, certificate validation, update signature checks,
  etc.) to simplify development or to save memory.
- Never commit secrets, tokens, credentials or `.env` files.
- Keep dependencies minimal, pinned and properly licensed. Record new
  third-party components and their licences in `docs/DECISIONS.md`.

## 3. Honesty rules

- **Never fabricate** test results, benchmarks, download counts, stars,
  compatibility claims or release links.
- Never describe a planned or incomplete feature as implemented or complete.
- Never present a platform as supported until a working build has been
  produced *and tested*.
- Keep documentation synchronised with the actual implementation. If code and
  docs disagree, fix the docs in the same change.
- Report blockers transparently in `docs/DEVELOPMENT_STATE.md` and in your
  final report.

## 4. Branding rules

- Follow `docs/BRAND_GUIDELINES.md`. The primary palette is fixed:
  `#6FBCEB` (rear sail), `#1684D1` (front sail), `#174EA4` (hull).
- **Do not redesign the approved logo** (minimalist three-shape sailboat) or
  add elements to it without owner permission.
- Logo provenance and trademark status are **unresolved**
  (`docs/BRAND_PROVENANCE.md`). While unresolved and the repository is public:
  - do **not** commit the logo master, logo-derived exports, or the owner's
    reference image; they live in the git-ignored `branding-private/` folder
    and in the owner's private review page;
  - README / public visuals must use source-independent artwork only
    (waves, wind, typography).
- Use only properly licensed fonts (currently Inter, SIL OFL 1.1). Never use
  proprietary assets from Chrome, Firefox, Brave, Safari or other browsers.

## 5. Git & review workflow

- Workflow: Claude Code Cloud → development branch → pull request →
  GitHub Actions → downloadable test builds → owner testing → stable release.
- Never commit directly to `main`. Never force-push or rewrite shared history.
- Use coherent, descriptive commits. Commit and **push meaningful checkpoints
  incrementally** — do not wait until a task is finished.
- **Do not merge pull requests** and **do not publish releases** without
  explicit owner approval.

## 6. Cost rules

- No paid infrastructure, paid CI, subscriptions or paid developer programs
  without explicit owner approval. Prefer free GitHub-hosted runners.
- Never activate or purchase any service on the owner's behalf.

## 7. Checkpoint protocol (interruption recovery)

Usage limits can end a session at any moment. Therefore:

1. Update `docs/DEVELOPMENT_STATE.md` *before* starting a subtask and *after*
   finishing it (active task, done/pending lists, decisions, blockers, branch,
   last pushed commit, continuation steps).
2. Commit and push after every meaningful unit of progress.
3. Prefer small, self-contained commits that leave the branch in a working state.
4. Anything not pushed is at risk; anything only in chat is lost.

## 8. Repository map

| Path | Purpose |
| --- | --- |
| `README.md` | Public project presentation |
| `docs/` | Vision, requirements, roadmap, decisions, state, research plan, branding |
| `assets/readme/` | Source-independent README artwork (generated; do not hand-edit) |
| `scripts/brand/` | Reproducible asset generation & validation (Node ≥ 20) |
| `branding-private/` | **Git-ignored.** Private logo master + exports |
| `.github/workflows/` | Lightweight validation CI only (no browser builds yet) |

Common commands:

```bash
cd scripts/brand && npm ci
npm run build:readme   # regenerate assets/readme/*
npm run build:brand    # regenerate branding-private/exports (needs private master)
npm run validate       # SVG/PNG/link/palette checks
```

## 9. Scope guard

Do not start browser-engine work, clone large upstream trees, or pick an engine
until the owner approves the engine feasibility study
(`docs/TECHNICAL_RESEARCH_PLAN.md`).
