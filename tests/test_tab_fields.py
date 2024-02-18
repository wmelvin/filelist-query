import pytest
from filelist_query.ui import UI
from textual.widgets import OptionList


async def test_field_list():
    app = UI()
    async with app.run_test() as pilot:
        ft = pilot.app.query_one("#fields-tab")
        fl = ft.query_one("#field_list")
        assert fl
        assert fl.option_count > 0


async def test_move_options():
    app = UI()
    async with app.run_test() as pilot:
        await move_options(pilot)


async def move_options(pilot):
    sc = pilot.app.screen
    assert sc

    fld_lst = pilot.app.query_one("#field_list")
    assert isinstance(fld_lst, OptionList)
    assert fld_lst.option_count > 0

    sel_lst = pilot.app.query_one("#selected_list")
    assert isinstance(sel_lst, OptionList)

    sc.set_focus(fld_lst)
    foc = sc.focused
    assert foc

    await pilot.press("down", "enter")
    await pilot.click("#add")

    sc.set_focus(sel_lst)
    await pilot.press("down", "enter")
    await pilot.click("#down")
    await pilot.click("#remove")

    sc.set_focus(fld_lst)
    await pilot.press("down", "down", "down", "enter")
    await pilot.click("#add")

    sc.set_focus(sel_lst)


@pytest.mark.xfail(reason="not ready to capture snapshot")
def test_snap_move_options(snap_compare):
    assert snap_compare("../src/filelist_query/ui.py", run_before=move_options)
