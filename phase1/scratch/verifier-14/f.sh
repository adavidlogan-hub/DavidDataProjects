# usage: f.sh <url> <county> <check>  -> fetch, save to scratch, print status + links
cd /home/user/DavidDataProjects
U="$1"; C="$2"; K="${3:-check2}"
python3 -m txprecinct.get "$U" --agent verifier-14 --purpose "$K:$C" 2>&1 | tail -1 | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); print('STATUS',d['status'],d['ok'],d['error'],d['content_hash'])"
python3 -c "import sys; sys.path.insert(0,'.'); from txprecinct.config import load_config; from txprecinct.store import Store; from txprecinct.fetch import normalize_url; r=Store(load_config().state_dir).latest_ok(normalize_url(sys.argv[1])); r=dict(r) if r else {}; print({k:r.get(k) for k in r if k not in ('body',)})" "$U"
