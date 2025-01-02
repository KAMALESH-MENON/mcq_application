from uuid import UUID

from sqlalchemy.orm import Session

from src.app.models.data_models import UserHistory
from src.app.repositories.base_repository import BaseRepository


class HistoryRepository(BaseRepository[UserHistory]):
    def __init__(self, session: Session):
        self.session = session

    def get(self, id):
        return self.session.query(UserHistory).filter(UserHistory.user_id == id).all()

    def get_all(self):
        return self.session.query(UserHistory).all()

    def add(self, user: UserHistory):
        self.session.add(user)
        self.session.commit()

    def update(self, id: UUID, **kwargs):
        user = self.get(id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.session.commit()

    def delete(self, user_id: str):
        user = self.get(user_id)
        self.session.delete(user)
        self.session.commit()
