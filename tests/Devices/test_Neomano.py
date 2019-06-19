
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

    # Should change after processing a move and waiting appropriate time to move it to the fully closed state
    output, timeout = toggle_mode.process(Nexus.ClassifiedInput.MOVE)
    assert timeout == True
    assert output == Neomano.Output_Command.FLEX
    toggle_mode.state = Neomano.State.FLEXED
    assert toggle_mode.state != Neomano.State.EXTENDED

    # Shouln't change after processing a rest
    output, timeout = toggle_mode.process(Nexus.ClassifiedInput.REST)
    assert timeout == False
    assert output == Neomano.Output_Command.FLEX
    assert toggle_mode.state != Neomano.State.EXTENDED

    # Moving again should set it back and wait appropriate time then set state to be extended state
    toggle_mode.process(Nexus.ClassifiedInput.MOVE)
    assert timeout == True
    assert output == Neomano.Output_Command.EXTENDED
    toggle_mode.state = Neomano.State.EXTEND
    assert toggle_mode.state == Neomano.State.EXTENDED

def test_continuous():

    continuous_mode = Neomano.Continuous_Condition()
    
    #
    # If Move signal send out flex
    # If rest signal send out a stop signal
    # send out reset signal?
    # timeout should always return 0 because it should only close while patient thinking of moving
    #
    
    output, timeout = continuous_mode.process(Nexus.ClassifiedInput.MOVE)
    assert output == Neomano.Output_Command.FLEX 
    assert timeout == False
    
    output, timeout = continuous_mode.process(Nexus.ClassifiedInput.REST)
    assert output == Neomano.Output_Command.EXTEND
    assert timeout == False

def _test_timed():

    timed_mode = Neomano.Timed_Condition()
    
    #
    # If move signal, set flex signal till cap
    # Wait for time to run
    # timestep is a user defined variable based on the input from the gui
    # timing is handled in the main portion of the class not within the process
    # 
    #
    
    # check move command given
    output, timeout = timed_mode.process(Nexus.ClassifiedInput.MOVE)
    assert output == Neomano.Output_Command.FLEX
    assert timeout == True
  
    # check rest
    output, timeout = timed_mode.process(Nexus.ClassifiedInput.REST)
    assert output == Neomano.Output_Command.EXTEND
    assert timeout == False

    return

def _test_modular():

    modular_mode = Neomano.Modular_Condition()
    
    #
    # Desired outcome is to incrementally step the patients hand closed
    # Timing of steps to be handled by the main neomano class
    #

    # check move given results in flex command and true
    output, timeout = modular_mode.process(Nexus.ClassifiedInput.MOVE)
    assert output == Neomano.Output_Command.FLEX 
    assert timeout == True
    
    # check rest given results in extend and false
    output, timeout = modular_mode.process(Nexus.ClassifiedInput.REST)
    assert output == Neomano.Output_Command.EXTEND 
    assert timeout == False
    #
    # This code should be run in the main neomano portion since it relates to the specific timing of the patients movement
    #
