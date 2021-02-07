from __future__ import annotations
import gc 
from importlib import reload
from .Task import Task 
from .Schedule import Schedule 
import time 
'''
Scheduler.py
defines the Scheduler class for scheduling your tasks to run
'''



class Scheduler():

    def __init__(
        self
    ):
        self.schedules = []
        self.tasks = []
        self.components = []
        for obj in gc.get_objects():
            if isinstance(obj, Task):
                self.tasks.append(obj)
                self.components.append(obj)
            elif isinstance(obj, Schedule):
                self.schedules.append(obj)
                self.components.append(obj)


        self.schedule_states = {
            'ready': set(),
            'not_ready': set([schedule for schedule in self.schedules])
        }
        self.task_states = {
            'ready': set(),
            'not_ready': set([task for task in self.tasks])
        }


    def _find_ready_schedules(self):
        for schedule in self.schedule_states['not_ready']:
            if schedule.check_ready_status():
                print(f'Moving schedule {schedule.name} to state: ready')
                self.schedule_states['ready'].add(schedule)
        self.schedule_states['not_ready'] -= self.schedule_states['ready']

    def _find_ready_tasks(self):
        for task in self.task_states['not_ready']:
            if task.check_ready_status():
                print(f'Moving task {task.name} to state: ready')
                self.task_states['ready'].add(task)
        self.task_states['not_ready'] -= self.task_states['ready']

    def start(
        self,
        refresh_secs: int = 10,
    ):
        print('Starting scheduler')
        while(True):        # loop 4eva
            self._find_finished_tasks()
            self._find_ready_schedules()
            self._find_ready_tasks()
            self._run_ready_tasks()

            # set ready tasks to run
            time.sleep(refresh_secs)    # wait to check again
        

