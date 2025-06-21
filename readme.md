# Reddit Scraper — quick start

A tiny command-line tool that downloads every **submission + full comment tree**
from a subreddit during a date range.  
Output = newline-delimited JSON (optional CSVs).

---

## 1 Prerequisites

| What                         | Why                                                               |
| ---------------------------- | ----------------------------------------------------------------- |
| Python ≥ 3.9                 | runtime                                                           |
| A **Reddit script-type app** | yields the `client_id` and `client_secret` you must put in `.env` |

### How to create the Reddit app (60 sec)

1. Log in on reddit.com and open **[ prefs / apps ](https://www.reddit.com/prefs/apps)**
2. Click **“Create app”**
3. Choose **script**
4. Fill **name** (anything), **redirect URI** → `http://localhost` (unused for scripts)
5. Click **create** – you’ll see:
   - a **14 or 22-char string** under the app name → **client ID**
   - a long **secret** string
6. Keep that tab open; you’ll copy both into `.env`.

---

## 2 Install (editable dev mode)

```bash
git clone https://github.com/your-org/reddit_scraper.git
cd reddit_scraper
python -m venv .venv && source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -U pip
python -m pip install -e .                                # pulls necessary dependencies of the project
```

````

> Need prod-only? run `python -m pip install .` instead of `-e`.

---

## 3 Credentials

Create a tiny **`.env`** file in the project root:

```dotenv
REDDIT_CLIENT_ID=xxxxxxxxxxxxxx                 # ← copy the 14 or 22-char ID
REDDIT_CLIENT_SECRET=yyyyyyyyyyyyyyyyyyyyyyyyyy # ← copy the long secret
REDDIT_USER_AGENT=reddit_scraper/0.1 by <your_username>
```

_(Nothing else is required; the scraper loads `.env` automatically.)_

---

## 4 Run a scrape

```bash
# syntax: reddit-scraper <subreddit> <start> <end> [flags]
python -m reddit_scraper.cli python 2025-06-15 2025-06-20 \
  --min-score 10 \
  --csv
```

Flag cheat-sheet:

| Flag                      | Meaning                                                 |
| ------------------------- | ------------------------------------------------------- |
| `--min-score N`           | skip posts with score < N                               |
| `--flair "Help,Question"` | include only those flairs (comma-sep, case-insensitive) |
| `--csv`                   | also write `*_submissions.csv` & `*_comments.csv`       |
| `--progress-db my.sqlite` | alternate checkpoint file                               |
| `--log-level DEBUG`       | verbose logging                                         |

Rerun the **same command** any time; already-saved IDs are skipped.

---

## 5 Sample one-liner

```bash
python -m reddit_scraper.cli learnpython 2025-06-20 2025-06-20 --min-score 5
```

Expected files:

```
output.ndjson
progress.sqlite
output_submissions.csv   # if --csv given
output_comments.csv
```

Happy scraping 🎉

````
