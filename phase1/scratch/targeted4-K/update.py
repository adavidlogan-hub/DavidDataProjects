"""targeted4-K: record retried (sandbox-allowlist) files on six evidence files."""
import json, sys
sys.path.insert(0, '.')
from phase1.schema import compute_tag, compute_confidence, validate_v2

ALLOW = "this sandbox's egress block (body 'Host not in allowlist: {h}. Add this host to your network egress settings to allow access.'), not a county response"

def load(c):
    return json.load(open(f'phase1/evidence/{c}.json'))

def save(c, r):
    tag, _ = compute_tag(r['elections'])
    r['tag'] = tag
    r['confidence'] = compute_confidence(r)
    validate_v2(r)
    json.dump(r, open(f'phase1/evidence/{c}.json', 'w'), indent=2, ensure_ascii=False)
    open(f'phase1/evidence/{c}.json', 'a').write('\n')
    print(c, r['tag'], r['confidence'])

def replace(r, key, old, new):
    assert old in r[key], (r['county'], key, old)
    r[key] = r[key].replace(old, new, 1)

def src(url, h, quote, supports):
    return {"url": url, "via": "fetch_module", "content_hash": h, "quote": quote, "supports": supports}

# Cherokee
r = load('Cherokee')
u = "https://www.co.cherokee.tx.us/ips/cms/othercountyoffices/2026-03%5CUNOFFICIAL%20Precinct%20Results%2003-03-2026.pdf"
r['sources'].append(src(u, "53ae48d18ef9fa428ea823ba1006485caf0460a97f811dc043f937acc0416b92",
    "HTTP 200 after redirect; final_url http://www.co.cherokee.tx.us/ips/cms/index.html (county home page HTML, HTTrack-mirrored template, not a PDF)",
    "the backslash form of the primary precinct link (as written in the page's href) is not a file on the server; the earlier HTTP 403 for it (verifier-6) was " + ALLOW.format(h="www.co.cherokee.tx.us")))
r['elections']['2026_primary']['fact'] += (" Targeted pass 4 (targeted4-K): the forward-slash copy is the only copy; the backslash href '2026-03%5CUNOFFICIAL Precinct Results 03-03-2026.pdf' redirects to the county home page. "
    "The report has per-precinct candidate votes with an 'Election Day Voting' column (e.g. precinct 12, US Senator DEM, James Talarico 10 election day); header also reads 'OFFICIAL RESULTS ... Polling Places Reporting 20 of 24'; PDF CreationDate Thu Mar 5 21:30:30 2026 UTC (3:30 PM CST Mar 5). "
    "A conditional re-request on 2026-10-03 got HTTP 304 with ETag \"69ab9511-2f8a4e\" (hex 69ab9511 = 2026-03-07 03:01:37 UTC), so the Last-Modified is the file's stored time, not the request time. Printed run time and upload time are both after election night, so rule 47 cannot give END; no election-night county-totals file was opened, so not LATER.")
r['notes'] += (" Targeted pass 4 2026-10-03 (targeted4-K): no election changed. The retried backslash URL 'othercountyoffices/2026-03%5CUNOFFICIAL Precinct Results 03-03-2026.pdf' (earlier HTTP 403 for verifier-6 was " + ALLOW.format(h="www.co.cherokee.tx.us") +
    ") now redirects to the county home page index.html (content hash 53ae48d1..., same as the 8 of 8 redirect), so it adds no file. The forward-slash primary precinct file is unchanged (HTTP 304, ETag 69ab9511 = 2026-03-07 03:01:37 UTC, matching Last-Modified, so this server gives a real file time, not the request time): per-precinct election-day votes, Run Time 3:30 PM Run Date 03/05/2026, CreationDate 2026-03-05 21:30 UTC, uploaded 2026-03-06 21:01 CT, all after election night. 2026_primary stays UNDETERMINED under rule 47 and DECISIONS 67 (no election-night precinct or county-totals file opened). 2 fetches (1 cache, 1 conditional).")
save('Cherokee', r)

# Donley
r = load('Donley')
replace(r, 'notes', "Seed URL (http default.aspx) and https /page/donley.Elections returned HTTP 403;",
    "Seed URL (http default.aspx) returned HTTP 403, which was " + ALLOW.format(h="www.co.donley.tx.us") + " (on 2026-10-03 it redirects to https://www.co.donley.tx.us/); https /page/donley.Elections returned a genuine IIS '403 - Forbidden: Access is denied.' page;")
