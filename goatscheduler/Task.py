from __future__ import annotations
from typing import Callable
from .TaskRunHandler import TaskRunHandler
"""
Task.py
defines the most basic "task" used by the scheduler 
"""

class Task():
    #TODO: add sqlalchemy compatibility and a 'unique_name' field. Task metadata will persist through
    # the sqlite db with tasks of the same name. This will be used when reloading other tasks
    def __init__(
        self,
        name: str,
        callable: Callable,
        run_handler: TaskRunHandler = TaskRunHandler(),
        **kwargs
    ):
        """Initialize base task

        Args:
            callable (function, optional): the callable function you want the task to run. Defaults to None.
        """
        self.name               = name 
        self.callable           = callable
        self.callable_args      = None 
        self.task_dependencies  = set()
        self.task_dependents    = set()
        self.kwargs             = kwargs

    def __str__(self):
        dependencies = ', '.join([dependency.name for dependency in self.task_dependencies])
        dependents = ', '.join([dependent.name for dependent in self.task_dependents])
        return f'Task: {self.name}\nTask Dependencies: {dependencies}\nTask Dependents: {dependents}'

    def execute(self):
        self.callable(**self.kwargs)


    def add_dependency_link(self, task: Task):
        task.task_dependencies.add(self)
        self.task_dependents.add(task)

    def __rshift__(self, task: Task):
        self.add_dependency_link(task)

