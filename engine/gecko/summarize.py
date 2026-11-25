#!/usr/bin/env python3
"""Summarise measured build metrics into results.json and the job summary.

    summarize.py <metrics-dir>
Reads timings.csv, resources.csv, env.json (and smoke/smoke.json if present).
"""
import csv
import json
import os
import sys

D = sys.argv[1]
out = {}
env_path = os.path.join(D, "env.json")
if os.path.exists(env_path):
    out.update(json.load(open(env_path)))

steps = []
if os.path.exists(os.path.join(D, "timings.csv")):
    for r in csv.DictReader(open(os.path.join(D, "timings.csv"))):
        steps.append({"step": r["step"], "seconds": int(r["seconds"]), "exit_code": int(r["exit_code"])})
out["steps"] = steps

res = os.path.join(D, "resources.csv")
if os.path.exists(res):
    rows = list(csv.DictReader(open(res)))
    if rows:
        tot = int(rows[0]["mem_total_kib"])
        out["mem_total_gib"] = round(tot / 2**20, 2)
        out["peak_mem_used_gib"] = round(max(tot - int(r["mem_available_kib"]) for r in rows) / 2**20, 2)
        out["peak_swap_used_gib"] = round(max(int(r["swap_total_kib"]) - int(r["swap_free_kib"]) for r in rows) / 2**20, 2)
        used = [int(r["disk_used_kib"]) for r in rows]
        out["disk_used_start_gib"] = round(used[0] / 2**20, 1)
        out["disk_used_peak_gib"] = round(max(used) / 2**20, 1)
        out["disk_avail_min_gib"] = round(min(int(r["disk_avail_kib"]) for r in rows) / 2**20, 1)
        out["max_load1"] = max(float(r["load1"]) for r in rows)
        out["samples"] = len(rows)

smoke = os.path.join(D, "smoke", "smoke.json")
if os.path.exists(smoke):
    out["smoke"] = json.load(open(smoke))

json.dump(out, open(os.path.join(D, "results.json"), "w"), indent=2)

lines = ["## Gecko build experiment — measured results", ""]
for k in ["firefox_version", "runner", "source_sha256", "package", "package_bytes", "package_sha256",
          "mem_total_gib", "peak_mem_used_gib", "peak_swap_used_gib", "disk_used_start_gib",
          "disk_used_peak_gib", "disk_avail_min_gib", "max_load1"]:
    if k in out:
        lines.append(f"- **{k}**: `{out[k]}`")
lines += ["", "| Step | Seconds | Exit |", "| --- | --- | --- |"]
lines += [f"| {s['step']} | {s['seconds']} | {s['exit_code']} |" for s in steps]
if "smoke" in out:
    lines += ["", "| Smoke check | Status | Detail |", "| --- | --- | --- |"]
    lines += [f"| {r['check']} | {r['status']} | {r['detail'][:140].replace('|', '/')} |" for r in out["smoke"]]
text = "\n".join(lines) + "\n"
print(text)
summary = os.environ.get("GITHUB_STEP_SUMMARY")
if summary:
    open(summary, "a").write(text)
