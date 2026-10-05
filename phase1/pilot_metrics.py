"""Summarize fetch and search activity from the shared cache index, by agent and host class."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from txprecinct.config import load_config  # noqa: E402
from txprecinct.store import Store  # noqa: E402


def metrics() -> dict:
    store = Store(load_config().state_dir)
    with store.connect() as con:
        by_agent = con.execute(
            "SELECT agent, host_class, COUNT(*) n, SUM(error IS NULL) ok, SUM(error IS NOT NULL) failed "
            "FROM fetches GROUP BY agent, host_class ORDER BY agent, host_class").fetchall()
        errors = con.execute(
            "SELECT error, COUNT(*) n FROM fetches WHERE error IS NOT NULL GROUP BY error ORDER BY n DESC").fetchall()
        robots = con.execute("SELECT host, status, error FROM robots ORDER BY host").fetchall()
        span = con.execute("SELECT MIN(fetched_at), MAX(fetched_at) FROM fetches").fetchone()
    return {
        "by_agent": [dict(r) for r in by_agent],
        "errors": [dict(r) for r in errors],
        "robots_hosts": [dict(r) for r in robots],
        "first_fetch_epoch": span[0], "last_fetch_epoch": span[1],
    }


if __name__ == "__main__":
    print(json.dumps(metrics(), indent=2))
