# reddit_scraper/services/csv_export.py
from __future__ import annotations

import json
from pathlib import Path
from typing import List

import pandas as pd
from tqdm import tqdm


def ndjson_to_csv(
    ndjson_path: str | Path,
    submissions_csv: str | Path,
    comments_csv: str | Path,
    chunk_size: int = 2_000,
) -> None:
    """
    Convert an ND-JSON file (one submission-tree per line) into two flat CSVs.

    * submissions_csv  – one row per post
    * comments_csv     – one row per comment (with submission_id column)
    """
    ndjson_path   = Path(ndjson_path)
    submissions_csv = Path(submissions_csv)
    comments_csv    = Path(comments_csv)

    submissions_csv.parent.mkdir(parents=True, exist_ok=True)

    # truncate / create
    submissions_csv.write_text("")
    comments_csv.write_text("")

    sub_rows: List[dict] = []
    com_rows: List[dict] = []

    with ndjson_path.open(encoding="utf-8") as fp:
        for line in tqdm(fp, desc="Converting → CSV"):
            tree = json.loads(line)

            # submission row (drop comments)
            sub_rows.append({k: v for k, v in tree.items() if k != "comments"})

            # comment rows
            for c in tree["comments"]:
                com_rows.append({"submission_id": tree["id"], **c})

            if len(sub_rows) >= chunk_size:
                _flush(sub_rows, submissions_csv)
                _flush(com_rows, comments_csv)

    # remainder
    _flush(sub_rows, submissions_csv)
    _flush(com_rows, comments_csv)


def _flush(rows: List[dict], outfile: Path) -> None:
    if not rows:
        return
    header = not outfile.exists() or outfile.stat().st_size == 0
    pd.DataFrame.from_records(rows).to_csv(outfile, mode="a",
                                           header=header, index=False)
    rows.clear()
