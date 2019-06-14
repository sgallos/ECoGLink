
import os
import sys
import pytest

sys.path.append(os.path.realpath('./'))

import ECoGLink.Devices.Neomano as Neomano
# from ECoGLink.Devices.Neomano import *
from ECoGLink.Devices.Nexus import *

def test_toggle():

    # Should initialize to the state you set
    toggle_mode = Neomano.Toggle_Condition(state = Neomano.State.EXTENDED)
    assert toggle_mode.state == Neomano.State.EXTENDED

    # Should change after processing a move
    toggle_mode.process(NexusOutput.MOVE)
    assert toggle_mode.state != Neomano.State.EXTENDED

    # Shouln't change after processing a rest
    toggle_mode.process(NexusOutput.REST)
    assert toggle_mode.state != Neomano.State.EXTENDED

    # Moving again should set it back
    toggle_mode.process(NexusOutput.MOVE)
    assert toggle_mode.state == Neomano.State.EXTENDED

def test_continuous():

    continuous_mode = Neomano.Continuous_Condition()

    assert Neomano.OutputCommand.FLEX == continuous_mode.process(NexusOutput.MOVE)

    assert Neomano.OutputCommand.EXTEND == continuous_mode.process(NexusOutput.REST)
