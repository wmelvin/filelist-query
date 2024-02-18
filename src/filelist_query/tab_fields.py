from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, OptionList, TabPane
from textual.widgets.option_list import Option

from filelist_query.data import get_db_table_columns


class FieldsTab(TabPane):
    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        yield Horizontal(
            OptionList(id="field_list"),
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

    def on_mount(self) -> None:
        field_list = self.query_one("#field_list")
        fields = get_db_table_columns(self.app.db_file, "view_filelist")
        for field in fields:
            field_list.add_option(Option(field))
            #  Add file_name by default.
            if field == "file_name":
                self.select_field("file_name")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "field_list":
            self.title = f"Field: {event.option.prompt}"
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
            field_list = self.query_one("#field_list")
            ix = field_list.highlighted
            if ix is not None:
                sel = field_list.get_option_at_index(ix).prompt
                self.select_field(sel)
        elif event.button.id == "remove":
            selected_list = self.query_one("#selected_list")
            ix = selected_list.highlighted
            if ix is not None:
                selected_list.remove_option_at_index(ix)
        elif event.button.id == "up":
            self.swap_prompt(False)
        elif event.button.id == "down":
            self.swap_prompt(True)

    def is_selected(self, field: str) -> bool:
        selected_list = self.query_one("#selected_list")
        for ix in range(selected_list.option_count):
            if selected_list.get_option_at_index(ix).prompt == field:
                return True
        return False

    def select_field(self, field: str) -> None:
        if self.is_selected(field):
            return
        selected_list = self.query_one("#selected_list")
        selected_list.add_option(Option(field))

    def get_selected_fields(self) -> list[str]:
        selected_list = self.query_one("#selected_list")
        return [
            selected_list.get_option_at_index(ix).prompt
            for ix in range(selected_list.option_count)
        ]
