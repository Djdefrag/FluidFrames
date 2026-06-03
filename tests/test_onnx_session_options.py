from __future__ import annotations

import ast
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "FluidFrames.py"


def _load_inference_session_source() -> str:
    module = ast.parse(SOURCE.read_text(encoding="utf-8"))
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef) and node.name == "_load_inferenceSession":
            return ast.get_source_segment(SOURCE.read_text(encoding="utf-8"), node) or ""
    raise AssertionError("_load_inferenceSession was not found")


def test_onnxruntime_session_options_suppress_warning_logs() -> None:
    source = _load_inference_session_source()

    assert "sess_options.enable_profiling = False" in source
    assert "sess_options.log_severity_level = 3" in source
    assert "providers = ['DmlExecutionProvider']" in source
    assert "provider_options = provider_options" in source
