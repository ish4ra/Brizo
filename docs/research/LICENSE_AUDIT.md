# Licence Audit and Project Licence Recommendation

Verified 2026-11-25. Labels and IDs: [SOURCES.md](SOURCES.md). Not legal advice.

## 1. Upstream and component licences

| Component | Licence | Evidence | Obligation summary |
| --- | --- | --- | --- |
| Gecko / Firefox source | MPL-2.0 (+ third-party) | ZEN1, FL1 (forks state MPL-2.0) [V]; Mozilla tree [A] | File-level copyleft: modified MPL files stay MPL and their source must be published |
| Firefox **trademarks and branding** | Not open | [A] (Mozilla trademark policy) | Must build **unbranded** and remove "Firefox" names and logos (Zen, Floorp do: "not affiliated", FL1) |
| Chromium | BSD-3-Clause + many third-party | [A]; CEF1 BSD | Notices; third-party licence list |
| ungoogled-chromium patches | BSD-3-Clause | HE1 ("LICENSE.ungoogled_chromium") [V] | Notice |
| Helium own code | GPL-3.0 | HE1 [V] | Copyleft. Reusing Helium patches makes those parts GPL-3.0 |
| brave-core, adblock-rust | MPL-2.0 | BR1, BR2 [V] | File-level copyleft, compatible with MPL Brizo code |
| uBlock Origin / uBO Lite | GPL-3.0 | UBO1 [V] | Bundle unmodified as a separate add-on (aggregate) with source link |
| EasyList / EasyPrivacy | Defined on easylist.to | EL2 **[U]** | Verify before embedding lists in releases |
| FFmpeg | LGPL-2.1+ (default) / GPL-2.0+ (`--enable-gpl`) | FFM1 [V] | Ship an LGPL build as a separate binary plus source offer; avoid `--enable-nonfree` |
| yt-dlp | Unlicense source; GPLv3+ PyInstaller binaries | YT1 [V] | Optional separate helper with its licence text |
| aria2 | GPL-2.0 | AR1 [V] | Separate binary if used |
| Inter font | SIL OFL-1.1 | Task 001 [V] | Include licence |
| Codecs (H.264/HEVC/AAC) | Patent-encumbered | [A] | Use OS decoders / Cisco OpenH264 as Firefox does; do not ship own patented encoders |

## 2. Recommendation for Brizo's own code

**Recommend: MPL-2.0** (not applied; needs owner approval, per D-005).

- Same licence as the recommended Gecko base, so no friction when code moves
  between Brizo patches and upstream files.
- Compatible with BSD (Chromium fallback) and with adblock-rust and brave-core (MPL-2.0).
- MPL-2.0 is GPL-compatible via its Secondary License clause, so Brizo can
  ship alongside GPL components (uBO, FFmpeg GPL builds if ever needed) as separate works.
- File-level copyleft keeps improvements to Brizo's files open, without forcing
  a licence on unrelated components.

Alternatives: **GPL-3.0** if the project wants Helium-style strong copyleft or
reuses Helium patches; **BSD-3-Clause** only if a Chromium base with
maximum permissiveness is chosen.

## 3. Separate, unresolved brand questions

These are **independent of the engine choice**:
- The "Brizo" name has had no trademark search (BRAND_PROVENANCE).
- The logo reference provenance is unconfirmed; logo assets stay private.
