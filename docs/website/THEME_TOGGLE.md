# Light/Dark Appearance: README Limits and Website Toggle

Last verified: 2026-11-25 (Task 002).

## 1. What a GitHub README can and cannot do

| Capability | Possible in a README? | Evidence |
| --- | --- | --- |
| Run JavaScript | **No.** GitHub sanitises README HTML, and SVGs embedded via `<img>` never execute scripts | GitHub markup sanitisation; the repository validator rejects scripts in SVGs |
| Change the viewer's GitHub theme | **No.** No supported README mechanism exists | none |
| Show different artwork for light and dark | **Yes**, `<picture>` + `<source media="(prefers-color-scheme: dark)">` | GitHub docs source (`github/docs`, *basic-writing-and-formatting-syntax.md*: "The `<picture>` HTML element is supported."); GitHub changelog 2022-08-15 (GA) |
| Link to the viewer's appearance settings | **Yes**, `https://github.com/settings/appearance` | Verified 2026-11-25: signed-out requests redirect to `/login?return_to=…/settings/appearance`; a made-up settings path returns 404 |

Therefore the README has **no theme switch**. It has a compact note under the
hero: sun/moon icons, the text "Artwork adapts to light and dark mode
automatically", and a link labelled **GitHub appearance settings**. The link
opens GitHub's own settings page (sign-in required); it does not switch anything.

### Which preference does `<picture>` follow?

- `prefers-color-scheme` is evaluated by the viewer's browser. With
  GitHub's theme on *Sync with system*, the artwork follows the operating system.
  This was verified in Chromium: the dark sources load under a dark colour scheme.
- GitHub's 2022 changelog describes this markup as showing the image for the
  theme the viewer uses on GitHub. Whether an explicit GitHub theme that
  *differs* from the OS overrides the media query could **not** be verified from
  the Claude sandbox, because GitHub's front-end JavaScript host is blocked there.
  Third-party reports conflict.
  **Owner check:** set GitHub to *Dark* while the OS is light, then reload the README.
- The legacy `#gh-dark-mode-only` / `#gh-light-mode-only` URL fragments are not
  used. The current GitHub docs page no longer documents them.

### Reduced motion in README artwork (finding, fixed)

In Chromium with reduced motion emulated, an animated SVG **inside `<img>`
keeps animating**: the `@media (prefers-reduced-motion)` rule inside the SVG
did not apply. An *inline* SVG stopped correctly. Whether a real OS-level
setting reaches `<img>` SVGs could not be tested in the sandbox.

Fix (GitHub-compatible, no JS): each README `<picture>` now lists
reduced-motion sources first, which serve the static first-frame PNGs:

```html
<picture>
  <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="assets/readme/static/hero-dark.png">
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/readme/static/hero-light.png">
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/hero-dark.svg">
  <img alt="…" src="assets/readme/hero-light.svg">
</picture>
```

The page itself evaluates `<picture>` media queries, so they respect the setting.
`scripts/brand/validate.mjs` enforces this pattern.

## 2. Website toggle (future Brizo website, not deployed)

Reference implementation: [`theme-toggle-reference.html`](theme-toggle-reference.html)
(single file, no framework). Behaviour test:
`node scripts/brand/test-theme-toggle.cjs` (Playwright; 10 checks pass).

| Requirement | How |
| --- | --- |
| Sun/Moon toggle | One 32 px `<button>`; it shows the icon of the theme you would switch to |
| Instant full-page switch | All colours are CSS custom properties; the toggle sets `data-theme` on `<html>` |
| System preference | With no saved choice, `@media (prefers-color-scheme: dark)` decides; live OS changes are followed through a `matchMedia` listener |
| Persisted choice | `localStorage['brizo-theme']` (wrapped in try/catch); a pre-paint inline script applies it, so there is no flash |
| Back to system | A "Use system setting" button appears only while a choice is saved |
| Keyboard | Native button (Tab, Enter, Space), visible `:focus-visible` ring, `aria-label` names the action, a polite live region announces the result |
| Reduced motion | Icon rotation and transition are disabled under `prefers-reduced-motion` |
| Multi-tab | A `storage` event keeps open tabs in sync |

Deploying a website (e.g. GitHub Pages) needs separate owner approval.
