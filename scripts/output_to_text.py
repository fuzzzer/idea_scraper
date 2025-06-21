# scripts/output_to_text.py
"""
Turn ../output.ndjson into human-readable .txt files (one per submission)
inside ../outputs/conversations/.

Simply run:
    python scripts/output_to_text.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import indent, wrap
from typing import Any, Dict

# -------- paths ----------------------------------------------------------- #
BASE = Path(__file__).parent.parent          # project root (..)
INPUT_NDJSON = BASE / "output.ndjson"        # produced by the scraper
OUTPUT_DIR = BASE / "outputs" / "conversations"           # where .txt files land

LINE_WIDTH = 100      # wrap columns
INDENT = "    "       # four spaces per depth


# -------- helpers --------------------------------------------------------- #
def _sanitize(text: str) -> str:
    """Make a chunk safe for filenames."""
    return re.sub(r"[^\w\-]+", "_", text.strip())[:80] or "submission"


def _wrap(text: str) -> str:
    return "\n".join(wrap(text, LINE_WIDTH)) if text else ""


def _fmt_comment(c: Dict[str, Any], depth: int = 0) -> str:
    pad = INDENT * depth
    header = f"[+{c['score']}] {c.get('author') or '[deleted]'}:"
    body = _wrap(c["body"])
    block = "\n".join([header, body] if body else [header])
    out = indent(block, pad)

    for reply in c.get("replies", []):
        out += "\n" + _fmt_comment(reply, depth + 1)
    return out


# -------- main ------------------------------------------------------------ #
def convert() -> None:
    if not INPUT_NDJSON.exists():
        raise FileNotFoundError(
            f"{INPUT_NDJSON} not found – run the scraper first or adjust the path."
        )

    OUTPUT_DIR.mkdir(exist_ok=True)

    with INPUT_NDJSON.open(encoding="utf-8") as fp:
        for line in fp:
            tree = json.loads(line)
            title = tree["title"]
            fname = f"{tree['id']}_{_sanitize(title)}.txt"
            path = OUTPUT_DIR / fname

            with path.open("w", encoding="utf-8") as out:
                # header
                out.write(f"{title}\n{'-'*len(title)}\n")
                meta = (
                    f"Author: {tree.get('author') or '[deleted]'} | "
                    f"Score: {tree['score']} | "
                    f"Flair: {tree.get('link_flair_text')}\n\n"
                )
                out.write(meta)

                # body
                body = _wrap(tree["selftext"])
                if body:
                    out.write(body + "\n\n")

                # comments
                out.write("Comments\n--------\n")
                for c in tree["comments"]:
                    out.write(_fmt_comment(c) + "\n")

            print("✓", path.relative_to(BASE))


if __name__ == "__main__":
    convert()
