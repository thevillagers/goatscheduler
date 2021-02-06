from __future__ import annotations
from typing import Type, List, Set, Union, AnyStr
from .Task import Task 
from .Component import Component



class Schedule(Component):

    def __init__(
        self,
        name: str,
        parent: Schedule = None,
        components: List[Type[Component]] = [],
        dependencies: List[Type[Component]] = [],
        dependents: List[Type[Component]] = []
    ) -> None:
        super().__init__(
            name=name,
            parent=parent,
            dependencies=dependencies,
            dependents=dependents
        )
        self.components: List[Union[Task, Schedule]]    = []

        for component in components:
            self.add_component(component)


    def __str__(self):
        dependencies = ', '.join([dependency.name for dependency in self.dependencies])
        dependents = ', '.join([dependent.name for dependent in self.dependents])
        name = f'Schedule: {self.name}\n'
        parent = f'Parent: {self.parent if self.parent is not None else "No parent"}\n'
        components = f'Components: {", ".join([component.name for component in self.components])}\n'
        dependencies = f'Dependencies: {dependencies}\n'
        dependents = f'Dependents: {dependents}\n'
        return name + parent + components + dependencies + dependents 

    def add_component(self, component: Union[Task, Schedule]):
        if component not in self:
            print(f'Adding component {component.name} to {self.name}')
            self.components.append(component)
            component.parent = self

    def __iadd__(self, components):
        if not isinstance(components, list): components = [components]
        for component in components:
            self.add_component(component)

    def __contains__(self, components):
        if not isinstance(components, list): components = [components]
        return set(components).issubset(set(self.components))
