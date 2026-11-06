#!/usr/bin/env python3
"""Extract candidate performance reports from one public Reddit thread.

Usage:
    python -I scripts/import_reddit.py https://www.reddit.com/r/.../comments/...
    python -I scripts/import_reddit.py --file saved-thread.json --out data/reports/inbox

This fetches a single thread, extracts game / build / CPU / GPU / RAM / FPS
from the post and its comments, and writes review candidates to
data/reports/inbox/. It does not crawl subreddits, paginate, or commit.
A human must review each candidate and move it to data/reports/.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
USER_AGENT = "whichforks-intake/1.0 (single-thread manual review)"

GAMES = [
    ("Mario Kart World", r"\b(?:mkw|mario kart world|mario kart)\b"),
    ("Donkey Kong Bananza", r"\b(?:dkb|donkey kong bananza|bananza)\b"),
    ("Pokemon Pokopia", r"\bpokopia\b"),
    ("Splatoon Raiders", r"\bsplatoon raiders\b"),
    ("Zelda: Ocarina of Time remake", r"\b(?:oot|ocarina of time)\b"),
    ("Yoshi and the Mysterious Book", r"\byoshi\b"),
    ("Hyrule Warriors: Age of Imprisonment", r"\bhyrule warriors\b"),
    ("Star Fox", r"\bstar fox\b"),
    ("Mario Tennis Fever", r"\bmario tennis\b"),
    ("Fire Emblem Fortune's Weave", r"\bfire emblem\b"),
]

FORKS = [
    ("frizti-lichii", r"\bfrizti\b"),
    ("lichii", r"\blichii\b"),
    ("zendnevs-eglantine", r"\bzendnevs\b"),
    ("smileytatsu-eglantine", r"\bsmileytatsu\b"),
    ("selevet-eglantine", r"\bselevet\b"),
    ("orchid", r"\borchid\b"),
    ("notsapinho-eglantine", r"\bnotsapinho\b"),
    ("pokedinner", r"\bpokedinner\b|\bpoke dinner\b"),
    ("eglantine-upstream", r"\beglantine\b"),
]

CPU_RE = re.compile(
    r"\b(?:Ryzen [3579] \d{4}[A-Za-z0-9]*|\d{4}X3D|i[3579][- ]?\d{4,5}[A-Za-z]?|"
    r"Core Ultra [579] \d{3}[A-Za-z]*)\b",
    re.I,
)
GPU_RE = re.compile(
    r"\b(?:RTX \d{4}(?: Ti| Super)?|GTX \d{3,4}(?: Ti| Super)?|"
    r"RX \d{4}(?: XT| XTX| GRE)?|Arc [A-Z]\d{3})\b",
    re.I,
)
RAM_RE = re.compile(r"(\d{1,3})\s*GB(?:\s*(?:of\s*)?RAM|\s+DDR\d)", re.I)
FPS_RANGE_RE = re.compile(r"(\d{1,3})\s*(?:-|to)\s*(\d{1,3})\s*FPS", re.I)
FPS_SINGLE_RE = re.compile(r"(?<![\d-])(\d{1,3})\s*FPS", re.I)
BUILD_RE = re.compile(r"\b(?:build[- ]?\d{2,3}|frizti[ -]v\d+|v\d+\.\d+(?:\.\d+)?)\b", re.I)


def fetch(url: str, timeout: int) -> list:
    if not url.rstrip("/").endswith(".json"):
        url = url.split("?")[0].rstrip("/") + ".json"
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def strip_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text or "")


def pick(pattern: str, *texts: str) -> str | None:
    for text in texts:
        match = re.search(pattern, text or "", re.I)
        if match:
            return match.group(0).strip()
    return None


def parse_fps(text: str) -> str | None:
    range_match = FPS_RANGE_RE.search(text)
    if range_match:
        return f"{range_match.group(1)}-{range_match.group(2)} FPS"
    single = FPS_SINGLE_RE.search(text)
    if single:
        return f"{single.group(1)} FPS"
    return None


def date_from_utc(timestamp) -> str:
    if not timestamp:
        return ""
    return datetime.fromtimestamp(float(timestamp), tz=timezone.utc).date().isoformat()


def candidate(text: str, source_url: str, author: str, created_utc) -> dict | None:
    game = None
    for name, pattern in GAMES:
        if re.search(pattern, text, re.I):
            game = name
            break
    fps = parse_fps(text)
    cpu = pick(CPU_RE.pattern, text)
    gpu = pick(GPU_RE.pattern, text)
    ram_match = RAM_RE.search(text)
    if not game or not fps or not (cpu or gpu):
        return None
    fork_id = "unknown"
    for name, pattern in FORKS:
        if re.search(pattern, text, re.I):
            fork_id = name
            break
    build = pick(BUILD_RE.pattern, text) or "not stated"
    snippet = strip_urls(text).replace("\n", " ").strip()[:240]
    return {
        "review_required": True,
        "source_url": source_url,
        "game": game,
        "fork_id": fork_id,
        "build": build,
        "cpu": cpu or "not stated",
        "gpu": gpu or "not stated",
        "ram_gb": int(ram_match.group(1)) if ram_match else None,
        "performance": fps,
        "reporter": author or "unknown",
        "date": date_from_utc(created_utc),
        "evidence": snippet,
    }


def walk_comments(children, post_title: str, post_url: str, out: list) -> None:
    for child in children:
        if child.get("kind") != "t1":
            continue
        data = child.get("data", {})
        body = data.get("body", "")
        text = f"{post_title}\n{body}"
        permalink = data.get("permalink")
        url = f"https://www.reddit.com{permalink}" if permalink else post_url
        found = candidate(text, url, data.get("author", ""), data.get("created_utc"))
        if found:
            out.append(found)
        replies = data.get("replies")
        if isinstance(replies, dict):
            walk_comments(replies.get("data", {}).get("children", []), post_title, post_url, out)


def parse_thread(payload: list) -> tuple[dict, list[dict]]:
    post = payload[0]["data"]["children"][0]["data"]
    title = post.get("title", "")
    selftext = post.get("selftext", "")
    permalink = post.get("permalink")
    post_url = f"https://www.reddit.com{permalink}" if permalink else ""
    found = []
    post_candidate = candidate(f"{title}\n{selftext}", post_url, post.get("author", ""), post.get("created_utc"))
    if post_candidate:
        found.append(post_candidate)
    if len(payload) > 1:
        walk_comments(payload[1].get("data", {}).get("children", []), title, post_url, found)
    seen = set()
    unique = []
    for item in found:
        key = (item["source_url"], item["game"], item["cpu"], item["gpu"], item["build"], item["performance"])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return post, unique


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", nargs="?", help="one Reddit thread URL")
    parser.add_argument("--file", type=Path, help="saved Reddit JSON instead of a live fetch")
    parser.add_argument("--out", type=Path, default=ROOT / "data" / "reports" / "inbox")
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()

    if not args.url and not args.file:
        parser.print_help()
        return 2

    try:
        if args.file:
            payload = json.loads(args.file.read_text(encoding="utf-8"))
        else:
            payload = fetch(args.url, args.timeout)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"error: cannot read thread: {exc}", file=sys.stderr)
        return 1

    post, reports = parse_thread(payload)
    args.out.mkdir(parents=True, exist_ok=True)
    post_id = post.get("id", "thread")
    written = []
    for index, report in enumerate(reports, 1):
        path = args.out / f"{post_id}-{index}.json"
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        written.append(path)
        print(f"{report['game']}: {report['cpu']} / {report['gpu']} / {report['performance']} -> {path}")
    if not written:
        print("No candidate with a game, FPS and CPU or GPU was found.")
        return 0
    print(f"\n{len(written)} candidate(s) in {args.out}. Review before moving to data/reports/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
