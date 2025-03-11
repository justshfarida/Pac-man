from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class Entity(Protocol):
    @abstractmethod
    def move(self) -> None:
        ...

    @abstractmethod
    def draw(self, screen) -> None:
        ...