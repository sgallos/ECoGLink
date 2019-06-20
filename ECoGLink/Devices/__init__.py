
from abc import ABC, abstractmethod, abstractproperty

class Device(ABC):

    vendor_id = 4292
    product_id = 60000   
    
    @abstractmethod
    def __init__(self, port):
        self.port = port
        return

    @abstractmethod
    def process(self, signal_input):
        mode = self.mode
        mode.process(signal_input)
