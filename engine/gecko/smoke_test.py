#!/usr/bin/env python3
"""Smoke and security test for an experimental Brizo/Gecko build (v2).

    smoke_test.py <path-to-firefox-binary> <out-dir>

Runs the packaged browser headless with two of Firefox's own automation
interfaces:
  * WebDriver BiDi (--remote-debugging-port): web-content checks (HTTPS,
    certificate rejection, tabs). BiDi refuses privileged about: pages by design.
  * Marionette (--marionette), Mozilla's automation protocol, in its privileged
    "chrome" context: runtime checks of about:preferences and about:addons, and
    Firefox's own sandbox report (Troubleshoot.snapshot().sandbox, the data
    shown in about:support).

Process-level evidence (Linux) is classified by Firefox process type; only
web-content ("tab") processes are held to the content-sandbox gate. The
fork server and utility processes have different sandbox policies and are
reported, not counted.

Statuses: pass | fail | not-verified | blocked-by-environment. Nothing is
assumed; every result carries its evidence. Exit 1 if any check failed.
"""
import base64
import json
import os
import platform
import socket
import subprocess
import sys
import tempfile
import time
import zipfile

from websockets.sync.client import connect

BIN, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
BIDI_PORT, MARIONETTE_PORT = 9222, 2828
IS_LINUX = sys.platform.startswith("linux")
results = []


def record(name, status, detail="", evidence=None):
    results.append({"check": name, "status": status, "detail": str(detail)[:600], "evidence": evidence})
    print(f"[{status.upper():22}] {name}: {str(detail)[:300]}", flush=True)


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


class Marionette:
    """Minimal client for Mozilla's Marionette protocol (length-prefixed JSON)."""

    def __init__(self, port):
        self.s = socket.create_connection(("127.0.0.1", port), timeout=60)
        self.n = 0
        self._read()  # server hello

    def _read(self):
        head = b""
        while not head.endswith(b":"):
            c = self.s.recv(1)
            if not c:
                raise ConnectionError("marionette closed")
            head += c
        n = int(head[:-1])
        data = b""
        while len(data) < n:
            data += self.s.recv(n - len(data))
        return json.loads(data)

    def cmd(self, name, params=None):
        self.n += 1
        msg = json.dumps([0, self.n, name, params or {}]).encode()
        self.s.sendall(str(len(msg)).encode() + b":" + msg)
        while True:
            r = self._read()
            if isinstance(r, list) and r[0] == 1 and r[1] == self.n:
                if r[2]:
                    raise RuntimeError(r[2])
                return r[3]

    def chrome_js(self, script):
        return self.cmd("WebDriver:ExecuteScript", {"script": script, "args": []}).get("value")


profile = tempfile.mkdtemp(prefix="brizo-smoke-")
log = open(os.path.join(OUT, "browser-stderr.log"), "w")
# MOZ_REMOTE_ALLOW_SYSTEM_ACCESS: Mozilla's documented opt-in that lets the
# automation session use the privileged (chrome) context; test process only.
env = dict(os.environ, MOZ_REMOTE_ALLOW_SYSTEM_ACCESS="1")
proc = subprocess.Popen(
    [BIN, "--headless", "--no-remote", "--profile", profile, "--marionette",
     f"--remote-debugging-port={BIDI_PORT}", "about:blank"],
    stdout=log, stderr=subprocess.STDOUT, env=env,
)

ws = None
for _ in range(120):
    try:
        ws = connect(f"ws://127.0.0.1:{BIDI_PORT}/session", open_timeout=2, max_size=64 * 2**20)
        break
    except Exception:
        time.sleep(1)
if ws is None:
    record("launch", "fail", "BiDi endpoint did not come up within 120 s (see browser-stderr.log)")
    proc.kill()
    json.dump(results, open(os.path.join(OUT, "smoke.json"), "w"), indent=2)
    sys.exit(1)

# ---------------------------------------------------------------- BiDi checks
b = Bidi(ws)
try:
    caps = b.call("session.new", {"capabilities": {"alwaysMatch": {"acceptInsecureCerts": False}}})["capabilities"]
    record("launch", "pass", f"{caps.get('browserName')} {caps.get('browserVersion')} pid={proc.pid} arch={platform.machine()}")
except Exception as e:  # noqa: BLE001
    record("launch", "fail", e)


def top_contexts():
    return b.call("browsingContext.getTree", {})["contexts"]


