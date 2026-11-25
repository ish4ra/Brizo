#!/usr/bin/env python3
"""Automated smoke test for an experimental Brizo/Gecko Linux build.

Drives the *packaged* browser over Firefox's built-in WebDriver BiDi endpoint
(no extra driver binary). Every check is recorded as pass / fail / not-verified,
never assumed.

    smoke_test.py <path-to-firefox-binary> <out-dir>
"""
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
import zipfile

from websockets.sync.client import connect

BIN, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
PORT = 9222
results = []


def record(name, status, detail=""):
    results.append({"check": name, "status": status, "detail": str(detail)[:500]})
    print(f"[{status.upper():12}] {name}: {detail}", flush=True)


class Bidi:
    def __init__(self, ws):
        self.ws, self.n = ws, 0

    def call(self, method, params=None, timeout=60):
        self.n += 1
        my_id = self.n
        self.ws.send(json.dumps({"id": my_id, "method": method, "params": params or {}}))
        deadline = time.time() + timeout
        while time.time() < deadline:
            msg = json.loads(self.ws.recv(timeout=timeout))
            if msg.get("id") == my_id:
                if msg.get("type") == "error":
                    raise RuntimeError(f"{msg.get('error')}: {msg.get('message')}")
                return msg["result"]
        raise TimeoutError(method)

    def eval(self, ctx, expr):
        r = self.call("script.evaluate", {"expression": expr, "target": {"context": ctx}, "awaitPromise": True})
        return r.get("result", {}).get("value")


profile = tempfile.mkdtemp(prefix="brizo-smoke-")
log = open(os.path.join(OUT, "browser-stderr.log"), "w")
proc = subprocess.Popen(
    [BIN, "--headless", "--no-remote", "--profile", profile, f"--remote-debugging-port={PORT}", "about:blank"],
    stdout=log, stderr=subprocess.STDOUT,
)

ws = None
for _ in range(90):
    try:
        ws = connect(f"ws://127.0.0.1:{PORT}/session", open_timeout=2, max_size=64 * 2**20)
        break
    except Exception:
        time.sleep(1)
if ws is None:
    record("launch", "fail", "BiDi endpoint did not come up within 90 s (see browser-stderr.log)")
    proc.kill()
    json.dump(results, open(os.path.join(OUT, "smoke.json"), "w"), indent=2)
    sys.exit(1)

b = Bidi(ws)
try:
    caps = b.call("session.new", {"capabilities": {"alwaysMatch": {"acceptInsecureCerts": False}}})["capabilities"]
    record("launch", "pass", f"{caps.get('browserName')} {caps.get('browserVersion')} pid={proc.pid}")
except Exception as e:  # noqa: BLE001
    record("launch", "fail", e)

def top_contexts():
    return b.call("browsingContext.getTree", {})["contexts"]

ctx = top_contexts()[0]["context"]

# HTTPS navigation
try:
    b.call("browsingContext.navigate", {"context": ctx, "url": "https://example.com/", "wait": "complete"})
    title = b.eval(ctx, "document.title")
    proto = b.eval(ctx, "location.protocol")
    ok = proto == "https:" and "Example" in (title or "")
    record("https_navigation", "pass" if ok else "fail", f"title={title!r} protocol={proto}")
    shot = b.call("browsingContext.captureScreenshot", {"context": ctx})["data"]
    open(os.path.join(OUT, "example-com.png"), "wb").write(base64.b64decode(shot))
except Exception as e:  # noqa: BLE001
    record("https_navigation", "fail", e)

# Certificate validation must reject an expired certificate
try:
    try:
        b.call("browsingContext.navigate", {"context": ctx, "url": "https://expired.badssl.com/", "wait": "complete"})
        nav_err = None
    except Exception as e:  # noqa: BLE001
        nav_err = e
    uri = b.eval(ctx, "document.documentURI") or ""
    rejected = uri.startswith("about:certerror") or uri.startswith("about:neterror") or nav_err is not None
    record("certificate_validation", "pass" if rejected else "fail",
           f"documentURI={uri[:80]!r} navigate_error={str(nav_err)[:120] if nav_err else None}")
except Exception as e:  # noqa: BLE001
    record("certificate_validation", "not-verified", e)

