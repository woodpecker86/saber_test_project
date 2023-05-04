from typing import List, NamedTuple

from .yaml_parse import get_task_set, get_build_set


TASKS = {}
BUILDS = {}


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

    def __init__(self, name: str, tasks: List[str]):
        self.name = name
        self.tasks = tasks

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self.name}, tasks={self.tasks})'

    def get_ordered_tasks(self) -> List[str]:
        pass


def set_context() -> None:
    global TASKS, BUILDS
    raw_data: dict = get_task_set()
    TASKS = {task['name']:Task(*task.values()) for task in raw_data['tasks']}
    raw_data: dict = get_build_set()
    BUILDS = {build['name']: Build(*build.values()) for build in raw_data['builds']}


