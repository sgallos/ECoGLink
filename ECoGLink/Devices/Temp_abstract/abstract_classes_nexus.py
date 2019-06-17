# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:42:05 2019

@author: charl
"""

from abc import ABC, abstractmethod
import matlab.engine
 
class Nexus():
    #
    #
    # must haves
    # one matlab engine open total
    # one com port to receive signal
    # one opening of nexus
    # Jar file location - jssc
    #
    #
    #
    #
 
    def __init__(self, locN, locJ, port):
        self.locN = locN
        self.locJ = locJ
        self.port = port
        self.eng = matlab.engine.start_matlab()
        self.eng.javaaddpath(self.locN, nargout =0)
        self.eng.javaaddpath(self.locJ, nargout =0)
        self.eng.workspace['inst'] = self.eng.mdt.neuro.nexus.NexusInstrument(nargout = 1)
        self.eng.workspace['s2'] = self.eng.mdt.neuro.nexus.SerialConnection(self.port)
        self.eng.eval('inst.connect(s2)')
        self.eng.workspace['provider']= self.eng.mdt.neuro.nexus.ThreadedNexusInstrument(self.eng.eval('inst'))
        
#        @abstractmethod
#        def set_nexusjar_location(self, locN):
#        # set location for nexus jar
#        pass
#    
#        @abstractmethod
#        def set_jsscjar_location(self, locJ):
#        # set location for jssc jar
#        pass
#    
#        @abstractmethod
#        def setup_nexus(self, comport):
#        # set up nexus 
#        # return location for instance of engine
#        # return location for instance of mdt 
#        pass
    
        super().__init__()
    
   
    
    @abstractmethod
    def get_nexus_status(self):
        # return nexus status
        self.eng.eval('inst.getNexusStatus', nargout = 0)
        return
    
    @abstractmethod
    def set_nexus_config(self, timeouta, timeoutb):
        # set nexus time out configs
        self.timeouta = timeouta
        self.timeoutb = timeoutb
        self.eng.eval('inst.setNexusConfiguration(' + self.timeouta + ',' + self.timeoutb + ')')
        return
    
    @abstractmethod
    def start_data_session(self):
        # start data collection stream
        self.eng.eval('inst.startDataSession')
        return
    
    @abstractmethod
    def get_data_packet(self):
        # get packet
        # return data packet
        self.eng.eval('inst.getDataPacket',nargout = 0)
        pass
    
    @abstractmethod
    def stop_data_session(self):
        # end the data session
        self.eng.eval('inst.stopDataSession')
        pass
    
    @abstractmethod
    def get_data_packet_useable(self):
        # get packet
        # return data packet
        self.eng.grab_data_pkts(1, nargout = 1)
        pass