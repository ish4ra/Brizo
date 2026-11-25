# Security Architecture and Release Sustainability

Verified 2026-11-25. Labels and IDs: [SOURCES.md](SOURCES.md).

## 1. Upstream security tracking

| Need | Plan (Gecko base) |
| --- | --- |
| Know when to ship | Watch Mozilla Security Advisories (MFSA) and Firefox release tags; a scheduled workflow opens an issue on each new release or advisory [A] |
| Emergency patches | Same-day rebase of the patch set onto the dot release, automated build, owner smoke test, publish |
| Channel choice | **Firefox Release** (4-week cadence) for parity with Firefox security fixes. ESR is the fallback if rebase cost is too high [A] |
| Patch-set discipline | Small, documented patches; anything security-relevant is never patched out |

The Chromium fallback has the same structure (Chrome Releases blog plus Chromium
tags). Its multi-day free builds (FREE_BUILD_FEASIBILITY) would delay fixes, which is a key reason it is not primary.

## 2. Protections that stay on

Process sandbox, site isolation (Fission), certificate validation and
CRLite/OCSP behaviour as upstream, HTTPS-Only available, Safe Browsing
(through a privacy-respecting provider or proxy decision, open item),
password storage in the OS keychain and NSS with an optional primary password, and
extension signature enforcement.

## 3. Updates and release integrity

| Item | Plan |
| --- | --- |
| Update mechanism | Mozilla's MAR-based updater with **Brizo's own signing key** (Gecko base) [A]; key kept offline or in GitHub encrypted secrets with environment protection |
| Release artifacts | GitHub Releases; SHA-256 checksums; **Sigstore/cosign keyless signatures** or GitHub artifact attestations (`actions/attest-build-provenance`), which are free for public repos [A] |
| SBOM | SPDX or CycloneDX generated in CI (e.g. `syft`) per release |
| Dependency pinning | Pinned upstream tarball hashes, pinned Actions by commit SHA, Dependabot for workflow actions |
| CI hardening | `permissions: contents: read` by default, no `pull_request_target` with untrusted code, protected `release` environment needing owner approval |
| Reproducibility | Record toolchain versions; aim for reproducible Linux builds first [A] |

## 4. Platform distribution limits without paid accounts

| Platform | Without paid membership | Consequence |
| --- | --- | --- |
| macOS | Apps can be ad-hoc signed but not Developer ID-signed or notarised [A]. Since macOS Sequoia, Control-click no longer overrides Gatekeeper for software not correctly signed or notarised (S3) [V]. Users must allow the app in System Settings › Privacy & Security | Test builds are fine for the owner; **public releases need the Apple Developer Program (USD 99/year)**. That is an owner decision, as ungoogled-chromium-macos funds it (UC2) |
| Windows | Unsigned or self-signed installers trigger SmartScreen "unrecognised app" warnings until reputation builds [A] | Acceptable for testing. Options for later: free code signing for OSS (e.g. SignPath Foundation) [A], or paid OV/EV certificates (owner decision) |
| Linux | No signing gate; publish GPG-signed tarballs, Flatpak or AppImage | No cost |

No paid service is activated by this plan.
