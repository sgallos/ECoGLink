
import os
import sys
import pytest
sys.path.append(os.path.realpath("./"))

from ECoGLink.Devices import *

def test_Device():

    with pytest.raises(TypeError):
        new_device = Device()

    return
