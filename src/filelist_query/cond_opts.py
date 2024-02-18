from __future__ import annotations


# Define an enum for condition options.
class ConditionOptions:
    CONTAINS = 1
    NOT_CONTAINS = 2
    STARTS_WITH = 3
    NOT_STARTS_WITH = 4
    ENDS_WITH = 5
    NOT_ENDS_WITH = 6
    EQUALS = 7
    NOT_EQUALS = 8


# Define a dictionary that maps condition options to SQL fragment strings.
cond_sql_frag = {
    ConditionOptions.CONTAINS: " like '%{}%'",
    ConditionOptions.NOT_CONTAINS: " not like '%{}%'",
    ConditionOptions.STARTS_WITH: " like '{}%'",
    ConditionOptions.NOT_STARTS_WITH: " not like '{}%'",
    ConditionOptions.ENDS_WITH: " like '%{}'",
    ConditionOptions.NOT_ENDS_WITH: " not like '%{}'",
    ConditionOptions.EQUALS: " = '{}'",
    ConditionOptions.NOT_EQUALS: " != '{}'",
}

cond_name = {
    ConditionOptions.CONTAINS: "contains",
    ConditionOptions.NOT_CONTAINS: "does not contain",
    ConditionOptions.STARTS_WITH: "starts with",
    ConditionOptions.NOT_STARTS_WITH: "does not start with",
    ConditionOptions.ENDS_WITH: "ends with",
    ConditionOptions.NOT_ENDS_WITH: "does not end with",
    ConditionOptions.EQUALS: "equals",
    ConditionOptions.NOT_EQUALS: "does not equal",
}


def get_cond_opt(cond: ConditionOptions) -> list[tuple[str, int]]:
    return (cond_name[cond], cond)

# TODO: This is too specific. Defaults based on field type are needed.
select_condition_options = {
    "file_name": [
        get_cond_opt(ConditionOptions.CONTAINS),
        get_cond_opt(ConditionOptions.NOT_CONTAINS),
        get_cond_opt(ConditionOptions.STARTS_WITH),
        get_cond_opt(ConditionOptions.NOT_STARTS_WITH),
        get_cond_opt(ConditionOptions.ENDS_WITH),
        get_cond_opt(ConditionOptions.NOT_ENDS_WITH),
        get_cond_opt(ConditionOptions.EQUALS),
        get_cond_opt(ConditionOptions.NOT_EQUALS),
    ],
    "dir_name": [
        get_cond_opt(ConditionOptions.CONTAINS),
        get_cond_opt(ConditionOptions.NOT_CONTAINS),
        get_cond_opt(ConditionOptions.STARTS_WITH),
        get_cond_opt(ConditionOptions.NOT_STARTS_WITH),
        get_cond_opt(ConditionOptions.ENDS_WITH),
        get_cond_opt(ConditionOptions.NOT_ENDS_WITH),
        # Because the dir_name field is a full directory path, the equals
        # and not equals conditions are not useful.
    ],
}
