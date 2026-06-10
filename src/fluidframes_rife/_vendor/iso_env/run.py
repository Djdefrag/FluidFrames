import os
import subprocess
import warnings
from pathlib import Path

from filelock import FileLock

from fluidframes_rife._vendor.iso_env.api import _install_impl, installed, purge
from fluidframes_rife._vendor.iso_env.types import IsoEnvArgs
from fluidframes_rife._vendor.iso_env.util import get_verbose_from_env, to_full_cmd_list


def _get_lock_path(venv_path: Path) -> Path:
    """Get the lock file path for a given venv path."""
    resolved_path = venv_path.resolve()
    return resolved_path.parent / f".{resolved_path.name}.lock"


def _to_str(src: bytes | str | list[str] | None) -> str:
    if src is None:
        return ""
    if isinstance(src, list):
        return subprocess.list2cmdline(src)
    if isinstance(src, str):
        return src
    return src.decode("utf-8")


def run(
    args: IsoEnvArgs,
    cmd_list: list[str],
    verbose: bool | None = None,
    **process_args,
) -> subprocess.CompletedProcess:
    """Runs the command using the isolated environment."""
    verbose = verbose if verbose is not None else get_verbose_from_env()

    # Use file lock to protect the check-then-act pattern
    lock_path = _get_lock_path(args.venv_path)
    lock_path.parent.mkdir(exist_ok=True, parents=True)

    with FileLock(str(lock_path), timeout=300):
        if not installed(args, verbose=verbose):
            purge(args.venv_path)
            _install_impl(args, verbose=verbose)
    env = dict(os.environ)
    if "env" in process_args:
        env = process_args.pop("env")
    if "VIRTUAL_ENV" in env:
        del env["VIRTUAL_ENV"]
    full_cmd_list = to_full_cmd_list(args, cmd_list, verbose=verbose, **process_args)
    check = process_args.pop("check", True)
    try:
        shell = process_args.pop("shell", False)
        cp = subprocess.run(
            full_cmd_list, env=env, check=check, shell=shell, **process_args
        )
        return cp
    except subprocess.CalledProcessError as exc:
        warn_errors = os.environ.get("ISO_ENV_WARN_ERRORS", "0") == "1"
        if warn_errors:
            stderr = _to_str(exc.stderr)
            stdout = _to_str(exc.stdout)
            cmd_str = _to_str(full_cmd_list)
            error_msg = f"\n\nFailed to run:\n  {cmd_str}\n{exc.returncode}\n\nstdout: {stdout}\nstderr: {stderr}\n\n"
            warnings.warn(error_msg)
        raise


def open_proc(
    args: IsoEnvArgs,
    cmd_list: list[str],
    verbose: bool | None = None,
    **process_args,
) -> subprocess.Popen:
    """Runs the command using the isolated environment."""
    verbose = verbose if verbose is not None else get_verbose_from_env()

    # Use file lock to protect the check-then-act pattern
    lock_path = _get_lock_path(args.venv_path)
    lock_path.parent.mkdir(exist_ok=True, parents=True)

    with FileLock(str(lock_path), timeout=300):
        if not installed(args, verbose=verbose):
            purge(args.venv_path)
            _install_impl(args, verbose=verbose)
    full_cmd_list = to_full_cmd_list(args, cmd_list, verbose=verbose, **process_args)
    shell = process_args.pop("shell", False)
    if verbose:
        full_path = Path(".").resolve()
        full_cmd_str = subprocess.list2cmdline(full_cmd_list)
        print(f"Running in {full_path}: {full_cmd_str}")

    env = dict(os.environ)
    if "env" in process_args:
        env = process_args.pop("env")
    if "VIRTUAL_ENV" in env:
        del env["VIRTUAL_ENV"]

    proc = subprocess.Popen(  # type: ignore
        full_cmd_list,
        shell=shell,
        env=env,
        **process_args,
    )
    return proc
