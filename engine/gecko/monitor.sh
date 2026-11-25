#!/usr/bin/env bash
# Background resource sampler: writes CSV every 15 s until killed.
#   monitor.sh <out.csv> <path-for-disk>
OUT="$1"; P="${2:-/}"
echo "epoch,mem_total_kib,mem_available_kib,swap_total_kib,swap_free_kib,disk_used_kib,disk_avail_kib,load1" > "$OUT"
while true; do
  m=$(awk '/MemTotal|MemAvailable|SwapTotal|SwapFree/{printf "%s,",$2}' /proc/meminfo)
  d=$(df -k --output=used,avail "$P" | tail -1 | awk '{printf "%s,%s",$1,$2}')
  l=$(cut -d' ' -f1 /proc/loadavg)
  echo "$(date +%s),${m}${d},${l}" >> "$OUT"
  sleep 15
done
