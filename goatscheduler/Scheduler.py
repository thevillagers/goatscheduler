from __future__ import annotations
import gc 
from importlib import reload
from .Task import Task 
from .Schedule import Schedule 
import time
import threading
'''
Scheduler.py
defines the Scheduler class for scheduling your tasks to run
'''



class Scheduler():

    def __init__(
        self,
        max_threads: int = 3
    ):
        self.schedules = []
        self.tasks = []
        self.components = []
        self.max_threads = max_threads
        self.task_threads = []
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


    def _refresh_schedule_states(self):
        for schedule in self.schedules:
            schedule.refresh_state()

    def _refresh_task_states(self):
        for task in self.tasks:
            task.refresh_state()

    def _run_ready_tasks(self):
        print(f'Preparing to run ready tasks')
        thread_idx_to_kill = []
        for i, task_thread in enumerate(self.task_threads):
            if not task_thread.is_alive():
                thread_idx_to_kill.append(i)
        for i in sorted(thread_idx_to_kill, reverse=True): # delete references to dicts from the worker list
            del self.task_threads[i]
        
        i = 0
        while len(self.task_threads) < self.max_threads and i < len(self.tasks):
            if self.tasks[i].state['ready']:
                print(f'Starting task {self.tasks[i].name}')
                self.task_threads.append(threading.Thread(target=self.tasks[i].run))
                self.task_threads[-1].start()
            i += 1
        print(f'Ran all possible ready tasks')

    
    def start(
        self,
        refresh_secs: int = 10,
        max_threads: int = 3
    ):
        print('Starting scheduler')
        while(True):        # loop 4eva
            self._refresh_schedule_states()
            self._refresh_task_states()
            self._run_ready_tasks()

            # set ready tasks to run
            print(f'Sleeping for {refresh_secs} seconds')
            time.sleep(refresh_secs)    # wait to check again
        

