from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, OptionList, TabPane
from textual.widgets.option_list import Option

from filelist_query.data import DbColumnInfo, get_db_table_columns


class ColumnsTab(TabPane):
    def __init__(self, title, id) -> None:  # noqa: A002
        super().__init__(title, id=id)
        self._data_columns: list[DbColumnInfo] = None

    def compose(self) -> ComposeResult:
        yield Horizontal(
            OptionList(id="column_list"),
            VerticalScroll(
                Button("Add", id="add"),
                Button("Remove", id="remove"),
                id="buttonbar1",
                classes="buttonbar",
            ),
            OptionList(id="selected_list"),
            VerticalScroll(
                Button("Up", id="up"),
                Button("Down", id="down"),
                id="buttonbar2",
                classes="buttonbar",
            ),
        )

    def _load_column_info(self) -> None:
        self._data_columns = get_db_table_columns(self.app.db_file, "view_filelist")

    def on_mount(self) -> None:
        self._load_column_info()
        column_list = self.query_one("#column_list")
        for column in self._data_columns:
            column_list.add_option(Option(column.name))
            #  Add file_name by default.
            if column.name == "file_name":
                self.select_column("file_name")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "column_list":
            self.title = f"Column: {event.option.prompt}"
            self.query_one("#add").add_class("active")
            self.query_one("#remove").remove_class("active")
            self.query_one("#up").remove_class("active")
            self.query_one("#down").remove_class("active")
        elif event.option_list.id == "selected_list":
            self.title = f"Selected: {event.option.prompt}"
            self.query_one("#add").remove_class("active")
            self.query_one("#remove").add_class("active")
            self.query_one("#up").add_class("active")
            self.query_one("#down").add_class("active")

    # There is no direct access to the list of options, so swapping the
    # prompt seems to be the way to move items (prompts) up and down.
    def swap_prompt(self, move_down: bool) -> None:
        opt_list = self.query_one("#selected_list")
        ix_a = opt_list.highlighted
        if ix_a is None:
            return
        ix_b = ix_a + 1 if move_down else ix_a - 1
        if ix_b < 0 or ix_b >= opt_list.option_count:
            return
        temp = opt_list.get_option_at_index(ix_a).prompt
        opt_list.replace_option_prompt_at_index(
            ix_a, opt_list.get_option_at_index(ix_b).prompt
        )
        opt_list.replace_option_prompt_at_index(ix_b, temp)
        opt_list.highlighted = ix_b

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if not event.button.has_class("active"):
            return
        if event.button.id == "add":
            column_list = self.query_one("#column_list")
            ix = column_list.highlighted
            if ix is not None:
                sel = column_list.get_option_at_index(ix).prompt
                self.select_column(sel)
        elif event.button.id == "remove":
            selected_list = self.query_one("#selected_list")
            ix = selected_list.highlighted
            if ix is not None:
                selected_list.remove_option_at_index(ix)
        elif event.button.id == "up":
            self.swap_prompt(False)
        elif event.button.id == "down":
            self.swap_prompt(True)

    def is_selected(self, column: str) -> bool:
        selected_list = self.query_one("#selected_list")
        for ix in range(selected_list.option_count):
            if selected_list.get_option_at_index(ix).prompt == column:
                return True
        return False

    def select_column(self, column: str) -> None:
        if self.is_selected(column):
            return
        selected_list = self.query_one("#selected_list")
        selected_list.add_option(Option(column))

    def get_selected_columns(self) -> list[str]:
        selected_list = self.query_one("#selected_list")
        return [
            selected_list.get_option_at_index(ix).prompt
            for ix in range(selected_list.option_count)
        ]

    def get_all_columns(self) -> list[str]:
        return [col.name for col in self._data_columns]

    def get_column_type(self, column_name: str) -> str:
        for col in self._data_columns:
            if col.name == column_name:
                return col.datatype
        return None
