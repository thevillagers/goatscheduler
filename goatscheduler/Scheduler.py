from __future__ import annotations
import gc 
from importlib import reload
from .Task import Task 
from .Schedule import Schedule 
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
        for obj in gc.get_objects():
            if isinstance(obj, Task):
                self.tasks.append(obj)
            elif isinstance(obj, Schedule):
                self.schedules.append(obj)

    def start(self):
        print('Starting scheduler')
        

