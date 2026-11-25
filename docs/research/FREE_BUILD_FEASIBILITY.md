# Free Cloud Build Feasibility

**Question:** can Brizo build, update and ship a full desktop browser using only
free GitHub-hosted runners, with no local toolchain and no paid service?

**Short answer:** **not demonstrated.** A Gecko-based build has a credible
free path that still has to be measured. A Chromium-based build on free runners
is possible only as a slow, multi-job chain ("days", per projects that did it),
which is too slow for browser security releases. Labels: see [SOURCES.md](SOURCES.md).

## 1. What free runners actually provide

| Fact | Value | Evidence |
| --- | --- | --- |
| Cost for public repos | Standard runners free and unlimited | GH1, GH4 [V] |
| Job time limit | **6 h per job** (35 days per workflow run) | GH2 [V] |
| Concurrency (Free plan) | 20 jobs, of which 5 macOS | GH2 [V] |
| Linux/Windows x64 & arm64 | 4 vCPU, 16 GB RAM | GH1 [V], probe [M] |
| macOS arm64 (`macos-latest`) | **3 CPU, 7 GB RAM** | GH1 [V], probe [M] |
| macOS Intel (`macos-15-intel`) | 4 CPU, 14 GB RAM | GH1 [V], probe [M] |
| Documented disk | 14 GB SSD | GH1 [V] |
| **Actual free disk** | Linux x64 87 → **116 GiB** after cleanup; Linux arm64 106 → 119; Windows D: 220; macOS arm64 96; macOS Intel 108 | probe [M] (undocumented, may change) |
| Cache | 10 GB / repo, entries evicted after 7 days unused; more is billed | GH3 [V] |
| Artifacts | Free for public repos (metering applies to private repos), retention ≤ 90 days | GH4 [V], retention [A] |
| Compiler caches | `sccache`/`ccache` not preinstalled except `ccache` on Windows; installable | probe [M] |

Full probe table: [`research/probe/RESULTS-2026-11-25.md`](../../research/probe/RESULTS-2026-11-25.md).

## 2. Upstream build demands

| | Chromium 158 | Firefox 161 |
| --- | --- | --- |
| Source archive | 3.95 GiB `.tar.xz` (lite 0.92) [M] | 0.77 GiB `.tar.xz` [M] |
| Disk (official guidance) | **≥ 100 GB** free (CR1, CR2) [V] | not re-verified [U]; forks build on standard Linux runners after `free-disk-space` (ZEN1) [V] |
| RAM | ≥ 8 GB, > 16 GB "highly recommended" (CR1) [V] | not re-verified [U] |
| Cross-compile to Windows from Linux | Supported with limits (Crashpad cannot report crashes) CR4 [V] | Yes, used in production by Zen (ZEN1) [V] |
| Cross-compile to macOS from Linux | **No.** Needs a macOS host and Xcode (CR3) [V] | **Yes.** Zen compiles macOS release builds on Linux runners (ZEN1) [V] |
| Who builds it in the open, and on what | ungoogled-chromium-macos and Helium say sponsored runners cut builds "from days to hours" (UC2, HE2) [V] | Zen: third-party 8–16 vCPU Linux runners for compile, free GitHub runners for PGO (ZEN1) [V] |

## 3. Per-platform verdict

| Platform (priority) | Chromium-based on free runners | Gecko-based on free runners |
| --- | --- | --- |
| 1. macOS Apple Silicon | **Not practical.** Must build on a macOS host; the free arm64 runner has 3 CPU / 7 GB, below Chromium's guidance, and 6 h per job. Would need many chained jobs that resume from a saved object directory. [A], consistent with UC2 "days" | **Plausible, unmeasured.** Cross-compile on 4 vCPU / 16 GB Linux with the macOS SDK, as Zen does on larger runners. Packaging, signing and smoke tests on `macos-latest`. [A] |
| 2. Windows x64 | **Theoretically possible but slow.** Chained jobs on `windows-latest` (D: 220 GiB) or a Linux cross build; total compile time unknown, likely several 6 h jobs. [A] | **Plausible, unmeasured.** Linux cross build (Zen pattern) or native `windows-latest`. [A] |
| 3. Linux x64 | **Possible with chaining**: disk fits after cleanup (116 GiB vs ≥100 GB guidance, tight); a 4-core full build is not expected to finish in one 6 h job. [A] | **Plausible, unmeasured.** Most likely to fit inside one 6 h job, especially with sccache warm. [A] |

Why multi-day Chromium chains are a problem even if they work: Chromium ships a
new milestone roughly every 4 weeks, with security updates in between. A
release pipeline measured in days delays security fixes to users. For a
browser, that is a security defect, not just an inconvenience.

## 4. Legitimate techniques to stay within free limits

| Technique | Applies to | Status |
| --- | --- | --- |
| Delete unused preinstalled toolchains in our own VM (as `free-disk-space` does) | All Linux | Measured: +29 GiB in 93 s [M] |
| Use Windows `D:` for the build tree | Windows | Measured: 220 GiB free [M] |
| `sccache` with the GitHub Actions cache backend | Both engines | Used by Zen (ZEN1) [V]; 10 GB cache cap may thrash for Chromium [A] |
| Patch-based downstream (patches + upstream tarball, no fork history) | Both | Used by ungoogled-chromium, Helium, Zen [V] |
| Chained jobs resuming from an artifact or cache of the object directory | Both | Used historically by Chromium forks [S/A]; fragile, slow |
| Disable expensive optimisation in test builds (no PGO/LTO for nightlies) | Both | Standard practice [A] |
| Reuse **official upstream binaries** | Shell/embedding architectures only (CEF builds, Qt) | Avoids engine compile entirely; extension limits apply (see ENGINE_COMPARISON) |
| Other free compute (e.g. donated or sponsored runners, open-source credits) | Both | Real precedent (UC2, HE2, ZEN1 sponsors) but **not guaranteed** and needs owner approval |

## 5. Required follow-up measurement (Phase 1b, needs owner approval)

The decisive number is unknown: **how long a Gecko build takes on a free
4 vCPU / 16 GB runner, and how much disk and RAM it needs at peak.** Proposed
bounded experiment (zero cost, public repo, about 2 runner-hours):

1. `ubuntu-latest`: fetch the Firefox 161.0 source tarball (0.77 GiB), run
   `free-disk-space`, set up sccache, and run an unbranded opt build of
   `browser/` with a 330-minute timeout. Record wall time, peak RAM and disk,
   and the sccache size.
2. Run it again with a warm sccache to measure the incremental and security-update path.
3. Only if (1) fits: try a Linux → macOS arm64 cross build, then a Linux →
   Windows cross build.

Success criterion: an unsigned, runnable Firefox-engine build for Linux x64
inside one 6 h job, then the same for macOS arm64 via cross-compile.

Nothing in this document claims a browser has been built. A green
documentation-validation workflow says nothing about compile capacity.
