import json, sys
sys.path.insert(0, '.')
from phase1.schema import validate_v2
p = 'phase1/evidence/Walker.json'
d = json.load(open(p))
d['notes'] += (" Targeted pass 4 2026-10-02 (targeted4-I): no election changed. Tried: (1) eGov stores each document at /egov/documents/<unix upload time>_<n>.pdf "
               "(item 10238 resolves to /egov/documents/1781808693_24638.pdf = 18 Jun 2026 18:51:33 GMT), so posting times are readable, but the removed runoff 'Unofficial Results' item 10174 "
               "also returns HTTP 404 at view=detail, and its file name cannot be known without probing. Item 10175 'May 26, 2026 Election Night Reconciliation Form' resolves to "
               "/egov/documents/1779845954_50967.pdf (Last-Modified Wed, 27 May 2026 01:39:14 GMT = 8:39 PM CDT election night), a one-page RICOH scan of the reconciliation form, not results; "
               "it shows only that the office posted on election night, not what results were posted. The browse list (department 141) dates the 2024 files 04/06/2026 (re-uploads). "
               "(2) Check 4: four web searches; the City of Huntsville page 'November 5, 2024 Election and Voter's Information' links 'Unofficial Election Results' "
               "(DocumentCenter/View/23589, CreationDate Wed Nov 6 04:21:00 2024 UTC), which is the city's own one-page summary of its at-large council races with totals only "
               "('Final Unofficial Results of Election Returns November 5, 2024, General Election At-Large Councilmembers'), not a Walker County file and no per-precinct numbers, so it decides nothing; "
               "no Huntsville Item or other page with Walker County per-precinct numbers was found. (3) wayback-data: no targeted archives or sweep for Walker (sweep pending); "
               "the main harvest of co.walker.tx.us has no election-night captures. Not on newtools.cira.state.tx.us (eGov site).")
validate_v2(d)
json.dump(d, open(p, 'w'), indent=2, ensure_ascii=False)
t = open(p, encoding='utf-8').read(); print([c for c in set(t) if ord(c) > 127])
