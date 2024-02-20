from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from platformdirs import user_data_path

APP_NAME = "filelist_query"


@dataclass
class PredicateAttrs:
    pred_type: str = ""
    field: str = ""
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


class AppData:
    def __init__(self):
        self.current_query: QueryAttrs | None = None

    @classmethod
    def app_data_path(self) -> Path | None:
        p = user_data_path(APP_NAME, appauthor=False)
        if p.exists():
            return p
        return None
