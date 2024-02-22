from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from platformdirs import user_data_path

APP_NAME = "filelist_query"


@dataclass
class PredicateAttrs:
    pred_type: str = ""
    column: str = ""
    condition: int = 0
    criteria: str = ""


class QueryAttrs:
    data_file: str = ""
    columns_all: list[str]
    columns_selected: list[str]
    predicates: list[PredicateAttrs]
    default_sql: str
    last_sql: str
    last_run_dt: datetime

    def as_dict(self) -> dict:
        d = self.__dict__
        d["last_run_dt"] = self.last_run_dt.isoformat()
        d["predicates"] = [p.__dict__ for p in self.predicates]
        return d


class AppData:
    def __init__(self):
        self.current_query: QueryAttrs | None = None

    @classmethod
    def app_data_path(self, do_create: bool = False) -> Path | None:
        p = user_data_path(APP_NAME, appauthor=False, ensure_exists=do_create)
        if p.exists():
            return p
        return None

    def save(self) -> None:
        p = self.app_data_path(True)
        if p:
            data_file = p / "filelist_query_data.json"
            with data_file.open("w") as f:
                json.dump(self.current_query.as_dict(), f, indent=4)
