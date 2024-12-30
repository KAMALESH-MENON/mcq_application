from uuid import UUID
from sqlalchemy.orm import Session
from src.app.models.data_models import User
from src.app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        self.session = session
        
    def get(self, id: UUID):
        return self.session.query(User).filter(User.user_id == id).first()
    
    def get_all(self):
        return self.session.query(User).all()

    def add(self, user: User):
        self.session.add(user)
        self.session.commit()

    def update(self, id: UUID, **kwargs):
        user = self.get(id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.session.commit()

    def delete(self, id: UUID):
        user = self.get(id)
        self.session.delete(user)
        self.session.commit()