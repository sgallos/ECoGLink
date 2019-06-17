
import os
import sys
import time
import pytest

sys.path.append(os.path.realpath('./'))

import ECoGLink.Devices.Neomano as Neomano
import ECoGLink.Devices.Nexus as Nexus

def test_toggle():

    # Should initialize to the state you set
    toggle_mode = Neomano.Toggle_Condition(state = Neomano.State.EXTENDED)
    assert toggle_mode.state == Neomano.State.EXTENDED

    # Should change after processing a move
    toggle_mode.process(Nexus.ClassifiedInput.MOVE)
    assert toggle_mode.state != Neomano.State.EXTENDED

    # Shouln't change after processing a rest
    toggle_mode.process(Nexus.ClassifiedInput.REST)
    assert toggle_mode.state != Neomano.State.EXTENDED

    # Moving again should set it back
    toggle_mode.process(Nexus.ClassifiedInput.MOVE)
    assert toggle_mode.state == Neomano.State.EXTENDED

def test_continuous():

    continuous_mode = Neomano.Continuous_Condition()

    assert Neomano.Output_Command.FLEX == continuous_mode.process(Nexus.ClassifiedInput.MOVE)

    assert Neomano.Output_Command.EXTEND == continuous_mode.process(Nexus.ClassifiedInput.REST)

def _test_timed():

    timed_mode = Neomano.Timed_Condition(5)

    assert Neomano.Output_Command.FLEX == continuous_mode.process(Nexus.ClassifiedInput.MOVE)
    assert Neomano.Output_Command.FLEX == continuous_mode.process(Nexus.ClassifiedInput.MOVE)
    time.sleep(timed_mode.delay)
    assert Neomano.Output_Command.EXTEND == continuous_mode.process(Nexus.ClassifiedInput.MOVE)

    return

def _test_modular():

    modular_mode = Neomano.Modular_Condition(steps=5, delay=2)

    assert Neomano.Output_Command.FLEX == modular_mode.process(Nexus.ClassifiedInput.MOVE)

    while (modular_mode.is_moving):
        # No matter the input, output should be flex until step is completed
        assert Neomano.Output_Command.FLEX == modular_mode.process(Nexus.ClassifiedInput.MOVE)
        assert Neomano.Output_Command.FLEX == modular_mode.process(Nexus.ClassifiedInput.REST)

    # After elapsed time, there should be a minimum delay before the next MOVE signal will work
    assert modular_mode.step == 1
    while (modular_mode.is_delaying):
        assert Neomano.Output_Command.STOP == modular_mode.process(Nexus.ClassifiedInput.MOVE)
        assert Neomano.Output_Command.STOP == modular_mode.process(Nexus.ClassifiedInput.REST)

    # Let's skip to the final step
    while (modular_mode.step != modular_mode.steps-1):
        prev_step = modular_mode.step
        modular_mode.process(Nexus.ClassifiedInput.MOVE)
        while (modular_mode.is_moving or modular_mode.is_delaying):
            pass
        
        assert modular_mode.step == prev_step + 1

    modular_mode.process(Nexus.ClassifiedInput.MOVE)
    while (modular_mode.is_moving):
        assert Neomano.Output_Command.EXTEND == modular_mode.process(Nexus.ClassifiedInput.MOVE)
        assert Neomano.Output_Command.EXTEND == modular_mode.process(Nexus.ClassifiedInput.REST)

    return

# Because we receive no input from the neomano, we'll stick with one interface
# rather than building a real and virtual device
def _test_neomano_setup():

    # Neomano must inherit from the Device class
    assert Neomano.Neomano.__base__.__name__ == 'Device'

    # Validate that the Neomano class has the following properties and methods
    assert hasattr(Neomano.Neomano, 'set_flexion')
    assert hasattr(Neomano.Neomano, 'flex_percent')
    assert hasattr(Neomano.Neomano, 'stop')
    assert hasattr(Neomano.Neomano, '_prev_flex_percent_request')
    assert hasattr(Neomano.Neomano, '_prev_flex_percent_request_time')
    assert hasattr(Neomano.Neomano, '_flex_time')
    assert hasattr(Neomano.Neomano, '_extend_time')
    assert hasattr(Neomano.Neomano, 'is_moving')
    assert hasattr(Neomano.Neomano, 'state')
    assert hasattr(Neomano.Neomano, 'process')
    assert hasattr(Neomano.Neomano, 'mode')
    assert hasattr(Neomano.Neomano, 'is_connected')
    assert hasattr(Neomano.Neomano, 'name')

    device = Neomano.Neomano()

    assert device.name == 'insert device name!' # TODO: Get device name!
    assert device.mode == Neomano.Mode.CONTINUOUS
    assert device.state == Neomano.State.EXTENDED
    assert device._extend_time == 3 # determine extend time
    assert device._flex_time == 3 # determine flex time

    assert device.is_moving == False
    device.set_flexion(0.25)
    device.set_flexion(0.75)
    assert device.is_moving == True
    assert device.flex_percent < device._prev_flex_percent_request
    time.sleep(device._flex_time * abs(device._prev_flex_percent_request - device.flex_percent) - (time.time() - device._prev_flex_percent_request_time))
    assert device.is_moving == False
    assert device.state == Neomano.State.FLEXED

    device.set_flexion(1)
    assert device.is_moving == True
    device.stop()
    assert device.is_moving == False
    
    device.set_flexion(0)
    time.sleep(device._extend_time * abs(device._prev_flex_percent_request - device.flex_percent) - (time.time() - device._prev_flex_percent_request_time))

    device.process(Nexus.ClassifiedInput.MOVE)
    assert device.state == Neomano.State.FLEXED

    device.process(Nexus.ClassifiedInput.REST)
    assert device.state == Neomano.State.EXTENDED

    # Output command to Flex, Extend, Stop

    # Change the current mode
    # Check the current output position
    # Check the current mode
    # Check if the device is connected
    # Set the port for the device

    return

