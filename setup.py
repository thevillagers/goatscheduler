'''
setup.py
(c) Vinny Meller

setup script for goatscheduler, a lightweight, flexible scheduler tor many possible workflows
'''

from setuptools import setup, find_packages
from codecs import open
import os 

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().splitlines()

with open(os.path.join(HERE, 'VERSION'), encoding='utf-8') as f:
    VERSION = f.read().strip()

with open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name                = 'goatscheduler',
    version             = VERSION,
    description         = 'GOAT Scheduler',
    long_description    = LONG_DESCRIPTION,
    url                 = 'https://www.github.com/thevillagers/goatscheduler',
    author              = 'Vinny Meller',
    author_email        = 'vinny@goathousing.com',
    license             = 'License :: OSI Approved :: MIT License',
    keywords            = 'scheduler flexible task',
    packages            = find_packages(exclude=[]),
    package_data        = {'goatscheduler': ['VERSION'],},
    install_requires    = install_requires,
)
   
