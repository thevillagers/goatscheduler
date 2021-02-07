from __future__ import annotations
from typing import Callable, Union, List, Type
#from .Schedule import Schedule
from .TaskRunHandler import TaskRunHandler
from .Component import Component
import datetime

class Task(Component):

    def __init__(
        self,
        name: str,
        callable: Callable,
        callable_kwargs: dict = {},
        parent: Schedule = None,
        run_manager: TaskRunHandler = TaskRunHandler()
    ):
        super().__init__(
            name=name,
            parent=parent
        )
        self.callable           = callable
        self.callable_kwargs    = callable_kwargs
    def __str__(self):
        dependencies = f'Dependencies: {", ".join([dependency.name for dependency in self.dependencies])}\n' 
        dependents = f'Dependents: {", ".join([dependent.name for dependent in self.dependents])}\n'
        name = f'Task: {self.name}\n'
        parent = f'Parent: {self.parent.name if self.parent is not None else "No parent"}\n'
        return name + parent + dependencies + dependents 

    def run(self):
        self.state['running'] = 1
        self.state['ready'] = 0
        self.state['not_ready'] = 1
        try: 
            function_return = self.callable(**self.callable_kwargs)
            if isinstance(function_return, dict):
                self.state.update(function_return)
            self.state['success'] = 1
            self.state['fail'] = 0 
        except Exception as e:
            self.state['success'] = 0
            self.state['fail'] = 1
            print(e)
        self.state['running'] = 0

    def refresh_state(self):
        if self.state['success'] or self.state['fail'] or self.state['running']:
            self.state['ready'] = 0
            self.state['not_ready'] = 1
            return False
        for dependency in self.dependencies:
            if dependency.state['success'] != 1:
                self.state['ready'] = 0
                self.state['not_ready'] = 1
                return False 
        self.state['ready'] = 1
        self.state['not_ready'] = 0
        return True