from typing import List, Union
from uuid import UUID

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.data_models import User
from app.repositories.base_repository import BaseRepository
from app.schemas.mcq_schemas import UserOutput, UserRegisterInput

pwd_context = CryptContext(schemes=["bcrypt"])


class UserRepository(BaseRepository[User]):
    """A repository class for managing `User` objects in the database."""

    def __init__(self, session: Session):
        """
        Initialize the UserRepository with a database session.

        Parameters: session : Session(SQLAlchemy session object)
        """
        self.session = session

    def get(self, user_id: UUID) -> User:
        """
        Retrieve a single user by their UUID.

        Parameters: user_id : UUID

        Returns: User
            The User object

        """
        user = self.session.query(User).filter(User.user_id == user_id).first()
        return user

    def get_all(self) -> List[User]:
        """
        Retrieve all users from the database.

        Returns: List[User]
            A list of User objects.
        """
        users = self.session.query(User).all()
        return users

    def add(self, user: UserRegisterInput) -> None:
        """
        Add a new user to the database.

        Parameters: user : UserRegisterInput
            The user details for registration.

        Raises: ValueError
            If the username already exists in the database.
        """
        if self.check_username_exists(user.username):
            raise ValueError("Username already exists.")
        if self.check_email_exists(user.email):
            raise ValueError("Email already exists.")
        self.session.add(user)

    def update(self, user_id: UUID, **kwargs) -> None:
        """
        Update user details.

        Parameters:
            user_id : UUID
                The unique identifier of the user to update.
            **kwargs : dict
                Key-value pairs of the attributes to update.
        """
        existing_user = self.get(user_id=user_id)
        if existing_user:
            for key, value in kwargs.items():
                setattr(existing_user, key, value)

    def delete(self, user_id: UUID) -> bool:
        """
        Delete a user from the database.

        Parameters: user_id : UUID
            The unique identifier of the user to delete.
        """
        user = self.session.query(User).filter(User.user_id == user_id).first()
        if user is None:
            return False
        self.session.delete(user)
        return True

    def check_username_exists(self, username: str) -> Union[User, None]:
        """
        Parameters: username : str
            The username to check.

        Returns: Union[User, None]
            The User object if the user exists, otherwise None.
        """
        return self.session.query(User).filter_by(username=username).first()

    def check_email_exists(self, email: str) -> bool:
        """
        Parameters: email : str
            The email to check.

        Returns: bool
            True if the email exists, otherwise False.
        """
        return self.session.query(User).filter_by(email=email).first() is not None
