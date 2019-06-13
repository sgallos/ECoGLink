# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:42:05 2019

@author: charl
"""

from abc import ABC, abstractmethod
 
class Nexus(ABC):
    #
    #
    # must haves
    # one matlab engine open total
    # one com port to receive signal
    # one opening of nexus
    # Jar file location - nexus
    # Jar file location - jssc
    #
    #
    #
    #
 
    def __init__(self, value):
        self.value = value
        super().__init__()
    
    @abstractmethod
    def set_nexusjar_location(self, locN):
        # set location for nexus jar
        pass
    
    @abstractmethod
    def set_jsscjar_location(self, locJ):
        # set location for jssc jar
        pass
    
    @abstractmethod
    def setup_nexus(self, comport):
        # set up nexus 
        # return location for instance of engine
        # return location for instance of mdt 
        pass
    
    @abstractmethod
    def get_nexus_status(self):
        # return nexus status
        pass
    
    @abstractmethod
    def set_nexus_config(self, timeouta, timeoutb):
        # set nexus time out configs
        pass
    
    @abstractmethod
    def start_data_session(self):
        # start data collection stream
        pass
    
    @abstractmethod
    def get_data_packet(self):
        # get packet
        # return data packet
        pass
    
    @abstractmethod
    def stop_data_session(self):
        # end the data session
        pass