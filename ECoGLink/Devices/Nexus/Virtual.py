# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 14:06:22 2019

@author: charl
"""

import ECoGLink.Devices.Nexus as Nexus

class Virtual(Nexus._Nexus):
    
    def __init__(self, port):
        self.isInitialized = True
        self.port_status = Nexus.Port_Status.SUCCESS
        return
    
    def get_data_packet(self):
        ch1 = [[0]]*80
        ch2 = [[0]]*2
        ch3 = [[0]]*80
        ch4 = [[0]]*2
        return [ch1, ch2, ch3, ch4]
    
    def get_state(self):
        return
    