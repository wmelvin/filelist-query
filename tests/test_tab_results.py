from filelist_query.ui import UI
from textual.widgets import DataTable


async def test_results_tab():
    app = UI()
    async with app.run_test() as pilot:
        rt = pilot.app.query_one("#results-tab")
        assert rt
        dt = rt.query_one("#results-table")
        assert dt
        assert isinstance(dt, DataTable)
