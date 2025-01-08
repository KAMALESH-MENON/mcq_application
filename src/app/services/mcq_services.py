import random

import pandas as pd
from fastapi import HTTPException, UploadFile

from app.models.data_models import MCQ
from app.schemas.mcq_schemas import (
    MCQCreate,
    MCQCreateOutput,
    PaginatedResponse,
    UserOutput,
)
from app.services.unit_of_work import BaseUnitOfWork
from app.utils.model_to_dict import model_to_dict, pydantic_to_dict


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
            status_code=401, detail="Access denied. Admin role required."
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


def bulk_add_mcqs(
    unit_of_work: BaseUnitOfWork, file: UploadFile, current_user: UserOutput
) -> int:
    """
    Bulk adds MCQs from an uploaded file to the database.

    Args:
        unit_of_work (BaseUnitOfWork): The unit of work object that manages database transactions and repositories.
        file (UploadFile): Uploaded Excel file containing MCQ data.
        current_user (UserOutput): Current authenticated user.

    Returns:
        int: Count of MCQs successfully added.

    Raises:
        HTTPException: If the user is not an admin.
        HTTPException: The file format is invalid.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=401, detail="Access denied. Admin role required."
        )

    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400, detail="Invalid file format. Upload an Excel file."
        )

    try:
        df = pd.read_excel(file.file)
        added_count = 0
        with unit_of_work:
            for _, row in df.iterrows():
                mcq_data = {
                    "type": row.get("type"),
                    "question": row.get("question"),
                    "options": row.get("options"),
                    "correct_option": row.get("correct_answer"),
                    "created_by": current_user.user_id,
                }
                mcq = MCQ(**mcq_data)
                unit_of_work.mcq.add(mcq)
                added_count += 1

        return added_count

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


def get_all(
    unit_of_work: BaseUnitOfWork,
    type: str,
    page: int,
    page_size: int,
) -> dict:
    """
    Retrieve paginated MCQs with optional type filter and pagination.
    """
    with unit_of_work:
        mcqs = unit_of_work.mcq.get_all(type_=type)

        if mcqs is None:
            raise HTTPException(status_code=404, detail="User not found")

        mcqs_list_object = [(MCQCreate(**model_to_dict(mcq))) for mcq in mcqs]

        if not mcqs_list_object:
            raise HTTPException(
                status_code=404, detail="No MCQs found for the given type"
            )

        total_count = len(mcqs_list_object)
        total_pages = (total_count // page_size) + (
            1 if total_count % page_size > 0 else 0
        )

        start = (page - 1) * page_size
        end = start + page_size

        random.shuffle(mcqs_list_object)
        paginated_mcqs_list_object = mcqs_list_object[start:end]

        next_page = page + 1 if page < total_pages else None

        return PaginatedResponse(
            currentPage=page,
            totalPage=total_pages,
            nextPage=next_page,
            totalCount=total_count,
            data=paginated_mcqs_list_object,
        )
