# Gecko build experiment (Task 003)

**Experimental feasibility builds only.** This directory builds **unmodified,
unbranded Firefox** from official source on free GitHub-hosted runners, to
measure whether Brizo can build and maintain a Gecko-based browser at zero cost.
It is not the Brizo browser and not a release. Measured results are in
[`docs/research/GECKO_BUILD_EXPERIMENT.md`](../../docs/research/GECKO_BUILD_EXPERIMENT.md).

## Upstream pin

| Item | Value |
| --- | --- |
| Product | Firefox (Release channel) |
| Version | **161.0** |
| Upstream tag | `FIREFOX_161_0_RELEASE` (github.com/mozilla-firefox/firefox) |
| Why | Newest *tagged* release on 2026-11-25. `release` already carries 161.0.1, but that was not yet tagged as released. Release is security-supported until the next dot or major release |
| Next step | Bump `FIREFOX_VERSION` in the three workflows for each new release (see "Maintenance") |

## Source acquisition (no upstream code is committed here)

`fetch-source.sh` downloads `firefox-<v>.source.tar.xz` from
`archive.mozilla.org` and verifies it in a chain:
1. import `KEY` (Mozilla's release signing key published next to the release),
2. `gpg --verify SHA256SUMS.asc SHA256SUMS`,
3. compare the tarball's SHA-256 with its `SHA256SUMS` line.

It fails closed on any mismatch. The tarball (0.77 GiB) is unpacked inside the
runner only. Only Brizo's scripts, mozconfigs and workflows are in git.

> Hardening backlog: pin Mozilla's signing-key fingerprint in the repository
> instead of trusting the `KEY` file fetched alongside the release.

## Toolchains

`--enable-bootstrap` lets Firefox's own configure download the **exact
toolchains upstream CI uses** (clang, Rust, cbindgen, nasm, node, Linux sysroot)
from Mozilla's artefact service, pinned by the source tree. Platform SDKs:

| Platform | SDK source | Why |
| --- | --- | --- |
| Linux x64 | Bootstrapped sysroot | Upstream default |
| macOS arm64 | **Xcode 26.6 on the GitHub `macos-latest` runner** (Apple hardware), passed via `--with-macos-sdk` | Firefox 161 requires SDK ≥ 26.5. Without the flag, bootstrap would download a Mozilla-repackaged Apple SDK, which we avoid for licence reasons. `macos-15-intel` only has Xcode ≤ 26.3 |
| Windows x64 | **Visual Studio + Windows SDK installed on `windows-latest`**, via `VC_PATH` / `WINDOWSSDKDIR` | Without them, configure bootstraps Mozilla's repackaged `vs` bundle (`build/moz.configure/windows-toolchain.configure`) |

Windows additionally uses Mozilla's official **MozillaBuild** environment from
`ftp.mozilla.org` (its SHA-256 is recorded in the metrics artifact).

## Build configuration

`mozconfig.<platform>`: `--enable-application=browser`, `--enable-bootstrap`,
`--with-ccache=sccache`, `--disable-tests`. Everything else is upstream default
(optimised, non-debug). **No security feature is disabled.** The content
sandbox, site isolation (Fission), certificate validation and update signature
code are untouched. `--disable-tests` only skips test-only binaries.
Branding: no `--enable-official-branding`, so Mozilla's *unofficial* branding is
used, as required for third-party builds by Mozilla's trademark policy.

**Experimental vs production:** a production Brizo build would add Brizo
branding, PGO/LTO, a Brizo update channel and signing key, crash-report
handling, and Brizo patches. None of that is here.

## Runners (all standard, free for public repositories)

| Platform | Runner | Measured capacity (probe, Task 002) |
| --- | --- | --- |
| Linux x64 | `ubuntu-latest` | 4 vCPU, 15.6 GiB, ~116 GiB free after cleanup |
| macOS arm64 | `macos-latest` | 3 CPU (M1), 7 GiB, ~96 GiB free |
| Windows x64 | `windows-latest` | 4 vCPU, 16 GiB, D: ~220 GiB free |

Jobs are capped at 355 min (GitHub limit: 360). Compiles are capped at 290 min
so logs, metrics and partial sccache state are still saved after a timeout.

## Workflow layout (after attempt 2 / attempt 1 findings)

| Workflow | Shape |
| --- | --- |
| `gecko-build-linux.yml` | One job (cold compile measured at 1 h 45 m with a 16 GiB swapfile) |
| `gecko-build-macos.yml` → `gecko-stage-macos.yml` | Up to **3 chained jobs**. Each repeats verified source + configure, restores a local sccache dir from the previous stage (artifact), compiles for ≤ 285 min, then hands the cache on. The finishing stage packages, smoke-tests and uploads |
| `gecko-build-windows.yml` → `gecko-stage-windows.yml` | Same staged design on `windows-latest` with MozillaBuild |
| `gecko-preflight.yml` | No compile: artifact round-trip on 3 OSes, 2 GiB handoff timing, official-Firefox sandbox baseline, cache inventory |

Every job ends with `acceptance.py`. It records source, configure, compile, package, smoke,
security, metrics-upload and package-upload outcomes separately, and **fails the job**
unless all required stages and the security checks pass. Packages that fail the security
gate are uploaded only as `…-DIAGNOSTIC-security-unverified`. Uploaded paths are canonical
`RUNNER_TEMP` paths. Attempt 2 lost its artifacts to a `..` path.

## Cache strategy

Linux: sccache with the GitHub Actions cache backend (`SCCACHE_GHA_ENABLED`,
`mozilla-actions/sccache-action@v0.0.9`). Measured: 859 (Linux) and 461 (macOS) write
errors, with 6,601 entries totalling 4.03 GiB, so the errors are not a size-limit effect.
macOS/Windows: a **local-disk sccache dir handed between stages as an artifact**
(preflight: 2 GiB uploaded in 25 s and arrived intact). Objects are written during the
compile, so a timed-out run still warms the next one. Limits: 10 GB per
repository, entries evicted after 7 days unused (GitHub docs). All three
platforms share this budget, so expect eviction thrash. Measured sizes are in
the results doc.

## Reproducibility

- Pinned: upstream version and tarball hash (logged), toolchains (pinned by the
  upstream tree), Python 3.12, sccache action version, runner image (logged per run).
- Not yet bit-for-bit reproducible. Runner images change weekly and
  timestamps are embedded. Mozilla has reproducible-build work for Linux that
  Brizo could adopt later.

## Starting builds

Edit `triggers/<linux|macos|windows>.txt` on `claude/task-003-gecko-build` and
push. Nothing else starts a build. Check the previous run's metrics artifact
before re-running a configuration.

## Maintenance implications

- Every Firefox release (about 4-weekly) and dot release means: bump the version, run
  all platforms, smoke test. The workload is mostly CI time while Brizo has no patches.
- Once Brizo patches exist, each release also needs a rebase (Zen/LibreWolf model).
- Security releases need a fast cold or warm build. See the measured sustainability
  assessment in the results doc.

## Files

| File | Purpose |
| --- | --- |
| `fetch-source.sh` | Download and verify official source |
| `mozconfig.*` | Per-platform build configuration |
| `step.sh` | Time each step into `timings.csv` |
| `monitor.sh` / `monitor.py` | 15-second RAM/disk/load sampler (Linux / portable) |
| `smoke_test.py` | Headless WebDriver BiDi smoke test of the packaged build |
| `summarize.py`, `write_env.py` | Results JSON and job summary |
| `win-mach.sh` | Run mach inside MozillaBuild |
| `triggers/*.txt` | Per-platform build start switches |
