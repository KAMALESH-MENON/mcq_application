from datetime import datetime
from enum import Enum

from pydantic import UUID4, BaseModel


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class UserLoginInput(BaseModel):
    username: str
    password: str


class UserLoginOutput(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    username: str
    role: UserRole


class UserRegisterInput(UserBase):
    password: str


class UserRegisterOutput(BaseModel):
    user_id: UUID4


class UserOutput(UserBase):
    user_id: UUID4


class Options(BaseModel):
    a: str
    b: str
    c: str
    d: str


class OptionEnum(str, Enum):
    a = "a"
    b = "b"
    c = "c"
    d = "d"


class TypeEnum(str, Enum):
    python = "python"
    java = "java"
    csharp = "c#"


class MCQBase(BaseModel):
    type: str
    question: str
    options: Options
    correct_answer: OptionEnum


class MCQCreate(MCQBase):
    created_by: UUID4


class MCQ(MCQBase):
    mcq_id: UUID4
    created_at: datetime


class SubmissionInput(BaseModel):
    user_id: UUID4
    mcq_id: UUID4
    user_answer: str
    is_correct: bool


class SubmissionOutput(SubmissionInput):
    pass


class UserHistory(BaseModel):
    user_id: UUID4
    total_score: float
    percentage: float
    total_attempts: int
    attempted_at: datetime
