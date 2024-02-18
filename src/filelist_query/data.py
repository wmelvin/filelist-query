from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path

import dotenv


@dataclass
class DbColumnInfo:
    name: str
    type: str


def get_db_file() -> Path:
    dotenv.load_dotenv()
    file_name = os.environ.get("FILELIST_QUERY_DEFAULT_FILE")
    if file_name:
        p = Path(file_name)
        if p.exists():
            return p
        raise FileNotFoundError(f"File not found: {file_name}")
    dir_name = os.environ.get("FILELIST_QUERY_DIR_LATEST")
    if dir_name:
        p = Path(dir_name).expanduser().resolve()
        if p.exists():
            files = list(p.glob("*.sqlite"))
            files.sort(key=lambda x: x.stat().st_mtime)
            if files:
                return files[-1]
            raise FileNotFoundError(f"No sqlite files in {dir_name}")
        raise FileNotFoundError(f"Directory not found: {dir_name}")
    return None


def list_columns(con: sqlite3.Connection, table: str) -> list[DbColumnInfo]:
    cur = con.cursor()
    # https://www.sqlite.org/pragma.html#pragma_table_info
    stmt = f"PRAGMA table_info({table});"
    rows = cur.execute(stmt).fetchall()
    cur.close()
    return [DbColumnInfo(row[1], row[2]) for row in rows]


def get_db_table_columns(db_path: Path, table: str) -> list[DbColumnInfo]:
    if db_path is None:
        return ["(no database file specified)"]
    con = sqlite3.connect(str(db_path))
    columns = list_columns(con, table)
    con.close()
    return columns
