# Blockers

Status as of 2026-10-02 14:15 UTC.

## Open

None blocking the pilot. Item 2 below is worked around, not fixed.

## Worked around

2. **web.archive.org is unreachable from the build container (2026-10-02, from 14:07 UTC).**
   - Symptom: the CONNECT tunnel opens but the TLS handshake is reset after about 12 seconds on every attempt (curl error 35; proxy log "tunnel closed code 1006"). The hosted page-fetch tool also refuses web.archive.org. Memento aggregator and archive.ph are unreachable too.
   - Likely cause: web.archive.org refusing traffic from this cloud provider's egress addresses. The environment's network setting does not control this.
   - What does work from the container: archive.org itself, including the availability API, which returns only the single snapshot closest to a timestamp. That cannot show what a page contained.
   - **Workaround (in use): GitHub Actions.** GitHub-hosted runners reach web.archive.org normally (test run 2026-10-02 14:09 UTC: CDX listing HTTP 200 in 1.9 s, snapshot replay HTTP 200 in 1.6 s; Harris Live-Results captured at 2024-11-05 20:39 CST). The harvest runs there as .github/workflows/wayback-harvest.yml using the same fetch module and config, so the archive.org limit (1 request per 2 s, 429 backoff), robots.txt, and caching still apply. One harvest runs at a time. Raw snapshots go to the wayback-data branch. Pushing a change to phase1/wayback_targets.json starts a harvest.
   - Limits of the workaround: about 6 hours per job on GitHub-hosted runners; the full 254-county harvest needs to be split across several runs. Uses GitHub Actions minutes on the owner's account.
   - Second fallback: run `python -m phase1.wayback_harvest` from the Windows laptop or any home connection; it writes the same output format.

## Resolved

1. **Network egress was blocked for every target host (2026-10-02 13:49 to 14:07 UTC).** County sites, sos.state.tx.us, archive.org, and general sites were rejected by the environment's network policy (proxy 403 "connect_rejected"); only the hosted web search tool worked.
   - Resolved 14:07 UTC: the owner set the environment (named "Default") to full network access. County sites, sos.state.tx.us, and archive.org now work through the fetch module (harrisvotes.com fetched with HTTP 200).
   - Residual effect: research agents worked from search results only until 14:07 UTC; they were told to backfill contacts, results URLs, platforms, and usage notice text with direct fetches for counties finished before then.
   - Not affected at any point: the poller and dry run run on the Windows laptop, which has normal internet access.
