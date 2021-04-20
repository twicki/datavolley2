from abc import ABC, abstractmethod


class AbstractAction(ABC):
    def __init__(self, time_stamp=None, auto_generated=False):
        super().__init__()
        self.time_stamp = time_stamp
        self.auto_generated = auto_generated

    @abstractmethod
    def __str__(self):
        pass
