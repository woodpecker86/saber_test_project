import logging
from typing import List, NamedTuple, Iterable, Set, Dict, Union

from .yaml_parse import get_task_set, get_build_set


TASKS = {}

logger = logging.getLogger(__name__)


class TaskList:

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, obj_type=None):
        return getattr(obj, self.private_name)

    def __set__(self, instance, value):
        data = [TASKS[task] for task in value]
        setattr(instance, self.private_name, data)


class Task(NamedTuple):
    name: str
    dependencies: List[str]


class Build:
    tasks = TaskList()

    def __init__(self, name: str, tasks: Iterable):
        self.name = name
        self.tasks = tasks
        self._ordered_tasks = list()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self.name}, tasks={self.tasks})'

    def get_ordered_tasks(self) -> List[str]:
        if self.is_ordered_tasks_empty():
            for task in self.tasks:
                self.add_task_dependencies(task)
        return self._ordered_tasks

    def is_ordered_tasks_empty(self) -> bool:
        return not self._ordered_tasks

    def add_task_dependencies(self, task: Task) -> None:
        if task.dependencies:
            for dependency in task.dependencies:
                self.add_task_dependencies(TASKS[dependency])
        if task.name not in self._ordered_tasks:
            self._ordered_tasks.append(task.name)


def set_context() -> Union[Dict[str, List[Task]], None]:
    global TASKS
    try:
        raw_data: dict = get_task_set()
        TASKS = {task['name']: Task(*task.values()) for task in raw_data['tasks']}
        raw_data: dict = get_build_set()
        builds = {build['name']: Build(*build.values()) for build in raw_data['builds']}
    except TypeError as exc:
        logger.warning(f"Can't set context. Something's wrong with data files.")
    else:
        return builds


