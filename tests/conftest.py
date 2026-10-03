import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

TEST_TOML = """
[client]
user_agent = "TXPrecinctTest/0.1"
timeout_seconds = 5
retries = 2
retry_backoff_base_seconds = 0.05
respect_robots = true
robots_cache_seconds = 3600
robots_failure_cache_seconds = 600
global_max_concurrency = 20
ca_bundle = ""
[paths]
state_dir = "{state}"
[host_classes.county]
min_interval_seconds = {county_interval}
max_concurrency = 1
backoff_on_429_seconds = 0.2
[host_classes.vendor]
min_interval_seconds = 0.0
max_concurrency = 4
backoff_on_429_seconds = 0.1
exponential_backoff = true
suffixes = ["localhost"]
[host_classes.archive]
min_interval_seconds = 2.0
max_concurrency = 1
backoff_on_429_seconds = 60
exponential_backoff = true
suffixes = ["archive.org"]
"""


class Server:
    """Scriptable local HTTP server. routes: path -> list of (status, headers, body) consumed in order;
    the last entry repeats."""

    def __init__(self):
        self.routes = {}
        self.hits = []
        self.lock = threading.Lock()
        self.active = 0
        self.max_active = 0
        self.delay = 0.0
        srv = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                with srv.lock:
                    srv.hits.append((time.time(), self.path, dict(self.headers)))
                    srv.active += 1
                    srv.max_active = max(srv.max_active, srv.active)
                    seq = srv.routes.get(self.path)
                    if seq is None:
                        resp = (404, {}, b"not found")
                    else:
                        resp = seq[0] if len(seq) == 1 else seq.pop(0)
                if srv.delay:
                    time.sleep(srv.delay)
                status, headers, body = resp
                if callable(body):
                    status, headers, body = body(self.headers)
                self.send_response(status)
                for k, v in headers.items():
                    self.send_header(k, v)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                with srv.lock:
                    srv.active -= 1

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.port = self.httpd.server_address[1]
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def hits_for(self, path):
        return [h for h in self.hits if h[1] == path]


@pytest.fixture
def server():
    s = Server()
    yield s
    s.httpd.shutdown()


@pytest.fixture
def make_client(tmp_path):
    from txprecinct.config import load_config
    from txprecinct.fetch import FetchClient

    def _make(county_interval=0.0, agent="test"):
        cfg_path = tmp_path / "fetch.toml"
        cfg_path.write_text(TEST_TOML.format(state=str(tmp_path / "state").replace("\\", "/"),
                                             county_interval=county_interval))
        return FetchClient(load_config(cfg_path), agent=agent)

    return _make
