from src.app.repositories.user_repository import UserRepository
from src.app.models.data_models import User, UserRole
from uuid import uuid4
from sqlalchemy.orm import Session
from src.app.config.database import Base, engine

def init_db():
    Base.metadata.create_all(bind=engine)
    
def test_add():
    init_db()
    session = Session()
    repo = UserRepository(session)
    new_user = User(
        user_id=uuid4(),
        username="kamalesh",
        password="test",
        role=UserRole.ADMIN
        )
    repo.add(new_user)

if __name__ == "__main__":
    test_add()
# from src.app.repositories.user_repository import UserRepository
# from src.app.models.data_models import User, UserRole
# from uuid import uuid4
# from unittest.mock import MagicMock
# import pytest

# def test_add():
#     # Mock the database session
#     mock_session = MagicMock()

#     # Create an instance of UserRepository with the mock session
#     repo = UserRepository(mock_session)

#     # Create a new user
#     new_user = User(
#         user_id=uuid4(),
#         username="kamalesh",
#         password="test",
#         role=UserRole.ADMIN
#     )

#     # Call the add method
#     repo.add(new_user)

#     # Check if add() was called on the session with the new user
#     mock_session.add.assert_called_once_with(new_user)

#     # Check if commit() was called on the session
#     mock_session.commit.assert_called_once()

# if __name__ == "__main__":
#     pytest.main()
