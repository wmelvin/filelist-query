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
from filelist_query.sc_history import HistoryScreen
from filelist_query.tab_columns import ColumnsTab
from filelist_query.tab_criteria import CriteriaTab
from filelist_query.tab_query import QueryTab
from filelist_query.tab_results import ResultsTab


class FileTab(TabPane):
    def compose(self) -> ComposeResult:
        yield Static("File", classes="tab-content")


class UI(App):
    BINDINGS = [
        Binding("ctrl+x", "exit_app", "eXit", priority=True),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("h", "load_history", "load History"),
    ]
    CSS_PATH = "style.tcss"

    def __init__(self, db_file: str | Path = None, do_load: bool = True):
        self._do_load_app_data = do_load
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
        with TabbedContent(initial="columns-tab"):
            yield FileTab("File", id="file-tab")
            yield ColumnsTab("Columns", id="columns-tab")
            yield CriteriaTab("Criteria", id="criteria-tab")
            yield QueryTab("Query", id="query-tab")
            yield ResultsTab("Results", id="results-tab")
        yield Footer()

    def on_mount(self) -> None:
        if self._do_load_app_data:
            self._app_data.load()
        if self._app_data.current_query.last_sql:
            query_text = self.query_one("#query-text")
            query_text.text = self._app_data.current_query.last_sql
        columns_tab = self.query_one("#columns-tab")
        columns_tab.set_columns(self._app_data.current_query)
        if self._app_data.current_query.predicates:
            criteria_tab = self.query_one("#criteria-tab")
            criteria_tab.set_predicates(self._app_data.current_query.predicates)
        # TODO: Set other tab data from AppData.

    def update_criteria(self):
        criteria_tab = self.query_one("#criteria-tab")
        criteria_tab.sync_predicates()
        # criteria_tab.update_predicates_columns()

    def update_query(self):
        columns_tab = self.query_one("#columns-tab")
        selected_columns = columns_tab.get_selected_columns()
        criteria_tab = self.query_one("#criteria-tab")
        predicates = criteria_tab.get_predicates_str()
        query_text = self.query_one("#query-text")
        query_text.text = (
            f"SELECT {', '.join(selected_columns)}\nFROM view_filelist\n"
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
        msg, err = populate_data_table(self.db_file, results_table, text)
        self.title = f"{msg} {err}"
        # TODO: Something other than showing the error in the title.
        if not err:
            self.update_app_data()
            self._app_data.add_to_history()

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

    def action_load_history(self) -> None:
        self.push_screen(HistoryScreen())

    def action_exit_app(self) -> None:
        self.exit()

    def bypass_selections(self, default_sql: str) -> None:
        if default_sql:
            self._bypass_selections = True
            self._default_sql = default_sql

    def update_app_data(self) -> None:
        columns_tab = self.query_one("#columns-tab")
        criteria_tab = self.query_one("#criteria-tab")
        query_text = self.query_one("#query-text")

        qry = QueryAttrs()
        qry.data_file = str(self.db_file)
        qry.columns_selected = columns_tab.get_selected_columns()
        qry.predicates = criteria_tab.get_predicates()
        qry.default_sql = self._default_sql
        qry.last_sql = query_text.text
        qry.last_run_dt = self._app_data.current_query.last_run_dt or datetime.now(
            timezone.utc
        )
        # TODO: Set when query is run.

        self._app_data.current_query = qry

    def save_app_data(self) -> None:
        self.update_app_data()
        self._app_data.save()

    @property
    def db_file(self) -> Path:
        return self._db_file


if __name__ == "__main__":
    ui = UI()
    # print(f"\n{ui.db_file = }")
    ui.bypass_selections(get_default_sql())
    ui.run()
