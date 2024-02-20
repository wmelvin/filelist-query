from textual.app import ComposeResult
from textual.widgets import DataTable, TabPane


class ResultsTab(TabPane):
    def compose(self) -> ComposeResult:
        yield DataTable(id="results-table")
