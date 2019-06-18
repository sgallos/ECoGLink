
from enum import Enum
from .Operation_mode import Operation_mode
import ECoGLink.Devices.Nexus as Nexus

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

@author: Charlie
"""

#Continuous state
class Continuous_Condition(Operation_mode):
    
    
    def __init__(self):
        return
    
    def process(self, BMI_input):
        #
        # If Move signal start to flex
        # If Rest signal stop flexion
        # At some signal reset this to start flexion again
        #
        if BMI_input == Nexus.ClassifiedInput.MOVE:
            Hardware_output = Output_Command.FLEX
        else:
            Hardware_output = Output_Command.EXTEND
        return Hardware_output

#Toggle state
class Toggle_Condition(Operation_mode):
    
    def __init__(self, state = State.STOPPED , delay):
        self.state = state
        self.delay = delay
        return
    
    def process(self, BMI_input):
        #
        # If Move signal and prior was not previously flexed set flexion to max length
        # If Move signal and prior was previously flexed extend to origin
        # If Rest signal maintain current state of flexion
        #
        if BMI_input == Nexus.ClassifiedInput.MOVE and self.state != State.FLEXED:
            Hardware_output = Output_Command.FLEX
            timeout = True
          
        elif BMI_input == Nexus.ClassifiedInput.MOVE and self.state != State.EXTENDED:
            Hardware_output = Output_Command.EXTEND
            timeout = True
            
        elif BMI_input == Nexus.ClassifiedInput.REST and self.state == State.FLEXED:
            Hardware_output = Output_Command.FLEX
            timeout = False
        else:
            Hardware_output = Output_Command.STOP
            timeout = False
        
        return Hardware_output, timeout


class Neomano(Device):
    name = "SLAB_USBtoUART"
    __flex_time__ = 3
    __extend_time__ = 3
    
    modes = [toggle, continuous, timed, modular]
    
    mode = mode[0]
    
    def process(NexusInput):
        output, timout = self.get_mode().process(NexusInput)
        
        

    
# Time based state
class Time_Based_Condition():
    
    
    def __init__(self, time_left):
        self.time_left = time_left
        return
    
    def process(self, BMI_input, increment):
        if BMI_input == 1:
            if time_left != 0:
                Hardware_output = 1
                time_left = time_left - increment
                return
            elif time_left == 0:
                Hardware_output = 0
                return
        elif BMI_input == 0:
            if time_left != 0:
                Hardware_output = 1
            Hardware_output = 0

