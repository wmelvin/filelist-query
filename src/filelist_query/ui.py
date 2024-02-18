from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Label, Static, TabbedContent, TabPane

from filelist_query.data import get_db_file


class FileTab(TabPane):
    def compose(self) -> ComposeResult:
        yield Static("File", classes="tab-content")

class FieldsTab(TabPane):
    def compose(self) -> ComposeResult:
        yield Static("Fields", classes="tab-content")


class CriteriaTab(TabPane):
    def compose(self) -> ComposeResult:
        yield Static("Criteria", classes="tab-content")


class QueryTab(TabPane):
    def compose(self) -> ComposeResult:
        yield Static("Query", classes="tab-content")


class ResultsTab(TabPane):
    def compose(self) -> ComposeResult:
        yield Label("Results", classes="tab-content", id="results-content")


class UI(App):
    BINDINGS = [
        ("x", "exit_app", "eXit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]
    CSS_PATH = "style.tcss"

    def __init__(self, db_file: str | Path = None):
        if db_file is None:
            self._db_file = get_db_file()
        elif isinstance(db_file, str):
            self._db_file = Path(db_file)
        else:
            self._db_file = db_file
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with TabbedContent(initial="fields"):
            yield FileTab("File", id="file")
            yield FieldsTab("Fields", id="fields")
            yield CriteriaTab("Criteria", id="criteria")
            yield QueryTab("Query", id="query")
            yield ResultsTab("Results", id="results")

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_exit_app(self) -> None:
        self.exit()

    @property
    def db_file(self) -> Path:
        return self._db_file


if __name__ == "__main__":
    ui = UI()
    # print(f"\n{ui.db_file = }")
    ui.run()
