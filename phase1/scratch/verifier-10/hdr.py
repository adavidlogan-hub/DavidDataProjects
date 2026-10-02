import sys,json; sys.path.insert(0,'.')
from txprecinct.config import load_config; from txprecinct.store import Store; from txprecinct.fetch import normalize_url
s=Store(load_config().state_dir)
for u in sys.argv[1:]:
    r=s.latest_ok(normalize_url(u)); d=dict(r) if r else {}
    h=d.get('headers') or d.get('response_headers') or ''
    print(u.split('/')[-1], {k:d[k] for k in d if k in ('fetched_at','fetched_at_utc','last_modified','content_hash','status')})
