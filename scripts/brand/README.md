# Brand & README asset tooling

Reproducible generation and validation of Brizo visual assets. Requires Node ≥ 20 only:
no system packages, no browser, no network after `npm ci`.

```bash
npm ci
npm run build:readme   # -> assets/readme/*.svg + static/*.png (public, source-independent)
npm run build:brand    # -> branding-private/exports/** (PRIVATE, needs the logo master)
npm run validate       # checks SVG parsing, palette, PNG sizes/alpha, Markdown links
```

| File | Purpose |
| --- | --- |
| `lib.mjs` | Palette, Inter text outlining, resvg rendering, ICO/ICNS/BMP encoders, PNG decoder |
| `build-readme-assets.mjs` | Animated hero, divider, capability cards and roadmap (light/dark) |
| `build-brand-assets.mjs` | Logo variants, lockups, PNG ladder (16–1024), Windows ICO, macOS ICNS + iconset, Linux hicolor, favicons, toolbar icons, GitHub social preview, NSIS/DMG installer art |
| `build-private-hero.mjs` | PRIVATE animated sailing-logo hero → `branding-private/hero-<version>/` (needs the master) |
| `validate.mjs` | Repository validation used by CI |
| `test-theme-toggle.cjs` | Behaviour test for `docs/website/theme-toggle-reference.html` (needs Playwright) |

## Logo master (private)

`build-brand-assets.mjs` reads `branding-private/source/brizo-mark.svg` and
`brizo-mark-small.svg` (paths with ids `rear-sail`, `front-sail`, `hull`). The
folder is git-ignored and the script refuses to write into tracked paths,
because logo provenance is unresolved ([BRAND_PROVENANCE.md](../../docs/BRAND_PROVENANCE.md)).
A copy of the master is attached to the owner's private review page; see
`docs/DEVELOPMENT_STATE.md` for its location.

## Licences of tools

`@resvg/resvg-js` MPL-2.0 · `opentype.js` MIT · `@fontsource/inter` (Inter) SIL OFL 1.1.
