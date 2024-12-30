from abc import ABC, abstractmethod
from uuid import UUID
class BaseRepository[T](ABC):

    @abstractmethod
    def get(self, id: UUID) -> T:
        return NotImplemented

    @abstractmethod
    def get_all(self) -> list[T]:
        return NotImplemented

    @abstractmethod
    def add(self, **kwargs: object) -> None:
        return NotImplemented

    @abstractmethod
    def update(self, id: UUID, **kwargs: object) -> None:
        return NotImplemented

    @abstractmethod
    def delete(self, id: UUID) -> None:
        return NotImplemented
