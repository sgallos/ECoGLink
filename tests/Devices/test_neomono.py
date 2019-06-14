
import os
import sys
import pytest

sys.path.append(os.path.realpath('./'))

from ECoGLink.Devices.Neomono import *
from ECoGLink.Devices.Nexus import *

def test_toggle():

    # Should initialize to the state you set
    toggle_mode = Toggle_Condition(state = Neomono_state.EXTENDED)
    assert toggle_mode.state == Neomono_state.EXTENDED

    # Should change after processing a move
    toggle_mode.process(NexusOutput.MOVE)
    assert toggle_mode.state != Neomono_state.EXTENDED

    # Shouln't change after processing a rest
    toggle_mode.process(NexusOutput.REST)
    assert toggle_mode.state != Neomono_state.EXTENDED

    # Moving again should set it back
    toggle_mode.process(NexusOutput.MOVE)
    assert toggle_mode.state == Neomono_state.EXTENDED

def test_continuous():

    continuous_mode = Continuous_Condition()

    assert Neomono_output.FLEX == continuous_mode.process(NexusOutput.MOVE)

    assert Neomono_output.EXTEND == continuous_mode.process(NexusOutput.REST)
