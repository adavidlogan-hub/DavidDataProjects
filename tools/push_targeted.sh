#!/usr/bin/env bash
# Push phase1/targeted/{archives,wayback,pdfs,sweep} to the wayback-data branch. Used by targeted-archives.yml pdf-probe.yml, and archive-file-sweep.yml.
# Requires TOKEN, REPO, RUN_ID, JOB in the environment.
set -u
REMOTE="https://x-access-token:${TOKEN}@github.com/${REPO}.git"
WD=$(mktemp -d)
git clone -q --depth 1 --branch wayback-data "$REMOTE" "$WD"
mkdir -p "$WD/phase1/targeted"
for d in archives wayback pdfs sweep sweep2; do
  if [ -d "phase1/targeted/$d" ]; then cp -r "phase1/targeted/$d" "$WD/phase1/targeted/"; fi
done
cd "$WD"
git config user.name "targeted-archives"
git config user.email "targeted-archives@users.noreply.github.com"
git add phase1/targeted
git commit -q -m "Targeted archive search run ${RUN_ID} (${JOB})" || echo "nothing new"
for delay in 0 2 4 8 16; do
  sleep "$delay"
  git pull -q --rebase origin wayback-data || true
  if git push -q origin wayback-data; then echo pushed; exit 0; fi
done
echo "push failed after retries; results are in the run artifact"
exit 1
