from typing import List
from uuid import UUID

from fastapi import APIRouter

from src.app.schemas.mcq_schemas import UserInput, UserOutput
from src.app.services import UserUnitOfWork, user_services

router = APIRouter(tags=["User"])


@router.get("/users/{user_id}", response_model=UserOutput)
def get_user(user_id: UUID) -> UserOutput:
    """
    Get user by user_id
    """
    return user_services.get(user_id=user_id, unit_of_work=UserUnitOfWork())


@router.post("/users", response_model=UserOutput)
def create_user(user: UserInput) -> UserOutput:
    """
    Add a new user
    """
    user_services.add(user, unit_of_work=UserUnitOfWork())
    return user


@router.get("/users", response_model=List[UserOutput])
def get_all_users() -> List[UserOutput]:
    """
    Get all users
    """
    return user_services.get_all(unit_of_work=UserUnitOfWork())
