# Research Sources (Task 002)

All sources were read on **2026-11-25** unless stated otherwise. Most were read
from their canonical GitHub repositories via `raw.githubusercontent.com`,
because the research sandbox could not reach most documentation websites
directly. Citations in the research docs use the IDs below.

Evidence labels used throughout:
**[V]** verified in a primary source · **[M]** measured by us ·
**[S]** secondary source (news, blog) · **[A]** untested assumption or estimate ·
**[U]** unresolved (could not be checked).

## GitHub Actions (github/docs, branch `main`)

| ID | Source | Used for |
| --- | --- | --- |
| GH1 | `data/reusables/actions/supported-github-runners.md` | Runner specs: public repos x64/arm64 Linux & Windows 4 vCPU / 16 GB / 14 GB SSD; macOS arm64 3 CPU (M1) / 7 GB / 14 GB; macOS Intel 4 / 14 GB / 14 GB; "free and unlimited on public repositories" |
| GH2 | `content/actions/reference/limits.md` | 6 h job execution limit; 35-day workflow run; 256 matrix jobs; Free plan 20 concurrent jobs / 5 macOS |
| GH3 | `content/actions/reference/workflows-and-actions/dependency-caching.md` | Cache 10 GB per repo by default, 7-day eviction; usage beyond 10 GB is billed |
| GH4 | `content/billing/concepts/product-billing/github-actions.md` | Standard hosted runners free in public repositories; metering described for private repos |
| GH5 | `content/get-started/writing-on-github/…/basic-writing-and-formatting-syntax.md` | "The `<picture>` HTML element is supported." |
| GH6 | `data/reusables/actions/macos-runner-limitations.md` | arm64 macOS: no nested virtualisation, no static UDID |

## Chromium family

| ID | Source | Used for |
| --- | --- | --- |
| CR1 | `chromium/chromium` `docs/linux/build_instructions.md` | ≥8 GB RAM (>16 GB highly recommended), ≥100 GB free disk, ~30 GB git cache, fetch "30 minutes … many hours" |
| CR2 | `docs/windows_build_instructions.md` | ≥100 GB on NTFS, Visual Studio 2026, Windows 11 SDK |
| CR3 | `docs/mac_build_instructions.md` | Xcode + macOS SDK required (macOS host) |
| CR4 | `docs/win_cross.md` | Windows targets can be cross-built from Linux/Mac, with limits (e.g. Crashpad cannot report crashes) |
| CR5 | chromiumdash Stable / Linux (via probe) | Chromium stable 158.0.8127.88; source tarball 3.95 GiB (lite 0.92 GiB) [M] |
| UC1 | `ungoogled-software/ungoogled-chromium` `chromium_version.txt`, `patches/series` | Tracks 158.0.8127.88; carries `core/ungoogled-chromium/extensions-manifestv2.patch` |
| UC2 | `ungoogled-software/ungoogled-chromium-macos` `README.md` | Sponsored (Depot) Actions runners "reduce build times from days to hours"; notarised with a paid Apple Developer ID |
| HE1 | `imputnet/helium` `README.md`, `patches/series`, `patches/ungoogled-chromium/extensions-manifestv2.patch` | Helium: ungoogled-chromium based, GPL-3.0 own code, bundled uBlock Origin fork; MV2 patch edits 4 files incl. `extensions/browser/manifest_v2_handler.cc` |
| HE2 | `imputnet/helium-macos`, `helium-linux` READMEs | Sponsored runners: "within hours, not days" |
| BR1 | `brave/brave-core` `LICENSE`, `package.json` | MPL-2.0; brave-core 1.102.37 |
| BR2 | `brave/adblock-rust` `Cargo.toml`, `README.md` | adblock-rust 0.13.6, MPL-2.0; network + cosmetic filtering, uBO syntax extensions, uBO-compatible scriptlet/redirect resources, Apple content-blocking export |
| CEF1 | `chromiumembedded/cef` `README.md` (Bitbucket/GitHub mirror) | BSD-licensed, tracks Chromium branches |
| QT1 | `qt/qtwebengine` `dev` `src/core/api/qwebengineextensionmanager.h` | `QWebEngineExtensionManager` with load/install/unload/uninstall extension APIs exists on the dev branch |
| EL1 | `electron/electron` `docs/api/extensions.md` | "Electron supports a subset of the Chrome Extensions API"; does not support arbitrary Chrome extensions |

