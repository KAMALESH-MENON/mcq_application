from enum import Enum as PyEnum
from uuid import uuid4

from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Boolean,
    Column,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.app.config.database import Base


class UserRole(str, PyEnum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default="user")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    created_mcqs = relationship(
        "MCQ", back_populates="creator", cascade="all, delete-orphan"
    )
    submissions = relationship(
        "UserSubmission", back_populates="user", cascade="all, delete-orphan"
    )
    history = relationship(
        "UserHistory", back_populates="user", cascade="all, delete-orphan"
    )


class UserSubmission(Base):
    __tablename__ = "user_submissions"

    submission_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.user_id"), nullable=False)
    mcq_id = Column(UUID, ForeignKey("mcqs.mcq_id"), nullable=False)
    user_answer = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)
    attempted_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="submissions")
    mcq = relationship("MCQ", back_populates="submissions")


class UserHistory(Base):
    __tablename__ = "user_history"

    history_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.user_id"), nullable=False)
    total_score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    total_attempts = Column(Integer, nullable=False)
    attempted_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="history")


class MCQ(Base):
    __tablename__ = "mcqs"

    mcq_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String, nullable=False)
    question = Column(String, nullable=False)
    options = Column(JSON, nullable=False)
    correct_answer = Column(String, nullable=False)
    created_by = Column(UUID, ForeignKey("users.user_id"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    creator = relationship("User", back_populates="created_mcqs")
    submissions = relationship(
        "UserSubmission", back_populates="mcq", cascade="all, delete-orphan"
    )
