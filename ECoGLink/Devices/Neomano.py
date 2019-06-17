
from enum import Enum
from .Operation_mode import Operation_mode
import ECoGLink.Devices.Nexus as Nexus
from ECoGLink.Devices import Device

class State(Enum):
    STOPPED = 0
    FLEXED = 1
    EXTENDED = 2

class Output_Command(Enum):
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
        if BMI_input == Nexus.ClassifiedInput.MOVE:
            Hardware_output = Output_Command.FLEX
        else:
            Hardware_output = Output_Command.EXTEND
        return Hardware_output

#Toggle state
class Toggle_Condition(Operation_mode):
    
    def __init__(self, state = State.STOPPED):
        self.state = state
        return
    
    def process(self, BMI_input):
        if BMI_input == Nexus.ClassifiedInput.MOVE and self.state != State.FLEXED:
            Hardware_output = Output_Command.FLEX
            self.state = State.FLEXED
        elif BMI_input == Nexus.ClassifiedInput.MOVE and self.state != State.EXTENDED:
            Hardware_output = Output_Command.EXTEND
            self.state = State.EXTENDED
        elif BMI_input == Nexus.ClassifiedInput.REST and self.state == State.FLEXED:
            Hardware_output = Output_Command.FLEX
        else:
            Hardware_output = Output_Command.STOP
        
        return Hardware_output

class Neomano(Device):
    name = "SLAB_USBtoUART"
