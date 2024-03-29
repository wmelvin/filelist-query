from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path

import dotenv
from textual.widgets import DataTable

RESULT_ROW_LIMIT = 2000


@dataclass
class DbColumnInfo:
    name: str
    datatype: str


def run_sql(cur: sqlite3.Cursor, stmt: str, data=None):
    try:
        if data:
            cur.execute(stmt, data)
        else:
            cur.execute(stmt)
    except Exception as e:
        print("\n{}\n".format(stmt))
        raise e


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


def get_default_sql() -> str:
    dotenv.load_dotenv()
    return os.environ.get("FILELIST_QUERY_DEFAULT_SQL")


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


def populate_data_table(
    db_file: Path, data_table: DataTable, stmt: str
) -> tuple[str, str]:
    """Populate a DataTable with the results of a SQL statement.
    The DataTable should be empty before calling this function.

    This function does the following:
    * Opens a connection to the database file.
    * Executes the SQL statement.
    * Adds the columns to the DataTable.
    * Adds the rows to the DataTable.
    * Closes the connection to the database file.
    * Returns a tuple of messages and errors.

    params: db_file: pathlib.Path
    params: data_table: textual.widgets.DataTable
    params: stmt: str
    return: tuple[str, str]
    """
    msg = ""
    err = ""
    mtime_before = db_file.stat().st_mtime
    con = sqlite3.connect(str(db_file))
    cur = con.cursor()
    try:
        run_sql(cur, stmt)
        columns = [x[0] for x in cur.description]
        data_table.add_columns(*columns)
        for row in cur.fetchmany(RESULT_ROW_LIMIT):
            data_table.add_row(*row)
        row_count = data_table.row_count
        msg = f"Rows returned = {row_count}"
        if row_count >= RESULT_ROW_LIMIT:
            msg += f" (limit of {RESULT_ROW_LIMIT} rows reached)"
    except sqlite3.OperationalError as e:
        err = f"ERROR in SQL: {e}"
    finally:
        cur.close()
        con.rollback()
        con.close()
        # The SQLite database file should not be modified.
        assert db_file.stat().st_mtime == mtime_before  # noqa: S101
    return (msg, err)


def exclude_dirs_clause() -> str:
    """Return a string that can be used in a WHERE clause to exclude certain
    directories from the query results.

    Excludes:
    * Work-in-progress backup directories (_0_bak).
    * Syncthing backup directories (.stversions).
    """
    exclude = ["dir_name not like '_0_bak'", "dir_name not like '.stversions'"]
    return "".join([f" and ({x})" for x in exclude])
