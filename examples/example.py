from goatscheduler.Task import Task
from goatscheduler.Schedule import Schedule 
from goatscheduler.Scheduler import Scheduler

import time

# First define the callables. In a real use case you'd be importing from your moduels/libraries to have access to callables
def sleep_x_secs(x: int) -> None:
    print(f'Going to sleep for {x} seconds')
    time.sleep(x)
    print(f'Finished sleeping!')

def do_crazy_math(x: int, y: int) -> None:
    z = x + y
    return {'result': z}


# Tasks are instantiated with a name, callable, and callable kwargs
do_some_math = Task(name='do_some_math', callable=do_crazy_math, callable_kwargs={'x': 2, 'y': 3})
wait_5_secs = Task(name='wait_5_secs', callable=sleep_x_secs, callable_kwargs={'x': 5})

# do_some_math is declared to be a dependency for wait_5_secs
do_some_math >> wait_5_secs

# We create a schedule for team1 to denote their ownership over the tasks inside, and add the first two tasks to their schedule
team1_schedule = Schedule(name='team1')
team1_schedule += [do_some_math, wait_5_secs]


# we create a final task doing even crazier math
do_final_math = Task(name='do_final_math', callable=do_crazy_math, callable_kwargs={'x': 1000, 'y': 550})

# we declare team1's schedule as a whole to be a dependency for the final math output
team1_schedule >> do_final_math

# Instantiate the scheduler and tell it to start
scheduler = Scheduler(name='goatscheduler_test', reset_backend=True)
scheduler.start(refresh_secs=2)