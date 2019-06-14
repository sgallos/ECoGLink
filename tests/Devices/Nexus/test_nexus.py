# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 11:25:38 2019

@author: charl
"""

import os 
import sys
import pytest

import ECoGLink.Devices.Nexus as Nexus
import ECoGLink.Devices.Nexus.Virtual as NVDM
import ECoGLink.Devices.Nexus.Real as NRDM


# initialize it
    # check that NexusInstrument is first part of string
    # check port
    # check NexusStatus 
    # get Data packet  

# check NexusStatus
    
# get Data packet  

def test_nexus():
    with pytest.raises(TypeError):
        nexus = Nexus._Nexus()

def nexus_test(cls):
    
    # Validate nexus initializtion
    nexus_file_location = ''
    jssc_file_location = ''
    port = 'COM5'   # Device.Find device port 
    NVD = cls(port = port)
    assert NVD.isInitialized == True
    assert NVD.port_status == Nexus.Port_Status.SUCCESS
    assert (NVD.get_state() != Nexus.State.LINK_FAILED_NO_RESPONSE) and (NVD.get_state() != Nexus.State.LINK_FAILED_DEVICE_ERROR)

    # Validate that the structure returned data packet is [80, 2, 80, 2]
    data_packet = NVD.get_data_packet()
    assert len(data_packet[0]) == 80
    assert len(data_packet[1]) == 2
    assert len(data_packet[2]) == 80
    assert len(data_packet[3]) == 2
    
    assert type(data_packet[0][0][0]) == int
    assert type(data_packet[1][0][0]) == int
    assert type(data_packet[2][0][0]) == int
    assert type(data_packet[3][0][0]) == int
    
    
def test_nexus_virtual():
    nexus_test(NVDM.Virtual)
    
def test_nexus_real():
    nexus_test(NRDM.Real)