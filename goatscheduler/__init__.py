from .Logger import Logger 
from .API import BackendAPI 
import threading 
import os 
import shutil

# Check that required prereqs exist
if shutil.which('npm') is None:
    print('you must have npm installed to run this')
    raise Exception

if shutil.which('vue') is None:
    print('you must have vue installed to run this')
    raise Exception


logger = Logger().logger


def run_frontend():
    curr_path = os.path.dirname(os.path.abspath(__file__))
    frontend_path = os.path.join(curr_path, 'frontend')
    os.system(f'npm --prefix {frontend_path} run serve')

frontend = threading.Thread(target=run_frontend)
frontend.start()
