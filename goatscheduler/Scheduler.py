from __future__ import annotations
import gc 
from importlib import reload
from .Component import Component
from .RunState import RunState
from .Task import Task 
from typing import List 
from .Schedule import Schedule 
from .SchedulerBackend import SchedulerBackend
import time
import threading
from . import logger
'''
Scheduler.py
defines the Scheduler class for scheduling your tasks to run
'''



class Scheduler():
    """Scheduler to run workflows
    """

    def __init__(
        self,
        name: str,
        max_threads: int = 3,
        reset_backend: bool = False
        ) -> None:
        """Initializes scheduler to run your workflow

        Args:
            max_threads (int, optional): Max amount of threads to run your Tasks. Defaults to 3.
        """
        self.name = name
        self.backend = SchedulerBackend(scheduler_name=self.name, reset_backend=reset_backend)

        self.schedules: List[Schedule]
        self.schedules = []

        self.tasks: List[Task]
        self.tasks = []

        self.components: List[Component]
        self.components = []

        self.max_threads: int
        self.max_threads = max_threads

        self.task_threads: List[dict]
        self.task_threads = []

        for obj in gc.get_objects():
            if isinstance(obj, Task):
                self.tasks.append(obj)
                self.components.append(obj)
                self.backend.add_component(name=obj.name, component_type='task')
                obj.backend = self.backend
            elif isinstance(obj, Schedule):
                self.schedules.append(obj)
                self.components.append(obj)
                self.backend.add_component(name=obj.name, component_type='schedule')
                obj.backend = self.backend



        for component in self.components:
            for dependency in component.dependencies:
                self.backend.add_component_dependency(component_name=component.name, dependency_name=dependency.name)
            for dependent in component.dependents:
                self.backend.add_component_dependent(component_name=component.name, dependent_name=dependent.name)
            


    def _refresh_schedule_states(self) -> None:
        """Refreshes the states of the Schedules in the Scheduler
        """
        for schedule in self.schedules:
            schedule.refresh_state()

    def _refresh_task_states(self) -> None:
        """Refreshes the states of the Tasks in the Scheduler
        """
        for task in self.tasks:
            task.refresh_state()
    
    def kill_dead_threads(self) -> None:
        """Kills the threads that have finished running (or timed out)
        """
        thread_idx_to_kill = []
        for i, task_thread in enumerate(self.task_threads):
            if not task_thread['thread'].is_alive():
                thread_idx_to_kill.append(i)
        for i in sorted(thread_idx_to_kill, reverse=True):
            logger.log(20, f'Killing thread {i} - ran task {self.task_threads[i]["task"].name}')
            del self.task_threads[i]
    
    def run_ready_tasks(self) -> None:
        """Runs any tasks that are ready up to the number of max threads
        """
        i = 0
        while len(self.task_threads) < self.max_threads and i < len(self.tasks):
            if self.tasks[i].get_state() is RunState.READY:
                new_task_thread = {
                    'task': self.tasks[i],
                    'thread': threading.Thread(target=self.tasks[i].run)
                }
                self.task_threads.append(new_task_thread)
                logger.log(20, f'Starting thread {len(self.task_threads)-1} - running task {self.tasks[i].name}')
                self.task_threads[-1]['thread'].start()
            i += 1


    def refresh_states(self, refresh_secs: int) -> None:
        """Refreshes the states of Schedules and then Tasks, then sleeps. Loops forever.

        Args:
            refresh_secs (int): The amount of seconds to sleep in between refreshing states.
        """
        while True:
            self._refresh_schedule_states()
            self._refresh_task_states()
            time.sleep(refresh_secs)

    def handle_task_threads(self, refresh_secs: int) -> None:
        """Handles the whole process of killing and starting new threads.
        Kills dead threads and then runs ready tasks. Sleeps in between and loops forever.

        Args:
            refresh_secs (int): The amount of seconds to sleep in between refreshing states.
        """
        while True:
            self.kill_dead_threads()
            self.run_ready_tasks()
            time.sleep(refresh_secs)

    def start(self, refresh_secs: int = 5) -> None:
        """Starts the scheduler

        Args:
            refresh_secs (int, optional): The number of seconds to sleep between refreshing states and starting & killing threads. Defaults to 5.
        """
        logger.log(20, f'Starting scheduler {self.name}')
        
        refresh_states_thread = threading.Thread(target=self.refresh_states, args=(refresh_secs,))
        handle_task_threads = threading.Thread(target=self.handle_task_threads, args=(refresh_secs,))

        refresh_states_thread.start()
        handle_task_threads.start()
        

