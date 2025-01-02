from typing import List, Union
from uuid import UUID

from sqlalchemy.orm import Session

from src.app.models.data_models import User
from src.app.repositories.base_repository import BaseRepository
from src.app.schemas.mcq_schemas import UserInput, UserOutput


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        self.session = session

    def get(self, user_id: UUID) -> Union[UserOutput, None]:
        user = self.session.query(User).filter(User.user_id == user_id).first()
        return user

    def get_all(self) -> List[Union[UserOutput, None]]:
        users = self.session.query(User).all()
        return users

    def add(self, **kwargs: object) -> User:
        user = User(**kwargs)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user_id: UUID, **kwargs):
        user = self.get(user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.session.commit()

    def delete(self, user_id: UUID):
        user = self.get(user_id)
        self.session.delete(user)
        self.session.commit()
