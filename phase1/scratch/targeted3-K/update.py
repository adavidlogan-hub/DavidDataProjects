import json, sys
sys.path.insert(0, '/home/user/DavidDataProjects')
from phase1.schema import compute_tag, compute_confidence, validate_v2
from phase1.schema import RESULT_TO_TAG
AG = 'targeted3-K'
P = '/home/user/DavidDataProjects/phase1/evidence/%s.json'

def load(c): return json.load(open(P % c))
def save(c, d):
    tag, single = compute_tag(d['elections'])
    d['tag'] = tag
    d['confidence'] = compute_confidence(d)
    validate_v2(d)
    json.dump(d, open(P % c, 'w'), indent=2, ensure_ascii=False)
    print(c, d['tag'], d['confidence'], {k: (v['result'], v['check']) for k, v in d['elections'].items()})
def note(d, s): d['notes'] = (d['notes'] + ' ' if d['notes'] else '') + 'Targeted pass 3 2026-10-02 (%s): %s' % (AG, s)
def src(url, via, h, quote, supports): return dict(url=url, via=via, content_hash=h, quote=quote, supports=supports)
def el(result, check, ctf, pfs, n, url, fact):
    return dict(result=result, check=check, county_totals_first_seen=ctf, precinct_first_seen=pfs,
                night_updates_with_precinct_numbers=n, evidence_url=url, fact=fact)

# ---------------- Haskell ----------------
d = load('Haskell')
H = 'https://www.haskellcountytx.gov/upload/page/7706/'
u_rp = H + 'ELECTION-UNOFFICIAL-RESULT-REPORT_52585_1772604388995.pdf'
u_dp = H + 'ELECTION-UNOFFICIAL-RESULT-REPORT%20DEMOCRATIC%203.3.26.pdf'
u_rpp = H + 'REPUBLICAN%20PRECINCT%20BY%20PRECINCT%203.3.26.pdf'
u_dpp = H + 'DEMOCRATIC%20PRECINCT%20BY%20PRECINCT%203.3.26.pdf'
u_rr = H + 'REPUBLICAN%20UNOFFICIAL%20RESULTS%205.26.26.pdf'
u_dr = H + 'UNOFFICIAL%20DEMOCRATIC%20RUNOFF%20RESULTS%205.26.26.pdf'
u_rpct = H + 'PRIMARY%20RUNOFF%20PCT%20BY%20PCT.pdf'
u_24 = H + 'precinct%20by%20precinct%20for%20nov%202024%20election.pdf'
d['results_url'] = 'https://www.haskellcountytx.gov/page/haskell.Elections'
d['platform'] = 'county_pdfs'
d['host'] = 'www.haskellcountytx.gov'
d['evidence_url'] = u_rr
d['elections']['2026_primary'] = el('LATER', '2', '2026-03-03 23:16 CT', '2026-04-01 15:44 CT', '0', u_dp,
    "County page links 'MARCH 3, 2026 DEMOCRATIC UNOFFICIAL RESULTS' (SOS-format 'Texas Secretary of State Election Unofficial Results Report 2026 DEMOCRATIC PRIMARY ELECTION March 03, 2026 HASKELL County', county totals with columns 'Early Voting by Mail / Early Voting In Person / Election Day Count / Early Voting Count / Total Voters', e.g. 'JAMES TALARICO 3 33 17 36 53'), PDF CreationDate 2026-03-04 05:00:07 UTC, Last-Modified Wed, 04 Mar 2026 05:16:53 GMT (11:16 PM CST election night); and 'MARCH 3, 2026 REPUBLICAN UNOFFICIAL RESULTS' (same format, 'JOHN CORNYN 11 202 215 213 428'), CreationDate 2026-03-04 06:06:29 UTC (12:06 AM CST), Last-Modified Wed, 04 Mar 2026 13:54:56 GMT. The only primary precinct files, 'REPBUBLICAN PRECINCT BY PRECINCT 3.3.26' and 'DEOMOCRATIC PRECINCT BY PRECINCT 3.3.26', are scans with Last-Modified Wed, 01 Apr 2026 20:44:30 GMT and 20:43:36 GMT. County totals on election night; precinct numbers four weeks later.")
