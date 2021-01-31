from __future__ import annotations
from typing import Type, List, Set, Union, AnyStr
from .Component import Component
from .Task import Task 



class Schedule(Component):

    def __init__(
        self,
        name: str,
        components: List[Type[Component]] = []
    ) -> None:
        super().__init__(name)
        self.components     = []
        self.add_components(components)

    def add_component(self, component: Type[Component]) -> None:
        self.components.append(component)
        for comp in component.components:
            self.add_dependency_link(comp)

    def add_components(self, components: List[Component]) -> None:
        for component in components:
            self.add_component(component)