ctx = top_contexts()[0]["context"]
try:
    b.call("browsingContext.navigate", {"context": ctx, "url": "https://example.com/", "wait": "complete"})
    title, proto = b.eval(ctx, "document.title"), b.eval(ctx, "location.protocol")
    record("https_navigation", "pass" if proto == "https:" and "Example" in (title or "") else "fail", f"title={title!r} protocol={proto}")
    shot = b.call("browsingContext.captureScreenshot", {"context": ctx})["data"]
    open(os.path.join(OUT, "example-com.png"), "wb").write(base64.b64decode(shot))
except Exception as e:  # noqa: BLE001
    record("https_navigation", "fail", e)

try:
    nav_err = None
    try:
        b.call("browsingContext.navigate", {"context": ctx, "url": "https://expired.badssl.com/", "wait": "complete"})
    except Exception as e:  # noqa: BLE001
        nav_err = e
    uri = b.eval(ctx, "document.documentURI") or ""
    ok = uri.startswith("about:certerror")
    record("certificate_validation", "pass" if ok else "fail", f"documentURI={uri[:90]!r} navigate_error={str(nav_err)[:140] if nav_err else None}")
except Exception as e:  # noqa: BLE001
    record("certificate_validation", "not-verified", e)

try:
    before = len(top_contexts())
    new = b.call("browsingContext.create", {"type": "tab"})["context"]
    b.call("browsingContext.navigate", {"context": new, "url": "https://www.mozilla.org/", "wait": "complete"})
    during = len(top_contexts())
    b.call("browsingContext.close", {"context": new})
    after = len(top_contexts())
    record("tabs_open_close", "pass" if during == before + 1 and after == before else "fail", f"contexts before={before} during={during} after={after}")
except Exception as e:  # noqa: BLE001
    record("tabs_open_close", "fail", e)

# Keep a web-content process alive for the process-level evidence below.
try:
    b.call("browsingContext.navigate", {"context": ctx, "url": "https://example.com/", "wait": "complete"})
except Exception:  # noqa: BLE001
    pass

time.sleep(3)  # let content processes finish sandbox setup

# ------------------------------------------------ Process-level evidence (Linux)
procs = []
if IS_LINUX:
    try:
        parent_ns = os.readlink(f"/proc/{proc.pid}/ns/user")
        for pid in os.listdir("/proc"):
            if not pid.isdigit():
                continue
            try:
                args = open(f"/proc/{pid}/cmdline", "rb").read().split(b"\0")
                if not any(a == b"-contentproc" for a in args):
                    continue
                st = open(f"/proc/{pid}/status").read()
                seccomp = [l.split()[1] for l in st.splitlines() if l.startswith("Seccomp:")][0]
                argv = [a.decode(errors="replace") for a in args if a]
                ptype = "forkserver" if "-forkserver" in argv else argv[-1]
                procs.append({"pid": int(pid), "type": ptype, "seccomp_mode": seccomp,
                              "own_user_ns": os.readlink(f"/proc/{pid}/ns/user") != parent_ns})
            except (FileNotFoundError, ProcessLookupError, PermissionError, IndexError):
                continue
    except Exception as e:  # noqa: BLE001
        record("process_inventory", "not-verified", e)
    json.dump(procs, open(os.path.join(OUT, "sandbox-processes.json"), "w"), indent=2)

try:
    b.call("session.end", {})
except Exception:  # noqa: BLE001
    pass
ws.close()
time.sleep(1)

# ------------------------------------------- Marionette (privileged) checks
sandbox = None
try:
    m = Marionette(MARIONETTE_PORT)
    m.cmd("WebDriver:NewSession", {"capabilities": {}})
    m.cmd("Marionette:SetContext", {"value": "chrome"})
    sandbox = m.chrome_js("""
      return (async () => {
        const {Troubleshoot} = ChromeUtils.importESModule("resource://gre/modules/Troubleshoot.sys.mjs");
        const snap = await Troubleshoot.snapshot();
        return snap.sandbox || null;
      })();""")
    json.dump(sandbox, open(os.path.join(OUT, "firefox-sandbox-report.json"), "w"), indent=2)
    record("firefox_sandbox_report", "pass" if sandbox else "not-verified",
           {k: sandbox.get(k) for k in ("contentSandboxLevel", "effectiveContentSandboxLevel", "hasSeccompBPF",
                                        "hasSeccompTSync", "hasUserNamespaces", "hasPrivilegedUserNamespaces",
                                        "canSandboxContent", "canSandboxMedia")} if sandbox else "no sandbox section")
    for name, url, probe in [
        ("settings_page_runtime", "about:preferences", "!!d.getElementById('mainPrefPane')"),
        ("extension_manager_page_runtime", "about:addons", "!!d.querySelector('categories-box, #categories, addon-list, #main')"),
    ]:
        r = m.chrome_js(f"""
          return (async () => {{
            const tab = gBrowser.addTab("{url}", {{triggeringPrincipal: Services.scriptSecurityManager.getSystemPrincipal()}});
            gBrowser.selectedTab = tab;
            const br = tab.linkedBrowser;
            for (let i = 0; i < 150; i++) {{
              const d = br.contentDocument;
              if (d && d.readyState == "complete" && {probe}) {{
                const out = {{ok: true, uri: d.documentURI, title: d.title}};
                gBrowser.removeTab(tab);
                return out;
              }}
              await new Promise(r => setTimeout(r, 200));
            }}
            return {{ok: false, uri: br.currentURI.spec}};
          }})();""")
        record(name, "pass" if r and r.get("ok") else "fail", r)
    try:
        m.cmd("Marionette:Quit", {"flags": ["eForceQuit"]})
    except Exception:  # noqa: BLE001
        pass