# Tabs: open and close
try:
    before = len(top_contexts())
    new = b.call("browsingContext.create", {"type": "tab"})["context"]
    b.call("browsingContext.navigate", {"context": new, "url": "https://www.mozilla.org/", "wait": "complete"})
    during = len(top_contexts())
    b.call("browsingContext.close", {"context": new})
    after = len(top_contexts())
    ok = during == before + 1 and after == before
    record("tabs_open_close", "pass" if ok else "fail", f"contexts before={before} during={during} after={after}")
except Exception as e:  # noqa: BLE001
    record("tabs_open_close", "fail", e)

# Sandbox evidence: inspect content processes (children with -contentproc)
try:
    b.call("browsingContext.navigate", {"context": ctx, "url": "https://example.com/", "wait": "complete"})
    time.sleep(2)
    out = subprocess.run(["ps", "-eo", "pid,args"], capture_output=True, text=True).stdout
    pids = [int(l.split()[0]) for l in out.splitlines()[1:] if "-contentproc" in l]
    parent_ns = os.readlink(f"/proc/{proc.pid}/ns/user")
    info = []
    seccomp_ok = 0
    for pid in pids:
        try:
            st = open(f"/proc/{pid}/status").read()
            sec = [l.split()[1] for l in st.splitlines() if l.startswith("Seccomp:")][0]
            ns = os.readlink(f"/proc/{pid}/ns/user")
            info.append({"pid": pid, "seccomp": sec, "own_user_ns": ns != parent_ns})
            seccomp_ok += sec == "2"
        except Exception as e:  # noqa: BLE001
            info.append({"pid": pid, "error": str(e)})
    json.dump(info, open(os.path.join(OUT, "sandbox-processes.json"), "w"), indent=2)
    status = "pass" if pids and seccomp_ok == len(pids) else ("fail" if pids else "not-verified")
    record("content_sandbox_seccomp", status,
           f"{seccomp_ok}/{len(pids)} content processes in seccomp filter mode; user-namespace isolated: "
           f"{sum(1 for i in info if i.get('own_user_ns'))}/{len(pids)}")
except Exception as e:  # noqa: BLE001
    record("content_sandbox_seccomp", "not-verified", e)

# Settings and extension manager pages (privileged; BiDi may not script them)
for name, url, probe in [
    ("settings_page", "about:preferences", "!!document.getElementById('mainPrefPane') || document.title"),
    ("extension_manager_page", "about:addons", "!!document.querySelector('addon-list, #categories, categories-box') || document.title"),
]:
    try:
        b.call("browsingContext.navigate", {"context": ctx, "url": url, "wait": "complete"})
        try:
            v = b.eval(ctx, probe)
            record(name, "pass" if v else "fail", f"probe={v!r}")
        except Exception as e:  # noqa: BLE001
            record(name, "not-verified", f"navigated, but privileged page not scriptable via BiDi: {e}")
    except Exception as e:  # noqa: BLE001
        record(name, "not-verified", f"navigation refused by BiDi: {e}")

try:
    b.call("session.end", {})
except Exception:  # noqa: BLE001
    pass
ws.close()
proc.terminate()
try:
    proc.wait(timeout=20)
except subprocess.TimeoutExpired:
    proc.kill()

# Static packaging check: settings + add-ons manager UI are present in omni.ja
try:
    appdir = os.path.dirname(os.path.realpath(BIN))
    names = set()
    cands = [appdir, os.path.join(appdir, "..", "Resources")]  # Linux layout, macOS .app layout
    for omni in [os.path.join(d, *p) for d in cands for p in (["omni.ja"], ["browser", "omni.ja"])]:
        if os.path.exists(omni):
            with zipfile.ZipFile(omni) as z:
                names.update(z.namelist())
    has_prefs = any(n.endswith("preferences/preferences.xhtml") for n in names)
    has_addons = any(n.endswith("aboutaddons.html") for n in names)
    record("package_contains_settings_ui", "pass" if has_prefs else "fail", "preferences.xhtml in omni.ja")
    record("package_contains_addons_manager", "pass" if has_addons else "fail", "aboutaddons.html in omni.ja")
except Exception as e:  # noqa: BLE001
    record("package_static_checks", "not-verified", e)

json.dump(results, open(os.path.join(OUT, "smoke.json"), "w"), indent=2)
fails = [r for r in results if r["status"] == "fail"]
print(f"\n{len(results)} checks: {len(results) - len(fails)} not failed, {len(fails)} failed")
sys.exit(1 if fails else 0)
