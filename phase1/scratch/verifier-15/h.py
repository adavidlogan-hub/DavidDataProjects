import sys; sys.path.insert(0,'.')
from txprecinct.config import load_config; from txprecinct.store import Store; from txprecinct.fetch import normalize_url
s=Store(load_config().state_dir)
def h(u):
    r=s.latest_ok(normalize_url(u)); return (r['content_hash'], r['last_modified']) if r else (None,None)
if __name__=='__main__':
    for u in sys.argv[1:]: print(h(u), u)
