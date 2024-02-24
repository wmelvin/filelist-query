import pytest
from filelist_query.ui import UI
from textual.widgets import Select


async def test_criteria_tab():
    app = UI()
    async with app.run_test() as pilot:
        ct = pilot.app.query_one("#criteria-tab")
        assert ct
        # There should initially be one predicate.
        select_pred = ct.query_one("#select-pred")
        assert select_pred
        select_column = ct.query_one("#select-column")
        assert select_column
        select_condition = ct.query_one("#select-condition")
        assert select_condition
        criteria_input = ct.query_one("#criteria-input")
        assert criteria_input


async def focus_criteria_tab(pilot):
    sc = pilot.app.screen
    assert sc

    await pilot.press("right")

    criteria_tab = pilot.app.query_one("#criteria-tab")
    assert criteria_tab
    sc.set_focus(criteria_tab)

    sel = pilot.app.query_one("#select_column")
    assert sel
    assert isinstance(sel, Select)

    sc.set_focus(sel)
    foc = sc.focused
    assert foc

    await pilot.press("down")


@pytest.mark.xfail(reason="not ready to capture snapshot")
def test_snap_criteria_tab(snap_compare):
    assert snap_compare("../src/filelist_query/ui.py", run_before=focus_criteria_tab)
