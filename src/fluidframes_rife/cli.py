"""
FluidFrames.RIFE launcher.
"""

from __future__ import annotations

import datetime as _datetime
import os
import shutil
import subprocess
import sys
import threading
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from importlib.resources import files
from pathlib import Path
from typing import IO

from fluidframes_rife._vendor.iso_env import IsoEnv, IsoEnvArgs, Requirements

RUNTIME_ENV_VAR = "FLUIDFRAMES_RUNTIME_ENV"
RUNTIME_TIMEOUT_ENV_VAR = "FLUIDFRAMES_LAUNCH_TIMEOUT_SECONDS"
RUNTIME_LOG_DIR_ENV_VAR = "FLUIDFRAMES_LOG_DIR"
RUNTIME_PYTHON_VERSION = "==3.10.*"
RUNTIME_LOCK_FILE = "requirements.runtime.lock.txt"
PACKAGE_DIST_NAME = "fluidframes-rife"
PACKAGE_MODULE_NAME = "fluidframes_rife"
APP_CACHE_NAME = "FluidFrames.RIFE"
LOG_TAIL_LINES = 40


def _runtime_lock_text() -> str:
    lock_resource = files("fluidframes_rife").joinpath(RUNTIME_LOCK_FILE)
    return lock_resource.read_text(encoding="utf-8").strip()


def _default_runtime_env_path() -> Path:
    override = os.environ.get(RUNTIME_ENV_VAR)
    if override:
        return Path(override).expanduser()

    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / APP_CACHE_NAME / "runtime-py310"


def _default_log_dir(env: Mapping[str, str] | None = None) -> Path:
    """Return the directory where launch logs are written."""
    env = env if env is not None else os.environ
    override = env.get(RUNTIME_LOG_DIR_ENV_VAR)
    if override:
        return Path(override).expanduser()

    if os.name == "nt":
        base = Path(env.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local"))
    else:
        base = Path(env.get("XDG_STATE_HOME") or (Path.home() / ".local" / "state"))
    return base / APP_CACHE_NAME / "logs"


def _new_log_path(log_dir: Path, now: _datetime.datetime | None = None) -> Path:
    """Return a fresh, timestamped log file path under ``log_dir``."""
    now = now if now is not None else _datetime.datetime.now()
    return log_dir / f"launch-{now.strftime('%Y%m%d-%H%M%S')}-{os.getpid()}.log"


def _runtime_process_env(package_import_root: Path | None = None) -> dict[str, str]:
    env = dict(os.environ)
    scripts_dir = Path(sys.executable).resolve().parent
    env["PATH"] = f"{scripts_dir}{os.pathsep}{env.get('PATH', '')}"
    env.pop("PYTHONPATH", None)
    if package_import_root is not None:
        env["PYTHONPATH"] = str(package_import_root)
    return env


def _ignore_runtime_package_copy(src: str, names: list[str]) -> list[str]:
    ignored = []
    for name in names:
        if name == "__pycache__" or name.endswith((".pyc", ".pyo")):
            ignored.append(name)
    return ignored


def _sync_package_import_root(runtime_path: Path) -> Path:
    """Copy this launcher package into the runtime without exposing outer site-packages."""
    source_package = Path(__file__).resolve().parent
    import_root = runtime_path / "launcher-package"
    target_package = import_root / PACKAGE_MODULE_NAME
    if target_package.exists():
        shutil.rmtree(target_package)
    import_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source_package,
        target_package,
        ignore=_ignore_runtime_package_copy,
    )
    return import_root


def _prepare_runtime(iso: IsoEnv, runtime_args: IsoEnvArgs) -> Path:
    bootstrap_env = _runtime_process_env()
    with _parent_runtime_path(bootstrap_env):
        iso.run(["python", "-c", "pass"], env=bootstrap_env)
    return _sync_package_import_root(runtime_args.venv_path)


@contextmanager
def _parent_runtime_path(env: dict[str, str]) -> Iterator[None]:
    original_path = os.environ.get("PATH")
    os.environ["PATH"] = env.get("PATH", original_path or "")
    try:
        yield
    finally:
        if original_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = original_path


def _runtime_args() -> IsoEnvArgs:
    return IsoEnvArgs(
        venv_path=_default_runtime_env_path(),
        build_info=Requirements(_runtime_lock_text(), python_version=RUNTIME_PYTHON_VERSION),
    )


def _timeout_seconds() -> float | None:
    timeout = os.environ.get(RUNTIME_TIMEOUT_ENV_VAR)
    if not timeout:
        return None
    return float(timeout)


def _terminate_process_tree(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def _tee_stream(src: IO[bytes], destinations: list[IO[bytes]]) -> None:
    """Copy bytes from ``src`` to every destination until ``src`` reaches EOF."""
    while True:
        chunk = src.read(4096)
        if not chunk:
            break
        for dest in destinations:
            try:
                dest.write(chunk)
                dest.flush()
            except (BrokenPipeError, ValueError):
                pass


def _format_failure_message(returncode: int, log_path: Path, tail: str) -> str:
    header = f"FluidFrames GUI exited with code {returncode}. Full log: {log_path}"
    if not tail.strip():
        return header + "\n"
    return f"{header}\n--- last {LOG_TAIL_LINES} log lines ---\n{tail}\n--- end ---\n"


def _tail_text(text: str, max_lines: int = LOG_TAIL_LINES) -> str:
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text.rstrip("\n")
    return "\n".join(lines[-max_lines:])


def _read_log_tail(log_path: Path, max_lines: int = LOG_TAIL_LINES) -> str:
    try:
        text = log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return _tail_text(text, max_lines)


def run_fluidframes(timeout_seconds: float | None = None) -> int:
    """Run the GUI inside the managed runtime environment."""
    runtime_args = _runtime_args()
    iso = IsoEnv(runtime_args)
    package_import_root = _prepare_runtime(iso, runtime_args)
    runtime_env = _runtime_process_env(package_import_root)
    log_dir = _default_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = _new_log_path(log_dir)

    with _parent_runtime_path(runtime_env), log_path.open("wb") as log_file:
        proc = iso.open_proc(
            ["python", "-u", "-m", "fluidframes_rife.FluidFrames"],
            env=runtime_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0,
        )
        parent_stdout = getattr(sys.stdout, "buffer", sys.stdout)
        tee_thread = threading.Thread(
            target=_tee_stream,
            args=(proc.stdout, [log_file, parent_stdout]),
            daemon=True,
        )
        tee_thread.start()

        try:
            if timeout_seconds is None:
                returncode = proc.wait()
            else:
                try:
                    returncode = proc.wait(timeout=timeout_seconds)
                except subprocess.TimeoutExpired:
                    _terminate_process_tree(proc)
                    returncode = 0
        finally:
            tee_thread.join(timeout=5)

    if returncode != 0:
        tail = _read_log_tail(log_path)
        sys.stderr.write(_format_failure_message(returncode, log_path, tail))
        sys.stderr.flush()
    return returncode


def main() -> int:
    """Launch FluidFrames.RIFE in its isolated Python 3.10 runtime."""
    return run_fluidframes(timeout_seconds=_timeout_seconds())


if __name__ == "__main__":
    sys.exit(main())
