import sys,subprocess,json,re,io
sys.path.insert(0,'.')
from txprecinct.config import load_config
from txprecinct.store import Store
from txprecinct.fetch import normalize_url
county=sys.argv[1]
for u in sys.argv[2:]:
    r=subprocess.run(['python3','-m','txprecinct.get',u,'--agent','targeted3-B','--purpose','check2:'+county],capture_output=True,text=True)
    j=json.loads(r.stdout.strip().splitlines()[-1])
    print('URL',u,'ok',j['ok'],j['status'],j.get('content_hash'))
    if not j['ok']: continue
    row=dict(Store(load_config().state_dir).latest_ok(normalize_url(u)))
    print('  hdr', {k:row.get(k) for k in row if k in ('last_modified','fetched_at','content_type','date')})
    data=subprocess.run(['python3','-m','txprecinct.cat',u],capture_output=True).stdout
    open('/tmp/claude-0/t3b.pdf','wb').write(data)
    md=subprocess.run(['pdfinfo','/tmp/claude-0/t3b.pdf'],capture_output=True,text=True).stdout
    print('  meta',' | '.join(l for l in md.splitlines() if l.split(':')[0] in ('Producer','Creator','CreationDate','ModDate','Pages','Title')))
    t=subprocess.run(['pdftotext','-l','1','-layout','/tmp/claude-0/t3b.pdf','-'],capture_output=True,text=True).stdout
    print('  p1:',re.sub(r'\s+',' ',t)[:int(__import__('os').environ.get('N','600'))])
