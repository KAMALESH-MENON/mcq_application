from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.app.models.user import User, UserRole
from src.app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):
    """Repository for User model to handle database operations."""

    def __init__(self, session: Session):
        self.session = session

    def get_one(self, id):
        pass

    def get_all(self):
        pass

    def add(self, username: str, password: str, role: UserRole = UserRole.USER) -> User:
        """Create a new user."""
        try:
            new_user = User(username=username, password=password, role=role)
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            return new_user
        except IntegrityError as error:
            self.session.rollback()
            raise ValueError("Username already exists") from error

    def update(self, id):
        pass

    def delete(self, id):
        pass

if __name__ == "__main__":
    from src.app.config.database import get_db
    session = next(get_db())
    test = UserRepository(next(get_db()))
    try:
        test.add(username="test_user4", password="test_password", role=UserRole.USER)
        print("User added.")
    except ValueError as e:
        print(f"Error: {e}")
