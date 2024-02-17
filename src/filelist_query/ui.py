from __future__ import annotations

from pathlib import Path

from textual.app import App


class UI(App):
    def __init__(self, db_file:str|Path = None):
        if db_file is None:
            self._db_file = None  # TODO: get_db_file()
        elif isinstance(db_file, str):
            self._db_file = Path(db_file)
        else:
            self._db_file = db_file
        super().__init__()

    @property
    def db_file(self) -> Path:
        return self._db_file
