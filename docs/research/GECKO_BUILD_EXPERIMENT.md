# Gecko Build Experiment: Measured Results (Task 003)

Firefox **161.0** (`FIREFOX_161_0_RELEASE`), unmodified and unbranded, on standard free
GitHub-hosted runners. Method: [`engine/gecko/README.md`](../../engine/gecko/README.md).
Every number below comes from the cited job log (downloaded and checked on 2026-11-25).
A green step is never taken as proof: compile, package, runtime and security outcomes are
recorded separately.

## Summary

| Platform | Run | Source verify | Configure | Compile | Package | Runtime smoke | Security gate | Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Linux x64 #1 | [45580332174](https://github.com/ish4ra/Brizo/actions/runs/45580332174) | ✅ 26 s | ✅ 107 s | ❌ runner lost at ~18 min | — | — | — | none |
| Linux x64 #2 | [45584240076](https://github.com/ish4ra/Brizo/actions/runs/45584240076) (job 139101652546) | ✅ 34 s | ✅ 128 s | ✅ **6270 s** (1 h 44 m 30 s), exit 0 | ✅ 59 s | ✅ partial (below) | ❌ not passed | ❌ **none uploaded** (path bug) |
| macOS arm64 #1 | [45581403273](https://github.com/ish4ra/Brizo/actions/runs/45581403273) (job 139092070436) | ✅ 209 s | ✅ 236 s | ❌ **timed out**: 17,401 s, exit 142 (290 min alarm) | skipped | skipped | — | metrics only (`gecko-macos-arm64-metrics`, id 15029122780, 49,659 B) |
| Windows x64 | not started | | | | | | | |

GitHub showed macOS #1 as a green ✅ even though compilation failed: the Compile step used
`continue-on-error`. Linux #2 showed ❌ even though it compiled and packaged: only the artifact
upload failed. Both conclusions were misleading. The workflows are being fixed (see "Workflow corrections").

## Linux x64 attempt 1: runner lost

The runner received a shutdown signal (exit 143) about 18 min into compile. The `always()` steps
could not run, so no metrics survived. **Cause not proven.** Attempt 2 measured very high memory
use in the same phase of the build (next section), which is *consistent with* memory
exhaustion in a 15.6 GiB VM without swap.

## Linux x64 attempt 2: compiled and packaged; artifacts lost

| Metric | Value |
| --- | --- |
| Runner | `ubuntu-latest`, 4 vCPU, 15.61 GiB RAM, plus a 16 GiB swapfile |
| Compile | exit 0, **6270 s** |
| Peak RAM used | **15.06 GiB** (of 15.61) |
| Peak swap used | **11.2 GiB**. Sample at 09:52 UTC (min 27, `dom/ipc`): 15.4 GB RAM + 9.8 GB swap |
| Peak disk used / min free | 67.4 GiB / 76.9 GiB |
| sccache | 5,230 compiles; hit rate 26.10% (C/C++ 18.15%, Rust 69.30%); **859 cache write errors** |
| Package | `brizo-gecko-experiment-161.0-linux-x86_64.tar.xz`, **89,694,928 bytes** |
| SHA-256 | `e08f899c0364a6219b23df8b1966db2edcc1c264be6198e0ea28d6f4385a41ba` |
| Upload | ❌ `Invalid pattern '/home/runner/work/Brizo/Brizo/../metrics'. Relative pathing '.' and '..' is not allowed.` The metrics upload failed and the package upload was skipped. **The artifact API lists 0 artifacts.** The package existed only on the terminated VM and **cannot be recovered** |

Smoke test of the packaged build (headless, WebDriver BiDi):

| Check | Result |
| --- | --- |
| Launch | ✅ firefox 161.0 |
| HTTPS navigation | ✅ example.com over https |
| Invalid certificate rejected | ✅ `about:certerror … SEC_ERROR_EXPIRED_CERTIFICATE` |
| Open and close tabs | ✅ 1 → 2 → 1 contexts |
| Settings UI / Add-ons Manager present in the package | ✅ / ✅ (`omni.ja`) |
| Content sandbox (seccomp) | ❌ 9/10 "content" processes in seccomp filter mode |
| User-namespace isolation | ❌ 0/10 |
| Settings / Add-ons Manager at runtime | ⚠️ not verified: BiDi refuses `about:preferences` and `about:addons` |

The security findings are under investigation (see "Sandbox investigation"). They are **not**
waived.

## macOS arm64 attempt 1: timed out at ~55%

