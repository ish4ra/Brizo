# Gecko Build Experiment: Measured Results (Task 003)

Firefox **161.0** (`FIREFOX_161_0_RELEASE`), unmodified and unbranded, on standard free
GitHub-hosted runners. Method and configuration: [`engine/gecko/README.md`](../../engine/gecko/README.md).
Only results backed by workflow evidence are recorded here. **Status: in progress.**

## Runs

| Platform | Run | Commit | Result |
| --- | --- | --- | --- |
| Linux x64, attempt 1 | [45580332174](https://github.com/ish4ra/Brizo/actions/runs/45580332174) | `e504837` | **Failed:** runner lost mid-compile (details below) |
| Linux x64, attempt 2 | [45584240076](https://github.com/ish4ra/Brizo/actions/runs/45584240076) | `fa61ecc` | In progress at 10:55 UTC (compiling since 09:23 UTC) |
| macOS arm64 | [45581403273](https://github.com/ish4ra/Brizo/actions/runs/45581403273) | `49eaca1` | In progress at 10:55 UTC (compiling since 09:08 UTC) |
| Windows x64 | not started | — | Waiting for the Linux attempt 2 result |

## Linux x64, attempt 1 (verified from the job log)

| Step | Result | Duration |
| --- | --- | --- |
| Free disk (remove unused preinstalled toolchains) | success | 137 s |
| Fetch source + GPG/SHA-256 verification + unpack | success | 26 s |
| Configure (bootstraps upstream toolchains) | success | 107 s (≈ 1 min 36 s of mach time) |
| Compile | **runner shutdown** after ≈ 18 min (09:17 UTC), exit 143 | — |
| Package, smoke test, metrics upload | skipped (the runner was lost) | — |

Log evidence: `##[error]The runner has received a shutdown signal.` No metrics were
uploaded, because the `always()` steps cannot run once the runner is gone.

**Cause: not established.** Memory exhaustion is suspected: 4 parallel compile jobs
(including rustc) on a 15.6 GiB VM with no swap. That is a hypothesis, not a measurement.
Attempt 2 adds a 16 GiB swapfile and streams memory, swap, disk and build progress to the
job log every 60 s, so evidence survives even if the runner is lost again.

## macOS arm64 (verified so far)

- Xcode 26.6 selected, and its macOS SDK passed via `--with-macos-sdk`.
- Source verified. Configure **succeeded** (09:04:48 → 09:08:46 UTC), which confirms that
  Firefox 161 accepts the runner's Apple SDK, with no repackaged SDK downloaded.

## Pending measurements (to fill from each run's `gecko-*-metrics` artifact)

Compile duration · peak memory and swap · peak disk · sccache stats · package size and
SHA-256 · smoke tests (launch, HTTPS, certificate rejection, tabs, sandbox evidence, settings
and add-ons UI) · artifact names and download links.

## Interpretation rules

A green *Compile* step alone does not prove a usable browser: the step is
`continue-on-error`, and packaging plus the runtime smoke test are what count. No
platform is "supported" until a package exists and runs.
