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
        dependencies: List[Type[Component]] = [],
        dependents: List[Type[Component]] = []
    ):
        super().__init__(
            name=name,
            parent=parent,
            dependencies=dependencies,
            dependents=dependents
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
        return_dict = {'task_failed': 1, 'task_start_timestamp': datetime.datetime.now()}
        try: 
            function_return = self.callable(**self.callable_kwargs)
            return_dict['task_failed'] = 0
            return_dict['task_end_timestamp'] = datetime.datetime.now()
            return_dict['task_runtime'] = return_dict['task_end_timestamp'] - return_dict['task_start_timestamp']
            if isinstance(function_return, dict):
                return_dict.update(function_return)
        except Exception as e:
            print(e)
        
        self.run_status = return_dict