from __future__ import annotations

import datetime as _datetime
import io
import os
import subprocess
from pathlib import Path
from typing import Any

import pytest

from fluidframes_rife import cli
from iso_env import Requirements


def test_iso_env_accepts_runtime_python_version() -> None:
    requirements = Requirements("onnxruntime-directml", python_version="==3.10.*")

    assert requirements.content == "onnxruntime-directml"
    assert requirements.python_version == "==3.10.*"


def test_runtime_args_use_override_path_and_locked_python(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runtime_path = tmp_path / "runtime"
    monkeypatch.setenv(cli.RUNTIME_ENV_VAR, str(runtime_path))

    args = cli._runtime_args()
    lock_text = args.build_info.content

    assert args.venv_path == runtime_path
    assert args.build_info.python_version == cli.RUNTIME_PYTHON_VERSION
    assert cli.PACKAGE_DIST_NAME not in lock_text
    assert "onnxruntime-directml==1.17.3" in lock_text


def test_runtime_process_env_exposes_launcher_scripts_and_package_root(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    scripts_dir = tmp_path / "Scripts"
    scripts_dir.mkdir()
    launcher_python = scripts_dir / "python.exe"
    launcher_python.touch()

    monkeypatch.setattr(cli.sys, "executable", str(launcher_python))
    import_root = tmp_path / "runtime-import-root"
    monkeypatch.setenv("PATH", "existing-path")
    monkeypatch.setenv("PYTHONPATH", "outer-pythonpath")

    env = cli._runtime_process_env(import_root)

    assert env["PATH"].split(os.pathsep)[0] == str(scripts_dir.resolve())
    assert env["PATH"].endswith("existing-path")
    assert env["PYTHONPATH"] == str(import_root)


class _FakeProcess:
    """Stand-in for ``subprocess.Popen`` exposing just what the launcher uses."""

    def __init__(
        self,
        stdout_bytes: bytes = b"",
        returncode: int = 0,
        raise_timeout: bool = False,
    ) -> None:
        self.stdout = io.BytesIO(stdout_bytes)
        self._returncode = returncode
        self._raise_timeout = raise_timeout
        self.wait_calls: list[float | None] = []

    def wait(self, timeout: float | None = None) -> int:
        self.wait_calls.append(timeout)
        if self._raise_timeout:
            raise subprocess.TimeoutExpired(["python"], timeout)
        return self._returncode

    def poll(self) -> int | None:
        return self._returncode


def _install_fake_iso_env(
    monkeypatch: pytest.MonkeyPatch,
    process: _FakeProcess,
    open_calls: list[tuple[object, list[str], dict[str, Any]]] | None = None,
) -> None:
    prepare_calls = []

    class FakeIsoEnv:
        def __init__(self, args: object) -> None:
            self.args = args

        def open_proc(self, command: list[str], **process_args: Any) -> _FakeProcess:
            if open_calls is not None:
                open_calls.append((self.args, command, process_args))
            return process

    monkeypatch.setattr(cli, "IsoEnv", FakeIsoEnv)
    runtime_args = object()
    import_root = Path("runtime-import-root")
    monkeypatch.setattr(cli, "_runtime_args", lambda: runtime_args)
    monkeypatch.setattr(cli, "_prepare_runtime", lambda iso, args: prepare_calls.append((iso, args)) or import_root)
    monkeypatch.setattr(cli, "_runtime_process_env", lambda package_import_root=None: {"PATH": "x", "PYTHONPATH": str(package_import_root)})


def test_run_fluidframes_pipes_subprocess_output_to_log_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    open_calls: list[tuple[object, list[str], dict[str, Any]]] = []
    process = _FakeProcess(stdout_bytes=b"hello from gui\n")
    _install_fake_iso_env(monkeypatch, process, open_calls)
    monkeypatch.setenv(cli.RUNTIME_LOG_DIR_ENV_VAR, str(tmp_path))

    assert cli.run_fluidframes() == 0

    assert len(open_calls) == 1
    _, command, process_args = open_calls[0]
    assert command == ["python", "-u", "-m", "fluidframes_rife.FluidFrames"]
    assert process_args["stdout"] is subprocess.PIPE
    assert process_args["stderr"] == subprocess.STDOUT

    log_files = list(tmp_path.glob("launch-*.log"))
    assert len(log_files) == 1
    assert log_files[0].read_bytes() == b"hello from gui\n"


def test_run_fluidframes_reports_failure_with_log_tail(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    crash_output = b"Traceback (most recent call last):\nImportError: numpy.core.multiarray failed to import\n"
    process = _FakeProcess(stdout_bytes=crash_output, returncode=1)
    _install_fake_iso_env(monkeypatch, process)
    monkeypatch.setenv(cli.RUNTIME_LOG_DIR_ENV_VAR, str(tmp_path))

    assert cli.run_fluidframes() == 1

    err = capsys.readouterr().err
    assert "FluidFrames GUI exited with code 1" in err
    assert "ImportError: numpy.core.multiarray failed to import" in err
    log_files = list(tmp_path.glob("launch-*.log"))
    assert len(log_files) == 1
    assert str(log_files[0]) in err


def test_run_fluidframes_timeout_terminates_process(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    terminated: list[object] = []
    process = _FakeProcess(raise_timeout=True)
    _install_fake_iso_env(monkeypatch, process)
    monkeypatch.setenv(cli.RUNTIME_LOG_DIR_ENV_VAR, str(tmp_path))
    monkeypatch.setattr(cli, "_terminate_process_tree", lambda proc: terminated.append(proc))

    assert cli.run_fluidframes(timeout_seconds=0.01) == 0
    assert terminated == [process]


def test_main_passes_launch_timeout_to_runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []
    monkeypatch.setenv(cli.RUNTIME_TIMEOUT_ENV_VAR, "2.5")

    def fake_run_fluidframes(timeout_seconds: float | None = None) -> int:
        calls.append(timeout_seconds)
        return 17

    monkeypatch.setattr(cli, "run_fluidframes", fake_run_fluidframes)

    assert cli.main() == 17
    assert calls == [2.5]


def test_default_log_dir_honors_override(tmp_path: Path) -> None:
    override = tmp_path / "custom-logs"
    env = {cli.RUNTIME_LOG_DIR_ENV_VAR: str(override)}

    assert cli._default_log_dir(env=env) == override


def test_new_log_path_is_timestamped_and_unique(tmp_path: Path) -> None:
    fixed_now = _datetime.datetime(2026, 6, 2, 12, 34, 56)
    path = cli._new_log_path(tmp_path, now=fixed_now)

    assert path.parent == tmp_path
    assert path.name.startswith("launch-20260602-123456-")
    assert path.suffix == ".log"


def test_tail_text_keeps_only_last_lines() -> None:
    text = "\n".join(str(i) for i in range(100))
    tail = cli._tail_text(text, max_lines=5)

    assert tail.splitlines() == ["95", "96", "97", "98", "99"]


def test_runtime_lock_pins_directml_compatible_versions() -> None:
    """The DirectML ONNX runtime stack runs against NumPy 1.x here."""
    lock_text = cli._runtime_lock_text()

    assert "numpy==1.26.4" in lock_text
    assert "numpy==2." not in lock_text
    assert "opencv-python-headless==4.11.0.86" in lock_text
    assert "opencv-python-headless==4.12" not in lock_text
    assert "onnxruntime-directml==1.17.3" in lock_text
    assert "pillow==9.5.0" in lock_text
    assert "tkinterdnd2==0.4.4.1" in lock_text
