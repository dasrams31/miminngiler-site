#!/bin/bash
# Autosync MiminNgiler: jika ada perubahan di source site, otomatis deploy ke
# GitHub Pages (gh-pages) + sinkron ke staging backup harian.
# Dipanggil oleh cron tiap 5 menit. Idempoten & anti-overlap via flock.
set -e
SITE="$HOME/workspace/miminngiler-site"
STAGING="$HOME/workspace/releases/miminngiler/site"
HASHFILE="$SITE/.sync-hash"
LOCK="$SITE/.autosync.lock"

exec 9>"$LOCK"
flock -n 9 || { echo "Autosync: lock aktif (kemungkinan cron harian sedang deploy), lewati."; exit 0; }

hash_dir() {
  find "$SITE" -type f \
    -not -name '.sync-hash' \
    -not -name '.autosync.lock' \
    -not -path '*/.git/*' \
    | sort | xargs md5sum 2>/dev/null | md5sum | cut -d' ' -f1
}

NEW_HASH="$(hash_dir)"
OLD_HASH="$(cat "$HASHFILE" 2>/dev/null || echo '')"

if [ "$NEW_HASH" = "$OLD_HASH" ]; then
  exit 0
fi

echo "Autosync: perubahan terdeteksi, menjalankan deploy..."
bash "$SITE/deploy.sh"
# sinkron ke staging (sumber backup harian ke GitHub) — script ikut disimpan
rsync -a --delete --exclude='.sync-hash' --exclude='.autosync.lock' \
  "$SITE/" "$STAGING/"
# catat hash SETELAH deploy (build.py me-regenerate p-*.html)
hash_dir > "$HASHFILE"
echo "Autosync selesai."
