# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 14:06:22 2019

@author: charl
"""

import ECoGLink.Devices.Nexus as Nexus

class Virtual(Nexus._Nexus):

    def __init__(self, port = None):
        super().__init__(port)
        self.is_initialized = True
        self.port_status = Nexus.Port_Status.CONNECTED
        return
    
    def __del__(self):
        return

    def get_data_packet(self):
        ch1 = [0]*80
        ch2 = [0]*2
        ch3 = [0]*80
        ch4 = [0]*2
        return [ch1, ch2, ch3, ch4]
    
    def get_state(self):
        return Nexus.State.INS_CONNECTED

    def get_status(self):
        return Nexus.Status(self.get_state(), 1, 2, 1.0, False, 0, 0)

    def set_configuration(self, main_session_timeout, host_session_timeout):
        return 108

    def start_data_session(self):
        return 108

    def stop_data_session(self):
        return 108

    def connect(self):
        # Connect to device
        if self.port_status != Nexus.Port_Status.CONNECTED:
            self.port_status = Nexus.Port_Status.CONNECTED
        elif self.port_status == Nexus.Port_Status.CONNECTED:
            self.port_status = Nexus.Port_Status.ALREADY_CONNECTED
        return self.port_status
    
    def disconnect(self):
        # Disconnect to device
        return 0
