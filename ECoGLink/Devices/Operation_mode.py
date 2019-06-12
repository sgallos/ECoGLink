
from abc import ABC, abstractmethod

class Operation_mode(ABC):

    def __init__(self):
        return

    @abstractmethod
    def process(self, input_signal):
        pass
