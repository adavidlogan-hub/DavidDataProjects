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

# ---------------- Coryell
c='Coryell'; d=load(c)
M24="https://coryellcountytax.com/wp-json/wp/v2/media?after=2024-11-05T00:00:00&before=2024-11-08T00:00:00&per_page=100"
M26P="https://coryellcountytax.com/wp-json/wp/v2/media?after=2026-03-03T00:00:00&before=2026-03-06T00:00:00&per_page=100"
M26R="https://coryellcountytax.com/wp-json/wp/v2/media?after=2026-05-26T00:00:00&before=2026-05-29T00:00:00&per_page=100"
P24="https://coryellcountytax.com/wp-content/uploads/2024/11/Precinct-Results-final-unofficial-11-5-2024-09-15-38-PM.pdf"
C24="https://coryellcountytax.com/wp-content/uploads/2024/11/Cumulative-Results-11-5-2024-09-14-58-PM.pdf"
P26="https://coryellcountytax.com/wp-content/uploads/2026/03/rep-final-unofficial.pdf"
P26b="https://coryellcountytax.com/wp-content/uploads/2026/03/rep-pct.pdf"
P26d="https://coryellcountytax.com/wp-content/uploads/2026/03/dem-pct.pdf"
C26a="https://coryellcountytax.com/wp-content/uploads/2026/03/rep-1.pdf"
C26b="https://coryellcountytax.com/wp-content/uploads/2026/03/rep2.pdf"
C26c="https://coryellcountytax.com/wp-content/uploads/2026/03/rep3.pdf"
PR="https://coryellcountytax.com/wp-content/uploads/2026/05/final-unoff-pct-rep.pdf"
CR1="https://coryellcountytax.com/wp-content/uploads/2026/05/6-of-8-rep-1.pdf"
CR2="https://coryellcountytax.com/wp-content/uploads/2026/05/final-unofficial-rep-1.pdf"
d['elections']['2024_general'].update({"result":"END","check":"2","county_totals_first_seen":"2024-11-05 19:22 CT",
 "precinct_first_seen":"2024-11-05 21:41 CT","night_updates_with_precinct_numbers":"1","evidence_url":P24,
 "fact":"WordPress media library (wp-json/wp/v2/media) lists election-night uploads on 2024-11-05 (site time, date_gmt +6h): Cumulative-Results-11-5-2024-07-23-26-PM.pdf at 19:22:11, Cumulative-Results-11-5-2024-08-39-16-PM.pdf at 20:34:40, Cumulative-Results-11-5-2024-09-14-58-PM.pdf at 21:11:04, FINAL-UNOFFICIAL-11-05-2024.pdf (9-page scan) at 21:39:41, Precinct-Results-final-unofficial-11-5-2024-09-15-38-PM.pdf at 21:41:22. The precinct file reads 'Precinct Results Report Unofficial Results CORYELL COUNTY, TEXAS ... GENERAL ELECTION Polling Places Reporting 12 of 12 = 100.00% Run Time 9:15 PM 11/5/2024 Run Date 11/05/2024 ... 101 - BS4 ... Absentee Voting Early Voting Election Day Voting Total Donald J. Trump JD Vance REP 2 ... 145 ... 15 ... 162'; Last-Modified Wed, 06 Nov 2024 03:41:22 GMT (9:41 PM CST). The earlier uploads are Cumulative (county total) reports. One election-night precinct posting with the final unofficial count: END."})
