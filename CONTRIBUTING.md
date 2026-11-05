# Contributing

Thanks for helping keep this list useful. The Switch 2 emulation scene changes hourly, so the main job is accurate, dated, source-linked updates.

## Rules

1. One fork per PR. Don't bundle unrelated additions.
2. Link upstream. Every entry needs the repository URL (GitHub or Forgejo) and, when available, the releases page.
3. State the evidence. For each game claim, say whether it comes from:
   - the fork's README or release notes (documented), or
   - a community report (community-reported), with a link and date.
4. Include context: platform, GPU and driver, build tag, and game tested.
5. No copyrighted files. No ROMs, keys, firmware or links to them. No "repack" or ad-gated download links.
6. Update, don't duplicate. If a fork already has a row, edit the row and bump its release or build fields.

## Reporting your experience

You don't need to write JSON to contribute a data point.

- Fast path: open an [experience report](issues/new?template=experience-report.yml) issue. Use the exact build tag, game title, CPU, GPU and driver, RAM, settings and outcome.
- Structured path: add `data/reports/YYYY-MM-DD-<fork-id>-<slug>.json` following [data/reports/README.md](data/reports/README.md), then run:

```bash
python -I scripts/reports.py validate
python -I scripts/reports.py render
```

Rules:

- One report per build, game and config. Duplicates from the same reporter are collapsed.
- No ROMs, keys, firmware or links to them.
- Reports are public; use your GitHub handle.
- Don't edit someone else's report. Add a new one or open an issue with a correction.
- A recommendation changes only after two independent reports on the same game, fork and GPU class agree.

Maintainers: create the `experience-report` label if it doesn't exist, and regenerate `docs/REPORTS.md` after merging reports.

## Adding a fork

Add an entry to `data/forks.json`:

```json
{
  "id": "short-slug",
  "name": "Display Name (Author)",
  "repo": "https://github.com/author/repo",
  "releases": "https://github.com/author/repo/releases",
  "host": "GitHub",
  "role": "one-line role",
  "platforms": ["Windows"],
  "gpu": ["NVIDIA", "AMD"],
  "best_for": ["Game or use case"],
  "latest_release": { "tag": "build-1", "date": "2026-11-05", "prerelease": true },
  "license": "GPL-3.0",
  "stars_at_check": 0,
  "confidence": "documented",
  "notes": "Short, factual, sourced."
}
```

Allowed `confidence` values: `documented`, `community-reported`, `source-only`, `unverified`.

Then add the fork to the relevant README tables and, if necessary, the game matrix. Use the same wording as the JSON so the two don't drift.

## Checking links and reports

```bash
python -I scripts/check_links.py
python -I scripts/reports.py validate
python -I scripts/performance_data.py
```

The link checker exits non-zero on dead (404/410) or unreachable URLs. Rate limits and 5xx answers are retried, then reported as INCONCLUSIVE without failing the run. The report validator exits non-zero on schema errors. After editing a performance table, regenerate the JSON, SVG charts and coverage page, and commit them; CI checks that they are current. Fix dead links or mark the fork as archived or removed in the same PR.

## Removing a fork

Forks disappear (DMCA, renames, abandoned accounts). If a link is dead:

- Try to find the renamed repo first.
- If it's gone, remove it from the tables and note the removal in the update log.
- Don't silently replace a dead link with a random mirror.

## Style

- English, short sentences, no hype.
- Use "community-reported" instead of presenting unverified FPS numbers as fact.
- Prefer recent reports. A 31 Oct report on an old build is history, not evidence for the current build.
- A self-reported release note from a release-only repo needs independent confirmation before it changes a first pick.
- Keep the confidence labels and the `Last verified` date honest.

## Update log

Add a row to the README update log with the date and a one-line summary.
