from __future__ import annotations
from typing import Type, List, Set, Union, AnyStr


class Component:

    def __init__(
        self,
        name: str,
        parent: Schedule = None,
    ):
        self.name           = name 
        self.parent         = parent 
        
        self.dependencies   = []
        self.dependents     = []

        self.status_dict    = {}


    def __str__(self):
        # Implement this for task and schedule separately
        raise NotImplementedError

    def _add_dependency(self, component):
        print(f'calling _add_dependency on {self.name} with {component.name}')
        self.dependencies.append(component)

    def _add_dependent(self, component):
        print(f'calling _add_dependent on {self.name} with {component.name}')
        self.dependents.append(component)

    def runs_before(self, component):
        component._add_dependency(self)
        self._add_dependent(component)

    def runs_after(self, component):
        self._add_dependency(component)
        component._add_dependent(self)

    def __rshift__(self, components):
        if not isinstance(components, list): components = [components]
        print(len(components))
        for component in components:
            self.runs_before(component)
        
        if len(components) == 1: return components[0]
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
        if len(components) == 1: return components[0]
        return components 

    def __rlshift__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
            self.runs_before(component)
        return self 

    def check_ready_status(self):
        raise NotImplementedError