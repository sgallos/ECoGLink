
import os
import sys
import pytest

sys.path.append(os.path.realpath('./'))

from ECoGLink.Devices.Neomono.Neomono import *
from ECoGLink.Devices.Nexus.Outputs import *

def test_toggle():

    # Should initialize to the state you set
    toggle_mode = Toggle_mode(Neomono_state.EXTENDED)
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