d['elections']['2026_runoff'] = el('LATER', '2', '2026-05-26 19:58 CT', '2026-06-29 10:04 CT', '0', u_rr,
    "County page links 'MAY 26, 2026 DEMOCRATIC UNOFFICIAL RESULTS' (scan, Last-Modified Wed, 27 May 2026 00:58:27 GMT = 7:58 PM CDT) and 'MAY 26, 2026 REPUBLICAN UNOFFICIAL RESULTS' (scan, Last-Modified Wed, 27 May 2026 01:33:23 GMT = 8:33 PM CDT). Read from the page images: 'Texas Secretary of State Election Unofficial Results Report 2026 REPUBLICAN PRIMARY RUNOFF ELECTION May 26, 2026 HASKELL County', county totals only, e.g. 'KEN PAXTON 15 125 133 140 273' (Election Day Count 133). 'PRIMARY RUNOFF RESULTS FOR PRECINCT BY PRECINCT/ REP AND DEM' is a scan with Last-Modified Mon, 29 Jun 2026 15:04:45 GMT. County totals on election night; precinct numbers a month later.")
d['elections']['2024_general']['fact'] = "Only 2024 general results file on the county page is 'NOVEMBER 5TH 2024 PRECINCT BY PRECINCT ELECTION RESULTS' (scan, PDF CreationDate 2025-07-08 15:49:54 UTC, Last-Modified Thu, 05 Feb 2026 14:43:37 GMT); no election-night file survives. Wayback harvest (target co.haskell.tx.us) found no election-night captures; web.archive.org unreachable from this session for the current host. Rule 43: UNDETERMINED."
d['sources'] += [
 src('https://www.haskellcountytx.gov/page/haskell.Elections', 'fetch_module', '95eed95d697e9bada393bb55f132a88de5dc67d3afd5581893e2cbcc4c535ce4', "MARCH 3, 2026 REPUBLICAN UNOFFICIAL RESULTS; MARCH 3, 2026 DEMOCRATIC UNOFFICIAL RESULTS; REPBUBLICAN PRECINCT BY PRECINCT 3.3.26; MAY 26, 2026 REPUBLICAN UNOFFICIAL RESULTS; MAY 26, 2026 DEMOCRATIC UNOFFICIAL RESULTS; PRIMARY RUNOFF RESULTS FOR PRECINCT BY PRECINCT/ REP AND DEM; NOVEMBER 5TH 2024 PRECINCT BY PRECINCT ELECTION RESULTS", 'list of result files per election'),
 src(u_dp, 'fetch_module', '6137815f96bbb9fb31a85b9cc9ea0ae3383d12303ad1dadfc119a20162ee25f8', "Election Unofficial Results Report 2026 DEMOCRATIC PRIMARY ELECTION March 03, 2026 HASKELL County ... Election Day Count ... JAMES TALARICO 3 33 17 36 53 [Last-Modified Wed, 04 Mar 2026 05:16:53 GMT; CreationDate 2026-03-04 05:00:07 UTC]", '2026_primary county totals uploaded on election night'),
 src(u_rp, 'fetch_module', '1b826c4588d34c5fa58ad3199c7d1964fa5ff4e63ff73b5fe0ada788fd277ee7', "Election Unofficial Results Report 2026 REPUBLICAN PRIMARY ELECTION ... JOHN CORNYN 11 202 215 213 428 [CreationDate 2026-03-04 06:06:29 UTC; Last-Modified Wed, 04 Mar 2026 13:54:56 GMT]", '2026_primary Republican county totals printed on election night'),
 src(u_rpp, 'fetch_module', '597033042e2238362a7cfcff8467bc78852b9e46277ac473ce0f465842c0b4e1', "[scan, Last-Modified Wed, 01 Apr 2026 20:44:30 GMT]", '2026_primary precinct numbers posted Apr 1'),
 src(u_dpp, 'fetch_module', '376fab3a38162f3b05a9271ca46b20600858d15f6e3c413dc7d9a88ee5cd1d9a', "[scan, Last-Modified Wed, 01 Apr 2026 20:43:36 GMT]", '2026_primary precinct numbers posted Apr 1'),
 src(u_rr, 'fetch_module', '627f863178a89c8dd44a3f21d4230282cdf5d6750ce3fbc40b723ac7512d0e6d', "(from page image) Election Unofficial Results Report 2026 REPUBLICAN PRIMARY RUNOFF ELECTION May 26, 2026 HASKELL County ... KEN PAXTON 15 125 133 140 273 [Last-Modified Wed, 27 May 2026 01:33:23 GMT]", '2026_runoff county totals uploaded on election night'),
 src(u_dr, 'fetch_module', '2301e9483e5dd7d040508e40a438b63d94b36e686923f16030ca0ed16a92a703', "(from page image) Election Unofficial Results Report 2026 DEMOCRATIC PRIMARY RUNOFF ELECTION ... VIKKI GOODWIN 0 12 2 12 14 [Last-Modified Wed, 27 May 2026 00:58:27 GMT]", '2026_runoff county totals uploaded 7:58 PM CDT'),
 src(u_rpct, 'fetch_module', 'd95c42410e8482c6f3caec70f977c92ec177dc9685dab4af16b3b5ae363fc230', "[scan, Last-Modified Mon, 29 Jun 2026 15:04:45 GMT]", '2026_runoff precinct numbers posted Jun 29'),
 src(u_24, 'fetch_module', 'f2f55f63755248b3ef0f4e4a8892366f0b751b4d2d0c1365a47fb05f04ab5743', "[scan, CreationDate 2025-07-08, Last-Modified Thu, 05 Feb 2026 14:43:37 GMT]", '2024_general only post-election file'),
]
d['tag_rationale'] = '2026_primary and 2026_runoff are LATER (check 2: SOS-format county totals uploaded on election night, precinct files uploaded weeks later); 2024_general UNDETERMINED. Two LATER results give COUNTY_ONLY_PRECINCT_AT_CANVASS.'
note(d, "Settled the verifier disagreement (TARGETED3_BRIEF 2c) from files opened in this pass: the county host www.haskellcountytx.gov now loads through the fetch module. 2026_primary UNDETERMINED to LATER (check 2; Democratic county-totals report uploaded 2026-03-03 23:16 CT, precinct-by-precinct files uploaded 2026-04-01). 2026_runoff UNDETERMINED to LATER (check 2; county totals uploaded 19:58 and 20:33 CT, precinct file uploaded 2026-06-29). 2024_general stays UNDETERMINED (only a July 2025 scan). Agrees with the verifier. Wayback harvest had no captures (it targeted the old host co.haskell.tx.us); web.archive.org was unreachable from this session (robots check connection reset). No sweep file (sweep pending/not covering this county).")
save('Haskell', d)

