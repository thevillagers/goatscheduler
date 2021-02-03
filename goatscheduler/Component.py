from __future__ import annotations
from typing import Type, List, Set, Union, AnyStr


class Component:

    def __init__(
        self,
        name: str
    ) -> None:
        self.name                                   = name
        self.dependencies:  List[Type[Component]]   = []
        self.dependents:    List[Type[Component]]   = []

    def __str__(self):
        dependencies = ', '.join([dependency.name for dependency in self.dependencies])
        dependents = ', '.join([dependent.name for dependent in self.dependents])
        return f'Component: {self.name}\nDependencies: {dependencies}\nDependents: {dependents}'


    def _add_dependency(self, component: Type[Component]):
        self.dependencies = list(set(self.dependencies + [component]))

    def _add_dependent(self, component: Type[Component]):
        self.dependents = list(set(self.dependents + [component]))

    def add_dependency_link(self, component: Type[Component]):
        component._add_dependency(self)
        self._add_dependent(component)
    
    def __rshift__(self, component: Type[Component]):
        self.add_dependency_link(component)

    def __rrshift__(self, components: List[Type[Component]]):
        for component in components:
            if isinstance(component, Component):
                component.add_dependency_link(self)

    def __lshift__(self, component: Type[Component]):
        component.add_dependency_link(self)

    def __rlshift__(self, components: List[Type[Component]]):
        for component in components:
            if isinstance(component, Component):
                self.add_dependency_link(component)