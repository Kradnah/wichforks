#!/usr/bin/env python3
"""Check that every repo/release URL in data/forks.json still resolves.

Usage:
    python -I scripts/check_links.py
    python -I scripts/check_links.py --data data/forks.json --timeout 15 --delay 1

Dead links (404/410) and unreachable hosts exit 1. Rate limits and 5xx
answers are retried; if they persist they are reported as INCONCLUSIVE and
do not fail the run, because that says nothing about the link itself.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

USER_AGENT = "whichforks-linkcheck/1.0"
KEYS = ("repo", "releases")
RETRY_STATUS = {429, 500, 502, 503, 504}


def fetch(url: str, timeout: int) -> tuple[int | None, str]:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    try:
        with urlopen(request, timeout=timeout) as response:
            response.read(1)
            return response.status, response.geturl()
    except HTTPError as exc:
        return exc.code, url
    except URLError as exc:
        return None, str(exc.reason)
    except OSError as exc:
        return None, str(exc)


def check(url: str, timeout: int, retries: int) -> tuple[int | None, str, int]:
    for attempt in range(1, retries + 1):
        status, final = fetch(url, timeout)
        if status is None or status in RETRY_STATUS:
            if attempt < retries:
                time.sleep(2 * attempt)
                continue
        return status, final, attempt
    return status, final, retries


def classify(status: int | None) -> str:
    if status is None:
        return "UNREACHABLE"
    if 200 <= status < 400:
        return "OK"
    if status in (404, 410):
        return "DEAD"
    if status in RETRY_STATUS or status == 403:
        return "INCONCLUSIVE"
    return "FAIL"


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=root / "data" / "forks.json")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--delay", type=float, default=1.0, help="seconds between URLs")
    args = parser.parse_args()

    try:
        data = json.loads(args.data.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read {args.data}: {exc}", file=sys.stderr)
        return 2

    counts = {"OK": 0, "DEAD": 0, "FAIL": 0, "INCONCLUSIVE": 0, "UNREACHABLE": 0}
    checked = 0

    for fork in data.get("forks", []):
        for key in KEYS:
            url = fork.get(key)
            if not url:
                continue
            checked += 1
            status, final_url, attempts = check(url, args.timeout, args.retries)
            outcome = classify(status)
            counts[outcome] += 1
            suffix = f" (after {attempts} tries)" if attempts > 1 else ""
            print(f"{outcome:<12} {status if status is not None else '---':>4}  {fork['name']:<34} {key:<8} {url}{suffix}")
            if outcome == "OK" and final_url.rstrip("/") != url.rstrip("/"):
                print(f"             redirected to: {final_url}")
            time.sleep(args.delay)

    print(f"\n{checked} URLs: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
    return 1 if counts["DEAD"] or counts["FAIL"] or counts["UNREACHABLE"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
