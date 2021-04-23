# goatscheduler
python scheduler 


Must have node & vue installed

Once cloing the repo, be sure to run "npm install" in goatscheduler/frontend. I'll automate this part eventually.




Usage:

There are two distinct entities in GOAT Scheduler, a Schedule and a Task. 

Tasks are what actually get run - they're defined by a Python callable passed in when instantiating a new task.

Schedules are collections of Tasks or other Schedules (they can infinitely nest).