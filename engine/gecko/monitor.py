#!/usr/bin/env python3
"""Portable resource sampler (macOS/Windows/Linux) writing the same CSV
columns as monitor.sh, every 15 s until killed.
    monitor.py <out.csv> <path-for-disk>"""
import os, sys, time
import psutil

out, path = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.abspath(os.sep)
with open(out, "w") as f:
    f.write("epoch,mem_total_kib,mem_available_kib,swap_total_kib,swap_free_kib,disk_used_kib,disk_avail_kib,load1\n")
while True:
    vm, sw, du = psutil.virtual_memory(), psutil.swap_memory(), psutil.disk_usage(path)
    try:
        load1 = os.getloadavg()[0]
    except (AttributeError, OSError):
        load1 = psutil.getloadavg()[0]
    k = lambda b: int(b // 1024)
    with open(out, "a") as f:
        f.write(f"{int(time.time())},{k(vm.total)},{k(vm.available)},{k(sw.total)},{k(sw.free)},{k(du.used)},{k(du.free)},{load1:.2f}\n")
    time.sleep(15)
