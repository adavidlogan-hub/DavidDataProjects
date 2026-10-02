"""Harvest Wayback Machine captures of county results pages for election-night windows.

Runs where web.archive.org is reachable (a GitHub Actions runner or the Windows
laptop). Uses the shared fetch module, so the archive.org rate limit
(1 request per 2 s, backoff on 429) and the cache apply.

For each target in phase1/wayback_targets.json:
  1. CDX listing per election window (7pm to 3am Central), collapsed by digest so
     only captures whose content changed are listed, images/css/js excluded.
  2. Raw replay (id_) of each distinct capture, up to a per-county cap, saved
     verbatim under phase1/wayback_snapshots/<County>/.
Nothing is parsed or altered here; analysis happens later on the saved bytes.

    python -m phase1.wayback_harvest --agent wayback-harvest [--only Harris,Dallas] [--cap 120]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from phase1.wayback_probe import WINDOWS, to_central  # noqa: E402
from txprecinct.fetch import FetchClient  # noqa: E402

ROOT = Path(__file__).resolve().parent
TARGETS = ROOT / "wayback_targets.json"
SNAP_DIR = ROOT / "wayback_snapshots"
EXCLUDE_MIME = ("image/.*", "text/css", "application/javascript", "text/javascript", "application/x-javascript",
                "font/.*", "application/font.*", "application/x-font.*", "video/.*", "audio/.*", "warc/revisit")
EXT = {"text/html": "html", "application/json": "json", "application/pdf": "pdf", "text/csv": "csv",
       "text/plain": "txt", "application/xml": "xml", "text/xml": "xml"}


def cdx_url(prefix: str, frm: str, to: str, match_type: str, original_regex: str = "") -> str:
    filters = "".join(f"&filter=!mimetype:{quote(m, safe='')}" for m in EXCLUDE_MIME)
    if original_regex:
        filters += f"&filter=original:{quote(original_regex, safe='')}"
    return (f"https://web.archive.org/cdx/search/cdx?url={quote(prefix, safe='')}&matchType={match_type}"
            f"&from={frm}&to={to}&output=json&fl=timestamp,original,statuscode,mimetype,digest,length"
            f"&filter=statuscode:200{filters}&collapse=digest&limit=5000")


EXTENDED_WINDOWS = {  # 7 PM election day to 9 AM next day, Central, as UTC
    "2024_general": ("20241106010000", "20241106150000", -6),
    "2026_primary": ("20260304010000", "20260304150000", -6),
    "2026_runoff": ("20260527000000", "20260527140000", -5),
}


def harvest_county(client: FetchClient, target: dict, cap: int, snap_dir: Path = SNAP_DIR,
                   windows: dict = WINDOWS) -> dict:
    county = target["county"]
    out_dir = snap_dir / county.replace(" ", "_")
    out_dir.mkdir(parents=True, exist_ok=True)
    index = {"county": county, "targets": target["url_prefixes"], "harvested_at_utc":
             time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "windows": {}}
    fetched = 0
    for wname, (frm, to, off) in windows.items():
        win_fetched = 0
        win = {"cdx": [], "captures": []}
        seen_digest = set()
        for prefix in target["url_prefixes"]:
            mt = target.get("match_type", "prefix")
            url = cdx_url(prefix, frm, to, mt, target.get("original_regex", ""))
            r = client.get(url, purpose=f"wayback_cdx:{county}:{wname}")
            win["cdx"].append({"url": url, "ok": r.ok, "error": r.error, "content_hash": r.content_hash})
            if not r.ok:
                continue
            rows = json.loads(r.text() or "[]")
            if not rows:
                continue
            assert rows[0] == ["timestamp", "original", "statuscode", "mimetype", "digest", "length"], rows[0]
            for ts, orig, status, mime, digest, length in rows[1:]:
                if digest in seen_digest:
                    continue
                seen_digest.add(digest)
                win["captures"].append({"timestamp_utc": ts, "local": to_central(ts, off), "original": orig,
                                        "mimetype": mime, "digest": digest, "length": length})
        win["captures"].sort(key=lambda c: c["timestamp_utc"])
        for cap_rec in win["captures"]:
            if win_fetched >= cap:
                cap_rec["skipped"] = "per-window cap reached"
                continue
            replay = f"https://web.archive.org/web/{cap_rec['timestamp_utc']}id_/{cap_rec['original']}"
            r = client.get(replay, purpose=f"wayback_replay:{county}:{wname}")
            fetched += 1
            win_fetched += 1
            cap_rec.update(replay_url=replay, ok=r.ok, error=r.error, content_hash=r.content_hash)
            if r.ok:
                ext = EXT.get((cap_rec["mimetype"] or "").split(";")[0], "bin")
                fname = f"{wname}_{cap_rec['timestamp_utc']}_{r.content_hash[:12]}.{ext}"
                p = out_dir / fname
                if not p.exists():
                    p.write_bytes(r.body)  # raw bytes exactly as served by the archive
                cap_rec["saved_as"] = f"{out_dir.name}/{fname}"
        index["windows"][wname] = win
    index["replays_fetched"] = fetched
    (out_dir / "index.json").write_text(json.dumps(index, indent=2))
    return {w: len(v["captures"]) for w, v in index["windows"].items()} | {"replays": fetched}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", default="wayback-harvest")
    ap.add_argument("--only", default="")
    ap.add_argument("--cap", type=int, default=60, help="max replays per county per window")
    ap.add_argument("--batch", default="", help="i/n: harvest every n-th target starting at i (0-based)")
    ap.add_argument("--targets-file", default=str(TARGETS))
    ap.add_argument("--snap-dir", default=str(SNAP_DIR))
    ap.add_argument("--extended", action="store_true", help="7 PM to 9 AM windows instead of 7 PM to 3 AM")
    a = ap.parse_args(argv)
    targets = json.loads(Path(a.targets_file).read_text())
    if isinstance(targets, dict):  # targeted format: {county: {"wayback_prefixes": [...]}}
        targets = [{"county": c, "url_prefixes": v["wayback_prefixes"], "match_type": "prefix"}
                   for c, v in targets.items()]
    if a.batch:
        i, n = (int(x) for x in a.batch.split("/"))
        assert 0 <= i < n, f"bad --batch {a.batch}"
        targets = targets[i::n]
    only = {c.strip() for c in a.only.split(",") if c.strip()}
    client = FetchClient(agent=a.agent)
    t0 = time.time()
    for t in targets:
        if only and t["county"] not in only:
            continue
        assert t["url_prefixes"], f"{t['county']}: no url_prefixes"
        print(json.dumps({"county": t["county"], **harvest_county(
            client, t, a.cap, Path(a.snap_dir), EXTENDED_WINDOWS if a.extended else WINDOWS)}), flush=True)
    with client.store.connect() as con:
        blocked = con.execute("SELECT COUNT(*) FROM fetches WHERE host_class = 'archive' AND fetched_at >= ? "
                              "AND error = 'robots_disallowed_or_unreachable'", (t0,)).fetchone()[0]
    print(json.dumps({"elapsed_seconds": round(time.time() - t0, 1), "robots_blocked_requests": blocked}))
    # Loud failure: a robots.txt outage must not pass as "no captures".
    return 2 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
