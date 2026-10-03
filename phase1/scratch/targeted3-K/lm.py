import sys; sys.path.insert(0,'/home/user/DavidDataProjects')
from txprecinct.config import load_config; from txprecinct.store import Store; from txprecinct.fetch import normalize_url
r=Store(load_config().state_dir).latest_ok(normalize_url(sys.argv[1]))
d=dict(r) if r else {}
import json
h=d.get('headers') or d.get('response_headers') or ''
print(d.get("last_modified"), "|", d.get("content_hash"))
