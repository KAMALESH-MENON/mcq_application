from abc import ABC

from sqlalchemy.orm import Session

from src.app.config.database import get_db
from src.app.repositories.history_repository import HistoryRepository
from src.app.repositories.mcq_repository import McqRepository
from src.app.repositories.submission_repository import SubmissionRepository
from src.app.repositories.user_repository import UserRepository


class BaseUnitOfWork(ABC):
    def __init__(self, session_factory=get_db):
        self.session_factory = session_factory
        self.session = None

    def __enter__(self):
        self.session = next(self.session_factory())
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        self.session.close()

    def commit(self):
        try:
            self.session.commit()
        except Exception as e:
            self.rollback()
            raise e

    def rollback(self):
        self.session.rollback()


class UserUnitOfWork(BaseUnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.user = UserRepository(self.session)
        return self


class SubmissionUnitOfWork(BaseUnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.submission = SubmissionRepository(self.session)
        return self


class McqUnitOfWork(BaseUnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.mcq = McqRepository(self.session)
        return self


class HistoryUnitOfWork(BaseUnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.history = HistoryRepository(self.session)
        return self
