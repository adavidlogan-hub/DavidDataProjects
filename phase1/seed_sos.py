"""Build the 254-county seed table from two TX SOS pages fetched through the shared client.

  county.shtml : county election officials (title, name, address, email, phone, fax)
  links.shtml  : county web sites ("Only counties with publicized links are provided")

Values are copied as shown on the SOS pages (whitespace collapsed, HTML entities
decoded); nothing is inferred. Output: data/seed_counties.csv and
data/sos_officials_parsed.json (every office entry, including counties with more
than one listed office).

    python -m phase1.seed_sos
"""
from __future__ import annotations

import csv
import html
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from txprecinct.fetch import FetchClient  # noqa: E402

OFFICIALS_URL = "https://www.sos.state.tx.us/elections/voter/county.shtml"
LINKS_URL = "https://www.sos.state.tx.us/elections/voter/links.shtml"
DATA = Path(__file__).resolve().parent.parent / "data"
PHONE_RE = re.compile(r"^\(?\d{3}\)?[\s.-]*\d{3}[\s.-]*\d{4}")
EXPECTED_COUNTIES = 254


DASHES = {chr(0x2013): "-", chr(0x2014): "-"}


def deliverable_text(value: str) -> tuple[str, bool]:
    """Deliverables may not contain en or em dashes. Replace with a plain hyphen and report
    whether anything changed; the exact source bytes stay in the cache under the page hash."""
    out = value
    for k, v in DASHES.items():
        out = out.replace(k, v)
    return out, out != value


def normalize_entry(e: dict) -> dict:
    changed = False
    out = {}
    for k, v in e.items():
        if isinstance(v, str):
            v, c = deliverable_text(v)
        elif isinstance(v, list):
            pairs = [deliverable_text(x) for x in v]
            v, c = [x for x, _ in pairs], any(c for _, c in pairs)
        else:
            c = False
        out[k] = v
        changed = changed or c
    out["dash_normalized"] = changed
    return out


def clean(s: str) -> str:
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return " ".join(html.unescape(s).split())


CANONICAL = {"Mcculloch": "McCulloch", "Mclennan": "McLennan", "Mcmullen": "McMullen", "Dewitt": "DeWitt",
             "De Witt": "DeWitt"}


def county_key(name: str) -> str:
    name = clean(name).upper().replace(" COUNTY", "").strip()
    key = " ".join(w.capitalize() for w in name.split())
    return CANONICAL.get(key, key)


def parse_officials(page: str) -> list[dict]:
    entries = []
    for dl in re.findall(r"<dl>(.*?)</dl>", page, flags=re.S | re.I):
        dt = re.search(r"<dt>(.*?)</dt>", dl, flags=re.S | re.I)
        if not dt or "COUNTY" not in clean(dt.group(1)).upper():
            continue
        county = county_key(dt.group(1))
        dds = re.findall(r"<dd>(.*?)</dd>", dl, flags=re.S | re.I)
        rec = {"county": county, "office_title": "", "official": "", "address": [], "email": "",
               "abbm_email": "", "phone": "", "fax": "", "other": []}
        for i, dd in enumerate(dds):
            # Some entries pack several lines into one <dd> separated by <br>; treat each line alike.
            for j, raw in enumerate(re.split(r"<br\s*/?>", dd, flags=re.I)):
                text = clean(raw)
                mail = re.search(r'mailto:([^"\s?]+)', raw)
                if mail and "Application" in text:
                    rec["abbm_email"] = mail.group(1).strip()
                elif mail:
                    rec["email"] = rec["email"] or mail.group(1).strip()
                elif text.upper().startswith("FAX"):
                    rec["fax"] = text.split(":", 1)[-1].strip()
                elif PHONE_RE.match(text):
                    rec["phone"] = rec["phone"] or text
                elif i == 0 and j == 0:
                    rec["office_title"] = text
                elif i == 1 and j == 0:
                    rec["official"] = text
                elif text:
                    rec["address"].append(text)
        entries.append(rec)
    return entries


def parse_links(page: str) -> dict[str, str]:
    start = page.find('name="County"')
    assert start > 0, "County Sources anchor not found on links page"
    out = {}
    for href, label in re.findall(r'<a href="([^"]+)">(.*?)</a>', page[start:], flags=re.S | re.I):
        if "county" in clean(label).lower():
            out[county_key(label)] = html.unescape(href.strip())
    return out


def main() -> int:
    client = FetchClient(agent="seed-sos")
    off = client.get(OFFICIALS_URL, purpose="seed: officials")
    lnk = client.get(LINKS_URL, purpose="seed: county websites")
    assert off.ok and lnk.ok, f"seed fetch failed: {off.error} {lnk.error}"
    entries = [normalize_entry(e) for e in parse_officials(off.text())]
    links = parse_links(lnk.text())
    counties = sorted({e["county"] for e in entries})
    assert len(counties) == EXPECTED_COUNTIES, f"expected {EXPECTED_COUNTIES} counties, parsed {len(counties)}"
    unknown_links = sorted(set(links) - set(counties))
    assert not unknown_links, f"links page names counties not in officials list: {unknown_links}"
    DATA.mkdir(exist_ok=True)
    fetched = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(off.fetched_at))
    (DATA / "sos_officials_parsed.json").write_text(json.dumps(
        {"source": OFFICIALS_URL, "content_hash": off.content_hash, "fetched_at_utc": fetched,
         "entries": entries}, indent=2))
    cols = ["county", "office_title", "official", "phone", "email", "abbm_email", "fax", "address",
            "offices_listed", "county_website_sos", "dash_normalized", "sos_officials_hash", "sos_links_hash"]
    with open(DATA / "seed_counties.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for c in counties:
            es = [e for e in entries if e["county"] == c]
            first = es[0]
            w.writerow({"county": c, "office_title": first["office_title"], "official": first["official"],
                        "phone": first["phone"], "email": first["email"], "abbm_email": first["abbm_email"],
                        "fax": first["fax"], "address": " | ".join(first["address"]), "offices_listed": len(es), "dash_normalized": "y" if first["dash_normalized"] else "n",
                        "county_website_sos": links.get(c, ""), "sos_officials_hash": off.content_hash,
                        "sos_links_hash": lnk.content_hash})
    (DATA / "all_counties.txt").write_text("\n".join(counties) + "\n")
    multi = [c for c in counties if sum(e["county"] == c for e in entries) > 1]
    print(json.dumps({"counties": len(counties), "office_entries": len(entries), "with_website": len(links),
                      "missing_phone": sum(1 for c in counties if not next(e for e in entries if e["county"] == c)["phone"]),
                      "missing_email": sum(1 for c in counties if not next(e for e in entries if e["county"] == c)["email"]),
                      "multi_office_counties": len(multi)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
