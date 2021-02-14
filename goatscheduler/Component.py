from __future__ import annotations
from typing import Type, List, Set, Union, AnyStr
import datetime
from enum import Enum
from . import logger

class RunState(Enum):
    NONE        = 1
    READY       = 2
    NOT_READY   = 3 
    RUNNING     = 3
    SUCCESS     = 4 
    FAIL        = 5


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

        self.init_timestamp = datetime.datetime.now()

        self.state          = RunState.NONE 



    def __str__(self):
        # Implement this for task and schedule separately
        raise NotImplementedError

    def _add_dependency(self, component):
        logger.log(20, f'<Adding dependency {component.name} to {self.name}>')
        self.dependencies.append(component)

    def _add_dependent(self, component):
        logger.log(20, f'<Adding dependent {component.name} to {self.name}>')
        self.dependents.append(component)

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


    def has_run(self):
        return self.state is RunState.SUCCESS or self.state is RunState.FAIL

    def is_running(self):
        return self.state is RunState.RUNNING

    def set_state(self, state):
        if state is self.state: 
            return
        logger.log(20, f'<State of {self.name} changed from {self.state} to {state}>')
        self.state = state

    def dependencies_successful(self):
        for dependency in self.dependencies:
            if dependency.state is not RunState.SUCCESS:
                return False 
        return True

    def propagate_state_downstream(self, state):
        to_prop = self.dependents
        visited = set() 
        while len(to_prop) > 0:
            if to_prop[0] in visited:
                to_prop = to_prop[1:]
                continue 
            component = to_prop[0]
            component.set_state(state)
            visited.add(component)
            for dependent in component.dependents:
                to_prop.append(dependent)
            to_prop = to_prop[1:]
    
    def refresh_state(self):
        raise NotImplementedError
    