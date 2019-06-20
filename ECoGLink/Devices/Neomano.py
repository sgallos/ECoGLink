
from enum import Enum
from .Operation_mode import Operation_mode
from ECoGLink.Devices import Device
import ECoGLink.Devices.Nexus as Nexus
import time

class State():
    STOPPED = 0
    FLEXED = 1
    EXTENDED = 2
    
    def __init__(self, initValue = STOPPED):
        self.__state = initValue
    
    def set(self, newValue):
        self.__state = newValue
        
    def get(self):
        return self.__state

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

@author: Charlie & Kevin
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
            timeout = False
        else:
            Hardware_output = Output_Command.EXTEND
            timeout = False
        return Hardware_output, timeout

#Toggle state
class Toggle_Condition(Operation_mode):
    
    def __init__(self, DeviceStateRef):
        self.state = DeviceStateRef
        print("New Toggle Condition")
        return
    
    def process(self, BMI_input):
        #
        # If Move signal and prior was not previously flexed set flexion to max length
        # If Move signal and prior was previously flexed extend to origin
        # If Rest signal maintain current state of flexion
        #
        if BMI_input == Nexus.ClassifiedInput.MOVE and self.state.get() == State.EXTENDED:
            Hardware_output = Output_Command.FLEX
            timeout = True
          
        elif BMI_input == Nexus.ClassifiedInput.MOVE and self.state.get() == State.FLEXED:
            Hardware_output = Output_Command.EXTEND
            timeout = True
            
        elif BMI_input == Nexus.ClassifiedInput.REST and self.state.get() == State.FLEXED:
            Hardware_output = Output_Command.FLEX
            timeout = False
        elif BMI_input == Nexus.ClassifiedInput.REST and self.state.get() == State.EXTENDED:
            Hardware_output = Output_Command.EXTEND
            timeout = False
        
        return Hardware_output, timeout


class Neomano(Device):
    
    name = 'SLAB_USBtoUART'
    __flex_time = 1
    __extend_time = 1
    
    def __init__(self):     
        self.state = State(State.EXTENDED)
        self.toggle_state = False
        self.time_start = 0
        self.timeout = False
        self.time_remaining = 0
        self.time_condition_delay = 1
        self.time_step = 0
        self.number_step = 0
        self.total_step = 0
        self.mode = Mode.CONTINUOUS
        self.modes = {
                Mode.CONTINUOUS: Continuous_Condition(),
                Mode.TOGGLE: Toggle_Condition(self.state),
                Mode.TIMED: Time_Based_Condition()
                }
        
    def stop(self):
        pass
    
    def is_connected():
        pass
    
    def process(self, signal_input):
            
        condition = self.modes[self.mode]
        hardward_output, timeoutpro = condition.process(signal_input)
        ############### fix this shit#############
        if self.mode == Mode.TOGGLE:
            if hardward_output == Output_Command.FLEX:
                self.state.set(State.FLEXED)
            elif hardward_output == Output_Command.EXTEND:
                self.state.set(State.EXTENDED)
            self.timeout = timeoutpro
            if self.timeout == True:
                time.sleep(1)
                if self.toggle_state == False:
                    self.toggle_state = True
                else:
                    self.toggle_state = False
        if self.mode == Mode.CONTINUOUS:
            if hardward_output == Output_Command.FLEX:
                self.state.set(State.FLEXED)
            elif hardward_output == Output_Command.EXTEND:
                self.state.set(State.EXTENDED)
        if self.mode == Mode.TIMED:
            self.timeout = timeoutpro
            if self.timeout == True:
                if hardward_output == Output_Command.FLEX:
                    time.sleep(self.__flex_time)
                    time.sleep(self.time_condition_delay)
                    time.sleep(self.__extend_time)
                    self.state.set(State.EXTENDED)
            if hardward_output == Output_Command.EXTEND:
                self.state.set(State.EXTENDED)
        return

#    
#    modes = [toggle, continuous, timed, modular]
#    
#    mode = mode[0]
#    
#    def process(NexusInput):
#        output, timout = self.get_mode().process(NexusInput)
        
        pass

    
# Time based stated
class Time_Based_Condition():
    # rewrite condition to account for sleeping
    def __init__(self):
        
        return
    
    def process(self, BMI_input):
        if BMI_input == Nexus.ClassifiedInput.REST:
                Hardware_output = Output_Command.EXTEND
                timeout = False
            
        elif BMI_input == Nexus.ClassifiedInput.MOVE:
                Hardware_output = Output_Command.FLEX
                timeout = True
            
            
        return Hardware_output, timeout
