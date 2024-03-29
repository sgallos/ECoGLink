# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 11:25:38 2019

@author: Charlie & Kevin
"""

import os 
import sys
import pytest

import ECoGLink.Devices.Nexus as Nexus
import ECoGLink.Devices.Nexus.Virtual as NVDM
import ECoGLink.Devices.Nexus.Real as NRDM

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

def test_nexus_virtual():
    nexus_test(NVDM.Virtual)
    
def test_nexus_real():
    nexus_test(NRDM.Real)

#############################################################################

def nexus_test(cls):
    
    NVD = cls()

    # We should run a separate set of tests if the device is not connected

    if NVD.port_status != Nexus.Port_Status.CONNECTED:
        nexus_disconnected_tests(NVD)
    else:
        nexus_connected_tests(NVD)

    return
    
def nexus_connected_tests(NVD):

    if not NVD.is_initialized:
        print("Device is connected but turned off")
        return
    
    assert NVD.is_initialized == True
    assert NVD.port_status == Nexus.Port_Status.CONNECTED

    assert NVD.get_status().State not in [Nexus.State.LINK_FAILED_DEVICE_ERR, Nexus.State.LINK_FAILED_NO_RESPONSE]
    assert NVD.get_status().BatteryPercent in [1.0, 0.75, 0.5, 0.25]
    assert isinstance(NVD.get_status().HostTimeoutMinutes, int)
    assert isinstance(NVD.get_status().MaintenanceTimeoutSeconds, int)
    assert NVD.get_status().BatteryDepleted == False
    assert isinstance(NVD.get_status().MajorVersion, int)
    assert isinstance(NVD.get_status().MinorVersion, int)
    
    # Need a validation for set_configureation!
    assert NVD.set_configuration(10, 10) != -1

    # Need start_data_session validation!
    assert NVD.start_data_session() != -1

    # Validate that the structure returned data packet is [80, 2, 80, 2]
    data_packet = NVD.get_data_packet()
    assert len(data_packet[0]) == 80
    assert len(data_packet[1]) == 2
    assert len(data_packet[2]) == 80
    assert len(data_packet[3]) == 2
    
    assert type(data_packet[0][0]) == int
    assert type(data_packet[1][0]) == int
    assert type(data_packet[2][0]) == int
    assert type(data_packet[3][0]) == int
    
    assert NVD.connect() == Nexus.Port_Status.ALREADY_CONNECTED
    assert NVD.disconnect() == 0
    assert NVD.connect() == Nexus.Port_Status.CONNECTED
    
    NVD.__del__()
    return

def nexus_disconnected_tests(NVD):
    assert NVD.is_initialized == False
    assert NVD.port_status == Nexus.Port_Status.NOT_FOUND
    return
    
    
