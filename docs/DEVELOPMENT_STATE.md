# Development State

> Single source of truth for resuming work. Update it at every checkpoint.
> Do not rely on chat history: this file plus `git log` must be enough.
> The **Active state** section is current. Everything under **History** is a
> record of earlier checkpoints and must not be treated as current instructions.

_Last updated: 2026-11-25 ~10:50 UTC · Task 003 in progress (builds running)_

## Active state

### Task
**Task 003: first real Gecko build experiment** (plus README hero work, now complete).
Owner approved testing Gecko. That is **not** approval of Gecko as the permanent
architecture, and **not** approval to merge PR #3. Free infrastructure only.

### Repository
| Item | State |
| --- | --- |
| `main` | Foundation (PR #1), research (PR #2), V2 hero (PR #4) and preview-link correction (PR #5) all merged. Check `git log origin/main` for the head |
| Experiment branch | `claude/task-003-gecko-build`, draft PR [ish4ra/Brizo#3](https://github.com/ish4ra/Brizo/pull/3) (**do not merge without separate owner approval**) |
| Merged and finished branches (kept, do not delete) | `claude/great-gates-umqsa8` (PR #1), `claude/task-002-engine-feasibility` (PR #2), `claude/task-003-hero-correction` (PR #4), `claude/task-003-preview-links` (PR #5) |

### Build experiment status (Firefox 161.0, tag `FIREFOX_161_0_RELEASE`)
| Platform | Run | Status at last check (10:46 UTC) | Notes |
| --- | --- | --- | --- |
| Linux x64 attempt 1 | [45580332174](https://github.com/ish4ra/Brizo/actions/runs/45580332174) | **Failed** | Source verified (26 s), configure OK (107 s). The runner got a shutdown signal (exit 143) 18 min into compile, and the `always()` steps were skipped, so **no metrics survived**. Memory exhaustion is **suspected, not proven** |
| Linux x64 attempt 2 | [45584240076](https://github.com/ish4ra/Brizo/actions/runs/45584240076) | **Compiling** since 09:23 UTC | Adds a 16 GiB swapfile; memory, disk and build progress are streamed to the job log every 60 s |
| macOS arm64 | [45581403273](https://github.com/ish4ra/Brizo/actions/runs/45581403273) | **Compiling** since 09:08 UTC | Native `macos-latest` (3 CPU / 7 GiB); configure succeeded with Xcode 26.6 SDK (Firefox 161 needs ≥ 26.5) |
| Windows x64 | not started | Waiting for the Linux attempt 2 result | Workflow `gecko-build-windows.yml` ready (native `windows-latest`, MozillaBuild, runner's VS/SDK via `VC_PATH`/`WINDOWSSDKDIR`) |

**Do not** start another Linux or macOS build while these runs are active. **Do not** rerun a
configuration that already succeeded. Builds start **only** by editing
`engine/gecko/triggers/<linux|macos|windows>.txt` on the experiment branch.

### Continuation steps (exact)
1. `git fetch origin && git checkout claude/task-003-gecko-build && git pull`.
2. Check runs 45584240076 and 45581403273 once (GitHub UI, or
   `curl -s https://api.github.com/repos/ish4ra/Brizo/actions/runs/<id>/jobs`).
3. For each finished run: download the `gecko-*-metrics` artifact (timings, resource CSV, smoke
   results, `results.json`) and, if present, the `brizo-gecko-experiment-*` package artifact. Record
   compile time, peak RAM, swap and disk, package size, SHA-256 and smoke results in
   `docs/research/GECKO_BUILD_EXPERIMENT.md` (create it), and in the table above.
4. If Linux attempt 2 failed: read the streamed `[res …]` lines in its job log and diagnose
   before any change. Do not retry the identical configuration.
5. After Linux is evaluated, start Windows: append a line to `engine/gecko/triggers/windows.txt`, then push.
6. Then: security-update sustainability assessment and the GO / CONDITIONAL GO / NO-GO verdict
   (`docs/research/ARCHITECTURE_DECISION_PROPOSAL.md` conditions C1–C4).
7. Commit as the owner identity per CLAUDE.md §5a. Do not merge PR #3.

### Branding (current, supersedes older notes below)
- Public README hero = owner-selected **provisional V2 sailing hero** (D-015). Only
  `assets/readme/hero-{light,dark}.svg` and their static PNGs may contain the mark;
  `validate.mjs` whitelists exactly those files. Everything else (master, exports, icons,
  reference) stays private in git-ignored `branding-private/`.
- Provenance and trademark are **unresolved** (BRAND_PROVENANCE, D-014). Nothing is cleared.
- Appearance previews (D-018): two 14 px icon links under the hero (sun → light SVG,
  moon → dark SVG on raw.githubusercontent.com). Exactly one hero banner is shown on the page.
- Private review pages: v1 brand https://claude.ai/artifact/DV8wzGrqYP72w57aH4X7Yr ·
  hero https://claude.ai/artifact/YKYxLma6FJ5WpT6x1ucn75. Packages `brizo-brand-review-v1.zip`,
  `brizo-hero-review-v2.zip`, `brizo-hero-review-v3-public-motif.zip` were delivered in the Claude
  conversations; the owner keeps copies. To rebuild, restore `source/brizo-mark.svg` into
  `branding-private/source/`.

### Open blockers
1. Gecko build feasibility not yet proven (runs in progress).
2. Logo provenance unknown; "BRIZO" Class 9 registration reported (unverified at USPTO).
3. Licence not chosen (MPL-2.0 recommended, D-005).
4. Sandbox limits: GitHub CSS/JS, the Mermaid viewer and docs.github.com are not reachable from Claude's sandbox.

### Owner decisions pending
Approve or reject merging PR #3 · trademark and provenance actions · licence · whether
Gecko becomes the permanent foundation (after build evidence) · whether to rewrite
history to remove the historical Claude contributor entry (not recommended, needs explicit approval).

## History (archived checkpoints — not current instructions)

### Task 003 timeline
- Started from PR #1 `9f6c21f`, PR #2 `e9e29db`, `main` `b68262a`.
- PR #1 merged → `main` `eae736c`. PR #2 retargeted, `main` merged in (`66ffefd`), merged → `5d020fc`.
- Bounded provenance check: no metadata or authorship record (ICC "Google Inc. 2016" only).
  Reported BRIZO Class 9 registration by Delta Faucet Co. (aggregator sources).
- Temporary sloop motif published (`e809bd7`, D-013), then **rejected by the owner**. Superseded by D-015.
- V2 hero published with a `<details>` light/dark preview (PR #4 → `e6cb200`, D-015/D-016). The
  `<details>` showed three banners when expanded, was **rejected by the owner**, and was
  replaced by the icon links (PR #5, D-018).
- Attribution policy D-017 (CLAUDE.md §5a). Historical commits authored as
  `Claude <noreply@anthropic.com>` remain. They are not rewritten without owner approval.

### Task 002 (complete)
Feasibility research and runner probe merged via PR #2: `docs/research/`, `research/probe/`.
Verdict at that time: CONDITIONAL GO on Gecko, pending measured builds (this task).

### Task 001 (complete)
Foundation merged via PR #1: CLAUDE.md, docs, brand tooling `scripts/brand/`, validator and CI,
source-independent README artwork, private logo master and 100 private exports.
Original branch: `claude/great-gates-umqsa8`. Older rule "logo assets may never be public"
is now narrowed by D-015 (hero files only).
