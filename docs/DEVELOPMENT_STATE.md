# Development State

> Single source of truth for resuming work. Update it at every checkpoint.
> Do not rely on chat history: this file plus `git log` must be enough.

_Last updated: 2026-11-25 · Task 003 in progress_

## Active task

**Task 003: Foundation integration, README hero finalisation, first real Gecko build experiment.**
Started 2026-11-25 from: PR #1 head `9f6c21f`, PR #2 head `e9e29db`, `main` `b68262a` (both PRs CI-green, no reviews).
Owner approved: the V2 hero design, merging PR #1 then PR #2 after verification, and the Gecko build experiment
(not yet Gecko as the permanent architecture). No paid infrastructure.

Phases (update as you go):
- [ ] T1 Gecko Linux x64 experiment: branch `claude/task-003-gecko-build`, workflow `gecko-build-linux.yml`, Firefox **161.0** (`FIREFOX_161_0_RELEASE`)
- [ ] T2 Logo provenance check (bounded); decide the public hero (V2 exact logo, or a distinct temporary motif)
- [ ] T3 README hero update on PR #1 branch + live GitHub render check
- [ ] T4 Merge PR #1 → main (merge commit); retarget PR #2 → main; merge PR #2
- [ ] T5 Platform builds: macOS arm64, then Windows x64 (incremental, after Linux evidence)
- [ ] T6 Security-update sustainability assessment + architecture verdict

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

- **Private review page v1, brand assets** (owner's claude.ai account): https://claude.ai/artifact/DV8wzGrqYP72w57aH4X7Yr
- **Private review page v2, animated sailing hero**: https://claude.ai/artifact/YKYxLma6FJ5WpT6x1ucn75
- **Zip package v2** `brizo-hero-review-v2.zip` (hero SVGs, stills, GIFs, generation source), delivered in the Task 002 conversation. Rebuild with `node scripts/brand/build-private-hero.mjs --version v2`.
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

## Task 002 handover (2026-11-25)

| Branch | PR | Contents |
| --- | --- | --- |
| `claude/great-gates-umqsa8` | [ish4ra/Brizo#1](https://github.com/ish4ra/Brizo/pull/1) (draft) | Task 001 + 002A (private hero tooling, appearance note, reduced-motion fix, toggle reference). Head `9f6c21f` |
| `claude/task-002-engine-feasibility` | [ish4ra/Brizo#2](https://github.com/ish4ra/Brizo/pull/2) (draft, base = PR #1 branch) | Feasibility research, runner probe, ADR (CONDITIONAL GO, Gecko) |

Merge order if approved: PR #1 into `main`, then retarget PR #2 to `main`.

**Next task (needs owner approval): Task 003, the Gecko build experiment C1–C4**
(`docs/research/ARCHITECTURE_DECISION_PROPOSAL.md` §3). Start a new branch from
`claude/task-002-engine-feasibility` (or `main` after merges). Bounded CI only,
no product code. Check Apple SDK terms before C3.

Resume checklist: `git fetch origin`, then check out the research branch, then
`cd scripts/brand && npm ci && npm run build:readme && npm run validate` (must pass with no diff).