| Metric | Value |
| --- | --- |
| Runner | `macos-latest`, arm64, 3 CPU, 7.0 GiB |
| SDK | MacOSX26.5.sdk from Xcode 26.6 (accepted by configure) |
| Compile | **exit 142**: 290 min alarm after 17,401 s |
| Peak RAM / swap | 5.9 GiB / 2.1 GiB |
| Peak disk / min free | 11.8 GiB / 74.8 GiB |
| sccache | 2,885 compiles; hit rate 2.76%; **461 write errors** |
| Progress at timeout | compiling `js/src/debugger` (log). Linux #2 reached the same `js/src/builtin` point at minute 59 of 104.5 (≈ 56%). macOS also did 2,885 of the ≈ 5,230 compiles Linux needed (≈ 55%). **Estimated cold build ≈ 8.5 h**, which exceeds the 6 h job limit |

## Interpretation (so far)

- **Linux x64:** a free runner can compile and package Firefox in about 1 h 45 m, but only with
  swap: memory peaked at 15.1 GiB RAM + 11.2 GiB swap. That is feasible, but it has no margin.
- **macOS arm64:** a single free job cannot finish a cold build. A staged build is needed,
  with resumable compiler cache handed between jobs. See the workflow corrections.
- **Windows x64:** no data yet.
- No package is downloadable yet. No platform is "supported".

## Artifact upload failure (Linux #2): root cause and fix

Root cause: `actions/upload-artifact` rejects paths with `.`/`..` segments, and the workflow
uploaded `${{ github.workspace }}/../metrics`. The metrics upload failed and the package upload
never ran. **Fix:** every uploaded path is now a canonical `RUNNER_TEMP` path. **Preflight**
([45635212713](https://github.com/ish4ra/Brizo/actions/runs/45635212713),
[45635843712](https://github.com/ish4ra/Brizo/actions/runs/45635843712)): dummy metrics and
packages round-tripped with SHA-256 verification on `ubuntu-latest`, `windows-latest` and
`macos-latest`. A 2 GiB payload uploaded from macOS in **25 s** and downloaded intact.

## Sandbox investigation: resolved methodology flaws, no Firefox defect found

Baseline: **Mozilla's official Firefox 161.0 Linux build** (verified via KEY → signed SHA256SUMS
→ hash `3e9b1e51…25733`), preflight [45637174497](https://github.com/ish4ra/Brizo/actions/runs/45637174497):

| Evidence | Without AppArmor profile | With Ubuntu-style AppArmor userns profile |
| --- | --- | --- |
| Host | `kernel.apparmor_restrict_unprivileged_userns = 1` (Ubuntu default on the runner) | same |
| Firefox's own report (`Troubleshoot.snapshot().sandbox`) | level 6 configured / 6 effective, seccomp-BPF ✓, **`hasUserNamespaces: false`** | level 6/6, seccomp-BPF ✓, **`hasUserNamespaces: true`** |
| Web-content ("tab") processes in seccomp filter mode | **7/7** | **7/7** |
| Web-content processes in their own user namespace | blocked by environment | **7/7** |
| Other children | fork server seccomp 0 (unsandboxed by design: it forks content processes, which sandbox themselves); rdd 2; utility 2 | same |
| about:preferences / about:addons at runtime (Marionette chrome context) | ✅ "Settings" / ✅ "Add-ons Manager" | ✅ / ✅ |

Conclusions:
1. Attempt 2's "9/10 seccomp" counted the **fork server** as a content process. That was a
   classification flaw in the test, not a sandbox failure. The test now classifies processes by type.
2. Attempt 2's "0/10 user namespaces" was **environmental**: Ubuntu's AppArmor restriction
   blocks unprivileged user namespaces for binaries without a profile. Ubuntu's own Firefox package
   ships a profile granting `userns` for this reason. With an equivalent profile, the official
   build shows full namespace isolation. The build workflow now installs that profile before
   testing. **Nothing is disabled or relaxed. The profile enables Firefox's namespace layer.**
3. BiDi refuses privileged `about:` pages by design. They are now tested through Marionette's
   privileged context, with Mozilla's documented `MOZ_REMOTE_ALLOW_SYSTEM_ACCESS=1` opt-in
   for the test process only.
4. A user namespace reported as unavailable is recorded as **`blocked-by-environment`**, never as a pass.

## Cache findings

- Actions cache at preflight: **6,601 entries, 4.03 GiB** (limit 10 GiB). The 859 (Linux) and
  461 (macOS) sccache write errors are therefore **not** a size-limit effect. Throttling of many
  small cache writes is the likely cause [A].
- macOS/Windows now use a local-disk sccache directory handed between chained jobs as an
  artifact, which avoids the cache service entirely.

## Retries (one each, after preflight)

See the run table in `docs/DEVELOPMENT_STATE.md`. Results will be added here.