u = "http://www.co.donley.tx.us/upload/page/0087/docs/MarchPrimary20260001.pdf"
r['sources'].append(src(u, "d643144dc8ff0d037a4bbe6f384923e63e1b64a23830868c929e6820f5eb64de",
    "HTTP 200, application/pdf, Last-Modified Wed, 04 Mar 2026 05:19:06 GMT, ETag \"4a99526c96abdc1:0\" (byte-identical to the https copy)",
    "confirms 2026_primary END: same precinct report and same 11:19 PM CST election-night upload time over http; earlier http 403s (research-3, verifier-5) were the sandbox block"))
r['notes'] += (" Targeted pass 4 2026-10-03 (targeted4-K): no election changed. The retried http URL of '03032026 Primary unofficial' (MarchPrimary20260001.pdf; earlier HTTP 403 for research-3 and verifier-5 was " + ALLOW.format(h="www.co.donley.tx.us") +
    ") now returns the same bytes as the https copy (content hash d643144d...), Last-Modified Wed, 04 Mar 2026 05:19:06 GMT (11:19 PM CST Mar 3), CreationDate 4 Mar 2026 05:16:48 UTC; confirms 2026_primary END. 1 fetch (cache).")
save('Donley', r)

# Kimble
r = load('Kimble')
replace(r, 'notes', "2024 archive entry over http returned 403; https works.",
    "2024 archive entry over http returned 403 (" + ALLOW.format(h="www.co.kimble.tx.us") + "; on 2026-10-03 the http URL loads, redirected to https); https works.")
u = "http://www.co.kimble.tx.us/upload/page/0097/Final%20Cumulative%20Results-11-5-2024%2010-23-14%20PM.pdf"
r['sources'].append(src(u, "ee0c40dce67f37c9ce992f86aab5f907320e2f2fe81fa1d37b0f31a39230c1e6",
    "Cumulative Results Report KIMBLE COUNTY, TEXAS ... GENERAL ELECTION ... Official Election Day Tally ... Precincts Reporting 7 of 7 ... Run Time 9:53 PM Run Date 11/05/2024 (Last-Modified Wed, 06 Nov 2024 04:00:43 GMT)",
    "confirms 2024_general LATER: archive link as written (http) redirects to the same county-totals file, uploaded 10:00 PM CST election night; earlier http 403 was the sandbox block"))
r['notes'] += (" Targeted pass 4 2026-10-03 (targeted4-K): no election changed. The retried http archive link for the 2024 general (earlier HTTP 403 for research-5 was " + ALLOW.format(h="www.co.kimble.tx.us") +
    ") redirects to the https file already recorded: same bytes (content hash ee0c40dc...), Last-Modified Wed, 06 Nov 2024 04:00:43 GMT (10:00 PM CST Nov 5), CreationDate Wed Nov 6 03:53:58 2024 UTC, Run Time 9:53 PM; county totals by Absentee / Early / Election Day only ('Precinct' appears only in 'Precincts Reporting' and 'County Commissioner, Precinct 1/3'). Confirms 2024_general LATER. 1 fetch (cache).")
save('Kimble', r)

# Hartley
r = load('Hartley')
replace(r, 'notes', "the page links its PDFs over http, which return 403, so they were fetched over https.",
    "the page links its PDFs over http, which returned 403 at first (" + ALLOW.format(h="www.co.hartley.tx.us") + "; on 2026-10-03 the http links load), so they were fetched over https.")
base = "http://www.co.hartley.tx.us/upload/page/0103/"
for f, h, lm, sup in [
    ("5.26.26%20Summary%20Results.pdf", "fcbbb36a7d0c55785162d27a0e969a4395d9df6079a92751b16cb3b6fd6e0fb7", "Fri, 29 May 2026 22:34:30 GMT", "runoff county-totals scan uploaded May 29 (after election night); 2026_runoff stays UNDETERMINED"),
    ("3.3.26%20Summary%20Results%20Rep.pdf", "8ae5cc0cde18e0a711de777219b8616b14f18dd0b15e71b02844cf3be1a6010b", "Thu, 12 Mar 2026 15:26:31 GMT", "primary summary uploaded Mar 12 (after election night); 2026_primary stays UNDETERMINED"),
    ("3.3.26%20Summary%20Results%20Report%20Rep.pdf", "77d95f05e48865e2f5e9acad63dffef30fffd27e2b1dd8467fe9c8150134f1db", "Mon, 16 Mar 2026 18:40:06 GMT", "primary precinct report uploaded Mar 16 (after election night); 2026_primary stays UNDETERMINED")]:
    r['sources'].append(src(base + f, h, f"HTTP 200 over http as linked, Last-Modified {lm}; byte-identical to the https copy", sup + "; earlier http 403s (research-4, verifier-5) were the sandbox block"))
