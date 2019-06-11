import os
import sys
sys.path.append(os.path.realpath("./"))
print(sys.path)

from ECoGLink.enums import *

def test_enums():
    assert AppState.CONTINUOUS == AppState.CONTINUOUS
    assert AppState.TOGGLE == AppState.TOGGLE
    assert AppState.TIMED == AppState.TIMED
