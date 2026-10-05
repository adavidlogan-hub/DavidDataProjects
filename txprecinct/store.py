"""SQLite index plus content-addressed blob store shared by every process.

One database file holds the fetch log, the latest-fetch pointer per URL,
robots.txt results, and the cross-process rate-limit state. Bodies are stored
once per SHA-256 so identical responses are never stored twice.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS fetches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    final_url TEXT,
    host TEXT NOT NULL,
    host_class TEXT NOT NULL,
    fetched_at REAL NOT NULL,
    status INTEGER,
    content_hash TEXT,
    content_type TEXT,
    etag TEXT,
    last_modified TEXT,
    elapsed_ms INTEGER,
    attempts INTEGER,
    error TEXT,
    agent TEXT,
    purpose TEXT
);
CREATE INDEX IF NOT EXISTS fetches_url ON fetches(url);
CREATE TABLE IF NOT EXISTS latest_ok (
    url TEXT PRIMARY KEY,
    fetch_id INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS robots (
    host TEXT PRIMARY KEY,
    checked_at REAL NOT NULL,
    status INTEGER,
    body TEXT,
    error TEXT
);
CREATE TABLE IF NOT EXISTS host_state (
    host TEXT PRIMARY KEY,
    next_allowed REAL NOT NULL DEFAULT 0,
    backoff_until REAL NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS host_slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    host TEXT NOT NULL,
    lease_until REAL NOT NULL
);
"""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Store:
    def __init__(self, state_dir: Path):
        self.state_dir = Path(state_dir)
        self.blob_dir = self.state_dir / "cache" / "blobs"
        self.log_dir = self.state_dir / "logs"
        self.blob_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.state_dir / "cache" / "index.sqlite"
        with self.connect() as con:
            con.executescript(SCHEMA)

    def connect(self) -> sqlite3.Connection:
        con = sqlite3.connect(self.db_path, timeout=60, isolation_level=None)
        con.execute("PRAGMA journal_mode=WAL")
        con.execute("PRAGMA busy_timeout=60000")
        con.row_factory = sqlite3.Row
        return con

    # Blobs -----------------------------------------------------------------
    def blob_path(self, content_hash: str) -> Path:
        assert len(content_hash) == 64, f"bad content hash {content_hash!r}"
        return self.blob_dir / content_hash[:2] / content_hash

    def put_blob(self, body: bytes) -> str:
        h = sha256(body)
        p = self.blob_path(h)
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            tmp = p.with_suffix(".tmp")
            tmp.write_bytes(body)
            tmp.replace(p)
        return h

    def get_blob(self, content_hash: str) -> bytes:
        body = self.blob_path(content_hash).read_bytes()
        if sha256(body) != content_hash:
            raise RuntimeError(f"blob {content_hash} failed hash verification")
        return body

    # Fetch log -------------------------------------------------------------
    def record_fetch(self, rec: dict, ok: bool) -> int:
        cols = ("url", "final_url", "host", "host_class", "fetched_at", "status", "content_hash",
                "content_type", "etag", "last_modified", "elapsed_ms", "attempts", "error", "agent", "purpose")
        with self.connect() as con:
            cur = con.execute(
                f"INSERT INTO fetches ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                [rec.get(c) for c in cols],
            )
            fid = cur.lastrowid
            if ok:
                con.execute("INSERT OR REPLACE INTO latest_ok (url, fetch_id) VALUES (?, ?)", (rec["url"], fid))
        if not ok:
            self.log_failure(rec)
        return fid

    def latest_ok(self, url: str) -> sqlite3.Row | None:
        with self.connect() as con:
            return con.execute(
                "SELECT f.* FROM latest_ok l JOIN fetches f ON f.id = l.fetch_id WHERE l.url = ?", (url,)
            ).fetchone()

    def log_failure(self, rec: dict) -> None:
        line = json.dumps({k: rec.get(k) for k in ("url", "host", "host_class", "fetched_at", "status",
                                                   "attempts", "error", "agent", "purpose")})
        with open(self.log_dir / "fetch_failures.jsonl", "a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    # Robots ----------------------------------------------------------------
    def get_robots(self, host: str) -> sqlite3.Row | None:
        with self.connect() as con:
            return con.execute("SELECT * FROM robots WHERE host = ?", (host,)).fetchone()

    def put_robots(self, host: str, status: int | None, body: str | None, error: str | None) -> None:
        with self.connect() as con:
            con.execute(
                "INSERT OR REPLACE INTO robots (host, checked_at, status, body, error) VALUES (?, ?, ?, ?, ?)",
                (host, time.time(), status, body, error),
            )

    def stats(self) -> dict:
        with self.connect() as con:
            rows = con.execute(
                "SELECT host_class, COUNT(*) n, SUM(error IS NULL) ok, SUM(error IS NOT NULL) failed "
                "FROM fetches GROUP BY host_class"
            ).fetchall()
        return {r["host_class"]: {"total": r["n"], "ok": r["ok"], "failed": r["failed"]} for r in rows}
