
from abc import ABC, abstractmethod, abstractproperty

class Device(ABC):

    @abstractmethod
    def __init__(self):
        return

    @property
    @abstractmethod
    def modes(self):
        pass

    def process(self, signal_input):
        mode = self.mode
        mode.process(signal_input)

    def delay (self, time_input):
        mode = self.mode
        mode.delay(time_input)


    @property
    def mode():
        return self.__mode

    @mode.setter
    def mode(self, mode):
        self.__mode = mode
