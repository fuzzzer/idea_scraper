# reddit_scraper/services/csv_export.py
from __future__ import annotations

import json
from pathlib import Path
from typing import List

import pandas as pd
from tqdm import tqdm


def ndjson_to_csv(
    ndjson_path: str | Path,
    submissions_csv: str | Path | None = None,
    comments_csv: str | Path | None = None,
    chunk_size: int = 2_000,
) -> None:
    """
    Convert an ND-JSON file (one submission-tree per line)
    into two flat CSV files:

    * <prefix>_submissions.csv
    * <prefix>_comments.csv
    """
    ndjson_path = Path(ndjson_path)
    base = ndjson_path.with_suffix("")

    submissions_csv = Path(submissions_csv or f"{base}_submissions.csv")
    comments_csv = Path(comments_csv or f"{base}_comments.csv")

    # ----- prepare output files (truncate if they exist) ----------
    submissions_csv.write_text("")
    comments_csv.write_text("")

    sub_rows: List[dict] = []
    com_rows: List[dict] = []
    with ndjson_path.open(encoding="utf-8") as fp:
        for line in tqdm(fp, desc="Converting → CSV"):
            tree = json.loads(line)

            # submission row (comments list removed)
            sub = {k: v for k, v in tree.items() if k != "comments"}
            sub_rows.append(sub)

            # comment rows inherit the submission id for easy joins
            for c in tree["comments"]:
                com_rows.append({"submission_id": tree["id"], **c})

            # write in manageable chunks
            if len(sub_rows) >= chunk_size:
                _append_chunk(sub_rows, submissions_csv)
                _append_chunk(com_rows, comments_csv)
                sub_rows.clear()
                com_rows.clear()

    # flush any remainder
    if sub_rows:
        _append_chunk(sub_rows, submissions_csv)
        _append_chunk(com_rows, comments_csv)


def _append_chunk(rows: List[dict], outfile: Path) -> None:
    """Append a list of dicts as CSV (header only on first write)."""
    header = not outfile.exists() or outfile.stat().st_size == 0
    df = pd.DataFrame.from_records(rows)
    df.to_csv(outfile, mode="a", header=header, index=False)
