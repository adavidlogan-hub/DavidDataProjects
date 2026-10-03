import sys
sys.path.insert(0,'.')
from txprecinct.config import load_config
from txprecinct.store import Store
from txprecinct.fetch import normalize_url
st=Store(load_config().state_dir)
def h(u):
    r=st.latest_ok(normalize_url(u)) if not u.startswith('websearch:') else st.latest_ok(u)
    return dict(r)['content_hash'] if r else None
if __name__=='__main__':
    for u in sys.argv[1:]: print(h(u),u)
