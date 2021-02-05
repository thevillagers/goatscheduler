from __future__ import annotations
from typing import Callable, Union, List 
#from .Schedule import Schedule
from .TaskRunHandler import TaskRunHandler
import datetime

class Task:

    def __init__(
        self,
        name: str,
        callable: Callable,
        callable_kwargs: dict = {},
        parent: Schedule    = None
    ):
        self.name           = name 
        self.callable       = callable
        self.callable_args  = callable_kwargs

        self.dependencies   = []
        self.dependents     = []
        self.run_status     = {}

    def __str__(self):
        dependencies = ', '.join([dependency.name for dependency in self.dependencies])
        dependents = ', '.join([dependent.name for dependent in self.dependents])
        return f'Task: {self.name}\nDependencies: {dependencies}\nDependents: {dependents}'


    def _add_dependency(self, task):
        self.dependencies = list(set(self.dependencies + [task]))

    def _add_dependent(self, task):
        self.dependents = list(set(self.dependents + [task]))

    def add_dependency_link(self, task):
        task._add_dependency(self)
        self._add_dependent(task)
    
    def __rshift__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
            self.add_dependency_link(component)
        return components 

    def __rrshift__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
                component.add_dependency_link(self)
        return self 

    def __lshift__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
            component.add_dependency_link(self)
        return components 

    def __rlshift__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
            self.add_dependency_link(component)
        return self 

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