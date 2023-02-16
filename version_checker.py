import sys
import tomli
import os
import requests
from packaging import version
import json

from packaging.version import Version


def get_public_version(project_name: str) -> Version:
    response = requests.get(f'https://pypi.org/pypi/{project_name}/json')
    response.raise_for_status()
    return version.parse(json.loads(response.content)['info']['version'])


if __name__ == '__main__':
    project_path = sys.argv[1]
    with open(os.path.join(project_path, 'pyproject.toml'), 'rb') as f:
        project = tomli.load(f)

    project_version = version.parse(project['project']['version'])
    public_project_version = get_public_version(project['project']['name'])

    os.environ['GITHUB_OUTPUT'] = f"local_version_is_higher={str(project_version > public_project_version).lower()}"

