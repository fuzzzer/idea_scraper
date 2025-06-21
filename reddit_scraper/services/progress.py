# reddit_scraper/services/progress.py
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, List


class ProgressTracker:
    """
    Tracks which submission IDs have already been scraped.
    Uses a single-table SQLite DB (`progress.sqlite` by default).
    """

    def __init__(self, db_path: str | Path = "progress.sqlite") -> None:
        self.path = Path(db_path)
        self.conn = sqlite3.connect(self.path)
        self._ensure_schema()

    # --------- Public API ----------------------------------------

    def is_done(self, submission_id: str) -> bool:
        """True if that ID is already marked as processed."""
        cur = self.conn.execute(
            "SELECT 1 FROM completed WHERE id = ? LIMIT 1", (submission_id,)
        )
        return cur.fetchone() is not None

    def mark_done(self, submission_id: str) -> None:
        """Insert the ID (ignores duplicates)."""
        self.conn.execute(
            "INSERT OR IGNORE INTO completed (id) VALUES (?)", (submission_id,)
        )
        self.conn.commit()

    def mark_batch_done(self, ids: Iterable[str]) -> None:
        """Bulk-insert many IDs efficiently."""
        self.conn.executemany(
            "INSERT OR IGNORE INTO completed (id) VALUES (?)", ((i,) for i in ids)
        )
        self.conn.commit()

    def list_done(self) -> List[str]:
        """Return all completed IDs (rarely needed, but handy for debugging)."""
        cur = self.conn.execute("SELECT id FROM completed")
        return [row[0] for row in cur.fetchall()]

    def close(self) -> None:
        self.conn.close()

    # --------- Internals -----------------------------------------

    def _ensure_schema(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS completed (
                id TEXT PRIMARY KEY
            )
            """
        )
        self.conn.commit()

    # --------- Context-manager sugar -----------------------------

    def __enter__(self) -> "ProgressTracker":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
