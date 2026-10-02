"""Fetch one URL through the shared client. Prints a JSON summary line.

    python -m txprecinct.get URL --agent research-A --purpose "phase1:Harris results page"

For a read-only listing service that only answers POST (Laserfiche portal folder listings),
pass --post-json '{...}'; --warmup URL first loads a page in the same session (cookies).
"""
import argparse
import json
import sys

from .fetch import FetchClient


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="txprecinct.get")
    ap.add_argument("url")
    ap.add_argument("--agent", required=True)
    ap.add_argument("--purpose", default="")
    ap.add_argument("--refresh", action="store_true", help="ignore cache (sends conditional headers)")
    ap.add_argument("--post-json", help="send this JSON body as a POST instead of a GET")
    ap.add_argument("--warmup", help="GET this URL first in the same session (sets cookies)")
    a = ap.parse_args(argv)
    client = FetchClient(agent=a.agent)
    if a.warmup:
        client.get(a.warmup, use_cache=False, purpose=a.purpose + " (warmup)")
    if a.post_json:
        r = client.post_json(a.url, json.loads(a.post_json), purpose=a.purpose)
    else:
        r = client.get(a.url, use_cache=not a.refresh, purpose=a.purpose)
    out = {"url": r.url, "ok": r.ok, "status": r.status, "error": r.error, "from_cache": r.from_cache,
           "content_hash": r.content_hash, "attempts": r.attempts}
    if r.ok:
        from .config import load_config
        from .store import Store
        out["blob_path"] = str(Store(load_config().state_dir).blob_path(r.content_hash))
    print(json.dumps(out))
    return 0 if r.ok else 2


if __name__ == "__main__":
    sys.exit(main())
