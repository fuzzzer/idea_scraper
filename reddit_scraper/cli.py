# reddit_scraper/cli.py
import argparse
import logging
from pathlib import Path
from typing import List, Optional

from reddit_scraper.logging_setup import setup_logging
from reddit_scraper.services.csv_export import ndjson_to_csv
from reddit_scraper.services.scraper import Scraper


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="reddit-scraper",
        description="Fetch subreddit submissions (and all comments) for a date range.",
    )
    p.add_argument("subreddit", help="Subreddit name without the r/ prefix")
    p.add_argument("start_date", help="ISO-8601 start date (e.g. 2024-01-01)")
    p.add_argument("end_date", help="ISO-8601 end date   (e.g. 2024-01-31)")
    p.add_argument("--min-score", type=int, default=None, help="Only keep posts with ≥ N score")
    p.add_argument(
        "--flair",
        type=str,
        help="Comma-separated list of flairs to include (case-insensitive)",
    )
    p.add_argument("--csv", action="store_true", help="Also export flattened CSV files")
    p.add_argument(
        "-o", "--output", default="output.ndjson", help="ND-JSON output file (default: output.ndjson)"
    )
    p.add_argument(
        "--progress-db",
        default="progress.sqlite",
        help="SQLite file for checkpoints (default: progress.sqlite)",
    )
    p.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Console log level (default: INFO)",
    )
    p.add_argument("--log-file", help="Optional path to a rotating log file")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    setup_logging(args.log_level, args.log_file)
    logging.getLogger(__name__).debug("CLI args: %s", vars(args))  # type: ignore[arg-type]

    flair_list: Optional[List[str]] = (
        [f.strip() for f in args.flair.split(",")] if args.flair else None
    )

    scraper = Scraper(
        subreddit=args.subreddit,
        start_date=args.start_date,
        end_date=args.end_date,
        output=Path(args.output),
        min_score=args.min_score,
        flairs=flair_list,
        progress_db=args.progress_db,
    )
    scraper.run()

    if args.csv:
        logging.info("Starting CSV export…")
        ndjson_to_csv(args.output)
        logging.info("CSV export complete.")


if __name__ == "__main__":
    main()
