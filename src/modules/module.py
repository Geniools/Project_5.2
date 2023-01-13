from abc import ABC, abstractmethod


# This class must be inherited by all modules
class Module(ABC):
    STATUS: str = None

    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def run(self) -> str:
        pass

    @property
    def results(self) -> str:
        return "This module has no results (or not implemented)"

    @property
    def name(self) -> str:
        return self._name
