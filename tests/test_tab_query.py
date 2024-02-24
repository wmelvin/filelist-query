from filelist_query.ui import UI


async def test_query_tab():
    app = UI()
    async with app.run_test() as pilot:
        qt = pilot.app.query_one("#query-tab")
        assert qt
        tx = qt.query_one("#query-text")
        assert tx
