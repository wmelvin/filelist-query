from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Input, Select, Static, TabPane

from filelist_query.app_data import PredicateAttrs
from filelist_query.cond_opts import cond_sql_frag, get_cond_select_list

select_pred_options = [
    "and",
    "or",
]


class Predicate(Static):
    def __init__(self) -> None:
        super().__init__()
        self.pred_attrs = PredicateAttrs()

    def compose(self) -> ComposeResult:
        yield Select(((p, p) for p in select_pred_options), id="select_pred")
        yield Select(
            (),
            id="select_field",
            prompt="Select field",
            allow_blank=True,
        )
        yield Select((), id="select_condition", allow_blank=True)
        yield Input(placeholder="Criteria", id="criteria-input")

    def update_fields(self) -> None:
        fields_tab = self.app.query_one("#fields-tab")
        selected_fields = fields_tab.get_selected_fields()
        sel: Select = self.query_one("#select_field")
        sel.set_options((fld, fld) for fld in selected_fields)

    def on_mount(self) -> None:
        self.update_fields()

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        if event.value == Select.BLANK:
            return
        if event.select.id == "select_field":
            fields_tab = self.app.query_one("#fields-tab")

            # Field name is in event.value.
            column_type = fields_tab.get_column_type(event.value)

            cond_opts = get_cond_select_list(column_type)

            sel: Select = self.query_one("#select_condition")
            sel.set_options(cond_opts)

            self.pred_attrs.field = event.value
            self.pred_attrs.condition = 0
        elif event.select.id == "select_condition":
            self.pred_attrs.condition = event.value
        elif event.select.id == "select_pred":
            self.pred_attrs.pred_type = event.value
        self.app.query_one(CriteriaTab).update_title()

    @on(Input.Changed)
    def set_query(self, event: Input.Changed) -> None:
        self.pred_attrs.criteria = event.value
        self.app.query_one(CriteriaTab).update_title()


class CriteriaTab(TabPane):
    BINDINGS = [
        ("a", "add_predicate", "Add"),
    ]

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(Predicate(), id="predicates")

    def update_fields(self) -> None:
        predicates = self.query(Predicate)
        for pred in predicates:
            pred.update_fields()

    def update_title(self) -> None:
        text = self.get_predicates_str()
        if not text:
            text = "Select"
        self.app.title = text

    def action_add_predicate(self) -> None:
        new_pred = Predicate()
        self.query_one("#predicates").mount(new_pred)
        new_pred.add_class("added")
        new_pred.scroll_visible()

    def get_predicates(self):
        predicates = []
        for pred in self.query(Predicate):
            pa = pred.pred_attrs
            if pa.field and pa.condition and pa.criteria:
                predicates.append(  # noqa: PERF401
                    (
                        pa.pred_type,
                        pa.field,
                        pa.condition,
                        pa.criteria,
                    )
                )
        return predicates

    def get_predicates_str(self):
        text = ""
        for pred in self.query(Predicate):
            pa = pred.pred_attrs
            if pa.field and pa.condition and pa.criteria:
                if text:
                    text += f" {pa.pred_type} "
                text += f"{pa.field}{cond_sql_frag(pa.condition).format(pa.criteria)}"
        return text
