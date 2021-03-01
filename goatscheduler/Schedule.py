from __future__ import annotations
from typing import Type, List, Set, Union, AnyStr
from .Task import Task 
from .Component import Component
from .RunState import RunState
from . import logger

ComponentSingleOrList = Union[Type[Component], List[Type[Component]]]

class Schedule(Component):
    """Schedule, the main organizational unit for Tasks
    """

    def __init__(
        self,
        name: str,
        components: List[Type[Component]] = []
    ) -> None:
        super().__init__(name=name)

        self.components: List[Type[Component]]
        self.components = []

        for component in components:
            self.add_component(component)


    def __str__(self) -> str:
        """String representation of the Schedule

        Returns:
            str: String representation of the Schedule
        """
        dependencies = ', '.join([dependency.name for dependency in self.dependencies])
        dependents = ', '.join([dependent.name for dependent in self.dependents])
        name = f'Schedule: {self.name}\n'
        parent = f'Parent: {self.parent if self.parent is not None else "No parent"}\n'
        components = f'Components: {", ".join([component.name for component in self.components])}\n'
        dependencies = f'Dependencies: {dependencies}\n'
        dependents = f'Dependents: {dependents}\n'
        return name + parent + components + dependencies + dependents 

    def add_component(self, component: Type[Component]) -> None:
        """Adds the specified component to the Schedule

        Args:
            component (Type[Component]): Component to add to the Schedule
        """
        if component not in self:
            logger.log(20, f'Adding component {component.name} to schedule {self.name}')
            self.components.append(component)
            component.parent = self

    def __iadd__(self, components: ComponentSingleOrList) -> None:
        """Add component or list of components to the components list of the Schedule

        Args:
            components (ComponentSingleOrList): Component or list of components to add to the Schedule
        """
        if not isinstance(components, list): components = [components]
        for component in components:
            self.add_component(component)
        return self 

    def __contains__(self, components: ComponentSingleOrList) -> bool:
        """Returns whether or not a component or list of components is contained within the Schedule

        Args:
            components (ComponentSingleOrList): Component or list of components

        Returns:
            bool: True if all passed components are contained in the Schedule, False otherwise
        """
        if not isinstance(components, list): components = [components]
        return set(components).issubset(set(self.components))

    def component_failed(self) -> bool:
        """Returns whether or not any of the components in the Schedule are marked as FAIL

        Returns:
            bool: True if at least one component has status FAIL
        """
        for component in self.components:
            if component.get_state() is RunState.FAIL:
                return True 
        return False 

    def components_successful(self) -> bool:
        """Returns whether or not all components in the Schedule are marked as SUCCESS

        Returns:
            bool: True if all components have state SUCCESS, False otherwise
        """
        for component in self.components:
            if component.get_state() is not RunState.SUCCESS:
                return False 
        return True 

    def refresh_state(self) -> None:
        """Refreshes the state of the schedule.
        """
        if self.parent is not None and self.parent.get_state() is not RunState.READY:
            return # Don't do anything if the parent is not ready 
        if not self.dependencies_successful():
            return
        if self.components_successful():
            self.set_state(RunState.SUCCESS)
            return 
        elif self.component_failed():
            self.set_state(RunState.FAIL)
            return 
        else: 
            self.set_state(RunState.READY)
            return 