# ---------------- Bosque ----------------
d = load('Bosque')
B = 'https://www.bosquecounty.gov/'
d['results_url'] = B + '198/Recent-Elections'
d['platform'] = 'county_pdfs'
d['host'] = 'www.bosquecounty.gov'
d['evidence_url'] = B + 'DocumentCenter/View/2515'
d['evidence_snapshot_timestamp'] = ''
d['precinct_first_seen_local_time'] = '2024-11-05 20:53 CT'
d['elections']['2024_general'] = el('END', '2', '', '2024-11-05 20:53 CT', '1', B + 'DocumentCenter/View/587/Pct-1-Iredell-PDF',
    "County page '2024 November 5 General Election' lists 'Pct 1 Iredell (PDF)' ... 'Pct 11 Cayote (PDF)', 'Unofficial Grand Totals (PDF)' and, separately, '... Official Results 11.05.24'. 'Pct 1 Iredell' (page image): 'Summary Results Report 2024 General Election November 5, 2024 ... UNOFFICIAL RESULTS PCT 1 IREDELL Bosque County', columns 'TOTAL VOTE % Absentee Early Voting Election Day', 'REP Donald J. Trump/JD Vance 534 90.36% 10 305 219', footer 'Precinct Summary - 11/05/2024 8:53 PM'; scan CreationDate 2024-11-06 03:13:41 UTC (9:13 PM CST). CivicPlus DocumentCenter sends no Last-Modified, so no upload time; the printed run time is on election night (rule 47). Corroborated by check 3: the archived election-night copy of the county's old elections page (Wayback 20241106052529 = 2024-11-05 23:25:29 CST, and again 02:16:09 CST) already links 'Unofficial Reconciliation 11.5.24', 'Unofficial Grand Totals', 'Pct 1 Iredell' ... 'Pct 11 Cayote', 'Early Voting and Ballot by Mail' (wp-content/uploads/2024/11/Pct-1-Iredell.pdf etc.). One election-night release seen, so END.")
