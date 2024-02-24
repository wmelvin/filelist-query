from filelist_query.ui import UI


async def test_criteria_tab():
    app = UI()
    async with app.run_test() as pilot:
        ct = pilot.app.query_one("#criteria-tab")
        assert ct
        # There should initially be one predicate.
        select_pred = ct.query_one("#select_pred")
        assert select_pred
        select_column = ct.query_one("#select_column")
        assert select_column
        select_condition = ct.query_one("#select_condition")
        assert select_condition
        criteria_input = ct.query_one("#criteria-input")
        assert criteria_input
