import pytest
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


async def focus_results_tab(pilot):
    sc = pilot.app.screen
    assert sc

    await pilot.press("right", "right", "right")

    results_tab = pilot.app.query_one("#results-tab")
    assert results_tab
    sc.set_focus(results_tab)


@pytest.mark.xfail(reason="not ready to capture snapshot")
def test_snap_results_tab(snap_compare):
    assert snap_compare("../src/filelist_query/ui.py", run_before=focus_results_tab)
