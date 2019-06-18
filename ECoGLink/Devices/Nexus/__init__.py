
import os
import re

from enum import Enum
from abc import ABC, abstractmethod 

class ClassifiedInput(Enum):
    MOVE = 1
    REST = 0

class State(Enum):
    IDLE = 0
    LINKING_TO_INS = 1
    LINK_FAILED_NO_RESPONSE = 2
    LINK_FAILED_DEVICE_ERR = 3
    INS_CONNECTED = 4
    MAINTENANCE_ENABLED = 5
    ST_MDT_SESSION = 6

class Status():
    def __init__(self, state, majorVersion, minorVersion, batteryPercent,
            batteryDepleted, hostTimeoutMinutes, maintenanceTimeoutSeconds):
        self.state = state 
        self.majorVersion = majorVersion 
        self.minorVersion = minorVersion 
        self.batteryPercent = batteryPercent 
        self.batteryDepleted = batteryDepleted 
        self.hostTimeoutMinutes = hostTimeoutMinutes 
        self.maintenanceTimeoutSeconds = maintenanceTimeoutSeconds 
    
class Port_Status(Enum):
    CONNECTED = 0.0
    NOT_FOUND = 1.0
    BUSY = 2.0
    ALREADY_OPENED = 4.0
    ALREADY_CONNECTED = -1.0

class Response_Code(Enum):
    SUCCESS = 0
    PAYLOAD_CRC_ERROR = 1
    INVALID_FRAME_TYPE = 2
    MESSAGE_INCOMPLETE = 3
    INVALID_FRAME_ID = 4
    INVALID_PAYLOAD_LENGTH = 5
    HEADER_CRC_ERROR = 6
    PREV_CMD_BUSY = 7
    INS_POR_INDICATED = 8
    BATT_DEPLETED = 9
    INVALID_DATA = 10
    NO_RESPONSE = 11
    NOT_CONNECTED = 12
    NO_INS_CODE_AVAILABLE = -1

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:42:05 2019

@author: charl & Kevin
@note: State is a value of the State enumeration. Status is a dictionary of
values that includes state, battery life, etc. See Java files for more detail
"""

class _Nexus(ABC):

    is_initialized = False
    port_status = Port_Status.NOT_FOUND
    vendor_id = 1659
    product_id = 8963
    
    @abstractmethod
    def __init__(self, port):
        self.port = port
        self.jssc_jar_file = "./ECoGLink/Devices/Nexus/jssc.jar"
        self.nexus_jar_file = "./ECoGLink/Devices/Nexus/nexus.jar"
        pass
    
    @abstractmethod
    def get_state():
        pass
    
    @abstractmethod
    def get_status():
        pass

    @abstractmethod
    def set_configuration():
        pass

    @abstractmethod
    def start_data_session():
        pass
    
    @abstractmethod
    def get_data_packet():
        pass

    @abstractmethod
    def stop_data_session():
        pass
