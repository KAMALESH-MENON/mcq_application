import ast
from typing import List, Optional
from uuid import UUID

from pydantic import TypeAdapter
from sqlalchemy import distinct
from sqlalchemy.orm import Session

from app.models.data_models import MCQ
from app.repositories.base_repository import BaseRepository
from app.schemas.mcq_schemas import MCQCreate, MCQCreateOutput

adapter = TypeAdapter(MCQCreate)


class McqRepository(BaseRepository[MCQ]):
    def __init__(self, session: Session):
        self.session = session

    def get(self, mcq_id: UUID) -> Optional[MCQ]:
        """
        Retrieve an MCQ by its ID.
        """
        return self.session.query(MCQ).filter(MCQ.mcq_id == mcq_id).first()

    def get_all(
        self,
        type_: Optional[str] = None,
    ) -> List[MCQCreate]:
        """
        Retrieve MCQs with optional filtering by type and pagination.
        """
        query = self.session.query(MCQ)

        if type_:
            mcqs = query.filter(MCQ.type == type_)

        mcqs_dict = []
        for mcq in mcqs:
            mcq_dict = mcq.__dict__.copy()
            mcq_dict["options"] = ast.literal_eval(
                mcq_dict["options"]
            )  # converting string to dict
            mcqs_dict.append(mcq_dict)
        return [adapter.validate_python(mcq) for mcq in mcqs_dict]

    def add(self, mcq: MCQCreate) -> None:
        """
        Add a new MCQ to the database.
        """
        self.session.add(mcq)

    def update(self, mcq_id: UUID, **kwargs) -> None:
        """
        Update an MCQ with given fields.
        """
        mcq = self.get(mcq_id)
        if mcq:
            for key, value in kwargs.items():
                setattr(mcq, key, value)
            self.session.commit()

    def delete(self, mcq_id: UUID):
        """
        Delete an MCQ by its ID.
        """
        user = self.get(mcq_id)
        self.session.delete(user)
        self.session.commit()

    def get_mcq_types(self) -> list[str]:
        """
        Retrieve distinct types of MCQs.

        Returns:
            list[str]: List of distinct MCQ types.
        """
        types = self.session.query(distinct(MCQ.type)).all()
        return [type_[0] for type_ in types]
