from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.data_models import UserSubmission
from app.repositories.base_repository import BaseRepository
from app.schemas.mcq_schemas import SubmissionInput


class SubmissionRepository(BaseRepository[UserSubmission]):
    """A repository class for managing `UserSubmission` objects in the database."""

    def __init__(self, session: Session):
        """
        Initialize the SubmissionRepository with a database session.

        Parameters: session : Session(SQLAlchemy session object)
        """
        self.session = session

    def get(self, submission_id) -> UserSubmission:
        """
        Retrieve a single user by their UUID.

        Parameters: user_id : UUID

        Returns: UserSubmission
            The UserSubmission object

        """
        submission = (
            self.session.query(UserSubmission)
            .filter(UserSubmission.submission_id == submission_id)
            .all()
        )
        return submission

    def get_all(self, user_id) -> List[UserSubmission]:
        """
        Retrieve all submission from the database.

        Returns: List[UserSubmission]
            A list of UserSubmission objects.
        """
        query = self.session.query(UserSubmission)

        if user_id:
            query = query.filter(UserSubmission.user_id == user_id)

        return query.all()

    def add(self, submission: SubmissionInput):
        """
        Add a new submission to the database.

        Parameters: user : SubmissionInput
            The submission details for SubmissionInput.
        """
        self.session.add(submission)

    def update(self, submission_id: UUID, **kwargs):
        """
        Update submission details.

        Parameters:
            user_id : UUID
                The unique identifier of the submission to update.
            **kwargs : dict
                Key-value pairs of the attributes to update.
        """
        user = self.get(submission_id)
        for key, value in kwargs.items():
            setattr(user, key, value)

    def delete(self, submission_id: UUID):
        """
        Delete a submission from the database.

        Parameters: submission_id : UUID
            The unique identifier of the submission to delete.
        """
        submission = self.get(submission_id)
        self.session.delete(submission)
