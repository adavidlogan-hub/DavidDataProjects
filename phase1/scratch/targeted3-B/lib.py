import json,sys
sys.path.insert(0,'.'); sys.path.insert(0,'phase1/scratch/targeted3-B')
from h import h
from phase1.schema import compute_tag, compute_confidence, validate_v2
AG='targeted3-B'
def src(url,quote,supports,via='fetch_module'):
    hh=h(url)
    assert hh, url
    return {"url":url,"via":via,"content_hash":hh,"quote":quote,"supports":supports}
def load(c): return json.load(open(f'phase1/evidence/{c}.json'))
def save(c,d,note,rationale=None):
    d['notes']=(d['notes'].rstrip()+' '+note).strip()
    tag,single=compute_tag(d['elections']); d['tag']=tag; d['confidence']=compute_confidence(d)
    if rationale: d['tag_rationale']=rationale
    validate_v2(d)
    json.dump(d,open(f'phase1/evidence/{c}.json','w'),indent=2,ensure_ascii=False); open(f'phase1/evidence/{c}.json','a').write('\n')
    print(c,d['tag'],d['confidence'])

