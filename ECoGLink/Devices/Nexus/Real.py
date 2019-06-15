# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 13:59:17 2019

@author: charl
"""

import ECoGLink.Devices.Nexus as Nexus
#import serial

class Real(Nexus._Nexus):
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
 
    def __init__(self, port):
        super().__init__(port)
        
        #self.reset()
        self.eng = matlab.engine.start_matlab()
        self.eng.javaaddpath(self.nexus_jar_file, nargout =0)
        self.eng.javaaddpath(self.jssc_jar_file, nargout =0)
        self.eng.workspace['inst'] = self.eng.mdt.neuro.nexus.NexusInstrument(nargout = 1)
        self.eng.workspace['s2'] = self.eng.mdt.neuro.nexus.SerialConnection(self.port)
        self.port_status = Nexus.Port_Status(self.eng.eval('inst.connect(s2)'))
        self.eng.workspace['provider']= self.eng.mdt.neuro.nexus.ThreadedNexusInstrument(self.eng.eval('inst'))
        self.eng.eval('inst.getNexusStatus', nargout = 0)
        self.isInitialized = True if self.eng.eval("inst.get('LastInsResponseString')") == 'SUCCESS' else False
        self.eng.eval('inst.setNexusConfiguration(30,15)')
        self.eng.eval('inst.startDataSession')
        
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
        
        ##
        ## reset com ports with ser.close() and ser.open()
        ##


    def get_nexus_status(self):
        # return nexus status
        return self.eng.eval('inst.getNexusStatus', nargout = 0)
    

    def set_nexus_config(self, timeouta, timeoutb):
        # set nexus time out configs
        self.timeouta = timeouta
        self.timeoutb = timeoutb
        self.eng.eval('inst.setNexusConfiguration(' + self.timeouta + ',' + self.timeoutb + ')')
        return
    
    def get_state(self):
        return
    def start_data_session(self):
        # start data collection stream
        self.eng.eval('inst.startDataSession')
        return
    

    def get_data_packet(self):
        # get packet
        # return data packet
        self.eng.workspace['data_packet_structure'] = self.eng.eval('inst.getDataPacket',nargout = 1)
        return self.eng.eval("data_packet_structure.get('data')")
    

    def stop_data_session(self):
        # end the data session
        self.eng.eval('inst.stopDataSession')
        pass

    def get_data_packet_useable(self):
        # get packet
        # return data packet
        self.eng.grab_data_pkts(1, nargout = 1)
        pass
    
#    def reset(self):
#        ser = serial.Serial(self.port, 9600, timeout = 1)
#        ser.close()
