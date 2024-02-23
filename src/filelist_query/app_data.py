from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from platformdirs import user_data_path

APP_NAME = "filelist_query"
APP_DATA_FILE = "filelist_query_data.json"


@dataclass
class PredicateAttrs:
    pred_type: str = ""
    column: str = ""
    condition: int = 0
    criteria: str = ""


class QueryAttrs:
    data_file: str = ""
    columns_selected: list[str]
    predicates: list[PredicateAttrs]
    default_sql: str
    last_sql: str
    last_run_dt: datetime

    def as_dict(self) -> dict:
        """Return a dictionary representation that is serializable to JSON."""
        d = self.__dict__
        d["last_run_dt"] = self.last_run_dt.isoformat()
        d["predicates"] = [p.__dict__ for p in self.predicates]
        return d

    def from_dict(self, dict_from_json: dict) -> None:
        """Set attributes from a dictionary deserialized from JSON."""
        self.data_file = dict_from_json["data_file"]
        self.columns_selected = dict_from_json["columns_selected"]
        self.predicates = [PredicateAttrs(**p) for p in dict_from_json["predicates"]]
        self.default_sql = dict_from_json["default_sql"]
        self.last_sql = dict_from_json["last_sql"]
        self.last_run_dt = datetime.fromisoformat(dict_from_json["last_run_dt"])


class AppData:
    def __init__(self):
        self.current_query: QueryAttrs = QueryAttrs()

    @classmethod
    def app_data_path(self, do_create: bool = False) -> Path | None:
        p = user_data_path(APP_NAME, appauthor=False, ensure_exists=do_create)
        if p.exists():
            return p
        return None

    def save(self) -> None:
        p = self.app_data_path(True)
        if p:
            data_file = p / APP_DATA_FILE
            with data_file.open("w") as f:
                json.dump(self.current_query.as_dict(), f, indent=4)

    def load(self) -> None:
        p = self.app_data_path()
        if p:
            data_file = p / APP_DATA_FILE
            if data_file.exists():
                with data_file.open("r") as f:
                    d = json.load(f)
                    self.current_query.from_dict(d)
