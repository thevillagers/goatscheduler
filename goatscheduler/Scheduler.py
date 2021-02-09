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

    
    def kill_dead_threads(self):
        thread_idx_to_kill = []
        for i, task_thread in enumerate(self.task_threads):
            if not task_thread['thread'].is_alive():
                thread_idx_to_kill.append(i)
        for i in sorted(thread_idx_to_kill, reverse=True):
            print(f'Finished task {self.task_threads[i]["task"].name}')
            del self.task_threads[i]
    
    def run_ready_tasks(self):
        print(f'Preparing to run ready tasks')
        i = 0
        while len(self.task_threads) < self.max_threads and i < len(self.tasks):
            if self.tasks[i].state['ready']:
                new_task_thread = {
                    'task': self.tasks[i],
                    'thread': threading.Thread(target=self.tasks[i].run)
                }
                self.task_threads.append(new_task_thread)
                print(f'Starting task {self.tasks[i].name}')
                self.task_threads[-1]['thread'].start()
            i += 1
        print(f'Ran all possible ready tasks')


    def refresh_states(self):
        self._refresh_schedule_states()
        self._refresh_task_states()

    def start(
        self,
        refresh_secs: int = 5
    ):
        print('Starting scheduler')
        while(True):        # loop 4eva
            self.refresh_states()
            self.kill_dead_threads()
            self.run_ready_tasks()
            time.sleep(refresh_secs)    # wait to check again
        

