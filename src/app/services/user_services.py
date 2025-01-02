from uuid import UUID

from fastapi.exceptions import HTTPException

from src.app.schemas.mcq_schemas import UserOutput
from src.app.services.unit_of_work import BaseUnitOfWork
from src.app.utils.model_to_dict import model_to_dict


def get(user_id: UUID, unit_of_work: BaseUnitOfWork) -> UserOutput:
    """
    Finds and returns a single user based on the UUID number

    Parameters
    ----------
    user_id: UUID
    unit_of_work: BaseUnitOfWork

    Returns
    -------

    """
    with unit_of_work:
        target_user = unit_of_work.user.get(user_id=user_id)
        if target_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        target_user_dict = UserOutput(**model_to_dict(target_user))

    return target_user_dict


def add(user, unit_of_work: BaseUnitOfWork):
    """
    adds user

    Parameters
    ----------
    user_id: UUID
    unit_of_work: BaseUnitOfWork

    Returns
    -------

    """
    with unit_of_work:
        unit_of_work.user.add(user=user)
        print("Added")
    return True


def get_all(unit_of_work: BaseUnitOfWork) -> dict:
    """
    Finds and returns a single user based on the UUID number

    Parameters
    ----------
    user_id: UUID
    unit_of_work: BaseUnitOfWork

    Returns
    -------

    """
    with unit_of_work:
        target_users = unit_of_work.user.get_all()

        if target_users is None:
            raise HTTPException(status_code=404, detail="User not found")

        target_users_object = [
            UserOutput(**model_to_dict(user)) for user in target_users
        ]

    return target_users_object
