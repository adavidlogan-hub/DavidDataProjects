import sys; sys.path.insert(0,'.')
from txprecinct.config import load_config
from txprecinct.store import Store
s=Store(load_config().state_dir)
c=s.connect()
pat=sys.argv[1]
for r in c.execute("select url,status,fetched_at,last_modified,content_type,agent,error,content_hash from fetches where url like ? order by url,fetched_at",(pat,)):
    print(tuple(r))
