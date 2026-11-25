# Performance Architecture and Benchmark Plan

No numbers in this document are results. Brizo publishes performance figures
only from this reproducible method.

## 1. Optimisation levers (planned)

| Lever | Gecko mechanism to build on [A] | Brizo work |
| --- | --- | --- |
| Tab sleeping | Tab unloading on memory pressure | Time-based sleep after N minutes, exclusions (audio, forms, pinned) |
| Smart discarding | Memory-pressure observers | Priority by last use, size and site type |
| Lazy session restore | Session store restores on demand | Default on |
| Background reduction | Timer throttling of background tabs | Stricter defaults, telemetry off |
| Extension cost | Per-extension process | Show per-extension memory; suspend idle event pages |
| Startup | Lazy-loaded components | Defer Media Grabber, helper checks and update checks |
| Battery | Hardware video decode, OS power APIs | Battery-saver profile |
| GPU/video | WebRender, hardware decode | Keep upstream defaults; verify on all three OSes |

**Never traded for memory:** process sandboxing, site isolation (Fission on
Gecko), certificate validation, safe browsing, update signature checks.

## 2. Benchmark method

**Browsers:** Brizo, Chrome, Firefox, Brave and Edge, latest stable on the same
day, default settings plus one "with uBO" variant where applicable.
**Hardware:** fixed machines per OS (macOS Apple Silicon, Windows x64, Linux
x64). Record model, RAM, OS build and power state. Plugged in, no other apps,
5-minute idle before each run. Free cloud runners are **not** used for
performance numbers (noisy shared VMs).

**Memory metric:** sum of the private (unique) memory of **all** browser
processes: macOS `footprint`, Windows Private Working Set via
`Get-Process`/ETW, Linux USS via `smem` or `/proc/*/smaps_rollup`. Never the
main process alone.

| Scenario | Steps | Metrics |
| --- | --- | --- |
| Cold start | Reboot, launch to first paint of a local blank page | Time to first paint, total memory at +10 s |
| Warm start | Quit, relaunch | Same |
| Idle | 1 blank tab, 5 min | Memory, CPU % average |
| 1 tab | Fixed static site | Memory, page load time |
| 5 tabs | Fixed corpus | Memory after 60 s |
| 20 tabs | Fixed corpus | Memory after 120 s; again after sleep or discard |
| Discard | 20 tabs, trigger sleep | Memory recovered, time to restore a tab |
| Media | 1080p VP9 and H.264 playback, 5 min | CPU %, dropped frames, energy (macOS `powermetrics`) |
| Extensions | 0 vs uBO vs uBO + Bitwarden + Dark Reader | Memory and CPU delta |
| Blocking | 50-site corpus | Requests blocked, load time |

Corpus: pages saved with SingleFile or replayed through a local record/replay
proxy, so content is identical across browsers. Each scenario runs 10
times; report the median and IQR, plus the raw data and scripts in the repo.
Any published comparison links to the raw data.
