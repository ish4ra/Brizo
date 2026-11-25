# Chrome and Firefox Extension Compatibility

Verified 2026-11-25. Labels and source IDs: [SOURCES.md](SOURCES.md).

## 1. Key facts

- **Chrome Web Store is MV3-only.** "Aug 31st 2026: All remaining Manifest V2
  extensions removed from the Chrome Web Store" (quoted in UBO1). Edge's
  consumer MV2 transition runs Aug–end 2026 (UBO1). [V]
- **Chromium code still contains MV2 support** that downstreams re-enable
  with a 4-file patch (`extensions-manifestv2.patch`, UC1/HE1, Chromium
  158). Upstream can delete the underlying code at any time. [V]/[A]
- **Firefox supports MV2 and MV3**, including blocking `webRequest`.
  uBO's own README says "uBO works best on Firefox". [V] UBO1
- **`webextension-polyfill` is not a compatibility layer.** It wraps Chrome's
  callback `chrome.*` APIs in Promise-based `browser.*` and is a no-op on
  Firefox (WEP1). Namespace translation does **not** add missing APIs. [V]
- **Real API gaps exist** (MDN1): incompatible `proxy` APIs, incompatible
  sidebar models (`sidebar_action` vs `side_panel`/`sidePanel`), no
  `debugger` or `declarativeContent` in Firefox, differences in `webRequest`
  async blocking, `tabs.executeScript` URL resolution, notifications. [V]

## 2. Ecosystem differences that matter to Brizo

| Area | Chrome (Chromium) | Firefox (Gecko) | Consequence |
| --- | --- | --- | --- |
| Package | CRX3 (signed by store) | XPI (signed by Mozilla/AMO) | Each engine verifies its own format; cross-installing needs re-validation and **must not skip signature checks** |
| Namespace | `chrome.*` (Promises in MV3) | `browser.*` + `chrome.*` alias | Mostly solvable |
| Background | MV3 service worker only | Event pages (MV2/MV3); service workers [A] | Lifecycle differences break some extensions |
| Network | `declarativeNetRequest`; blocking `webRequest` only for policy-installed extensions [A] | `webRequest` blocking + DNR (MDN2) | Full uBO only on Gecko or MV2-patched Chromium |
| Proxy | `proxy.settings` + ProxyConfig | `proxy.onRequest` | Proxy/VPN extensions are engine-specific |
| Sidebar | `sidePanel` | `sidebarAction` | UI extensions need adapters |
| Native messaging | Manifest location and `allowed_origins` | `allowed_extensions`, different paths (MDN1) | Installer must register both formats |
| Store | Chrome Web Store: installation into third-party Chromium browsers is common practice; **terms not re-verified** [U] | AMO: XPIs are downloadable; signatures are Mozilla's | Store integration "where permitted" needs a legal read of each store's terms |

## 3. Realistic dual-ecosystem options

| Option | Effort | Notes |
| --- | --- | --- |
| A. Gecko base, Firefox add-ons native; Chrome extensions only via their Firefox editions | Low | Covers most of the test list below today |
| B. A on Gecko **plus** a CRX→WebExtension import tool for MV3 extensions without a Firefox edition, using API shims for `sidePanel` etc. | High | "Adaptable" class only; never universal |
| C. Chromium base, Chrome extensions native; Firefox add-ons by re-packaging XPI as an unpacked extension | High | Firefox-only APIs (`proxy.onRequest`, `sidebarAction`, blocking webRequest in MV3) missing; Mozilla signature not verifiable by Chromium |
| D. Own WebExtensions runtime on one engine (Orion model) | Very high | Kagi needed years and kept it experimental (S1) |

## 4. Test plan

Run each extension on the candidate builds (Phase 3+). Record install source,
version, manifest version, and pass/fail per scenario. Never sideload by
bypassing signatures. Use official store or GitHub release packages only.

| Extension | Ecosystems published | Expected on Gecko base | Expected on Chromium base | Key scenarios |
| --- | --- | --- | --- | --- |
| uBlock Origin | Firefox (MV2); Chromium MV2 via GitHub only (UBO1) | **Native** (full) | Native only with MV2 patch; otherwise **policy-restricted** (CWS removal) | EasyList blocking, cosmetic, scriptlets, logger, element picker, dynamic filtering |
| uBlock Origin Lite | Chrome, Edge, Firefox (UBOL1) | Native [A] | Native | Default rulesets, per-site modes |
| Bitwarden | Chrome, Firefox [A] | Native | Native | Unlock, autofill, native messaging (biometrics), passkeys |
| Dark Reader | Chrome, Firefox [A] | Native | Native | Dynamic theme on 20 sites; site list; performance |
| Violentmonkey | Chrome, Firefox [A] | Native | Native (MV3 userScripts API) [A] | Install script, GM_* APIs, `@run-at document-start` |
| Tampermonkey | Chrome, Firefox [A] | Native | Native | Same as above, sync |
| SponsorBlock | Chrome, Firefox [A] | Native | Native | Segment skip on YouTube, submission |
| Return YouTube Dislike | Chrome, Firefox [A] | Native | Native | Counts shown, API calls |
| Enhancer for YouTube | Chrome; Firefox edition **[U]** | Adaptable or unsupported | Native | Player controls, volume wheel |
| SingleFile | Chrome, Firefox [A] | Native | Native | Save page, downloads API |
| Video DownloadHelper | Chrome, Firefox + native companion app [A] | Native | Native | Detection, companion native messaging |
| Proxy/VPN extension (e.g. FoxyProxy) | Both, engine-specific code [A] | Native (Firefox edition) | Native (Chrome edition) | `proxy` API behaviour (MDN1) |
| Side-panel extension (Chrome-only) | Chrome | **Substantial work** (`sidePanel` shim) | Native | Panel opens, persists |
| DevTools / `debugger` extension | Chrome | **Unsupported** (no `debugger` API, MDN1) | Native | Attach to tab |

Classification key: **Native** · **Adaptable** (small shim) · **Substantial
work** · **Unsupported** · **Policy-restricted** (blocked by store or vendor
policy, not by technology). "[A]" rows must be confirmed against the live
store listings in Phase 3. Store availability was not verified in this sandbox.

## 5. Conclusion

No base gives both ecosystems natively. A **Gecko base** gives full Firefox
compatibility, full-strength uBO, and the Firefox editions of nearly every
listed popular extension. True **CRX support is a separate, later research
project** and must never be marketed as universal.
