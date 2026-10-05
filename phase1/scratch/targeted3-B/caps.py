import json,subprocess,sys
for p in sys.argv[1:]:
    try: d=json.loads(subprocess.check_output(['git','show','origin/wayback-data:'+p],stderr=subprocess.DEVNULL))
    except Exception as e: print(p,'MISSING'); continue
    print('##',p, d.get('targets'))
    for w,v in d.get('windows',{}).items():
        errs=[c.get('error') for c in v.get('cdx',[])]
        print(' ',w,'cdx errors',errs,'captures',len(v.get('captures',[])))
        for c in v.get('captures',[]): print('    ',c['local'],c['original'][:150],c.get('saved_as'))
