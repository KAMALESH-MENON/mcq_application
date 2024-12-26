from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    def get_one(self, id):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def add(self, id):
        raise NotImplementedError

    @abstractmethod
    def update(self, id):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id):
        raise NotImplementedError
