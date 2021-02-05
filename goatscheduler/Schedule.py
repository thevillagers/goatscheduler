from __future__ import annotations
from typing import Type, List, Set, Union, AnyStr
from .Task import Task 



class Schedule:

    def __init__(
        self,
        name: str,
        components: List[Union[Task, Schedule]],
        parent: Schedule = None
    ) -> None:
        self.name                                       = name 
        self.components: List[Union[Task, Schedule]]    = []
        self.dependencies: List[Union[Task, Schedule]]  = []
        self.dependents: List[Union[Task, Schedule]]    = []
        for component in components:
            self.add_component(component)


    def __str__(self):
        dependencies = ', '.join([dependency.name for dependency in self.dependencies])
        dependents = ', '.join([dependent.name for dependent in self.dependents])
        return f'Schedule: {self.name}\nComponents: {", ".join([component.name for component in self.components])}\nDependencies: {dependencies}\nDependents: {dependents}'

    def add_component(self, component: Union[Task, Schedule]):
        self.components = list(set(self.components + [component]))
        self.dependencies = list(set(self.dependencies + component.dependencies))
        self.dependents = list(set(self.dependents + component.dependents))


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
            print(component)
            component.add_dependency_link(self)

    def __lshift__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
            component.add_dependency_link(self)

    def __rlshift__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
            self.add_dependency_link(component)