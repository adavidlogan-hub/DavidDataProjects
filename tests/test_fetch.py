import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

ROBOTS_OK = (200, {"Content-Type": "text/plain"}, b"User-agent: *\nDisallow: /private\n")


def base(server, host="127.0.0.1"):
    return f"http://{host}:{server.port}"


def test_host_classification(make_client):
    c = make_client()
    assert c.cfg.classify("results.enr.clarityelections.com").name == "county"  # test config: only localhost is vendor
    assert c.cfg.classify("web.archive.org").name == "archive"
    assert c.cfg.classify("localhost").name == "vendor"
    assert c.cfg.classify("www.harrisvotes.com").name == "county"


def test_real_config_classification():
    from txprecinct.config import load_config
    cfg = load_config()
    assert cfg.classify("results.enr.clarityelections.com").name == "vendor"
    assert cfg.classify("web.archive.org").name == "archive"
    assert cfg.classify("www.sos.state.tx.us").name == "sos"
    assert cfg.classify("www.harrisvotes.com").name == "county"
    assert cfg.host_classes["county"].min_interval_seconds == 3.0
    assert cfg.host_classes["vendor"].max_concurrency == 4
    assert cfg.host_classes["archive"].min_interval_seconds == 2.0
    assert cfg.timeout_seconds == 20 and cfg.retries == 2


def test_fetch_caches_and_does_not_refetch(server, make_client):
    server.routes = {"/robots.txt": [ROBOTS_OK], "/page": [(200, {"ETag": '"v1"'}, b"hello")]}
    c = make_client()
    r1 = c.get(base(server) + "/page")
    assert r1.ok and r1.body == b"hello" and not r1.from_cache
    assert r1.content_hash and len(r1.content_hash) == 64
    r2 = c.get(base(server) + "/page")
    assert r2.from_cache and r2.body == b"hello" and r2.content_hash == r1.content_hash
    assert len(server.hits_for("/page")) == 1
    # a second client (another agent) also sees the cache
    c2 = make_client(agent="other")
    assert c2.get(base(server) + "/page").from_cache


def test_user_agent_sent(server, make_client):
    server.routes = {"/robots.txt": [ROBOTS_OK], "/ua": [(200, {}, b"x")]}
    make_client().get(base(server) + "/ua")
    assert server.hits_for("/ua")[0][2]["User-Agent"] == "TXPrecinctTest/0.1"


def test_conditional_request_304(server, make_client):
    def cond(headers):
        if headers.get("If-None-Match") == '"v1"':
            return 304, {"ETag": '"v1"'}, b""
        return 200, {"ETag": '"v1"'}, b"body-v1"
    server.routes = {"/robots.txt": [ROBOTS_OK], "/c": [(0, {}, cond)]}
    c = make_client()
    r1 = c.get(base(server) + "/c")
    r2 = c.get(base(server) + "/c", use_cache=False)
    assert r2.not_modified and r2.status == 304 and r2.body == b"body-v1"
    assert server.hits_for("/c")[1][2].get("If-None-Match") == '"v1"'
    assert r2.content_hash == r1.content_hash


def test_duplicate_bodies_stored_once(server, make_client):
    server.routes = {"/robots.txt": [ROBOTS_OK], "/a": [(200, {}, b"same")], "/b": [(200, {}, b"same")]}
    c = make_client()
    ra, rb = c.get(base(server) + "/a"), c.get(base(server) + "/b")
    assert ra.content_hash == rb.content_hash
    blobs = [p for p in c.store.blob_dir.rglob("*") if p.is_file()]
    assert len(blobs) == 1


def test_robots_disallow_blocks_fetch(server, make_client):
    server.routes = {"/robots.txt": [ROBOTS_OK], "/private/x": [(200, {}, b"secret")]}
    c = make_client()
    r = c.get(base(server) + "/private/x")
    assert not r.ok and r.error == "robots_disallowed_or_unreachable"
    assert server.hits_for("/private/x") == []


def test_robots_404_allows(server, make_client):
    server.routes = {"/p": [(200, {}, b"ok")]}  # robots.txt -> 404
    assert make_client().get(base(server) + "/p").ok


def test_robots_5xx_disallows(server, make_client):
    server.routes = {"/robots.txt": [(503, {}, b"down")], "/p": [(200, {}, b"ok")]}
    r = make_client().get(base(server) + "/p")
    assert not r.ok and server.hits_for("/p") == []


def test_retries_then_success(server, make_client):
    server.routes = {"/robots.txt": [ROBOTS_OK],
                     "/flaky": [(503, {}, b"e"), (503, {}, b"e"), (200, {}, b"finally")]}
    r = make_client().get(base(server) + "/flaky")
    assert r.ok and r.attempts == 3 and r.body == b"finally"


def test_retries_exhausted_logs_failure(server, make_client):
    server.routes = {"/robots.txt": [ROBOTS_OK], "/dead": [(500, {}, b"err")]}
    c = make_client()
    r = c.get(base(server) + "/dead")
    assert not r.ok and r.attempts == 3 and r.error == "HTTP 500"
    assert len(server.hits_for("/dead")) == 3
    lines = (c.store.log_dir / "fetch_failures.jsonl").read_text().splitlines()
    rec = json.loads(lines[-1])
    assert rec["url"].endswith("/dead") and rec["attempts"] == 3


def test_404_not_retried(server, make_client):
    server.routes = {"/robots.txt": [ROBOTS_OK]}
    r = make_client().get(base(server) + "/missing")
    assert not r.ok and r.attempts == 1 and r.status == 404


