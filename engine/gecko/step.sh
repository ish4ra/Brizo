#!/usr/bin/env bash
# Run a command and record its wall time and exit code.
#   step.sh <timings.csv> <name> <command...>
CSV="$1"; NAME="$2"; shift 2
[ -f "$CSV" ] || echo "step,start_epoch,end_epoch,seconds,exit_code" > "$CSV"
S=$(date +%s); set +e; "$@"; RC=$?; set -e; E=$(date +%s)
echo "$NAME,$S,$E,$((E-S)),$RC" >> "$CSV"
echo "::notice title=${NAME}::${NAME} took $((E-S)) s (exit ${RC})"
exit $RC
