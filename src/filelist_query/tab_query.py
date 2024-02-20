from textual.app import ComposeResult
from textual.widgets import TabPane, TextArea


class QueryTab(TabPane):
    def compose(self) -> ComposeResult:
        text_area = TextArea.code_editor(
            "", language="sql", show_line_numbers=False, id="query-text"
        )
        yield text_area
