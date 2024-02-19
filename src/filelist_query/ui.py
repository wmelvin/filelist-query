from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static, TabbedContent, TabPane

from filelist_query.data import get_db_file
from filelist_query.tab_criteria import CriteriaTab
from filelist_query.tab_fields import FieldsTab
from filelist_query.tab_query import QueryTab
from filelist_query.tab_results import ResultsTab


class FileTab(TabPane):
    def compose(self) -> ComposeResult:
        yield Static("File", classes="tab-content")


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
        with TabbedContent(initial="fields-tab"):
            yield FileTab("File", id="file-tab")
            yield FieldsTab("Fields", id="fields-tab")
            yield CriteriaTab("Criteria", id="criteria-tab")
            yield QueryTab("Query", id="query-tab")
            yield ResultsTab("Results", id="results-tab")

    def update_criteria(self):
        criteria_tab = self.query_one("#criteria-tab")
        criteria_tab.update_fields()

    def update_query(self):
        fields_tab = self.query_one("#fields-tab")
        selected_fields = fields_tab.get_selected_fields()
        criteria_tab = self.query_one("#criteria-tab")
        predicates = criteria_tab.get_predicates_str()
        query_text = self.query_one("#query-text")
        query_text.text = (
            f"SELECT {', '.join(selected_fields)}\nFROM view_filelist\n"
            f"WHERE {predicates}"
        )

    def update_results(self):
        fields_tab = self.query_one("#fields-tab")
        # criteria_tab = self.query_one("#criteria-tab")
        results_table = self.query_one("#results-table")
        selected_fields = fields_tab.get_selected_fields()
        # predicates = criteria_tab.get_predicates()
        results_table.clear(columns=True)
        results_table.add_columns(*selected_fields)

    def on_tabbed_content_tab_activated(
        self, event: TabbedContent.TabActivated
    ) -> None:
        label = event.tab.label.plain
        self.title = f"Tab: {label}"
        if label == "Results":
            self.update_results()
        elif label == "Query":
            self.update_query()
        elif label == "Criteria":
            self.update_criteria()

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
