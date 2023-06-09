from os import path
from typing import Dict, Union
import logging

import yaml

from .settings import BUILD_PATH

logger = logging.getLogger(__name__)


def get_build_set() -> Dict[str, list]:
    return get_file_content('builds.yaml')


def get_task_set() -> Dict[str, list]:
    return get_file_content('tasks.yaml')


def get_file_content(name: str) -> Union[Dict[str, list], None]:
    file_path = path.join(BUILD_PATH, name)
    try:
        data = yaml.safe_load(open(file_path))
    except yaml.YAMLError as exc:
        logger.warning(f'File "{name}" get errors. {exc}')
    else:
        return data