d['elections']['2026_primary'].update({"result":"END","check":"2","county_totals_first_seen":"2026-03-03 19:04 CT",
 "precinct_first_seen":"2026-03-03 22:32 CT","night_updates_with_precinct_numbers":"1","evidence_url":P26b,
 "fact":"WordPress media library lists on 2026-03-03 (site time CST): rep-1.pdf/dem1.pdf at 19:04, rep2.pdf/dem-2.pdf at 20:28, rep3.pdf/dem3.pdf at 21:48 (all 'Cumulative Results Report ... Unofficial Results', run 7:07 PM, 8:32 PM, 9:51 PM), then rep-final-unofficial.pdf at 22:32:11, dem-pct.pdf at 22:33:51 and rep-pct.pdf at 22:34:36. rep-pct.pdf reads 'Precinct Results Report Unofficial Results CORYELL COUNTY, TEXAS ... PRIMARY ELECTION Polling Places Reporting 12 of 12 = 100.00% Run Time 9:52 PM 3/3/2026 Run Date 03/03/2026 ... 101 ... Absentee Voting Early Voting Election Day Voting Total Anna Bender 2 ... 12 ... 8 ... 22'; Last-Modified Wed, 04 Mar 2026 04:34:36 GMT (10:34 PM CST). rep-final-unofficial.pdf is the same 186-page precinct report (Last-Modified Wed, 04 Mar 2026 04:32:11 GMT). One election-night precinct posting (one report run, posted under two names) with the final unofficial count: END."})
d['elections']['2026_runoff'].update({"result":"END","check":"2","county_totals_first_seen":"2026-05-26 19:02 CT",
 "precinct_first_seen":"2026-05-26 20:58 CT","night_updates_with_precinct_numbers":"1","evidence_url":PR,
 "fact":"WordPress media library lists on 2026-05-26 (site time CDT): early-absentee-REP.pdf 19:02, 6-of-8-rep.pdf 20:10 and 6-of-8-rep-1.pdf 20:15 ('Cumulative Results Report ... Polling Places Reporting 6 of 8 ... Run Time 8:10 PM'), final-unofficial-rep.pdf 20:32, final-unofficial-rep-1.pdf 20:57 ('Cumulative Results Report ... 8 of 8 ... Run Time 8:33 PM'), final-unoff-pct-rep.pdf 20:58:36 and final-unoff-pct-dem.pdf 20:59:06. final-unoff-pct-rep.pdf reads 'Precinct Results Report Unofficial Results CORYELL COUNTY, TEXAS ... PRIMARY RUNOFF ELECTION Polling Places Reporting 8 of 8 = 100.00% Run Time 8:34 PM 5/26/2026 Run Date 05/26/2026 ... 101 ... John Cornyn 10 ... 98 ... 49 ... 157'; Last-Modified Wed, 27 May 2026 01:58:36 GMT (8:58 PM CDT). One election-night precinct posting with the final unofficial count: END."})
