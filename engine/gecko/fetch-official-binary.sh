#!/usr/bin/env bash
# Download and VERIFY Mozilla's official Firefox Linux x86_64 build (comparison baseline).
#   fetch-official-binary.sh <version> <dest-dir>
# Verification chain: Mozilla release KEY -> GPG signature on SHA256SUMS -> archive hash.
set -euo pipefail
V="$1"; DEST="$2"; BASE="https://archive.mozilla.org/pub/firefox/releases/${V}"
REL="linux-x86_64/en-US/firefox-${V}.tar.xz"
mkdir -p "$DEST/dl"; cd "$DEST/dl"
curl -fsSL --retry 4 -o KEY "$BASE/KEY"
curl -fsSL --retry 4 -o SHA256SUMS "$BASE/SHA256SUMS"
curl -fsSL --retry 4 -o SHA256SUMS.asc "$BASE/SHA256SUMS.asc"
export GNUPGHOME="$(mktemp -d)"; gpg --batch --quiet --import KEY; gpg --batch --verify SHA256SUMS.asc SHA256SUMS
curl -fsSL --retry 4 -o ff.tar.xz "$BASE/$REL"
EXPECTED="$(grep " ${REL}\$" SHA256SUMS | awk '{print $1}')"; ACTUAL="$(sha256sum ff.tar.xz | awk '{print $1}')"
[ -n "$EXPECTED" ] && [ "$EXPECTED" = "$ACTUAL" ] || { echo "SHA-256 mismatch"; exit 1; }
echo "official binary verified: $REL $ACTUAL"
tar -xf ff.tar.xz -C "$DEST"; rm -f ff.tar.xz
