# Project Vision

> Everything in this document describes **goals**. None of it is implemented yet.

## Mission

Build a **free, open-source desktop browser** that is fast, private by default,
light on system resources and open to the extension ecosystems people already
rely on.

## Who it is for

- People who want strong privacy protection without assembling it from add-ons.
- People who use extensions from **both** the Chrome and Firefox ecosystems.
- People who download media they are entitled to and want one integrated tool.
- People on modest hardware or battery power who want a browser that does less
  in the background.

## Brand meaning

Brizo is a deity of ancient Greek tradition associated with protecting sailors.
The brand stands for **freedom and exploration, effortless browsing, privacy
and protection, speed, independence and the open web.**

## Long-term goals

1. **Dual extension ecosystem.** Chrome extensions and Firefox add-ons under one
   secure manager, as far as research proves possible.
2. **Built-in privacy engine.** Blocking of ads, trackers and cosmetic clutter on
   by default, at a level comparable to uBlock Origin.
3. **Integrated Media Grabber.** Detection and download of authorised, non-DRM
   media, with a robust queue.
4. **Lightweight performance.** Measurable efficiency through tab sleeping, lazy
   restore and on-demand services.
5. **Modern desktop experience.** Vertical tabs, workspaces, split view,
   profiles and more, each weighed against the lightweight goal.

Details: [FEATURE_REQUIREMENTS.md](FEATURE_REQUIREMENTS.md).

## Non-negotiables

- Security protections (sandboxing, site isolation, certificate validation,
  signed updates) are never weakened for convenience or memory savings.
- No DRM circumvention or unauthorised access.
- No fabricated benchmarks, compatibility claims or test results.
- No telemetry by default.
- No paid infrastructure without explicit owner approval.

## Development model

- Free and open source. Licence pending (see [DECISIONS.md](DECISIONS.md)).
- Developed primarily through Claude Code Cloud and GitHub:
  development branch → pull request → GitHub Actions (free runners) →
  downloadable test builds → owner testing → stable release.
- No mandatory local toolchain, no paid CI, no mandatory paid Apple Developer
  membership. Whether this is achievable for a full browser is the open
  question of [Phase 1](TECHNICAL_RESEARCH_PLAN.md).

## Platform targets

Long term: Windows x64/ARM64, macOS Apple Silicon/Intel, Linux x64/ARM64.
Initial testing priority: macOS Apple Silicon → Windows x64 → Linux x64.
No platform is supported until a working build is produced and tested.
