# Contributing

Thanks for helping keep this list useful. The Switch 2 emulation scene changes hourly, so the main job is **accurate, dated, source-linked** updates.

## Rules

1. **One fork per PR.** Don't bundle unrelated additions.
2. **Link upstream.** Every entry needs the repository URL (GitHub/Forgejo) and, when available, the releases page.
3. **State the evidence.** For each game claim, say whether it comes from:
   - the fork's README/release notes (**documented**), or
   - a community report (**community-reported**), with a link/date.
4. **Include context:** platform, GPU/driver, build tag, and game tested.
5. **No copyrighted files.** No ROMs, keys, firmware, or links to them. No "repack" or ad-gated download links.
6. **No aggregator-only links** unless the aggregator itself links upstream for every entry and bundles nothing copyrighted.
7. **Update, don't duplicate.** If a fork already has a row, edit the row and bump its release/build fields.

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

## Checking links

```bash
python -I scripts/check_links.py
```

The script exits non-zero on dead (404/410) or unreachable URLs. Rate limits and 5xx answers are retried, then reported as INCONCLUSIVE without failing the run. Fix dead links or mark the fork as archived/removed in the same PR.

## Removing a fork

Forks disappear (DMCA, renames, abandoned accounts). If a link is dead:

- Try to find the renamed repo first.
- If it's gone, remove it from the tables and note the removal in the update log.
- Don't silently replace a dead link with a random mirror.

## Style

- English, short sentences, no hype.
- Use "community-reported" rather than presenting unverified FPS numbers as fact.
- Keep the confidence labels and the `Last verified` date honest.

## Update log

Add a row to the README update log with the date and a one-line summary.
