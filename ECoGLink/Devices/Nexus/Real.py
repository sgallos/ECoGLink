"""
Created on Fri Jun 14 13:59:17 2019

@author: Charlie & Kevin
"""

import sys
import time
import subprocess
import serial
import serial.tools.list_ports as lp

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
 
    def __init__(self, port = None):
        super().__init__(port if port != None else self.__detect_com_port__())
        
        self.__start_jvm__()
        self.inst = self.gateway.jvm.NexusInstrument()
        self.serialport = self.gateway.jvm.SerialConnection(self.port)
        self.port_status = self.connect()
        self.provider = self.gateway.jvm.ThreadedNexusInstrument(self.inst)
        self.get_status()
        self.is_initialized = True if self.get_response_code() == Nexus.Response_Code.SUCCESS else False
        self.set_configuration(30, 15)
        self.start_data_session()
        
    def __del__(self):
        print ('Shutting Down Java')
        if(self.jvm != None):
            self.jvm.terminate()
        return

    def get_response_code(self):
        return Nexus.Response_Code(self.inst.getLastInsResponseCode())

    def __detect_com_port__(self):
        port_infos = lp.comports(include_links = True)
        potential_nexus_port_info = list(filter(lambda x: x.pid == self.product_id and x.vid == self.vendor_id, port_infos))
        if len(potential_nexus_port_info) < 1:
            raise Exception ('THE COM_PORT WAS NOT FOUND')
            return

        nexus_port_info = potential_nexus_port_info[0]
        return nexus_port_info.device

    def __start_jvm__(self):
        nexus_dir = "./ECoGLink/Devices/Nexus"
        py4j = f"{nexus_dir}/py4j0.10.8.1.jar" # self.__find_py4j__()
        jssc = f"{nexus_dir}/jssc.jar"
        nexus = f"{nexus_dir}/nexus.jar"
        separator = ";"
        if sys.platform != "win32":
            separator = ":"
        jar_includes = f"{nexus_dir}{separator}{py4j}{separator}{jssc}{separator}{nexus}"
        print(jar_includes)
        args = ['java', '-cp', jar_includes, 'py4j.examples.NexusEntryPoint']

        # if(self.py4j_loc == None):
            # raise Exception('py4j.jar not found - cannot continue interaction with device')

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
                raise Exception("Failed to start gateway")

        # Start Gateaway
        self.gateway = JavaGateway()
        java_import(self.gateway.jvm, 'mdt.neuro.nexus.*')
        return

    def get_status(self):
        # return nexus status
        if self.port_status != Nexus.Port_Status.CONNECTED and self.port_status != Nexus.Port_Status.ALREADY_CONNECTED:
            return
        
        alpha = self.inst.getNexusStatus()
        status = Nexus.Status(
            alpha.getState().ordinal(),
            alpha.getMajorVersion(),
            alpha.getMinorVersion(),
            alpha.getBatteryPercent(),
            alpha.isBatteryDepleted(),
            alpha.getHostTimeoutMinutes(),
            alpha.getMaintenanceTimeoutSeconds())
        return status
    

    def set_configuration(self, main_session_timeout, host_session_timeout):
        # set nexus time out configs
        self.main_session_timeout = main_session_timeout
        self.host_session_timeout = host_session_timeout
        return self.inst.setNexusConfiguration(main_session_timeout, host_session_timeout)
    
    def get_state(self):
        return self.get_status().State

    def start_data_session(self):
        # start data collection stream
        self.inst.startDataSession()
        return
    

    def get_data_packet(self):
        # get packet
        # return data packet
        data_packet_structure = self.inst.getDataPacket()
        java_data = data_packet_structure.getData()
        
        data = []
        for java_channel_data in java_data:
            channel_data = []
            for jdata in java_channel_data:
                channel_data.append(jdata)
            
            data.append(channel_data)
        
        return data
    

    def stop_data_session(self):
        # end the data session
        self.eng.eval('inst.stopDataSession')
        pass

    def get_data_packet_useable(self):
        # get packet
        # return data packet
        self.start_data_session()
        return self.get_data_packet()
   
    def connect(self):
        # Connect to device
        self.port_status = Nexus.Port_Status(self.inst.connect(self.serialport))
        return self.port_status
    
    def disconnect(self):
        # Disconnect to device
        result = self.inst.disconnect()
        if(result == 0):
            self.port_status = Nexus.Port_Status.NOT_FOUND
        if(result == -1):
            # TODO add what happens here if fails to disconnect
            pass
        return result
          
#    def reset(self):
#        ser = serial.Serial(self.port, 9600, timeout = 1)
#        ser.close()
