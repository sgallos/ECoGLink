
from abc import ABC, abstractmethod, abstractproperty

class Device(ABC):

    @abstractmethod
    def __init__(self):
        return

    @abstractmethod
    def process(self, signal_input):
        mode = self.mode
        mode.process(signal_input)
