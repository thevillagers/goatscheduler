from __future__ import annotations
from typing import Type, List, Set, Union, AnyStr
import datetime
from enum import Enum 

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


    def has_run(self):
        return self.state is RunState.SUCCESS or self.state is RunState.FAIL

    def is_running(self):
        return self.state is RunState.RUNNING

    def is_ready(self):
        raise NotImplementedError

    def refresh_state(self):
        raise NotImplementedError
    
    def set_state(self, state):
        self.state = state

    
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
    