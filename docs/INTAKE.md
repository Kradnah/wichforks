# Collecting reports from public threads

The guide does not run a scheduled scraper over subreddits. Reddit's terms restrict automated collection, rate limits make polling unreliable, and a bot that republishes posts would carry usernames, deleted content and sometimes game-file links into the repo. A report also needs a human check before it can change a recommendation.

Instead, `scripts/import_reddit.py` reads one thread on demand and writes review candidates. It does not crawl a subreddit, follow pagination, run on a schedule, or commit anything.

## Run it on one thread

```bash
python -I scripts/import_reddit.py "https://www.reddit.com/r/switch2emulation/comments/abc123/example/"
```

If Reddit blocks the request, save the thread's JSON from a browser session and pass the file:

```bash
python -I scripts/import_reddit.py --file thread.json --out data/reports/inbox
```

The script writes one JSON file per candidate to `data/reports/inbox/`, which is gitignored. It extracts:

- game
- fork, when the thread names one
- build tag
- CPU, GPU and RAM
- FPS range or single value
- date and source URL
- a short evidence snippet

It keeps a candidate only when it finds a game, an FPS value and a CPU or GPU. A comment that quotes another post can still produce a duplicate, so review every file.

## Review before publishing

1. Open the candidate and the linked comment. Confirm it is first-hand. Drop "I heard" or "a friend" claims.
2. Fill missing fields from the thread. Set `fork_id` to an id in `data/forks.json`, choose a `status`, and use the date of the report. The script uses the comment date.
3. Remove usernames, personal information, and any ROM, key, firmware or download link from `evidence`.
4. Rename the file to `data/reports/YYYY-MM-DD-<fork-id>-<slug>.json`, move it there, and set `reporter` to your GitHub handle.
5. Run:

```bash
python -I scripts/reports.py validate
python -I scripts/reports.py render
```

## What the script will not do

- Crawl a subreddit or a user profile.
- Page through a subreddit or search results.
- Store deleted or private content.
- Run on a schedule or open a pull request.
- Treat a candidate as a published report.

To watch several subreddits, use Reddit's own search alerts, then feed one relevant thread at a time into the script. That keeps the volume and the personal data under control.
