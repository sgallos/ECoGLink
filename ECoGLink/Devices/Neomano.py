
from enum import Enum
from .Operation_mode import Operation_mode
from ECoGLink.Devices import Device
import ECoGLink.Devices.Nexus as Nexus
import time
import serial
import serial.tools.list_ports as lp

class Mode(Enum):
    CONTINUOUS = 1
    TOGGLE = 2
    TIMED = 3
    MODULAR = 4

class Output_Command(Enum):
    STOP = 0
    FLEX = 1
    EXTEND = 2

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
   
#####################################
"""
Created on Wed Jun 12 10:28:52 2019

@author: Charlie & Kevin
"""

class Neomano(Device):
    
    name = 'SLAB_USBtoUART'
    __flex_time = 1
    __extend_time = 1
    
    def __init__(self, port = None):  
        
        super().__init__(port if port != None else self.__detect_com_port__())

        if self.port == None:
            return
        
        self.bauderate = 115200
        self.mode = Mode.CONTINUOUS
        self.state = State(State.EXTENDED)
        self.modes = {
                Mode.CONTINUOUS: Continuous_Condition(),
                Mode.TOGGLE: Toggle_Condition(self.state),
                Mode.TIMED: Time_Based_Condition()
                }
        self.number_step = 0
        self.timeout_com = .5
        self.time_start = 0
        self.timeout = False
        self.time_remaining = 0
        self.time_condition_delay = 1
        self.time_step = 0
        self.toggle_state = False
        #self.total_step = 0
        
        # set and open serial coms with neomano
        self.ser = serial.Serial(self.port, baudrate=self.bauderate, timeout= self.timeout_com)
        if self.ser.isOpen == False:
            self.ser.open()
    
    def __detect_com_port__(self):
        port_infos = lp.comports(include_links = True)
        potential_neomano_port_info = list(filter(lambda x: x.pid == self.product_id and x.vid == self.vendor_id, port_infos))
        if len(potential_neomano_port_info) < 1:
            return

        neomano_port_info = potential_neomano_port_info[0]
        return neomano_port_info.device
    
    def is_connected():
        # is implementation of this necessary 
        pass
    
    def stop(self):
        pass
    
    def process(self, signal_input):
            
        condition = self.modes[self.mode]
        hardward_output, timeoutpro = condition.process(signal_input)
        
        if self.mode == Mode.TOGGLE:
            if hardward_output == Output_Command.FLEX:
                self.write_neomano(hardward_output)
                self.state.set(State.FLEXED)
            elif hardward_output == Output_Command.EXTEND:
                self.write_neomano(Output_Command.EXTEND)
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
                self.write_neomano(Output_Command.EXTEND)
                self.state.set(State.EXTENDED)
        if self.mode == Mode.TIMED:
            self.timeout = timeoutpro
            if self.timeout == True:
                if hardward_output == Output_Command.FLEX:
                    self.write_neomano(hardward_output)
                    time.sleep(self.__flex_time)
                    time.sleep(self.time_condition_delay)
                    self.write_neomano(Output_Command.EXTEND)
                    time.sleep(self.__extend_time)
                    self.state.set(State.EXTENDED)
            if hardward_output == Output_Command.EXTEND:
                self.write_neomano(Output_Command.EXTEND)
                self.state.set(State.EXTENDED)
        return
    
    def write_neomano(self, hardware_output):
        
        if hardware_output == Output_Command.FLEX:
            self.ser.write(b'1')
        elif hardware_output == Output_Command.EXTEND:
            self.ser.write(b'2')
        elif hardware_output == Output_Command.STOP:
            self.ser.write(b'0')
        return

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
        elif BMI_input == Nexus.ClassifiedInput.REST:
            Hardware_output = Output_Command.EXTEND
            timeout = False
        return Hardware_output, timeout
   

#Timed state
class Timed_Condition(Operation_mode):
    
    def __init__(self):
        #self.delay = delay
        return
 
    def process(self, BMI_input):
        if BMI_input == Nexus.ClassifiedInput.MOVE:
            Hardware_output = Output_Command.FLEX
            timeout = True
        elif BMI_input == Nexus.ClassifiedInput.REST:
            Hardware_output = Output_Command.EXTEND
            timeout = False
        return Hardware_output, timeout

# Time based stated
class Time_Based_Condition():
 
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