#    while (modular_mode.is_moving):
#        # No matter the input, output should be flex until step is completed
#        assert Neomano.Output_Command.FLEX == modular_mode.process(Nexus.ClassifiedInput.MOVE)
#        assert Neomano.Output_Command.FLEX == modular_mode.process(Nexus.ClassifiedInput.REST)
#
#    # After elapsed time, there should be a minimum delay before the next MOVE signal will work
#    assert modular_mode.step == 1
#    while (modular_mode.is_delaying):
#        assert Neomano.Output_Command.STOP == modular_mode.process(Nexus.ClassifiedInput.MOVE)
#        assert Neomano.Output_Command.STOP == modular_mode.process(Nexus.ClassifiedInput.REST)
#
#    # Let's skip to the final step
#    while (modular_mode.step != modular_mode.steps-1):
#        prev_step = modular_mode.step
#        modular_mode.process(Nexus.ClassifiedInput.MOVE)
#        while (modular_mode.is_moving or modular_mode.is_delaying):
#            pass
#        
#        assert modular_mode.step == prev_step + 1
#
#    modular_mode.process(Nexus.ClassifiedInput.MOVE)
#    while (modular_mode.is_moving):
#        assert Neomano.Output_Command.EXTEND == modular_mode.process(Nexus.ClassifiedInput.MOVE)
#        assert Neomano.Output_Command.EXTEND == modular_mode.process(Nexus.ClassifiedInput.REST)

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
    assert hasattr(Neomano.Neomano, 'toggle_state')
    assert hasattr(Neomano.Neomano, 'time_start')
    assert hasattr(Neomano.Neomano, 'time_left')
    assert hasattr(Neomano.Neomano, 'time_step')
    assert hasattr(Neomano.Neomano, 'number_step')
    assert hasattr(Neomano.Neomano, 'total_step')
    assert hasattr(Neomano.Neomano, 'mode')

    device = Neomano.Neomano()

    assert device.name == 'insert device name!' # TODO: Get device name!
    #assert device.mode == Neomano.Mode.CONTINUOUS 
    #
    # why did you want to assert that it starts in continuous mode?
    #
    assert device.state == Neomano.State.EXTENDED
    assert device.__extend_time__ == 3 # determine extend time
    assert device.__flex_time__ == 3 # determine flex time

    # Check full run of toggles
    device.mode = Neomano.Mode.TOGGLE
    device.process(Nexus.ClassifiedInput.MOVE)
    assert device.state == Neomano.State.FLEXED
    assert device.toggle_state == True
    device.process(Nexus.ClassifiedInput.REST)
    assert device.state == Neomano.State.FLEXED
    assert device.toggle_state == True
    device.process(Nexus.ClassifiedInput.MOVE)
    assert device.state == Neomano.State.EXTENDED
    assert device.toggle_state == False
    device.process(Nexus.ClassifiedInput.MOVE)
    assert device.state == Neomano.State.FLEXED
    assert device.toggle_state == True
    
    # Check full run of continous
    device.mode = Neomano.Mode.CONTINUOUS
    device.process(Nexus.ClassifiedInput.MOVE)
    assert device.state == Neomano.State.FLEXED
    device.process(Nexus.ClassifiedInput.REST)
    assert device.state == Neomano.State.EXTENDED
    
    # Check full run of timed
    device.mode = Neomano.Mode.TIMED
    device.time_start = 1
    device.time_left = -1
    device.process(Nexus.ClassifiedInput.MOVE)
    assert device.state == Neomano.State.FLEXED
    assert device.time_left < 1
    # we could also just send back system waiting if we get that we started and time is less than start and greater than 0
    device.process(Nexus.ClassifiedInput.MOVE)
    assert device.state == Neomano.State.FLEXED
    # set time to 0 and make sure that move extends on 0
    device.time_left = 0
    device.process(Nexus.ClassifiedInput.MOVE)
    assert device.state == Neomano.State.EXTENDED
    device.process(Nexus.ClassifiedInput.REST)
    assert device.state == Neomano.State.EXTENDED
    
    device.time_left = -1
    device.process(Nexus.ClassifiedInput.REST)
    assert device.state == Neomano.State.EXTENDED
    device.process(Nexus.ClassifiedInput.MOVE)
    assert device.state == Neomano.State.FLEXED
    
    
    
    # modular_mode = Neomano.Modular_Condition()



#    assert device.is_moving == False
#    device.set_flexion(0.25)
#    device.set_flexion(0.75)
#    assert device.is_moving == True
#    assert device.flex_percent < device._prev_flex_percent_request
#    time.sleep(device._flex_time * abs(device._prev_flex_percent_request - device.flex_percent) - (time.time() - device._prev_flex_percent_request_time))
#    assert device.is_moving == False
#    assert device.state == Neomano.State.FLEXED
#
#    device.set_flexion(1)
#    assert device.is_moving == True
#    device.stop()
#    assert device.is_moving == False
#    
#    device.set_flexion(0)
#    time.sleep(device._extend_time * abs(device._prev_flex_percent_request - device.flex_percent) - (time.time() - device._prev_flex_percent_request_time))
#
#    device.process(Nexus.ClassifiedInput.MOVE)
#    assert device.state == Neomano.State.FLEXED
#
#    device.process(Nexus.ClassifiedInput.REST)
#    assert device.state == Neomano.State.EXTENDED

    # Output command to Flex, Extend, Stop

    # Change the current mode
    # Check the current output position
    # Check the current mode
    # Check if the device is connected
    # Set the port for the device

    return

