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

    def get(self, user_id: UUID) -> Union[UserOutput, None]:
        """
        Retrieve a single user by their UUID.

        Parameters: user_id : UUID

        Returns: Union[UserOutput, None]
            The user details as a UserOutput object if found, otherwise None.
        """
        user = self.session.query(User).filter(User.user_id == user_id).first()
        if user:
            return UserOutput(**user.__dict__)
        return None

    def get_all(self) -> List[Union[UserOutput, None]]:
        """
        Retrieve all users from the database.

        Returns: List[Union[UserOutput, None]]
            A list of UserOutput objects representing all users.
        """
        target_users = self.session.query(User).all()
        users = [UserOutput(**user.__dict__) for user in target_users]
        return users

    def add(self, user: UserRegisterInput):
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

    def update(self, user_id: UUID, **kwargs):
        """
        Update user details.

        Parameters:
            user_id : UUID
                The unique identifier of the user to update.
            **kwargs : dict
                Key-value pairs of the attributes to update.
        """
        existing_user = self.session.query(User).filter_by(user_id=user_id).first()
        if existing_user:
            for key, value in kwargs.items():
                setattr(existing_user, key, value)
        user = self.session.query(User).filter(User.user_id == user_id).first()
        if user:
            return UserOutput(**user.__dict__)

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
