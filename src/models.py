from typing import List, NamedTuple, Iterable, Set

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

    def __init__(self, name: str, tasks: Iterable):
        self.name = name
        self.tasks = tasks
        self._ordered_tasks = list()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self.name}, tasks={self.tasks})'

    def get_ordered_tasks(self) -> List[str]:
        if self.is_ordered_tasks_empty():
            for task in self.tasks:
                if task.dependencies:
                    self.add_task_dependencies(task)
                self._ordered_tasks.append(task.name)
        return self._ordered_tasks

    def is_ordered_tasks_empty(self) -> bool:
        return not self._ordered_tasks

    def add_task_dependencies(self, task: Task) -> None:
        if not task.dependencies:
            self._ordered_tasks.append(task.name)
        for dependency in task.dependencies:
            self.add_task_dependencies(TASKS[dependency])


def set_context() -> None:
    global TASKS, BUILDS
    raw_data: dict = get_task_set()
    TASKS = {task['name']: Task(*task.values()) for task in raw_data['tasks']}
    raw_data: dict = get_build_set()
    BUILDS = {build['name']: Build(*build.values()) for build in raw_data['builds']}


