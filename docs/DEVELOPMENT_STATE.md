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
  - Run 1: https://github.com/ish4ra/Brizo/actions/runs/45580332174 (`e504837`). **FAILED:** source fetch and verify 26 s, configure 107 s OK; the runner received a shutdown signal (exit 143) **18 min into compile** (09:17 UTC). The always() steps were skipped, so no metrics survived. Suspected memory exhaustion (4 parallel jobs, 15.6 GiB, no swap); unconfirmed because the metrics were lost with the VM.
  - Run 2: https://github.com/ish4ra/Brizo/actions/runs/45584240076 (`fa61ecc`): same config plus a 16 GiB swapfile, with memory, disk and build progress streamed to the job log every 60 s (evidence survives a runner loss)
- [x] T2 Logo provenance check: rights NOT established (no metadata or authorship record; only a Google/Skia ICC profile). Name: a reported live BRIZO Class 9 registration by Delta Faucet Co. (unverified at USPTO). Decision: the public hero uses a distinct temporary motif
- [x] T3 Public hero = V2 layout and animation with a temporary distinct sloop motif (`e809bd7`); live GitHub render verified (4 theme × motion combos, 0 broken images)
- [x] T3b **Owner correction:** the sloop was rejected. The approved V2 hero with the exact provisional mark is published (D-015, narrow validator whitelist); a compact sun/moon `<details>` light/dark preview replaces the settings line (D-016); attribution policy set (D-017, CLAUDE.md §5a). PR [ish4ra/Brizo#4](https://github.com/ish4ra/Brizo/pull/4) merged → `main` **`e6cb200`**; live render verified; no build triggers touched
- [x] T4 PR #1 merged → `main` `eae736c`; PR #2 retargeted, `main` merged in (`66ffefd`), merged → `main` **`5d020fc`** (merge commits, history preserved, original branches kept)
- [ ] T5 Platform builds (incremental)
  - macOS arm64 run 1: https://github.com/ish4ra/Brizo/actions/runs/45581403273 (commit `49eaca1`, native `macos-latest`, Xcode 26.6 SDK; Firefox 161 needs SDK ≥ 26.5)
  - Windows x64: workflow prepared after Linux evidence; native `windows-latest`, VC_PATH/WINDOWSSDKDIR from the installed VS (no `vs` bootstrap)
- Draft PR for the experiment: [ish4ra/Brizo#3](https://github.com/ish4ra/Brizo/pull/3) (do not merge without owner approval)

**How builds are started:** edit `engine/gecko/triggers/<linux|macos|windows>.txt` on `claude/task-003-gecko-build` and push. Nothing else starts a build.
Never re-run a configuration that already succeeded; read the run's `*-metrics` artifact and step summary first.
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