def test_network_error_logged(make_client):
    c = make_client()
    r = c.get("http://127.0.0.1:9/nothing")  # discard port, refused
    assert not r.ok and r.error


def test_429_backoff_respected(server, make_client):
    server.routes = {"/robots.txt": [ROBOTS_OK],
                     "/t": [(429, {"Retry-After": "1"}, b""), (200, {}, b"ok")]}
    r = make_client().get(base(server) + "/t")
    hits = server.hits_for("/t")
    assert r.ok and len(hits) == 2 and hits[1][0] - hits[0][0] >= 0.95


def test_county_min_interval(server, make_client):
    server.routes = {"/robots.txt": [ROBOTS_OK], "/1": [(200, {}, b"1")], "/2": [(200, {}, b"2")],
                     "/3": [(200, {}, b"3")]}
    c = make_client(county_interval=0.4)
    for p in ("/1", "/2", "/3"):
        c.get(base(server) + p)
    times = sorted(h[0] for h in server.hits)  # robots + 3 pages, all same host
    gaps = [b - a for a, b in zip(times, times[1:])]
    assert all(g >= 0.38 for g in gaps), gaps


def test_vendor_concurrency_capped_at_4(server, make_client):
    server.delay = 0.3
    server.routes = {f"/v{i}": [(200, {}, b"v%d" % i)] for i in range(10)}
    c = make_client()
    ths = [threading.Thread(target=c.get, args=(base(server, "localhost") + f"/v{i}",)) for i in range(10)]
    [t.start() for t in ths]
    [t.join() for t in ths]
    assert 2 <= server.max_active <= 4, server.max_active


def test_interval_holds_across_processes(server, tmp_path, make_client):
    server.routes = {"/robots.txt": [ROBOTS_OK]} | {f"/p{i}": [(200, {}, b"%d" % i)] for i in range(6)}
    c = make_client(county_interval=0.5)
    c.get(base(server) + "/p0")  # warm robots cache
    cfg_path = tmp_path / "fetch.toml"
    code = ("import sys; sys.path.insert(0, %r)\n"
            "from txprecinct.config import load_config\nfrom txprecinct.fetch import FetchClient\n"
            "c = FetchClient(load_config(%r), agent=sys.argv[1])\n"
            "for p in sys.argv[2:]: c.get(%r + p)\n") % (str(Path(__file__).resolve().parent.parent),
                                                       str(cfg_path), base(server))
    env = dict(os.environ)
    procs = [subprocess.Popen([sys.executable, "-c", code, "a", "/p1", "/p2"], env=env),
             subprocess.Popen([sys.executable, "-c", code, "b", "/p3", "/p4"], env=env)]
    for p in procs:
        assert p.wait(timeout=60) == 0
    times = sorted(h[0] for h in server.hits if h[1] in ("/p1", "/p2", "/p3", "/p4"))
    gaps = [b - a for a, b in zip(times, times[1:])]
    assert len(times) == 4 and all(g >= 0.45 for g in gaps), gaps


def test_searchlog_roundtrip(tmp_path, make_client):
    c = make_client()
    env = dict(os.environ, TXP_FETCH_CONFIG=str(tmp_path / "fetch.toml"))
    root = str(Path(__file__).resolve().parent.parent)
    run = lambda *a, inp=None: subprocess.run([sys.executable, "-m", "txprecinct.searchlog", *a], cwd=root,
                                              env=env, input=inp, capture_output=True)
    assert run("check", "Harris  County results").returncode == 1
    assert run("record", "--agent", "t", "--county", "Harris", "harris county RESULTS",
               inp=b"result text").returncode == 0
    out = run("check", "Harris  County results")
    assert out.returncode == 0 and out.stdout.endswith(b"result text")


def test_normalize_url():
    from txprecinct.fetch import normalize_url
    assert normalize_url("https://x.gov/upload/DEM-Ballots by mail 3-5-24.pdf") == \
        "https://x.gov/upload/DEM-Ballots%20by%20mail%203-5-24.pdf"
    assert normalize_url("https://x.gov/a%20b?q=1 2&r=x#frag") == "https://x.gov/a%20b?q=1%202&r=x"
    assert normalize_url("HTTPS://x.gov/ok/path?a=1") == "https://x.gov/ok/path?a=1"


def test_url_with_space_fetches(server, make_client):
    server.routes = {"/robots.txt": [ROBOTS_OK], "/a%20b.pdf": [(200, {}, b"pdf")]}
    r = make_client().get(base(server) + "/a b.pdf")
    assert r.ok and r.body == b"pdf"


def test_robots_transient_failure_is_retried(server, make_client):
    server.routes = {"/robots.txt": [(503, {}, b"busy"), ROBOTS_OK], "/p": [(200, {}, b"ok")]}
    r = make_client().get(base(server) + "/p")
    assert r.ok and len(server.hits_for("/robots.txt")) == 2


def test_post_json_is_stored_under_its_own_key(make_client, monkeypatch):
    import json as _json
    client = make_client()
    sent = {}

    def fake_raw(url, extra, data=None):
        sent.update(url=url, data=data, ctype=extra.get("Content-Type"))
        return 200, b'{"ok": true}', {}, url, None
    monkeypatch.setattr(client, "_raw_request", fake_raw)
    monkeypatch.setattr(client, "_robots_allows", lambda *a: True)
    r = client.post_json("https://portal.example.org/svc/List", {"folderId": 333})
    assert r.ok and r.url.startswith("https://portal.example.org/svc/List#post-")
    assert _json.loads(sent["data"]) == {"folderId": 333} and sent["ctype"].startswith("application/json")
    assert client.store.latest_ok("https://portal.example.org/svc/List") is None
