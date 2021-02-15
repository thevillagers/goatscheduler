from __future__ import annotations
from typing import Callable, Union, List, Type
from .Component import Component, RunState
import datetime
from pytimeparse import parse
from enum import Enum
import io 
from contextlib import redirect_stdout
from . import logger

class Task(Component):
    """Task, the building blocks of the scheduler.
    """

    def __init__(
        self,
        name: str,
        callable: Callable,
        callable_kwargs: dict = {},
        run_interval: str = None
    ):
        """Instantiate a Task. Used for making schedules.

        Args:
            name (str): Unique name for logging and the UI to distinguish this component from others
            callable (Callable): The Python callable that this Task should run
            callable_kwargs (dict, optional): If your function takes arguments, pass them as a dictionary here. Defaults to {}.
            run_interval (str, optional): If you want your task to run repeatedly after an amount of time, specify it here. Defaults to None.
        """
        super().__init__(name=name)
        self.callable           = callable
        self.callable_kwargs    = callable_kwargs

        self.run_interval: int
        if run_interval is not None:
            self.run_interval = parse(run_interval)
        else:
            self.run_interval = None 

        self.last_run_timestamp: datetime.datetime
        self.last_run_timestamp = None


    def __str__(self) -> str:
        """Returns string representation of this Task

        Returns:
            str: String representation of this Task
        """
        dependencies = f'Dependencies: {", ".join([dependency.name for dependency in self.dependencies])}\n' 
        dependents = f'Dependents: {", ".join([dependent.name for dependent in self.dependents])}\n'
        name = f'Task: {self.name}\n'
        parent = f'Parent: {self.parent.name if self.parent is not None else "No parent"}\n'
        return name + parent + dependencies + dependents 

    def run(self) -> None:
        """Runs the callable specified for this task and does some work to track the state of the run

        Returns:
            None, will be a dictionary in a later version.
        """
        self.set_state(RunState.RUNNING)
        self.last_run_timestamp = datetime.datetime.now()
        f = io.StringIO()
        with redirect_stdout(f):
            try: 
                function_return = self.callable(**self.callable_kwargs)
                if isinstance(function_return, dict):
                    pass # do something later

                self.set_state(RunState.SUCCESS)
            except Exception as e:
                self.set_state(RunState.FAIL)
                self.propagate_state_downstream(RunState.NOT_READY)
                logger.log(30, f'<{e}>')
        out = f.getvalue()
        logger.log(20, f'{self.name}:\n{out}')


    def refresh_state(self) -> None:
        """Refreshes the state of the Task
        """
        if self.has_run():
            if self.run_interval is None: 
                return  # Don't change state if it has already run and isn't set to rerun
            elif datetime.datetime.now() > self.last_run_timestamp + datetime.timedelta(seconds=self.run_interval):
                if self.parent is not None:
                    self.parent.set_state(RunState.NONE)
                self.set_state(RunState.NONE)
                self.propagate_state_downstream(RunState.NONE)  # reset the state of anything downstream of current task if this is set to rerun
                return 
            else: 
                return 


        if self.parent is not None and self.parent.state is not RunState.READY:
            return # don't do anything if the parent is not ready
        if not self.dependencies_successful() or self.is_running():
            return  # Don't change state if dependencies weren't all success or if it is running
        if self.has_run():
            if self.run_interval is None: 
                return  # Don't change state if it has already run and isn't set to rerun
            elif datetime.datetime.now() > self.last_run_timestamp + datetime.timedelta(seconds=self.run_interval):
                self.set_state(RunState.READY)
                self.propagate_state_downstream(RunState.NONE)  # reset the state of anything downstream of current task if this is set to rerun
                return 
            else: 
                return 
        else: 
            self.set_state(RunState.READY)
            return 

