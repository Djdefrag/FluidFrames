from __future__ import annotations

from fluidframes_rife._dnd import parse_dropped_file_paths


def test_parse_dropped_file_paths_splits_tcl_file_list() -> None:
    drop_data = "{C:/Users/niteris/My Video.mp4} C:/Temp/clip.mov"

    assert parse_dropped_file_paths(drop_data) == [
        "C:/Users/niteris/My Video.mp4",
        "C:/Temp/clip.mov",
    ]


def test_parse_dropped_file_paths_handles_empty_payload() -> None:
    assert parse_dropped_file_paths("") == []


def test_parse_dropped_file_paths_falls_back_to_raw_payload() -> None:
    def splitlist(_: str) -> tuple[str, ...]:
        raise ValueError("invalid Tcl list")

    assert parse_dropped_file_paths("C:/Temp/clip.mov", splitlist=splitlist) == ["C:/Temp/clip.mov"]


def test_parse_dropped_file_paths_handles_malformed_tcl_list() -> None:
    assert parse_dropped_file_paths("{C:/Temp/clip.mov") == ["{C:/Temp/clip.mov"]
