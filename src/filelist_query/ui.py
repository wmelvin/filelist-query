from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, Static, TabbedContent, TabPane

from filelist_query.app_data import AppData, QueryAttrs
from filelist_query.data import (
    exclude_dirs_clause,
    get_db_file,
    get_default_sql,
    populate_data_table,
)
from filelist_query.tab_criteria import CriteriaTab
from filelist_query.tab_fields import FieldsTab
from filelist_query.tab_query import QueryTab
from filelist_query.tab_results import ResultsTab


class FileTab(TabPane):
    def compose(self) -> ComposeResult:
        yield Static("File", classes="tab-content")


class UI(App):
    BINDINGS = [
        Binding("ctrl+x", "exit_app", "eXit", priority=True),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]
    CSS_PATH = "style.tcss"

    def __init__(self, db_file: str | Path = None):
        self._bypass_selections: bool = False
        self._default_sql: str = ""
        self._app_data = AppData()
        if db_file is None:
            self._db_file = get_db_file()
        elif isinstance(db_file, str):
            self._db_file = Path(db_file)
        else:
            self._db_file = db_file
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial="fields-tab"):
            yield FileTab("File", id="file-tab")
            yield FieldsTab("Fields", id="fields-tab")
            yield CriteriaTab("Criteria", id="criteria-tab")
            yield QueryTab("Query", id="query-tab")
            yield ResultsTab("Results", id="results-tab")
        yield Footer()

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
            f"WHERE {predicates}\n{exclude_dirs_clause()}"
        )

    def update_results(self):
        query_tab = self.query_one("#query-tab")
        query_text = query_tab.query_one("#query-text")
        if self._bypass_selections:
            # Replace SQL in Querytab.
            query_text.text = self._default_sql
        text = query_text.text
        results_table = self.query_one("#results-table")
        results_table.clear(columns=True)
        msg = populate_data_table(self.db_file, results_table, text)
        if msg:
            self.title = msg
            # TODO: Something other than showing an error in the title.

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
        elif label == "File":
            # TODO: Temporary for initial development.
            self.save_app_data()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_exit_app(self) -> None:
        self.exit()

    def bypass_selections(self, default_sql: str) -> None:
        if default_sql:
            self._bypass_selections = True
            self._default_sql = default_sql

    def save_app_data(self) -> None:
        fields_tab = self.query_one("#fields-tab")
        criteria_tab = self.query_one("#criteria-tab")
        query_text = self.query_one("#query-text")

        qry = QueryAttrs()
        qry.data_file = str(self.db_file)
        qry.columns_all = fields_tab.get_all_fields()
        qry.columns_selected = fields_tab.get_selected_fields()
        qry.predicates = criteria_tab.get_predicates()
        qry.default_sql = self._default_sql
        qry.last_sql = query_text.text
        qry.last_run_dt = datetime.now(timezone.utc)  # TODO: Set when query is run.

        self._app_data.current_query = qry
        self._app_data.save()

    @property
    def db_file(self) -> Path:
        return self._db_file


if __name__ == "__main__":
    ui = UI()
    # print(f"\n{ui.db_file = }")
    ui.bypass_selections(get_default_sql())
    ui.run()