d['elections']['2026_primary'] = el('END', '2', '', '2026-03-03 21:32 CT', '1', B + 'DocumentCenter/View/2235',
    "County page '2026 March 3rd Primary Election', tab 'UNOFFICIAL RESULTS', lists 'Grand Totals Unofficial Results', 'Early Voting Unofficial Results 03.03.2026' and 'Pct. 1 Iredell Unofficial Results' ... 'Pct. 11 Cayote Unofficial Results'. 'Pct. 1 Iredell Unofficial Results' (page image): 'Precinct Summary Results Report 2026 Primary Election March 3, 2026 UNOFFICIAL RESULTS IREDELL PCT 1 Bosque County, Texas', 'Ken Paxton 117 48.75% 2 48 67' (Absentee, Early Voting, Election Day), footer 'Precinct Summary - 03/03/2026 9:32 PM'; scan CreationDate 2026-03-04 03:44:05 UTC (9:44 PM CST). DocumentCenter gives no Last-Modified, so the printed run time on election night decides (rule 47).")
d['elections']['2026_runoff'] = el('END', '2', '', '2026-05-26 20:34 CT', '1', B + 'DocumentCenter/View/2515',
    "County page '2026 May 26th Primary Runoff' lists 'Unofficial Grand Totals 05.26.26', 'Early Voting Unofficial Results 05.26.26', 'Unofficial Precinct Totals 05.26.26', 'Preliminary Election Reconciliation - Unofficial Totals 05.26.26'. 'Unofficial Precinct Totals 05.26.26' (page image): 'Precinct Summary Results Report 2026 Primary Runoff Election May 26, 2026 UNOFFICIAL RESULTS PRECINCT 1 - MERIDIAN (3) Bosque County, Texas', 'Ken Paxton 282 67.63% 10 129 143' (Absentee, Early Voting, Election Day), footer 'Precinct Summary - 05/26/2026 8:34 PM'; scan CreationDate 2026-05-27 02:11:38 UTC (9:11 PM CDT). No Last-Modified from DocumentCenter; printed run time on election night (rule 47).")