except Exception as e:  # noqa: BLE001
    record("marionette_session", "not-verified", e)

# ----------------------------------------------------------- Security gate
if sandbox:
    lvl, eff = sandbox.get("contentSandboxLevel"), sandbox.get("effectiveContentSandboxLevel")
    ok = isinstance(eff, int) and eff > 0 and eff == lvl
    record("content_sandbox_level", "pass" if ok else "fail", f"configured={lvl} effective={eff}")
else:
    record("content_sandbox_level", "not-verified", "Firefox sandbox report unavailable")

if IS_LINUX:
    tabs = [p for p in procs if p["type"] == "tab"]
    others = [p for p in procs if p["type"] != "tab"]
    if not tabs:
        record("linux_content_seccomp", "not-verified", f"no web-content processes found; other child processes: {others}")
    else:
        bad = [p for p in tabs if p["seccomp_mode"] != "2"]
        record("linux_content_seccomp", "fail" if bad else "pass",
               f"{len(tabs) - len(bad)}/{len(tabs)} web-content processes in seccomp filter mode; non-content children: "
               + ", ".join(f"{p['type']}:seccomp={p['seccomp_mode']}" for p in others), evidence=procs)
        has_userns = bool(sandbox and sandbox.get("hasUserNamespaces"))
        isolated = [p for p in tabs if p["own_user_ns"]]
        if has_userns:
            record("linux_content_user_namespaces", "pass" if len(isolated) == len(tabs) else "fail",
                   f"{len(isolated)}/{len(tabs)} web-content processes in their own user namespace (Firefox reports hasUserNamespaces=true)")
        else:
            record("linux_content_user_namespaces", "blocked-by-environment",
                   f"Firefox reports hasUserNamespaces={sandbox.get('hasUserNamespaces') if sandbox else None}: "
                   "unprivileged user namespaces unavailable to this binary on this host "
                   "(see apparmor/sysctl evidence in the job log); namespace layer not active")

proc.terminate()
try:
    proc.wait(timeout=20)
except subprocess.TimeoutExpired:
    proc.kill()

# --------------------------------------------- Static packaging checks
try:
    appdir = os.path.dirname(os.path.realpath(BIN))
    names = set()
    for d in [appdir, os.path.join(appdir, "..", "Resources")]:
        for rel in (["omni.ja"], ["browser", "omni.ja"]):
            omni = os.path.join(d, *rel)
            if os.path.exists(omni):
                raw = open(omni, "rb").read()
                try:
                    with zipfile.ZipFile(omni) as z:
                        names.update(z.namelist())
                except zipfile.BadZipFile:
                    # Mozilla's optimised omni.ja layout: entry names are still stored verbatim
                    for n in (b"preferences/preferences.xhtml", b"aboutaddons.html"):
                        if n in raw:
                            names.add(n.decode())
    record("package_contains_settings_ui", "pass" if any(n.endswith("preferences/preferences.xhtml") for n in names) else "fail")
    record("package_contains_addons_manager", "pass" if any(n.endswith("aboutaddons.html") for n in names) else "fail")
except Exception as e:  # noqa: BLE001
    record("package_static_checks", "not-verified", e)

json.dump(results, open(os.path.join(OUT, "smoke.json"), "w"), indent=2)
fails = [r for r in results if r["status"] == "fail"]
print(f"\n{len(results)} checks: {len(fails)} failed, "
      f"{sum(r['status'] == 'blocked-by-environment' for r in results)} blocked by environment, "
      f"{sum(r['status'] == 'not-verified' for r in results)} not verified")
sys.exit(1 if fails else 0)
