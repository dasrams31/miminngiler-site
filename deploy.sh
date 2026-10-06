#!/bin/bash
# Deploy katalog MiminNgiler ke GitHub Pages (branch gh-pages)
set -e
SITE="$HOME/workspace/miminngiler-site"
WT="$HOME/workspace/releases/miminngiler-gh-pages"
REPO="$HOME/workspace/releases/miminngiler"

# pastikan worktree ada
if [ ! -f "$WT/.git" ]; then
  cd "$REPO" && git worktree add "$WT" gh-pages
fi

# generate halaman detail produk
python3 "$SITE/build.py"

# sinkron file site -> worktree (script internal tidak ikut ke publik)
rsync -a --delete --exclude='.git' --exclude='deploy.sh' --exclude='autosync.sh' \
  --exclude='.sync-hash' --exclude='.autosync.lock' "$SITE/" "$WT/"
# bersihkan file internal yang mungkin terlanjur ke-push sebelumnya
rm -f "$WT/autosync.sh" "$WT/.sync-hash" "$WT/.autosync.lock"

cd "$WT"
git -c user.name="dasrams31" -c user.email="ramadanadipa176@gmail.com" add -A
if git -c user.name="dasrams31" -c user.email="ramadanadipa176@gmail.com" diff --cached --quiet; then
  echo "Tidak ada perubahan."
else
  git -c user.name="dasrams31" -c user.email="ramadanadipa176@gmail.com" commit -m "Update katalog $(date +%Y-%m-%d)" -q
  TOKEN="$(cat "$HOME/workspace/mc-portal/config/github_token")"
  git push "https://dasrams31:${TOKEN}@github.com/dasrams31/miminngiler.git" gh-pages -q
  echo "Deployed: https://dasrams31.github.io/miminngiler/"
fi
