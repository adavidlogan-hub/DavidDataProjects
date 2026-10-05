#!/bin/bash
# usage: probe.sh <County> <url>...
cd /home/user/DavidDataProjects
c=$1; shift
for u in "$@"; do
  echo "##### $u"
  python3 -m txprecinct.get "$u" --agent targeted3-F --purpose "check2:$c" 2>&1 | tail -1 | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); print('status',d['status'],'ok',d['ok'],'err',d['error'],'cache',d['from_cache'],'hash',d['content_hash'])"
  python3 -c "import sys; sys.path.insert(0,'.'); from txprecinct.config import load_config; from txprecinct.store import Store; from txprecinct.fetch import normalize_url; r=Store(load_config().state_dir).latest_ok(normalize_url(sys.argv[1])); d=dict(r) if r else {}; print({k:d.get(k) for k in ('last_modified','fetched_at','content_type','http_date','date') if k in d}); print([k for k in d])" "$u" 2>&1 | head -3
  f=/home/user/DavidDataProjects/phase1/scratch/targeted3-F/tmp.bin
  python3 -m txprecinct.cat "$u" --out $f 2>/dev/null
  if head -c 4 $f | grep -q '%PDF'; then pdfinfo $f 2>/dev/null | grep -E "CreationDate|ModDate|Pages|Producer|Creator"; pdftotext -layout $f - 2>/dev/null | head -${LINES_SHOW:-40}; fi
done
