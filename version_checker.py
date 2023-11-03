import re
import sys
import tomli
import os
import requests
from packaging import version
import json

from packaging.version import Version


def get_public_version(project_name: str, is_test = False) -> Version:
    response = requests.get(f'https://{"test." if is_test else ""}pypi.org/pypi/{project_name}/json')
    response.raise_for_status()
    return version.parse(json.loads(response.content)['info']['version'])


if __name__ == '__main__':
    pyproject_toml_path = sys.argv[1]
    test_regex = sys.argv[2]
    with open(pyproject_toml_path, 'rb') as f:
        project = tomli.load(f)

    project_version = version.parse(project['project']['version'])
    is_test = False
    if test_regex:
        if re.compile(test_regex).search(str(project_version)):
            is_test = True
    public_project_version = get_public_version(project['project']['name'], is_test)

    with open(os.environ['GITHUB_OUTPUT'], 'at') as f:
        f.write(f"local_version_is_higher={str(project_version > public_project_version).lower()}\n")
        f.write(f"local_version={str(project_version)}\n")
        f.write(f"public_version={str(public_project_version)}\n")
        f.write(f"is_test={str(is_test).lower()}\n")

