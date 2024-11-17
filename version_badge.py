import ast
import sys
from datetime import datetime
from pathlib import Path

from packaging import version as pv


def get_version(directory):
    with open(Path(directory) / "__version__.py", "r") as f:
        node = ast.parse(f.read())
        for child in node.body:
            target_type = ast.Constant
            is_version_str = (
                isinstance(child, ast.Assign)
                and any(
                    isinstance(target, ast.Name) and target.id == "__version__"
                    for target in child.targets
                )
                and isinstance(child.value, target_type)
            )
            if is_version_str:
                return child.value.value
    raise Exception("Couldn't find version")


def is_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def addv(version):
    if version.startswith("v") or is_date(version):
        return version
    return f"v{version}"


def get_version_color(version):
    try:
        parsed = pv.parse(version)
    except pv.InvalidVersion:
        return "lightgrey"
    if parsed.is_prerelease or version.startswith("0."):
        return "orange"
    return "blue"


if __name__ == "__main__":
    pkg_version = get_version(sys.argv[1])
    print('echo "LABEL=version" >> $GITHUB_ENV')
    print(f'echo "MESSAGE={addv(pkg_version)}" >> $GITHUB_ENV')
    print(f'echo "MESSAGE-COLOR={get_version_color(pkg_version)}" >> $GITHUB_ENV')
