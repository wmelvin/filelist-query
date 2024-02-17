from __future__ import annotations

from pathlib import Path

from textual.app import App

from filelist_query.data import get_db_file


class UI(App):
    def __init__(self, db_file: str | Path = None):
        if db_file is None:
            self._db_file = get_db_file()
        elif isinstance(db_file, str):
            self._db_file = Path(db_file)
        else:
            self._db_file = db_file
        super().__init__()

    @property
    def db_file(self) -> Path:
        return self._db_file


if __name__ == "__main__":
    ui = UI()
    print(f"\n{ui.db_file = }")
