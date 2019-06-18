
import os
import sys
import pytest
sys.path.append(os.path.realpath("./"))

from ECoGLink.Devices.Operation_mode import Operation_mode

def test_Operation_mode():

    with pytest.raises(TypeError):
        operation_mode = Operation_mode()

    return