d['sources'] += [
 src(B + '199/2024-November-5-General-Election', 'fetch_module', '55b53b54987d767e77debefa80f098976178947e10598635b4cb79e3364f65b8', "Pct 1 Iredell (PDF) ... PCT 9 Clifton (PDF); Unofficial Grand Totals (PDF); Unofficial Reconciliation 11.5.24 (PDF); Pct 1 Iredell Official Results 11.05.24 (PDF)", '2024_general file list'),
 src(B + 'DocumentCenter/View/587/Pct-1-Iredell-PDF', 'fetch_module', '837957ed3c03375b61f98249ab33da582ae3509d5f267b07b851dfe04f3290e5', "(page image) Summary Results Report 2024 General Election November 5, 2024 UNOFFICIAL RESULTS PCT 1 IREDELL ... REP Donald J. Trump/JD Vance 534 90.36% 10 305 219 ... Precinct Summary - 11/05/2024 8:53 PM [no Last-Modified header]", '2024_general precinct numbers printed on election night'),
 src(B + 'DocumentCenter/View/589/Unofficial-Grand-Totals-PDF', 'fetch_module', 'a684c6f9448614dd4557e8c34c0780b33d9cbe7d244545df2cb290a52159fb68', "[scan, CreationDate 2024-11-06 03:49:07 UTC]", '2024_general unofficial county totals'),
 src('phase1/wayback_snapshots/Bosque/2024_general_20241106052529_5ddaaf66ae2e.html', 'wayback_branch', '5ddaaf66ae2ebb016b742ac38a9f462c692bf9f1bee0d7c81025a54ba30266d7', "Unofficial Reconciliation 11.5.24 / Unofficial Grand Totals / Pct 1 Iredell / Pct 2 Walnut Springs / PCT 3 Meridian / ... / Pct 11 Cayote / Early Voting and Ballot by Mail (href .../bosquewebsite/wp-content/uploads/2024/11/Pct-1-Iredell.pdf)", 'archived election-night page (2024-11-05 23:25:29 CST) already links per-precinct unofficial files'),
 src('phase1/wayback_snapshots/Bosque/2024_general_20241106081609_f4348cd22bd7.html', 'wayback_branch', 'f4348cd22bd76f22eac9ad21bc090ce82139083797cf4d84d2410c18552896ce', "Unofficial Reconciliation 11.5.24 / Unofficial Grand Totals / Pct 1 Iredell ... Pct 11 Cayote", 'same list at 2024-11-06 02:16:09 CST'),
 src(B + '286/2026-March-3rd-Primary-Election', 'fetch_module', 'ed0fd50a87ff6f1ab40eb3ea6543f4138eddc0bf633c347d5860d7adafd7346b', "UNOFFICIAL RESULTS: Unofficial Reconciliation Totals; Grand Totals Unofficial Results; Early Voting Unofficial Results 03.03.2026; Pct. 1 Iredell Unofficial Results ... Pct. 11 Cayote Unofficial Results", '2026_primary file list'),
 src(B + 'DocumentCenter/View/2235', 'fetch_module', '6aefb57856687df1074eeadce1075e06bc6a168a53ee7e3d7214fae0ed995224', "(page image) Precinct Summary Results Report 2026 Primary Election March 3, 2026 UNOFFICIAL RESULTS IREDELL PCT 1 ... Ken Paxton 117 48.75% 2 48 67 ... Precinct Summary - 03/03/2026 9:32 PM", '2026_primary precinct numbers printed on election night'),
 src(B + '290/2026-May-26th-Primary-Runoff', 'fetch_module', '6af05a879bb3570d515a30dbaa4ef11773b78ca93be5933df67785fc6fcfac18', "Unofficial Grand Totals 05.26.26; Early Voting Unofficial Results 05.26.26; Unofficial Precinct Totals 05.26.26; Official Pct. by Pct. Totals 05.26.26", '2026_runoff file list'),
 src(B + 'DocumentCenter/View/2515', 'fetch_module', 'c1933d7670b8b5a6e420ad12486ab6de36539128dc3a00331da4cf4acb195221', "(page image) Precinct Summary Results Report 2026 Primary Runoff Election May 26, 2026 UNOFFICIAL RESULTS PRECINCT 1 - MERIDIAN (3) ... Ken Paxton 282 67.63% 10 129 143 ... Precinct Summary - 05/26/2026 8:34 PM", '2026_runoff precinct numbers printed on election night'),
]
d['tag_rationale'] = 'All three elections are END from check 2: unofficial per-precinct reports with election-day votes whose printed run times fall on election night, and DocumentCenter gives no upload time (rule 47); 2024 also corroborated by an election-night Wayback copy. Three END results give PRECINCT_END_OF_NIGHT.'
note(d, "The county moved to a CivicPlus site at www.bosquecounty.gov, now reachable (the earlier proxy block is gone). Its election pages list unofficial per-precinct reports for all three elections. 2024_general, 2026_primary, 2026_runoff UNDETERMINED to END (check 2, printed run times 2024-11-05 20:53, 2026-03-03 21:32, 2026-05-26 20:34 CT; DocumentCenter sends no Last-Modified, so no upload time contradicts). The Wayback harvest's two election-night captures of the old WordPress page (23:25 and 02:16 CST) already link the per-precinct files 'Pct 1 Iredell' to 'Pct 11 Cayote'. The DocumentCenter copies are migrated files; it was not possible to compare them with the archived WordPress originals because web.archive.org was unreachable (robots check connection reset). END rather than LIVE: per-precinct files may have been posted one by one, but no upload times show separate election-night releases. Old WP REST endpoint returns 404. No sweep file for this county.")
save('Bosque', d)

