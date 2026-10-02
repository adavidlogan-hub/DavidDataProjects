"""Fetch one URL through the shared client. Prints a JSON summary line.

    python -m txprecinct.get URL --agent research-A --purpose "phase1:Harris results page"
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
    a = ap.parse_args(argv)
    r = FetchClient(agent=a.agent).get(a.url, use_cache=not a.refresh, purpose=a.purpose)
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
