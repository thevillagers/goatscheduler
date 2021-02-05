from __future__ import annotations
from typing import Type, List, Set, Union, AnyStr
from .Task import Task 



class Schedule:

    def __init__(
        self,
        name: str,
        components: List[Union[Task, Schedule]] = [],
        parent: Schedule = None
    ) -> None:
        self.name                                       = name
        self.parent                                     = parent
        self.components: List[Union[Task, Schedule]]    = []
        self.dependencies: List[Union[Task, Schedule]]  = []
        self.dependents: List[Union[Task, Schedule]]    = []
        for component in components:
            self.add_component(component)


    def __str__(self):
        dependencies = ', '.join([dependency.name for dependency in self.dependencies])
        dependents = ', '.join([dependent.name for dependent in self.dependents])
        name = f'Schedule: {self.name}\n'
        parent = f'Parent: {self.parent}\n'
        components = f'Components: {", ".join([component.name for component in self.components])}\n'
        dependencies = f'Dependencies: {dependencies}\n'
        dependents = f'Dependents: {dependents}\n'
        return name + parent + components + dependencies + dependents 

    def add_component(self, component: Union[Task, Schedule]):
        if component not in self:
            self.components.append(component)
            component.parent = self 

        for dependency in component.dependencies:
            self._add_dependency(dependency)
        
        for dependent in component.dependents:
            self._add_dependent(dependent)


    def _add_dependency(self, task):
        if task not in self:
            self.dependencies = list(set(self.dependencies + [task]))

    def _add_dependent(self, task):
        if task not in self:
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
            print(component)
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

    def __iadd__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
            self.add_component(component)

    def __contains__(self, components):
        if not isinstance(components, list): components = [components]
        return set(components).issubset(set(self.components))
