from typing import NamedTuple, List


class Task(NamedTuple):
    name: str
    dependencies: List[str]


class Build(NamedTuple):
    name: str
    tasks: List[Task]


