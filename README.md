# Texas county precinct-reporting research and election-night poller

Internal project. See DECISIONS.md, BLOCKERS.md, and PILOT_REPORT.md.

- `config/fetch.toml`: the single source of per-host rate limits and client settings.
- `txprecinct/`: shared fetch module (rate limits, robots.txt, retries, cache).
- `phase1/`: county research evidence, verification, and CSV build.
- `tests/`: run `python -m pytest -q tests`.
