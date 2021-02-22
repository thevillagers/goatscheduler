from __future__ import annotations
from typing import Type, List, Union
import datetime
from .RunState import RunState
from . import logger
from .SchedulerBackend import SchedulerBackend

ComponentSingleOrList = Union[Type['Component'], List[Type['Component']]]

# The parent class for tasks and schedules
class Component:
    """There should never be an instance of this class Component. Make a Task or Schedule.
    """

    def __init__(self, name: str) -> None:
        """Initializes the required pieces for a Component, the base of Tasks and Schedules

        Args:
            name (str): A unique name for logging and UI purposes
        """
        self.name = name 

        self.backend: SchedulerBackend
        self.backend = None 

        self.parent: Schedule
        self.parent = None 
    
        self.dependencies: List[Type[Component]]
        self.dependencies = []

        self.dependents: List[Type[Component]]
        self.dependents = []

        self.init_timestamp: datetime.datetime
        self.init_timestamp = datetime.datetime.now()




    def __str__(self) -> str:
        """Defines the string representation for a component

        Raises:
            NotImplementedError: This function is not implemented for the base class "Component".
            Children must implement it.
        """
        raise NotImplementedError

    def _add_dependency(self, component: Type[Component]) -> None:
        """Adds a component to the list of dependencies

        Args:
            component (Type[Component]): Component to add as a dependency
        """
        #logger.log(20, f'Adding dependency {component.name} to {self.name}')
        self.dependencies.append(component)

    def _add_dependent(self, component: Type[Component]) -> None:
        """Adds a component to the list of dependents

        Args:
            component (Type[Component]): Component to add as a dependent
        """
        #logger.log(20, f'Adding dependent {component.name} to {self.name}')
        self.dependents.append(component)

    def runs_before(self, component: Type[Component]) -> None:
        """Adds the necessary links to say this component runs before the passed component

        Args:
            component (Type[Component]): The component that self runs before
        """
        component._add_dependency(self)
        self._add_dependent(component)

    def runs_after(self, component: Type[Component]) -> None:
        """Adds the necessary links to say this component runs after the passed component

        Args:
            component (Type[Component]): The component that self runs after
        """
        self._add_dependency(component)
        component._add_dependent(self)

    def __rshift__(self, components: Type[Component]) -> ComponentSingleOrList:
        """Adds the necessary links to say the left component runs before the right component(s)

        Args:
            components (Type[Component]): Component of list of components to run after the left component

        Returns:
            ComponentSingleOrList: The right side of the operator, either a component or list of components
        """
        if not isinstance(components, list): components = [components]
        for component in components:
            self.runs_before(component)
        
        if len(components) == 1: return components[0]
        return components

    def __rrshift__(self, components: ComponentSingleOrList) -> Type[Component]:
        """Adds the necessary links to say the left component(s) run before the right component

        Args:
            components (ComponentSingleOrList): A component. I think it can't be a list.

        Returns:
            Type[Component]: Returns the right side, which I think has to be 1 component and not a list.
        """
        if not isinstance(components, list): components = [components]
        for component in components:
            self.runs_after(component)
        return self 

    def __lshift__(self, components: Type[Component]) -> ComponentSingleOrList:
        """Adds the necessary links to say the left component runs after the right component(s)

        Args:
            components (Type[Component]): Component or list of components

        Returns:
            ComponentSingleOrList: Component or list of components from the right side of the operator
        """
        if not isinstance(components, list): components = [components]
        for component in components:
            self.runs_after(component)
        if len(components) == 1: return components[0]
        return components 

    def __rlshift__(self, components: ComponentSingleOrList) -> Type[Component]:
        """Adds the necessary links to say the left component(s) run after the right component

        Args:
            components (ComponentSingleOrList): A component

        Returns:
            Type[Component]: The component on the right side of the operator
        """
        if not isinstance(components, list): components = [components]
        for component in components:
            self.runs_before(component)
        return self 

    def get_state(self) -> RunState:
        return self.backend.get_component_state(name=self.name)

    def has_run(self) -> bool:
        """Returns whether or not the component has already run

        Returns:
            bool: True = state is SUCCESS or FAIL, False = anything else
        """
        state = self.get_state()
        return state is RunState.SUCCESS or state is RunState.FAIL

    def is_running(self) -> bool:
        """Returns whether or not the component is currently running

        Returns:
            bool: True if component state is RUNNING, false otherwise
        """
        state = self.get_state()
        return state is RunState.RUNNING

    def set_state(self, state: RunState) -> None:
        """Sets the state of self to the passed state

        Args:
            state (RunState): the desired new state of the component
        """
        if self.backend is None:
            logger.log(40, f'Idiot, can\'t change state with no backend')
            raise Exception
        curr_state = self.get_state()
        if state is curr_state:
            return
        self.backend.update_component_state(name=self.name, state=state)
        logger.log(20, f'State of {self.name} changed from {curr_state} to {state}')

    def dependencies_successful(self) -> bool:
        """Returns whether or not the status of all dependencies is SUCCESS

        Returns:
            bool: False if any dependency's state != SUCCESS, True otherwise
        """
        for dependency in self.dependencies:
            if dependency.get_state() is not RunState.SUCCESS:
                return False 
        return True

    def propagate_state_downstream(self, state: RunState) -> None:
        """Sets the state of all dependent tasks recursively to the passed state

        Args:
            state (RunState): The state all downstream tasks will be set to
        """
        logger.log(20, f'Component {self.name} propagating state {state} downstream')
        to_prop = self.dependents
        visited = set()
        parents = set()
        while len(to_prop) > 0:
            component = to_prop[0]
            parent = component.parent
            
            to_prop = to_prop[1:] 

            if parent is not None and parent not in parents:
                parent.set_state(state)

            if component in visited:
                continue 

            component.set_state(state)
            visited.add(component)
            for dependent in component.dependents:
                to_prop.append(dependent)
    
    def refresh_state(self) -> None:
        """Refreshes the state of a component. Needs to be implemented separately for children.

        Raises:
            NotImplementedError: Not implemented for base class Component
        """
        raise NotImplementedError
    