""" 
RunSchedule.py
defines the class that controls how and when tasks get run
"""
from pytimeparse import parse
import pycron
from datetime import datetime, timedelta
class TaskRunHandler():

    def __init__(
        self,
        cron: str = None,
        rerun_interval: str = None,
        run_offset: str = None
    ):
        self.cron = cron

        # parse if rerun_interval is passed
        if rerun_interval:
            self.rerun_interval = parse(rerun_interval)
        else: 
            self.rerun_interval = None
        
        # prase if run_offset is passed
        if run_offset:
            self.run_offset = parse(run_offset)
        else: 
            self.run_offset = None 

        self.init_time = datetime.now()
        self.last_run = None

    def run_now(self):
        """Check whether 

        Returns:
            [type]: [description]
        """
        if self.cron:
            if pycron.is_now(self.cron):
                return True 
        if self.rerun_interval:
            if self.last_run:
                if datetime.now() > self.last_run + timedelta(seconds=self.rerun_interval):
                    return True 
            else: 
                if self.run_offset:
                    if datetime.now() > self.init_time + timedelta(seconds=self.run_offset):
                        return True
                else: 
                    return True 
        return False 