d['evidence_url']=PR; d['precinct_first_seen_local_time']="2024-11-05 21:41 CT"
d['sources']+= [
 src(M24,"2024-11-05T21:41:22 ... Precinct-Results-final-unofficial-11-5-2024-09-15-38-PM.pdf; 2024-11-05T21:11:04 ... Cumulative-Results-11-5-2024-09-14-58-PM.pdf; 2024-11-05T20:34:40 ... Cumulative-Results-11-5-2024-08-39-16-PM.pdf; 2024-11-05T19:22:11 ... Cumulative-Results-11-5-2024-07-23-26-PM.pdf","2024 general election-night upload times (WordPress media date; date_gmt is +6h)"),
 src(P24,"Precinct Results Report Unofficial Results CORYELL COUNTY, TEXAS ... Polling Places Reporting 12 of 12 = 100.00% Run Time 9:15 PM 11/5/2024 Run Date 11/05/2024 (Last-Modified Wed, 06 Nov 2024 03:41:22 GMT)","2024 general precinct report printed and uploaded on election night"),
 src(C24,"Cumulative Results Report CORYELL COUNTY, TEXAS Unofficial Results ... Run Time 9:14 PM 11/5/2024 (Last-Modified Wed, 06 Nov 2024 03:11:04 GMT)","2024 general county totals before the precinct report"),
 src(M26P,"2026-03-03T22:34:36 rep-pct; 22:33:51 dem-pct; 22:32:11 rep-final-unofficial; 22:31:23 dem-final-unofficial; 21:48:47 rep3; 20:28:35 rep2; 19:04:40 rep-1 (date_gmt 2026-03-04T04:34:36 etc.)","2026 primary election-night upload times"),
 src(P26b,"Precinct Results Report Unofficial Results CORYELL COUNTY, TEXAS ... Polling Places Reporting 12 of 12 = 100.00% Run Time 9:52 PM 3/3/2026 Run Date 03/03/2026 (Last-Modified Wed, 04 Mar 2026 04:34:36 GMT)","2026 primary precinct report printed and uploaded on election night"),
 src(P26,"Precinct Results Report Unofficial Results ... Run Time 9:52 PM 3/3/2026 (PDF Title Count_PrecinctResults, 186 pages; Last-Modified Wed, 04 Mar 2026 04:32:11 GMT)","same precinct report uploaded at 10:32 PM CST"),
 src(P26d,"Precinct Results Report Unofficial Results ... Run Time 9:53 PM 3/3/2026 (Last-Modified Wed, 04 Mar 2026 04:33:51 GMT)","Democratic precinct report on election night"),
 src(C26a,"Cumulative Results Report ... Unofficial Results ... Precincts Reporting 0 of 16 ... Run Time 7:07 PM 3/3/2026 (Last-Modified Wed, 04 Mar 2026 01:04:40 GMT)","earlier updates were county totals"),
 src(C26b,"Cumulative Results Report ... Run Time 8:32 PM 3/3/2026 (Last-Modified Wed, 04 Mar 2026 02:28:35 GMT)","county totals update"),
 src(C26c,"Cumulative Results Report ... Polling Places Reporting 12 of 12 ... Run Time 9:51 PM 3/3/2026 (Last-Modified Wed, 04 Mar 2026 03:48:47 GMT)","county totals update"),
 src(M26R,"2026-05-26T20:58:36 final-unoff-pct-rep.pdf; 20:59:06 final-unoff-pct-dem.pdf; 20:57:24 final-unofficial-rep-1.pdf; 20:32:40 final-unofficial-rep.pdf; 20:15:22 6-of-8-rep-1.pdf; 20:10:08 6-of-8-rep.pdf; 19:02:12 early-absentee-REP.pdf (date_gmt +5h)","2026 runoff election-night upload times"),
 src(PR,"Precinct Results Report Unofficial Results CORYELL COUNTY, TEXAS ... PRIMARY RUNOFF ELECTION Polling Places Reporting 8 of 8 = 100.00% Run Time 8:34 PM 5/26/2026 Run Date 05/26/2026 (Last-Modified Wed, 27 May 2026 01:58:36 GMT)","2026 runoff precinct report printed and uploaded on election night"),
 src(CR1,"Cumulative Results Report ... Polling Places Reporting 6 of 8 = 75.00% Run Time 8:10 PM 5/26/2026 (Last-Modified Wed, 27 May 2026 01:15:22 GMT)","runoff county totals update before precinct report"),
 src(CR2,"Cumulative Results Report ... Polling Places Reporting 8 of 8 = 100.00% Run Time 8:33 PM 5/26/2026 (Last-Modified Wed, 27 May 2026 01:57:24 GMT)","runoff final county totals"),
]
save(c,d,"Targeted pass 3 2026-10-02 (targeted3-B): new angle, the county WordPress site's public media library (wp-json/wp/v2/media filtered by date) lists every upload with its time, including election-night files no longer linked from the results pages. All three elections now END by check 2: county totals (Cumulative) posted from about 7 PM, then one Unofficial Precinct Results Report with the final count, printed and uploaded on election night (2024 general 9:15 PM printed / 9:41 PM uploaded; 2026 primary 9:52 PM / 10:32 PM; 2026 runoff 8:34 PM / 8:58 PM). Upload times agree between the media library date and the file's Last-Modified header. PDF CreationDate runs about 3 to 4 minutes ahead of the web server clock (for example rep-1.pdf created 01:08 UTC, uploaded 01:04 UTC), so printed times are taken from the report text. Wayback check 3 for coryellcountytax.com found 0 captures; sweep pending.",
 "All three elections are END from check 2 (an Unofficial Precinct Results Report printed and uploaded once on each election night, after county-total updates), so the tag is PRECINCT_END_OF_NIGHT; confidence med because check 2 had both printed run time and server upload time on election night.")
