
from enum import Enum
from .Operation_mode import Operation_mode
from .Nexus import NexusOutput

class State(Enum):
    STOPPED = 0
    FLEXED = 1
    EXTENDED = 2

class OutputCommand(Enum):
    STOP = 0
    FLEX = 1
    EXTEND = 2

class Mode(Enum):
    CONTINUOUS = 1
    TOGGLE = 2
    TIMED = 3
    MODULAR = 4
    
#####################################
"""
Created on Wed Jun 12 10:28:52 2019

@author: charl
"""

#Continuous state
class Continuous_Condition(Operation_mode):
    
    
    def __init__(self):
        return
    
    def process(self, BMI_input):
        if BMI_input == NexusOutput.MOVE:
            Hardware_output = OutputCommand.FLEX
        else:
            Hardware_output = OutputCommand.EXTEND
        return Hardware_output

#Toggle state
class Toggle_Condition(Operation_mode):
    
    def __init__(self, state = State.STOPPED):
        self.state = state
        return
    
    def process(self, BMI_input):
        if BMI_input == NexusOutput.MOVE and self.state != State.FLEXED:
            Hardware_output = OutputCommand.FLEX
            self.state = State.FLEXED
        elif BMI_input == NexusOutput.MOVE and self.state != State.EXTENDED:
            Hardware_output = OutputCommand.EXTEND
            self.state = State.EXTENDED
        elif BMI_input == NexusOutput.REST and self.state == State.FLEXED:
            Hardware_output = OutputCommand.FLEX
        else:
            Hardware_output = OutputCommand.STOP
        
        return Hardware_output
