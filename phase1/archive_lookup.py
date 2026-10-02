"""Targeted archive search beyond the Wayback Machine (runs on GitHub Actions).

For each target URL, list mementos from the Memento TimeTravel aggregator (which
searches many public web archives) and from archive.today, keep those whose
capture time falls between 7 PM election day and 9 AM the next morning (county
local), and save the archive.today captures' raw bytes. Wayback captures found
this way are listed only; Wayback content is fetched by the Wayback job.

    python -m phase1.archive_lookup --targets phase1/targeted/targets.json --out phase1/targeted/archives
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from txprecinct.fetch import FetchClient  # noqa: E402

# 7 PM election day to 9 AM next day, as UTC (Central: CST -6 for Nov and Mar, CDT -5 for May).
WINDOWS_UTC = {
    "2024_general": (datetime(2024, 11, 6, 1, tzinfo=timezone.utc), datetime(2024, 11, 6, 15, tzinfo=timezone.utc)),
    "2026_primary": (datetime(2026, 3, 4, 1, tzinfo=timezone.utc), datetime(2026, 3, 4, 15, tzinfo=timezone.utc)),
    "2026_runoff": (datetime(2026, 5, 27, 0, tzinfo=timezone.utc), datetime(2026, 5, 27, 14, tzinfo=timezone.utc)),
}
LINK_RE = re.compile(r'<([^>]+)>;\s*rel="([^"]*memento[^"]*)";\s*datetime="([^"]+)"')


def which_window(dt: datetime) -> str | None:
    for k, (a, b) in WINDOWS_UTC.items():
        if a <= dt <= b:
            return k
    return None


def parse_linkformat(text: str) -> list[dict]:
    out = []
    for uri, rel, dts in LINK_RE.findall(text):
        dt = datetime.strptime(dts, "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone.utc)
        out.append({"uri": uri, "datetime_utc": dt.isoformat(), "window": which_window(dt)})
    return out


def lookup(client: FetchClient, url: str) -> dict:
    res = {"url": url, "sources": {}}
    tm = f"https://timetravel.mementoweb.org/timemap/link/{url}"
    r = client.get(tm, purpose="targeted:memento")
    res["sources"]["memento_aggregator"] = {"timemap": tm, "ok": r.ok, "error": r.error,
                                            "content_hash": r.content_hash,
                                            "mementos": parse_linkformat(r.text()) if r.ok else []}
    at = f"https://archive.ph/timemap/{url}"
    r = client.get(at, purpose="targeted:archive.today")
    res["sources"]["archive_today"] = {"timemap": at, "ok": r.ok, "error": r.error, "content_hash": r.content_hash,
                                       "mementos": parse_linkformat(r.text()) if r.ok else []}
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    targets = json.loads(Path(a.targets).read_text())
    out = Path(a.out)
    client = FetchClient(agent="archive-lookup")
    for county, spec in targets.items():
        cdir = out / county.replace(" ", "_")
        cdir.mkdir(parents=True, exist_ok=True)
        results = []
        for url in spec["urls"]:
            res = lookup(client, url)
            for src, info in res["sources"].items():
                for m in info["mementos"]:
                    if m["window"] and "web.archive.org" not in m["uri"] and "archive.org/wayback" not in m["uri"]:
                        r = client.get(m["uri"], purpose=f"targeted:{src}:{county}")
                        m.update(ok=r.ok, error=r.error, content_hash=r.content_hash)
                        if r.ok:
                            fn = f"{m['window']}_{m['datetime_utc'][:19].replace(':', '')}_{r.content_hash[:12]}.html"
                            (cdir / fn).write_bytes(r.body)
                            m["saved_as"] = f"{cdir.name}/{fn}"
            results.append(res)
        (cdir / "archives_index.json").write_text(json.dumps({"county": county, "generated_utc":
                                                              time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                                              "lookups": results}, indent=2))
        n = sum(1 for r in results for s in r["sources"].values() for m in s["mementos"] if m["window"])
        print(json.dumps({"county": county, "mementos_in_windows": n}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
