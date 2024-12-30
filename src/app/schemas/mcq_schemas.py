from pydantic import BaseModel, UUID4
from datetime import datetime
from enum import Enum 

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class UserBase(BaseModel):
    username: str
    role: UserRole

class UserInput(UserBase):
    password: str

class UserOutput(UserBase):
    user_id: UUID4
    created_at: datetime

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
