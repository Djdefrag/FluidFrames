import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Requirements:
    content: str
    python_version: str | None = None

    def __post_init__(self):
        from fluidframes_rife._vendor.iso_env.util import check_python_str

        self.content = self.content.strip()
        if self.python_version is not None:
            check_python_str(self.python_version)

    def __repr__(self):
        return self.content


@dataclass
class PyProjectToml:
    content: str

    def __post_init__(self):
        self.content = self.content.strip()

    def __repr__(self):
        return self.content


@dataclass
class IsoEnvArgs:
    venv_path: Path
    build_info: Requirements | PyProjectToml


@dataclass
class EnvironmentPartition:
    env: dict[str, str]
    process_args: dict[str, str]


class IsoEnv:
    def __init__(self, args: IsoEnvArgs) -> None:
        self.args = args

    def run(self, cmd_list: list[str], **process_args) -> subprocess.CompletedProcess:
        from fluidframes_rife._vendor.iso_env.run import run

        return run(self.args, cmd_list, **process_args)

    def open_proc(self, cmd_list: list[str], **process_args) -> subprocess.Popen:
        from fluidframes_rife._vendor.iso_env.run import open_proc

        return open_proc(self.args, cmd_list, **process_args)
