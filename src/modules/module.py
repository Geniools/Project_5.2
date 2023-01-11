from abc import ABC, abstractmethod


class Module(ABC):
    STATUS: str = None

    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def run(self) -> str:
        pass

    @property
    def name(self) -> str:
        return self._name
