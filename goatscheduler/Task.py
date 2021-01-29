from __future__ import annotations
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
        callable,
        run_handler: TaskRunHandler = TaskRunHandler(),
        **kwargs
    ):
        """Initialize base task

        Args:
            callable (function, optional): the callable function you want the task to run. Defaults to None.
        """
        self.callable           = callable
        self.callable_args      = None 
        self.task_dependencies  = set()
        self.task_dependents    = set()
        self.kwargs             = kwargs

    def execute(self):
        self.callable(**self.kwargs)


    def add_dependency_link(self, task: Task):
        self.task_dependencies.add(task)
        task.task_dependents.add(self)

    def __rshift__(self, task: Task):
        self.add_dependency_link(task)

