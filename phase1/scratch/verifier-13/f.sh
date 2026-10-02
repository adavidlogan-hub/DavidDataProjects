#!/bin/bash
# usage: f.sh county url outfile
cd /home/user/DavidDataProjects
python3 -m txprecinct.get "$2" --agent verifier-13 --purpose "check2:$1" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['status'], d['ok'], d.get('content_hash'), d.get('error'))"
python3 -c "import sys; sys.path.insert(0,'.'); from txprecinct.config import load_config; from txprecinct.store import Store; from txprecinct.fetch import normalize_url; r=Store(load_config().state_dir).latest_ok(normalize_url(sys.argv[1])); d=dict(r) if r else {}; print({k:d.get(k) for k in d if k in ('fetched_at','last_modified','content_type','status','headers','http_last_modified')} or d)" "$2"
[ -n "$3" ] && python3 -m txprecinct.cat "$2" --out "$3" && file "$3"
