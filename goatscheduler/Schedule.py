from __future__ import annotations
from typing import Type, List, Set, Union
from .Task import Task 


class Schedule():

    def __init__(self, tasks: Set[Type[Task]] = None) -> None:
        self.tasks = set()
        self.task_dependencies = set()
        self.task_dependents = set()
        if tasks is not None and not isinstance(tasks, set):
            tasks = set(tasks)
        
        if tasks is not None:
            self.add_tasks(tasks)
    
    
    def _add_dependencies_from_task(self, task: Type[Task]) -> None:
        for dependency in task.task_dependencies:
            self.task_dependencies.add(dependency)
    
    def _add_dependents_from_task(self, task: Type[Task]) -> None:
        for dependent in task.task_dependents:
            self.task_dependents.add(dependent)
    
    
    def add_task(self, task: Type[Task]) -> None:
        self.tasks.add(task)
        self._add_dependencies_from_task(task)
        self._add_dependents_from_task(task)

    def add_tasks(self, tasks: Union(List[Type[Task]], Set[Type[Task]])) -> None:
        tasks = set(tasks)
        for task in tasks:
            self.add_task(task)