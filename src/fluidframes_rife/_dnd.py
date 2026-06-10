from __future__ import annotations

from collections.abc import Callable
from tkinter import Tcl, TclError


def parse_dropped_file_paths(
    drop_data: str,
    splitlist: Callable[[str], tuple[str, ...]] | None = None,
) -> list[str]:
    """Parse the Tcl list payload returned by Tk drag-and-drop file events."""
    if not drop_data:
        return []

    if splitlist is None:
        splitlist = Tcl().splitlist

    try:
        return [str(path) for path in splitlist(drop_data)]
    except (TclError, TypeError, ValueError):
        return [drop_data]