r['notes'] += (" Targeted pass 4 2026-10-03 (targeted4-K): no election changed. The three http links as written on Voter.Information (earlier HTTP 403 for research-4 and verifier-5 was " + ALLOW.format(h="www.co.hartley.tx.us") +
    ") now load and are byte-identical to the https copies already recorded: '5.26.26 Summary Results.pdf' (hash fcbbb36a..., Last-Modified Fri, 29 May 2026 22:34:30 GMT, scan CreationDate 2026-05-29 23:31 UTC), '3.3.26 Summary Results Rep.pdf' (hash 8ae5cc0c..., Last-Modified Thu, 12 Mar 2026 15:26:31 GMT, CreationDate 2026-03-12 16:21 UTC), '3.3.26 Summary Results Report Rep.pdf' (hash 77d95f05..., 36 pages by precinct, Last-Modified Mon, 16 Mar 2026 18:40:06 GMT, CreationDate 2026-03-16 19:36 UTC). All after election night, so 2026_primary and 2026_runoff stay UNDETERMINED. 3 fetches (cache).")
save('Hartley', r)

# Lynn
r = load('Lynn')
replace(r, 'notes', "(http links return 403; https works)",
    "(http links returned 403 at first, which was " + ALLOW.format(h="www.co.lynn.tx.us") + "; on 2026-10-03 they load; https works)")
base = "http://www.co.lynn.tx.us/upload/page/0086/"
r['sources'].append(src(base + "20260303223813.pdf", "1269e3d52dcb9f5d293db930a5928a8666a65f75f8da118270cbb72904a2f807",
    "HTTP 200 over http as linked, Last-Modified Wed, 04 Mar 2026 03:41:48 GMT; byte-identical to the https copy",
    "confirms 2026_primary END (precinct report uploaded 9:41 PM CST election night); earlier http 403 (research-5) was the sandbox block"))
r['sources'].append(src(base + "20260526201006.pdf", "a0e996849b4e3039a7f5b5e16ec043bb2ee3b9357dff8b7bd3acf9f3b81553b1",
    "HTTP 200 over http as linked, Last-Modified Wed, 27 May 2026 01:13:14 GMT; byte-identical to the https copy",
    "confirms 2026_runoff END (precinct report uploaded 8:13 PM CDT election night); earlier http 403 (research-5) was the sandbox block"))
r['notes'] += (" Targeted pass 4 2026-10-03 (targeted4-K): no election changed. The http links as written on the Elections page (earlier HTTP 403 for research-5 was " + ALLOW.format(h="www.co.lynn.tx.us") +
    ") now load: 20260303223813.pdf (hash 1269e3d5..., Last-Modified Wed, 04 Mar 2026 03:41:48 GMT = 9:41 PM CST Mar 3) and 20260526201006.pdf (hash a0e99684..., Last-Modified Wed, 27 May 2026 01:13:14 GMT = 8:13 PM CDT May 26), byte-identical to the https copies already read; confirms 2026_primary END and 2026_runoff END. 2 fetches (cache).")
save('Lynn', r)

# Schleicher
r = load('Schleicher')
replace(r, 'notes', "Archive links point to www.schleichercounty.gov, which returned HTTP 403 to the fetch module;",
    "Archive links point to www.schleichercounty.gov, which returned HTTP 403 to the fetch module at first (" + ALLOW.format(h="www.schleichercounty.gov") + "; on 2026-10-03 it loads);")
u = "http://www.schleichercounty.gov/upload/page/0086/UNOFFICIAL%20RESULTS.pdf"
r['sources'].append(src(u, "3ebc52a609595c534aeb43f5419b398f9a2e58b0dfbc0f01f3a01a75a5e615f0",
    "HTTP 200, application/pdf, Last-Modified Wed, 06 Nov 2024 03:22:22 GMT (byte-identical to the www.co.schleicher.tx.us copy; image PDF, CreationDate Wed Nov 6 02:38:54 2024 UTC)",
    "confirms 2024_general LATER: the archive link as written serves the same county-totals report uploaded 9:22 PM CST election night; earlier 403s (research-7) were the sandbox block"))
r['notes'] += (" Targeted pass 4 2026-10-03 (targeted4-K): no election changed. The archive link as written, http://www.schleichercounty.gov/upload/page/0086/UNOFFICIAL RESULTS.pdf (earlier HTTP 403 twice for research-7 was " + ALLOW.format(h="www.schleichercounty.gov") +
    "), now loads: same bytes as the www.co.schleicher.tx.us copy (hash 3ebc52a6...), Last-Modified Wed, 06 Nov 2024 03:22:22 GMT (9:22 PM CST Nov 5) on the county's other host too. Confirms 2024_general LATER. 1 fetch (cache).")
save('Schleicher', r)
