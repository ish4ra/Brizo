#!/usr/bin/env bash
# Download and VERIFY the official Firefox source tarball from archive.mozilla.org.
#   fetch-source.sh <version> <dest-dir>
# Verification chain: Mozilla release KEY -> GPG signature on SHA256SUMS -> tarball hash.
set -euo pipefail
V="$1"; DEST="$2"
BASE="https://archive.mozilla.org/pub/firefox/releases/${V}"
TAR="firefox-${V}.source.tar.xz"
mkdir -p "$DEST/dl"; cd "$DEST/dl"
curl -fsSL --retry 4 -o KEY "$BASE/KEY"
curl -fsSL --retry 4 -o SHA256SUMS "$BASE/SHA256SUMS"
curl -fsSL --retry 4 -o SHA256SUMS.asc "$BASE/SHA256SUMS.asc"
export GNUPGHOME="$(mktemp -d)"
gpg --batch --quiet --import KEY
gpg --batch --verify SHA256SUMS.asc SHA256SUMS
echo "GPG signature on SHA256SUMS: OK"
curl -fsSL --retry 4 -o "$TAR" "$BASE/source/$TAR"
EXPECTED="$(grep " source/${TAR}\$" SHA256SUMS | awk '{print $1}')"
ACTUAL="$(sha256sum "$TAR" | awk '{print $1}')"
[ -n "$EXPECTED" ] && [ "$EXPECTED" = "$ACTUAL" ] || { echo "SHA-256 mismatch: expected=$EXPECTED actual=$ACTUAL"; exit 1; }
echo "source_sha256=$ACTUAL" | tee -a "${GITHUB_OUTPUT:-/dev/null}"
echo "tarball_bytes=$(stat -c %s "$TAR")" | tee -a "${GITHUB_OUTPUT:-/dev/null}"
cd "$DEST"
tar -xf "dl/$TAR"
rm -f "dl/$TAR"
SRC="$(find "$DEST" -maxdepth 1 -mindepth 1 -type d -name 'firefox-*' | head -1)"
echo "srcdir=$SRC" | tee -a "${GITHUB_OUTPUT:-/dev/null}"
echo "unpacked_gib=$(du -s --block-size=1G "$SRC" | cut -f1)" | tee -a "${GITHUB_OUTPUT:-/dev/null}"
