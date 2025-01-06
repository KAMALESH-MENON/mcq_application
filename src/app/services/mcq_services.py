from fastapi.exceptions import HTTPException

from app.models.data_models import MCQ
from app.schemas.mcq_schemas import MCQCreate, MCQCreateOutput, UserOutput
from app.services.unit_of_work import BaseUnitOfWork


def fetch_mcq_types(unit_of_work: BaseUnitOfWork) -> list[str]:
    """
    Retrieve distinct MCQ types using Unit of Work.

    Args:
        unit_of_work (BaseUnitOfWork): UnitOfWork instance.

    Returns:
        list[str]: List of distinct MCQ types.
    """
    with unit_of_work:
        return unit_of_work.mcq.get_mcq_types()


def add_mcq(
    unit_of_work: BaseUnitOfWork, mcq: MCQCreate, current_user: UserOutput
) -> MCQCreateOutput:
    """
    Adds a new MCQ to the database. Only user with role as "admin" can create the mcq.

    Args:
        unit_of_work (BaseUnitOfWork): The unit of work object that manages database transactions and repositories.
        mcq (MCQCreate): MCQ schema
        current_user (UserOutput): The current authenticated user, used to check authorization.

    Returns:
        MCQCreateOutput: The output model containing the data of the newly created MCQ, including its ID.

    Raises:
        HTTPException: If the user's role is not "admin".
        HTTPException: If the provided MCQ type is not valid.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Access denied. Admin role required."
        )
    with unit_of_work:
        mcq_data = mcq.model_dump()
        mcq = MCQ(**mcq_data)
        existing_types = fetch_mcq_types(unit_of_work=unit_of_work)
        if mcq.type not in existing_types:
            raise HTTPException(status_code=400, detail="Invalid mcq type input.")
        unit_of_work.session.add(mcq)
        unit_of_work.session.flush()
        unit_of_work.session.refresh(mcq)
        return MCQCreateOutput(**mcq.__dict__)
