import curses
from typing import Any, Callable, Tuple
from .selector import dict_select
from .common import IndexedDict, default_item_display
from .actions import run_function, select, edit


def dict_ui(
    base_window: curses.window,
    dictionary: dict,
    item_display: Callable[
        [Tuple[str, dict], bool], Tuple[str, int]
    ] = default_item_display,
    start_line: int = 0,
    start_pos: int = 0,
):

    while True:
        base_window.clear()
        base_window.refresh()

        item, (start_line, start_pos) = dict_select(
            base_window,
            IndexedDict(dictionary),
            item_display,
            start_line=start_line,
            start_pos=start_pos,
        )
        functionality = item[1].get("functionality")

        if functionality == "run_function":
            run_function(item[1])
        elif functionality == "select":
            dictionary[item[0]]["value"] = select(
                base_window, item[1]["options"], item_display
            )
        elif functionality == "edit":
            dictionary[item[0]]["value"] = edit(base_window, item)
        elif functionality == "sub_menu":
            dict_ui(base_window, item[1]["menu"])

        if exit_after_action := item[1].get("exit_after_action"):
            if exit_after_action:
                break

    base_window.clear()
    base_window.refresh()


def selection_ui(
    base_window: curses.window,
    options: dict,
    item_display: Callable[
        [Tuple[str, dict], bool], Tuple[str, int]
    ] = default_item_display,
    start_line: int = 0,
    start_pos: int = 0,
) -> Any:
    value = select(base_window, options, item_display, start_line, start_pos)
    base_window.clear()
    base_window.refresh()
    return value


def editor_ui(
    base_window: curses.window,
    name: str,
    value: str = "",
    validator: Callable[[str], bool] = lambda _: True,
    allowed_human_readable: str = "",
) -> str:
    value = edit(
        base_window,
        (
            name,
            {
                "value": value,
                "validator": validator,
                "allowed_human_readable": allowed_human_readable,
            },
        ),
    )
    base_window.clear()
    base_window.refresh()
    return value
