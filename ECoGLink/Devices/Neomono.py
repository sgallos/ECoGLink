
from enum import Enum

class Neomono_state(Enum):
    STOPPED = 0
    FLEXED = 1
    EXTENED = 2

class Neomono_mode(Enum):
    CONTINUOUS = 1
    TOGGLE = 2
    TIMED = 3
    MODULAR = 4
