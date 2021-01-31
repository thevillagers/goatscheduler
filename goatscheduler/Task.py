from __future__ import annotations
from typing import Callable
from .TaskRunHandler import TaskRunHandler
from .Component import Component

class Task(Component):

    def __init__(
        self,
        name: str,
        callable: Callable,
        callable_args: dict = {},
        run_handler: TaskRunHandler = TaskRunHandler(),
        **kwargs
    ):
        super().__init__(name)
        self.components     = [self]
        self.callable       = callable
        self.callable_args  = callable_args
        self.kwargs         = kwargs


    def execute(self):
        self.callable(**self.callable_args)