## Gecko family

| ID | Source | Used for |
| --- | --- | --- |
| FF1 | `mozilla-firefox/firefox` `browser/config/version.txt` (main) | Nightly 163.0a1 |
| FF2 | product-details (via probe) | Firefox release 161.0; source tarball 0.77 GiB [M] |
| ZEN1 | `zen-browser/desktop` `dev` `README.md`, `surfer.json`, `.github/workflows/*.yml` | MPL-2.0; based on Firefox 161.0; Linux, Windows **and macOS** release builds compile on Linux runners (`blacksmith-8/16vcpu-ubuntu-2404`, a third-party provider); PGO profiling on GitHub `macos-26`, `macos-15-intel`, `windows-latest`; sccache via GitHub cache; `free-disk-space` action |
| FL1 | `Floorp-Projects/Floorp` `README.md` | MPL-2.0, Firefox-based, x86_64 + ARM64 |
| WF1 | `WaterfoxCo/Waterfox` `README.md` | Uses the Mozilla `mach` build system |

## Extensions & content blocking

| ID | Source | Used for |
| --- | --- | --- |
| UBO1 | `gorhill/uBlock` `README.md`, `LICENSE.txt` | GPL-3.0; quotes Chrome "Aug 31st 2026: All remaining Manifest V2 extensions removed from the Chrome Web Store"; Edge MV2 consumer transition Aug–end 2026; uBO for Chromium MV2 available from GitHub releases (manual install, no auto-update) |
| UBOL1 | `uBlockOrigin/uBOL-home` `README.md` | uBO Lite: MV3, fully declarative, default lists (uBO, EasyList, EasyPrivacy, Peter Lowe) |
| MDN1 | `mdn/content` `…/webextensions/chrome_incompatibilities/index.md` | Concrete Chrome vs Firefox API differences (proxy, sidebar, webRequest, debugger, declarativeContent…) |
| MDN2 | `mdn/content` `…/api/declarativenetrequest/index.md` | Firefox DNR documentation |
| WEP1 | `mozilla/webextension-polyfill` `README.md` | Promise-based `browser.*` wrapper for Chrome; a no-op on Firefox; not an API-compatibility layer |
| EL2 | `easylist/easylist` `README.md` | Licence defined at easylist.to/pages/licence.html. **[U]** not reachable from the sandbox |

## Media tools

| ID | Source | Used for |
| --- | --- | --- |
| YT1 | `yt-dlp/yt-dlp` `LICENSE`, `README.md` | Source is Unlicense; PyInstaller executables include GPLv3+ code, so the combined binary is GPLv3+ |
| FFM1 | `FFmpeg/FFmpeg` `LICENSE.md` | LGPL-2.1+ by default; `--enable-gpl` makes it GPL-2.0+; some filters GPL-3.0 |
| AR1 | `aria2/aria2` `COPYING`, `README.rst` | GPL-2.0; TLS via OS, GnuTLS or OpenSSL |

## Secondary sources [S]

| ID | Source | Used for |
| --- | --- | --- |
| S1 | [Kagi blog: Orion 1.0](https://blog.kagi.com/orion), [Kagi Orion FAQ](https://browser.kagi.com/faq.html) | WebKit base; Web Extensions API ported to WebKit to run Chrome and Firefox extensions (experimental) |
| S2 | [AlternativeTo, Oct 2026](https://alternativeto.net/news/2026/10/kagi-ends-development-of-orion-for-linux-and-windows-open-sources-code-to-community/), [Digital Trends](https://digitaltrends.com/computing/kagi-is-pulling-orion-from-windows-and-linux-leaving-its-cross-browser-extension-dream-behind/) | Kagi ended Orion for Linux/Windows and reportedly open-sourced that code **[U]**, licence not checked |
| S3 | [Apple developer news: runtime protection in macOS Sequoia](https://developer.apple.com/news/?id=saqachfa) | Control-click no longer overrides Gatekeeper for software that is not correctly signed or notarised |
| S4 | [GitHub Blog: images for dark/light mode](https://github.blog/developer-skills/github/how-to-make-your-images-in-markdown-on-github-adjust-for-dark-mode-and-light-mode/) | `<picture>` + `prefers-color-scheme` pattern |
