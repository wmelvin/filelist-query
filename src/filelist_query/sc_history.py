from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, Label, ListItem, ListView, Markdown

from filelist_query.app_data import QueryAttrs


class HistoryScreen(Screen):
    def __init__(self) -> None:
        self._history_list: list[QueryAttrs] = []
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Button("Load", id="load-button"), Button("Close", id="close-button")
        )
        yield Markdown(id="sql-text")
        yield ListView(ListItem(Label("nada")), id="history-list")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "load-button":
            list_view = self.query_one(ListView)
            ix = list_view.index
            qa = self._history_list[ix]
            self.app.set_current_query_from_history(qa)

            # -- The query will be run against the current data file, so it
            #    does not matter whether the original file exists.
            #
            # if not (qa.data_file and Path(qa.data_file).exists()):
            #     md = self.query_one(Markdown)
            #     md.update(
            #         f"Selected query data file is not available:\n \n{qa.data_file}\n"
            #     )
            #     md.add_class("warning")
            #     return

            # TODO: Have the app load the selected history item.
            self.app.pop_screen()
        elif event.button.id == "close-button":
            self.app.pop_screen()

    def on_mount(self) -> None:
        self._history_list = self.app.get_history_list()
        if not self._history_list:
            return
        hist_list = self.query_one("#history-list")
        hist_list.clear()
        for qa in self._history_list:
            dt_str = qa.last_run_dt.strftime("%Y-%m-%d %H:%M")
            where_idx = qa.last_sql.lower().find("where")
            sql_substr = qa.last_sql[where_idx:] if where_idx > 0 else qa.last_sql
            hist_list.append(ListItem(Label(f"{dt_str} : {sql_substr[:50]}")))
        ix = hist_list.index
        self.show_sql(self._history_list[ix].last_sql)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        ix = event.list_view.index
        self.show_sql(self._history_list[ix].last_sql)

    def show_sql(self, sql: str) -> None:
        md = self.query_one(Markdown)
        md.remove_class("warning")
        md.update(f"\n```sql\n{sql}\n```")
