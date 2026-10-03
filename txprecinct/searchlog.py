"""Record web-search evidence in the shared cache so no agent repeats a query.

The research agents' only working evidence channel in the pilot environment is
a server-side web search tool that this code cannot call. Agents therefore run
the search, then pipe the verbatim result text here. It is stored like any
other fetch: timestamped, hashed, deduplicated.

    python -m txprecinct.searchlog check "query text"
    python -m txprecinct.searchlog record --agent research-1 --county Harris "query text" < result.txt
"""
from __future__ import annotations

import argparse
import sys
import time
from urllib.parse import quote

from .config import load_config
from .store import Store


def search_key(query: str) -> str:
    return "websearch:?q=" + quote(" ".join(query.split()).lower())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="txprecinct.searchlog")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("query")
    r = sub.add_parser("record")
    r.add_argument("--agent", required=True)
    r.add_argument("--county", default="")
    r.add_argument("query")
    args = ap.parse_args(argv)

    store = Store(load_config().state_dir)
    key = search_key(args.query)
    if args.cmd == "check":
        row = store.latest_ok(key)
        if row is None:
            print("NOT_CACHED")
            return 1
        print(f"CACHED fetched_at={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(row['fetched_at']))} "
              f"hash={row['content_hash']}")
        sys.stdout.write(store.get_blob(row["content_hash"]).decode("utf-8"))
        return 0
    body = sys.stdin.buffer.read()
    if not body.strip():
        raise SystemExit("refusing to record an empty search result")
    h = store.put_blob(body)
    store.record_fetch({"url": key, "host": "websearch", "host_class": "websearch", "fetched_at": time.time(),
                        "status": 200, "content_hash": h, "content_type": "text/plain", "attempts": 1,
                        "agent": args.agent, "purpose": f"phase1:{args.county}"}, ok=True)
    print(f"RECORDED hash={h}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
