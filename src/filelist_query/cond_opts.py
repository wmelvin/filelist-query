from __future__ import annotations

from dataclasses import dataclass

COND_TYPE_STR = 0
COND_TYPE_NUM = 1

@dataclass
class ConditionItem:
    type: int
    display_name: str
    sql_fragment: str

conditions_dict = {
    1 : ConditionItem(COND_TYPE_STR, "contains", " like '%{}%'"),
    2 : ConditionItem(COND_TYPE_STR, "does not contain", " not like '%{}%'"),
    3 : ConditionItem(COND_TYPE_STR, "starts with", " like '{}%'"),
    4 : ConditionItem(COND_TYPE_STR, "does not start with", " not like '{}%'"),
    5 : ConditionItem(COND_TYPE_STR, "ends with", " like '%{}'"),
    6 : ConditionItem(COND_TYPE_STR, "does not end with", " not like '%{}'"),
    7 : ConditionItem(COND_TYPE_STR, "equals", " = '{}'"),
    8 : ConditionItem(COND_TYPE_STR, "does not equal", " != '{}'"),
    9 : ConditionItem(COND_TYPE_NUM, "greater than", " > {}"),
    10 : ConditionItem(COND_TYPE_NUM, "less than", " < {}"),
    11 : ConditionItem(COND_TYPE_NUM, "equals", " = {}"),
    12 : ConditionItem(COND_TYPE_NUM, "does not equal", " != {}"),
    13 : ConditionItem(COND_TYPE_NUM, "greater than or equal", " >= {}"),
    14 : ConditionItem(COND_TYPE_NUM, "less than or equal", " <= {}"),
}

def get_cond_select_list(db_col_type: str) -> list[tuple[str, int]]:
    cond_type = COND_TYPE_STR if db_col_type == "TEXT" else COND_TYPE_NUM
    return [
        (v.display_name, k)
        for k, v in conditions_dict.items()
        if v.type == cond_type
    ]


def cond_sql_frag(cond_key:int) -> str:
    return conditions_dict[cond_key].sql_fragment
