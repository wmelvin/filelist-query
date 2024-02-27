from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, Label, ListItem, ListView, TextArea


class HistoryScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Button("Load", id="load-button"), Button("Close", id="close-button")
        )
        text_area = TextArea.code_editor(
            "", language="sql", show_line_numbers=False, id="sql-text"
        )
        yield text_area
        yield ListView(ListItem(Label("nada")), id="history-list")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "load-button":
            # TODO: load the selected history item.
            self.app.pop_screen()
        elif event.button.id == "close-button":
            self.app.pop_screen()
