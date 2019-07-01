# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 13:47:39 2019

@author: charl
"""

# Neomano hardware outputs 

from enum import Enum
from .Operation_mode import Operation_mode
from ECoGLink.Devices import Device
import ECoGLink.Devices.Nexus as Nexus
import ECoGLink.Devices.Neomano as Neomano

class State(Enum):
    STOPPED = 0
    FLEXED = 1
    EXTENDED = 2
    

class Neomano_hardware(Neomano, neomano_state_output, neomano_controller_output):
        def __init__(self):
            self.neomano_state = State.EXTENDED
            self.neomano_state_output = neomano_state_output
            self.neomano_controller_output = neomano_controller_output
            self.hardware_output(neomano_controller_output)
            self.set_state(neomano_state_output)
            pass
        
        def set_state(self, neomano_state_output):
            if self.neomano_state == State.EXTENDED:
                self.neomano_state = State.FLEXED
            elif self.neomano_state == State.FLEXED:
                self.neomano_state = State.EXTENDED
            pass
        
        def hardware_output(self, neomano_controller_output):
            pass
        