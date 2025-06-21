# reddit_scraper/services/txt_export.py
"""
Convert an ND-JSON file (one submission per line) into **individual** TXT files.

Called programmatically by the CLI.
"""

from __future__ import annotations

import json, re
from pathlib import Path
from textwrap import indent, wrap
from typing import Any, Dict

LINE_WIDTH = 100
INDENT = "    "


def _sanitize(s: str) -> str:
    return re.sub(r"[^\w\-]+", "_", s.strip())[:80] or "submission"


def _wrap(t: str) -> str:
    return "\n".join(wrap(t, LINE_WIDTH)) if t else ""


def _fmt(c: Dict[str, Any], depth: int = 0) -> str:
    pad = INDENT * depth
    header = f"[+{c['score']}] {c.get('author') or '[deleted]'}:"
    body = _wrap(c["body"])
    block = "\n".join([header, body] if body else [header])
    out = indent(block, pad)
    for r in c.get("replies", []):
        out += "\n" + _fmt(r, depth + 1)
    return out


def ndjson_to_txt(ndjson_path: str | Path, out_dir: str | Path) -> None:
    ndjson_path = Path(ndjson_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with ndjson_path.open(encoding="utf-8") as fp:
        for line in fp:
            tree = json.loads(line)
            fname = f"{tree['id']}_{_sanitize(tree['title'])}.txt"
            path = out_dir / fname
            with path.open("w", encoding="utf-8") as out:
                out.write(f"{tree['title']}\n{'-'*len(tree['title'])}\n")
                meta = (
                    f"Author: {tree.get('author') or '[deleted]'} | "
                    f"Score: {tree['score']} | Flair: {tree.get('link_flair_text')}\n\n"
                )
                out.write(meta)
                body = _wrap(tree["selftext"])
                if body:
                    out.write(body + "\n\n")
                out.write("Comments\n--------\n")
                for c in tree["comments"]:
                    out.write(_fmt(c) + "\n")
