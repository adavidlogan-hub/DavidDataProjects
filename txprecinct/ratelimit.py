"""Per-host rate limiting that holds across processes.

State lives in the shared SQLite file, so separate agent processes and the
poller all respect one set of limits per host. Each acquire takes a lease
(a concurrency slot) and pushes the host's next-allowed time forward by the
class's minimum interval.
"""
from __future__ import annotations

import threading
import time

from .config import HostClass
from .store import Store

POLL_SECONDS = 0.1


class HostLimiter:
    def __init__(self, store: Store, global_max_concurrency: int, lease_seconds: float):
        self.store = store
        self.lease_seconds = lease_seconds
        self.global_sem = threading.BoundedSemaphore(global_max_concurrency)

    def acquire(self, host: str, hc: HostClass) -> int:
        self.global_sem.acquire()
        try:
            return self._acquire_slot(host, hc)
        except BaseException:
            self.global_sem.release()
            raise

    def _acquire_slot(self, host: str, hc: HostClass) -> int:
        assert hc.max_concurrency >= 1, f"{hc.name}: max_concurrency must be >= 1"
        while True:
            con = self.store.connect()
            try:
                con.execute("BEGIN IMMEDIATE")
                now = time.time()
                con.execute("DELETE FROM host_slots WHERE lease_until < ?", (now,))
                row = con.execute("SELECT next_allowed, backoff_until FROM host_state WHERE host = ?",
                                  (host,)).fetchone()
                next_allowed = row["next_allowed"] if row else 0.0
                backoff_until = row["backoff_until"] if row else 0.0
                in_use = con.execute("SELECT COUNT(*) FROM host_slots WHERE host = ?", (host,)).fetchone()[0]
                gate = max(next_allowed, backoff_until)
                if gate <= now and in_use < hc.max_concurrency:
                    cur = con.execute("INSERT INTO host_slots (host, lease_until) VALUES (?, ?)",
                                      (host, now + self.lease_seconds))
                    con.execute(
                        "INSERT INTO host_state (host, next_allowed, backoff_until) VALUES (?, ?, ?) "
                        "ON CONFLICT(host) DO UPDATE SET next_allowed = excluded.next_allowed",
                        (host, now + hc.min_interval_seconds, backoff_until),
                    )
                    con.execute("COMMIT")
                    return cur.lastrowid
                con.execute("COMMIT")
                wait = max(gate - now, POLL_SECONDS)
            finally:
                con.close()
            time.sleep(min(wait, 1.0))

    def release(self, slot_id: int) -> None:
        try:
            with self.store.connect() as con:
                con.execute("DELETE FROM host_slots WHERE slot_id = ?", (slot_id,))
        finally:
            self.global_sem.release()

    def backoff(self, host: str, seconds: float) -> None:
        until = time.time() + seconds
        with self.store.connect() as con:
            con.execute(
                "INSERT INTO host_state (host, next_allowed, backoff_until) VALUES (?, 0, ?) "
                "ON CONFLICT(host) DO UPDATE SET backoff_until = MAX(backoff_until, excluded.backoff_until)",
                (host, until),
            )