# ---------------- Parmer ----------------
d = load('Parmer')
W = 'https://parmercounty.texas.gov/index.php?rest_route=/wp/v2/media&after=%s&per_page=100'
w24 = W % '2024-11-05T12:00:00&before=2024-11-07T00:00:00'
w26p = W % '2026-03-03T12:00:00&before=2026-03-05T00:00:00'
w26r = W % '2026-05-26T12:00:00&before=2026-05-28T00:00:00'
U = 'https://parmercounty.texas.gov/wp-content/uploads/'
f24 = U + '2024/11/Unofficial-Results-General-Election-Nov.-5-2024.pdf'
f26p = U + '2026/03/Unoffical-3-3-2026-Primary.pdf'
f26r = U + '2026/05/Unoffical-Results-Runoff-5-26-26.pdf'
d['evidence_url'] = f26r
d['precinct_first_seen_local_time'] = '2026-05-26 21:08 CT'
d['elections']['2024_general'] = el('LATER', '2', '2024-11-05 21:43 CT', '2025-01-29 10:27 CT', '0', f24,
    "WordPress upload log (wp/v2/media, date_gmt equals date, so UTC) for 2024-11-05 12:00 to 2024-11-07 00:00 lists, on election night, only 'Unofficial Results General Election Nov. 5, 2024' (2024-11-06T03:43:44 = 9:43 PM CST) and 'Unofficial Election Reconciliation Nov. 5, 2024' (03:48:10 = 9:48 PM CST). The results file (Last-Modified Wed, 06 Nov 2024 03:43:44 GMT, matching) is county totals (page images): 'Summary Results Report TX Parmer County 241105 General 6110 November 5, 2024 UNOFFICIAL RESULTS Total Ballots 11-5-2024 Parmer County', 'REP Donald J. Trump/JD Vance 2,123', 'Precincts Reporting 7 of 7', footer 'Election Summary - 11/05/2024 9:27 PM'. No precinct report was uploaded that night; precinct pages ('Pct.101') appear only in the official file uploaded Wed, 29 Jan 2025 16:27:00 GMT.")
d['elections']['2026_primary'] = el('LATER', '2', '2026-03-03 21:58 CT', '', '0', f26p,
    "WordPress upload log for 2026-03-03 12:00 to 2026-03-05 00:00 UTC lists on election night only 'Unoffical 3-3-2026 Primary' (2026-03-04T03:58:19 = 9:58 PM CST; Last-Modified Wed, 04 Mar 2026 03:58:19 GMT; CreationDate D:20260303215351-06'00'). It holds a 'Preliminary Election Reconciliation - Unofficial Totals' page and county totals (page image): 'Summary Results Report Primary 2026 UNOFFICIAL RESULTS TX PARMER 260303 Primary 6110 March 3, 2026 Parmer County', 'Ken Paxton 427 37.20% 3 133 291', footer 'Election Summary - 03/03/2026 9:13 PM'. Next upload is the SOS Democratic report at 2026-03-04T15:52:56 UTC (next morning). No precinct report that night; the county's only later primary file is the official county-totals report (Mar 19), so precinct numbers were never published online by the county.")
d['elections']['2026_runoff'] = el('END', '2', '2026-05-26 21:08 CT', '2026-05-26 21:08 CT', '1', f26r,
    "WordPress upload log for 2026-05-26 12:00 to 2026-05-28 00:00 UTC lists 'Unoffical Results Runoff 5-26-26' at 2026-05-27T02:08:35 (9:08 PM CDT), with byte-identical re-uploads at 02:18:08, 02:51:39 and 12:26:29 UTC. The file (Last-Modified Wed, 27 May 2026 02:08:35 GMT, matching) has reconciliation and county-total pages, then pages headed 'Summary Results Report UNOFFICIAL PRECINCT RESULTS 2026 RUNOFF TX Parmer 260526 Primary Runoff 6110 May 26, 2026 Parmer County' for precincts 101, 201, 202, 301, 303, 401, 402; page image for '101': 'Ken Paxton 73 2 12 59' (TOTAL, Absentee, Early Voting, Election Day), footer 'Precinct Summary - 05/26/2026 7:53 PM'. Precinct numbers with election-day votes uploaded on election night once (re-uploads identical), so END.")
