import os
import re
import shutil

from fluidframes_rife._vendor.iso_env.types import IsoEnvArgs


def get_verbose_from_env() -> bool:
    return os.environ.get("ISO_ENV_VERBOSE", "0") == "1"


def to_full_cmd_list(
    args: IsoEnvArgs,
    cmd_list: list[str],
    **process_args,  # needed to capture unexpected arguments
) -> list[str]:
    uv = shutil.which("uv")
    assert uv is not None, "uv not found."
    preamble = [
        uv,
        "run",
        "--project",
        str(args.venv_path),
    ]
    return preamble + cmd_list


_ERROR_MESSAGE_CHECK_PYTHON_STR = """
A valid version string must have:
- An operator: one of ==, >=, <=, >, <, or ~=.
- A major version number.
- A minor version number.
- A patch version number OR a '*' wildcard.

Examples of valid strings:
    >=3.11.0
    ==3.11.*

Examples of invalid strings:
    >=3.11    (missing patch version)
"""


def check_python_str(python_version: str) -> None:
    """
    Validates that the python_version string is in a valid format.

    A valid version string must have:
    - An operator: one of ==, >=, <=, >, <, or ~=.
    - A major version number.
    - A minor version number.
    - A patch version number OR a '*' wildcard.

    Examples of valid strings:
        >=3.11.0
        ==3.11.*

    Examples of invalid strings:
        >=3.11    (missing patch version)
        ==3.11    (missing patch version)

    Raises:
        ValueError: If the python_version string is invalid.
    """
    pattern = r"^(==|>=|<=|>|<|~=)\d+\.\d+\.(\d+|\*)$"
    if not re.match(pattern, python_version):
        error_msg = f"Invalid python version string: {python_version}\n\n{_ERROR_MESSAGE_CHECK_PYTHON_STR}"
        raise ValueError(error_msg)
