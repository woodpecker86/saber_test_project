

from .models import Build, Task
from .yaml_parse import get_task_set, get_build_set


CLASS_MAPPING = {'builds': Build,
                 'tasks': Task}


async def set_context() -> None:
    pass
