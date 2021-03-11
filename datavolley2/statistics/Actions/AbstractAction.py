from abc import ABC, abstractmethod


class AbstractAction(ABC):
    def __init__(self, time_stamp=None):
        super().__init__()
        self.time_stamp = time_stamp

    @abstractmethod
    def __str__(self):
        pass