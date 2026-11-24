# Development State

> Single source of truth for resuming work. Update it at every checkpoint.
> Do not rely on chat history: this file plus `git log` must be enough.

_Last updated: 2026-11-24 · end of Task 001_

## Active task

**Task 001: Project initialization, branding preparation, repository foundation & animated README.**
Status: **complete. Awaiting owner review** of the draft PR and the private brand review.
Do **not** start Task 002 (engine feasibility) until the owner approves.

## Branch & checkpoints

| | |
| --- | --- |
| Development branch | `claude/great-gates-umqsa8` (Claude Code session branch) |
| Base | `main` @ `b68262a` (Initial commit, untouched) |
| Pull request | Draft PR `claude/great-gates-umqsa8` → `main` (do not merge without owner approval) |
| Last CI-verified commit | `49944b4`, workflow *Validate* run #2 passed on `ubuntu-latest` |

Checkpoint history (oldest first): `62bdb36` state tracker → `b4576a8` CLAUDE.md + tooling →
`1784240` README artwork → `9de2317` README + docs → `d6ba44b` validator + CI →
`49944b4` local badges → final state update (this file).

## Completed subtasks

- [x] Repository inspected: public repo, 1 commit on `main`, no PRs, no workflows, README only
- [x] `.gitignore` (incl. private `branding-private/`), `CLAUDE.md` development rules
- [x] Logo master v1 vector candidate (private) + small-size variant
- [x] Asset tooling `scripts/brand/` (resvg, opentype.js, Inter OFL; in-house ICO/ICNS/BMP)
- [x] 100 private logo-derived exports: lockups, mono, PNG 16–1024, ICO, ICNS + iconset, Linux hicolor, favicons, toolbar, GitHub social/avatar, NSIS + DMG art
- [x] Source-independent animated README artwork (light/dark, reduced-motion, static PNGs, local badges)
- [x] README, CONTRIBUTING, SECURITY, CHANGELOG, docs set (vision, requirements, roadmap, decisions, research plan, brand guidelines, provenance)
- [x] `scripts/brand/validate.mjs` + `.github/workflows/validate.yml` (passing)
- [x] README rendered on github.com in headless Chromium (light + dark): `<picture>` switching works, all repo SVGs load, hero animation confirmed running
- [x] Private owner review page + zip package delivered in the Claude conversation

## Pending (owner)

See "Owner decisions needed" below. Nothing technical is pending for Task 001.

## Current technical decisions

See [DECISIONS.md](DECISIONS.md). D-001 to D-003 and D-006 to D-008 accepted; D-004 (provenance),
D-005 (licence) and D-009 (engine) pending.

## Unresolved blockers

1. **Logo provenance unknown** (D-004). Logo assets cannot go into the public repo or README.
2. **"Brizo" trademark not cleared.**
3. **Licence not chosen** (D-005, by design, until the engine is chosen).
4. Environment note: the Claude Code sandbox egress proxy blocks `img.shields.io`,
   `camo.githubusercontent.com` and GitHub's static CSS/Mermaid viewer, so README checks on
   github.com were partially unstyled. Mitigation: badges are local SVGs. The Mermaid
   diagram could not be visually confirmed from the sandbox; confirm in a normal browser.

## Where the private brand files are

The git-ignored `branding-private/` folder exists **only in the session container**, which is
ephemeral. Durable copies:

- **Private review page** (owner's claude.ai account): https://claude.ai/artifact/DV8wzGrqYP72w57aH4X7Yr
- **Zip package** `brizo-brand-review-v1.zip` (source + all exports), delivered in the Task 001
  Claude conversation. The owner should keep a copy.

To regenerate in a new session: place `brizo-mark.svg` and `brizo-mark-small.svg` from the zip's
`source/` into `branding-private/source/`, then `cd scripts/brand && npm ci && npm run build:brand`.

## Owner decisions needed

1. Approve / adjust logo master v1 and the small-size variant.
2. Confirm the reference image's origin and rights; decide on a trademark search.
3. Approve the tagline, the Inter wordmark and the proposed neutral/semantic colours.
4. Review and (optionally) mark the draft PR ready; merging is the owner's call.
5. Approve starting **Task 002: Engine feasibility study**.

## Continuation instructions

1. `git fetch origin && git checkout claude/great-gates-umqsa8 && git pull` (or `main` if the PR has merged).
2. Read `CLAUDE.md`, this file and `docs/DECISIONS.md`.
3. `cd scripts/brand && npm ci && npm run build:readme && npm run validate`. This must pass with no git diff.
4. Only after owner approval: begin Task 002 per `docs/TECHNICAL_RESEARCH_PLAN.md`, on a new branch,
   updating this file before and after each subtask.
