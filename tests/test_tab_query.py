import pytest
from filelist_query.ui import UI


async def test_query_tab():
    app = UI()
    async with app.run_test() as pilot:
        qt = pilot.app.query_one("#query-tab")
        assert qt
        tx = qt.query_one("#query-text")
        assert tx


async def focus_query_tab(pilot):
    sc = pilot.app.screen
    assert sc

    await pilot.press("right", "right")

    query_tab = pilot.app.query_one("#query-tab")
    assert query_tab
    sc.set_focus(query_tab)


@pytest.mark.xfail(reason="not ready to capture snapshot")
def test_snap_query_tab(snap_compare):
    assert snap_compare("../src/filelist_query/ui.py", run_before=focus_query_tab)
