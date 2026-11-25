#!/usr/bin/env python3
"""Final acceptance gate for a Gecko experiment job.

    acceptance.py <metrics-dir> <platform>
Reads step outcomes from environment variables OUTCOME_<STEP> (GitHub step
outcomes: success/failure/cancelled/skipped/"") and smoke/smoke.json.
Writes acceptance.json and a job-summary table, prints SECURITY_OK=true|false
to $GITHUB_OUTPUT, and exits 1 unless every required stage passed. This keeps
continue-on-error steps from hiding a failure in the job conclusion.
"""
import json
import os
import sys

D, PLATFORM = sys.argv[1], sys.argv[2]
STAGES = ["source", "configure", "compile", "package", "smoke", "metrics_upload", "package_upload"]
out = {s: os.environ.get(f"OUTCOME_{s.upper()}", "") or "not-run" for s in STAGES}

smoke = []
p = os.path.join(D, "smoke", "smoke.json")
if os.path.exists(p):
    smoke = json.load(open(p))
security_checks = [r for r in smoke if r["check"].startswith(("content_sandbox", "linux_content", "certificate_validation"))]
sec_fail = [r for r in security_checks if r["status"] != "pass"]
security = "pass" if security_checks and not sec_fail else ("not-run" if not security_checks else "fail")
runtime_fail = [r for r in smoke if r["status"] == "fail"]

result = {
    "platform": PLATFORM,
    "stages": out,
    "security_gate": security,
    "security_gate_failures": sec_fail,
    "runtime_failures": runtime_fail,
}
required_ok = all(out[s] == "success" for s in ("source", "configure", "compile", "package", "metrics_upload", "package_upload"))
result["accepted"] = bool(required_ok and security == "pass" and not runtime_fail and out["smoke"] == "success")
json.dump(result, open(os.path.join(D, "acceptance.json"), "w"), indent=2)

lines = [f"## Acceptance gate: {PLATFORM}", "", "| Stage | Outcome |", "| --- | --- |"]
lines += [f"| {s} | {out[s]} |" for s in STAGES]
lines += [f"| **security gate** | **{security}** |", f"| **ACCEPTED** | **{result['accepted']}** |", ""]
for r in sec_fail:
    lines.append(f"- security `{r['check']}`: {r['status']}. {r['detail'][:200]}")
text = "\n".join(lines) + "\n"
print(text)
if os.environ.get("GITHUB_STEP_SUMMARY"):
    open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(text)
sys.exit(0 if result["accepted"] else 1)
