import subprocess

from .types import IsoEnv, IsoEnvArgs, PyProjectToml, Requirements


def iso_run(
    args: IsoEnvArgs, cmd_list: list[str], **process_args
) -> subprocess.CompletedProcess:
    """Runs the command using the isolated environment."""
    from .run import run

    return run(args, cmd_list, **process_args)


def iso_open_process(
    args: IsoEnvArgs, cmd_list: list[str], **process_args
) -> subprocess.Popen:
    """Runs the command using the isolated environment."""
    from .run import open_proc

    return open_proc(args, cmd_list, **process_args)


__all__ = ["IsoEnv", "IsoEnvArgs", "Requirements", "PyProjectToml", "IsoEnv"]
