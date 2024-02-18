import os
import sqlite3
from pathlib import Path

import dotenv


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


def list_columns(con: sqlite3.Connection, table: str):
    cur = con.cursor()
    stmt = f"PRAGMA table_info({table});"
    rows = cur.execute(stmt).fetchall()
    cur.close()
    return [row[1] for row in rows]


def get_db_table_columns(db_path: Path, table: str):
    if db_path is None:
        return ["(no database file specified)"]
    con = sqlite3.connect(str(db_path))
    columns = list_columns(con, table)
    con.close()
    return columns
