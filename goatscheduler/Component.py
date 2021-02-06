from __future__ import annotations
from typing import Type, List, Set, Union, AnyStr


class Component:

    def __init__(
        self,
        name: str,
        parent: Schedule = None,
        dependencies: List[Type[Component]] = [],
        dependents: List[Type[Component]] = []
    ):
        self.name           = name 
        self.parent         = parent 
        
        self.dependencies   = dependencies 
        self.dependents     = dependents 

        self.status_dict    = {}


    def __str__(self):
        # Implement this for task and schedule separately
        raise NotImplementedError

    def _add_dependency(self, component):
        if component not in self.dependencies: self.dependencies.append(component)

    def _add_dependent(self, component):
        if component not in self.dependents: self.dependents.append(component)

    def runs_before(self, component):
        component._add_dependency(self)
        self._add_dependent(component)

    def runs_after(self, component):
        self._add_dependency(component)
        component._add_dependent(self)

    def __rshift__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
            self.runs_before(component)
        return components 

    def __rrshift__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
                self.runs_after(component)
        return self 

    def __lshift__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
            self.runs_after(component)
        return components 

    def __rlshift__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
            self.runs_before(component)
        return self 