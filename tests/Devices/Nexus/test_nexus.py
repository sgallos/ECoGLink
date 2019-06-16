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

    # Should fail to initialize
    with pytest.raises(TypeError):
        nexus = Nexus._Nexus()

    assert hasattr(Nexus._Nexus, 'is_initialized') == True
    assert hasattr(Nexus._Nexus, 'port_status') == True
    assert hasattr(Nexus._Nexus, 'get_state') == True
    assert hasattr(Nexus._Nexus, 'get_status') == True

    assert hasattr(Nexus._Nexus, 'set_configuration') == True

    assert hasattr(Nexus._Nexus, 'start_data_session') == True
    assert hasattr(Nexus._Nexus, 'stop_data_session') == True
    assert hasattr(Nexus._Nexus, 'get_data_packet') == True

def nexus_test(cls):
    
    # Validate nexus initializtion
    port = 'COM5'   # Device.Find device port 
    NVD = cls(port = port)

    # We should run a separate set of tests if the device is not connected
    if NVD.is_initialized == False:
        nexus_disconnected_tests(NVD)
    else:
        nexus_connected_tests(NVD)

    return
    
def nexus_connected_tests(NVD):

    assert NVD.is_initialized == True
    assert NVD.port_status == Nexus.Port_Status.CONNECTED
    # Need an assertion for the state
    # assert (NVD.get_state() != Nexus.State.LINK_FAILED_NO_RESPONSE) and (NVD.get_state() != Nexus.State.LINK_FAILED_DEVICE_ERROR)

    # Need a validation for set_configureation!
    assert NVD.set_configuration(10, 10) != -1

    # Need start_data_session validation!
    assert NVD.start_data_session(10, 10) != -1

    # Validate that the structure returned data packet is [80, 2, 80, 2]
    # data_packet = NVD.get_data_packet()
    # assert len(data_packet[0]) == 80
    # assert len(data_packet[1]) == 2
    # assert len(data_packet[2]) == 80
    # assert len(data_packet[3]) == 2
    
    # assert type(data_packet[0][0][0]) == int
    # assert type(data_packet[1][0][0]) == int
    # assert type(data_packet[2][0][0]) == int
    # assert type(data_packet[3][0][0]) == int

    return

def nexus_disconnected_tests(NVD):
    assert NVD.is_initialized == False
    # We need a way to auto search for the device!!!
    # assert NVD.port_status == Nexus.Port_Status.CONNECTED
    return
    
def test_nexus_virtual():
    nexus_test(NVDM.Virtual)
    
def test_nexus_real():
    nexus_test(NRDM.Real)
