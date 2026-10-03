import sys; sys.path.insert(0,'.')
from txprecinct.config import load_config; from txprecinct.store import Store; from txprecinct.fetch import normalize_url
st=Store(load_config().state_dir)
for u in sys.argv[1:]:
    r=st.latest_ok(normalize_url(u))
    if not r: print(u,'-> none'); continue
    d=dict(r); print(u); print('   ', {k:d.get(k) for k in d if k in ('fetched_at','status','content_hash','last_modified','headers_json','http_status')})
