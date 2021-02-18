from enum import Enum


class RunState(Enum):
    NONE        = 1
    READY       = 2
    NOT_READY   = 3 
    RUNNING     = 3
    SUCCESS     = 4 
    FAIL        = 5
