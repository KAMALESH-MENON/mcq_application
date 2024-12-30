from uuid import UUID
from sqlalchemy.orm import Session
from src.app.models.data_models import MCQ
from src.app.repositories.base_repository import BaseRepository

class MCQRepository(BaseRepository[MCQ]):
    def __init__(self, session: Session):
        self.session = session

    def get(self, id):
        return self.session.query(MCQ).filter(MCQ.mcq_id == id).first()
    
    def get_all(self):
        return self.session.query(MCQ).all()

    def add(self, user: MCQ):
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