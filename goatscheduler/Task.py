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
        self.status_dict['in_progress'] = 1
        self.status_dict['task_start_timestamp'] = datetime.datetime.now()
        try: 
            function_return = self.callable(**self.callable_kwargs)
            self.status_dict['in_progress'] = 0
            self.status_dict['task_failed'] = 0
            self.status_dict['task_end_timestamp'] = datetime.datetime.now()
            self.status_dict['task_runtime'] = self.status_dict['task_end_timestamp'] - self.status_dict['task_start_timestamp']
            if isinstance(function_return, dict):
                self.status_dict.update(function_return)
        except Exception as e:
            self.status_dict['task_failed'] = 1
            print(e)

    def check_ready_status(self):
        for dependency in self.dependencies:
            if 'success' not in dependency.status_dict or dependency['success'] != 1:
                return False 
        return True