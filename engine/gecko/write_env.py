#!/usr/bin/env python3
"""Write env.json for summarize.py.  write_env.py <metrics-dir> <runner> <source_sha256> <compile_outcome> [package]"""
import hashlib, json, os, sys
d, runner, src_sha, outcome = sys.argv[1:5]
pkg = sys.argv[5] if len(sys.argv) > 5 else ""
info = {"firefox_version": os.environ.get("FIREFOX_VERSION"), "runner": runner,
        "image": os.environ.get("ImageOS"), "image_version": os.environ.get("ImageVersion"),
        "source_sha256": src_sha, "compile_outcome": outcome}
if pkg and os.path.exists(pkg):
    h = hashlib.sha256()
    with open(pkg, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    info.update(package=os.path.basename(pkg), package_bytes=os.path.getsize(pkg), package_sha256=h.hexdigest())
json.dump(info, open(os.path.join(d, "env.json"), "w"), indent=2)
print(json.dumps(info, indent=2))
