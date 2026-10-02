"""Load the single fetch config file and classify hosts into rate-limit classes."""
from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "config" / "fetch.toml"
CLASS_MATCH_ORDER = ("archive", "vendor", "sos")


@dataclass(frozen=True)
class HostClass:
    name: str
    min_interval_seconds: float
    max_concurrency: int
    backoff_on_429_seconds: float
    exponential_backoff: bool = False
    suffixes: tuple[str, ...] = ()


@dataclass(frozen=True)
class FetchConfig:
    user_agent: str
    timeout_seconds: float
    retries: int
    retry_backoff_base_seconds: float
    respect_robots: bool
    robots_cache_seconds: float
    robots_failure_cache_seconds: float
    global_max_concurrency: int
    ca_bundle: str
    state_dir: Path
    host_classes: dict[str, HostClass] = field(default_factory=dict)

    def classify(self, host: str) -> HostClass:
        host = host.lower().split(":")[0]
        for name in CLASS_MATCH_ORDER:
            hc = self.host_classes.get(name)
            if hc is None:
                continue
            for suf in hc.suffixes:
                if host == suf or host.endswith("." + suf):
                    return hc
        return self.host_classes["county"]


def load_config(path: str | os.PathLike | None = None, state_dir: str | os.PathLike | None = None) -> FetchConfig:
    path = Path(path or os.environ.get("TXP_FETCH_CONFIG") or DEFAULT_CONFIG)
    with open(path, "rb") as fh:
        raw = tomllib.load(fh)
    client = raw["client"]
    classes = {}
    for name, spec in raw["host_classes"].items():
        classes[name] = HostClass(
            name=name,
            min_interval_seconds=float(spec["min_interval_seconds"]),
            max_concurrency=int(spec["max_concurrency"]),
            backoff_on_429_seconds=float(spec["backoff_on_429_seconds"]),
            exponential_backoff=bool(spec.get("exponential_backoff", False)),
            suffixes=tuple(s.lower() for s in spec.get("suffixes", ())),
        )
    if "county" not in classes:
        raise ValueError(f"{path}: host_classes.county is required (default class)")
    sd = Path(state_dir or os.environ.get("TXP_STATE_DIR") or raw["paths"]["state_dir"])
    if not sd.is_absolute():
        sd = REPO_ROOT / sd
    return FetchConfig(
        user_agent=client["user_agent"],
        timeout_seconds=float(client["timeout_seconds"]),
        retries=int(client["retries"]),
        retry_backoff_base_seconds=float(client["retry_backoff_base_seconds"]),
        respect_robots=bool(client["respect_robots"]),
        robots_cache_seconds=float(client["robots_cache_seconds"]),
        robots_failure_cache_seconds=float(client["robots_failure_cache_seconds"]),
        global_max_concurrency=int(client["global_max_concurrency"]),
        ca_bundle=str(client.get("ca_bundle", "")),
        state_dir=sd,
        host_classes=classes,
    )
