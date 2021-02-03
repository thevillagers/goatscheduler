from __future__ import annotations
from typing import Callable, Union, List 
#from .Schedule import Schedule
from .TaskRunHandler import TaskRunHandler

class Task:

    def __init__(
        self,
        name: str,
        callable: Callable,
        callable_args: dict = {},
        **kwargs
    ):
        self.name           = name 
        self.callable       = callable
        self.callable_args  = callable_args
        self.kwargs         = kwargs

        self.dependencies   = []
        self.dependents     = []

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

    def __rrshift__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
                component.add_dependency_link(self)

    def __lshift__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
            component.add_dependency_link(self)

    def __rlshift__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
            self.add_dependency_link(component)