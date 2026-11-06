# Community reports

One JSON file per report. These are aggregated into [`docs/REPORTS.md`](../docs/REPORTS.md) by `scripts/reports.py render`, and CI validates every file on a PR.

## Filename

```
YYYY-MM-DD-<fork-id>-<short-slug>.json
```

Example: `2026-11-05-orchid-mario-kart-world-alice.json`

- The date must match the `date` field.
- Include the fork id in the slug so files sort predictably; the filename is only validated for its date prefix.
- Keep the rest of the slug short and lowercase.

## Schema

Required:

| Field | Type | Notes |
|---|---|---|
| `fork_id` | string | Must match an `id` in `data/forks.json` |
| `build` | string | Exact release tag or build, e.g. `build-212` |
| `date` | string | `YYYY-MM-DD`, the day you tested |
| `game` | string | Title only. No file names or title IDs |
| `platform` | string | `Windows 11`, `Windows 10`, `Linux`, `macOS`, `Android`, `PS5`, etc. |
| `cpu` | string | e.g. `Ryzen 7 5800X3D` |
| `gpu` | string | e.g. `Radeon RX 9070 XT` |
| `ram_gb` | integer | e.g. `32` |
| `status` | string | `perfect`, `playable`, `broken`, or `wont-boot` |
| `reporter` | string | GitHub handle, so reports can be de-duplicated |

Optional:

| Field | Type | Notes |
|---|---|---|
| `driver` | string | Driver version, `Mesa RADV git`, `Turnip`, etc. |
| `game_version` | string | e.g. `1.0.0` |
| `settings` | string | Resolution, API, upscaler, FPS cap, tweaks |
| `fps_typical` | integer | Warm-cache average, not the best spike |
| `fps_range` | string | e.g. `35-55` |
| `issues` | array of strings | e.g. `["shader stutter", "asset glitches"]` |
| `notes` | string | Workarounds, duration, build-to-build changes |
| `source_url` | string | Link to the issue or comment where you posted details |

## Example

```json
{
  "fork_id": "orchid",
  "build": "v0.7.2",
  "date": "2026-11-05",
  "game": "Mario Kart World",
  "game_version": "1.0.0",
  "platform": "Linux",
  "cpu": "Ryzen 7 5800X3D",
  "gpu": "Radeon RX 9070 XT",
  "driver": "Mesa RADV git",
  "ram_gb": 32,
  "settings": "Vulkan, 1440p, 60 FPS cap, TAA",
  "status": "playable",
  "fps_typical": 35,
  "fps_range": "28-42",
  "issues": ["asset glitches", "shader stutter"],
  "notes": "Warm cache; first two minutes stutter.",
  "reporter": "example"
}
```

## Validate and render

```bash
python -I scripts/reports.py validate
python -I scripts/reports.py render
```

`validate` checks required fields, the fork id, the status enum, the date and filename match, and numeric fields. `render` rewrites `docs/REPORTS.md`; commit the result.

## Intake candidates

`scripts/import_reddit.py` writes review candidates to `data/reports/inbox/`. That directory is gitignored, and the validator only reads the top level of `data/reports/`. Review a candidate, fill the required fields, give it a dated filename, and move it into `data/reports/` before running validate and render. See [the intake guide](../../docs/INTAKE.md) for the review steps.

## Review rules

- Don't edit someone else's report. Add a new report or open an issue with a correction.
- One report per build, game and config. Duplicate reports from the same person and build are collapsed.
- No copyrighted files. No ROMs, keys, firmware or links to them.
- Reports are anecdotes. Two independent reports on the same game, fork and GPU class are needed before a recommendation changes.
- Maintainers may close a report that lacks a real build tag or hardware details.
