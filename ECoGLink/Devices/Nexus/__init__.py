
from enum import Enum
from abc import ABC, abstractmethod 

class ClassifiedInput(Enum):
    MOVE = 1
    REST = 0

class State(Enum):
    IDLE = 'IDLE'
    LINKING_TO_INS = 'LINKING_TO_INS'
    LINK_FAILED_NO_RESPONSE = 'LINK_FAILED_NO_RESPONSE'
    LINK_FAILED_DEVICE_ERROR = 'LINK_FAILED_DEVICE_ERROR'
    SUPERVISORY_SESSION = 'SUPERVISORY_SESSION'
    MAINTENANCE_SESSION = 'MAINTENANCE_SESSION'
    
class Port_Status(Enum):
    SUCCESS = 0.0
    DISCONNECT = 1.0
    BUSY = 2.0
    ALREADY_CONNECTED = -1.0


# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:42:05 2019

@author: charl
"""

class _Nexus(ABC):
    
    @abstractmethod
    def __init__(self, port):
        self.port = port
        self.jssc_jar_file = "./ECoGLink/Devices/Nexus/jssc.jar"
        self.nexus_jar_file = "./ECoGLink/Devices/Nexus/nexus.jar"
        pass
    
    @abstractmethod
    def get_data_packet():
        pass
    
    @abstractmethod
    def get_state():
        pass
    
    