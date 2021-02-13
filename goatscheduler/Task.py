from __future__ import annotations
from typing import Callable, Union, List, Type
from .Component import Component, RunState
import datetime
from pytimeparse import parse
from enum import Enum

class Task(Component):





    def __init__(
        self,
        name: str,
        callable: Callable,
        callable_kwargs: dict = {},
        parent: Schedule = None,
        run_interval: str = None
    ):
        super().__init__(
            name=name,
            parent=parent
        )
        self.callable           = callable
        self.callable_kwargs    = callable_kwargs

        if run_interval is not None:
            self.run_interval = parse(run_interval)
        else:
            self.run_interval = None 

        self.last_run_timestamp = None


    def __str__(self):
        dependencies = f'Dependencies: {", ".join([dependency.name for dependency in self.dependencies])}\n' 
        dependents = f'Dependents: {", ".join([dependent.name for dependent in self.dependents])}\n'
        name = f'Task: {self.name}\n'
        parent = f'Parent: {self.parent.name if self.parent is not None else "No parent"}\n'
        return name + parent + dependencies + dependents 

    def run(self):
        self.state = RunState.RUNNING 
        try: 
            function_return = self.callable(**self.callable_kwargs)
            if isinstance(function_return, dict):
                pass # do something later
            self.set_state(RunState.SUCCESS)
        except Exception as e:
            self.set_state(RunState.FAIL)
            self.propagate_state_downstream(RunState.NOT_READY)
            print(e)

    ## state related functions

    def dependencies_successful(self):
        for dependency in self.dependencies:
            if dependency.state is not RunState.SUCCESS:
                return False 
        return True


    def refresh_state(self):
        if not self.dependencies_successful():
            return 
        


    def is_ready(self):
        if not self.dependencies_successful():
            return False    # If dependencies aren't all success yet, return False but don't change state
        if self.is_running():
            return False    # Return false if already running, but don't change the state
        if self.has_run():
            if self.run_interval is None:
                return False    # Return false if already ran and there is no run interval, but don't change the state from Succes or Fail
            if datetime.datetime.now() > self.last_run_timestamp + datetime.timedelta(seconds=self.run_interval):   # If there is a run interval and it already ran, set the state to Ready, clear all the dependents
                self.set_state(RunState.READY)
                self.propagate_state_downstream(RunState.NONE)
                return True 
            else:
                return False    # return False but don't change the state if it ran but is not ready to rerun yet
        else:
            self.set_state(RunState.READY)  #  if it hasn't run yet set the state to ready and return true
            return True