d['sources'] += [
 src(w24, 'fetch_module', '5a4fd879c8fba8369e4747cdecb4af90506f071076a950a0c67cba63532d0908', '2024-11-06T03:48:10 Unofficial Election Reconciliation Nov. 5, 2024; 2024-11-06T03:43:44 Unofficial Results General Election Nov. 5, 2024; 2024-11-05T17:14:05 April 29, 2019 Meeting Minutes; 2024-11-05T15:50:32 Screenshot', 'complete WP upload log over 2024 election night'),
 src(f24, 'fetch_module', '92ec90c0256740458be31b72f13aec6477de09ac3d2e98a1b3fe273f8bfb14d6', '(page image) Summary Results Report TX Parmer County 241105 General 6110 ... UNOFFICIAL RESULTS Total Ballots 11-5-2024 ... Precincts Reporting 7 of 7 ... Election Summary - 11/05/2024 9:27 PM [Last-Modified Wed, 06 Nov 2024 03:43:44 GMT]', '2024_general county totals uploaded election night'),
 src(w26p, 'fetch_module', '893f97a79771017f15a3d1945043e14783c2a4f905eb6bc81bbb2c2d67400ddf', '2026-03-04T22:39:57 Image_003; 2026-03-04T15:52:56 ELECTION-UNOFFICIAL-RESULT-REPORT_030426; 2026-03-04T14:44:37 Notice of Hand Count; 2026-03-04T14:44:33 David-White-4-2 2; 2026-03-04T03:58:19 Unoffical 3-3-2026 Primary', 'complete WP upload log over 2026 primary night'),
 src(f26p, 'fetch_module', 'ee162b0ff5cfad92e18130b3d0d7db7778a098082e109ca7918a2439a2e42304', '(page image) Summary Results Report Primary 2026 UNOFFICIAL RESULTS TX PARMER 260303 Primary 6110 ... Ken Paxton 427 37.20% 3 133 291 ... Election Summary - 03/03/2026 9:13 PM [Last-Modified Wed, 04 Mar 2026 03:58:19 GMT]', '2026_primary county totals uploaded election night'),
 src(w26r, 'fetch_module', '357e6989953fb3f5fa2a80931742691f17d0cca323d09fd419922b521ee4f763', '2026-05-27T12:26:29 Unoffical Results Runoff 5-26-26 (-3); 2026-05-27T02:51:39 (-2); 2026-05-27T02:18:08 (-1); 2026-05-27T02:08:35 Unoffical Results Runoff 5-26-26; 2026-05-26T20:39:46 Minutes 5-12-26', 'complete WP upload log over 2026 runoff night'),
 src(f26r, 'fetch_module', '4b1771b961054e2dfd36ebcccd36f16d6e3b548b26213d0bfabe387d0e0c5be7', '(page image) Summary Results Report UNOFFICIAL PRECINCT RESULTS 2026 RUNOFF TX Parmer 260526 Primary Runoff 6110 ... 101 ... Ken Paxton 73 2 12 59 ... Precinct Summary - 05/26/2026 7:53 PM [Last-Modified Wed, 27 May 2026 02:08:35 GMT]', '2026_runoff precinct numbers uploaded election night'),
]
d['tag_rationale'] = '2024_general and 2026_primary are LATER (check 2: complete WordPress upload logs show only county-totals files uploaded on election night); 2026_runoff is END (precinct report uploaded 9:08 PM CDT). Two LATER results give COUNTY_ONLY_PRECINCT_AT_CANVASS.'
note(d, "WordPress upload log (index.php?rest_route=/wp/v2/media; the /wp-json/ path returns the HTML home page) found election-night uploads the earlier passes missed: the files are no longer linked from the Elections page. 2024_general UNDETERMINED to LATER (check 2; county totals uploaded 21:43 CT, no precinct upload that night). 2026_primary UNDETERMINED to LATER (check 2; county totals uploaded 21:58 CT, no precinct upload that night). 2026_runoff UNDETERMINED to END (check 2; unofficial file with per-precinct pages uploaded 21:08 CT). Note the runoff PDF CreationDate D:20260526205712-06'00' is 49 minutes after the 21:08 CDT upload if read literally; the scanner apparently ignores daylight time (20:57 CDT wall clock), and the server upload time decides. Wayback harvest had no captures (2024 CDX connection refused). No sweep file.")
save('Parmer', d)

