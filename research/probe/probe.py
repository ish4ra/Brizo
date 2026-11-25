"""Bounded, zero-cost GitHub-hosted runner probe for Brizo (Task 002).
Reports hardware, disk and toolchains. Downloads nothing large: upstream source
sizes are read from HTTP Content-Length headers only."""
import json, os, platform, shutil, subprocess, sys, time, urllib.request

def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120).stdout.strip()
    except Exception as e:  # noqa: BLE001
        return f"ERR {e}"

def mem_gib():
    try:
        if sys.platform.startswith("linux"):
            for line in open("/proc/meminfo"):
                if line.startswith("MemTotal"):
                    return round(int(line.split()[1]) / 1048576, 1)
        if sys.platform == "darwin":
            return round(int(sh("sysctl -n hw.memsize")) / 1073741824, 1)
        if sys.platform == "win32":
            out = sh('powershell -NoProfile -Command "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory"')
            return round(int(out) / 1073741824, 1)
    except Exception:  # noqa: BLE001
        return None

def disks():
    paths = ["C:\\", "D:\\"] if sys.platform == "win32" else ["/", "/mnt"] if sys.platform.startswith("linux") else ["/", "/System/Volumes/Data"]
    out = {}
    for p in paths:
        if os.path.exists(p):
            u = shutil.disk_usage(p)
            out[p] = {"total_gib": round(u.total / 2**30, 1), "free_gib": round(u.free / 2**30, 1)}
    return out

def head_size(url):
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=30) as r:
            return round(int(r.headers.get("Content-Length", 0)) / 2**30, 2)
    except Exception as e:  # noqa: BLE001
        return f"ERR {e}"

def get_json(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}

r = {
    "runner_label": os.environ.get("PROBE_LABEL"),
    "image": os.environ.get("ImageOS"), "image_version": os.environ.get("ImageVersion"),
    "os": platform.platform(), "machine": platform.machine(),
    "cpus": os.cpu_count(), "mem_gib": mem_gib(), "disk_before": disks(),
    "tools": {
        "clang": sh("clang --version").splitlines()[:1], "python": platform.python_version(),
        "ninja": sh("ninja --version"), "ccache": sh("ccache --version").splitlines()[:1],
        "sccache": sh("sccache --version"), "rustc": sh("rustc --version"), "node": sh("node --version"),
        "git": sh("git --version"),
    },
}
if sys.platform == "darwin":
    r["tools"]["xcode"] = sh("xcodebuild -version").splitlines()[:2]
    r["tools"]["macos_sdks"] = sh("ls /Applications | grep -i xcode")
if sys.platform == "win32":
    r["tools"]["visual_studio"] = sh('"C:\\Program Files (x86)\\Microsoft Visual Studio\\Installer\\vswhere.exe" -latest -property catalog_productDisplayVersion')
    r["tools"]["win_sdk"] = sh('dir /b "C:\\Program Files (x86)\\Windows Kits\\10\\Include"')

# Policy-compliant disk cleanup: delete preinstalled toolchains we would not use
# (only inside our own ephemeral VM). Linux only, timed.
if sys.platform.startswith("linux") and os.environ.get("PROBE_CLEANUP") == "1":
    t = time.time()
    for d in ["/usr/share/dotnet", "/usr/local/lib/android", "/opt/ghc", "/usr/local/.ghcup",
              "/opt/hostedtoolcache/CodeQL", "/usr/local/share/boost", "/usr/share/swift"]:
        sh(f"sudo rm -rf {d}")
    sh("sudo docker image prune --all --force")
    r["cleanup_seconds"] = round(time.time() - t)
    r["disk_after_cleanup"] = disks()

if os.environ.get("PROBE_SOURCES") == "1":
    rel = get_json("https://chromiumdash.appspot.com/fetch_releases?channel=Stable&platform=Linux&num=1")
    cv = rel[0]["version"] if isinstance(rel, list) and rel else None
    ff = get_json("https://product-details.mozilla.org/1.0/firefox_versions.json")
    fv = ff.get("LATEST_FIREFOX_VERSION")
    r["upstream"] = {
        "chromium_stable": cv,
        "chromium_source_tar_xz_gib": head_size(f"https://commondatastorage.googleapis.com/chromium-browser-official/chromium-{cv}.tar.xz") if cv else None,
        "chromium_source_lite_tar_xz_gib": head_size(f"https://commondatastorage.googleapis.com/chromium-browser-official/chromium-{cv}-lite.tar.xz") if cv else None,
        "firefox_release": fv,
        "firefox_source_tar_xz_gib": head_size(f"https://archive.mozilla.org/pub/firefox/releases/{fv}/source/firefox-{fv}.source.tar.xz") if fv else None,
    }

print(json.dumps(r, indent=2))
with open(os.environ.get("GITHUB_STEP_SUMMARY", os.devnull), "a") as f:
    f.write(f"### {r['runner_label']}\n```json\n{json.dumps(r, indent=2)}\n```\n")
with open(f"probe-{r['runner_label']}.json", "w") as f:
    json.dump(r, f, indent=2)
