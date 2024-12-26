import uuid
from enum import Enum as PyEnum
from sqlalchemy import (
    Column, String,
    TIMESTAMP, Enum, func)
from sqlalchemy.dialects.postgresql import UUID
from src.app.config.database import Base

class UserRole(PyEnum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default="user") 
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
