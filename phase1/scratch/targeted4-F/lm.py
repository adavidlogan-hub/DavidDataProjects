import sys; sys.path.insert(0,'.')
from txprecinct.config import load_config; from txprecinct.store import Store; from txprecinct.fetch import normalize_url
st=Store(load_config().state_dir)
for u in sys.argv[1:]:
    r=st.latest_ok(normalize_url(u)); d=dict(r) if r else {}
    print(u.split('/')[-1], {k:d.get(k) for k in d if 'modif' in k.lower() or k in ('fetched_at','status','content_hash','headers')})
