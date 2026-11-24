# Brizo Brand Guidelines

Status: **draft for owner review.** The logo is a *provisional candidate*;
see [BRAND_PROVENANCE.md](BRAND_PROVENANCE.md) before using it anywhere public.

## 1. Identity

| | |
| --- | --- |
| Project name | **Brizo** |
| Product name | **Brizo Browser** |
| Working tagline | *Fast. Private. Lightweight. Open.* (pending owner approval) |
| Personality | Serious, modern, calm, premium. Not a gaming, crypto or student-project look. |
| Themes | Freedom & exploration · effortless browsing · privacy & protection · speed · independence · the open web |

Name origin: Brizo, a deity of ancient Greek (Delian) tradition associated with
protecting sailors and seafarers.

## 2. Logo (approved direction, provisional artwork)

The owner selected a minimalist sailboat mark, **Balanced** colour variation:

| Element | Colour | Notes |
| --- | --- | --- |
| Large rear sail | Light Sail Blue `#6FBCEB` | Tall, curved, sharp rounded tip |
| Smaller front sail | Primary Blue `#1684D1` | Rounded triangle, overlaps the rear sail |
| Lower hull | Deep Ocean Blue `#174EA4` | Wide, rounded, separated from the sails by a gap |

Construction rules:

- Flat fills only. **No** gradients, shadows, 3D, textures or outlines in the mark.
- Smooth, rounded geometry; the three shapes stay separate objects
  (layer order: rear sail → front sail → hull).
- **Never add** birds, shields, globes, compasses, rings, letters or decoration.
- Do not redraw, rotate, recolour or re-proportion the mark without owner approval.

### Variants

| Variant | Use |
| --- | --- |
| Full-colour mark | Default, on light *or* dark backgrounds |
| Small-size mark | ≤ 32 px only. The hull is lowered slightly so the sail/hull gap stays visible |
| Monochrome (`#0F172A` / `#FFFFFF`) | Single-colour contexts. A knock-out gap separates the two sails |
| Wordmark | "Brizo" set in Inter SemiBold, −1.5 % tracking, outlined |
| Horizontal lockup | Mark + wordmark; cap height ≈ 36 % of mark height, gap ≈ 20 % |
| Vertical lockup | Mark above wordmark; cap height ≈ 20 % of mark height |
| Product lockup | Mark + "Brizo Browser" |

### Clear space & minimum size

- Clear space around the mark: at least **25 % of the mark height** on every side.
- Square app icons use a consistent **1/16 (6.25 %)** margin.
- Minimum size: 16 px (small-size geometry), 20 mm in print.

## 3. Colour system

### Primary (fixed, do not alter)

| Token | Hex | Role |
| --- | --- | --- |
| `--brizo-light-sail` | `#6FBCEB` | Rear sail; accents on dark UI; links on dark |
| `--brizo-primary` | `#1684D1` | Front sail; primary actions, focus, selection |
| `--brizo-deep-ocean` | `#174EA4` | Hull; links and emphasis on light UI |

### Supporting

| Token | Hex | Role |
| --- | --- | --- |
| `--brizo-bg-light` | `#F4F8FC` | Light surfaces |
| `--brizo-bg-dark` | `#0B1220` | Dark surfaces |
| `--brizo-border` | `#D8E5F3` | Soft borders (light) |
| `--brizo-white` | `#FFFFFF` | Cards, text on dark |
| `--brizo-text` | `#0F172A` | Primary text on light |

### Theme tokens (proposal)

| Token | Light | Dark |
| --- | --- | --- |
| Surface / background | `#F4F8FC` | `#0B1220` |
| Surface / raised | `#FFFFFF` | `#111A2E` |
| Border | `#D8E5F3` | `#1E2B44` |
| Text / primary | `#0F172A` | `#FFFFFF` |
| Text / secondary | `#475569` | `#A9B8CC` |
| Accent / action fill | `#1684D1` | `#1684D1` |
| Accent / link text | `#174EA4` | `#6FBCEB` |

`#111A2E`, `#1E2B44`, `#475569`, `#A9B8CC` are **proposed** supporting neutrals
(owner approval pending). They do not replace any brand colour.

### Measured contrast (WCAG 2.x)

| Foreground | on `#FFFFFF` | on `#F4F8FC` | on `#0B1220` |
| --- | --- | --- | --- |
| `#6FBCEB` | 2.09 | 1.95 | **8.98** |
| `#1684D1` | 4.00 | 3.74 | 4.69 |
| `#174EA4` | **7.89** | **7.39** | 2.37 |
| `#0F172A` | **17.85** | **16.73** | — |
| `#FFFFFF` | — | — | **18.72** |
| `#475569` | **7.58** | **7.10** | — |
| `#A9B8CC` | — | — | **9.29** |

Consequences:

- `#1684D1` is fine for **fills** (buttons with white text ≥ 18.66 px bold /
  large text, icons, focus rings) but **below 4.5:1 for body text** on light
  backgrounds. Use `#174EA4` for text links in light mode.
- In dark mode, use `#6FBCEB` for text links. `#174EA4` is decorative only on dark.
- The hull (`#174EA4`) on `#0B1220` is 2.37:1. The mark stays recognisable
  thanks to the lighter sails, so the dark-background version keeps the fixed
  colours. A lighter dark-mode hull is **not** used without owner approval.

### Semantic colours (proposal, not yet approved)

| Purpose | Light | Dark |
| --- | --- | --- |
| Success | `#15803D` | `#4ADE80` |
| Warning | `#B45309` | `#FBBF24` |
| Danger | `#B91C1C` | `#F87171` |

## 4. Typography

- **Inter** (SIL Open Font License 1.1), via `@fontsource/inter`.
- Wordmark: Inter SemiBold 600; headlines: Inter Bold 700; UI/body: Inter 400–500.
- In generated SVGs, text is converted to outlines so no font loading is needed.

## 5. Imagery & motion

- Source-independent motifs: layered waves, wind lines, dotted navigation courses.
- Motion is slow and subtle (8–26 s loops), linear or ease-in-out, never flashing.
- Always honour `prefers-reduced-motion`.

## 6. Do not

- Use proprietary assets or trade dress from Chrome, Firefox, Brave, Safari, Edge or others.
- Add gradients or effects to the mark.
- Publish the provisional logo while provenance is unresolved.
- Present the tagline as final before owner approval.

## 7. Asset sources

| What | Where |
| --- | --- |
| Generators | `scripts/brand/` (`build-brand-assets.mjs`, `build-readme-assets.mjs`) |
| README artwork | `assets/readme/` (generated, public, source-independent) |
| Logo master & exports | `branding-private/` (**git-ignored**) + the owner's private review page |
