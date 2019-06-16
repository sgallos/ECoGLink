# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 13:59:17 2019

@author: charl
"""

import time
import subprocess
from py4j.java_gateway import JavaGateway, java_import
import ECoGLink.Devices.Nexus as Nexus

class Real(Nexus._Nexus):

    jvm = None

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
        
        # self.__start_jvm__()
        # self.inst = self.gateway.jvm.NexusInstrument()
        # self.s2 = self.gateway.jvm.SerialConnection(self.port)
        # self.port_status = Nexus.Port_Status(self.inst.connect(self.s2))
        # self.provider = self.gateway.jvm.ThreadedNexusInstrument(self.inst)
        # self.get_status()
        # self.is_initialized = True if Nexus.Response_Code(self.inst.getLastInsResponseCode()) == Nexus.Response_Code.SUCCESS else False
        # self.set_configuration(30, 15)
        # self.start_data_session()
        
    def __del__(self):
        if(self.jvm != None):
            self.jvm.terminate()
        return

    def __start_jvm__(self):
        py4j = self.__find_py4j__()
        nexus_dir = "./ECoGLink/Devices/Nexus"
        jssc = f"{nexus_dir}/jssc.jar"
        nexus = f"{nexus_dir}/nexus.jar"
        jar_includes = f"{nexus_dir}:{py4j}:{jssc}:{nexus}"
        args = ['java', '-cp', jar_includes, 'py4j.examples.NexusEntryPoint']
        self.jvm = subprocess.Popen(args, stdout=subprocess.PIPE)
        timeout = 10
        start_time = time.time()
        for line in iter(self.jvm.stdout.readline, ''):
            if (line.strip() == b'Gateway Server Started'):
                print(line)
                break
            cur_time = time.time()
            duration = cur_time - start_time
            if (duration > timeout):
                print("Failed to start gateway! TIMEOUT")
        self.gateway = JavaGateway()
        java_import(self.gateway.jvm, 'mdt.neuro.nexus.*')
        return

    def get_status(self):
        # return nexus status
        return self.inst.getNexusStatus()
    

    def set_configuration(self, main_session_timeout, host_session_timeout):
        # set nexus time out configs
        self.main_session_timeout = main_session_timeout
        self.host_session_timeout = host_session_timeout
        return self.inst.setNexusConfiguration(main_session_timeout, host_session_timeout)
    
    def get_state(self):
        return

    def start_data_session(self):
        # start data collection stream
        self.inst.startDataSession()
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
