import logging 
import sys 
import os 

class Logger:
    def __init__(self):
        log_path = os.path.expanduser('~/.goatscheduler')
        log_file_path = os.path.join(log_path, 'scheduler_log.txt')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
        file_handler = logging.FileHandler(filename=log_file_path)
        stdout_handler = logging.StreamHandler(sys.stdout)
        handlers = [file_handler, stdout_handler]

        logging.basicConfig(
            level=logging.DEBUG, 
            format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - <%(message)s>',
            handlers=handlers
        )

        self.logger = logging.getLogger('GOATSCHEDULER_LOGGER')