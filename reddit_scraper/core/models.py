# reddit_scraper/core/models.py
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional, Iterator, Union

from pydantic import BaseModel, Field, ConfigDict


class Comment(BaseModel):
    id: str
    parent_id: str
    link_id: str
    author: Optional[str] = Field(None, description="Reddit username or None (deleted)")
    body: str
    created_utc: int
    score: int
    depth: int
    replies: List["Comment"] = []  # ← nested children

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Submission(BaseModel):
    id: str
    title: str
    selftext: str
    created_utc: int
    author: Optional[str] = None
    score: int
    num_comments: int
    link_flair_text: Optional[str] = None
    url: str
    permalink: str
    comments: List[Comment]

    # ------- Factory --------------------------------------------------- #
    @classmethod
    def from_pushshift_reddit(cls, raw_tree: dict) -> "Submission":
        return cls(
            **raw_tree["submission"],
            comments=[Comment(**c) for c in raw_tree["comments"]],
        )

    # ------- Serialization -------------------------------------------- #
    def to_json_line(self) -> str:
        obj = self.dict()
        return json.dumps(obj, ensure_ascii=False)


# -------- I/O helper ---------------------------------------------------- #
def export_ndjson(
    submissions: Union[Iterator[Submission], List[Submission]],
    outfile: Union[str, Path],
    append: bool = False,
) -> None:
    mode = "a" if append else "w"
    path = Path(outfile)
    with path.open(mode, encoding="utf-8") as fp:
        for sub in submissions:
            fp.write(sub.to_json_line() + "\n")
