
from enum import Enum
from .Operation_mode import Operation_mode
from .Nexus import NexusOutput

class Neomano_state(Enum):
    STOPPED = 0
    FLEXED = 1
    EXTENDED = 2

class Neomano_output(Enum):
    STOP = 0
    FLEX = 1
    EXTEND = 2

class Neomano_mode(Enum):
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
            Hardware_output = Neomano_output.FLEX
        else:
            Hardware_output = Neomano_output.EXTEND
        return Hardware_output

#Toggle state
class Toggle_Condition(Operation_mode):
    
    def __init__(self, state = Neomano_state.STOPPED):
        self.state = state
        return
    
    def process(self, BMI_input):
        if BMI_input == NexusOutput.MOVE and self.state != Neomano_state.FLEXED:
            Hardware_output = Neomano_output.FLEX
            self.state = Neomano_state.FLEXED
        elif BMI_input == NexusOutput.MOVE and self.state != Neomano_state.EXTENDED:
            Hardware_output = Neomano_output.EXTEND
            self.state = Neomano_state.EXTENDED
        elif BMI_input == NexusOutput.REST and self.state == Neomano_state.FLEXED:
            Hardware_output = Neomano_output.FLEX
        else:
            Hardware_output = Neomano_output.STOP
        
        return Hardware_output
