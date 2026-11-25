#!/usr/bin/env bash
# Run a mach command inside the MozillaBuild environment (invoked via MozillaBuild's bash).
#   win-mach.sh <srcdir-unix-path> <mach args...>
set -euo pipefail
cd "$1"; shift
export MOZCONFIG="$PWD/mozconfig"
exec ./mach --no-interactive "$@"
