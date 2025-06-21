# Reddit Scraper — quick start

A tiny command-line tool that downloads every **submission + full comment tree**
from a subreddit during a date range.  
Output = newline-delimited JSON (and, if you want, CSVs / per-post TXT files
and a single _merged_ TXT)

---

## 1 Prerequisites

| What                         | Why                                                               |
| ---------------------------- | ----------------------------------------------------------------- |
| Python ≥ 3.9                 | runtime                                                           |
| A **Reddit script-type app** | yields the `client_id` and `client_secret` you must put in `.env` |

### How to create the Reddit app (60 sec)

1. Log in on reddit.com and open **[prefs / apps](https://www.reddit.com/prefs/apps)**
2. Click **“Create app”**
3. Choose **script**
4. Fill **name** (anything) & **redirect URI** → `http://localhost` (unused)
5. Click **Create** – you’ll see  
   • a 14- or 22-char string under the app name → **client ID**  
   • a long **secret**
6. Keep that tab open; you’ll copy both into `.env`.

---

## 2 Install (editable dev mode)

```bash
git clone https://github.com/your-org/reddit_scraper.git
cd reddit_scraper
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
python -m pip install -U pip
python -m pip install -e .                             # pulls project dependencies
```

---

## 3 Credentials

Create a tiny **`.env`** file in the project root:

```dotenv
REDDIT_CLIENT_ID=xxxxxxxxxxxxxx                 # ← copy the ID
REDDIT_CLIENT_SECRET=yyyyyyyyyyyyyyyyyyyyyyyyyy # ← copy the secret
REDDIT_USER_AGENT=reddit_scraper/0.1 by <your_username>
```

That’s it – the scraper autoloads the file.

---

## 4 Run a scrape

```bash
# syntax: reddit-scraper <subreddit> <start> <end> [flags]
python -m reddit_scraper.cli learnpython 2025-06-15 2025-06-20 \
  --min-score 2 \
  --csv \
  --txt \
  --merged
```

### Flag cheat-sheet

| Flag                      | Meaning / side effect                                        |
| ------------------------- | ------------------------------------------------------------ |
| `--min-score N`           | skip posts with score < N                                    |
| `--flair "A,B"`           | include only those flairs (comma-sep, case-insensitive)      |
| `--csv`                   | export two flat CSVs (`*_submissions.csv`, `*_comments.csv`) |
| `--txt`                   | export **per-post** TXT conversations                        |
| `--merged` (+ `--txt`)    | also create one big TXT with all conversations               |
| `--progress-db my.sqlite` | alternate checkpoint DB                                      |
| `--log-level DEBUG`       | verbose logging                                              |

> Re-run the **same command** at any time; already-saved IDs are skipped.

### Where the artefacts land

All outputs go under **`outputs/`**:

```
outputs/
├── data/                output_<sub>_<start>__<end>.ndjson
├── progress/            progress_<sub>_<start>__<end>.sqlite
├── csv/                 (only if --csv)  *_submissions.csv / *_comments.csv
└── txt/
    ├── conversations_<sub>_<start>__<end>/   # one TXT per post  (if --txt)
    └── all_conversations_<sub>_<start>__<end>.txt   # merged (if --merged)
```

---

## 5 Sample one-liner

```bash
python -m reddit_scraper.cli learnpython 2025-06-20 2025-06-20 --min-score 5 --txt
```

Look in `outputs/` for the freshly created files.

Happy scraping 🎉
