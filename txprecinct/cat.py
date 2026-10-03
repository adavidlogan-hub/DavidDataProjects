"""Print a cached body, decompressed if the server sent it gzip-compressed.

The cache keeps exact bytes as received (some hosts, e.g. Clarity, gzip responses
even when not asked to). This tool is for reading them.

    python -m txprecinct.cat <url-or-content-hash> [--out FILE]
"""
import argparse
import gzip
import sys

from .config import load_config
from .fetch import normalize_url
from .store import Store


def decoded(body: bytes) -> bytes:
    return gzip.decompress(body) if body[:2] == b"\x1f\x8b" else body


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="txprecinct.cat")
    ap.add_argument("ref")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    store = Store(load_config().state_dir)
    h = a.ref
    if "://" in a.ref:
        row = store.latest_ok(normalize_url(a.ref))
        if row is None:
            print(f"not cached: {a.ref}", file=sys.stderr)
            return 1
        h = row["content_hash"]
    data = decoded(store.get_blob(h))
    if a.out:
        open(a.out, "wb").write(data)
    else:
        sys.stdout.buffer.write(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
