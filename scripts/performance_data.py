#!/usr/bin/env python3
"""Build the normalized performance dataset, SVG charts and coverage page.

Usage:
    python -I scripts/performance_data.py

Reads the report tables from docs/MKW.md, docs/DONKEY-KONG.md,
docs/POKOPIA.md and the non-duplicated sections of docs/PERFORMANCE.md.
Writes data/performance-reports.json, docs/charts/*.svg and docs/COVERAGE.md.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CHARTS = DOCS / "charts"
SKIP_SECTIONS = {"Mario Kart World", "Donkey Kong Bananza", "Pokemon Pokopia"}
PALETTE = [
    "#2563eb", "#dc2626", "#16a34a", "#d97706", "#7c3aed",
    "#0891b2", "#db2777", "#65a30d", "#ea580c", "#4f46e5",
]


def clean(value: str) -> str:
    value = (value or "").strip()
    value = re.sub(r"\*\*(.*?)\*\*", r"\1", value)
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    return value.strip()


def split_row(line: str) -> list[str]:
    return [clean(cell) for cell in line.strip().strip("|").split("|")]


def parse_fps(text: str) -> tuple[int | None, int | None, int | None]:
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    values: list[int] = []
    ranges = re.findall(r"(\d+)\s*(?:-|to)\s*(\d+)\s*FPS", text, re.I)
    for low, high in ranges:
        values.extend([int(low), int(high)])
    plus = re.findall(r"(\d+)\+\s*FPS", text, re.I)
    for value in plus:
        values.append(int(value))
    under = re.findall(r"under\s*(\d+)\s*FPS", text, re.I)
    for value in under:
        values.append(int(value))
    singles = re.findall(r"(?<![\d-])(\d{1,3})\s*FPS", text, re.I)
    for value in singles:
        values.append(int(value))
    singles_cap = re.findall(r"(\d{1,3})\s*FPS\s*(?:cap|lock)", text, re.I)
    for value in singles_cap:
        values.append(int(value))
    if not values:
        return None, None, None
    low = min(values)
    high = max(values)
    return low, high, round((low + high) / 2)


def gpu_vendor(gpu: str) -> str:
    text = gpu.lower()
    if "steam deck" in text:
        return "Steam Deck"
    if "rog ally" in text or "z1 extreme" in text or "780m" in text:
        return "AMD"
    if any(token in text for token in ("rtx", "gtx", "quadro", "nvidia")):
        return "NVIDIA"
    if any(token in text for token in ("rx", "radeon", "amd")):
        return "AMD"
    if any(token in text for token in ("arc", "intel", "iris")):
        return "Intel"
    if any(token in text for token in ("adreno", "snapdragon", "mali")):
        return "Android"
    if "apple" in text or re.search(r"\bm[1-4]\b", text):
        return "Apple"
    return "Unknown"


def cpu_vendor(cpu: str) -> str:
    text = cpu.lower()
    if "steam deck" in text or "z1 extreme" in text:
        return "AMD"
    if "ryzen" in text or "amd" in text or re.search(r"\b\d{4}x3d\b", text):
        return "AMD"
    if re.search(r"\bi[3579][- ]?\d", text) or "core ultra" in text or "intel" in text:
        return "Intel"
    if re.match(r"^(1[0-9]{4}|[0-9]{5})[a-z]?$", text):
        return "Intel"
    if re.match(r"^[2579][0-9]{3}[a-z0-9]*$", text):
        return "AMD"
    if "apple" in text or re.search(r"\bm[1-4]\b", text):
        return "Apple"
    if "snapdragon" in text or "arm" in text:
        return "ARM"
    return "Unknown"


def gpu_model(gpu: str) -> str:
    text = clean(gpu)
    if not text or text.lower() in {"not stated", "unknown", "n/a"}:
        return "Unknown"
    if "steam deck" in text.lower():
        return "Steam Deck"
    text = re.sub(r"\b(Laptop|Mobile|Linux|Windows|AMD|NVIDIA|GPU|iGPU)\b", "", text, flags=re.I)
    text = re.sub(r"\b\d+\s*GB\b", "", text, flags=re.I)
    text = re.sub(r"\s+", " ", text).strip(" ,")
    text = text.replace("780M", "Radeon 780M")
    if not text or text.lower() in {"amd", "nvidia"}:
        return "Unknown"
    return text


def cpu_model(cpu: str) -> str:
    text = clean(cpu)
    if not text or text.lower() in {"not stated", "unknown", "n/a"}:
        return "Unknown"
    text = re.sub(r"\b(Intel|AMD)\b", "", text, flags=re.I)
    text = re.sub(r"\s+", " ", text).strip(" ,")
    text = text.replace("12th-gen i5", "i5 12th-gen")
    text = text.replace("14th-gen i7", "i7 14th-gen")
    text = text.replace("Ultra 255HX", "Core Ultra 255HX")
    text = text.replace("i5 12th-gen 2.5 GHz", "i5 12th-gen")
    canonical = {
        "7700X": "Ryzen 7 7700X",
        "7800X3D": "Ryzen 7 7800X3D",
        "9800X3D": "Ryzen 7 9800X3D",
        "5800X3D": "Ryzen 7 5800X3D",
        "5700X3D": "Ryzen 7 5700X3D",
        "5500X3D": "Ryzen 5 5500X3D",
        "5800X": "Ryzen 7 5800X",
        "5700X": "Ryzen 7 5700X",
        "7600X": "Ryzen 5 7600X",
        "7600": "Ryzen 5 7600",
        "5600X": "Ryzen 5 5600X",
        "5600": "Ryzen 5 5600",
        "13400F": "i5-13400F",
        "Z1 Extreme": "Ryzen Z1 Extreme",
    }
    if text in canonical:
        return canonical[text]
    if text.lower() == "5700":
        text = "Ryzen 7 5700"
    return text or "Unknown"


def ram_gb(ram: str) -> int | None:
    match = re.search(r"(\d+)\s*GB", ram, re.I)
    return int(match.group(1)) if match else None


def build_family(build: str) -> str:
    text = build.lower()
    if "pokedinner" in text:
        return "PokeDinner"
    if "zendnevs" in text:
        return "ZendNevs"
    if "smiley" in text:
        return "SmileyTatsu"
    if "selevet" in text:
        return "Selevet"
    if "orchid" in text or "lichii" in text or "zortos" in text or "notsapinho" in text or "jojo" in text:
        return "Other fork"
    if re.search(r"\bbuild\b|\bv0\.1\.0\b|^\d{3}$|^20[0-9]$", text):
        return "Eglantine build"
    return "Unspecified"


def normalize(row: dict, game: str) -> dict | None:
    game = clean(game)
    if not game or game.lower() == "game":
        return None
    build = clean(row.get("Build", "unspecified")) or "unspecified"
    cpu = clean(row.get("CPU", "not stated")) or "not stated"
    gpu = clean(row.get("GPU", "not stated")) or "not stated"
    ram = clean(row.get("RAM", "not stated")) or "not stated"
    performance = clean(row.get("Performance", ""))
    notes = clean(row.get("Notes", ""))
    date = clean(row.get("Date", ""))
    source = clean(row.get("Source", ""))
    if not source:
        build_lower = build.lower()
        if "sighya" in notes.lower():
            source = f"SigHya Discord, {date}" if date else "SigHya Discord"
        elif "zendnevs" in build_lower:
            source = "ZendNevs release notes"
        elif "orchid" in build_lower:
            source = "Orchid README"
        elif "lichii" in build_lower:
            source = "Lichii reports"
        else:
            source = f"Discord, {date}" if date else "Discord"
    low, high, mid = parse_fps(performance)
    recent = date in {"3 Nov", "4 Nov", "5 Nov"}
    return {
        "game": game,
        "date": date,
        "build": build,
        "cpu": cpu,
        "gpu": gpu,
        "ram": ram,
        "performance": performance,
        "notes": notes,
        "source": source,
        "gpu_vendor": gpu_vendor(gpu),
        "cpu_vendor": cpu_vendor(cpu),
        "gpu_model": gpu_model(gpu),
        "cpu_model": cpu_model(cpu),
        "ram_gb": ram_gb(ram),
        "fps_min": low,
        "fps_max": high,
        "fps_mid": mid,
        "build_family": build_family(build),
        "recent": recent,
    }


def parse_doc(path: Path, default_game: str | None = None) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    reports: list[dict] = []
    section = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            section = line[3:].strip()
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1]):
            header = split_row(line)
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                cells = split_row(lines[i])
                if len(cells) == len(header):
                    row = dict(zip(header, cells))
                    game = default_game or row.get("Game") or section
                    if section not in SKIP_SECTIONS:
                        normalized = normalize(row, game)
                        if normalized:
                            reports.append(normalized)
                i += 1
            continue
        i += 1
    return reports


def dedupe(reports: list[dict]) -> list[dict]:
    seen = set()
    output = []
    for report in reports:
        key = (
            report["game"], report["build"], report["cpu"], report["gpu"],
            report["ram"], report["performance"],
        )
        if key in seen:
            continue
        seen.add(key)
        output.append(report)
    return output


def escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def nice_step(max_value: int) -> int:
    if max_value <= 5:
        return 1
    if max_value <= 10:
        return 2
    if max_value <= 25:
        return 5
    if max_value <= 50:
        return 10
    if max_value <= 100:
        return 20
    return 50


def stacked_chart(
    categories: list[str],
    series: dict[str, dict[str, int]],
    title: str,
    subtitle: str,
    path: Path,
    width: int = 1100,
    left: int = 300,
    color_map: dict[str, str] | None = None,
    sort_categories: bool = True,
) -> None:
    games = sorted(series)
    totals = {category: sum(series[game].get(category, 0) for game in games) for category in categories}
    categories = [category for category in categories if totals.get(category, 0) > 0]
    if sort_categories:
        categories.sort(key=lambda category: totals[category], reverse=True)
    if not categories:
        return
    max_total = max(totals.values())
    step = nice_step(max_total)
    ticks = list(range(0, max_total + step, step))
    max_tick = ticks[-1]
    bar_h = 24
    gap = 10
    bottom = 46
    chart_w = width - left - 90
    colors = color_map or {game: PALETTE[index % len(PALETTE)] for index, game in enumerate(games)}

    legend_rows: list[list[str]] = []
    row: list[str] = []
    legend_x = 24
    for game in games:
        item_w = 18 + len(game) * 6.2 + 12
        if row and legend_x + item_w > width - 24:
            legend_rows.append(row)
            row = []
            legend_x = 24
        row.append(game)
        legend_x += item_w
    if row:
        legend_rows.append(row)
    top = 98 + max(0, len(legend_rows) - 1) * 16
    height = top + len(categories) * (bar_h + gap) + bottom

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="24" y="32" font-family="Segoe UI, Arial, sans-serif" font-size="20" font-weight="600" fill="#111827">{escape(title)}</text>',
        f'<text x="24" y="52" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="#6b7280">{escape(subtitle)}</text>',
    ]

    for legend_row, games_row in enumerate(legend_rows):
        legend_x = 24
        legend_y = 76 + legend_row * 16
        for game in games_row:
            svg.append(f'<rect x="{legend_x}" y="{legend_y - 9}" width="10" height="10" fill="{colors[game]}"/>')
            svg.append(f'<text x="{legend_x + 15}" y="{legend_y}" font-family="Segoe UI, Arial, sans-serif" font-size="11" fill="#374151">{escape(game)}</text>')
            legend_x += 18 + len(game) * 6.2 + 12

    for tick in ticks:
        x = left + (tick / max_tick) * chart_w
        svg.append(f'<line x1="{x:.1f}" y1="{top - 8}" x2="{x:.1f}" y2="{height - bottom + 4}" stroke="#e5e7eb" stroke-width="1"/>')
        svg.append(f'<text x="{x:.1f}" y="{height - bottom + 22}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="10" fill="#9ca3af">{tick}</text>')

    y = top
    for category in categories:
        total = totals[category]
        svg.append(f'<text x="{left - 12}" y="{y + 16}" text-anchor="end" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="#111827">{escape(category)}</text>')
        x = left
        for game in games:
            value = series[game].get(category, 0)
            if not value:
                continue
            segment_w = max(0.8, (value / max_tick) * chart_w)
            svg.append(f'<rect x="{x:.1f}" y="{y}" width="{segment_w:.1f}" height="{bar_h}" fill="{colors[game]}"/>')
            x += segment_w
        svg.append(f'<text x="{x + 8:.1f}" y="{y + 16}" font-family="Segoe UI, Arial, sans-serif" font-size="11" fill="#4b5563">{total}</text>')
        y += bar_h + gap

    svg.append("</svg>")
    path.write_text("\n".join(svg), encoding="utf-8")


def group_series(reports: list[dict], category_key: str, limit: int | None = None) -> tuple[list[str], dict[str, dict[str, int]]]:
    counts = Counter(report[category_key] for report in reports if report[category_key] != "Unknown")
    categories = [category for category, _ in counts.most_common(limit)]
    series: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for report in reports:
        category = report[category_key]
        if category not in categories:
            continue
        series[report["game"]][category] += 1
    return categories, series


def generate_charts(reports: list[dict]) -> None:
    CHARTS.mkdir(parents=True, exist_ok=True)
    all_games = sorted({report["game"] for report in reports})
    game_colors = {game: PALETTE[index % len(PALETTE)] for index, game in enumerate(all_games)}

    gpu_categories, gpu_series = group_series(reports, "gpu_model", 14)
    stacked_chart(
        gpu_categories, gpu_series,
        "Reports by GPU model",
        "Number of reports per GPU, split by game. Reports without a named GPU are excluded.",
        CHARTS / "gpu-models.svg",
        color_map=game_colors,
    )

    cpu_categories, cpu_series = group_series(reports, "cpu_model", 14)
    stacked_chart(
        cpu_categories, cpu_series,
        "Reports by CPU model",
        "Number of reports per CPU, split by game. Reports without a named CPU are excluded.",
        CHARTS / "cpu-models.svg",
        color_map=game_colors,
    )

    games = [game for game, _ in Counter(report["game"] for report in reports).most_common()]
    vendor_series: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for report in reports:
        vendor_series[report["gpu_vendor"]][report["game"]] += 1
    stacked_chart(
        games, vendor_series,
        "Reports per game",
        "Number of reports per game, split by GPU vendor.",
        CHARTS / "games.svg",
        left=340,
    )

    date_order = ["31 Oct", "1 Nov", "2 Nov", "3 Nov", "4 Nov", "5 Nov"]
    date_series: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for report in reports:
        if report["date"] in date_order:
            date_series[report["game"]][report["date"]] += 1
    stacked_chart(
        date_order, date_series,
        "Reports by date",
        "Number of reports per day, split by game. The 3-5 Nov window drives the first-pick recommendations.",
        CHARTS / "dates.svg",
        left=180,
        color_map=game_colors,
        sort_categories=False,
    )

    vendors = ["NVIDIA", "AMD", "Intel", "Steam Deck", "Android", "Apple", "Unknown"]
    game_series: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for report in reports:
        game_series[report["game"]][report["gpu_vendor"]] += 1
    stacked_chart(
        vendors, game_series,
        "Reports by GPU vendor",
        "Number of reports per GPU vendor, split by game.",
        CHARTS / "gpu-vendors.svg",
        left=200,
        color_map=game_colors,
    )

    ram_labels = ["8 GB", "12 GB", "16 GB", "20 GB", "24 GB", "32 GB", "40 GB", "64 GB", "Unknown"]
    ram_series: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for report in reports:
        label = f"{report['ram_gb']} GB" if report["ram_gb"] else "Unknown"
        ram_series[report["game"]][label] += 1
    stacked_chart(
        ram_labels, ram_series,
        "Reports by RAM",
        "Number of reports per RAM size, split by game.",
        CHARTS / "ram.svg",
        left=200,
        color_map=game_colors,
    )

    builds = ["PokeDinner", "ZendNevs", "SmileyTatsu", "Selevet", "Eglantine build", "Other fork", "Unspecified"]
    build_series: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for report in reports:
        build_series[report["game"]][report["build_family"]] += 1
    stacked_chart(
        builds, build_series,
        "Reports by build family",
        "Number of reports per build family, split by game.",
        CHARTS / "builds.svg",
        left=220,
        color_map=game_colors,
    )

    setup_counts = Counter(
        f"{report['cpu_model']} + {report['gpu_model']}"
        for report in reports
        if report["cpu_model"] != "Unknown" and report["gpu_model"] != "Unknown"
    )
    setups = [setup for setup, _ in setup_counts.most_common(15)]
    setup_series: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for report in reports:
        setup = f"{report['cpu_model']} + {report['gpu_model']}"
        if setup in setups:
            setup_series[report["game"]][setup] += 1
    stacked_chart(
        setups, setup_series,
        "Most reported CPU and GPU combinations",
        "Top 15 setups by number of reports, split by game.",
        CHARTS / "top-setups.svg",
        left=330,
        color_map=game_colors,
    )


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return lines


def generate_coverage(reports: list[dict]) -> None:
    games = [game for game, _ in Counter(report["game"] for report in reports).most_common()]
    named_gpu = [report for report in reports if report["gpu_model"] != "Unknown"]
    named_cpu = [report for report in reports if report["cpu_model"] != "Unknown"]
    setups = {
        (report["cpu_model"], report["gpu_model"], report["ram"])
        for report in reports
        if report["cpu_model"] != "Unknown" and report["gpu_model"] != "Unknown"
    }
    recent_reports = [report for report in reports if report["recent"]]

    lines = [
        "# Coverage: what was tested on what",
        "",
        "<!-- Generated by scripts/performance_data.py. Do not edit by hand. -->",
        "",
        f"The dataset has {len(reports)} reports across {len(games)} games, {len(named_gpu)} with a named GPU, {len(named_cpu)} with a named CPU and {len(setups)} distinct CPU and GPU combinations. {len(recent_reports)} reports are from the 3-5 Nov window used for the first-pick recommendations.",
        "",
        "The source data is [`data/performance-reports.json`](../data/performance-reports.json). Charts are in [`charts/`](charts/).",
        "",
        "## Charts",
        "",
        "![Reports by GPU model](charts/gpu-models.svg)",
        "",
        "![Reports per game](charts/games.svg)",
        "",
        "![Reports by date](charts/dates.svg)",
        "",
        "![Reports by CPU model](charts/cpu-models.svg)",
        "",
        "![Reports by GPU vendor](charts/gpu-vendors.svg)",
        "",
        "![Reports by RAM](charts/ram.svg)",
        "",
        "![Reports by build family](charts/builds.svg)",
        "",
        "![Most reported setups](charts/top-setups.svg)",
        "",
        "## Recent reports (3-5 Nov)",
        "",
        "These are the reports used for the first-pick recommendations. Older rows are history, not current evidence.",
        "",
    ]

    rows = []
    recent_named = [
        report for report in recent_reports
        if report["cpu_model"] != "Unknown" or report["gpu_model"] != "Unknown"
    ]
    for report in sorted(recent_named, key=lambda item: (item["date"], item["game"]), reverse=True):
        setup = f"{report['cpu_model']} / {report['gpu_model']}"
        rows.append([report["date"], report["game"], report["build"], setup, report["performance"], report["source"]])
    lines += markdown_table(["Date", "Game", "Build", "Setup", "Performance", "Source"], rows)
    lines += ["", "Reports with no named CPU or GPU are excluded from this table but remain in the JSON.", ""]
    lines += ["", "## Game by GPU vendor", ""]

    vendors = ["NVIDIA", "AMD", "Intel", "Steam Deck", "Android", "Apple", "Unknown"]
    rows = []
    for game in games:
        subset = [report for report in reports if report["game"] == game]
        rows.append([game] + [str(sum(1 for report in subset if report["gpu_vendor"] == vendor)) for vendor in vendors])
    lines += markdown_table(["Game"] + vendors, rows)
    lines += ["", "## Game by top GPU models", ""]

    top_gpus = [model for model, _ in Counter(report["gpu_model"] for report in named_gpu).most_common(12)]
    rows = []
    for game in games:
        subset = [report for report in reports if report["game"] == game]
        rows.append([game] + [str(sum(1 for report in subset if report["gpu_model"] == model)) for model in top_gpus])
    lines += markdown_table(["Game"] + top_gpus, rows)
    lines += ["", "An all-zero row means the reports did not name that GPU; check the vendor table for Unknown counts.", ""]
    lines += ["## Game by CPU vendor", ""]

    cpu_vendors = ["AMD", "Intel", "Apple", "ARM", "Unknown"]
    rows = []
    for game in games:
        subset = [report for report in reports if report["game"] == game]
        rows.append([game] + [str(sum(1 for report in subset if report["cpu_vendor"] == vendor)) for vendor in cpu_vendors])
    lines += markdown_table(["Game"] + cpu_vendors, rows)
    lines += ["", "## Game by build family", ""]

    build_families = ["PokeDinner", "ZendNevs", "SmileyTatsu", "Selevet", "Eglantine build", "Other fork", "Unspecified"]
    rows = []
    for game in games:
        subset = [report for report in reports if report["game"] == game]
        rows.append([game] + [str(sum(1 for report in subset if report["build_family"] == family)) for family in build_families])
    lines += markdown_table(["Game"] + build_families, rows)
    lines += ["", "## Setups tested", ""]

    setup_map: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    setup_counts = Counter()
    for report in reports:
        if report["cpu_model"] == "Unknown" or report["gpu_model"] == "Unknown":
            continue
        key = (report["cpu_model"], report["gpu_model"], report["ram"])
        setup_map[key].add(report["game"])
        setup_counts[key] += 1
    rows = []
    for key, count in setup_counts.most_common(30):
        cpu, gpu, ram = key
        rows.append([cpu, gpu, ram, ", ".join(sorted(setup_map[key])), str(count)])
    lines += markdown_table(["CPU", "GPU", "RAM", "Games tested", "Reports"], rows)
    lines += ["", "## Gaps", ""]

    gaps = []
    for game in games:
        subset = [report for report in reports if report["game"] == game]
        present = {report["gpu_vendor"] for report in subset}
        if "Steam Deck" in present:
            present.add("AMD")
        missing = [vendor for vendor in ("NVIDIA", "AMD") if vendor not in present]
        if missing:
            gaps.append(f"- {game}: no {' or '.join(missing)} report.")
    lines += gaps or ["- No NVIDIA or AMD gap found."]
    lines += [
        "",
        "These gaps use all reports. A game can look covered by an old report and still have no recent result.",
        "",
        "Reports marked `not stated` for CPU, GPU or RAM are counted in the game totals but excluded from setup charts.",
        "",
        "## Missing data",
        "",
        "Most reports do not include the driver version, game version or 1% lows. A repeated setup with a different build can still produce a different result.",
        "",
    ]
    (DOCS / "COVERAGE.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    reports = []
    reports += parse_doc(DOCS / "MKW.md", "Mario Kart World")
    reports += parse_doc(DOCS / "DONKEY-KONG.md", "Donkey Kong Bananza")
    reports += parse_doc(DOCS / "POKOPIA.md", "Pokemon Pokopia")
    reports += parse_doc(DOCS / "PERFORMANCE.md")
    reports = dedupe(reports)

    data = {
        "generated": "2026-11-05",
        "source": "Parsed from docs/MKW.md, docs/DONKEY-KONG.md, docs/POKOPIA.md and docs/PERFORMANCE.md",
        "count": len(reports),
        "reports": reports,
    }
    (ROOT / "data" / "performance-reports.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    generate_charts(reports)
    generate_coverage(reports)
    print(f"wrote {len(reports)} reports, charts and coverage page")


if __name__ == "__main__":
    main()
