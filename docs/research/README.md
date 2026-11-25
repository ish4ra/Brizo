# Task 002 Research: Browser Foundation Feasibility

Date: 2026-11-25 · Branch: `claude/task-002-engine-feasibility`

**Verdict: CONDITIONAL GO**. Gecko (Firefox Release) downstream patch set as
the primary foundation, conditional on a free-runner build measurement.
Fallbacks: a Chromium patch set (needs donated or paid compute) and a CEF prototype shell.

| Document | Question answered |
| --- | --- |
| [ARCHITECTURE_DECISION_PROPOSAL.md](ARCHITECTURE_DECISION_PROPOSAL.md) | What we recommend, the conditions, the fallbacks |
| [ENGINE_COMPARISON.md](ENGINE_COMPARISON.md) | Chromium, ungoogled, Helium, Brave, Gecko forks, WebKit/Orion, Qt, CEF, Electron |
| [FREE_BUILD_FEASIBILITY.md](FREE_BUILD_FEASIBILITY.md) | What free runners really provide (measured) and what each engine needs |
| [EXTENSION_COMPATIBILITY.md](EXTENSION_COMPATIBILITY.md) | Chrome vs Firefox extension reality and the test plan |
| [CONTENT_BLOCKING.md](CONTENT_BLOCKING.md) | uBO, uBO Lite, adblock-rust, Shields |
| [MEDIA_GRABBER.md](MEDIA_GRABBER.md) | Detector, queue, FFmpeg and yt-dlp helpers, safety |
| [PERFORMANCE_BENCHMARK_PLAN.md](PERFORMANCE_BENCHMARK_PLAN.md) | Optimisation levers and a reproducible benchmark |
| [SECURITY_ARCHITECTURE.md](SECURITY_ARCHITECTURE.md) | Upstream tracking, updates, signing limits |
| [LICENSE_AUDIT.md](LICENSE_AUDIT.md) | Component licences, recommended Brizo licence |
| [SOURCES.md](SOURCES.md) | Every source with ID, date and evidence label |

Measured data: [`research/probe/RESULTS-2026-11-25.md`](../../research/probe/RESULTS-2026-11-25.md).

Method: primary sources were read from upstream repositories; runner capacity
was measured with a bounded, zero-cost probe (no source checkout, no build).
**No browser was compiled.** Statements are labelled [V] verified, [M] measured,
[S] secondary, [A] assumption, [U] unresolved.