# ---------------- Clay ----------------
d = load('Clay')
C = 'https://www.claycountytx.net/_files/ugd/cb6725_'
d['elections']['2026_runoff']['fact'] = "Under 'May 26 Primary Run-Off' the county page links 'Early Voting.pdf', 'Elec Day.pdf', 'Totals.pdf', 'Recon Official Final' and others. All three results files are scans made after the canvass: 'Elec Day.pdf' ('Election Summary Results Report UNOFFICIAL RESULTS Election Day Canvass 2026 Primary Runoff Election', footer 'Election Summary - 06/01/2026 01:26PM', Last-Modified Tue, 02 Jun 2026 14:53:00 GMT), 'Totals.pdf' (county totals plus 'Precinct Summary Results Report ... Combined Pct Canvass PCT 1, 8, 9, 15, 20', footer 'Precinct Summary - 06/01/2026 01:27PM', Last-Modified Tue, 02 Jun 2026 14:53:15 GMT), 'Early Voting.pdf' (Last-Modified Tue, 02 Jun 2026 14:51:18 GMT). No election-night file survives, so UNDETERMINED (rule 43). Wayback harvest found no election-night captures of claycountytx.net."
d['sources'] += [
 src('https://www.claycountytx.net/electionsadmin', 'fetch_module', '863c2f3a5dc15184ae4a2718c9ad888f664fd63e60feeebe11b8bb4aaf0ee81f', 'May 26 Primary Run-Off / Early Voting.pdf / Elec Day.pdf / Totals.pdf / Election Notice / Rep Hand Count / Dem Hand Count / Recon. Votes Cast / Canv. Notice- DEM / Notice HandCount / Testing Notice / Recon Official Final', '2026_runoff file list'),
 src(C + 'f61abee4bf0240b78477aecd84666421.pdf', 'fetch_module', '7410e30ed306ee9675a9022e55291ff3c166cf88c22d5d99c95084c6302352fc', 'Election Summary Results Report UNOFFICIAL RESULTS Election Day Canvass 2026 Primary Runoff Election ... Election Summary - 06/01/2026 01:26PM [Last-Modified Tue, 02 Jun 2026 14:53:00 GMT]', '2026_runoff file made after election night'),
 src(C + '774ddb4662db43098b799223ae42eadd.pdf', 'fetch_module', '33cebbdf300ad3676a8e7e4e61045c9de725ac790d0e2012d37db56c52a28628', 'Precinct Summary Results Report UNOFFICIAL RESULTS 2026 Primary Runoff Election Combined Pct Canvass PCT 1, 8, 9, 15, 20 Precinct Summary - 06/01/2026 01:27PM [Last-Modified Tue, 02 Jun 2026 14:53:15 GMT]', '2026_runoff precinct numbers Jun 1-2'),
 src(C + '282d0d1cef4a473e9c85b486755aaf62.pdf', 'fetch_module', '844c9da1063d194aeb0efa0c3be7f6fb8d9cd575af07d5326ddd3244a82673bf', 'UNOFFICIAL RESULTS ... 2026 Primary Runoff Election ... ABBM Canvass [Last-Modified Tue, 02 Jun 2026 14:51:18 GMT]', '2026_runoff early voting file after election night'),
]
note(d, "Found the runoff files the first pass missed (section 'May 26 Primary Run-Off' on the elections page): 'Early Voting.pdf', 'Elec Day.pdf', 'Totals.pdf' were all printed 2026-06-01 and uploaded 2026-06-02, so 2026_runoff stays UNDETERMINED (no election-night file). The Wayback harvest has no election-night captures for any of the three elections. No sweep file. Tag unchanged (LIVE 2024, LATER 2026 primary).")
save('Clay', d)

# ---------------- notes only ----------------
for c, s in [
 ('Aransas', "Tried: Wayback harvest (no election-night captures for aransascountytx.gov in any window); one web search (located only sample ballots in /electionadmin/e-docs/ and a news link that returns 404); /electionadmin/e-docs/ also returns the Incapsula challenge page, not circumvented. No sweep file. Nothing changed."),
 ('Runnels', "Tried: Wayback harvest (no captures for co.runnels.tx.us in 2024 and 2026 primary windows; runoff CDX timed out; harvest did not cover runnelscounty.org); web.archive.org unreachable from this session; re-read the Elections page link list (only November 2026 items, a May 2025 bond precinct results file, and a 2020 L&A notice); one web search found no Runnels results page or third-party precinct results. No sweep file. Nothing changed."),
 ('Knox', "Tried: Wayback harvest (no election-night captures for knoxcountytexas.org); re-checked the site navigation (no results or archive page); one web search found no Knox County TX results page or election-night precinct publication (only out-of-state Knox counties and scanned weekly newspapers). No sweep file. Nothing changed."),
 ('Foard', "Tried: Wayback harvest (no Foard folder on the wayback-data branch); web.archive.org unreachable from this session; one web search found no third-party election-night precinct results and no other county results page. The verifier agrees all three elections are UNDETERMINED. No sweep file. Nothing changed."),
]:
    d = load(c); note(d, s); save(c, d)
